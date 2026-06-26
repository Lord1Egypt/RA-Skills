#!/bin/bash
# 启动上下文压缩系统

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
SYSTEM_PID_FILE="$SCRIPT_DIR/system.pid"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否已经在运行
if [ -f "$SYSTEM_PID_FILE" ]; then
    SYSTEM_PID=$(cat "$SYSTEM_PID_FILE")
    if kill -0 "$SYSTEM_PID" 2>/dev/null; then
        log_warning "上下文压缩系统已经在运行 (PID: $SYSTEM_PID)"
        echo "使用 stop_system.sh 停止系统"
        exit 1
    else
        log_warning "发现旧的PID文件，清理中..."
        rm "$SYSTEM_PID_FILE"
    fi
fi

echo "=" | tr "=" "="
echo "   上下文压缩系统启动"
echo "=" | tr "=" "="
echo ""

# 1. 检查依赖
log_info "检查依赖..."
if ! command -v python3 &> /dev/null; then
    log_error "Python3 未安装"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log_info "Python 版本: $PYTHON_VERSION"

# 2. 检查组件
log_info "检查组件..."
COMPONENTS=("monitor.py" "hierarchical_compactor.py" "config.json")
MISSING_COMPONENTS=()

for component in "${COMPONENTS[@]}"; do
    if [ -f "$SCRIPT_DIR/$component" ]; then
        log_success "  $component ✓"
    else
        log_error "  $component ✗"
        MISSING_COMPONENTS+=("$component")
    fi
done

if [ ${#MISSING_COMPONENTS[@]} -gt 0 ]; then
    log_error "缺少组件: ${MISSING_COMPONENTS[*]}"
    exit 1
fi

# 3. 检查数据库
log_info "检查数据库..."
DB_FILE="$SCRIPT_DIR/context_compactor.db"
if [ -f "$DB_FILE" ]; then
    DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
    log_info "  数据库文件: $DB_FILE ($DB_SIZE)"
else
    log_warning "  数据库文件不存在，将在首次运行时创建"
fi

# 4. 启动集成服务
log_info "启动集成服务..."
cd "$SCRIPT_DIR"

# 启动集成服务（后台运行）
nohup python3 integration.py >> "$LOG_DIR/integration.log" 2>&1 &
INTEGRATION_PID=$!

# 等待服务启动
sleep 3

if kill -0 "$INTEGRATION_PID" 2>/dev/null; then
    log_success "集成服务启动成功 (PID: $INTEGRATION_PID)"
    echo $INTEGRATION_PID > "$SYSTEM_PID_FILE"
else
    log_error "集成服务启动失败"
    echo "查看日志: $LOG_DIR/integration.log"
    exit 1
fi

# 5. 显示状态
echo ""
log_info "系统状态:"
echo "  PID: $INTEGRATION_PID"
echo "  日志目录: $LOG_DIR"
echo "  数据库: $DB_FILE"
echo "  配置: $SCRIPT_DIR/config.json"

# 6. 显示启动日志
echo ""
log_info "启动日志摘要:"
tail -n 5 "$LOG_DIR/integration.log" 2>/dev/null || echo "  无历史日志"

# 7. 显示快速命令
echo ""
echo "=" | tr "=" "="
echo "   快速命令"
echo "=" | tr "=" "="
echo "  停止系统: ./stop_system.sh"
echo "  检查状态: ./check_status.sh"
echo "  查看日志: tail -f $LOG_DIR/integration.log"
echo "  手动压缩: python3 hierarchical_compactor.py --trigger manual"
echo ""

# 8. 显示分层策略
echo "=" | tr "=" "="
echo "   分层压缩策略"
echo "=" | tr "=" "="
python3 -c "
import json
try:
    with open('$SCRIPT_DIR/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    tiers = config.get('tiers', {})
    for tier_name, tier_config in tiers.items():
        print(f'  {tier_name.upper()}层:')
        print(f'    描述: {tier_config.get(\"description\", \"N/A\")}')
        print(f'    保留天数: {tier_config.get(\"retention_days\", \"N/A\")}')
        print(f'    最大项目数: {tier_config.get(\"max_items\", \"N/A\")}')
        print(f'    重要性阈值: {tier_config.get(\"importance_threshold\", \"N/A\")}')
        print()
        
except Exception as e:
    print(f'  读取配置失败: {e}')
"

# 9. 显示触发机制
echo "=" | tr "=" "="
echo "   触发机制"
echo "=" | tr "=" "="
python3 -c "
import json
try:
    with open('$SCRIPT_DIR/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    triggers = config.get('trigger_mechanisms', {})
    for trigger_name, trigger_config in triggers.items():
        if trigger_config.get('enabled', False):
            print(f'  {trigger_name}: 启用')
            if 'threshold' in trigger_config:
                print(f'    阈值: {trigger_config[\"threshold\"]}')
            if 'interval_seconds' in trigger_config:
                print(f'    间隔: {trigger_config[\"interval_seconds\"]}秒')
            print()
        
except Exception as e:
    print(f'  读取配置失败: {e}')
"

log_success "上下文压缩系统启动完成"
echo ""
echo "系统将持续监控上下文使用情况，并根据需要自动执行压缩优化。"