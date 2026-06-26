#!/bin/bash
# Startup Toolkit - Launch your startup in minutes

NAME="${1:-mystartup}"

echo "🚀 Launching $NAME..."

echo "📦 Creating project structure..."
mkdir -p $NAME/{frontend,backend,database,docker}

echo "✅ $NAME is ready!"
echo ""
echo "Next steps:"
echo "  cd $NAME"
echo "  docker-compose up"
