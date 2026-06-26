#!/usr/bin/env bash
# verify.sh — validate dev environment end-to-end
#
# Checks system prerequisites, installed tools, and optional KVM.
# Exits non-zero if any critical check fails.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

pass() { echo -e "  ${GREEN}PASS${NC} $*"; PASS=$((PASS + 1)); }
fail() { echo -e "  ${RED}FAIL${NC} $*"; FAIL=$((FAIL + 1)); }
skip() { echo -e "  ${YELLOW}SKIP${NC} $*"; WARN=$((WARN + 1)); }

check_cmd() {
    local cmd="$1"
    local label="${2:-$cmd}"
    if command -v "$cmd" &>/dev/null; then
        pass "$label"
    else
        fail "$label"
    fi
}

check_cmd_optional() {
    local cmd="$1"
    local label="${2:-$cmd}"
    if command -v "$cmd" &>/dev/null; then
        pass "$label"
    else
        skip "$label (optional)"
    fi
}

export PATH="/usr/local/go/bin:$HOME/go/bin:/usr/local/bin:$PATH"
export GOPATH="$HOME/go"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  vagrant-skill: dev environment verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ─── 1. System prerequisites ───────────────────────────────────────────────
echo -e "\n▶ System prerequisites"

if command -v docker &>/dev/null; then
    pass "Docker $(docker --version | awk '{print $3}' | tr -d ',')"
else
    fail "Docker"
fi

if [[ -x /usr/local/go/bin/go ]]; then
    pass "Go $(/usr/local/go/bin/go version | awk '{print $3}')"
else
    fail "Go"
fi

check_cmd mage "Mage"
check_cmd git "Git"
check_cmd curl "curl"
check_cmd jq "jq"

# ─── 2. KVM (optional — depends on host) ─────────────────────────────────
echo -e "\n▶ KVM / nested virtualization"

if [[ -e /dev/kvm ]]; then
    pass "KVM available (/dev/kvm)"
    check_cmd_optional qemu-system-x86_64 "QEMU"
    check_cmd_optional virsh "libvirt"
else
    skip "KVM not available (no nested virt — VirtualBox host?)"
fi

# ─── 3. Network tools ──────────────────────────────────────────────────────
echo -e "\n▶ Network tools"

for cmd in iptables ip dnsmasq dig; do
    check_cmd "$cmd"
done

# ─── 4. Docker functional test ──────────────────────────────────────────────
echo -e "\n▶ Docker functional"

if command -v docker &>/dev/null; then
    if docker info &>/dev/null; then
        pass "Docker daemon running"
    else
        fail "Docker daemon not running"
    fi
else
    skip "Docker not installed"
fi

# ─── 5. Project sync ────────────────────────────────────────────────────────
echo -e "\n▶ Project"

if [[ -d /project ]]; then
    file_count=$(find /project -maxdepth 1 -type f | wc -l)
    pass "Project synced at /project ($file_count files in root)"
else
    skip "No project synced (set PROJECT_SRC to sync)"
fi

# ─── Summary ────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  ${GREEN}PASS: $PASS${NC}  ${RED}FAIL: $FAIL${NC}  ${YELLOW}SKIP: $WARN${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ $FAIL -gt 0 ]]; then
    echo -e "\n${RED}$FAIL checks failed${NC}"
    exit 1
fi

echo -e "\n${GREEN}Dev environment fully verified!${NC}"
