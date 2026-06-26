#!/bin/bash
# Setup script for OpenClaw Vertex AI Memory Bank Plugin
# Checks prerequisites, creates Memory Bank instance, installs plugin, configures openclaw.json

set -e

echo "=== OpenClaw Vertex AI Memory Bank Setup ==="
echo ""

# Check prerequisites
check_cmd() {
  if ! command -v "$1" &> /dev/null; then
    echo "ERROR: $1 is required but not installed."
    echo "  Install: $2"
    exit 1
  fi
}

check_cmd gcloud "https://cloud.google.com/sdk/docs/install"
check_cmd npm "https://nodejs.org/"
check_cmd node "https://nodejs.org/"

echo "Prerequisites OK (gcloud, npm, node)"
echo ""

# Get GCP project
DEFAULT_PROJECT=$(gcloud config get-value project 2>/dev/null || true)
read -p "GCP Project ID [$DEFAULT_PROJECT]: " PROJECT_ID
PROJECT_ID=${PROJECT_ID:-$DEFAULT_PROJECT}

if [ -z "$PROJECT_ID" ]; then
  echo "ERROR: No project ID provided."
  exit 1
fi

# Get region
read -p "GCP Region [us-central1]: " REGION
REGION=${REGION:-us-central1}

echo ""
echo "Project: $PROJECT_ID"
echo "Region:  $REGION"
echo ""

# Check auth
echo "Checking GCP authentication..."
if ! gcloud auth print-access-token &> /dev/null; then
  echo "Not authenticated. Running: gcloud auth application-default login"
  gcloud auth application-default login
fi
echo "Authenticated."
echo ""

# Enable Vertex AI API
echo "Enabling Vertex AI API..."
gcloud services enable aiplatform.googleapis.com --project="$PROJECT_ID" 2>/dev/null || true
echo "Vertex AI API enabled."
echo ""

# Create reasoning engine
echo "Creating Memory Bank instance (reasoning engine)..."
RESPONSE=$(curl -s -X POST \
  "https://${REGION}-aiplatform.googleapis.com/v1beta1/projects/${PROJECT_ID}/locations/${REGION}/reasoningEngines" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"display_name": "openclaw-memory-bank"}')

# Extract reasoning engine ID from response
ENGINE_NAME=$(echo "$RESPONSE" | grep -o '"name": "[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$ENGINE_NAME" ]; then
  echo "ERROR: Failed to create reasoning engine."
  echo "Response: $RESPONSE"
  echo ""
  echo "If you already have a reasoning engine, enter its ID manually."
  read -p "Reasoning Engine ID: " ENGINE_ID
else
  ENGINE_ID=$(echo "$ENGINE_NAME" | grep -o '[0-9]*$')
  echo "Created reasoning engine: $ENGINE_ID"
fi

echo ""

# Clone and install plugin
PLUGIN_DIR="$HOME/.openclaw/plugins/openclaw-vertex-memorybank"
echo "Installing plugin to $PLUGIN_DIR..."

if [ -d "$PLUGIN_DIR" ]; then
  echo "Plugin directory exists. Pulling latest..."
  cd "$PLUGIN_DIR" && git pull
else
  git clone https://github.com/Shubhamsaboo/openclaw-vertexai-memorybank.git "$PLUGIN_DIR"
  cd "$PLUGIN_DIR"
fi

npm install
npm run build
echo "Plugin installed and built."
echo ""

# Configure openclaw.json
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
echo "Configuring openclaw.json..."

if [ ! -f "$OPENCLAW_CONFIG" ]; then
  echo "ERROR: openclaw.json not found at $OPENCLAW_CONFIG"
  echo "Add this manually to your openclaw.json plugins section:"
  echo ""
  echo "  \"openclaw-vertex-memorybank\": {"
  echo "    \"enabled\": true,"
  echo "    \"path\": \"$PLUGIN_DIR\","
  echo "    \"config\": {"
  echo "      \"projectId\": \"$PROJECT_ID\","
  echo "      \"location\": \"$REGION\","
  echo "      \"reasoningEngineId\": \"$ENGINE_ID\""
  echo "    }"
  echo "  }"
  exit 0
fi

echo ""
echo "Add this to the 'plugins' section of $OPENCLAW_CONFIG:"
echo ""
echo "  \"openclaw-vertex-memorybank\": {"
echo "    \"enabled\": true,"
echo "    \"path\": \"$PLUGIN_DIR\","
echo "    \"config\": {"
echo "      \"projectId\": \"$PROJECT_ID\","
echo "      \"location\": \"$REGION\","
echo "      \"reasoningEngineId\": \"$ENGINE_ID\""
echo "    }"
echo "  }"
echo ""
read -p "Restart OpenClaw gateway now? [y/N]: " RESTART
if [ "$RESTART" = "y" ] || [ "$RESTART" = "Y" ]; then
  openclaw gateway restart
  echo "Gateway restarting. Check logs: tail -f ~/.openclaw/logs/gateway.log | grep memory"
fi

echo ""
echo "=== Setup complete ==="
echo "Your agent now has persistent memory powered by Vertex AI Memory Bank."
