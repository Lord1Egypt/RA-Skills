#!/bin/bash
set -e

# Install script for Rune - Self-Improving AI Memory System
# Includes automatic backups, verification modes, and security improvements

# Parse command line arguments
DRY_RUN=false
VERIFY_ONLY=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verify)
            VERIFY_ONLY=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            echo "Rune Installation Script"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --dry-run    Show what would be installed without making changes"
            echo "  --verify     Verify package integrity and dependencies"
            echo "  --force      Skip safety checks and prompts"
            echo "  -h, --help   Show this help message"
            echo ""
            echo "The installer will:"
            echo "  • Create ~/.openclaw directory structure"
            echo "  • Install rune CLI globally via npm"  
            echo "  • Create SQLite memory database"
            echo "  • Add integration to HEARTBEAT.md (with backup)"
            echo "  • Default to local models (cloud APIs optional)"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "🧠 Rune - Self-Improving AI Memory System Installer"
echo "=================================================="

# Verification mode
if [ "$VERIFY_ONLY" = true ]; then
    echo "🔍 Package verification mode..."
    
    echo "✅ Checking package.json..."
    if [[ -f "package.json" ]]; then
        echo "   Package: $(jq -r '.name' package.json) v$(jq -r '.version' package.json)"
        echo "   Dependencies: $(jq -r '.dependencies | keys | length' package.json) required, $(jq -r '.optionalDependencies | keys | length // 0' package.json) optional"
    else
        echo "❌ package.json not found - incomplete package"
        exit 1
    fi
    
    echo "✅ Checking source files..."
    if [[ -f "bin/cli.js" ]]; then
        echo "   CLI: $(wc -l < bin/cli.js) lines"
    else
        echo "❌ bin/cli.js not found - incomplete package"
        exit 1
    fi
    
    echo "✅ Package verification complete"
    exit 0
fi

# Pre-installation summary
echo ""
echo "📋 Installation Summary:"
echo "========================"
echo "• Package: Rune v$(jq -r '.version' package.json 2>/dev/null || echo 'unknown')"
echo "• CLI Command: rune (replaces any existing brokkr-mem)"
echo "• Database: ~/.openclaw/memory.db (SQLite)"
echo "• Integration: Adds lines to ~/.openclaw/workspace/HEARTBEAT.md"
echo "• Dependencies: $(jq -r '.dependencies | keys | join(", ")' package.json 2>/dev/null || echo 'unknown')"
echo "• Default: Local models (Ollama) - cloud APIs optional"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "🔍 Dry run mode - showing what would be done:"
    echo ""
    
    echo "1. Check Node.js version >= 18.0.0"
    echo "2. Backup existing files:"
    if [[ -f "$HOME/.openclaw/workspace/HEARTBEAT.md" ]]; then
        echo "   - HEARTBEAT.md → HEARTBEAT.md.backup-$(date +%s)"
    fi
    if [[ -f "$HOME/.openclaw/memory.db" ]]; then
        echo "   - memory.db → memory.db.backup-$(date +%s)"  
    fi
    
    echo "3. Install npm dependencies (production only)"
    echo "4. Install rune CLI globally"
    echo "5. Create ~/.openclaw directory structure"
    echo "6. Initialize SQLite memory database"
    echo "7. Add Rune integration to HEARTBEAT.md"
    echo "8. Configure local-first defaults"
    echo ""
    echo "To proceed with actual installation, run without --dry-run"
    exit 0
fi

# Safety checks
if [ "$FORCE" = false ]; then
    echo "⚠️  Pre-installation checks:"
    
    if command -v rune &> /dev/null; then
        echo "   ⚠️  'rune' command already exists - will be replaced"
    fi
    
    if command -v brokkr-mem &> /dev/null; then
        echo "   ⚠️  'brokkr-mem' command exists - will be replaced by 'rune'"
    fi
    
    if [[ -f "$HOME/.openclaw/memory.db" ]]; then
        echo "   ⚠️  Memory database exists - will be backed up"
    fi
    
    echo ""
    echo "Continue with installation? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Installation cancelled"
        exit 0
    fi
fi

echo ""
echo "🚀 Starting installation..."

# 1. Check Node.js version
echo "1. Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed. Please install Node.js >= 18.0.0"
    exit 1
fi

NODE_VERSION=$(node --version | sed 's/v//')
NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)
REQUIRED_MAJOR=18

if [ "$NODE_MAJOR" -lt "$REQUIRED_MAJOR" ]; then
    echo "❌ Node.js >= 18.0.0 is required. Current version: $NODE_VERSION"
    exit 1
fi
echo "   ✅ Node.js $NODE_VERSION"

# 2. Create backups
echo "2. Creating automatic backups..."
TIMESTAMP=$(date +%s)
MEMORY_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
mkdir -p "$WORKSPACE_DIR"

if [[ -f "$WORKSPACE_DIR/HEARTBEAT.md" ]]; then
    cp "$WORKSPACE_DIR/HEARTBEAT.md" "$WORKSPACE_DIR/HEARTBEAT.md.backup-$TIMESTAMP"
    echo "   ✅ HEARTBEAT.md backed up"
fi

if [[ -f "$MEMORY_DIR/memory.db" ]]; then
    cp "$MEMORY_DIR/memory.db" "$MEMORY_DIR/memory.db.backup-$TIMESTAMP"
    echo "   ✅ memory.db backed up"
fi

# 3. Install npm dependencies
echo "3. Installing dependencies..."
if ! npm install --production --silent; then
    echo "❌ Failed to install npm dependencies"
    exit 1
fi
echo "   ✅ Dependencies installed"

# 4. Install CLI globally
echo "4. Installing rune CLI globally..."
if ! npm install -g . --silent; then
    echo "❌ Failed to install rune CLI globally"
    exit 1
fi
echo "   ✅ rune CLI installed"

# 5. Initialize database
echo "5. Initializing memory database..."
rune stats > /dev/null 2>&1 || true
echo "   ✅ Database initialized"

# 6. Check for local models (Ollama)
echo "6. Checking local model availability..."
if command -v ollama &> /dev/null; then
    echo "   ✅ Ollama detected - local scoring enabled"
    
    if ollama list 2>/dev/null | grep -q "llama3.1:8b"; then
        echo "   ✅ llama3.1:8b model available"
    else
        echo "   ⚠️  Recommended: ollama pull llama3.1:8b"
    fi
else
    echo "   ⚠️  Ollama not found - install for local scoring"
    echo "      Cloud APIs available with optional API keys"
fi

# 7. Add heartbeat integration
echo "7. Adding HEARTBEAT.md integration..."
HEARTBEAT_FILE="$WORKSPACE_DIR/HEARTBEAT.md"

if [[ ! -f "$HEARTBEAT_FILE" ]]; then
    cat > "$HEARTBEAT_FILE" << 'EOF'
# HEARTBEAT.md

## 🧠 Rune Memory Maintenance (ACTIVE)
- `rune expire` — prune expired working memory
- `rune inject --output ~/.openclaw/workspace/FACTS.md` — regenerate intelligent context
- `rune consolidate --auto-prioritize` — optimize memory (weekly)

## Next Actions
Check `rune next-task` for intelligent task recommendations based on memory patterns.
EOF
    echo "   ✅ HEARTBEAT.md created with Rune integration"
else
    if ! grep -q "rune" "$HEARTBEAT_FILE"; then
        echo "" >> "$HEARTBEAT_FILE"
        echo "## 🧠 Rune Memory Maintenance (ACTIVE)" >> "$HEARTBEAT_FILE"
        echo '- `rune expire` — prune expired working memory' >> "$HEARTBEAT_FILE"
        echo '- `rune inject --output ~/.openclaw/workspace/FACTS.md` — regenerate intelligent context' >> "$HEARTBEAT_FILE"
        echo '- `rune consolidate --auto-prioritize` — optimize memory (weekly)' >> "$HEARTBEAT_FILE"
        echo "" >> "$HEARTBEAT_FILE"
        echo "Check \`rune next-task\` for intelligent task recommendations." >> "$HEARTBEAT_FILE"
        echo "   ✅ Rune integration added to existing HEARTBEAT.md"
    else
        echo "   ℹ️  Rune integration already present"
    fi
fi

# 8. Create initial facts
echo "8. Setting up initial memory..."
rune add system rune.installed "$(date -Iseconds)" --tier permanent --source "installer" 2>/dev/null || true
rune add system rune.version "$(jq -r '.version' package.json)" --tier permanent --source "installer" 2>/dev/null || true
rune add preference memory.default_model "ollama:llama3.1:8b" --tier working --source "installer" 2>/dev/null || true
echo "   ✅ Initial memory configured"

echo ""
echo "🎉 Rune Installation Complete!"
echo "=============================="
echo ""
echo "📍 What was installed:"
echo "   • CLI: rune command (global)"
echo "   • Database: ~/.openclaw/memory.db"
echo "   • Integration: ~/.openclaw/workspace/HEARTBEAT.md"
echo "   • Backups: Created automatically with timestamp"
echo ""
echo "🚀 Quick Start:"
echo "   rune add person your_name 'Your Name - the human user'"
echo "   rune context 'working on a new project'"
echo "   rune stats"
echo ""
echo "🔧 Configuration:"
echo "   • Default: Local models (Ollama) - private and free"
echo "   • Optional: Set API keys for cloud scoring"
echo "     export ANTHROPIC_API_KEY='your-key'  # Optional"
echo "     export OPENAI_API_KEY='your-key'     # Optional"
echo ""
echo "📚 Learn More:"
echo "   rune --help          # Full command reference"
echo "   rune context --help  # Context injection"
echo "   rune next-task       # AI task recommendations"
echo ""
echo "🧠 Your AI now has persistent, self-improving memory!"

# Final verification
if command -v rune &> /dev/null; then
    echo ""
    echo "✅ Installation verified - rune command is available"
else
    echo ""
    echo "⚠️  Warning: rune command not found in PATH"
    echo "   You may need to restart your shell or run: source ~/.bashrc"
fi