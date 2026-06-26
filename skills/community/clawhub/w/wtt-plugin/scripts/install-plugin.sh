#!/usr/bin/env bash
set -euo pipefail

# Universal installer for @cecwxf/wtt plugin.
# - First try native clawhub spec.
# - If current OpenClaw has scoped-package zip bug (ENOENT @scope/pkg.zip),
#   fallback to npm pack + local tgz install.

VERSION="${1:-0.1.19}"
SPEC="clawhub:@cecwxf/wtt@${VERSION}"
PKG="@cecwxf/wtt@${VERSION}"
TMPDIR="$(mktemp -d /tmp/openclaw-wtt-install-XXXXXX)"
trap 'rm -rf "$TMPDIR"' EXIT

echo "[wtt-install] OpenClaw: $(openclaw --version 2>/dev/null || true)"
echo "[wtt-install] Trying ${SPEC} ..."

set +e
OUT=$(openclaw plugins install "${SPEC}" 2>&1)
RC=$?
set -e

if [[ $RC -eq 0 ]]; then
  echo "$OUT"
  echo "[wtt-install] clawhub install ok"
  openclaw gateway restart
  exit 0
fi

echo "$OUT"

if echo "$OUT" | grep -q "ENOENT" && echo "$OUT" | grep -q "openclaw-clawhub-package"; then
  echo "[wtt-install] Detected scoped clawhub zip bug, fallback to npm pack path install"
else
  echo "[wtt-install] clawhub install failed for another reason; continuing with npm fallback"
fi

cd "$TMPDIR"
npm pack "$PKG" >/dev/null
TGZ=$(ls -1 cecwxf-wtt-${VERSION}.tgz 2>/dev/null || true)
if [[ -z "$TGZ" ]]; then
  echo "[wtt-install] ERROR: npm pack did not produce cecwxf-wtt-${VERSION}.tgz"
  exit 1
fi

# Remove existing plugin entry/files to avoid "plugin already exists".
openclaw plugins uninstall wtt --force >/dev/null 2>&1 || true

openclaw plugins install "$TMPDIR/$TGZ"
openclaw gateway restart

echo "[wtt-install] done: installed ${PKG} via $TMPDIR/$TGZ"
