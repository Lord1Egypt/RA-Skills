#!/usr/bin/env bash
# upgrade.sh — 单资产安全升级（Three Gates）
# 用法：bash upgrade.sh <asset-name> [--target <version>] [--dry-run]
# 依赖：~/.openclaw/inventory.json
set -u
export PATH="/opt/homebrew/bin:/opt/homebrew/opt/node/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

INVENTORY_FILE="${HOME}/.openclaw/inventory.json"
SKILL_BACKUPS="${HOME}/.openclaw/skill-backups"
EXT_BACKUPS="${HOME}/.openclaw/extensions-backup"
PLIST_BACKUPS="${HOME}/.openclaw/plist-backup"
GATEWAY_PLIST="${HOME}/Library/LaunchAgents/ai.openclaw.gateway.plist"
LOG_FILE="${HOME}/.openclaw/logs/smart-updater.log"

ASSET_NAME=""
TARGET_VERSION=""
DRY_RUN=false
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# --- Parse args ---
while [ $# -gt 0 ]; do
  case "$1" in
    --target) shift; TARGET_VERSION="${1:-}"; ;;
    --dry-run) DRY_RUN=true; ;;
    *) ASSET_NAME="$1"; ;;
  esac
  shift
done

if [ -z "$ASSET_NAME" ]; then
  echo "Usage: upgrade.sh <asset-name> [--target <version>] [--dry-run]" >&2
  exit 2
fi

# --- Helpers ---
log() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] smart-updater: $*"
  echo "$msg" >> "$LOG_FILE"
  echo "$msg"
}

die() { log "❌ $*"; exit 1; }

resolve_openclaw() {
  for p in /opt/homebrew/bin/openclaw /opt/homebrew/opt/node/bin/openclaw; do
    [ -x "$p" ] && echo "$p" && return 0
  done
  command -v openclaw 2>/dev/null && return 0
  return 1
}

OPENCLAW="$(resolve_openclaw || true)"
[ -z "${OPENCLAW:-}" ] && die "openclaw not found"

mkdir -p "$SKILL_BACKUPS" "$EXT_BACKUPS" "$PLIST_BACKUPS" "$(dirname "$LOG_FILE")"

# --- Load asset info from inventory ---
ASSET_JSON=$(python3 -c "
import json, sys
inv = json.load(open('$INVENTORY_FILE'))
for a in inv['assets']:
    if a['name'] == '$ASSET_NAME':
        print(json.dumps(a))
        sys.exit(0)
sys.exit(1)
" 2>/dev/null) || die "Asset '$ASSET_NAME' not found in inventory.json"

ASSET_TYPE=$(echo "$ASSET_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['type'])")
ASSET_SOURCE=$(echo "$ASSET_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('source',''))")
CURRENT_VERSION=$(echo "$ASSET_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('currentVersion', d.get('currentCommit','unknown')))")
INSTALLED_AT=$(echo "$ASSET_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('installedAt',''))")
NPM_PACKAGE=$(echo "$ASSET_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('npmPackage',''))")

log "=== Upgrade: $ASSET_NAME ($ASSET_TYPE/$ASSET_SOURCE) ==="
log "Current: $CURRENT_VERSION | Target: ${TARGET_VERSION:-latest} | Dry-run: $DRY_RUN"

# ============================================================
# GATE 1: Pre-flight
# ============================================================
log "--- Gate 1: Pre-flight ---"

# Check source is trackable
if [ "$ASSET_SOURCE" = "local" ]; then
  die "Gate 1 FAIL: '$ASSET_NAME' has no update source (source=local). Register a source first."
fi

if [ "$ASSET_TYPE" = "builtin" ]; then
  die "Gate 1 FAIL: '$ASSET_NAME' is a built-in skill. Upgrade OpenClaw core instead."
fi

# Check name collision: no other asset with same name but different source
CONFLICT_COUNT=$(python3 -c "
import json
inv = json.load(open('$INVENTORY_FILE'))
matches = [a for a in inv['assets'] if a['name'] == '$ASSET_NAME']
# Count distinct sources (excluding builtin)
sources = set(a.get('source','') for a in matches if a.get('type') != 'builtin')
print(len(sources))
" 2>/dev/null || echo "1")

if [ "$CONFLICT_COUNT" -gt 1 ]; then
  die "Gate 1 FAIL: Name conflict — '$ASSET_NAME' exists with multiple sources in inventory. Resolve manually."
fi

# Check install directory exists (for skills)
if [ "$ASSET_TYPE" = "skill" ] && [ -n "$INSTALLED_AT" ]; then
  if [ ! -d "$INSTALLED_AT" ]; then
    die "Gate 1 FAIL: Install directory '$INSTALLED_AT' does not exist."
  fi
fi

# For extensions: check gateway health + source eligibility
if [ "$ASSET_TYPE" = "extension" ]; then
  # Block auto-upgrade for extensions without plugins.installs record
  if [ "$ASSET_SOURCE" = "local" ] || [ "$ASSET_SOURCE" = "github" ]; then
    die "Gate 1 FAIL: '$ASSET_NAME' is a $ASSET_SOURCE extension without plugins.installs provenance. Cannot auto-upgrade safely. Upgrade manually: git pull + 'openclaw plugins install <path>' or 'openclaw gateway restart'."
  fi
  
  GW_STATUS=$("$OPENCLAW" gateway status 2>/dev/null || true)
  RUNNING=$(echo "$GW_STATUS" | grep "Runtime:" | grep -c "running" || true)
  if [ "$RUNNING" -lt 1 ]; then
    die "Gate 1 FAIL: Gateway is not running. Fix gateway before upgrading extensions."
  fi
  log "  ✅ Gateway is healthy"
fi

log "  ✅ Gate 1 passed"

# ============================================================
# GATE 2: Isolation (backup + execute)
# ============================================================
log "--- Gate 2: Isolation ---"

# --- Backup ---
case "$ASSET_TYPE" in
  skill)
    BACKUP_DIR="${SKILL_BACKUPS}/${ASSET_NAME}-${CURRENT_VERSION}-${TIMESTAMP}"
    log "  Backing up to $BACKUP_DIR"
    if ! $DRY_RUN; then
      cp -r "$INSTALLED_AT" "$BACKUP_DIR" || die "Gate 2 FAIL: Backup failed"
    fi
    log "  ✅ Backup complete"
    ;;
  extension)
    BACKUP_DIR="${EXT_BACKUPS}/${ASSET_NAME}-${CURRENT_VERSION}-${TIMESTAMP}"
    log "  Backing up to $BACKUP_DIR"
    if ! $DRY_RUN; then
      cp -r "$INSTALLED_AT" "$BACKUP_DIR" || die "Gate 2 FAIL: Backup failed"
    fi
    log "  ✅ Backup complete"
    
    # Clear jiti cache (mandatory for extensions)
    log "  Clearing jiti cache..."
    if ! $DRY_RUN; then
      rm -rf /tmp/jiti/
    fi
    log "  ✅ jiti cache cleared"
    ;;
  core)
    log "  Backing up gateway plist..."
    if ! $DRY_RUN; then
      cp "$GATEWAY_PLIST" "${PLIST_BACKUPS}/ai.openclaw.gateway.plist.${TIMESTAMP}" 2>/dev/null || log "  ⚠️ No gateway plist to backup"
      "$OPENCLAW" backup create --output "${HOME}/.openclaw/backups" --verify >> "$LOG_FILE" 2>&1 || log "  ⚠️ openclaw backup create failed (non-fatal)"
    fi
    log "  ✅ Backup complete"
    ;;
esac

# --- Execute upgrade ---
log "  Executing upgrade..."

if $DRY_RUN; then
  log "  🏃 [DRY-RUN] Would execute upgrade for $ASSET_NAME"
else
  case "$ASSET_SOURCE" in
    clawhub)
      # Try SkillHub (腾讯国内镜像) first — faster download, no rate limit
      SKILLHUB_ZIP_URL="https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/skills/${ASSET_NAME}.zip"
      SKILLHUB_TMP=$(mktemp -d)
      SKILLHUB_OK=false

      log "  Trying SkillHub mirror: $SKILLHUB_ZIP_URL"
      HTTP_CODE=$(curl -s -o "${SKILLHUB_TMP}/${ASSET_NAME}.zip" -w "%{http_code}" --connect-timeout 5 --max-time 30 "$SKILLHUB_ZIP_URL" 2>>"$LOG_FILE")
      
      if [ "$HTTP_CODE" = "200" ] && [ -s "${SKILLHUB_TMP}/${ASSET_NAME}.zip" ]; then
        log "  ✅ SkillHub download success (HTTP $HTTP_CODE), extracting..."
        # Extract zip over existing install dir
        EXTRACT_TMP=$(mktemp -d)
        if unzip -q "${SKILLHUB_TMP}/${ASSET_NAME}.zip" -d "$EXTRACT_TMP" 2>>"$LOG_FILE"; then
          # Find the skill dir inside the zip (usually first subdirectory)
          SKILL_SUBDIR=$(find "$EXTRACT_TMP" -maxdepth 1 -mindepth 1 -type d | head -1)
          if [ -n "$SKILL_SUBDIR" ] && [ -f "$SKILL_SUBDIR/SKILL.md" ]; then
            # Replace contents of INSTALLED_AT
            rm -rf "${INSTALLED_AT:?}"/*
            cp -r "$SKILL_SUBDIR"/. "$INSTALLED_AT/"
            SKILLHUB_OK=true
            log "  ✅ SkillHub install complete"
            UPGRADE_RC=0
          else
            log "  ⚠️ SkillHub zip has unexpected structure (no SKILL.md), falling back"
          fi
        else
          log "  ⚠️ SkillHub zip extraction failed, falling back"
        fi
        rm -rf "$EXTRACT_TMP"
      else
        log "  ⚠️ SkillHub unavailable (HTTP $HTTP_CODE), falling back to clawhub"
      fi
      rm -rf "$SKILLHUB_TMP"

      # Fallback: clawhub update
      if ! $SKILLHUB_OK; then
        log "  Running: clawhub update $ASSET_NAME"
        CLAWHUB_OUTPUT=$(clawhub update "$ASSET_NAME" 2>&1)
        UPGRADE_RC=$?
        echo "$CLAWHUB_OUTPUT" >> "$LOG_FILE"
        
        # clawhub may exit 0 even when it refuses to update due to local changes
        if echo "$CLAWHUB_OUTPUT" | grep -qi "local changes\|no match\|Use --force"; then
          log "  ⚠️ clawhub detected local modifications, retrying with --force"
          CLAWHUB_OUTPUT=$(clawhub update "$ASSET_NAME" --force 2>&1)
          UPGRADE_RC=$?
          echo "$CLAWHUB_OUTPUT" >> "$LOG_FILE"
        fi
      fi
      ;;
    npm)
      if [ "$ASSET_TYPE" = "core" ]; then
        VER_ARG="@latest"
        [ -n "$TARGET_VERSION" ] && VER_ARG="@$TARGET_VERSION"
        log "  Running: npm install -g openclaw${VER_ARG}"
        npm install -g "openclaw${VER_ARG}" >> "$LOG_FILE" 2>&1
        UPGRADE_RC=$?
        
        # Re-install gateway (updates plist)
        log "  Running: openclaw gateway install"
        "$OPENCLAW" gateway install >> "$LOG_FILE" 2>&1 || true
        
        # Config protection: diff plist
        if [ -f "${PLIST_BACKUPS}/ai.openclaw.gateway.plist.${TIMESTAMP}" ]; then
          if ! diff -q "$GATEWAY_PLIST" "${PLIST_BACKUPS}/ai.openclaw.gateway.plist.${TIMESTAMP}" >/dev/null 2>&1; then
            log "  ⚠️ Gateway plist changed by install. Diff:"
            diff "$GATEWAY_PLIST" "${PLIST_BACKUPS}/ai.openclaw.gateway.plist.${TIMESTAMP}" >> "$LOG_FILE" 2>&1 || true
            log "  ⚠️ Review plist changes and restore custom env vars if needed"
          fi
        fi
      else
        # Extension npm upgrade — use openclaw official plugin update path
        # This ensures plugins.installs record stays consistent
        PLUGIN_ID=$(python3 -c "
import json
inv = json.load(open('$INVENTORY_FILE'))
asset = next((a for a in inv['assets'] if a['name'] == '$ASSET_NAME'), {})
# Try to find the plugin ID from openclaw config
config = json.load(open('${HOME}/.openclaw/openclaw.json'))
installs = config.get('plugins', {}).get('installs', {})
for pid, info in installs.items():
    if info.get('resolvedName') == '$NPM_PACKAGE' or info.get('spec') == '$NPM_PACKAGE':
        print(pid)
        break
else:
    print('')
" 2>/dev/null || echo "")
        
        if [ -n "$PLUGIN_ID" ]; then
          # Official tracked plugin — use openclaw plugins update
          log "  Running: openclaw plugins update $PLUGIN_ID"
          "$OPENCLAW" plugins update "$PLUGIN_ID" >> "$LOG_FILE" 2>&1
          UPGRADE_RC=$?
        else
          # Fallback: npm install in directory (but warn about provenance gap)
          VER_ARG="@latest"
          [ -n "$TARGET_VERSION" ] && VER_ARG="@$TARGET_VERSION"
          log "  ⚠️ No plugins.installs record found, falling back to npm install"
          log "  Running: cd $INSTALLED_AT && npm install ${NPM_PACKAGE}${VER_ARG}"
          (cd "$INSTALLED_AT" && npm install "${NPM_PACKAGE}${VER_ARG}") >> "$LOG_FILE" 2>&1
          UPGRADE_RC=$?
        fi
        
        # Clean any .bak dirs in extensions/ (prevent duplicate plugin id)
        find "${HOME}/.openclaw/extensions/" -maxdepth 1 -name "*.bak*" -type d -exec rm -rf {} + 2>/dev/null || true
      fi
      ;;
    github)
      log "  Running: cd $INSTALLED_AT && git pull"
      (cd "$INSTALLED_AT" && git pull) >> "$LOG_FILE" 2>&1
      UPGRADE_RC=$?
      ;;
    *)
      die "Gate 2 FAIL: Unknown source '$ASSET_SOURCE'"
      ;;
  esac
  
  if [ "${UPGRADE_RC:-0}" -ne 0 ]; then
    log "  ❌ Gate 2 FAIL: Upgrade command returned non-zero exit code: $UPGRADE_RC"
    log "  Initiating rollback due to upgrade failure..."
    
    # Rollback from backup
    case "$ASSET_TYPE" in
      skill)
        if [ -d "${BACKUP_DIR:-}" ]; then
          rm -rf "$INSTALLED_AT"
          cp -r "$BACKUP_DIR" "$INSTALLED_AT"
          log "  ✅ Rolled back skill from backup"
        fi
        ;;
      extension)
        if [ -d "${BACKUP_DIR:-}" ]; then
          rm -rf "$INSTALLED_AT"
          cp -r "$BACKUP_DIR" "$INSTALLED_AT"
          rm -rf /tmp/jiti/
          "$OPENCLAW" gateway restart >> "$LOG_FILE" 2>&1 || true
          log "  ✅ Rolled back extension + restarted gateway"
        fi
        ;;
      core)
        PREV_CLEAN=$(echo "$CURRENT_VERSION" | sed 's/ .*//')
        log "  Rolling back to openclaw@$PREV_CLEAN"
        npm install -g "openclaw@$PREV_CLEAN" >> "$LOG_FILE" 2>&1 || true
        if [ -f "${PLIST_BACKUPS}/ai.openclaw.gateway.plist.${TIMESTAMP}" ]; then
          cp "${PLIST_BACKUPS}/ai.openclaw.gateway.plist.${TIMESTAMP}" "$GATEWAY_PLIST"
        fi
        "$OPENCLAW" gateway restart >> "$LOG_FILE" 2>&1 || true
        log "  ✅ Rolled back core + restored plist"
        ;;
    esac
    
    die "Upgrade of '$ASSET_NAME' failed (exit code $UPGRADE_RC) and was rolled back."
  fi
fi

log "  ✅ Gate 2 complete"

# ============================================================
# GATE 3: Post-flight (verify)
# ============================================================
log "--- Gate 3: Post-flight ---"

GATE3_PASS=true

if ! $DRY_RUN; then
  case "$ASSET_TYPE" in
    skill)
      # Check SKILL.md exists
      if [ ! -f "$INSTALLED_AT/SKILL.md" ]; then
        log "  ❌ SKILL.md missing after upgrade!"
        GATE3_PASS=false
      else
        log "  ✅ SKILL.md present"
      fi
      
      # Check file count >= backup (detect incomplete upgrade)
      if [ -d "${BACKUP_DIR:-}" ] && $GATE3_PASS; then
        OLD_COUNT=$(find "$BACKUP_DIR" -type f | wc -l | tr -d ' ')
        NEW_COUNT=$(find "$INSTALLED_AT" -type f | wc -l | tr -d ' ')
        if [ "$NEW_COUNT" -lt "$OLD_COUNT" ]; then
          log "  ❌ File count decreased: $OLD_COUNT → $NEW_COUNT (possible incomplete upgrade)"
          GATE3_PASS=false
        else
          log "  ✅ File count OK ($NEW_COUNT files, was $OLD_COUNT)"
        fi
      fi
      
      # Version verification: check SKILL.md version changed from CURRENT_VERSION
      if $GATE3_PASS; then
        NEW_SKILL_VER=$(grep -E "^version:" "$INSTALLED_AT/SKILL.md" 2>/dev/null | head -1 | sed 's/version:[[:space:]]*//')
        if [ -z "$NEW_SKILL_VER" ]; then
          log "  ⚠️ No version field in SKILL.md (non-fatal)"
        elif [ "$NEW_SKILL_VER" = "$CURRENT_VERSION" ]; then
          log "  ❌ Version unchanged after upgrade: still $NEW_SKILL_VER (upgrade may not have taken effect)"
          GATE3_PASS=false
        else
          log "  ✅ Version updated: $CURRENT_VERSION → $NEW_SKILL_VER"
        fi
      fi
      ;;
    extension)
      # Restart gateway and check
      log "  Restarting gateway..."
      "$OPENCLAW" gateway restart >> "$LOG_FILE" 2>&1 || true
      
      # Poll for gateway health (up to 60s)
      WAIT_COUNT=0
      RUNNING=0
      while [ $WAIT_COUNT -lt 12 ]; do
        sleep 5
        WAIT_COUNT=$((WAIT_COUNT + 1))
        GW_STATUS=$("$OPENCLAW" gateway status 2>/dev/null || true)
        RUNNING=$(echo "$GW_STATUS" | grep "Runtime:" | grep -c "running" || true)
        [ "$RUNNING" -ge 1 ] && break
      done
      
      if [ "$RUNNING" -lt 1 ]; then
        log "  ❌ Gateway not running after restart (waited ${WAIT_COUNT}x5s)!"
        GATE3_PASS=false
      else
        # Check gateway log for plugin registered + no duplicate id
        RECENT_LOG=$(tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null || true)
        if echo "$RECENT_LOG" | grep -qi "duplicate plugin id"; then
          log "  ❌ Duplicate plugin id detected in gateway logs!"
          GATE3_PASS=false
        elif echo "$RECENT_LOG" | grep -qi "plugin registered"; then
          log "  ✅ Gateway healthy, plugin registered confirmed"
        else
          log "  ⚠️ Gateway running but 'plugin registered' not found in recent logs (non-fatal)"
        fi
        
        # Provenance consistency check
        PLUGIN_INFO=$("$OPENCLAW" plugins info "$ASSET_NAME" 2>/dev/null || true)
        if echo "$PLUGIN_INFO" | grep -qi "without install.*provenance\|without.*load-path provenance"; then
          log "  ⚠️ Plugin still shows 'loaded without provenance' — management state may be drifted"
          log "  ⚠️ Code was upgraded but OpenClaw install record may not reflect the change"
        fi
        
        # Version consistency check: package.json vs what gateway loaded
        if [ -f "$INSTALLED_AT/package.json" ]; then
          PKG_VER=$(python3 -c "import json; print(json.load(open('$INSTALLED_AT/package.json')).get('version','?'))" 2>/dev/null || echo "?")
          log "  📋 package.json version: $PKG_VER"
        fi
      fi
      ;;
    core)
      # Restart and verify
      log "  Restarting gateway..."
      "$OPENCLAW" gateway restart >> "$LOG_FILE" 2>&1 || true
      sleep 10
      
      NEW_VERSION=$("$OPENCLAW" --version 2>/dev/null | head -1 || echo "unknown")
      log "  Version after upgrade: $NEW_VERSION"
      
      GW_STATUS=$("$OPENCLAW" gateway status 2>/dev/null || true)
      RUNNING=$(echo "$GW_STATUS" | grep "Runtime:" | grep -c "running" || true)
      
      if [ "$RUNNING" -lt 1 ]; then
        log "  ❌ Gateway not running after core upgrade!"
        GATE3_PASS=false
      else
        log "  ✅ Gateway healthy"
      fi
      ;;
  esac
fi

# --- Rollback on failure ---
if ! $GATE3_PASS; then
  log "🔄 Gate 3 FAILED — initiating rollback..."
  
  case "$ASSET_TYPE" in
    skill)
      if [ -d "$BACKUP_DIR" ]; then
        rm -rf "$INSTALLED_AT"
        cp -r "$BACKUP_DIR" "$INSTALLED_AT"
        log "  ✅ Rolled back skill from backup"
      fi
      ;;
    extension)
      if [ -d "$BACKUP_DIR" ]; then
        rm -rf "$INSTALLED_AT"
        cp -r "$BACKUP_DIR" "$INSTALLED_AT"
        rm -rf /tmp/jiti/
        "$OPENCLAW" gateway restart >> "$LOG_FILE" 2>&1 || true
        log "  ✅ Rolled back extension + restarted gateway"
      fi
      ;;
    core)
      PREV_CLEAN=$(echo "$CURRENT_VERSION" | sed 's/ .*//')
      log "  Rolling back to openclaw@$PREV_CLEAN"
      npm install -g "openclaw@$PREV_CLEAN" >> "$LOG_FILE" 2>&1 || true
      if [ -f "${PLIST_BACKUPS}/ai.openclaw.gateway.plist.${TIMESTAMP}" ]; then
        cp "${PLIST_BACKUPS}/ai.openclaw.gateway.plist.${TIMESTAMP}" "$GATEWAY_PLIST"
      fi
      "$OPENCLAW" gateway restart >> "$LOG_FILE" 2>&1 || true
      log "  ✅ Rolled back core + restored plist"
      ;;
  esac
  
  die "Upgrade of '$ASSET_NAME' failed and was rolled back."
fi

log "✅ Upgrade of '$ASSET_NAME' completed successfully"
$DRY_RUN && log "(This was a dry-run — no actual changes were made)"
exit 0
