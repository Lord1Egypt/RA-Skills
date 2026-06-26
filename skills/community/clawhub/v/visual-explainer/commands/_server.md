# Visual-Explainer: Start Server

Start an HTTP server with automatically selected available port, then serve the visual-explainer reports.

## Command

```bash
cd visual-explainer
./scripts/serve-report-best-port.sh
```

## What It Does

1. Checks port 8080, then 8081, 8082, ... until it finds an available port
2挽救 Starts the Python HTTP server in **background**
3. Prints the **current port** being served
4. Displays the **URL** to open in browser
5. Saves the port number to `scripts/server-port.txt` for later reference

## Access

After running the script, you'll see something like:

```
✅ Server started successfully!

📡 Listening on:
   http://localhost:8083
   http://192.168.50.60:8083

📡 Reports:
   http://192.168.50.60:8083/visual-explainer-skill-report.html

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Port: 8083
🆔 PID: 12345
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Open in Browser

```
http://192.168.50.60:<PORT>/visual-explainer-skill-report.html
```

Replace `<PORT>` with whatever port is shown in the output.

## Stop the Server

```bash
cd visual-explainer
./scripts/stop-server.sh
```

## Clean Up

To completely remove saved port and PID:

```bash
rm visual-explainer/scripts/server-port.txt
```