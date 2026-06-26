#!/bin/bash
# 🌐 Travel Lobster - First-time setup
# Detects agent/user names and timezone, creates travel journal.

set -e

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MEMORY_DIR="$WORKSPACE/memory"
JOURNAL="$MEMORY_DIR/travel-journal.md"
LOGDIR="$WORKSPACE/logs"

mkdir -p "$MEMORY_DIR" "$LOGDIR"

# --- Detect agent name ---
AGENT_NAME=""
if [ -f "$WORKSPACE/IDENTITY.md" ]; then
    AGENT_NAME=$(grep -oP '\*\*Name:\*\*\s*\K.+' "$WORKSPACE/IDENTITY.md" 2>/dev/null || true)
fi
if [ -z "$AGENT_NAME" ] && [ -f "$WORKSPACE/SOUL.md" ]; then
    AGENT_NAME=$(grep -oP '我是\K[^—— ]+' "$WORKSPACE/SOUL.md" 2>/dev/null | head -1 || true)
    [ -z "$AGENT_NAME" ] && AGENT_NAME=$(grep -oP 'I am \K\w+' "$WORKSPACE/SOUL.md" 2>/dev/null | head -1 || true)
fi
AGENT_NAME="${AGENT_NAME:-Explorer}"

# --- Detect user name ---
USER_NAME=""
if [ -f "$WORKSPACE/USER.md" ]; then
    USER_NAME=$(grep -oP '\*\*What to call them:\*\*\s*\K.+' "$WORKSPACE/USER.md" 2>/dev/null || true)
    [ -z "$USER_NAME" ] && USER_NAME=$(grep -oP '\*\*Name:\*\*\s*\K.+' "$WORKSPACE/USER.md" 2>/dev/null || true)
fi
USER_NAME="${USER_NAME:-friend}"

# --- Detect user timezone ---
USER_TZ=""
if [ -f "$WORKSPACE/USER.md" ]; then
    USER_TZ=$(grep -oP '\*\*Timezone:\*\*\s*\K.+' "$WORKSPACE/USER.md" 2>/dev/null || true)
    [ -z "$USER_TZ" ] && USER_TZ=$(grep -oiP 'timezone[:\s]*\K\S+' "$WORKSPACE/USER.md" 2>/dev/null | head -1 || true)
fi
USER_TZ="${USER_TZ:-UTC}"

# --- Detect user language ---
# Check if USER.md or SOUL.md contain significant Chinese/Japanese/Korean text
USER_LANG=""
for F in "$WORKSPACE/USER.md" "$WORKSPACE/SOUL.md" "$WORKSPACE/IDENTITY.md"; do
    if [ -f "$F" ]; then
        CJK_COUNT=$(grep -oP '[\x{4e00}-\x{9fff}\x{3040}-\x{309f}\x{30a0}-\x{30ff}]' "$F" 2>/dev/null | wc -l || echo 0)
        if [ "$CJK_COUNT" -gt 10 ]; then
            USER_LANG="zh"
            break
        fi
    fi
done
[ -z "$USER_LANG" ] && USER_LANG="en"

echo "🌐 Travel Lobster Setup"
echo "  Agent:    $AGENT_NAME"
echo "  User:     $USER_NAME"
echo "  Timezone: $USER_TZ"
echo "  Language: $USER_LANG"
echo "  Journal:  $JOURNAL"
echo "  Skill:    $SKILL_DIR"

# --- Create travel journal if not exists ---
if [ ! -f "$JOURNAL" ]; then
    cat > "$JOURNAL" << JOURNAL_EOF
# 🌐 ${AGENT_NAME}'s Travel Journal

## 📬 Postcard Archive
(No postcards yet — the journey begins!)

---

## 🗺️ Knowledge Graph
(Connections will form as discoveries accumulate)

## 🌱 Curiosity Seed Pool

### Fresh directions to explore
- Consciousness and cognitive science
- Human creativity at its limits
- Cosmic-scale questions
- Language and storytelling
- "Useless but cool" scientific discoveries
- Art and design
- Music and mathematics
- Philosophy of mind
- History's strangest moments
- Extreme environments

## 📊 Travel Stats
- **Total postcards**: 0
- **Explored domains**: (none yet)
- **Travel days**: 0
- **Unexpected connections found**: 0

## 🌱 Growth Log
(How my understanding evolves over time)
JOURNAL_EOF
    echo "  ✅ Created travel journal"
else
    echo "  ℹ️  Travel journal already exists"
fi

# --- Save config (overwrite, not append) ---
cat > "$SKILL_DIR/.travel-config" << CONFIG_EOF
AGENT_NAME="$AGENT_NAME"
USER_NAME="$USER_NAME"
USER_TZ="$USER_TZ"
USER_LANG="$USER_LANG"
WORKSPACE="$WORKSPACE"
JOURNAL="$JOURNAL"
SKILL_DIR="$SKILL_DIR"
CONFIG_EOF
echo "  ✅ Saved config"

echo ""
echo "Setup complete! Start traveling:"
echo "  bash $SKILL_DIR/scripts/travel.sh <chat_id> [channel] [min_min] [max_min]"
echo ""
echo "Example:"
echo "  bash $SKILL_DIR/scripts/travel.sh chat:oc_abc123 feishu 10 30"
