#!/bin/bash
set -euo pipefail

# trigger_agent.sh - Detect and invoke agent CLI to process pending transcription results
# Usage: trigger_agent.sh <pending_json_file> <agent_cli_config> [skill_dir]
#   agent_cli_config: "auto" | "opencode" | "claude" | "codex" | "gemini" | "none"

PENDING_FILE="$1"
AGENT_CLI="${2:-auto}"
SKILL_DIR="${3:-$(cd "$(dirname "$0")/.." && pwd)}"

if [ "$AGENT_CLI" = "none" ]; then
    exit 0
fi

# Detect which agent CLI is available
detect_agent() {
    for cli in opencode claude codex gemini; do
        if command -v "$cli" >/dev/null 2>&1; then
            echo "$cli"
            return 0
        fi
    done
    echo ""
    return 1
}

if [ "$AGENT_CLI" = "auto" ]; then
    AGENT_CLI=$(detect_agent) || true
    if [ -z "$AGENT_CLI" ]; then
        echo "[record2note] No agent CLI found (opencode/claude/codex/gemini). Skipping agent trigger."
        exit 0
    fi
    echo "[record2note] Auto-detected agent CLI: $AGENT_CLI"
fi

if ! command -v "$AGENT_CLI" >/dev/null 2>&1; then
    echo "[record2note] Agent CLI '$AGENT_CLI' not found. Skipping agent trigger."
    exit 0
fi

# Read config to build context
CONFIG="$SKILL_DIR/config.json"
if [ ! -f "$CONFIG" ]; then
    echo "[record2note] Config not found at $CONFIG. Skipping agent trigger."
    exit 0
fi

# Select note template based on note_mode
NOTE_MODE=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('note_mode','markdown'))" 2>/dev/null || echo "markdown")
if [ "$NOTE_MODE" = "obsidian" ]; then
    TEMPLATE="$SKILL_DIR/templates/note-template-obsidian.md"
else
    TEMPLATE="$SKILL_DIR/templates/note-template.md"
fi
if [ ! -f "$TEMPLATE" ]; then
    echo "[record2note] Template not found at $TEMPLATE. Skipping agent trigger."
    exit 0
fi

# Build self-contained prompt with all context
PROMPT=$(python3 - "$PENDING_FILE" "$CONFIG" "$TEMPLATE" << 'PYEOF'
import json, sys

pending_file = sys.argv[1]
config_path = sys.argv[2]
template_path = sys.argv[3]

with open(config_path, encoding='utf-8') as f:
    config = json.load(f)

with open(template_path, encoding='utf-8') as f:
    template = f.read()

vault = config.get('obsidian_vault', '')
subdir = config.get('obsidian_subdir', 'Journal/Transcripts')
archive_dir = config.get('archive_dir', '~/Recordings/archive')
watch_dir = config.get('watch_dir', '~/Recordings/raw')
note_mode = config.get('note_mode', 'markdown')
obsidian_index = config.get('obsidian_index', 'Recording Index')

prompt = f"""record2note has a new transcription result to process.

Pending file: {pending_file}
This JSON file contains `metadata` and `transcript` fields.

Please process this recording with the following steps:

1. Read the pending JSON file and extract `metadata` (`title_candidate`, `date`, `duration`, `source`, `speakers`, `language`, `note_mode`, `obsidian_index`) and `transcript`
2. Generate a structured note from the transcript:
   - Create a concise title (15 characters or less)
   - Write a 100-200 character summary that captures the core content
   - List 3-5 key points
   - If there are actionable items, format them as checkboxes
   - Add 1-3 tags
3. **Correct transcription errors**: speech recognition may produce homophone mistakes; correct them when context makes the intended meaning clear
4. **Transcript formatting**: organize the transcript into paragraphs and prefix each paragraph with its starting timestamp in `[MM:SS]` format; do not label every line
5. Use the following template to generate the final Markdown note and replace the variables (`{{{{title}}}}`, {{{{date}}}}, {{{{duration}}}}, {{{{source}}}}, {{{{speakers}}}}, {{{{language}}}}, {{{{tags}}}}, {{{{summary}}}}, {{{{keypoints}}}}, {{{{todos}}}}, {{{{transcript}}}}):

Template content:
{template}

6. Save the note to the Obsidian vault: {vault}/{subdir}/YYYY-MM-DD-<title>.md
7. Archive the original audio from the `source` path into the `{archive_dir}/YYYY-MM-DD/` directory
8. Update the note frontmatter `source` field to the archived path
9. Delete the original audio file from the watch directory (`source` path)
10. Delete the processed pending JSON file"""

if note_mode == 'obsidian':
    prompt += f"""

**Additional steps for Obsidian mode:**

11. Update the index page at `{vault}/{subdir}/{obsidian_index}.md`:
    - If the index page does not exist, create it:
      ```
      ---
      title: {obsidian_index}
      tags: [recording-index, recording]
      ---

      ## YYYY-MM-DD

      - [[YYYY-MM-DD-title]] - first sentence of the summary (50 characters or fewer)
      ```
    - If the index page already exists:
      - Find the `## YYYY-MM-DD` group for the matching date and append ` - [[YYYY-MM-DD-title]] - summary first sentence` below it
      - If there is no group for that date, insert a new `## YYYY-MM-DD` group near the top of the file after the frontmatter, sorted by date descending
      - Use the first sentence of the generated summary, limited to 50 characters
12. Ensure the note includes the `Index: [[{obsidian_index}]]` link (the template already exposes this variable)"""

print(prompt)
PYEOF
)

case "$AGENT_CLI" in
    opencode)
        echo "[record2note] Triggering opencode to process: $PENDING_FILE"
        nohup opencode run --title "record2note: $(basename "$PENDING_FILE")" "$PROMPT" >> /tmp/record2note-agent.log 2>&1 &
        ;;
    claude)
        echo "[record2note] Triggering claude to process: $PENDING_FILE"
        nohup claude -p --append-system-prompt "You are an assistant that processes voice transcription notes." "$PROMPT" >> /tmp/record2note-agent.log 2>&1 &
        ;;
    codex)
        echo "[record2note] Triggering codex to process: $PENDING_FILE"
        nohup codex "$PROMPT" >> /tmp/record2note-agent.log 2>&1 &
        ;;
    gemini)
        echo "[record2note] Triggering gemini to process: $PENDING_FILE"
        nohup gemini "$PROMPT" >> /tmp/record2note-agent.log 2>&1 &
        ;;
    *)
        echo "[record2note] Unknown agent CLI: $AGENT_CLI. Skipping." >&2
        exit 1
        ;;
esac

echo "[record2note] Agent triggered successfully (PID: $!)."
