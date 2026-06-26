#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
SKILLS_DIR="${SKILLS_DIR:-$WORKSPACE/skills}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECKSUMS="$SCRIPT_DIR/checksums.sha256"
VERIFY_ONLY="${VERIFY_ONLY:-false}"

BACKEND="$SKILLS_DIR/faster-whisper-local-service/scripts/deploy.sh"
PROXY="$SKILLS_DIR/webchat-https-proxy/scripts/deploy.sh"
GUI="$SKILLS_DIR/webchat-voice-gui/scripts/deploy.sh"

# --- Integrity verification ---

verify_checksums() {
  if [[ ! -f "$CHECKSUMS" ]]; then
    echo "ERROR: Checksum file not found at: $CHECKSUMS" >&2
    echo "Cannot verify sub-skill integrity. Aborting." >&2
    exit 3
  fi

  echo "=== [full-stack] Verifying sub-skill script integrity ==="
  local failed=0

  while IFS= read -r line; do
    # skip comments and empty lines
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line// }" ]] && continue

    local expected_hash file_rel
    expected_hash="$(echo "$line" | awk '{print $1}')"
    file_rel="$(echo "$line" | awk '{print $2}')"
    local file_abs="$SKILLS_DIR/$file_rel"

    if [[ ! -f "$file_abs" ]]; then
      echo "  MISSING: $file_rel" >&2
      ((failed++))
      continue
    fi

    local actual_hash
    actual_hash="$(sha256sum "$file_abs" | awk '{print $1}')"

    if [[ "$actual_hash" != "$expected_hash" ]]; then
      echo "  MISMATCH: $file_rel" >&2
      echo "    expected: $expected_hash" >&2
      echo "    actual:   $actual_hash" >&2
      ((failed++))
    else
      echo "  OK: $file_rel"
    fi
  done < "$CHECKSUMS"

  if [[ $failed -gt 0 ]]; then
    echo "" >&2
    echo "ERROR: $failed file(s) failed integrity check." >&2
    echo "Sub-skill scripts were modified after last audit." >&2
    echo "Re-audit the changed scripts, then update checksums.sha256." >&2
    echo "To update checksums after review:" >&2
    echo "  bash scripts/rehash.sh" >&2
    exit 4
  fi

  echo "  All checksums verified ✓"
  echo ""
}

verify_checksums

if [[ "$VERIFY_ONLY" == "true" ]]; then
  echo "Verification complete (--verify-only). No deployment performed."
  exit 0
fi

# --- Presence checks ---

if [[ ! -f "$BACKEND" ]]; then
  echo "ERROR: faster-whisper-local-service not found at: $SKILLS_DIR/faster-whisper-local-service" >&2
  echo "Install it first: npx clawhub install faster-whisper-local-service" >&2
  exit 2
fi

if [[ ! -f "$PROXY" ]]; then
  echo "ERROR: webchat-https-proxy not found at: $SKILLS_DIR/webchat-https-proxy" >&2
  echo "Install it first: npx clawhub install webchat-https-proxy" >&2
  exit 2
fi

if [[ ! -f "$GUI" ]]; then
  echo "ERROR: webchat-voice-gui not found at: $SKILLS_DIR/webchat-voice-gui" >&2
  echo "Install it first: npx clawhub install webchat-voice-gui" >&2
  exit 2
fi

# --- Deploy ---

echo "=== [full-stack] Step 1/3: Deploy backend (faster-whisper-local-service) ==="
bash "$BACKEND"

echo ""
echo "=== [full-stack] Step 2/3: Deploy HTTPS proxy (webchat-https-proxy) ==="
bash "$PROXY"

echo ""
echo "=== [full-stack] Step 3/3: Deploy voice GUI (webchat-voice-gui) ==="
bash "$GUI"

echo ""
echo "=== [full-stack] Deploy complete ==="
echo ""
echo "Next steps:"
echo "  1. Open https://<your-host>:${VOICE_HTTPS_PORT:-8443}/chat?session=main"
echo "  2. Accept the self-signed certificate"
echo "  3. Approve the pending device if prompted (openclaw devices approve ...)"
echo "  4. Click the mic button and speak"
