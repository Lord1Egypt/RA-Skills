#!/bin/bash
# Workspace Trash — soft-delete for workspace & agent workspace files
# Usage: trash.sh <action> [args...]
#   move <file|dir> [file|dir...]  — move items to trash
#   list                           — list trash contents
#   restore <item>                 — restore from trash to original location
#   empty                          — permanently delete all trash contents
#   size                           — show trash size
#
# Supports cross-filesystem moves (agent workspaces on different mounts).
# All trashed items land in the primary workspace's .trash/ directory.
#
# Dependencies: node (Node.js), standard POSIX utilities (mv, cp, rm, find, awk, date, basename, dirname)
# Environment:
#   OPENCLAW_HOME      — OpenClaw root directory (default: $HOME/.openclaw)
#   OPENCLAW_WORKSPACE — primary workspace directory (default: $OPENCLAW_HOME/workspace)
#
# Security:
# - Only files under $OPENCLAW_HOME can be trashed (symlinks resolved before check)
# - All user-provided paths are passed to Node.js via environment variables, never string interpolation
# - The "empty" action uses rm -rf to permanently delete trash contents — this is irreversible

set -euo pipefail

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$OPENCLAW_HOME/workspace}"
TRASH_DIR="$WORKSPACE/.trash"
MANIFEST="$TRASH_DIR/.manifest.json"

mkdir -p "$TRASH_DIR"
[ -f "$MANIFEST" ] || echo '[]' > "$MANIFEST"

# Resolve a path to its real absolute path (follows symlinks)
resolve_path() {
  local target="$1"
  if [ -d "$target" ]; then
    (cd "$target" && pwd -P)
  elif [ -e "$target" ]; then
    local dir
    dir="$(cd "$(dirname "$target")" && pwd -P)"
    echo "$dir/$(basename "$target")"
  else
    # For non-existent paths, resolve parent
    local dir
    dir="$(cd "$(dirname "$target")" 2>/dev/null && pwd -P)" || return 1
    echo "$dir/$(basename "$target")"
  fi
}

# Cross-filesystem safe move: try mv first, fall back to cp+rm
safe_move() {
  local src="$1"
  local dest="$2"
  if mv -- "$src" "$dest" 2>/dev/null; then
    return 0
  fi
  # mv failed (likely cross-filesystem) — use cp + rm
  if cp -a -- "$src" "$dest" 2>/dev/null; then
    rm -rf -- "$src" 2>/dev/null
    return 0
  fi
  return 1
}

action="${1:-help}"
shift 2>/dev/null || true

case "$action" in
  move)
    if [ $# -eq 0 ]; then
      echo "Usage: trash.sh move <file|dir> [file|dir...]"
      exit 1
    fi
    for item in "$@"; do
      if [ ! -e "$item" ]; then
        echo "⚠️  Not found: $item"
        continue
      fi

      # Resolve to real absolute path (follows symlinks to prevent traversal)
      abs_path="$(resolve_path "$item")"
      real_home="$(resolve_path "$OPENCLAW_HOME")"

      # Security: only allow trashing files inside ~/.openclaw/
      case "$abs_path" in
        "$real_home"/*)
          ;;
        "$real_home")
          echo "❌ Refusing to trash the OpenClaw root directory"
          continue
          ;;
        *)
          echo "❌ Refusing to trash file outside OpenClaw: $abs_path"
          continue
          ;;
      esac

      # Don't trash the trash
      real_trash="$(resolve_path "$TRASH_DIR")"
      case "$abs_path" in
        "$real_trash"/*)
          echo "❌ Cannot trash items already in trash: $abs_path"
          continue
          ;;
      esac

      # Generate unique trash name (timestamp + basename)
      ts=$(date +%s%N 2>/dev/null || date +%s)
      base=$(basename -- "$item")
      trash_name="${ts}_${base}"

      # Ensure unique
      while [ -e "$TRASH_DIR/$trash_name" ]; do
        ts=$((ts + 1))
        trash_name="${ts}_${base}"
      done

      if safe_move "$abs_path" "$TRASH_DIR/$trash_name"; then
        # Detect if it's a directory after move
        is_dir="false"
        [ -d "$TRASH_DIR/$trash_name" ] && is_dir="true"

        # Add to manifest — all data passed via env vars, not interpolation
        TRASH_MANIFEST="$MANIFEST" \
        TRASH_ITEM_NAME="$trash_name" \
        TRASH_ORIG_PATH="$abs_path" \
        TRASH_IS_DIR="$is_dir" \
        node -e '
          const fs = require("fs");
          const m = JSON.parse(fs.readFileSync(process.env.TRASH_MANIFEST, "utf8"));
          m.push({
            trashName: process.env.TRASH_ITEM_NAME,
            originalPath: process.env.TRASH_ORIG_PATH,
            deletedAt: new Date().toISOString(),
            isDir: process.env.TRASH_IS_DIR === "true"
          });
          fs.writeFileSync(process.env.TRASH_MANIFEST, JSON.stringify(m, null, 2));
        '
        echo "🗑️  Trashed: $item → .trash/$trash_name"
      else
        echo "❌ Failed to trash: $item"
      fi
    done
    ;;

  list|view)
    TRASH_MANIFEST="$MANIFEST" node -e '
      const fs = require("fs");
      const m = JSON.parse(fs.readFileSync(process.env.TRASH_MANIFEST, "utf8"));
      if (m.length === 0) { console.log("🗑️  Trash is empty."); process.exit(0); }
      console.log("🗑️  Trash contents (" + m.length + " items):");
      console.log("");
      m.forEach((e, i) => {
        const age = Math.round((Date.now() - new Date(e.deletedAt).getTime()) / 3600000);
        const ageStr = age < 1 ? "<1h ago" : age < 24 ? age + "h ago" : Math.round(age/24) + "d ago";
        const type = e.isDir ? "📁" : "📄";
        const fromAgent = e.originalPath.includes("/workspace-") ? " [agent]" : "";
        console.log("  " + (i+1) + ". " + type + " " + e.trashName.replace(/^\d+_/, "") + "  (" + ageStr + ")" + fromAgent);
        console.log("     Original: " + e.originalPath);
        console.log("     Trash ID: " + e.trashName);
      });
    '
    ;;

  restore)
    if [ -z "${1:-}" ]; then
      echo "Usage: trash.sh restore <trash_name or index>"
      exit 1
    fi
    target="$1"
    TRASH_MANIFEST="$MANIFEST" \
    TRASH_DIR_PATH="$TRASH_DIR" \
    TRASH_TARGET="$target" \
    node -e '
      const fs = require("fs");
      const path = require("path");
      const manifest = process.env.TRASH_MANIFEST;
      const trashDir = process.env.TRASH_DIR_PATH;
      const target = process.env.TRASH_TARGET;

      const m = JSON.parse(fs.readFileSync(manifest, "utf8"));
      let idx = parseInt(target, 10) - 1;
      if (isNaN(idx) || idx < 0 || idx >= m.length) {
        idx = m.findIndex(e => e.trashName === target || e.trashName.replace(/^\d+_/, "") === target);
      }
      if (idx === -1 || idx >= m.length) {
        console.log("❌ Not found in trash: " + target);
        process.exit(1);
      }
      const entry = m[idx];
      const trashPath = path.join(trashDir, entry.trashName);
      const origDir = path.dirname(entry.originalPath);

      // Ensure original directory exists
      fs.mkdirSync(origDir, { recursive: true });

      // Check if original location is occupied
      if (fs.existsSync(entry.originalPath)) {
        console.log("⚠️  Original location occupied: " + entry.originalPath);
        console.log("   Rename or remove it first, then retry.");
        process.exit(1);
      }

      // Use spawnSync to avoid shell interpretation of filenames
      const { spawnSync } = require("child_process");

      // Try mv first, fall back to cp+rm for cross-filesystem
      let result = spawnSync("mv", ["--", trashPath, entry.originalPath], { stdio: "pipe" });
      if (result.status !== 0) {
        result = spawnSync("cp", ["-a", "--", trashPath, entry.originalPath], { stdio: "pipe" });
        if (result.status !== 0) {
          console.log("❌ Failed to restore: cp failed with status " + result.status);
          process.exit(1);
        }
        const rmResult = spawnSync("rm", ["-rf", "--", trashPath], { stdio: "pipe" });
        if (rmResult.status !== 0) {
          console.log("⚠️  Restored but failed to clean trash copy");
        }
      }

      m.splice(idx, 1);
      fs.writeFileSync(manifest, JSON.stringify(m, null, 2));
      console.log("✅ Restored: " + entry.originalPath);
    '
    ;;

  empty)
    TRASH_MANIFEST="$MANIFEST" node -e '
      const fs = require("fs");
      const m = JSON.parse(fs.readFileSync(process.env.TRASH_MANIFEST, "utf8"));
      if (m.length === 0) { console.log("🗑️  Trash is already empty."); process.exit(0); }
      console.log("🗑️  Permanently deleting " + m.length + " items...");
    '
    # Delete all items except manifest — this is irreversible
    find "$TRASH_DIR" -mindepth 1 -not -name '.manifest.json' -exec rm -rf {} + 2>/dev/null || true
    echo '[]' > "$MANIFEST"
    echo "✅ Trash emptied."
    ;;

  size)
    COUNT=$(TRASH_MANIFEST="$MANIFEST" node -e 'console.log(JSON.parse(require("fs").readFileSync(process.env.TRASH_MANIFEST,"utf8")).length)' 2>/dev/null || echo 0)
    if [ "$COUNT" -gt 0 ] 2>/dev/null; then
      SIZE=$(find "$TRASH_DIR" -type f -not -name '.manifest.json' -printf '%s\n' 2>/dev/null | awk '{s+=$1}END{
        if(s>1073741824) printf "%.1fG\n",s/1073741824;
        else if(s>1048576) printf "%.0fM\n",s/1048576;
        else if(s>1024) printf "%.0fK\n",s/1024;
        else printf "%dB\n",s}')
      echo "🗑️  Trash: $COUNT items, $SIZE"
    else
      echo "🗑️  Trash is empty."
    fi
    ;;

  help|*)
    echo "Workspace Trash — soft-delete for OpenClaw files"
    echo ""
    echo "Usage: trash.sh <action> [args...]"
    echo ""
    echo "Actions:"
    echo "  move <file|dir>...   Move items to trash (supports cross-filesystem)"
    echo "  list                 List trash contents"
    echo "  restore <id|index>   Restore item to original location"
    echo "  empty                Permanently delete all trash (irreversible!)"
    echo "  size                 Show trash size"
    echo ""
    echo "Scope: any file under ~/.openclaw/ (primary + agent workspaces)"
    echo "Symlinks are resolved before scope check to prevent traversal."
    echo "Slash commands: /trash, /trash:view, /trash:empty, /trash:restore"
    ;;
esac
