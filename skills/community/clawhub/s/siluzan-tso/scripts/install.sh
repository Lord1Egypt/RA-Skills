#!/usr/bin/env bash
# =============================================================================
# siluzan-tso-cli - One-click install script
# Supported: macOS, Linux, Windows (WSL)
# =============================================================================

set -euo pipefail

# -- Package info (injected at build time) ------------------------------------
readonly PKG_NAME="siluzan-tso-cli"
# PKG_VERSION 锁定到与本脚本同批构建产物一致的版本，避免与 dist/skill 错位
readonly PKG_VERSION="1.1.30"
readonly CLI_BIN="siluzan-tso"
readonly SKILL_LABEL="Siluzan TSO"
readonly INSTALL_CMD="npm install -g siluzan-tso-cli"
readonly WEB_BASE="https://www.siluzan.com"

# -- Constants ----------------------------------------------------------------
readonly NODE_MAJOR_MIN=18
readonly NPM_MIRROR="https://registry.npmmirror.com"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

info()  { printf "${GREEN}[OK]${NC} %s\n" "$1"; }
warn()  { printf "${YELLOW}[!]${NC} %s\n" "$1"; }
error() { printf "${RED}[X]${NC} %s\n" "$1" >&2; }
step()  { printf "\n${BOLD}-- %s --${NC}\n" "$1"; }

# -- Detect OS ----------------------------------------------------------------
detect_os() {
  local uname_out
  uname_out=$(uname -s 2>/dev/null || echo "Unknown")
  case "$uname_out" in
    Darwin*)  echo "macos" ;;
    Linux*)   echo "linux" ;;
    MINGW*|MSYS*|CYGWIN*) echo "gitbash" ;;
    *)        echo "unknown" ;;
  esac
}

# -- Node.js ------------------------------------------------------------------
node_version_ok() {
  command -v node >/dev/null 2>&1 || return 1
  local major
  major=$(node -v | tr -d 'v' | cut -d. -f1)
  [ "$major" -ge "$NODE_MAJOR_MIN" ]
}

install_node() {
  local os_type
  os_type=$(detect_os)
  case "$os_type" in
    macos)
      if command -v brew >/dev/null 2>&1; then
        info "Installing Node.js LTS via Homebrew..."
        brew install node@22
        brew link --overwrite node@22 2>/dev/null || true
      else
        info "Installing Node.js LTS via install-node.vercel.app..."
        curl -fsSL https://install-node.vercel.app/lts | bash -s -- --yes
      fi
      ;;
    linux)
      if command -v apt-get >/dev/null 2>&1; then
        info "Installing Node.js 22.x via NodeSource (apt)..."
        curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
        sudo apt-get install -y nodejs
      elif command -v yum >/dev/null 2>&1; then
        info "Installing Node.js 22.x via NodeSource (yum)..."
        curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo -E bash -
        sudo yum install -y nodejs
      else
        info "Installing Node.js LTS via install-node.vercel.app..."
        curl -fsSL https://install-node.vercel.app/lts | bash -s -- --yes
      fi
      ;;
    gitbash)
      error "Cannot auto-install Node.js in Git Bash. Please use the PowerShell script or install manually."
      echo "  https://nodejs.org/en/download/"
      exit 1
      ;;
    *)
      error "Unsupported OS. Please install Node.js >= ${NODE_MAJOR_MIN} manually:"
      echo "  https://nodejs.org/en/download/"
      exit 1
      ;;
  esac

  export PATH="$HOME/.local/bin:$HOME/.nodejs/bin:/usr/local/bin:$PATH"
  hash -r 2>/dev/null || true

  if ! node_version_ok; then
    error "Node.js installation failed. Please install manually:"
    echo "  https://nodejs.org/en/download/"
    exit 1
  fi
}

# -- Main ---------------------------------------------------------------------
main() {
  echo ""
  echo -e "${BOLD}+---------------------------------------------+${NC}"
  echo -e "${BOLD}|  ${SKILL_LABEL} -- Install                  |${NC}"
  echo -e "${BOLD}+---------------------------------------------+${NC}"
  echo ""

  # Step 1: Environment check
  step "Step 1/4: Environment check"

  if node_version_ok; then
    info "Node.js $(node -v) found"
  else
    if command -v node >/dev/null 2>&1; then
      warn "Node.js $(node -v) is too old (need >= ${NODE_MAJOR_MIN}), upgrading..."
    else
      warn "Node.js not found, installing..."
    fi
    install_node
    info "Node.js $(node -v) installed"
  fi

  if command -v pnpm >/dev/null 2>&1; then
    PKG_MANAGER="pnpm"
  elif command -v npm >/dev/null 2>&1; then
    PKG_MANAGER="npm"
  else
    error "npm not found (Node.js installation may be incomplete)"
    exit 1
  fi
  info "$PKG_MANAGER ready"

  local current_registry
  current_registry=$(npm config get registry 2>/dev/null || echo "")
  if [ "$current_registry" != "$NPM_MIRROR" ] && [ "$current_registry" != "${NPM_MIRROR}/" ]; then
    info "Switching npm registry to China mirror for faster downloads..."
    npm config set registry "$NPM_MIRROR"
    info "npm registry set to $NPM_MIRROR"
  else
    info "npm registry already set to China mirror"
  fi

  # Step 2: Install CLI
  step "Step 2/4: Install ${PKG_NAME}"

  # 用打包时锁定的 PKG_VERSION，保证脚本与同批 dist/skill 行为对齐
  local install_target="${PKG_NAME}@${PKG_VERSION}"
  info "Running: $PKG_MANAGER install -g ${install_target}"
  $PKG_MANAGER install -g "${install_target}"
  info "${install_target} installed"

  info "Registering Skill to all AI platform global directories..."
  ${CLI_BIN} init --global --force

  if [ "${CLI_BIN}" = "siluzan-seo" ]; then
    info "siluzan-seo does not require login; skipping API Key setup."
  else
    step "Step 3/4: Configure API Key"
    echo ""
    ${CLI_BIN} login
  fi

  # Step 4: Done
  step "Step 4/4: Complete"
  echo ""
  echo -e "  ${GREEN}${SKILL_LABEL} installed successfully!${NC}"
  echo ""
  echo "  Skill registered to these global directories (all AI assistants):"
  echo -e "  ${DIM}~/.cursor/skills/  ~/.claude/skills/  ~/.agents/skills/"
  echo -e "  ~/.gemini/skills/  ~/.codex/skills/   ~/.kilo/skills/"
  echo -e "  ~/.codeium/windsurf/skills/  ~/.config/opencode/skills/"
  echo -e "  ~/.openclaw/skills/  ~/.workbuddy/skills/${NC}"
  echo ""
  echo "  Update CLI & Skill files: ${CLI_BIN} update"
  echo ""
  info "Need help? Visit ${WEB_BASE}"
  echo ""
}

main "$@"
