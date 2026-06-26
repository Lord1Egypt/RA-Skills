#!/usr/bin/env bash
# ================================================================
# Skills Monitor 服务器端一键部署脚本
# ================================================================
# 目标环境：腾讯云轻量应用服务器 (2核2G) OpenCloudOS 9.4
# 使用方式：
#   1. 本地执行 pack_and_upload.sh 打包上传到服务器
#   2. 服务器上自动执行此脚本
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

# ──────── 配置变量 ────────
APP_NAME="skills-monitor"
APP_DIR="/www/wwwroot/skills-monitor"
VENV_DIR="${APP_DIR}/venv"
LOG_DIR="${APP_DIR}/logs"
DATA_DIR="${APP_DIR}/server/data"
DEPLOY_SOURCE="${DEPLOY_SOURCE:-/tmp/skills-monitor-deploy}"
DOMAIN="${SM_DOMAIN:-}"
PORT=5100

# ──────── 前置检查 ────────
echo ""
echo "============================================="
echo "  Skills Monitor 一键部署"
echo "  目标目录: ${APP_DIR}"
echo "============================================="
echo ""

if [[ $EUID -ne 0 ]]; then
    fail "请使用 root 用户运行此脚本"
fi

# 打印系统信息
info "系统信息:"
info "  $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2 | tr -d '"' || uname -s)"
info "  内存: $(free -h | awk '/Mem:/{print $2}') / 磁盘可用: $(df -h / | awk 'NR==2{print $4}')"
echo ""

# ──────── Step 1: 安装系统依赖 ────────
info "Step 1/7: 检查并安装系统依赖..."

# 判断包管理器
if command -v dnf &>/dev/null; then
    PKG_MGR="dnf"
    # OpenCloudOS / RHEL 系
    dnf install -y -q python3 python3-pip supervisor nginx rsync 2>/dev/null || true
elif command -v yum &>/dev/null; then
    PKG_MGR="yum"
    yum install -y -q python3 python3-pip supervisor nginx rsync 2>/dev/null || true
elif command -v apt-get &>/dev/null; then
    PKG_MGR="apt"
    apt-get update -qq
    apt-get install -y -qq python3 python3-venv python3-pip supervisor nginx rsync > /dev/null 2>&1
else
    fail "不支持的包管理器，请手动安装 python3, supervisor, nginx"
fi

# 检查 Python 版本
PYTHON_BIN=$(command -v python3.11 || command -v python3.10 || command -v python3.9 || command -v python3)
PYTHON_VERSION=$($PYTHON_BIN --version 2>&1 | awk '{print $2}')
info "  Python: ${PYTHON_BIN} (${PYTHON_VERSION})"

# 版本检查：至少 3.9
PY_MINOR=$($PYTHON_BIN -c "import sys; print(sys.version_info.minor)")
PY_MAJOR=$($PYTHON_BIN -c "import sys; print(sys.version_info.major)")
if [[ $PY_MAJOR -lt 3 ]] || [[ $PY_MAJOR -eq 3 && $PY_MINOR -lt 9 ]]; then
    fail "需要 Python >= 3.9，当前版本 ${PYTHON_VERSION}"
fi

ok "系统依赖已就绪 (${PKG_MGR})"

# ──────── Step 2: 创建项目目录 ────────
info "Step 2/7: 创建项目目录..."

mkdir -p "${APP_DIR}"
mkdir -p "${LOG_DIR}"
mkdir -p "${DATA_DIR}"

ok "目录已创建: ${APP_DIR}"

# ──────── Step 3: 复制代码 ────────
info "Step 3/7: 部署代码文件..."

if [[ ! -d "${DEPLOY_SOURCE}/server" ]]; then
    fail "找不到部署源码: ${DEPLOY_SOURCE}/server"
fi

# 备份旧数据库
if [[ -f "${DATA_DIR}/skills_monitor_server.db" ]]; then
    BACKUP_NAME="skills_monitor_server.db.bak.$(date +%Y%m%d_%H%M%S)"
    cp "${DATA_DIR}/skills_monitor_server.db" "${DATA_DIR}/${BACKUP_NAME}"
    info "  已备份数据库: ${BACKUP_NAME}"
fi

# 复制代码
rsync -a --delete \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='venv/' \
    --exclude='.env' \
    --exclude='server/data/*.db' \
    --exclude='server/data/*.db.*' \
    --exclude='logs/' \
    "${DEPLOY_SOURCE}/server/" "${APP_DIR}/server/"

rsync -a --delete \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    "${DEPLOY_SOURCE}/skills_monitor/" "${APP_DIR}/skills_monitor/"

cp -f "${DEPLOY_SOURCE}/requirements.txt" "${APP_DIR}/"
cp -f "${DEPLOY_SOURCE}/setup.py"          "${APP_DIR}/"
[[ -f "${DEPLOY_SOURCE}/README.md" ]] && cp -f "${DEPLOY_SOURCE}/README.md" "${APP_DIR}/"

ok "代码已部署"

# ──────── Step 4: 创建/更新虚拟环境 ────────
info "Step 4/7: 配置 Python 虚拟环境..."

if [[ ! -d "${VENV_DIR}" ]]; then
    $PYTHON_BIN -m venv "${VENV_DIR}"
    info "  虚拟环境已创建"
else
    info "  虚拟环境已存在，复用"
fi

source "${VENV_DIR}/bin/activate"

pip install --upgrade pip -q 2>/dev/null
pip install -r "${APP_DIR}/requirements.txt" -q 2>/dev/null
pip install gunicorn -q 2>/dev/null

ok "依赖已安装"

# ──────── Step 5: 创建 .env ────────
info "Step 5/7: 检查环境变量配置..."

ENV_FILE="${APP_DIR}/.env"
if [[ ! -f "${ENV_FILE}" ]]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    cat > "${ENV_FILE}" << ENVEOF
# ============================================
# Skills Monitor 环境变量配置
# 生成时间: $(date '+%Y-%m-%d %H:%M:%S')
# ============================================

# ──── 基础配置 ────
SM_SECRET_KEY=${SECRET_KEY}
SM_DEBUG=false
SM_HOST=127.0.0.1
SM_PORT=${PORT}

# ──── 数据库 ────
SM_DB_TYPE=sqlite
SM_DATABASE_URL=sqlite:///${DATA_DIR}/skills_monitor_server.db

# ──── 微信公众号 ────
SM_WECHAT_OA_APP_ID=
SM_WECHAT_OA_APP_SECRET=
SM_WECHAT_OA_TOKEN=skills-monitor-wechat
SM_WECHAT_OA_AES_KEY=
SM_WECHAT_TPL_DAILY=
SM_WECHAT_TPL_ALERT=

# ──── 微信小程序 ────
SM_WECHAT_MP_APP_ID=
SM_WECHAT_MP_APP_SECRET=

# ──── H5 页面 ────
SM_H5_BASE_URL=http://localhost:${PORT}

# ──── 推送时间 ────
SM_REPORT_HOUR=21
SM_REPORT_MINUTE=0
ENVEOF
    chmod 600 "${ENV_FILE}"
    warn ".env 已创建，请稍后编辑: ${ENV_FILE}"
else
    ok ".env 已存在，跳过创建"
fi

# ──────── Step 6: Gunicorn + Supervisor 配置 ────────
info "Step 6/7: 配置 Gunicorn + Supervisor..."

# Gunicorn 配置
cat > "${APP_DIR}/gunicorn.conf.py" << 'GUNIEOF'
# Gunicorn 配置 — 2核2G 优化版
import multiprocessing

bind = "127.0.0.1:5100"
workers = 1
worker_class = "gthread"
threads = 4
timeout = 120
keepalive = 5
graceful_timeout = 30
max_requests = 500
max_requests_jitter = 50
accesslog = "/www/wwwroot/skills-monitor/logs/access.log"
errorlog = "/www/wwwroot/skills-monitor/logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" %(L)ss'
preload_app = True
GUNIEOF

# 启动脚本
cat > "${APP_DIR}/start.sh" << 'STARTEOF'
#!/usr/bin/env bash
set -a
source /www/wwwroot/skills-monitor/.env
set +a
cd /www/wwwroot/skills-monitor
exec /www/wwwroot/skills-monitor/venv/bin/gunicorn \
    -c /www/wwwroot/skills-monitor/gunicorn.conf.py \
    "server.app:create_app()"
STARTEOF
chmod +x "${APP_DIR}/start.sh"

# ──── 自动检测 Supervisor 配置目录 ────
SUPERVISOR_CONF_DIR=""
if [[ -d "/etc/supervisord.d" ]]; then
    # OpenCloudOS / RHEL 系: /etc/supervisord.d/*.ini
    SUPERVISOR_CONF_DIR="/etc/supervisord.d"
    SUPERVISOR_CONF_EXT=".ini"
elif [[ -d "/etc/supervisor/conf.d" ]]; then
    # Debian / Ubuntu: /etc/supervisor/conf.d/*.conf
    SUPERVISOR_CONF_DIR="/etc/supervisor/conf.d"
    SUPERVISOR_CONF_EXT=".conf"
else
    # 尝试从 supervisord.conf 中找
    if [[ -f "/etc/supervisord.conf" ]]; then
        INCLUDE_DIR=$(grep -oP 'files\s*=\s*\K[^\s]+' /etc/supervisord.conf 2>/dev/null | head -1 | sed 's|/\*\.ini||;s|/\*\.conf||')
        if [[ -n "${INCLUDE_DIR}" ]]; then
            mkdir -p "${INCLUDE_DIR}"
            SUPERVISOR_CONF_DIR="${INCLUDE_DIR}"
            SUPERVISOR_CONF_EXT=".ini"
        fi
    fi
fi

if [[ -z "${SUPERVISOR_CONF_DIR}" ]]; then
    # 最终回退
    mkdir -p "/etc/supervisord.d"
    SUPERVISOR_CONF_DIR="/etc/supervisord.d"
    SUPERVISOR_CONF_EXT=".ini"
    warn "未检测到 Supervisor 配置目录，使用默认路径: ${SUPERVISOR_CONF_DIR}"
fi

SUPERVISOR_CONF_FILE="${SUPERVISOR_CONF_DIR}/${APP_NAME}${SUPERVISOR_CONF_EXT}"
info "  Supervisor 配置: ${SUPERVISOR_CONF_FILE}"

cat > "${SUPERVISOR_CONF_FILE}" << SUPEOF
[program:${APP_NAME}]
command=${APP_DIR}/start.sh
directory=${APP_DIR}
user=root
autostart=true
autorestart=true
startsecs=5
startretries=3
redirect_stderr=false
stdout_logfile=${LOG_DIR}/supervisor_stdout.log
stderr_logfile=${LOG_DIR}/supervisor_stderr.log
stdout_logfile_maxbytes=5MB
stdout_logfile_backups=3
stderr_logfile_maxbytes=5MB
stderr_logfile_backups=3
stopwaitsecs=30
stopsignal=TERM
SUPEOF

# 确保 supervisord 正在运行
if ! pgrep -x supervisord > /dev/null 2>&1; then
    info "  启动 supervisord..."
    systemctl enable supervisord 2>/dev/null || true
    systemctl start supervisord 2>/dev/null || supervisord -c /etc/supervisord.conf 2>/dev/null || true
    sleep 2
fi

# 重载并启动
supervisorctl reread  > /dev/null 2>&1 || true
supervisorctl update  > /dev/null 2>&1 || true

if supervisorctl status "${APP_NAME}" 2>/dev/null | grep -q RUNNING; then
    supervisorctl restart "${APP_NAME}" > /dev/null 2>&1
    info "  服务已重启"
else
    supervisorctl start "${APP_NAME}" > /dev/null 2>&1 || true
    info "  服务已启动"
fi

ok "Supervisor 进程管理已配置"

# ──────── Step 7: Nginx 反向代理 ────────
info "Step 7/7: 配置 Nginx 反向代理..."

# 安装 Nginx（如果没有的话）
if ! command -v nginx &>/dev/null; then
    info "  正在安装 Nginx..."
    if [[ "${PKG_MGR}" == "dnf" ]]; then
        dnf install -y -q nginx 2>/dev/null || true
    elif [[ "${PKG_MGR}" == "yum" ]]; then
        yum install -y -q nginx 2>/dev/null || true
    elif [[ "${PKG_MGR}" == "apt" ]]; then
        apt-get install -y -qq nginx > /dev/null 2>&1 || true
    fi
fi

# 获取 server_name
if [[ -n "${DOMAIN}" ]]; then
    SERVER_NAME="${DOMAIN}"
else
    PUBLIC_IP=$(curl -s --max-time 5 ifconfig.me 2>/dev/null || echo "_")
    SERVER_NAME="${PUBLIC_IP}"
fi

# 检测 Nginx 配置目录
NGINX_CONF_DIR=""
if [[ -d "/etc/nginx/conf.d" ]]; then
    NGINX_CONF_DIR="/etc/nginx/conf.d"
elif [[ -d "/etc/nginx/sites-available" ]]; then
    NGINX_CONF_DIR="/etc/nginx/sites-available"
fi

if [[ -n "${NGINX_CONF_DIR}" ]]; then
    NGINX_CONF="${NGINX_CONF_DIR}/${APP_NAME}.conf"
else
    NGINX_CONF="${APP_DIR}/nginx_${APP_NAME}.conf"
fi

cat > "${NGINX_CONF}" << NGINXEOF
# Skills Monitor Nginx 反向代理
server {
    listen 80;
    server_name ${SERVER_NAME};

    location /static/ {
        alias ${APP_DIR}/server/static/;
        expires 7d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location = /health {
        proxy_pass http://127.0.0.1:${PORT};
        access_log off;
    }

    location / {
        proxy_pass http://127.0.0.1:${PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 10s;
        client_max_body_size 10m;
    }
}
NGINXEOF

# 启动 Nginx
if command -v nginx &>/dev/null; then
    # 如果有 sites-enabled 目录，创建软链
    if [[ -d "/etc/nginx/sites-enabled" ]] && [[ ! -L "/etc/nginx/sites-enabled/${APP_NAME}.conf" ]]; then
        ln -sf "${NGINX_CONF}" "/etc/nginx/sites-enabled/${APP_NAME}.conf"
    fi

    # 测试并重载
    if nginx -t 2>/dev/null; then
        systemctl enable nginx 2>/dev/null || true
        systemctl restart nginx 2>/dev/null || nginx -s reload 2>/dev/null || true
        ok "Nginx 已配置并启动"
    else
        warn "Nginx 配置测试失败，请检查: nginx -t"
    fi
else
    warn "Nginx 安装失败，配置已保存到: ${NGINX_CONF}"
    warn "请手动安装后使用此配置"
fi

# ──────── 开放防火墙端口 ────────
if command -v firewall-cmd &>/dev/null; then
    firewall-cmd --permanent --add-service=http  2>/dev/null || true
    firewall-cmd --permanent --add-service=https 2>/dev/null || true
    firewall-cmd --reload 2>/dev/null || true
    info "  防火墙已开放 80/443 端口"
fi

# ──────── 健康检查 ────────
echo ""
info "等待服务启动..."
sleep 3

HEALTH_OK=false
for i in 1 2 3 4 5; do
    if curl -sf "http://127.0.0.1:${PORT}/health" > /dev/null 2>&1; then
        HEALTH_OK=true
        break
    fi
    sleep 2
done

echo ""
echo "============================================="
if $HEALTH_OK; then
    HEALTH_RESP=$(curl -s "http://127.0.0.1:${PORT}/health" 2>/dev/null)
    echo -e "  ${GREEN}✅ Skills Monitor 部署成功！${NC}"
    echo ""
    echo "  健康检查: ${HEALTH_RESP}"
else
    echo -e "  ${YELLOW}⚠️  服务可能还在启动中${NC}"
    echo "  查看日志: tail -f ${LOG_DIR}/error.log"
    echo "  查看进程: supervisorctl status ${APP_NAME}"
fi

echo ""
echo "  项目目录:  ${APP_DIR}"
echo "  日志目录:  ${LOG_DIR}"
echo "  环境配置:  ${APP_DIR}/.env"
echo "  内网地址:  http://127.0.0.1:${PORT}"
echo "  外网地址:  http://${SERVER_NAME}"
echo ""
echo "  常用命令:"
echo "    supervisorctl status ${APP_NAME}"
echo "    supervisorctl restart ${APP_NAME}"
echo "    tail -f ${LOG_DIR}/error.log"
echo "    vim ${APP_DIR}/.env"
echo ""
echo "  下一步:"
echo "    1. 编辑 .env 填入微信公众号/小程序配置"
echo "    2. supervisorctl restart ${APP_NAME}"
echo "    3. 本地 Agent: export SM_SERVER_URL=\"http://${SERVER_NAME}\""
echo "============================================="
echo ""
