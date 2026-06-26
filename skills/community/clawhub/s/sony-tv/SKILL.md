---
name: sony-tv
description: Control Sony Bravia TV via IP Control protocol. Send IRCC remote commands, open URLs in TV browser, kill apps, and run diagnostics. Use when controlling a Sony TV on the local network.
version: 2.0.0
source: local-development
---

# Sony TV Control

Control a Sony Bravia TV over the local network using IP Control (IRCC-IP + REST API). **No server required** — all commands are direct HTTP calls to the TV.

## Configuration

- **TV IP**: `192.168.50.120`
- **PSK (Pre-Shared Key)**: `19890801`
- **TV Model**: KD-55X9500G (BRAVIA 4K)
- **Browser**: Chrome 77.0.3865.116 (WebAppRuntime 2.1.2+10)

## Quick Reference

All commands go directly to `http://192.168.50.120`. No intermediate server needed.

### IRCC Commands (Remote Control Buttons)

IRCC commands use SOAP over POST to `/sony/ircc`. Common IRCC codes:

| Command | IRCC Code |
|---------|-----------|
| Power On | `AAAAAQAAAAEAAAAuAw==` |
| Power Off | `AAAAAQAAAAEAAAAvAw==` |
| Toggle Power | `AAAAAQAAAAEAAAAVAw==` |
| Volume Up | `AAAAAQAAAAEAAAASAw==` |
| Volume Down | `AAAAAQAAAAEAAAATAw==` |
| Mute | `AAAAAQAAAAEAAAAUAw==` |
| Channel Up | `AAAAAQAAAAEAAAAQAw==` |
| Channel Down | `AAAAAQAAAAEAAAARAw==` |
| D-Pad Up | `AAAAAQAAAAEAAAB0Aw==` |
| D-Pad Down | `AAAAAQAAAAEAAAB1Aw==` |
| D-Pad Left | `AAAAAQAAAAEAAAA0Aw==` |
| D-Pad Right | `AAAAAQAAAAEAAAAzAw==` |
| Confirm/OK | `AAAAAQAAAAEAAABlAw==` |
| Home | `AAAAAQAAAAEAAABgAw==` |
| Exit | `AAAAAQAAAAEAAABjAw==` |
| Options | `AAAAAgAAAJcAAAA2Aw==` |
| Back | `AAAAAgAAAJcAAAAjAw==` |
| Play | `AAAAAgAAAJcAAAAaAw==` |
| Pause | `AAAAAgAAAJcAAAAZAw==` |
| Stop | `AAAAAgAAAJcAAAAYAw==` |
| Rewind | `AAAAAgAAAJcAAAAbAw==` |
| Forward | `AAAAAgAAAJcAAAAcAw==` |
| HDMI 1 | `AAAAAgAAABoAAABaAw==` |
| HDMI 2 | `AAAAAgAAABoAAABbAw==` |
| HDMI 3 | `AAAAAgAAABoAAABcAw==` |
| HDMI 4 | `AAAAAgAAABoAAABdAw==` |

Send any IRCC command:

```bash
TV="192.168.50.120"
PSK="19890801"
CODE="AAAAAQAAAAEAAAASAw=="  # Volume Up

curl -s -X POST "http://$TV/sony/ircc" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPACTION: "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"' \
  -H "X-Auth-PSK: $PSK" \
  -d "<?xml version=\"1.0\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"><IRCCCode>$CODE</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>"
```

### Power Control

```bash
# Power On
curl -s -X POST "http://192.168.50.120/sony/ircc" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPACTION: "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"' \
  -H "X-Auth-PSK: 19890801" \
  -d '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCCode>AAAAAQAAAAEAAAAuAw==</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'

# Power Off
curl -s -X POST "http://192.168.50.120/sony/ircc" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPACTION: "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"' \
  -H "X-Auth-PSK: 19890801" \
  -d '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCCode>AAAAAQAAAAEAAAAvAw==</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'
```

### Open URL in TV Browser

Launches a URL in the TV's built-in Chrome browser via `localapp://webappruntime`:

```bash
curl -s -X POST "http://192.168.50.120/sony/appControl" \
  -H "Content-Type: application/json" \
  -H "X-Auth-PSK: 19890801" \
  -d '{"method":"setActiveApp","params":[{"uri":"localapp://webappruntime?url=http://192.168.50.170:3000/diag.html","data":""}],"id":1,"version":"1.0"}'
```

### Kill All Apps (Close Browser)

Terminates all running apps on the TV (closes browser, stops web apps):

```bash
curl -s -X POST "http://192.168.50.120/sony/appControl" \
  -H "Content-Type: application/json" \
  -H "X-Auth-PSK: 19890801" \
  -d '{"method":"terminateApps","params":[],"id":1,"version":"1.0"}'
```

### Get Status

```bash
# Get volume
curl -s -X POST "http://192.168.50.120/sony/audio" \
  -H "Content-Type: application/json" \
  -H "X-Auth-PSK: 19890801" \
  -d '{"method":"getVolumeInformation","params":[{"target":"speaker"}],"id":1,"version":"1.0"}'

# Get power status
curl -s -X POST "http://192.168.50.120/sony/system" \
  -H "Content-Type: application/json" \
  -H "X-Auth-PSK: 19890801" \
  -d '{"method":"getPowerStatus","params":[],"id":1,"version":"1.0"}'
```

## Helper Script

For convenience, create a shell wrapper:

```bash
#!/bin/bash
# tv.sh - Sony TV control helper
TV="192.168.50.120"
PSK="19890801"

ircc() {
  curl -s -X POST "http://$TV/sony/ircc" \
    -H "Content-Type: text/xml; charset=utf-8" \
    -H 'SOAPACTION: "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"' \
    -H "X-Auth-PSK: $PSK" \
    -d "<?xml version=\"1.0\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"><IRCCCode>$1</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>"
}

case "$1" in
  power-on)    ircc "AAAAAQAAAAEAAAAuAw==" ;;
  power-off)   ircc "AAAAAQAAAAEAAAAvAw==" ;;
  vol-up)      ircc "AAAAAQAAAAEAAAASAw==" ;;
  vol-down)    ircc "AAAAAQAAAAEAAAATAw==" ;;
  mute)        ircc "AAAAAQAAAAEAAAAUAw==" ;;
  up)          ircc "AAAAAQAAAAEAAAB0Aw==" ;;
  down)        ircc "AAAAAQAAAAEAAAB1Aw==" ;;
  left)        ircc "AAAAAQAAAAEAAAA0Aw==" ;;
  right)       ircc "AAAAAQAAAAEAAAAzAw==" ;;
  confirm)     ircc "AAAAAQAAAAEAAABlAw==" ;;
  home)        ircc "AAAAAQAAAAEAAABgAw==" ;;
  back)        ircc "AAAAAgAAAJcAAAAjAw==" ;;
  hdmi1)       ircc "AAAAAgAAABoAAABaAw==" ;;
  hdmi2)       ircc "AAAAAgAAABoAAABbAw==" ;;
  open-url)    curl -s -X POST "http://$TV/sony/appControl" \
                 -H "Content-Type: application/json" \
                 -H "X-Auth-PSK: $PSK" \
                 -d "{\"method\":\"setActiveApp\",\"params\":[{\"uri\":\"localapp://webappruntime?url=$2\",\"data\":\"\"}],\"id\":1,\"version\":\"1.0\"}" ;;
  kill)        curl -s -X POST "http://$TV/sony/appControl" \
                 -H "Content-Type: application/json" \
                 -H "X-Auth-PSK: $PSK" \
                 -d '{"method":"terminateApps","params":[],"id":1,"version":"1.0"}' ;;
  *)           echo "Usage: tv.sh {power-on|power-off|vol-up|vol-down|mute|up|down|left|right|confirm|home|back|hdmi1|hdmi2|open-url <url>|kill}" ;;
esac
```

## Local Test Server (Optional)

The `test/` directory contains an optional Node.js Express server for:
- Hosting the diagnostic page (`diag.html`) locally
- Collecting diagnostic results from the TV browser
- Providing a web-based remote control UI

This is **not required** for controlling the TV. It is only useful for running diagnostics and the web UI.

```bash
cd test && npm install && npm start
# Server runs on http://0.0.0.0:3000
```

## Diagnostic Page

Access `http://<SERVER_IP>:3000/diag.html` on the TV's browser (via Open URL) to run a 57-test capability scan. Results are automatically POSTed back to `/api/diag-results`.

See [docs/diag-report.md](./docs/diag-report.md) for the full analysis.

## TV Browser Capabilities (KD-55X9500G)

- **Browser**: Chrome 77.0.3865.116 (WebAppRuntime 2.1.2+10)
- **Resolution**: 1920x1080
- **GPU**: Mali-G71
- **localStorage**: ~1.6 MB
- **Sony APIs**: All available (systemevents, picturemode, DirectoryReader, decimated-video, multicast-video, 4k-photo)
- **Not supported**: Service Worker

## Sony Proprietary APIs

Available in the TV browser via the `sony` namespace:

```javascript
// System events (power on/off, input change, etc.)
sony.tv.systemevents.addListener('event', callback);
sony.tv.systemevents.removeListener('event', callback);

// Picture mode
sony.tv.picturemode.getPictureMode();
sony.tv.picturemode.setPictureMode(mode);

// USB storage reading
sony.tv.DirectoryReader // Read USB storage

// HDMI embedded video
var obj = document.createElement('object');
obj.setAttribute('type', 'application/x-decimated-video');
// Methods: open, close, setWideMode

// Multicast video
// Methods: show, close

// 4K photo rendering
// Methods: open, show, preload
```

## Remote Key Codes

Detectable via `keydown` events in the TV browser:

| Key | Code |
|-----|------|
| VK_RED | 403 |
| VK_GREEN | 404 |
| VK_YELLOW | 405 |
| VK_BLUE | 406 |
| VK_PLAY | 415 |
| VK_PAUSE | 463 |
| VK_STOP | 413 |
