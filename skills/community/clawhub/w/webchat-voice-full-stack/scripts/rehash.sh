#!/usr/bin/env bash
set -euo pipefail

# Regenerate checksums.sha256 after manual audit of sub-skill scripts.
# Run this ONLY after reviewing changes — it updates the trusted baseline.

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
SKILLS_DIR="${SKILLS_DIR:-$WORKSPACE/skills}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECKSUMS="$SCRIPT_DIR/checksums.sha256"

SUB_SKILLS=(
  "faster-whisper-local-service"
  "webchat-https-proxy"
  "webchat-voice-gui"
)

echo "# SHA256 checksums for sub-skill scripts" > "$CHECKSUMS"
echo "# Generated: $(date -I)" >> "$CHECKSUMS"
echo "# Verify with: VERIFY_ONLY=true bash scripts/deploy.sh" >> "$CHECKSUMS"
echo "# If a checksum fails, the sub-skill was modified after installation." >> "$CHECKSUMS"
echo "# Re-audit before deploying." >> "$CHECKSUMS"

count=0
for skill in "${SUB_SKILLS[@]}"; do
  script_dir="$SKILLS_DIR/$skill/scripts"
  if [[ ! -d "$script_dir" ]]; then
    echo "WARNING: $skill/scripts not found, skipping" >&2
    continue
  fi
  while IFS= read -r -d '' script; do
    rel_path="${script#"$SKILLS_DIR/"}"
    hash="$(sha256sum "$script" | awk '{print $1}')"
    echo "$hash  $rel_path" >> "$CHECKSUMS"
    ((count++))
  done < <(find "$script_dir" -type f -name '*.sh' -print0 | sort -z)
done

echo ""
echo "Updated $CHECKSUMS with $count script(s)."
echo "Commit this change to record the new trusted baseline."
