---
name: hermes-webui-agent
description: Expert in deploying, configuring, and using Hermes WebUI—a web interface for Hermes Agent with persistent memory, scheduled jobs, and multi-platform messaging.
triggers:
  - "set up hermes web interface"
  - "configure hermes webui"
  - "run hermes agent from browser"
  - "deploy hermes with docker"
  - "troubleshoot hermes webui connection"
  - "create hermes scheduled job"
  - "access hermes from phone"
  - "configure hermes messaging apps"
---

# Hermes WebUI Agent

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Expert in deploying, configuring, and using **Hermes WebUI**—a lightweight web interface for Hermes Agent. This skill covers installation (native Python and Docker), configuration, SSH tunneling for remote access, messaging platform integration, scheduled jobs, workspace management, and troubleshooting common issues.

## What Hermes WebUI Does

Hermes WebUI provides browser-based access to [Hermes Agent](https://hermes-agent.nousresearch.com/), a self-hosted autonomous AI agent with:

- **Persistent memory** across sessions (user profiles, agent notes, self-improving skills)
- **Scheduled jobs** (cron-style tasks that run offline and deliver via Telegram, Discord, Slack, Signal, email)
- **Messaging platform integration** (10+ platforms)
- **Provider-agnostic** (OpenAI, Anthropic, Google, DeepSeek, OpenRouter, local models)
- **Self-hosted** (your conversations, your memory, your hardware)

The WebUI offers three-panel layout (sessions sidebar, chat center, workspace file browser), full CLI parity, and password protection for remote access.

## Installation

### Native Python (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/nesquena/hermes-webui.git
cd hermes-webui

# Run bootstrap (auto-detects Hermes Agent, creates venv, starts server)
python3 bootstrap.py

# Or use the shell launcher
./start.sh
```

The bootstrap will:
1. Detect or install Hermes Agent via the official installer
2. Create/activate a Python venv with dependencies
3. Start the web server on `http://localhost:8787`
4. Open the browser and show onboarding wizard

**For self-hosted VM/homelab** (daemon mode):

```bash
# Start as background daemon
./ctl.sh start

# Check status
./ctl.sh status

# View logs
./ctl.sh logs --lines 100

# Restart
./ctl.sh restart

# Stop
./ctl.sh stop
```

The daemon writes logs to `~/.hermes/webui.log` and PID to `~/.hermes/webui.pid`.

### Docker (Single Container - Simplest)

```bash
git clone https://github.com/nesquena/hermes-webui
cd hermes-webui

# Copy and edit environment file
cp .env.docker.example .env
# If your host UID isn't 1000 (check with `id -u`), edit .env:
# UID=501  # macOS example

# Start
docker compose up -d

# Open http://localhost:8787
```

**With password protection** (required for network exposure):

```bash
echo "HERMES_WEBUI_PASSWORD=your-strong-password" >> .env
docker compose up -d --force-recreate
```

### Docker (Multi-Container Setups)

**Two-container** (agent + WebUI isolated):

```bash
docker compose -f docker-compose.two-container.yml up -d
```

**Three-container** (agent + dashboard + WebUI):

```bash
docker compose -f docker-compose.three-container.yml up -d
```

### Manual Docker Run

```bash
docker pull ghcr.io/nesquena/hermes-webui:latest

docker run -d \
  -e WANTED_UID=$(id -u) \
  -e WANTED_GID=$(id -g) \
  -v ~/.hermes:/home/hermeswebui/.hermes \
  -e HERMES_WEBUI_STATE_DIR=/home/hermeswebui/.hermes/webui \
  -v ~/workspace:/workspace \
  -p 127.0.0.1:8787:8787 \
  ghcr.io/nesquena/hermes-webui:latest
```

## Configuration

### Environment Variables

Create `.env` in the project root or export variables:

```bash
# Port (default: 8787)
HERMES_WEBUI_PORT=9000

# Bind host (default: 127.0.0.1 for local-only, 0.0.0.0 for network)
HERMES_WEBUI_HOST=0.0.0.0

# Password protection (required if HOST is 0.0.0.0)
HERMES_WEBUI_PASSWORD=your-strong-password

# Hermes Agent directory (auto-detected)
HERMES_WEBUI_AGENT_DIR=/path/to/hermes-agent

# State directory (sessions, logs, etc.)
HERMES_WEBUI_STATE_DIR=~/.hermes/webui

# Default workspace directory
HERMES_WEBUI_DEFAULT_WORKSPACE=~/workspace

# Python executable (auto-detected from agent venv)
HERMES_WEBUI_PYTHON=/path/to/python

# Disable auto-install of Hermes Agent
HERMES_WEBUI_AUTO_INSTALL=

# Skip chmod enforcement (Docker only, for .env permission issues)
HERMES_SKIP_CHMOD=1
```

### SSH Tunnel for Remote Access

If running on a VM/server, access securely via SSH tunnel:

```bash
# On your local machine
ssh -L 8787:localhost:8787 user@your-server.com

# Then open http://localhost:8787 in your browser
```

For persistent tunneling, use `autossh`:

```bash
autossh -M 0 -f -N -L 8787:localhost:8787 user@your-server.com
```

### Daemon Lifecycle (ctl.sh)

```bash
# Start daemon (respects .env, inline overrides allowed)
HERMES_WEBUI_HOST=0.0.0.0 ./ctl.sh start

# Check status (PID, uptime, host:port, log path, /health)
./ctl.sh status

# Tail logs
./ctl.sh logs --lines 50

# Restart
./ctl.sh restart

# Stop
./ctl.sh stop
```

## Key Commands and API

### Starting the Server (Python)

```python
# From bootstrap.py or manual start
from pathlib import Path
import subprocess
import sys

# Detect Hermes Agent directory
agent_dir = Path.home() / ".hermes" / "hermes-agent"
if not agent_dir.exists():
    agent_dir = Path(__file__).parent.parent / "hermes-agent"

# Find Python from agent venv
venv_python = agent_dir / "venv" / "bin" / "python"
if not venv_python.exists():
    venv_python = Path(__file__).parent / ".venv" / "bin" / "python"

# Start server
subprocess.run([
    str(venv_python),
    "-m", "hermes_webui.server",
    "--port", "8787",
    "--host", "127.0.0.1"
])
```

### Server Module (hermes_webui/server.py)

```python
#!/usr/bin/env python3
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Load config from environment
PORT = int(os.getenv("HERMES_WEBUI_PORT", 8787))
HOST = os.getenv("HERMES_WEBUI_HOST", "127.0.0.1")
PASSWORD = os.getenv("HERMES_WEBUI_PASSWORD")
STATE_DIR = Path(os.getenv("HERMES_WEBUI_STATE_DIR", Path.home() / ".hermes" / "webui"))
AGENT_DIR = Path(os.getenv("HERMES_WEBUI_AGENT_DIR", Path.home() / ".hermes" / "hermes-agent"))

STATE_DIR.mkdir(parents=True, exist_ok=True)

# Password protection middleware
@app.before_request
def check_auth():
    if PASSWORD and request.endpoint not in ["login", "static"]:
        auth = request.headers.get("Authorization")
        if not auth or not check_password_hash(generate_password_hash(PASSWORD), auth):
            return jsonify({"error": "Unauthorized"}), 401

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "agent_dir": str(AGENT_DIR), "state_dir": str(STATE_DIR)})

@app.route("/api/sessions", methods=["GET"])
def list_sessions():
    sessions_dir = STATE_DIR / "sessions"
    sessions = [s.name for s in sessions_dir.glob("*.json")] if sessions_dir.exists() else []
    return jsonify({"sessions": sessions})

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
```

### Accessing the Agent in Python

```python
# WebUI uses the Hermes Agent SDK
import sys
from pathlib import Path

# Add agent to path
agent_dir = Path.home() / ".hermes" / "hermes-agent"
sys.path.insert(0, str(agent_dir))

from hermes.agent import Agent
from hermes.memory import Memory

# Initialize agent with memory
agent = Agent(
    memory=Memory(storage_dir=Path.home() / ".hermes" / "memory"),
    workspace_dir=Path.home() / "workspace"
)

# Send a message
response = agent.send_message("List my recent projects")
print(response)

# Access skills
skills = agent.memory.get_skills()
for skill in skills:
    print(f"Skill: {skill.name}, Uses: {skill.use_count}")
```

## Common Patterns

### Setting Up Scheduled Jobs

Scheduled jobs are configured via the Hermes Agent CLI, then accessible from WebUI:

```bash
# Create a cron job (from Hermes Agent directory)
cd ~/.hermes/hermes-agent
source venv/bin/activate

# Schedule a daily summary at 9 AM
hermes schedule create \
  --name "daily-summary" \
  --cron "0 9 * * *" \
  --prompt "Summarize my commits from yesterday and send to Telegram" \
  --messenger telegram
```

From the WebUI, jobs appear in the **Hermes Control Center** (bottom sidebar launcher) under "Scheduled Jobs."

### Messaging Platform Integration

Configure platforms via `hermes messenger` CLI:

```bash
# Telegram
hermes messenger add telegram --token "$TELEGRAM_BOT_TOKEN" --chat-id "$CHAT_ID"

# Discord
hermes messenger add discord --webhook-url "$DISCORD_WEBHOOK_URL"

# Slack
hermes messenger add slack --webhook-url "$SLACK_WEBHOOK_URL"

# Signal (requires signal-cli)
hermes messenger add signal --phone "+1234567890"
```

Reference in jobs or send messages:

```python
from hermes.messengers import get_messenger

telegram = get_messenger("telegram")
telegram.send("Deployment complete! ✅")
```

### Workspace File Browsing

The right panel in WebUI browses files from `HERMES_WEBUI_DEFAULT_WORKSPACE`. To switch workspaces mid-session:

```python
# Via WebUI API
POST /api/workspace/switch
{
  "path": "/home/user/new-project"
}
```

Or via agent message:

```
Switch workspace to ~/new-project
```

### Using Profiles

Profiles store user-specific context. Create via WebUI **Control Center > Profiles** or CLI:

```bash
hermes profile create work \
  --name "Work Profile" \
  --context "I'm a Python backend engineer working on FastAPI microservices. I prefer pytest for testing and Docker for deployment."

hermes profile activate work
```

From WebUI composer footer: dropdown shows active profile.

## Troubleshooting

### WebUI Can't Find Hermes Agent

**Symptom**: `Hermes Agent not found` error on startup.

**Fix**: Set explicit path:

```bash
export HERMES_WEBUI_AGENT_DIR=/path/to/hermes-agent
./start.sh
```

Or in `.env`:

```bash
HERMES_WEBUI_AGENT_DIR=/path/to/hermes-agent
```

### Permission Denied (Docker)

**Symptom**: `PermissionError` writing to `~/.hermes` or `/workspace`.

**Fix**: Set correct UID in `.env`:

```bash
# Check your UID
id -u

# In .env
UID=1000  # Replace with your actual UID
```

Then recreate:

```bash
docker compose down
docker compose up -d
```

### Password Not Working

**Symptom**: 401 Unauthorized even with correct password.

**Fix**: Check environment variable is set:

```bash
# In .env
HERMES_WEBUI_PASSWORD=your-password

# Verify it's loaded
docker compose config | grep PASSWORD
```

Recreate container:

```bash
docker compose up -d --force-recreate
```

### WebUI Shows Empty Workspace (Docker Two-Container)

**Symptom**: Workspace file browser is empty, but files exist on host.

**Fix**: This is architectural limitation #681. Tools run in WebUI container, not agent container. Use single-container setup:

```bash
docker compose -f docker-compose.yml up -d
```

Or extend WebUI Dockerfile to install needed tools:

```dockerfile
FROM ghcr.io/nesquena/hermes-webui:latest

USER root
RUN apk add --no-cache git nodejs npm
USER hermeswebui
```

### Model Provider Not Configured

**Symptom**: Onboarding wizard shows "Provider setup incomplete."

**Fix**: Complete setup via CLI:

```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate

# For OpenAI
hermes model add openai --api-key "$OPENAI_API_KEY"

# For Anthropic
hermes model add anthropic --api-key "$ANTHROPIC_API_KEY"

# For local model (Ollama)
hermes model add ollama --base-url http://localhost:11434

# Set default
hermes model set-default gpt-4
```

Then refresh WebUI.

### WSL Auto-Start Not Working

**Symptom**: WebUI doesn't start on Windows login.

**Fix**: See `docs/wsl-autostart.md`. Quick version:

1. Create `start-hermes.vbs` in `shell:startup`:

```vbscript
Set objShell = CreateObject("WScript.Shell")
objShell.Run "wsl -d Ubuntu -u yourusername -- /home/yourusername/hermes-webui/ctl.sh start", 0
```

2. Ensure `ctl.sh` is executable:

```bash
chmod +x ~/hermes-webui/ctl.sh
```

### Health Check Fails

**Symptom**: `/health` returns 500 or connection refused.

**Fix**: Check logs:

```bash
# Native Python
tail -f ~/.hermes/webui.log

# Docker
docker logs hermes-webui

# ctl.sh daemon
./ctl.sh logs
```

Common causes:
- Agent directory not found (set `HERMES_WEBUI_AGENT_DIR`)
- Port already in use (change `HERMES_WEBUI_PORT`)
- Python venv corrupted (delete `.venv` and re-run `bootstrap.py`)

### Podman Shared `.hermes` Fails

**Symptom**: Permission issues with Podman 3.4.

**Fix**: Upgrade to Podman 4+ or use single-container setup. Podman 3.4's `keep-id` has known limitations with shared volumes.

## Advanced Configuration

### Custom Agent Orchestration

Hermes can spawn other agents (Claude Code, Codex) and bring results back:

```python
from hermes.orchestration import spawn_agent

# Spawn Claude Code for heavy refactoring
result = spawn_agent(
    agent_type="claude-code",
    task="Refactor authentication module to use JWT",
    workspace="~/my-project"
)

# Result is stored in Hermes memory
agent.memory.add_note(f"Refactoring completed: {result.summary}")
```

From WebUI, trigger via message:

```
Spawn Claude Code to refactor the auth module
```

### Custom Skills

Skills are auto-written by Hermes. To manually add:

```bash
# In Hermes Agent directory
cd ~/.hermes/hermes-agent
source venv/bin/activate

hermes skill create deploy-to-prod \
  --description "Deploy current branch to production" \
  --steps "1. Run tests\n2. Build Docker image\n3. Push to registry\n4. Update k8s deployment"
```

Skills appear in WebUI **Control Center > Skills**.

### External Access (Production)

For production deployment behind a reverse proxy:

```nginx
# Nginx config
server {
    listen 443 ssl;
    server_name hermes.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/hermes.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hermes.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8787;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Ensure password is set:

```bash
HERMES_WEBUI_PASSWORD=strong-password
HERMES_WEBUI_HOST=127.0.0.1  # Keep local, proxy handles external
```

## Summary

Hermes WebUI provides full-featured browser access to Hermes Agent with zero configuration beyond initial bootstrap. Key capabilities:

- **Persistent memory** across sessions
- **Scheduled jobs** with multi-platform delivery
- **Self-improving skills**
- **Provider-agnostic** model support
- **Self-hosted** with SSH tunnel or reverse proxy access

Install via `bootstrap.py` (native) or Docker Compose, configure via environment variables, and access via `http://localhost:8787` or SSH tunnel. For production, use password protection and reverse proxy with HTTPS.
