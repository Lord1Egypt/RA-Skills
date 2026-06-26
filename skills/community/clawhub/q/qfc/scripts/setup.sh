#!/bin/bash
set -e

echo "Setting up QFC OpenClaw Skill..."
npm install
npm run build
echo "Setup complete."
