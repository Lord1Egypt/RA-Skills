#!/bin/bash
# summarize skill — multi-platform one-line installer
# curl -sL https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.sh | bash

set -e

REPO_SSH="git@github.com:gtbwpkwjnb-alt/summarize-skill.git"
REPO_HTTPS="https://github.com/gtbwpkwjnb-alt/summarize-skill.git"

# --- Platform auto-detect ---
detect_platform() {
    # ZCode (默认 ~/.agents/skills/)
    if [ -d "$HOME/.agents/skills" ] || [ -n "$ZCODE_CLI_VERSION" ]; then
        echo "$HOME/.agents/skills/summarize"
        return
    fi
    # CodeBuddy
    if [ -d "$HOME/.codebuddy/skills" ]; then
        echo "$HOME/.codebuddy/skills/summarize"
        return
    fi
    # Claude Code
    if [ -d "$HOME/.claude/skills" ] || [ -d "$HOME/.claude/plugins" ]; then
        echo "$HOME/.claude/skills/summarize"
        return
    fi
    # Codex (OpenAI)
    if [ -d "$HOME/.codex/skills" ] || [ -d "$HOME/.codex" ]; then
        echo "$HOME/.codex/skills/summarize"
        return
    fi
    # Reasonix
    if [ -d "$HOME/.reasonix/skills" ]; then
        echo "$HOME/.reasonix/skills/summarize"
        return
    fi
    # Fallback: generic agent-skills
    echo "$HOME/.agent-skills/summarize"
}

INSTALL_DIR=$(detect_platform)

echo "📦 summarize skill installer"
echo "   Target: $INSTALL_DIR"

if [ -d "$INSTALL_DIR" ]; then
    echo "   Already installed at $INSTALL_DIR"
    echo "🔄 Updating to latest version..."
    cd "$INSTALL_DIR"
    git pull --rebase 2>/dev/null || { cd "$HOME" && rm -rf "$INSTALL_DIR" && git clone "$REPO_SSH" "$INSTALL_DIR" 2>/dev/null || git clone "$REPO_HTTPS" "$INSTALL_DIR"; }
else
    echo "   Cloning into $INSTALL_DIR ..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone "$REPO_SSH" "$INSTALL_DIR" 2>/dev/null || git clone "$REPO_HTTPS" "$INSTALL_DIR"
fi

echo ""
echo "✅ summarize skill installed!  v$(cat "$INSTALL_DIR/VERSION")"
echo "   Path:    $INSTALL_DIR"
echo "   Trigger: 总结 / summarize"
echo ""
echo "📊 Manage:"
echo "   Update:  cd $INSTALL_DIR && git pull"
echo "   Issues:  https://github.com/gtbwpkwjnb-alt/summarize-skill/issues"
