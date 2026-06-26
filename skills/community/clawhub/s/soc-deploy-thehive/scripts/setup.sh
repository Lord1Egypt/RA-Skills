#!/bin/bash
# Deploy TheHive 5.4 + Cortex 3.1.8 on any Docker-ready Linux host
# Usage: ./setup.sh [password] [org-name] [thehive-secret]
# Run ON the target host (not remotely)

set -euo pipefail

PASSWORD="${1:-ChangeMe123!}"
ORG_NAME="${2:-SOC}"
TH_SECRET="${3:-$(openssl rand -base64 32)}"
DEPLOY_DIR=~/thehive-cortex

echo "=== TheHive + Cortex Deployment ==="
echo "Password: $PASSWORD | Org: $ORG_NAME"
echo ""

# Setup directory
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

# Write docker-compose.yml if not present
if [ ! -f docker-compose.yml ]; then
  echo "[0/11] Writing docker-compose.yml..."
  # If the file was SCP'd earlier, skip. Otherwise the SKILL.md instructs to SCP it.
  echo "ERROR: docker-compose.yml not found. SCP it from references/docker-compose.yml first."
  exit 1
fi

# Replace secret placeholder
sed -i "s|THEHIVE_SECRET_PLACEHOLDER|${TH_SECRET}|g" docker-compose.yml

# Start stack
echo "[1/11] Starting Docker Compose stack..."
docker compose up -d

# Wait for Elasticsearch
echo "[2/11] Waiting for Elasticsearch..."
for i in $(seq 1 30); do
  if curl -sf http://localhost:9200/_cluster/health > /dev/null 2>&1; then
    echo "  Elasticsearch is up!"
    break
  fi
  [ $i -eq 30 ] && { echo "  TIMEOUT waiting for Elasticsearch"; exit 1; }
  sleep 10
done

# Wait for TheHive
echo "[3/11] Waiting for TheHive..."
for i in $(seq 1 30); do
  if curl -sf http://localhost:9000/api/status > /dev/null 2>&1; then
    echo "  TheHive is up!"
    break
  fi
  [ $i -eq 30 ] && { echo "  TIMEOUT waiting for TheHive"; exit 1; }
  sleep 10
done

# Wait for Cortex
echo "[4/11] Waiting for Cortex..."
for i in $(seq 1 30); do
  if curl -sf http://localhost:9001/api/status > /dev/null 2>&1; then
    echo "  Cortex is up!"
    break
  fi
  [ $i -eq 30 ] && { echo "  TIMEOUT waiting for Cortex"; exit 1; }
  sleep 10
done

# TheHive: Login with defaults
echo "[5/11] TheHive: Logging in with default creds..."
TH_SESSION=$(curl -s -D - -X POST http://localhost:9000/api/v1/login \
  -H 'Content-Type: application/json' \
  -d '{"user":"admin@thehive.local","password":"secret"}' 2>&1 | \
  grep -i 'THEHIVE-SESSION' | head -1 | sed 's/.*THEHIVE-SESSION=//;s/;.*//' | tr -d '\r')

# TheHive: Change password
echo "[6/11] TheHive: Changing admin password..."
printf '{"currentPassword":"secret","password":"%s"}' "$PASSWORD" | \
curl -sf -X POST "http://localhost:9000/api/v1/user/admin@thehive.local/password/change" \
  -H "Cookie: THEHIVE-SESSION=$TH_SESSION" \
  -H 'Content-Type: application/json' -d @- > /dev/null

# TheHive: Generate API key
THEHIVE_KEY=$(curl -s -X POST "http://localhost:9000/api/v1/user/admin@thehive.local/key/renew" \
  -H "Cookie: THEHIVE-SESSION=$TH_SESSION")
echo "  TheHive API key: ${THEHIVE_KEY:0:20}..."

# Cortex: Run DB migration
echo "[7/11] Cortex: Running DB migration..."
curl -sf -X POST http://localhost:9001/api/maintenance/migrate \
  -H 'Content-Type: application/json' > /dev/null

# Cortex: Create superadmin
echo "[8/11] Cortex: Creating superadmin..."
printf '{"login":"admin","name":"Admin","password":"%s","roles":["superadmin"]}' "$PASSWORD" | \
curl -sf -X POST http://localhost:9001/api/user \
  -H 'Content-Type: application/json' -d @- > /dev/null

# Cortex: Login + get CSRF
CX_SESSION=$(printf '{"user":"admin","password":"%s"}' "$PASSWORD" | \
curl -s -D - -X POST http://localhost:9001/api/login \
  -H 'Content-Type: application/json' -d @- 2>&1 | \
  grep -i 'CORTEX_SESSION' | head -1 | sed 's/.*CORTEX_SESSION=//;s/;.*//' | tr -d '\r')

CSRF=$(curl -s -D - http://localhost:9001/api/user/admin \
  -H "Cookie: CORTEX_SESSION=$CX_SESSION" 2>&1 | \
  grep 'CORTEX-XSRF-TOKEN' | head -1 | sed 's/.*CORTEX-XSRF-TOKEN=//;s/;.*//' | tr -d '\r')

# Cortex: Create org
echo "[9/11] Cortex: Creating org '$ORG_NAME'..."
curl -sf -X POST http://localhost:9001/api/organization \
  -H "Cookie: CORTEX_SESSION=$CX_SESSION; CORTEX-XSRF-TOKEN=$CSRF" \
  -H "X-CORTEX-XSRF-TOKEN: $CSRF" \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"$ORG_NAME\",\"description\":\"$ORG_NAME organization\",\"status\":\"Active\"}" > /dev/null

# Cortex: Create org admin
ORG_ADMIN="$(echo "$ORG_NAME" | tr '[:upper:]' '[:lower:]')-admin"
printf '{"name":"%s Admin","roles":["read","analyze","orgadmin"],"organization":"%s","login":"%s"}' \
  "$ORG_NAME" "$ORG_NAME" "$ORG_ADMIN" | \
curl -sf -X POST http://localhost:9001/api/user \
  -H "Cookie: CORTEX_SESSION=$CX_SESSION; CORTEX-XSRF-TOKEN=$CSRF" \
  -H "X-CORTEX-XSRF-TOKEN: $CSRF" \
  -H 'Content-Type: application/json' -d @- > /dev/null

# Cortex: Generate API keys
echo "[10/11] Cortex: Generating API keys..."
CORTEX_SUPER_KEY=$(curl -s -X POST http://localhost:9001/api/user/admin/key/renew \
  -H "Cookie: CORTEX_SESSION=$CX_SESSION; CORTEX-XSRF-TOKEN=$CSRF" \
  -H "X-CORTEX-XSRF-TOKEN: $CSRF")

CORTEX_ORG_KEY=$(curl -s -X POST "http://localhost:9001/api/user/$ORG_ADMIN/key/renew" \
  -H "Cookie: CORTEX_SESSION=$CX_SESSION; CORTEX-XSRF-TOKEN=$CSRF" \
  -H "X-CORTEX-XSRF-TOKEN: $CSRF")

# Wire TheHive-Cortex integration
echo "[11/11] Wiring TheHive-Cortex integration..."
if ! grep -q "cortex-hostnames" docker-compose.yml; then
  sed -i '/--es-hostnames/a\      - "--cortex-hostnames"\n      - "cortex"\n      - "--cortex-keys"\n      - "'"$CORTEX_ORG_KEY"'"' docker-compose.yml
fi

docker compose up -d thehive
echo "  Waiting 30s for TheHive restart..."
sleep 30

# Verify
TH_CHECK=$(curl -sf http://localhost:9000/api/v1/user/current -H "Authorization: Bearer $THEHIVE_KEY" 2>&1 | grep -c login || echo "0")
CX_CHECK=$(curl -sf http://localhost:9001/api/status -H "Authorization: Bearer $CORTEX_SUPER_KEY" 2>&1 | grep -c versions || echo "0")

HOST_IP=$(hostname -I | awk '{print $1}')

# Save credentials
cat > "$DEPLOY_DIR/api-keys.txt" << EOF
=== TheHive + Cortex Credentials ===
Generated: $(date)

TheHive:
  URL: http://${HOST_IP}:9000
  User: admin@thehive.local
  Password: $PASSWORD
  API Key: $THEHIVE_KEY

Cortex:
  URL: http://${HOST_IP}:9001
  Superadmin: admin / $PASSWORD
  Superadmin API Key: $CORTEX_SUPER_KEY
  Org Admin: $ORG_ADMIN (API key only)
  Org Admin API Key: $CORTEX_ORG_KEY

MCP Connection:
  THEHIVE_URL=http://${HOST_IP}:9000
  THEHIVE_API_KEY=$THEHIVE_KEY
  CORTEX_URL=http://${HOST_IP}:9001
  CORTEX_API_KEY=$CORTEX_SUPER_KEY
EOF

echo ""
echo "=== Deployment Complete ==="
[ "$TH_CHECK" -gt 0 ] && echo "TheHive API: ✅" || echo "TheHive API: ❌"
[ "$CX_CHECK" -gt 0 ] && echo "Cortex API:  ✅" || echo "Cortex API:  ❌"
echo ""
echo "TheHive: http://${HOST_IP}:9000"
echo "Cortex:  http://${HOST_IP}:9001"
echo ""
echo "TheHive Admin: admin@thehive.local / $PASSWORD"
echo "TheHive Key:   $THEHIVE_KEY"
echo ""
echo "Cortex Super:  admin / $PASSWORD"
echo "Cortex Super Key: $CORTEX_SUPER_KEY"
echo "Cortex Org:    $ORG_ADMIN"
echo "Cortex Org Key:   $CORTEX_ORG_KEY"
echo ""
echo "Credentials saved to: $DEPLOY_DIR/api-keys.txt"
