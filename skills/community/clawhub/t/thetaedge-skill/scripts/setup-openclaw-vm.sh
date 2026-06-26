#!/usr/bin/env bash
#
# setup-openclaw-vm.sh
#
# Configures an Ubuntu 25.10 VirtualBox VM to run OpenClaw and Claude Code
# securely, isolated from the host machine.
#
# Usage:
#   ssh -A -p 2222 openclaw@localhost  # from host, with agent forwarding
#   bash setup-openclaw-vm.sh
#
# Prerequisites:
#   - Ubuntu 25.10 VM with user "openclaw"
#   - SSH agent forwarding enabled (for GitHub access)
#   - VirtualBox host-side isolation configured (see docs/vm-setup.md)

set -euo pipefail

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

info()  { printf '\n\033[1;34m==>\033[0m \033[1m%s\033[0m\n' "$*"; }
warn()  { printf '\033[1;33mWARN:\033[0m %s\n' "$*"; }
error() { printf '\033[1;31mERROR:\033[0m %s\n' "$*" >&2; exit 1; }

check_ubuntu() {
    if [ ! -f /etc/os-release ]; then
        error "Cannot detect OS. This script is designed for Ubuntu."
    fi
    . /etc/os-release
    if [ "$ID" != "ubuntu" ]; then
        error "This script is designed for Ubuntu, detected: $ID"
    fi
    info "Detected $PRETTY_NAME"
}

# --------------------------------------------------------------------------
# Step 1: System Update & Essential Packages
# --------------------------------------------------------------------------

install_system_packages() {
    info "Updating system packages..."
    sudo apt update && sudo apt upgrade -y

    info "Installing essential packages..."
    sudo apt install -y curl git ufw
}

# --------------------------------------------------------------------------
# Step 2: Enable and Configure SSH Server
# --------------------------------------------------------------------------

configure_ssh() {
    info "Enabling SSH server..."
    sudo systemctl enable --now ssh
    info "SSH server is running."
}

# --------------------------------------------------------------------------
# Step 3: Firewall (ufw)
# --------------------------------------------------------------------------

configure_firewall() {
    info "Configuring firewall..."

    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow 22/tcp comment "SSH for agent forwarding"
    sudo ufw allow from 127.0.0.1 to any port 18789 proto tcp comment "OpenClaw dashboard local only"
    sudo ufw --force enable

    info "Firewall enabled. Rules:"
    sudo ufw status verbose
}

# --------------------------------------------------------------------------
# Step 4: Install Node.js 22 via nvm
# --------------------------------------------------------------------------

install_nodejs() {
    info "Installing nvm and Node.js 22..."

    export NVM_DIR="$HOME/.nvm"

    if [ ! -s "$NVM_DIR/nvm.sh" ]; then
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
    fi

    # Load nvm into this shell session
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

    nvm install 22
    nvm alias default 22

    info "Node.js $(node --version) installed via nvm."
}

# --------------------------------------------------------------------------
# Step 5: Install OpenClaw
# --------------------------------------------------------------------------

install_openclaw() {
    info "Installing OpenClaw..."
    curl -fsSL https://openclaw.ai/install.sh | bash || true

    # The OpenClaw installer sets an npm prefix in ~/.npmrc which conflicts
    # with nvm. Remove it so nvm-managed node/npm work correctly.
    if [ -f "$HOME/.npmrc" ] && grep -q "prefix=" "$HOME/.npmrc"; then
        info "Removing OpenClaw's npm prefix (conflicts with nvm)..."
        rm -f "$HOME/.npmrc"
    fi

    # Ensure the npm-global bin dir is on PATH (OpenClaw installs there)
    if ! grep -q 'npm-global/bin' "$HOME/.bashrc"; then
        echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> "$HOME/.bashrc"
    fi
    export PATH="$HOME/.npm-global/bin:$PATH"

    info "OpenClaw installed."
}

# --------------------------------------------------------------------------
# Step 6: Install Claude Code
# --------------------------------------------------------------------------

install_claude_code() {
    info "Installing Claude Code..."

    # Ensure nvm/node are available
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

    npm install -g @anthropic-ai/claude-code
    info "Claude Code installed."
}

# --------------------------------------------------------------------------
# Step 7: Configure OpenClaw Securely
# --------------------------------------------------------------------------

configure_openclaw() {
    info "Configuring OpenClaw environment..."

    mkdir -p ~/.openclaw
    chmod 700 ~/.openclaw
    touch ~/.openclaw/.env
    chmod 600 ~/.openclaw/.env

    # Prompt for API key interactively (not in shell history or arguments)
    echo ""
    echo "Enter your Anthropic API key (input is hidden):"
    read -rs ANTHROPIC_API_KEY
    echo ""

    if [ -z "$ANTHROPIC_API_KEY" ]; then
        warn "No API key entered. You can add it later to ~/.openclaw/.env"
        warn "  echo 'ANTHROPIC_API_KEY=sk-...' >> ~/.openclaw/.env"
    else
        echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" >> ~/.openclaw/.env
        info "API key saved to ~/.openclaw/.env (permissions: 600)"
    fi

    unset ANTHROPIC_API_KEY
}

# --------------------------------------------------------------------------
# Step 8: Clone thetaedge-skill
# --------------------------------------------------------------------------

clone_thetaedge_skill() {
    info "Cloning thetaedge-skill..."

    local repo="git@github.com:thetaedge/thetaedge-skill.git"
    local dest="$HOME/projects/thetaedge-skill"

    if [ -d "$dest" ]; then
        info "thetaedge-skill already cloned at $dest, pulling latest..."
        git -C "$dest" pull
        return
    fi

    # Check SSH agent forwarding
    if [ -z "${SSH_AUTH_SOCK:-}" ]; then
        warn "SSH_AUTH_SOCK is not set. SSH agent forwarding may not be active."
        warn "Make sure you connected with: ssh -A -p 2222 openclaw@localhost"
        echo ""
        read -rp "Try cloning anyway? [y/N] " answer
        if [[ ! "$answer" =~ ^[Yy]$ ]]; then
            warn "Skipping clone. Run this script again with SSH agent forwarding."
            return
        fi
    fi

    # Add GitHub host key if not already known
    if ! ssh-keygen -F github.com &>/dev/null; then
        info "Adding GitHub to known hosts..."
        ssh-keyscan github.com >> "$HOME/.ssh/known_hosts" 2>/dev/null
    fi

    # Test GitHub connectivity
    info "Testing GitHub SSH access..."
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        info "GitHub SSH authentication successful."
    else
        warn "Could not confirm GitHub authentication. Attempting clone anyway..."
    fi

    mkdir -p "$HOME/projects"
    git clone "$repo" "$dest"
    info "Cloned thetaedge-skill to $dest"
}

# --------------------------------------------------------------------------
# Step 9: Register skill with OpenClaw
# --------------------------------------------------------------------------

register_skill() {
    info "Registering thetix skill with OpenClaw..."

    local skill_dir="$HOME/projects/thetaedge-skill"
    local installer="$skill_dir/scripts/install-thetix-skill.sh"

    if [ ! -f "$installer" ]; then
        warn "install-thetix-skill.sh not found at $installer. Skipping skill registration."
        return
    fi

    bash "$installer"
}

# --------------------------------------------------------------------------
# Step 10: Summary
# --------------------------------------------------------------------------

print_summary() {
    info "Setup complete!"
    echo ""
    echo "============================================"
    echo "  OpenClaw VM Setup Summary"
    echo "============================================"
    echo ""

    echo "System:"
    . /etc/os-release
    echo "  OS:       $PRETTY_NAME"
    echo "  Firewall: $(sudo ufw status | head -1)"
    echo ""

    echo "Installed:"

    # nvm/node
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
    echo "  Node.js:     $(node --version 2>/dev/null || echo 'not found')"
    echo "  npm:         $(npm --version 2>/dev/null || echo 'not found')"
    echo "  Claude Code: $(claude --version 2>/dev/null || echo 'not found')"
    echo "  OpenClaw:    $(openclaw --version 2>/dev/null || echo 'not found')"
    echo ""

    echo "Paths:"
    echo "  OpenClaw config: ~/.openclaw/"
    echo "  API key file:    ~/.openclaw/.env"
    echo "  Project:         ~/projects/thetaedge-skill/"
    echo ""

    echo "Next steps:"
    echo "  1. Verify your API key:  cat ~/.openclaw/.env"
    echo "  2. Start OpenClaw:       openclaw"
    echo "  3. Test thetix skill:    /thetix (inside Claude Code)"
    echo ""
    echo "  To re-enter API key:"
    echo "    echo 'ANTHROPIC_API_KEY=sk-...' > ~/.openclaw/.env"
    echo ""
    echo "============================================"
}

# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

main() {
    echo ""
    echo "============================================"
    echo "  OpenClaw VM Setup Script"
    echo "============================================"
    echo ""
    echo "This script will:"
    echo "  - Update system packages"
    echo "  - Configure SSH and firewall"
    echo "  - Install Node.js 22, OpenClaw, Claude Code"
    echo "  - Configure OpenClaw with your API key"
    echo "  - Clone thetaedge-skill and register the thetix skill"
    echo ""
    read -rp "Continue? [Y/n] " answer
    if [[ "$answer" =~ ^[Nn]$ ]]; then
        echo "Aborted."
        exit 0
    fi

    check_ubuntu
    install_system_packages
    configure_ssh
    configure_firewall
    install_nodejs
    install_openclaw
    install_claude_code
    configure_openclaw
    clone_thetaedge_skill
    register_skill
    print_summary
}

main "$@"
