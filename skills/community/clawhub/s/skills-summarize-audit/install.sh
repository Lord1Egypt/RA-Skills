#!/bin/bash
# skills-summarize-audit installer — 手动安装，见 README.md

set -e

REPO_SSH="git@github.com:gtbwpkwjnb-alt/skills-summarize-audit-skill.git"
REPO_HTTPS="https://github.com/gtbwpkwjnb-alt/skills-summarize-audit-skill.git"

detect_platform() {
    if [ -d "$HOME/.zcode/skills" ] || [ -n "$ZCODE_CLI_VERSION" ]; then
        echo "$HOME/.zcode/skills/skills-summarize-audit"
        return
    fi
    if [ -d "$HOME/.claude/skills" ]; then
        echo "$HOME/.claude/skills/skills-summarize-audit"
        return
    fi
    if [ -d "$HOME/.codex/skills" ]; then
        echo "$HOME/.codex/skills/skills-summarize-audit"
        return
    fi
    if [ -d "$HOME/.cursor/agent-skills" ]; then
        echo "$HOME/.cursor/agent-skills/skills-summarize-audit"
        return
    fi
    echo "$HOME/.agent-skills/skills-summarize-audit"
}

INSTALL_DIR=$(detect_platform)

echo "skills-summarize-audit installer"
echo "   Target: $INSTALL_DIR"

if [ "${1:-}" = "--dry-run" ]; then
    echo "   Dry run: no filesystem or network changes will be made."
    if [ -d "$INSTALL_DIR" ]; then
        echo "   Would verify a clean Git worktree, then run: git pull --ff-only"
    else
        echo "   Would clone from SSH, then HTTPS fallback if SSH is unavailable."
    fi
    exit 0
fi

if [ -d "$INSTALL_DIR" ]; then
    echo "   Already installed. Updating..."
    cd "$INSTALL_DIR"
    if [ -n "$(git status --porcelain)" ]; then
        echo "Local changes detected. Commit, stash, or back up the directory before updating." >&2
        exit 1
    fi
    if ! git pull --ff-only; then
        echo "Update failed. The existing installation was preserved; resolve the Git history manually." >&2
        exit 1
    fi
else
    echo "   Cloning..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone "$REPO_SSH" "$INSTALL_DIR" 2>/dev/null || git clone "$REPO_HTTPS" "$INSTALL_DIR"
fi

echo ""
echo "skills-summarize-audit installed!  v$(cat "$INSTALL_DIR/VERSION")"
echo "   Trigger: skills-summarize-audit / 技能审查 / 技能总结"
echo "   Issues:  https://github.com/gtbwpkwjnb-alt/skills-summarize-audit-skill/issues"
