#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
PACKAGE_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
JQ_VERSION=1.8.1
JQ_BASE_URL=https://github.com/jqlang/jq/releases/download/jq-${JQ_VERSION}
JQ_TEMP_DIR=
trap '[ -z "$JQ_TEMP_DIR" ] || rm -rf "$JQ_TEMP_DIR"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP

die() {
  echo "error: $1" >&2
  exit 1
}

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  elif command -v openssl >/dev/null 2>&1; then
    openssl dgst -sha256 "$1" | awk '{print $2}'
  else
    die "requires sha256sum, shasum, or openssl"
  fi
}

ensure_cli() {
  # Hub installers may write every file with mode 0644. The explicitly
  # referenced shell payload is runnable through bash without chmod.
  if [ -f "$SCRIPT_DIR/revdoku-cli.sh" ] && [ ! -L "$SCRIPT_DIR/revdoku-cli.sh" ]; then
    return
  fi
  # Source checkouts keep the generated public CLI in the package.
  # A missing executable means the installation is incomplete, not an update.
  if [ -f "$PACKAGE_ROOT/src/revdoku.sh.in" ] && [ -x "$PACKAGE_ROOT/bin/revdoku" ] && [ ! -L "$PACKAGE_ROOT/bin/revdoku" ]; then
    return
  fi
  die "bundled Revdoku CLI is missing or not executable; reinstall the complete skill from its original trusted source in the same scope"
}

ensure_jq() {
  if command -v jq >/dev/null 2>&1 || [ -x "$SKILL_DIR/bin/jq" ]; then
    return
  fi

  os=$(uname -s | tr '[:upper:]' '[:lower:]')
  arch=$(uname -m)
  case "$os/$arch" in
    darwin/arm64) asset=jq-macos-arm64; expected=a9fe3ea2f86dfc72f6728417521ec9067b343277152b114f4e98d8cb0e263603 ;;
    darwin/x86_64) asset=jq-macos-amd64; expected=e80dbe0d2a2597e3c11c404f03337b981d74b4a8504b70586c354b7697a7c27f ;;
    linux/x86_64) asset=jq-linux-amd64; expected=020468de7539ce70ef1bceaf7cde2e8c4f2ca6c3afb84642aabc5c97d9fc2a0d ;;
    linux/aarch64|linux/arm64) asset=jq-linux-arm64; expected=6bc62f25981328edd3cfcfe6fe51b073f2d7e7710d7ef7fcdac28d4e384fc3d4 ;;
    *) die "unsupported platform for bundled jq: $os/$arch" ;;
  esac

  mkdir -p "$SKILL_DIR/bin"
  JQ_TEMP_DIR=$(mktemp -d "$SKILL_DIR/bin/.jq.XXXXXX")
  tmp="$JQ_TEMP_DIR/jq"
  command -v curl >/dev/null 2>&1 || die "requires curl"
  curl -q --proto '=https' --proto-redir '=https' -fsSL "$JQ_BASE_URL/$asset" -o "$tmp"
  actual=$(sha256_file "$tmp")
  if [ "$actual" != "$expected" ]; then
    rm -f "$tmp"
    die "downloaded jq checksum mismatch"
  fi
  chmod 0755 "$tmp"
  mv "$tmp" "$SKILL_DIR/bin/jq"
  rm -rf "$JQ_TEMP_DIR"
  JQ_TEMP_DIR=
}

ensure_cli
offline=false
for arg in "$@"; do
  case "$arg" in --dry-run|--help|-h|help|--version|version) offline=true ;; esac
done
if [ "$offline" = false ]; then ensure_jq; fi

PATH="$SKILL_DIR/bin:$PATH"
export PATH

# Preserve the Skill entry path through the CLI's browser sign-in.
REVDOKU_SIGNUP_MEDIUM=skill
export REVDOKU_SIGNUP_MEDIUM

if [ -f "$SKILL_DIR/VERSION" ]; then
  REVDOKU_CLIENT_VERSION_FILE="$SKILL_DIR/VERSION"
  export REVDOKU_CLIENT_VERSION_FILE
fi

if [ -f "$SCRIPT_DIR/revdoku-cli.sh" ] && [ ! -L "$SCRIPT_DIR/revdoku-cli.sh" ]; then
  exec bash "$SCRIPT_DIR/revdoku-cli.sh" "$@"
fi

exec "$PACKAGE_ROOT/bin/revdoku" "$@"
