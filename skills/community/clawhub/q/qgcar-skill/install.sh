#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${QG_SKILL_REPO_URL:-https://github.com/qybaihe/qg-skill.git}"
TARBALL_URL="${QG_SKILL_TARBALL_URL:-https://github.com/qybaihe/qg-skill/archive/refs/heads/main.tar.gz}"
PACKAGE_NAME="${QG_SKILL_PACKAGE:-qg-skill}"
SKILL_NAME="${QG_SKILL_NAME:-qgcar-skill}"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
OPENCLAW_HOME_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
CODEX_SKILL_DIR="$CODEX_HOME_DIR/skills/$SKILL_NAME"
OPENCLAW_SKILL_DIR="$OPENCLAW_HOME_DIR/skills/$SKILL_NAME"

need_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

need_command node
need_command npm

node -e 'const major = Number(process.versions.node.split(".")[0]); if (major < 18) { console.error("Node.js 18+ is required."); process.exit(1); }'

install_from_source() {
  echo "Installing qg CLI from the GitHub checkout..."
  (
    cd "$repo_dir"
    npm install
    npm run build
    npm pack --pack-destination "$tmp_dir" >/dev/null
    tarball="$(find "$tmp_dir" -maxdepth 1 -type f -name "qg-skill-*.tgz" | head -n 1)"
    if [ -z "$tarball" ]; then
      echo "Failed to create qg-skill npm tarball." >&2
      exit 1
    fi
    npm install -g "$tarball"
  )
}

install_skill_to_dir() {
  local target_dir="$1"
  local label="$2"

  echo "Installing $label skill to $target_dir..."
  mkdir -p "$(dirname "$target_dir")"
  rm -rf "$target_dir"
  mkdir -p "$target_dir"

  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude ".git" --exclude "node_modules" "$repo_dir/" "$target_dir/"
  else
    cp -R "$repo_dir/." "$target_dir/"
    rm -rf "$target_dir/.git" "$target_dir/node_modules"
  fi
}

tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

repo_dir="$tmp_dir/repo"
if command -v git >/dev/null 2>&1; then
  git clone --depth 1 "$REPO_URL" "$repo_dir"
else
  need_command curl
  need_command tar
  mkdir -p "$repo_dir"
  curl -fsSL "$TARBALL_URL" | tar -xz -C "$tmp_dir"
  extracted_dir="$(find "$tmp_dir" -maxdepth 1 -type d -name "qg-skill-*" | head -n 1)"
  if [ -z "$extracted_dir" ]; then
    echo "Failed to extract qg-skill tarball." >&2
    exit 1
  fi
  repo_dir="$extracted_dir"
fi

echo "Installing qg CLI..."
if npm view "$PACKAGE_NAME" version --registry=https://registry.npmjs.org >/dev/null 2>&1; then
  if npm install -g "$PACKAGE_NAME"; then
    echo "Installed qg CLI from npm package: $PACKAGE_NAME"
  else
    echo "npm package install failed; falling back to source install."
    install_from_source
  fi
else
  echo "npm package is not available yet; falling back to source install."
  install_from_source
fi

install_skill_to_dir "$CODEX_SKILL_DIR" "Codex"
install_skill_to_dir "$OPENCLAW_SKILL_DIR" "OpenClaw"

echo ""
echo "Installed qg CLI:"
qg --version
echo ""
echo "Installed Codex skill: $CODEX_SKILL_DIR"
echo "Installed OpenClaw skill: $OPENCLAW_SKILL_DIR"
echo "Try: qg list --today --available"
