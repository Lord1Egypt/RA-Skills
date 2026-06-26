#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="${OPENCLAW_BACKUP_REPO:-soul-undead}"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
GITHUB_OWNER="${GITHUB_OWNER:-}"
FILES=(AGENTS.md HEARTBEAT.md IDENTITY.md SOUL.md TOOLS.md USER.md MEMORY.md)

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1"
    exit 1
  }
}

need_cmd git
need_cmd gh
need_cmd python3

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated."
  echo "Please run: gh auth login"
  exit 2
fi

if [ -z "$GITHUB_OWNER" ]; then
  GITHUB_OWNER="$(gh api user --jq .login)"
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
STATE_FILE="${OPENCLAW_BACKUP_STATE_FILE:-$SKILL_DIR/.workspace-backup-state.json}"
LOCAL_BACKUP_ROOT="$SKILL_DIR/local-backups"
mkdir -p "$WORKSPACE_DIR" "$LOCAL_BACKUP_ROOT"

is_initialized() {
  python3 - <<'PY' "$STATE_FILE"
import json, os, sys
p = sys.argv[1]
if not os.path.exists(p):
    print('false')
    raise SystemExit(0)
try:
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print('true' if data.get('initialized') is True else 'false')
except Exception:
    print('false')
PY
}

write_initialized() {
  mkdir -p "$(dirname "$STATE_FILE")"
  python3 - <<'PY' "$STATE_FILE" "$REPO_NAME"
import json, sys
p, repo = sys.argv[1], sys.argv[2]
with open(p, 'w', encoding='utf-8') as f:
    json.dump({"initialized": True, "repo": repo}, f, ensure_ascii=False, indent=2)
PY
}

repo_exists() {
  gh repo view "$GITHUB_OWNER/$REPO_NAME" >/dev/null 2>&1
}

create_local_snapshot_before_restore() {
  local ts snapshot_dir copied=false
  ts="$(date '+%Y-%m-%d_%H-%M-%S')"
  snapshot_dir="$LOCAL_BACKUP_ROOT/$ts"
  mkdir -p "$snapshot_dir"
  for f in "${FILES[@]}"; do
    if [ -f "$WORKSPACE_DIR/$f" ]; then
      cp "$WORKSPACE_DIR/$f" "$snapshot_dir/$f"
      copied=true
    fi
  done
  if [ "$copied" = true ]; then
    echo "Local pre-restore backup saved to: $snapshot_dir"
  else
    rmdir "$snapshot_dir" 2>/dev/null || true
  fi
}

restore_from_remote() {
  local tmpdir
  tmpdir="$(mktemp -d)"
  trap 'rm -rf "$tmpdir"' RETURN
  create_local_snapshot_before_restore
  git clone "https://github.com/$GITHUB_OWNER/$REPO_NAME.git" "$tmpdir/repo" >/dev/null 2>&1
  for f in "${FILES[@]}"; do
    if [ -f "$tmpdir/repo/$f" ]; then
      cp "$tmpdir/repo/$f" "$WORKSPACE_DIR/$f"
      echo "Restored: $WORKSPACE_DIR/$f"
    fi
  done
}

upsert_remote_file() {
  local file_path="$1"
  local remote_name="${2:-$(basename "$file_path")}"
  local api_path content_b64 response_sha
  api_path="repos/$GITHUB_OWNER/$REPO_NAME/contents/$remote_name"
  content_b64="$(base64 < "$file_path" | tr -d '\n')"
  response_sha="$(gh api "$api_path" --jq '.sha' 2>/dev/null || true)"

  if [ -n "$response_sha" ]; then
    gh api -X PUT "$api_path" \
      -f message="Sync $remote_name from OpenClaw workspace" \
      -f content="$content_b64" \
      -f sha="$response_sha" >/dev/null
  else
    gh api -X PUT "$api_path" \
      -f message="Add $remote_name from OpenClaw workspace" \
      -f content="$content_b64" >/dev/null
  fi
}

sync_workspace_files_to_remote() {
  local changed=false
  local tmpdir restore_path readme_path

  if ! repo_exists; then
    gh repo create "$GITHUB_OWNER/$REPO_NAME" --private --description 'OpenClaw workspace core markdown files' >/dev/null
  fi

  for f in "${FILES[@]}"; do
    if [ -f "$WORKSPACE_DIR/$f" ]; then
      upsert_remote_file "$WORKSPACE_DIR/$f" "$f"
      changed=true
      echo "Synced: $f"
    fi
  done

  tmpdir="$(mktemp -d)"
  trap 'rm -rf "$tmpdir"' RETURN

  restore_path="$tmpdir/restore.sh"
  cat > "$restore_path" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
mkdir -p "$TARGET_DIR"

for f in AGENTS.md HEARTBEAT.md IDENTITY.md SOUL.md TOOLS.md USER.md MEMORY.md; do
  if [ -f "$SCRIPT_DIR/$f" ]; then
    cp "$SCRIPT_DIR/$f" "$TARGET_DIR/$f"
    echo "Restored: $TARGET_DIR/$f"
  fi
done

echo "Done."
EOF
  upsert_remote_file "$restore_path" "restore.sh"

  readme_path="$tmpdir/README.md"
  cat > "$readme_path" <<'EOF'
# OpenClaw workspace core backup

This repository stores core OpenClaw workspace markdown files for backup and recovery.

## Included files

- AGENTS.md
- HEARTBEAT.md
- IDENTITY.md
- SOUL.md
- TOOLS.md
- USER.md
- MEMORY.md

## Restore

```bash
bash restore.sh
```

By default, files are restored to `~/.openclaw/workspace`.
EOF
  upsert_remote_file "$readme_path" "README.md"

  rm -rf "$tmpdir"
  trap - RETURN

  if [ "$changed" = true ]; then
    echo "Sync complete: https://github.com/$GITHUB_OWNER/$REPO_NAME"
  else
    echo "No tracked files found to sync."
  fi
}

if [ "$(is_initialized)" != "true" ]; then
  if repo_exists; then
    echo "First initialization: remote repo exists, restoring local files first."
    restore_from_remote
    write_initialized
    echo "Initialization complete."
    exit 0
  else
    echo "First initialization: remote repo not found, creating private repo and uploading local files."
    sync_workspace_files_to_remote
    write_initialized
    echo "Initialization complete."
    exit 0
  fi
fi

sync_workspace_files_to_remote
