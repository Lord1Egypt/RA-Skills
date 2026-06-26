#!/usr/bin/env bash
# shellcheck source=/dev/null
# setup.sh — general-purpose dev environment provisioner
#
# Installs a baseline development environment inside a Vagrant VM:
#   - System packages (build tools, networking, debug)
#   - Docker
#   - Go
#   - Mage build tool
#   - KVM tools (if nested KVM available)
#
# Idempotent: safe to run multiple times.
# Run as root (Vagrant provisioner handles this).

set -euo pipefail

# ─── Colors ─────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }

# ─── Versions ────────────────────────────────────────────────────────────────
GO_VERSION="${GO_VERSION:-1.24.3}"

ARCH=$(uname -m)

# ─── Preflight ───────────────────────────────────────────────────────────────
info "Checking prerequisites..."
[[ $EUID -eq 0 ]] || error "Must run as root"

info "Prerequisites OK: root, arch=$ARCH"

# ─── 1. System packages ────────────────────────────────────────────────────
install_system_deps() {
    info "Installing system packages (apt-get install is idempotent)..."
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq \
        build-essential \
        gcc \
        curl \
        git \
        jq \
        iptables \
        dnsmasq \
        dnsutils \
        net-tools \
        iproute2 \
        ca-certificates \
        gnupg \
        sqlite3 \
        libsqlite3-dev \
        procps \
        strace \
        util-linux \
        > /dev/null

    # dnsmasq conflicts with systemd-resolved on port 53; disable it by default
    systemctl stop dnsmasq 2>/dev/null || true
    systemctl disable dnsmasq 2>/dev/null || true

    info "System packages installed"
}

# ─── 2. Docker ──────────────────────────────────────────────────────────────
install_docker() {
    if command -v docker &>/dev/null; then
        info "Docker already installed: $(docker --version | awk '{print $3}' | tr -d ',')"
        return 0
    fi

    info "Installing Docker..."
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io > /dev/null

    systemctl enable --now docker
    usermod -aG docker vagrant

    info "Docker installed"
}

# ─── 3. Go ──────────────────────────────────────────────────────────────────
install_go() {
    if [[ -x /usr/local/go/bin/go ]]; then
        local installed_ver
        installed_ver=$(/usr/local/go/bin/go version | awk '{print $3}' | tr -d 'go')
        if [[ "$installed_ver" == "$GO_VERSION" ]]; then
            info "Go already installed: v${installed_ver}"
            return 0
        fi
        info "Upgrading Go from v${installed_ver} to v${GO_VERSION}..."
        rm -rf /usr/local/go
    fi

    info "Installing Go v${GO_VERSION}..."

    # Determine arch for Go download
    local go_arch
    case "$ARCH" in
        x86_64)  go_arch="amd64" ;;
        aarch64) go_arch="arm64" ;;
        arm64)   go_arch="arm64" ;;
        *)       error "Unsupported architecture for Go: $ARCH" ;;
    esac

    local go_tarball="go${GO_VERSION}.linux-${go_arch}.tar.gz"
    local go_base_url="https://go.dev/dl"
    local tmpdir
    tmpdir="$(mktemp -d)"

    curl -fsSL "${go_base_url}/${go_tarball}" -o "${tmpdir}/${go_tarball}"

    info "Verifying Go tarball checksum..."
    # Get expected hash from Go's JSON download API
    local expected_hash
    expected_hash=$(curl -fsSL "https://go.dev/dl/?mode=json&include=all" \
        | jq -r ".[] | select(.version==\"go${GO_VERSION}\") | .files[] | select(.filename==\"${go_tarball}\") | .sha256")

    if [[ -z "$expected_hash" ]]; then
        warn "Could not fetch checksum from Go API — skipping verification"
    else
        echo "${expected_hash}  ${go_tarball}" > "${tmpdir}/checksum"
        (cd "${tmpdir}" && sha256sum -c checksum)
    fi

    info "Extracting Go to /usr/local..."
    tar -C /usr/local -xzf "${tmpdir}/${go_tarball}"
    rm -rf "${tmpdir}"

    # Make Go available system-wide (login + non-login shells)
    cat > /etc/profile.d/go.sh << 'GOEOF'
export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"
export GOPATH="$HOME/go"
GOEOF

    info "Go v${GO_VERSION} installed"
}

# ─── 4. Mage ───────────────────────────────────────────────────────────────
install_mage() {
    export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"
    export GOPATH="$HOME/go"

    if command -v mage &>/dev/null; then
        info "Mage already installed"
        return 0
    fi

    info "Installing mage..."
    go install github.com/magefile/mage@latest
    cp "$HOME/go/bin/mage" /usr/local/bin/mage

    info "Mage installed"
}

# ─── 5. KVM tools (if available) ───────────────────────────────────────────
install_kvm_tools() {
    if [[ ! -e /dev/kvm ]]; then
        warn "KVM not available (/dev/kvm missing) — skipping KVM tools"
        warn "Nested KVM requires host-passthrough CPU mode"
        return 0
    fi

    info "KVM available — installing KVM tools..."
    apt-get install -y -qq qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils > /dev/null
    usermod -aG libvirt vagrant 2>/dev/null || true
    usermod -aG kvm vagrant 2>/dev/null || true

    info "KVM tools installed"
}

# ─── Run ─────────────────────────────────────────────────────────────────────
info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "vagrant-skill: dev environment setup"
info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

install_system_deps
install_docker
install_go
install_mage
install_kvm_tools

info ""
info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "Setup complete!"
info ""
info "  Tooling:    Go, Docker, mage, build-essential"
info "  KVM:        $(test -e /dev/kvm && echo 'available' || echo 'not available')"
if [[ -d /project ]]; then
    info "  Project:    /project (synced from host)"
fi
info ""
info "Quick start:"
info "  vagrant ssh"
info "  cd /project && make build   # or whatever your project uses"
info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
