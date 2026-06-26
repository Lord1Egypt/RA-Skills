#!/bin/bash
# cursor_doctor.sh - Diagnose environment

echo "=== Use Cursor Environment Check ==="
echo ""

# Check tmux
echo -n "tmux: "
if command -v tmux &> /dev/null; then
    TMUX_VER=$(tmux -V 2>&1 || echo "unknown")
    echo "✓ installed ($TMUX_VER)"
else
    echo "✗ NOT FOUND - run: sudo apt install tmux (or brew install tmux)"
fi

# Check Cursor CLI
echo -n "Cursor CLI: "
if command -v agent &> /dev/null; then
    AGENT_VER=$(agent --version 2>&1 || echo "unknown")
    echo "✓ installed ($AGENT_VER)"
elif command -v cursor-agent &> /dev/null; then
    AGENT_VER=$(cursor-agent --version 2>&1 || echo "unknown")
    echo "✓ installed ($AGENT_VER) (legacy command)"
else
    echo "✗ NOT FOUND - run: curl https://cursor.com/install -fsS | bash"
fi

# Check authentication
echo -n "Authentication: "
if [ -n "$CURSOR_API_KEY" ]; then
    echo "✓ CURSOR_API_KEY set"
elif [ -f "$HOME/.cursor/cli-config.json" ]; then
    # Check if authInfo exists in cli-config.json
    if grep -q "authInfo" "$HOME/.cursor/cli-config.json" 2>/dev/null; then
        # Redact email for privacy (show only domain)
        EMAIL=$(grep -o '"email": "[^"]*"' "$HOME/.cursor/cli-config.json" | head -1 | cut -d'"' -f4)
        DOMAIN=$(echo "$EMAIL" | cut -d'@' -f2)
        echo "✓ logged in (***@$DOMAIN)"
    else
        echo "⚠ NOT FOUND - run: agent login"
    fi
elif [ -f "$HOME/.cursor/credentials" ]; then
    echo "✓ credentials file exists"
else
    echo "⚠ NOT FOUND - run: agent login"
fi

# Check node/npm (optional)
echo -n "Node.js: "
if command -v node &> /dev/null; then
    NODE_VER=$(node --version)
    echo "✓ $NODE_VER"
else
    echo "○ not required but recommended"
fi

# Check git (optional)
echo -n "Git: "
if command -v git &> /dev/null; then
    GIT_VER=$(git --version)
    echo "✓ $GIT_VER"
else
    echo "○ not required but recommended"
fi

echo ""
echo "=== Summary ==="

ISSUES=0
if ! command -v tmux &> /dev/null; then
    echo "❌ tmux is required for background tasks"
    ISSUES=$((ISSUES + 1))
fi

if ! command -v agent &> /dev/null && ! command -v cursor-agent &> /dev/null; then
    echo "❌ Cursor CLI is required"
    ISSUES=$((ISSUES + 1))
fi

if [ -z "$CURSOR_API_KEY" ] && [ ! -f "$HOME/.cursor/cli-config.json" ]; then
    echo "❌ Authentication required - run: agent login"
    ISSUES=$((ISSUES + 1))
elif [ -f "$HOME/.cursor/cli-config.json" ] && ! grep -q "authInfo" "$HOME/.cursor/cli-config.json" 2>/dev/null; then
    echo "❌ Authentication required - run: agent login"
    ISSUES=$((ISSUES + 1))
fi

if [ $ISSUES -eq 0 ]; then
    echo "✅ All checks passed! Ready to use Cursor."
else
    echo "⚠️  $ISSUES issue(s) found. Please fix them above."
fi
