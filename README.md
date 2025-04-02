# Soccer Bot Project

A real-time soccer betting bot that monitors matches, compares odds, and generates alerts for specific events.

## Features

- **Live Odds and Markets**: Connects to WebSocket APIs for real-time updates on odds and market changes.
- **Pre-Match Stats and Odds**: Fetches pre-match data using HTTP APIs.
- **Alert System**: Generates alerts for specific events like goals, red cards, and other triggers.
- **Modular Design**: Separate modules for soccer-specific logic, shared utilities, and alert processing.
- **Logging**: Logs runtime information and errors for debugging and monitoring.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd my_bot_project
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

3. **WebSocket Connection**:
   - The application connects to a WebSocket API to receive live updates on odds and market changes.
   - Ensure the WebSocket server URL is configured in the `soccer/config.py` file.

4. **HTTP Connection**:
   - Pre-match stats and odds are fetched via HTTP APIs.
   - Configure the HTTP API endpoints and credentials in the `soccer/config.py` file.

## Project Structure

```
my_bot_project/
├── main.py                     # Main application orchestration file
├── README.md                   # Project overview and instructions
├── requirements.txt            # Project dependencies
├── common/                     # Shared modules across different sports
│   ├── __init__.py
│   ├── comparator.py           # Common logic for comparing pre-match odds with live data
│   ├── data_manager.py         # Manages in-memory data storage (live data, prematch odds)
│   └── scheduler.py            # Scheduling logic for periodic tasks (HTTP polling/WebSocket comparison)
├── config/                     # Global configuration settings
│   └── config.py               # Global settings (can import sport-specific configs)
├── logs/                       # Directory for log files
│   └── app.log                 # Log file for runtime information and errors
├── soccer/                     # Soccer-specific modules
│   ├── __init__.py
│   ├── config.py               # Soccer-specific configurations (API endpoints, credentials, thresholds)
│   ├── http_client.py          # Functions for fetching pre-match odds and static data via HTTP
│   ├── models.py               # Data models for soccer matches, odds, live events, and alerts
│   ├── utils.py                # Utility functions (data parsing, formatting, conversions)
│   ├── websocket_client.py     # Functions for handling WebSocket connection for live updates
│   └── alerts/                 # Soccer alert triggers and alert engine
│       ├── __init__.py
│       ├── alert_engine.py     # Main alert engine logic to coordinate alert processing
│       ├── goal_alert.py       # Alert trigger for goal events
│       ├── redcard_alert.py    # Alert trigger for red card events
│       └── other_alerts.py     # Additional alert triggers
└── tests/                      # Unit and integration tests
    ├── __init__.py
    ├── test_alerts.py          # Tests for alert triggers and engine
    ├── test_comparator.py      # Tests for comparison logic in common modules
    ├── test_http_client.py     # Tests for soccer HTTP client
    └── test_websocket_client.py# Tests for soccer WebSocket client
```

This structure includes the main application file (`main.py`), configuration files, modules for handling WebSocket and HTTP connections, and test files for unit and integration testing.

## Dependencies

- Flask==2.2.3
- Flask-SocketIO==5.3.3
- eventlet==0.33.0
- requests==2.31.0
- websockets==10.4
- python-dotenv==1.0.0
- APScheduler==3.9.1
- aiohttp==3.8.5
- pytest==7.4.0
- schedule==1.2.0

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## Development Environment

- Hosted on DigitalOcean
- Python virtual environment
- Requirements managed via requirements.txt

## Troubleshooting

- **WebSocket Connection Issues**:
  - Ensure the WebSocket server is running and accessible.
  - Verify the WebSocket URL and credentials in `soccer/config.py`.

- **HTTP Connection Issues**:
  - Check the API endpoints and credentials in `soccer/config.py`.

- **Dependency Issues**:
  - Reinstall dependencies using:
    ```bash
    pip install -r requirements.txt
    ```

## Recent Updates and Enhancements

### WebSocket Integration
- Configured the WebSocket client to connect to `mq.thesports.com` using the MQTT protocol over WebSockets.
- Subscribed to the Football topic (`sports/football`) and Tennis topic (`sports/tennis`) as per the account's subscription.
- Enabled secure WebSocket connections with TLS using `client.tls_set()`.
- Set the WebSocket path to `/mqtt` using `client.ws_set_options(path="/mqtt")`.
- Successfully connected to the WebSocket server and processed real-time sports data.

### Flask Application Setup
- Created a Flask application to serve the URL `https://livesportsalerts.io`.
- Integrated Flask-SocketIO to broadcast real-time WebSocket data to connected clients.
- Configured the Flask application to run on port 5000.
- Added a new `widgets.py` file under the `soccer` directory to serve an HTML page with an embedded sports widget.

### Nginx Configuration
- Configured Nginx as a reverse proxy to forward requests from `https://livesportsalerts.io` to the Flask application running on `http://127.0.0.1:5000`.
- Redirected all HTTP traffic (port 80) to HTTPS (port 443).
- Applied SSL/TLS certificates using Let's Encrypt for secure connections.
- Verified and tested the Nginx configuration to ensure seamless integration.

### Widget Integration
- Embedded a sports widget on the front page of `https://livesportsalerts.io` using the provided embed script.
- Updated the `widgets.py` file with the correct `profile_id`, `widget_id`, and `competition_ids`.
- Added a route to serve a `favicon.ico` file to resolve missing favicon errors.

### Troubleshooting and Fixes
- Resolved WebSocket handshake errors by ensuring the correct WebSocket path and secure connection settings.
- Fixed Nginx configuration issues to properly forward requests to the Flask application.
- Addressed module import errors by installing missing dependencies (`Flask`, `Flask-SocketIO`, etc.).
- Verified the Flask application and WebSocket client functionality through extensive testing.

### Final Outcome
- The application is now live at `https://livesportsalerts.io`.
- Real-time sports data is successfully fetched via WebSockets and displayed on the site.
- The sports widget is embedded and functional on the front page.
- The setup is secure, scalable, and ready for production use.

## Virtual Environment Setup

A virtual environment is used for this project to manage dependencies. It is located in the `venv/` directory.

### Activating the Virtual Environment

Before running the project, activate the virtual environment:

```bash
source venv/bin/activate
```

Alternatively, the `main.py` script automatically activates the virtual environment when executed.

### Updated Virtual Environment Setup

If the virtual environment is not already set up, follow these steps:

1. **Create the Virtual Environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install paho-mqtt
   ```

These steps ensure that the required dependencies are installed and the environment is ready for running the application.

### Recent Updates

- **WebSocket Client Enhancements**:
  - Updated the `main.py` script to ensure proper handling of the virtual environment and corrected the import path for the WebSocket client.
  - Verified and tested the WebSocket connection to ensure logs are displayed in the terminal.
  - Added debug logging to capture connection status and received messages.

These updates ensure that the WebSocket client connects seamlessly and provides real-time feedback in the terminal.

### Note

- The project terminology has been updated to reflect "football" instead of "soccer." All references to "soccer" in the codebase and documentation should now be understood as "football."
