#!/bin/bash
# quick-sysinfo: 快速获取本机系统信息
# 用法: sysinfo.sh [模块]
# 模块: all, cpu, mem, disk, net, env, load, proc, gpu, docker, openclaw

MODULE="${1:-all}"

# ============================================================
# 通用脱敏函数：读取 openclaw.json 并脱敏后输出
# ============================================================
sanitize_and_print_config() {
  python3 - "$@" << 'PYEOF'
import sys, json, re, os

REDACT_KEYS = sys.argv[1:]

def redact():
    return '[REDACTED]'

def should_redact(key):
    """检查字段名是否应脱敏"""
    key_lower = key.lower()
    return any(pat.lower() in key_lower for pat in REDACT_KEYS)

def sanitize(obj):
    """递归脱敏：key 匹配 → 值脱敏；否则递归"""
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if should_redact(k):
                result[k] = redact()
            else:
                result[k] = sanitize(v)
        return result
    elif isinstance(obj, list):
        return [sanitize(item) for item in obj]
    return obj

def print_safe(obj, indent=0, path=''):
    """安全打印：脱敏后只显示字段名和安全值"""
    pad = '  ' * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                print(f'{pad}{k}:')
                print_safe(v, indent + 1, path + '/' + k)
            elif isinstance(v, list):
                print(f'{pad}{k}: [列表 {len(v)} 项]')
            else:
                print(f'{pad}{k}: {v}')
    elif isinstance(obj, list):
        for i, item in enumerate(obj[:5]):
            print(f'{pad}[{i}]:')
            print_safe(item, indent + 1, path + '[]')
        if len(obj) > 5:
            print(f'{pad}  ... 共 {len(obj)} 项')

config_path = os.path.expanduser('~/.openclaw/openclaw.json')
if not os.path.exists(config_path):
    print('[配置文件不存在]')
    sys.exit(0)

try:
    with open(config_path) as f:
        data = json.load(f)

    sections = ['gateway', 'agents', 'channels', 'plugins']
    for sec in sections:
        if sec in data:
            print(f'\n=== {sec.upper()} ===')
            print_safe(sanitize(data[sec]))
except Exception as e:
    print(f'[读取失败: {e}]')
PYEOF
}

# ============================================================
# 获取脱敏后的 agent 模型名（避免 inline python 直接访问配置）
# ============================================================
get_openclaw_model() {
  python3 - << 'PYEOF'
import json, os, re

config_path = os.path.expanduser('~/.openclaw/openclaw.json')
if not os.path.exists(config_path):
    print('未知')
    sys.exit(0)

REDACT_RE = re.compile(r'(api_key|token|secret|password|key|auth_token|access_token|refresh_token|connection_string|private_key|client_secret|webhook_secret)', re.I)

try:
    with open(config_path) as f:
        data = json.load(f)

    def safe_str(v):
        s = str(v)
        return REDACT_RE.sub(lambda m: '[REDACTED]', s)

    agents = data.get('agents', {}).get('defaults', {})
    model = agents.get('model', {})
    primary = model.get('primary', '未知')

    # 脱敏后只取模型名部分
    if '/' in primary:
        # "provider/model-name" → 取 model 名
        print(primary.split('/')[-1])
    else:
        print(safe_str(primary))
except:
    print('未知')
PYEOF
}

get_openclaw_channels() {
  python3 - << 'PYEOF'
import json, os

config_path = os.path.expanduser('~/.openclaw/openclaw.json')
if not os.path.exists(config_path):
    print('未知')
    sys.exit(0)

try:
    with open(config_path) as f:
        data = json.load(f)
    ch = data.get('channels', {})
    active = [n for n, v in ch.items() if v.get('enabled')]
    print(', '.join(active) if active else '无')
except:
    print('未知')
PYEOF
}

# ============================================================
# 模块执行
# ============================================================
case "$MODULE" in
  cpu)
    echo "=== CPU 信息 ==="
    lscpu | grep -iE "^(Architecture|型号名称|Model name|CPU\(s\)|Thread|Core|Socket|CPU MHz|CPU 系列)" 2>/dev/null
    echo ""
    echo "=== CPU 使用率 ==="
    top -bn1 | head -5
    ;;
  mem)
    echo "=== 内存信息 ==="
    free -h
    echo ""
    echo "=== Swap ==="
    swapon --show 2>/dev/null || free -h | grep -iE "swap|交换" || echo "无 Swap"
    ;;
  disk)
    echo "=== 磁盘使用 ==="
    df -h | grep -E "^/dev|tmpfs"
    echo ""
    echo "=== IO 统计 (1秒采样) ==="
    iostat -x 1 1 2>/dev/null || echo "iostat 未安装"
    ;;
  net)
    echo "=== 网络接口 ==="
    ip -brief addr 2>/dev/null || ifconfig | grep -E "^[a-z]|inet "
    echo ""
    echo "=== 连接数 ==="
    ss -s 2>/dev/null | head -10
    ;;
  env)
    echo "=== 系统环境 ==="
    echo "主机名: $(hostname)"
    echo "系统: $(uname -sr)"
    echo "发行版: $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d'"' -f2)"
    echo "内核: $(uname -r)"
    echo "架构: $(uname -m)"
    echo "启动时间: $(uptime -s 2>/dev/null || who -b)"
    echo "当前用户: $(whoami)"
    echo "Shell: $SHELL"
    echo "Node: $(node -v 2>/dev/null || echo '未安装')"
    echo "Python: $(python3 --version 2>/dev/null || echo '未安装')"
    echo "Docker: $(docker --version 2>/dev/null || echo '未安装')"
    ;;
  load)
    echo "=== 系统负载 ==="
    uptime
    echo ""
    echo "=== Top 10 进程 (CPU) ==="
    ps aux --sort=-%cpu | head -11
    echo ""
    echo "=== Top 10 进程 (内存) ==="
    ps aux --sort=-%mem | head -11
    ;;
  proc)
    echo "=== 进程统计 ==="
    echo "总进程数: $(ps aux | wc -l)"
    echo "运行中: $(ps aux | awk '$8=="R"{c++}END{print c+0}')"
    echo "睡眠中: $(ps aux | awk '$8=="S"{c++}END{print c+0}')"
    echo ""
    echo "=== 关键服务状态 ==="
    for svc in sshd docker nginx openclaw-gateway; do
      status=$(systemctl is-active $svc 2>/dev/null || echo "unknown")
      echo "$svc: $status"
    done
    ;;
  gpu)
    echo "=== GPU 信息 ==="
    if command -v nvidia-smi &>/dev/null; then
      nvidia-smi --query-gpu=name,temperature.gpu,memory.used,memory.total,utilization.gpu --format=csv,noheader
    elif command -v rocm-smi &>/dev/null; then
      rocm-smi --showtemp --showmemuse --showuse
    else
      lspci | grep -i vga
    fi
    ;;
  docker)
    echo "=== Docker 容器 ==="
    docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Docker 未安装或无权限"
    echo ""
    echo "=== Docker 资源 ==="
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "无运行中容器"
    ;;
  openclaw)
    echo "=== OpenClaw 配置 ==="
    OC_BIN="$(command -v openclaw 2>/dev/null || echo 'openclaw')"
    OC_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
    echo "版本: $($OC_BIN --version 2>/dev/null || echo '未知')"
    echo ""

    # 脱敏后输出所有 section
    sanitize_and_print_config \
      api_key token secret password key \
      auth_token access_token refresh_token \
      connection_string private_key client_secret webhook_secret

    echo ""
    echo "=== 服务状态 ==="
    systemctl --user is-active openclaw-gateway 2>/dev/null || echo "  gateway: 未知"
    echo "  监听: $(ss -tlnp 2>/dev/null | grep -oP ':\K18789(?=\s)' | head -1 || echo '未知')"
    echo ""
    echo "=== Session 概览 ==="
    ls "$OC_HOME/agents/" 2>/dev/null | while read agent; do
      echo "  Agent: $agent"
    done
    ;;
  all|*)
    OC_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
    OC_CONFIG="$OC_HOME/openclaw.json"
    echo "📊 系统概览"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🖥️ 主机: $(hostname) | $(uname -sr)"
    echo "⏰ 运行: $(uptime -p 2>/dev/null || uptime)"
    echo ""
    echo "🧠 CPU:"
    cpu_model=$(lscpu | grep -i "型号名称\|Model name" | awk -F'：' '{print $2}' | sed 's/^[[:space:]]*//')
    [[ -z "$cpu_model" ]] && cpu_model=$(lscpu | grep -i "Model name" | awk -F':' '{print $2}' | sed 's/^[[:space:]]*//')
    echo "  ${cpu_model:-未知}"
    echo "  核心: $(nproc) | 负载: $(cat /proc/loadavg | cut -d' ' -f1-3)"
    echo ""
    echo "💾 内存:"
    free -h | grep -iE "Mem|内存" | awk '{printf "  总计: %s | 已用: %s | 可用: %s\n", $2, $3, $7}'
    echo ""
    echo "💿 磁盘:"
    df -h / | tail -1 | awk '{printf "  总计: %s | 已用: %s (%s) | 可用: %s\n", $2, $3, $5, $4}'
    echo ""
    echo "🌐 网络:"
    ip -4 addr show 2>/dev/null | grep inet | grep -v 127.0.0.1 | awk '{printf "  %s: %s\n", $NF, $2}'
    echo ""
    echo "🤖 OpenClaw:"
    echo "  模型: $(get_openclaw_model)"
    echo "  频道: $(get_openclaw_channels)"
    echo "  Gateway: $(systemctl --user is-active openclaw-gateway 2>/dev/null) | $(ss -tlnp 2>/dev/null | grep -oP ':\K18789(?=\s)' | head -1 || echo '未监听')"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ;;
esac
