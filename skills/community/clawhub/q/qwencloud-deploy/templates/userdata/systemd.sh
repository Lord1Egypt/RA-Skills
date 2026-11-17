#!/bin/bash
# qwencloud · systemd managed app
# Placeholders:
#   __APP_ARTIFACT_URL__   OSS signed URL of app artifact tar.gz
#   __APP_RUNTIME__        none | java | node | python
#   __START_COMMAND__          Full startup command (relative to /opt/qwencloud), e.g.
#                              ./server / "python3 app.py" / "sh -c 'java -jar /opt/qwencloud/*.jar'" /
#                              "node server.js" / "gunicorn -b :8080 app:app"
#   __APP_PORT__           App listening port
#   __APP_NAME__           Service name (systemd unit / log file name)
set -euxo pipefail

LOG=/var/log/qwencloud-bootstrap.log
exec >> "$LOG" 2>&1
echo "[$(date -u +%FT%TZ)] === qwencloud systemd bootstrap start ==="

APP_URL="__APP_ARTIFACT_URL__"
RUNTIME="__APP_RUNTIME__"
ENTRY="__START_COMMAND__"
PORT="__APP_PORT__"
APP_NAME="__APP_NAME__"

# 1. Install runtime
case "$RUNTIME" in
  java)
    if ! command -v java >/dev/null 2>&1; then
      if command -v dnf >/dev/null 2>&1; then dnf install -y java-17-openjdk-headless
      else yum install -y java-17-openjdk-headless; fi
    fi
    ;;
  node)
    if ! command -v node >/dev/null 2>&1; then
      # Install Node from the distro's GPG-signed package repos.
      # Order: (1) plain dnf install (on Alibaba Cloud Linux 3, nodejs 20 is a standalone package in
      #        alinux3-updates); (2) if no standalone package, enable a nodejs module stream and install;
      #        (3) older systems fall back to yum.
      if command -v dnf >/dev/null 2>&1; then
        if ! dnf install -y nodejs npm; then
          if dnf -q module list nodejs >/dev/null 2>&1; then
            dnf -y module reset nodejs || true
            # prefer 20, otherwise fall back to whatever default stream the image offers
            dnf -y module enable nodejs:20 || dnf -y module enable nodejs || true
            dnf install -y nodejs npm
          fi
        fi
      else
        yum install -y nodejs npm
      fi
    fi
    if ! command -v yarn >/dev/null 2>&1; then
      npm install -g yarn
    fi
    ;;
  python)
    if ! command -v python3 >/dev/null 2>&1; then
      yum install -y python3 python3-pip
    fi
    ;;
  none)
    : # No runtime installation needed (static binary, or runtime already exists)
    ;;
  *)
    echo "[warn] unknown runtime '$RUNTIME', skipping runtime install"
    ;;
esac

# 2. Pull artifacts
mkdir -p /opt/qwencloud
cd /opt/qwencloud
curl -fsSL "$APP_URL" -o app.tar.gz
tar -xzf app.tar.gz
rm -f app.tar.gz

# python: install dependencies
if [ "$RUNTIME" = "python" ] && [ -f requirements.txt ]; then
  python3 -m pip install --no-cache-dir -r requirements.txt
fi
# node: install dependencies (when artifact includes package.json)
if [ "$RUNTIME" = "node" ] && [ -f package.json ]; then
  yarn install --production
fi

# 3. Parse startup command
# ENTRY is the "full startup command" and the sole source of the command; the script does NOT
# inject any interpreter based on runtime — it only resolves the first token (argv[0]) to an
# absolute path, because systemd ExecStart requires argv[0] to be an absolute path.
# Whether it's ./server / "python3 run.py" / "java -jar <name>.jar" / "gunicorn app:app",
# it runs exactly as ENTRY specifies.
set -- $ENTRY
ARGV0="$1"; shift || true
case "$ARGV0" in
  /*)
    : ;;                                    # Already an absolute path, use as-is
  */*)
    # Relative path containing / (./server, subdir/app) → build absolute path; cannot use command -v as it returns relative paths as-is
    ARGV0="/opt/qwencloud/${ARGV0#./}"
    chmod +x "$ARGV0" 2>/dev/null || true
    ;;
  *)
    if command -v "$ARGV0" >/dev/null 2>&1; then
      ARGV0="$(command -v "$ARGV0")"        # Interpreter/tool on PATH (python3 / node / java / gunicorn ...)
    else
      ARGV0="/opt/qwencloud/$ARGV0"         # Executable in the artifact (bare filename, e.g. server)
      chmod +x "$ARGV0" 2>/dev/null || true
    fi ;;
esac
EXEC="$ARGV0 $*"

# 4. Write systemd unit
cat > /etc/systemd/system/${APP_NAME}.service <<UNIT
[Unit]
Description=${APP_NAME} app
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=/opt/qwencloud
Environment=PORT=${PORT}
EnvironmentFile=-/etc/qwencloud/db.env
ExecStart=${EXEC}
Restart=always
RestartSec=3
StandardOutput=append:/var/log/${APP_NAME}.log
StandardError=append:/var/log/${APP_NAME}.log

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable ${APP_NAME}
systemctl restart ${APP_NAME}

echo "[$(date -u +%FT%TZ)] systemd app up"
