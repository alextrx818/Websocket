import sys
import os
import subprocess
import asyncio
import logging

# --- Virtual Environment Check & Relaunch ---
if sys.prefix == sys.base_prefix:
    # Not running inside a virtual environment, so relaunch using the venv interpreter.
    venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'bin', 'python')
    if not os.path.exists(venv_python):
        print("Virtual environment not found. Please set it up first.")
        sys.exit(1)
    print("Not running in virtual environment. Relaunching...")
    subprocess.check_call([venv_python] + sys.argv)
    sys.exit()

# --- Logging Setup ---
logging.basicConfig(
    level=logging.DEBUG,  # Capture all log messages
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.info("Starting the application...")

# --- Import WebSocket Client ---
# Attempt to import from the 'football' module first.
try:
    from football.websocket_client import WebSocketClient
except ModuleNotFoundError:
    # Fallback to 'soccer' if the 'football' module isn't found.
    from soccer.websocket_client import WebSocketClient
    logger.warning("Module 'football' not found. Using 'soccer' module instead.")

# SOCKET_URI with the provided domain and credentials.
SOCKET_URI = "wss://mq.thesports.com:443?user=thenecpt&secret=0c55322e8e196d6ef9066fa4252cf386"

async def run():
    logger.info("🔌 Starting WebSocket connection test...")
    client = WebSocketClient(SOCKET_URI)

    try:
        # Connect to the WebSocket server.
        await client.connect()
        logger.info("✅ Connected to WebSocket server.")

        # Send a ping message (send_message is synchronous).
        client.send_message("heartbeat", "ping")
        logger.info("✅ Ping message sent.")

        # Wait a few seconds, then force a reconnect.
        await asyncio.sleep(5)
        logger.info("🔄 Attempting to reconnect to WebSocket server...")
        await client.reconnect()
        logger.info("✅ Reconnected to WebSocket server.")

        # Send another ping after reconnection.
        client.send_message("heartbeat", "ping")
        logger.info("✅ Second ping message sent. Waiting for messages...")

        # Wait to receive messages.
        logger.info("📡 Waiting to receive messages...")
        messages = await client.receive_messages(message_limit=5)

        if messages:
            logger.info("\n✅ Received messages:")
            for i, msg in enumerate(messages, 1):
                logger.info(f"[{i}] {msg}")
        else:
            logger.warning("⚠️ No messages received.")

    except Exception as e:
        logger.error(f"❌ Error during WebSocket test: {e}")

    finally:
        await client.close()
        logger.info("🔒 Connection closed.")

if __name__ == "__main__":
    asyncio.run(run())
