#!/bin/bash
set -e

echo "🔄 Updating Rune - Persistent AI Memory System..."

# Get current version
CURRENT_VERSION=$(brokkr-mem --version 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' || echo "unknown")
echo "Current version: $CURRENT_VERSION"

# Backup memory database before update
MEMORY_DB="$HOME/.openclaw/memory.db"
if [[ -f "$MEMORY_DB" ]]; then
    BACKUP_FILE="$HOME/.openclaw/memory_pre_update_$(date +%Y%m%d_%H%M%S).db"
    echo "💾 Creating backup at $BACKUP_FILE"
    cp "$MEMORY_DB" "$BACKUP_FILE"
fi

# Update npm dependencies
echo "📦 Updating dependencies..."
npm install --production

# Reinstall CLI globally
echo "🔧 Updating brokkr-mem CLI..."
npm install -g .

# Run database migrations if needed
echo "🗄️ Running database migrations..."
brokkr-mem stats > /dev/null 2>&1

# Check new version
NEW_VERSION=$(brokkr-mem --version 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' || echo "unknown")

if [[ "$NEW_VERSION" != "$CURRENT_VERSION" ]]; then
    echo "✅ Updated from $CURRENT_VERSION to $NEW_VERSION"
    
    # Log the update
    brokkr-mem add system rune.updated "Updated to version $NEW_VERSION on $(date -Iseconds)" --tier permanent
    
    # Run consolidation after update (good maintenance)
    echo "🧠 Running memory consolidation..."
    brokkr-mem consolidate --auto-prioritize
    
else
    echo "✅ Already up to date ($CURRENT_VERSION)"
fi

# Check for new recommended models
if command -v ollama &> /dev/null; then
    echo "🤖 Checking for model updates..."
    
    # Check if newer recommended models are available
    if ollama list | grep -q "llama3.1:8b"; then
        echo "✅ Recommended models are current"
    else
        echo "💡 Consider updating models: ollama pull llama3.1:8b"
    fi
fi

echo ""
echo "✅ Rune update complete!"
echo "🧠 Your persistent memory system is now up to date"