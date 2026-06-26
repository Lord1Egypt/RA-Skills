# Output Format Examples

## Service Start (Default - Background Mode)

```
╔════════════════════════════════════════════╗
║   Starting Chrome Remote Access Service    ║
╚════════════════════════════════════════════╝

• Checking dependencies...
• Checking port availability...
• Cleaning up old processes...
• Starting virtual display Xvfb :99 (1600x1200)...
  ✓ Xvfb started successfully
• Starting x11vnc (port 5900)...
  ✓ x11vnc started successfully
• Starting noVNC (port 6080)...
  ✓ noVNC started successfully
• Starting chromium...
  ✓ chromium started successfully

═════════════════════════════════════════════
          ✓ Service Started Successfully!
═════════════════════════════════════════════

📱 Remote Access URL (Recommended):
   http://10.37.225.235:6080/vnc.html?host=10.37.225.235&port=6080&password=03db4624014d&autoconnect=true

💻 Or connect via VNC client:
   10.37.225.235:5900 (Password: 03db4624014d)

🔑 VNC Password: 03db4624014d

Note: Service is running in background. Use ./status-remote-chrome.sh to check status
      Use ./stop-remote-chrome.sh to stop the service
```

## Service Start (With Proxy)

```
╔════════════════════════════════════════════╗
║   Starting Chrome Remote Access Service    ║
╚════════════════════════════════════════════╝

• Checking dependencies...
• Checking port availability...
• Cleaning up old processes...
• Starting virtual display Xvfb :99 (1600x1200)...
  ✓ Xvfb started successfully
• Starting x11vnc (port 5900)...
  ✓ x11vnc started successfully
• Starting noVNC (port 6080)...
  ✓ noVNC started successfully
• Starting chromium (using proxy: http://proxy.example.com:8080)...
  ✓ chromium started successfully

═════════════════════════════════════════════
          ✓ Service Started Successfully!
═════════════════════════════════════════════

📱 Remote Access URL (Recommended):
   http://10.37.225.235:6080/vnc.html?host=10.37.225.235&port=6080&password=03db4624014d&autoconnect=true

💻 Or connect via VNC client:
   10.37.225.235:5900 (Password: 03db4624014d)

🔑 VNC Password: 03db4624014d

Note: Service is running in background. Use ./status-remote-chrome.sh to check status
      Use ./stop-remote-chrome.sh to stop the service
```

## Service Start (Foreground Mode with -f)

```
[Same output as above, but:]

Note: Press Ctrl+C to stop all services

[Script keeps running and monitors processes]
```

## Service Start (Verbose Mode with -v)

```
[Includes all above, plus:]

📊 Process Information:
   Xvfb:    643126
   x11vnc:  643165
   noVNC:   643194
   Chrome:  643203

⚙️  Configuration:
   Resolution: 1600x1200
   Proxy:      http://proxy.example.com:8080
   Bypass:     localhost,*.example.com

Note: Service is running in background. Use ./status-remote-chrome.sh to check status
      Use ./stop-remote-chrome.sh to stop the service
```

## Status Check (Running)

```
╔════════════════════════════════════════════╗
║   Remote Chrome Service Status Monitor     ║
╚════════════════════════════════════════════╝

📊 Service Status: Running

Process Information:
  ✓ Xvfb (PID: 643126) - Memory: 93.8 MB
  ✓ x11vnc (PID: 643165) - Memory: 11.3 MB
  ✓ noVNC/websockify (PID: 643194) - Memory: 36.6 MB
  ✓ Chrome (PID: 643203) - Memory: 262.0 MB
    → Total Chrome processes memory: 864.3 MB

Ports and Addresses:
  ✓ VNC: 0.0.0.0:5900
  ✓ noVNC: 0.0.0.0:6080
  ✓ Chrome Debug: 127.0.0.1:9222

═════════════════════════════════════════════
          Access Information
═════════════════════════════════════════════

📱 Web Access URL (Recommended):
   http://10.37.225.235:6080/vnc.html?host=10.37.225.235&port=6080&password=03db4624014d&autoconnect=true

💻 VNC Client Connection:
   10.37.225.235:5900 (Password: 03db4624014d)

🔑 VNC Password: 03db4624014d

🔧 Chrome Remote Debugging:
   http://10.37.225.235:9222

📑 Chrome Tabs:
  Total 2 tabs

  • Search Developer Platform
    https://search.example.com/open/home?target_channel=tt_...
  • New Tab
    chrome://newtab/

Command Help:
   ./start-remote-chrome.sh    Start service
   ./stop-remote-chrome.sh     Stop service
   ./status-remote-chrome.sh   View status
```

## Status Check (Not Running)

```
╔════════════════════════════════════════════╗
║   Remote Chrome Service Status Monitor     ║
╚════════════════════════════════════════════╝

📊 Service Status: Not Running

To start the service, run:
   ./start-remote-chrome.sh

Command Help:
   ./start-remote-chrome.sh    Start service
   ./stop-remote-chrome.sh     Stop service
   ./status-remote-chrome.sh   View status
```

## Service Stop

```
Stopping Chrome Remote Access Service...

Currently running processes:
  Xvfb:    643126
  x11vnc:  643165
  websockify: 643194
  643930

Stopping services...
✓ x11vnc stopped
✓ websockify stopped
✓ Xvfb stopped

✓ Service stopped

Checking port status:
✓ Port 5900 released
✓ Port 6080 released
```

## Missing Dependencies

```
╔════════════════════════════════════════════╗
║   Starting Chrome Remote Access Service    ║
╚════════════════════════════════════════════╝

• Checking dependencies...

✗ Error: Missing required dependencies

The following dependencies are not installed:
  ✗ Xvfb (Virtual X Server)
  ✗ x11vnc (VNC Server)
  ✗ noVNC (Web VNC Client)

Installation commands:
  sudo apt-get install xvfb
  sudo apt-get install x11vnc
  sudo apt-get install novnc websockify

Note: After installing dependencies, re-run this script to start the service
```

## Port Already in Use

```
• Checking dependencies...
• Checking port availability...
✗ Error: Port 5900 (VNC) is already in use
Please run ./stop-remote-chrome.sh first, or modify the port number in the script
```

## Help Information

```
Usage: ./start-remote-chrome.sh [OPTIONS]

Options:
  -v, --verbose           Enable verbose logging
  -f, --foreground        Run in foreground mode (default: background)
  --proxy <url>           Set HTTP/HTTPS proxy server
  --proxy-bypass <list>   Set proxy bypass list (comma-separated)
  -h, --help              Display help information

Examples:
  ./start-remote-chrome.sh --proxy http://proxy.example.com:8080
  ./start-remote-chrome.sh --proxy http://proxy.example.com:8080 --proxy-bypass 'localhost,*.example.com'
  ./start-remote-chrome.sh -v -f
```
