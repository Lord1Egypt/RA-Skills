# Configuration Reference

## Script Parameters

These parameters can be configured via command-line options or modified in the `start-remote-chrome.sh` script:

```bash
# Display and Ports
DISPLAY_NUM=99              # Virtual display number
VNC_PORT=5900              # VNC server port (configurable via --vnc-port)
NOVNC_PORT=6080            # noVNC web access port (configurable via --novnc-port)
CHROME_DEBUG_PORT=9222     # Chrome remote debugging port (configurable via --chrome-debug-port)

# Display Settings
SCREEN_SIZE="1600x1200x24" # Resolution (width x height x color depth) - configurable via --screen-size

# Browser
CHROME_BIN="chromium"      # Browser binary (chromium, chromium-browser, google-chrome-stable, google-chrome)
```

## Command Line Options

### start-remote-chrome.sh

```bash
./start-remote-chrome.sh [OPTIONS]

Options:
  -v, --verbose                Enable verbose logging (show Chrome output, process details)
  -f, --foreground             Run in foreground mode (keeps script running, Ctrl+C to stop)
  --vnc-port <port>            VNC server port (default: 5900)
  --novnc-port <port>          noVNC web access port (default: 6080)
  --chrome-debug-port <port>   Chrome remote debugging port (default: 9222)
  --screen-size <WxHxD>        Screen resolution (default: 1600x1200x24)
  --proxy <url>                Set HTTP/HTTPS proxy server
  --proxy-bypass <list>        Set proxy bypass list (comma-separated)
  -h, --help                   Display help information

Default behavior:
- Runs in background mode (script exits after starting services)
- Shows only essential information (URLs, password)
- Suppresses Chrome and service logs
- No proxy configured by default (direct connection)
- Uses default ports: 5900 (VNC), 6080 (noVNC), 9222 (Chrome Debug)
- Uses default screen resolution: 1600x1200x24
```

### Port Configuration

All port numbers can be customized via command-line parameters:

```bash
# Use different ports to avoid conflicts
./start-remote-chrome.sh --vnc-port 5901 --novnc-port 6081 --chrome-debug-port 9223

# Use non-standard ports
./start-remote-chrome.sh --vnc-port 15900 --novnc-port 16080 --chrome-debug-port 19222
```

**Note:** When using custom ports, you must specify the same ports when running the status script:

```bash
./status-remote-chrome.sh --vnc-port 5901 --novnc-port 6081 --chrome-debug-port 9223
```

### Screen Resolution Configuration

The screen resolution can be set using the format `WidthxHeightxColorDepth`:

```bash
# Full HD (1920x1080)
./start-remote-chrome.sh --screen-size 1920x1080x24

# 4K resolution
./start-remote-chrome.sh --screen-size 3840x2160x24

# Custom resolution with different color depth
./start-remote-chrome.sh --screen-size 2560x1440x32

# Common resolutions:
# - 1600x1200 (4:3 aspect ratio, default)
# - 1920x1080 (Full HD, 16:9)
# - 2560x1440 (QHD, 16:9)
# - 3840x2160 (4K, 16:9)
```

The color depth can be:
- 24: 24-bit color (16.7 million colors) - recommended for most uses
- 32: 32-bit color (includes alpha channel) - for applications requiring transparency

### Proxy Configuration

#### Command-line Proxy

```bash
# Set proxy server
./start-remote-chrome.sh --proxy http://proxy.example.com:8080

# Set proxy with bypass list
./start-remote-chrome.sh --proxy http://proxy.example.com:8080 --proxy-bypass "localhost,127.0.0.1,*.example.com"

# Combine with other options
./start-remote-chrome.sh --proxy http://proxy.example.com:8080 -v
```

#### Environment Variables

The script also respects standard proxy environment variables:

```bash
# Set environment variables before running
export http_proxy="http://proxy.example.com:8080"
export https_proxy="http://proxy.example.com:8080"
export no_proxy="localhost,127.0.0.1,*.example.com"

./start-remote-chrome.sh
```

#### Priority Order

1. Command-line parameters (`--proxy`, `--proxy-bypass`)
2. Environment variables (`http_proxy`, `https_proxy`, `no_proxy`)
3. No proxy (direct connection)

### stop-remote-chrome.sh

```bash
./stop-remote-chrome.sh

No options. Stops all services and cleans up processes and password files.
```

### status-remote-chrome.sh

```bash
./status-remote-chrome.sh [OPTIONS]

Options:
  --vnc-port <port>            VNC server port (default: 5900)
  --novnc-port <port>          noVNC web access port (default: 6080)
  --chrome-debug-port <port>   Chrome remote debugging port (default: 9222)
  -h, --help                   Display help information

Displays comprehensive status information including:
- Process status and memory usage
- Port listening status
- Chrome tab information (requires jq for detailed view)
- VNC password and access URLs

Note: Port options must match the ports used when starting the service.
```

## Combining Multiple Options

You can combine multiple configuration options:

```bash
# Custom ports + custom resolution + proxy
./start-remote-chrome.sh \
  --vnc-port 5901 \
  --novnc-port 6081 \
  --chrome-debug-port 9223 \
  --screen-size 1920x1080x24 \
  --proxy http://proxy.example.com:8080 \
  --proxy-bypass "localhost,*.example.com" \
  -v

# Check status with matching ports
./status-remote-chrome.sh \
  --vnc-port 5901 \
  --novnc-port 6081 \
  --chrome-debug-port 9223
```

## File Locations

### Password Storage
- **Location**: `/tmp/remote-chrome-vnc-password.txt`
- **Permissions**: `600` (owner read/write only)
- **Lifecycle**: Created on start, deleted on stop
- **Purpose**: Allows status script to retrieve VNC password

### Logs
- **x11vnc log**: `/tmp/x11vnc.log`
- **Chrome output**: Suppressed by default (use `-v` to see)

## Network Configuration

### Ports
- **5900** (VNC): Raw VNC access - use with VNC clients
- **6080** (noVNC): Web-based VNC - access via browser
- **9222** (Chrome DevTools): Remote debugging protocol

### Firewall
If accessing from another machine, ensure firewall allows these ports:

```bash
# UFW (Ubuntu)
sudo ufw allow 5900/tcp
sudo ufw allow 6080/tcp
sudo ufw allow 9222/tcp

# firewalld (CentOS/RHEL)
sudo firewall-cmd --add-port=5900/tcp --permanent
sudo firewall-cmd --add-port=6080/tcp --permanent
sudo firewall-cmd --add-port=9222/tcp --permanent
sudo firewall-cmd --reload
```

### Access URLs

**Web Access (Recommended)**:
```
http://<HOST_IP>:6080/vnc.html?host=<HOST_IP>&port=6080&password=<PASSWORD>&autoconnect=true
```

**VNC Client Access**:
```
Address: <HOST_IP>:5900
Password: <PASSWORD>
```

**Chrome DevTools**:
```
http://<HOST_IP>:9222
```

## Memory Requirements

Typical memory usage:
- **Xvfb**: ~90-100 MB
- **x11vnc**: ~10-30 MB
- **noVNC/websockify**: ~30-40 MB
- **Chrome (main)**: ~250-350 MB
- **Chrome (all processes)**: ~800 MB - 1.5 GB (varies with tabs)

**Recommended minimum**: 2 GB RAM

## Integration with agent-browser

The Chrome instance can be controlled programmatically via the `agent-browser` skill:

```bash
# Start remote Chrome first
./start-remote-chrome.sh

# Connect with agent-browser
agent-browser connect --url http://localhost:9222

# Navigate
agent-browser open https://example.com
```

See `references/agent-browser-integration.md` for details.

## Troubleshooting

### Port Already in Use
```
✗ Error: Port 5900 (VNC) is already in use
```
**Solution**: Run `./stop-remote-chrome.sh` or change port numbers in the script.

### Missing Dependencies
```
✗ Error: Missing required dependencies
```
**Solution**: See `references/installation.md` for installation commands.

### Chrome Doesn't Start
- Check if Chrome/Chromium is installed
- Verify DISPLAY environment variable is set correctly
- Check system memory availability
- Use `-v` flag for detailed output

### NoVNC Not Accessible
- Verify port 6080 is not blocked by firewall
- Check if websockify is running (`pgrep -f websockify`)
- Ensure noVNC files are installed in `/usr/share/novnc/`

### Cannot Retrieve VNC Password
- Check if `/tmp/remote-chrome-vnc-password.txt` exists
- Verify file permissions
- Restart the service to regenerate password file

### Proxy Issues
- Verify proxy URL format: `http://host:port` or `https://host:port`
- Check if proxy server is accessible
- Test with `curl --proxy http://proxy.example.com:8080 http://example.com`
- Use `--proxy-bypass` for internal sites that shouldn't go through proxy
