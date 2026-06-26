# Scripts for Visual-Explainer

Utility scripts to help you serve and manage visual reports.

## Available Scripts

### `serve-report-best-port.sh` ⭐ **PRIMARY**
Starts HTTP server on best available port (8080+).
- Checks ports sequentially for availability
- Runs server in background
- Returns the actual port used
- Saves port number to `server-port.txt`

**Usage:**
```bash
./serve-report-best-port.sh
```

### `serve-report-alt-port.sh`
Serves on specific alternative port (8081 by default).

**Usage:**
```bash
./serve-report-alt-port.sh <port>
```

### `serve-report.sh`
Simple serve script (requires you to specify port).

**Usage:**
```bash
./serve-report.sh <port>
```

### `stop-server.sh`
Stops the Python HTTP server.

**Usage:**
```bash
./stop-server.sh
```

### `clean-server.sh`
Cleans up all server files and kills any Python HTTP servers.

**Usage:**
```bash
./clean-server.sh
```

## Quick Start

1. **Start server:**
   ```bash
   cd visual-explainer
   ./scripts/serve-report-best-port.sh
   ```

2. **Open browser:**
   ```
   http://192.168.50.60:<PORT>/visual-explainer-skill-report.html
   ```

3. **Stop server (when done):**
   ```bash
   ./scripts/stop-server.sh
   ```

## Server State Files

- `server-port.txt` — Saved port number (created when using `serve-report-best-port.sh`)