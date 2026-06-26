#!/bin/bash
# Deploy OpenClaw Pet Skill

echo "🐣 Deploying Agent Pet Skill for OpenClaw..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build (if needed)
echo "🔨 Building..."

# Start server
echo "🚀 Starting server..."
npm start

echo "✅ Pet skill is running!"
echo ""
echo "Add this to your OpenClaw bot:"
echo "Command: /pet"
echo "Webhook: http://localhost:3001/webhook"
