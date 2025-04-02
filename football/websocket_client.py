import asyncio
import json
import logging
import paho.mqtt.client as mqtt
from football.config import WEBSOCKET_DOMAIN, API_USER, API_SECRET, FOOTBALL_TOPIC

# Configure logger
logger = logging.getLogger("WebSocketClient")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class WebSocketClient:
    def __init__(self, uri):
        self.client = mqtt.Client(transport="websockets")
        self.client.ws_set_options(path="/mqtt")  # Set the WebSocket path
        self.client.tls_set()  # Enable TLS for secure connection
        self.client.username_pw_set(username=API_USER, password=API_SECRET)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.uri = uri  # Store the URI for connection
        self.heartbeat_interval = 30  # seconds
        self.heartbeat_task = None

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("✅ Connected to WebSocket server at %s.", WEBSOCKET_DOMAIN)
            client.subscribe(FOOTBALL_TOPIC)  # Subscribe to Football topic only
        elif rc in [4, 5]:
            logger.error("❌ Authentication failed. Check username, key, and IP whitelist.")

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            logger.info("Received message on topic '%s': %s", msg.topic, payload)
        except Exception as e:
            logger.error("Error parsing message: %s", e)

    def send_message(self, topic, message):
        """Send a message to the WebSocket server (synchronously)."""
        self.client.publish(topic, message)
        logger.info("📤 Message sent to topic '%s': %s", topic, message)

    async def start_heartbeat(self):
        while True:
            self.client.publish("heartbeat", "ping")
            logger.info("Heartbeat sent to keep the connection alive.")
            await asyncio.sleep(self.heartbeat_interval)

    async def connect(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.client.connect, WEBSOCKET_DOMAIN, 443)
        self.client.loop_start()
        # Start the asynchronous heartbeat task
        self.heartbeat_task = asyncio.create_task(self.start_heartbeat())

    async def close(self):
        """Gracefully close the WebSocket connection."""
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("🔒 WebSocket connection closed.")

    async def reconnect(self):
        logger.info("🔄 Reconnecting to WebSocket server...")
        await self.close()
        await self.connect()
        logger.info("✅ Reconnected to WebSocket server.")

    async def receive_messages(self, message_limit=5):
        """Receive a limited number of messages from the WebSocket server."""
        messages = []
        message_event = asyncio.Event()
        original_on_message = self.client.on_message

        def temporary_on_message(client, userdata, msg):
            messages.append(msg.payload.decode())
            if len(messages) >= message_limit:
                message_event.set()
            # Call the original callback for logging/processing
            original_on_message(client, userdata, msg)

        self.client.on_message = temporary_on_message

        logger.info("Waiting to receive %d messages...", message_limit)
        try:
            await message_event.wait()
        except asyncio.CancelledError:
            logger.info("Message waiting was cancelled.")
        finally:
            # Restore the original on_message callback
            self.client.on_message = original_on_message

        logger.info("Received %d messages.", len(messages))
        return messages

    def is_connected(self):
        """Check if the WebSocket client is connected."""
        return self.client.is_connected()
