#!/usr/bin/env bash
# ================================================================
# 腾讯云轻量应用服务器 — SSH 密钥登录配置
# ================================================================
# 腾讯云默认开启微信扫码 + 验证码验证，导致 scp 等非交互式命令失败
# 此脚本配置 SSH 密钥登录，一次配置后续免密操作
#
# 使用方式:
#   bash deploy/setup_ssh_key.sh root@82.156.182.240
# ================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }

# ──────── 获取服务器地址 ────────
if [[ $# -ge 1 ]]; then
    SERVER_SSH="$1"
else
    echo ""
    echo -e "${BLUE}请输入服务器 SSH 连接信息${NC}"
    read -p "服务器地址 (如 root@82.156.182.240): " SERVER_SSH
fi

[[ -z "${SERVER_SSH}" ]] && fail "服务器地址不能为空"

# 提取用户名和IP
SSH_USER="${SERVER_SSH%%@*}"
SSH_HOST="${SERVER_SSH##*@}"

echo ""
echo "============================================="
echo "  SSH 密钥登录配置"
echo "  服务器: ${SERVER_SSH}"
echo "============================================="
echo ""

# ──────── Step 1: 检查/生成本地密钥 ────────
info "Step 1: 检查本地 SSH 密钥..."

KEY_FILE=""
for f in ~/.ssh/id_ed25519.pub ~/.ssh/id_rsa.pub ~/.ssh/id_ecdsa.pub; do
    if [[ -f "$f" ]]; then
        KEY_FILE="$f"
        break
    fi
done

if [[ -z "$KEY_FILE" ]]; then
    info "未找到 SSH 密钥，正在生成..."
    ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "$(whoami)@$(hostname)"
    KEY_FILE=~/.ssh/id_ed25519.pub
    ok "密钥已生成: ${KEY_FILE}"
else
    ok "找到密钥: ${KEY_FILE}"
fi

PUB_KEY=$(cat "$KEY_FILE")
echo "  公钥: ${PUB_KEY:0:40}..."

# ──────── Step 2: 上传公钥 ────────
echo ""
info "Step 2: 上传公钥到服务器..."
echo ""
warn "⚠️  接下来需要通过腾讯云验证（可能有微信扫码/验证码）"
warn "   这是最后一次需要输入密码，配置完成后即可免密登录"
echo ""

# 使用 ssh-copy-id (会提示密码)
# 如果 ssh-copy-id 不可用，手动追加
if command -v ssh-copy-id &>/dev/null; then
    ssh-copy-id -i "$KEY_FILE" "${SERVER_SSH}"
else
    info "ssh-copy-id 不可用，使用手动方式..."
    cat "$KEY_FILE" | ssh "${SERVER_SSH}" "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
fi

# ──────── Step 3: 验证 ────────
echo ""
info "Step 3: 验证免密登录..."

if ssh -o BatchMode=yes -o ConnectTimeout=10 "${SERVER_SSH}" "echo 'SSH_KEY_OK'" 2>/dev/null | grep -q "SSH_KEY_OK"; then
    ok "✅ SSH 密钥登录配置成功！"
    echo ""
    echo "现在可以执行部署了:"
    echo -e "  ${GREEN}bash deploy/pack_and_upload.sh ${SERVER_SSH}${NC}"
    echo ""
else
    echo ""
    warn "自动验证未通过，可能是腾讯云安全设置导致"
    echo ""
    echo "请尝试以下替代方案："
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${YELLOW}方案 A: 腾讯云控制台配置 (推荐)${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  1. 打开腾讯云控制台 → 轻量应用服务器"
    echo "  2. 选择你的实例 → 远程登录 → 密钥"
    echo "  3. 创建密钥 → 绑定密钥 → 选择你的实例"
    echo ""
    echo "  或者手动添加公钥:"
    echo "  1. 点击实例 → 远程登录 → OrcaTerm 登录"
    echo "  2. 在 OrcaTerm 终端中执行:"
    echo ""
    echo -e "     ${BLUE}mkdir -p ~/.ssh && echo '${PUB_KEY}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys${NC}"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${YELLOW}方案 B: 通过 OrcaTerm 关闭扫码验证${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  1. 腾讯云控制台 → 实例 → 远程登录 → OrcaTerm"
    echo "  2. 在终端中执行:"
    echo ""
    echo -e "     ${BLUE}# 添加公钥"
    echo -e "     mkdir -p ~/.ssh"
    echo -e "     echo '${PUB_KEY}' >> ~/.ssh/authorized_keys"
    echo -e "     chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
    echo ""
    echo -e "     # (可选) 关闭密码登录，仅允许密钥"
    echo -e "     sed -i 's/^#\\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config"
    echo -e "     systemctl restart sshd${NC}"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "完成后再次运行部署:"
    echo -e "  ${GREEN}bash deploy/pack_and_upload.sh ${SERVER_SSH}${NC}"
fi
