---
name: remote-chrome
description: Launch, stop, restart, or check the status of a remote Chrome browser service using Xvfb, x11vnc, and noVNC. Use this whenever the user wants to start a headless Chrome browser accessible via web browser or VNC client, needs to stop the remote browser service, wants to restart the service, or asks for the current status/access URL of the remote browser. This is for running a full Chrome browser remotely with GUI access through a web interface. 
---

# Open Remote Chrome Browser Management

Launch and manage a remote Chrome browser with web-based VNC access 

## Quick Start

```bash
# Start service (auto-checks dependencies)
./start-remote-chrome.sh

# Check status and get access info
./status-remote-chrome.sh

# Stop service
./stop-remote-chrome.sh
```

That's it! The start script automatically checks dependencies and provides clear installation instructions if anything is missing.

## What You Get

- **Web Access**: Browser-based VNC client at `http://<IP>:6080`
- **VNC Access**: Direct VNC connection at `<IP>:5900`
- **Remote Debugging**: Chrome DevTools at `http://<IP>:9222`
- **Status Monitoring**: Process info, memory usage, open tabs, VNC password

## Scripts

| Script | Purpose |
|--------|---------|
| `start-remote-chrome.sh` | Start the service (with auto dependency check) |
| `stop-remote-chrome.sh` | Stop the service |
| `status-remote-chrome.sh` | Monitor status, memory, tabs, and get access info |

## Options

```bash
# Verbose mode (see Chrome output and process details)
./start-remote-chrome.sh -v

# Foreground mode (keep script running, Ctrl+C to stop)
./start-remote-chrome.sh -f

# Custom ports
./start-remote-chrome.sh --vnc-port 5901 --novnc-port 6081 --chrome-debug-port 9223

# Custom screen resolution
./start-remote-chrome.sh --screen-size 1920x1080x24

# With proxy and bypass list
./start-remote-chrome.sh --proxy http://proxy.example.com:8080 --proxy-bypass "localhost,127.0.0.1,*.example.com"

# Combined options
./start-remote-chrome.sh --screen-size 1920x1080x24 --vnc-port 5901 --novnc-port 6081 -v

# Get help
./start-remote-chrome.sh -h
```

## Configuration Parameters

The start script supports the following configurable parameters:

### Port Configuration

- `--vnc-port <port>`: VNC server port (default: 5900)
- `--novnc-port <port>`: noVNC web access port (default: 6080)
- `--chrome-debug-port <port>`: Chrome remote debugging port (default: 9222)

**Example:**
```bash
# Use different ports to avoid conflicts
./start-remote-chrome.sh --vnc-port 5901 --novnc-port 6081
```

### Screen Resolution

- `--screen-size <WxHxD>`: Screen resolution in format `WidthxHeightxColorDepth` (default: 1600x1200x24)

**Examples:**
```bash
# Full HD resolution with 24 color depth
./start-remote-chrome.sh --screen-size 1920x1080x24
```


### Examples

```bash
# Use corporate proxy
./start-remote-chrome.sh --proxy http://proxy.company.com:3128

# Use proxy with bypass list for internal sites
./start-remote-chrome.sh --proxy http://proxy.company.com:3128 --proxy-bypass "*.internal.com,localhost,10.*"

# No proxy (direct connection - default behavior)
./start-remote-chrome.sh
```

### Proxy Environment Variables

The script also respects standard proxy environment variables if set:
- `HTTP_PROXY` / `http_proxy`
- `HTTPS_PROXY` / `https_proxy`
- `NO_PROXY` / `no_proxy`

Priority: Command-line parameters > Environment variables > No proxy

## Common Tasks

### Start Service
```bash
./start-remote-chrome.sh
```
Output includes access URLs and VNC password.

### Check Status
```bash
./status-remote-chrome.sh
```
Shows: process status, memory usage, open Chrome tabs, VNC password, access URLs.

### Restart Service
```bash
./stop-remote-chrome.sh && ./start-remote-chrome.sh
```

## Integration with agent-browser

Control Chrome programmatically via the `agent-browser` skill:

```bash
# 1. Start remote Chrome (with debugging port enabled)
./start-remote-chrome.sh

# 2. Connect agent-browser to Chrome
agent-browser connect --url http://localhost:9222

# 3. Navigate and interact
agent-browser open https://example.com
agent-browser click "#button-id"
agent-browser type "#input-field" "text content"

# 4. Check open tabs
./status-remote-chrome.sh  # Shows all tabs opened by agent-browser
```

**Benefits**:
- Visual monitoring via VNC + programmatic control via agent-browser
- Use agent-browser for automation, VNC for visual verification
- Debug automation scripts in real-time through web interface

## References

For detailed information, see:
- **[Installation Guide](references/installation.md)** - Dependencies and installation commands
- **[Output Examples](references/output-examples.md)** - Sample output for all operations
- **[Configuration](references/configuration.md)** - Script parameters, ports, troubleshooting

## Need Help?

- Missing dependencies? The start script will tell you exactly what to install.
- Port conflicts? Run `./stop-remote-chrome.sh` first.
- Want details? Check the `references/` folder for comprehensive documentation.
