#!/usr/bin/env bash
# inventory.sh — OpenClaw 资产盘点
# 输出：~/.openclaw/inventory.json
# 用法：bash inventory.sh [--quiet]
set -u
export PATH="/opt/homebrew/bin:/opt/homebrew/opt/node/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

INVENTORY_FILE="${HOME}/.openclaw/inventory.json"
WORKSPACE="${HOME}/.openclaw/workspace"
EXTENSIONS_DIR="${HOME}/.openclaw/extensions"

# Auto-detect workspace if openclaw config has a different path
if [ -f "${HOME}/.openclaw/openclaw.json" ]; then
  CONFIGURED_WORKSPACE=$(python3 -c "
import json
c = json.load(open('${HOME}/.openclaw/openclaw.json'))
print(c.get('workspace', {}).get('dir', '') or c.get('workspaceDir', '') or '')
" 2>/dev/null || echo "")
  [ -n "$CONFIGURED_WORKSPACE" ] && [ -d "$CONFIGURED_WORKSPACE" ] && WORKSPACE="$CONFIGURED_WORKSPACE"
fi

SKILLS_DIR="${WORKSPACE}/skills"
BUILTIN_SKILLS_DIR=""
QUIET=false

[[ "${1:-}" == "--quiet" ]] && QUIET=true

log() { $QUIET || echo "$*" >&2; }

# Resolve openclaw
resolve_openclaw() {
  for p in /opt/homebrew/bin/openclaw /opt/homebrew/opt/node/bin/openclaw; do
    [ -x "$p" ] && echo "$p" && return 0
  done
  command -v openclaw 2>/dev/null && return 0
  return 1
}

OPENCLAW="$(resolve_openclaw || true)"
if [ -z "${OPENCLAW:-}" ]; then
  echo '{"error":"openclaw not found"}' > "$INVENTORY_FILE"
  exit 1
fi

# Detect built-in skills dir from openclaw binary path
BUILTIN_SKILLS_DIR=""
OC_REAL="$(readlink -f "$OPENCLAW" 2>/dev/null || realpath "$OPENCLAW" 2>/dev/null || readlink "$OPENCLAW" 2>/dev/null || true)"
if [ -n "$OC_REAL" ]; then
  # Follow symlinks to the actual .mjs file, then go up to package root/skills
  OC_PKG_DIR="$(dirname "$(dirname "$OC_REAL")")"
  if [ -d "$OC_PKG_DIR/skills" ]; then
    BUILTIN_SKILLS_DIR="$OC_PKG_DIR/skills"
  fi
fi
# Fallback: try common locations
if [ ! -d "${BUILTIN_SKILLS_DIR:-}" ]; then
  for candidate in \
    /opt/homebrew/Cellar/node/*/lib/node_modules/openclaw/skills \
    /opt/homebrew/opt/node/lib/node_modules/openclaw/skills \
    /usr/local/lib/node_modules/openclaw/skills \
    /usr/lib/node_modules/openclaw/skills \
    "$HOME/.nvm/versions/node"/*/lib/node_modules/openclaw/skills \
    "$HOME/.volta/tools/image/packages/openclaw"/*/skills \
    "$HOME/.local/lib/node_modules/openclaw/skills" \
    "$HOME/.npm-global/lib/node_modules/openclaw/skills"; do
    # Use glob — take the first match
    for d in $candidate; do
      [ -d "$d" ] && BUILTIN_SKILLS_DIR="$d" && break 2
    done
  done
fi

# Last resort: use npm to find it
if [ ! -d "${BUILTIN_SKILLS_DIR:-}" ]; then
  NPM_ROOT=$(npm root -g 2>/dev/null || true)
  if [ -n "$NPM_ROOT" ] && [ -d "$NPM_ROOT/openclaw/skills" ]; then
    BUILTIN_SKILLS_DIR="$NPM_ROOT/openclaw/skills"
  fi
fi

if [ ! -d "${BUILTIN_SKILLS_DIR:-}" ]; then
  log "  ⚠️ Could not find built-in skills directory"
  log "  Debug: OPENCLAW=$OPENCLAW"
  log "  Debug: OC_REAL=${OC_REAL:-unresolved}"
  log "  Debug: npm root -g=$(npm root -g 2>/dev/null || echo 'failed')"
fi

mkdir -p "$(dirname "$INVENTORY_FILE")"

# --- Collect assets via temp file ---
ASSETS_FILE=$(mktemp "${TMPDIR:-/tmp}/smart-updater-inv.XXXXXX")
echo "[]" > "$ASSETS_FILE"
cleanup() { rm -f "$ASSETS_FILE" /tmp/smart-updater-count.txt; }
trap cleanup EXIT

add_asset() {
  # Accepts key=value pairs, builds JSON safely via Python
  python3 -c "
import json, sys
arr = json.load(open('$ASSETS_FILE'))
obj = {}
for arg in sys.argv[1:]:
    k, v = arg.split('=', 1)
    obj[k] = v
arr.append(obj)
json.dump(arr, open('$ASSETS_FILE', 'w'))
" "$@"
}

# 1. OpenClaw core
log "📦 Scanning OpenClaw core..."
OC_VERSION="$("$OPENCLAW" --version 2>/dev/null | head -1 | sed 's/OpenClaw //' || echo "unknown")"
add_asset "name=openclaw" "type=core" "source=npm" "currentVersion=$OC_VERSION" "npmPackage=openclaw"

# 2. Extensions (check plugins.installs for source truth)
log "📦 Scanning extensions..."

# First, read OpenClaw's official install records
OC_CONFIG="${HOME}/.openclaw/openclaw.json"
INSTALLS_JSON=""
if [ -f "$OC_CONFIG" ]; then
  INSTALLS_JSON=$(python3 -c "
import json
c = json.load(open('$OC_CONFIG'))
installs = c.get('plugins', {}).get('installs', {})
# Map: directory basename -> install record
result = {}
for plugin_id, info in installs.items():
    ipath = info.get('installPath', '')
    if ipath:
        import os
        dirname = os.path.basename(ipath)
        result[dirname] = {
            'source': info.get('source', 'unknown'),
            'spec': info.get('spec', ''),
            'version': info.get('version', ''),
            'npmPackage': info.get('resolvedName', info.get('spec', '')),
            'pluginId': plugin_id
        }
    else:
        result[plugin_id] = {
            'source': info.get('source', 'unknown'),
            'spec': info.get('spec', ''),
            'version': info.get('version', ''),
            'npmPackage': info.get('resolvedName', info.get('spec', '')),
            'pluginId': plugin_id
        }
print(json.dumps(result))
" 2>/dev/null || echo "{}")
fi

if [ -d "$EXTENSIONS_DIR" ]; then
  for pkg_json in "$EXTENSIONS_DIR"/*/package.json; do
    [ -f "$pkg_json" ] || continue
    dir="$(dirname "$pkg_json")"
    dirname="$(basename "$dir")"
    
    # Skip backup dirs
    [[ "$dirname" == *.bak* ]] && continue
    [[ "$dirname" == *backup* ]] && continue
    
    info=$(python3 -c "
import json
d = json.load(open('$pkg_json'))
print(d.get('name','unknown'))
print(d.get('version','unknown'))
" 2>/dev/null || echo -e "unknown\nunknown")
    
    pkg_name=$(echo "$info" | head -1)
    pkg_version=$(echo "$info" | tail -1)
    
    # Check if this extension is tracked in plugins.installs
    EXT_SOURCE=$(python3 -c "
import json
installs = json.loads('$INSTALLS_JSON') if '$INSTALLS_JSON' else {}
rec = installs.get('$dirname', {})
print(rec.get('source', ''))
" 2>/dev/null || echo "")
    
    if [ "$EXT_SOURCE" = "npm" ]; then
      # Officially tracked npm plugin
      NPM_PKG=$(python3 -c "
import json
installs = json.loads('$INSTALLS_JSON')
print(installs.get('$dirname', {}).get('npmPackage', '$pkg_name'))
" 2>/dev/null || echo "$pkg_name")
      log "  → $pkg_name@$pkg_version (npm tracked)"
      add_asset "name=$pkg_name" "type=extension" "source=npm" "currentVersion=$pkg_version" "npmPackage=$NPM_PKG" "installedAt=$dir"
    else
      # Not in plugins.installs — local/path/github install
      # Check if it's a git repo
      if [ -d "$dir/.git" ]; then
        log "  → $pkg_name@$pkg_version (local/github)"
        add_asset "name=$pkg_name" "type=extension" "source=github" "currentVersion=$pkg_version" "installedAt=$dir"
      else
        log "  → $pkg_name@$pkg_version (local — no provenance)"
        add_asset "name=$pkg_name" "type=extension" "source=local" "currentVersion=$pkg_version" "installedAt=$dir"
      fi
    fi
  done
fi

# 3. ClawHub skills
log "📦 Scanning ClawHub skills..."
CLAWHUB_LIST=""
if command -v clawhub >/dev/null 2>&1; then
  CLAWHUB_LIST=$(clawhub list 2>/dev/null || true)
fi

clawhub_skills=()
if [ -n "$CLAWHUB_LIST" ]; then
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    skill_name=$(echo "$line" | awk '{print $1}')
    skill_version=$(echo "$line" | awk '{print $2}')
    [ -z "$skill_name" ] && continue
    
    clawhub_skills+=("$skill_name")
    
    # Read actual local version from SKILL.md (clawhub list may return registry version, not local)
    local_version=""
    if [ -f "$SKILLS_DIR/$skill_name/SKILL.md" ]; then
      local_version=$(grep -E "^version:" "$SKILLS_DIR/$skill_name/SKILL.md" 2>/dev/null | head -1 | sed 's/version:[[:space:]]*//')
    fi
    # Use SKILL.md version if available, fall back to clawhub list version
    actual_version="${local_version:-$skill_version}"
    if [ -n "$local_version" ] && [ "$local_version" != "$skill_version" ]; then
      log "  → $skill_name@$actual_version (clawhub, registry says $skill_version)"
    else
      log "  → $skill_name@$actual_version (clawhub)"
    fi
    add_asset "name=$skill_name" "type=skill" "source=clawhub" "currentVersion=$actual_version" "registryVersion=$skill_version" "installedAt=$SKILLS_DIR/$skill_name"
  done <<< "$CLAWHUB_LIST"
fi

# 4. GitHub-cloned skills (have .git)
log "📦 Scanning GitHub-cloned skills..."
log "  Scanning in: $SKILLS_DIR"
if [ -d "$SKILLS_DIR" ]; then
  for skill_dir in "$SKILLS_DIR"/*/; do
    [ -d "$skill_dir/.git" ] || continue
    skill_name="$(basename "$skill_dir")"
    
    # Skip if already registered as clawhub
    is_clawhub=false
    if [ ${#clawhub_skills[@]} -gt 0 ]; then
      for cs in "${clawhub_skills[@]}"; do
        [ "$cs" = "$skill_name" ] && is_clawhub=true && break
      done
    fi
    $is_clawhub && continue
    
    remote=$(cd "$skill_dir" && git remote get-url origin 2>/dev/null || echo "")
    commit=$(cd "$skill_dir" && git log -1 --format=%H 2>/dev/null || echo "unknown")
    short_commit=$(echo "$commit" | cut -c1-8)
    
    log "  → $skill_name@$short_commit (github: $remote)"
    add_asset "name=$skill_name" "type=skill" "source=github" "repo=$remote" "currentCommit=$commit" "installedAt=$skill_dir"
  done
fi

# 5. Built-in skills (shipped with openclaw)
log "📦 Scanning built-in skills..."
builtin_skills=()
if [ -d "${BUILTIN_SKILLS_DIR:-}" ]; then
  for skill_md in "$BUILTIN_SKILLS_DIR"/*/SKILL.md; do
    [ -f "$skill_md" ] || continue
    skill_name="$(basename "$(dirname "$skill_md")")"
    builtin_skills+=("$skill_name")
  done
  builtin_count=${#builtin_skills[@]}
  log "  → $builtin_count built-in skills (version tied to openclaw $OC_VERSION)"
  add_asset "name=_builtin_skills" "type=builtin" "source=bundled" "count=$builtin_count" "currentVersion=$OC_VERSION"
fi

# 6. Untracked skills (in workspace but not clawhub, not git, not built-in)
log "📦 Scanning untracked skills..."
if [ -d "$SKILLS_DIR" ]; then
  for skill_dir in "$SKILLS_DIR"/*/; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    skill_name="$(basename "$skill_dir")"
    
    # Skip clawhub
    is_clawhub=false
    if [ ${#clawhub_skills[@]} -gt 0 ]; then
      for cs in "${clawhub_skills[@]}"; do
        [ "$cs" = "$skill_name" ] && is_clawhub=true && break
      done
    fi
    $is_clawhub && continue
    
    # Skip git-cloned
    [ -d "$skill_dir/.git" ] && continue
    
    # This is untracked (even if a built-in skill has the same name — 
    # the workspace copy is a user override and should be tracked)
    # Cross-platform stat: macOS uses -f, Linux uses -c
    mod_time=$(stat -f "%Sm" -t "%Y-%m-%d" "$skill_dir/SKILL.md" 2>/dev/null || \
               stat -c "%y" "$skill_dir/SKILL.md" 2>/dev/null | cut -d' ' -f1 || \
               echo "unknown")
    log "  → $skill_name (untracked, last modified: $mod_time)"
    add_asset "name=$skill_name" "type=skill" "source=local" "installedAt=$skill_dir" "lastModified=$mod_time"
  done
fi

# --- Write output ---
SCAN_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

python3 -c "
import json
assets = json.load(open('$ASSETS_FILE'))
output = {
    'version': 1,
    'scanTime': '$SCAN_TIME',
    'totalAssets': len(assets),
    'assets': assets
}
with open('$INVENTORY_FILE', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(len(assets))
" > /tmp/smart-updater-count.txt

TOTAL=$(cat /tmp/smart-updater-count.txt)
rm -f /tmp/smart-updater-count.txt

log ""
log "✅ Inventory saved to $INVENTORY_FILE ($TOTAL assets)"
$QUIET && echo "$INVENTORY_FILE"
exit 0
