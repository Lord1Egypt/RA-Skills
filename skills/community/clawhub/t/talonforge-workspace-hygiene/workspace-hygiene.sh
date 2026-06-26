#!/bin/bash
# workspace-hygiene.sh — Auto-cleanup, runs daily via cron
# Keeps boot files lean, archives stale files, enforces limits

WORKSPACE="/root/.openclaw/workspace"
ARCHIVE="$WORKSPACE/memory/archive"
TODAY=$(date +%Y-%m-%d)
LOG="$WORKSPACE/memory/$TODAY.md"

mkdir -p "$ARCHIVE/frames" "$ARCHIVE/media" "$ARCHIVE/day-fragments"

trim_count=0
archive_count=0
lines_removed=0

# === 1. Root workspace: no junk files ===
# Move image files out of root
for ext in jpg jpeg png gif webp mp4 mp3 wav; do
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    mv "$f" "$ARCHIVE/frames/" 2>/dev/null
    ((archive_count++))
  done < <(find "$WORKSPACE" -maxdepth 1 -name "*.$ext" 2>/dev/null)
done

# Move package files out of root
for f in package.json package-lock.json; do
  if [ -f "$WORKSPACE/$f" ]; then
    mv "$WORKSPACE/$f" "$ARCHIVE/" 2>/dev/null
    ((archive_count++))
  fi
done

# === 2. MEMORY.md: trim action log if >5 entries ===
if [ -f "$WORKSPACE/MEMORY.md" ]; then
  mem_lines=$(wc -l < "$WORKSPACE/MEMORY.md")
  if [ "$mem_lines" -gt 80 ]; then
    # Archive excess, keep first 80 lines
    tail -n +81 "$WORKSPACE/MEMORY.md" >> "$ARCHIVE/memory-overflow-$TODAY.md" 2>/dev/null
    head -n 80 "$WORKSPACE/MEMORY.md" > "$WORKSPACE/MEMORY.md.tmp"
    mv "$WORKSPACE/MEMORY.md.tmp" "$WORKSPACE/MEMORY.md"
    ((lines_removed += mem_lines - 80))
    ((trim_count++))
  fi
fi

# === 3. AGENTS.md: trim if over 50 lines ===
if [ -f "$WORKSPACE/AGENTS.md" ]; then
  agent_lines=$(wc -l < "$WORKSPACE/AGENTS.md")
  if [ "$agent_lines" -gt 50 ]; then
    tail -n +51 "$WORKSPACE/AGENTS.md" >> "$ARCHIVE/agents-overflow-$TODAY.md" 2>/dev/null
    head -n 50 "$WORKSPACE/AGENTS.md" > "$WORKSPACE/AGENTS.md.tmp"
    mv "$WORKSPACE/AGENTS.md.tmp" "$WORKSPACE/AGENTS.md"
    ((lines_removed += agent_lines - 50))
    ((trim_count++))
  fi
fi

# === 4. Archive daily notes older than 3 days ===
cutoff=$(date -d "-3 days" +%Y-%m-%d 2>/dev/null || date -v-3d +%Y-%m-%d 2>/dev/null)
if [ -n "$cutoff" ]; then
  for f in "$WORKSPACE"/memory/20*.md; do
    [ ! -f "$f" ] && continue
    fname=$(basename "$f" .md)
    # Extract date prefix (YYYY-MM-DD)
    fdate=$(echo "$fname" | grep -oP '^\d{4}-\d{2}-\d{2}')
    [ -z "$fdate" ] && continue
    # Skip today's
    [ "$fdate" = "$TODAY" ] && continue
    # Archive if older than cutoff
    if [[ "$fdate" < "$cutoff" ]]; then
      mv "$f" "$ARCHIVE/" 2>/dev/null
      ((archive_count++))
    fi
  done
fi

# === 5. Archive stale memory/ files (not updated in 7+ days) ===
for f in "$WORKSPACE"/memory/*.md; do
  [ ! -f "$f" ] && continue
  fname=$(basename "$f")
  # Skip daily notes (handled above) and today's
  [[ "$fname" == "$TODAY"* ]] && continue
  [[ "$fname" == 20* ]] && continue
  # Check modification age
  mtime=$(stat -c %Y "$f" 2>/dev/null)
  now=$(date +%s)
  age_days=$(( (now - mtime) / 86400 ))
  if [ "$age_days" -gt 7 ]; then
    mv "$f" "$ARCHIVE/" 2>/dev/null
    ((archive_count++))
  fi
done

# === 6. Consolidate multiple daily note fragments ===
for date_dir in "$WORKSPACE"/memory/; do
  fragments=("$date_dir"$TODAY*.md)
  if [ ${#fragments[@]} -gt 1 ]; then
    # Keep the main one, archive fragments
    for f in "${fragments[@]}"; do
      fname=$(basename "$f")
      [ "$fname" = "$TODAY.md" ] && continue
      mv "$f" "$ARCHIVE/day-fragments/" 2>/dev/null
      ((archive_count++))
    done
  fi
done

# === 7. Remove empty files ===
find "$WORKSPACE/memory" -maxdepth 1 -name "*.md" -size -10c -delete 2>/dev/null

# === 8. Calculate boot load ===
boot_total=0
for f in AGENTS.md SOUL.md STATE.md MEMORY.md IDENTITY.md USER.md TOOLS.md HEARTBEAT.md; do
  n=$(wc -l < "$WORKSPACE/$f" 2>/dev/null || echo 0)
  boot_total=$((boot_total + n))
done

# === 9. Log ===
{
  echo ""
  echo "## Workspace Hygiene ($(date +%H:%M))"
  echo "- Trimmed: $trim_count files, $lines_removed lines removed"
  echo "- Archived: $archive_count files"
  echo "- Boot load: $boot_total lines"
  if [ "$archive_count" -gt 0 ] || [ "$trim_count" -gt 0 ]; then
    echo "- Status: CLEANED"
  else
    echo "- Status: CLEAN (no action needed)"
  fi
} >> "$LOG"

echo "Hygiene run complete: $trim_count trimmed, $archive_count archived, $boot_total boot lines"