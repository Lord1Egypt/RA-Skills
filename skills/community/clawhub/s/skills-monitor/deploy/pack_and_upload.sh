#!/usr/bin/env bash
# ================================================================
# Skills Monitor — 本地打包 & 上传到服务器
# ================================================================
# 在你的 Mac 上执行，自动打包必需的文件并上传到腾讯云服务器
#
# 使用方式:
#   # 方式 1: 交互式（会提示输入 IP）
#   bash deploy/pack_and_upload.sh
#
#   # 方式 2: 指定参数
#   bash deploy/pack_and_upload.sh root@1.2.3.4
#
#   # 方式 3: 带域名（部署时自动配置）
#   SM_DOMAIN=monitor.yourdomain.com bash deploy/pack_and_upload.sh root@1.2.3.4
# ================================================================

set -euo pipefail

# ──────── 颜色输出 ────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }

# ──────── 确定项目根目录 ────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PACK_DIR="/tmp/skills-monitor-pack"
ARCHIVE="/tmp/skills-monitor-deploy.tar.gz"
REMOTE_DIR="/tmp/skills-monitor-deploy"

cd "$PROJECT_ROOT"
info "项目根目录: ${PROJECT_ROOT}"

# ──────── 获取服务器地址 ────────
if [[ $# -ge 1 ]]; then
    SERVER_SSH="$1"
else
    echo ""
    echo -e "${BLUE}请输入服务器 SSH 连接信息${NC}"
    echo "  格式: root@<IP地址>"
    echo "  示例: root@43.128.1.100"
    echo ""
    read -p "服务器地址: " SERVER_SSH
fi

if [[ -z "${SERVER_SSH}" ]]; then
    fail "服务器地址不能为空"
fi

echo ""
echo "============================================="
echo "  Skills Monitor 打包上传"
echo "  目标服务器: ${SERVER_SSH}"
echo "============================================="
echo ""

# ──────── Step 1: 打包 ────────
info "Step 1/3: 打包项目文件..."

rm -rf "${PACK_DIR}"
mkdir -p "${PACK_DIR}"

# 复制必需的目录和文件
cp -r server/         "${PACK_DIR}/server/"
cp -r skills_monitor/ "${PACK_DIR}/skills_monitor/"
cp -r deploy/         "${PACK_DIR}/deploy/"
cp    requirements.txt "${PACK_DIR}/"
cp    setup.py         "${PACK_DIR}/"
[[ -f README.md ]] && cp README.md "${PACK_DIR}/"

# 清理不需要的文件
find "${PACK_DIR}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "${PACK_DIR}" -name "*.pyc" -delete 2>/dev/null || true
find "${PACK_DIR}" -name ".DS_Store" -delete 2>/dev/null || true

# 排除数据库文件（只部署代码，保留远端数据）
rm -f "${PACK_DIR}/server/data/"*.db 2>/dev/null || true

# 打包
cd /tmp
tar -czf "${ARCHIVE}" -C "${PACK_DIR}" .

ARCHIVE_SIZE=$(du -sh "${ARCHIVE}" | cut -f1)
ok "打包完成: ${ARCHIVE} (${ARCHIVE_SIZE})"

# ──────── Step 2: 上传 ────────
info "Step 2/3: 上传到服务器..."

# 先检测 SSH 连接是否正常（免密模式）
info "检测 SSH 连接..."
if ! ssh -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new "${SERVER_SSH}" "echo 'SSH_OK'" 2>/dev/null | grep -q "SSH_OK"; then
    echo ""
    fail "SSH 连接失败！腾讯云服务器需要先配置密钥登录。
    
  请运行:  bash deploy/setup_ssh_key.sh ${SERVER_SSH}
  
  或参考 deploy/README.md 中的 SSH 配置指南。"
fi
ok "SSH 连接正常"

# 先在远端创建目录并清理旧文件
ssh -o BatchMode=yes "${SERVER_SSH}" "rm -rf ${REMOTE_DIR} && mkdir -p ${REMOTE_DIR}"

# 上传压缩包
scp -o BatchMode=yes -q "${ARCHIVE}" "${SERVER_SSH}:/tmp/"

# 远端解压
ssh -o BatchMode=yes "${SERVER_SSH}" "cd ${REMOTE_DIR} && tar -xzf /tmp/skills-monitor-deploy.tar.gz"

ok "上传完成"

# ──────── Step 3: 远端执行部署 ────────
info "Step 3/3: 远程执行部署脚本..."
echo ""

# 构建远端环境变量
REMOTE_ENV=""
if [[ -n "${SM_DOMAIN:-}" ]]; then
    REMOTE_ENV="SM_DOMAIN=${SM_DOMAIN}"
fi

# SSH 执行远端部署脚本（不用 -t，避免触发腾讯云二维码验证）
ssh -o BatchMode=yes "${SERVER_SSH}" "${REMOTE_ENV} DEPLOY_SOURCE=${REMOTE_DIR} bash ${REMOTE_DIR}/deploy/deploy.sh"

echo ""
ok "====== 全部完成 ======"
echo ""
echo "后续操作:"
echo "  1. SSH 登录服务器编辑 .env 配置:"
echo "     ssh ${SERVER_SSH}"
echo "     vim /www/wwwroot/skills-monitor/.env"
echo ""
echo "  2. 重启服务使配置生效:"
echo "     ssh ${SERVER_SSH} 'supervisorctl restart skills-monitor'"
echo ""
echo "  3. 本地 Agent 指向服务器:"
echo "     export SM_SERVER_URL=\"http://你的服务器IP\""
echo ""

# ──────── 清理临时文件 ────────
rm -rf "${PACK_DIR}" "${ARCHIVE}"
