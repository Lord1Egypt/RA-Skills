#!/usr/bin/env bash
set -euo pipefail

VERSION="${XHS_MCP_VERSION:-latest}"
BIN_NAME="xiaohongshu-mcp"
FORCE_INSTALL="${XHS_MCP_FORCE_INSTALL:-0}"
CUSTOM_TARGET="${XHS_MCP_INSTALL_TARGET:-}"

INSTALL_TARGETS=()
if [ -n "$CUSTOM_TARGET" ]; then
  INSTALL_TARGETS+=("$CUSTOM_TARGET")
else
  INSTALL_TARGETS+=(
    "github.com/xpzouying/xiaohongshu-mcp/cmd/xiaohongshu-mcp"
    "github.com/xpzouying/xiaohongshu-mcp"
  )
fi

if [ "$FORCE_INSTALL" != "1" ] && command -v "$BIN_NAME" >/dev/null 2>&1; then
  echo "[OK] $BIN_NAME already exists: $(command -v "$BIN_NAME")"
  "$BIN_NAME" --help >/dev/null 2>&1 || true
  exit 0
fi

if ! command -v go >/dev/null 2>&1; then
  echo "[ERROR] go is not installed, and $BIN_NAME is not found in PATH."
  echo "Install Go first, then run one of:"
  for target in "${INSTALL_TARGETS[@]}"; do
    echo "  go install ${target}@${VERSION}"
  done
  exit 1
fi

GOBIN_PATH="$(go env GOBIN)"
if [ -z "$GOBIN_PATH" ]; then
  GOPATH_VALUE="$(go env GOPATH)"
  GOBIN_PATH="${GOPATH_VALUE}/bin"
fi

mkdir -p "$GOBIN_PATH"

echo "[INFO] Installing $BIN_NAME@$VERSION to $GOBIN_PATH ..."
PROXIES=()
if [ -n "${GOPROXY:-}" ]; then
  PROXIES+=("${GOPROXY}")
fi
PROXIES+=("https://proxy.golang.org,direct" "https://goproxy.cn,direct" "direct")

INSTALLED=0
INSTALLED_TARGET=""
for target in "${INSTALL_TARGETS[@]}"; do
  for proxy in "${PROXIES[@]}"; do
    echo "[INFO] Trying target=$target GOPROXY=$proxy"
    if GOBIN="$GOBIN_PATH" GOPROXY="$proxy" go install "${target}@${VERSION}"; then
      INSTALLED=1
      INSTALLED_TARGET="$target"
      break
    fi
  done
  if [ "$INSTALLED" -eq 1 ]; then
    break
  fi
done

if [ "$INSTALLED" -ne 1 ]; then
  echo "[ERROR] go install failed for all targets/proxies."
  echo "Tried targets:"
  for target in "${INSTALL_TARGETS[@]}"; do
    echo "  - ${target}@${VERSION}"
  done
  echo "You can download prebuilt binaries from:"
  echo "  https://github.com/xpzouying/xiaohongshu-mcp/releases"
  exit 1
fi

echo "[OK] install target: ${INSTALLED_TARGET}@${VERSION}"

if command -v "$BIN_NAME" >/dev/null 2>&1; then
  echo "[OK] Installed: $(command -v "$BIN_NAME")"
elif [ -x "$HOME/go/bin/$BIN_NAME" ]; then
  echo "[OK] Installed: $HOME/go/bin/$BIN_NAME"
else
  echo "[WARN] Installed into $GOBIN_PATH, but not in PATH."
  echo "Add it to PATH, for example:"
  echo "  export PATH=\"$GOBIN_PATH:\$PATH\""
fi
