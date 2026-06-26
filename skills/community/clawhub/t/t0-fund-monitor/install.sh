#!/bin/bash
# T+0 基金监控系统 - 一键安装脚本

set -e

SKILL_DIR=~/.openclaw/skills/fund-monitor
LOG_FILE=/tmp/fund-monitor-install.log

echo "========================================"
echo "  T+0 基金监控系统 - 安装脚本"
echo "========================================"
echo ""

# 检查 Python
echo "1. 检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python3 未安装"
    exit 1
fi

# 检查 pip
echo ""
echo "2. 检查 pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo "   ✅ $PIP_VERSION"
else
    echo "   ❌ pip3 未安装"
    exit 1
fi

# 创建目录
echo ""
echo "3. 创建目录..."
mkdir -p $SKILL_DIR/{tools,config,data,logs,references}
echo "   ✅ 目录已创建"

# 安装依赖
echo ""
echo "4. 安装 Python 依赖..."
pip3 install akshare pandas APScheduler pyyaml -q 2>&1 | tee -a $LOG_FILE

# 尝试安装 TA-Lib
echo ""
echo "5. 安装 TA-Lib..."
if pip3 install TA-Lib -q 2>&1 | tee -a $LOG_FILE; then
    echo "   ✅ TA-Lib 安装成功"
else
    echo "   ⚠️ TA-Lib 安装失败，尝试使用预编译包..."
    if pip3 install TA-Lib --only-binary :all: -q 2>&1 | tee -a $LOG_FILE; then
        echo "   ✅ TA-Lib 预编译包安装成功"
    else
        echo "   ❌ TA-Lib 安装失败，请手动安装 libta-lib-dev"
        echo "      Ubuntu/Debian: apt-get install libta-lib-dev"
        echo "      CentOS/RHEL: yum install ta-lib"
    fi
fi

# 设置权限
echo ""
echo "6. 设置权限..."
chmod +x $SKILL_DIR/tools/*.py 2>/dev/null || true
chmod +x $SKILL_DIR/tools/*.sh 2>/dev/null || true
echo "   ✅ 权限已设置"

# 验证安装
echo ""
echo "7. 验证安装..."
if python3 -c "import akshare, pandas, apscheduler, yaml" 2>&1 | tee -a $LOG_FILE; then
    echo "   ✅ 核心依赖验证通过"
else
    echo "   ❌ 依赖验证失败"
    exit 1
fi

# 创建默认配置
echo ""
echo "8. 创建默认配置..."
if [ ! -f $SKILL_DIR/config/default.yaml ]; then
    cat > $SKILL_DIR/config/default.yaml << 'YAML'
monitor:
  interval: 60
  fast_mode: true
  market_hours:
    start: "09:30"
    end: "15:00"
    noon_break:
      start: "11:30"
      end: "13:00"

signals:
  buy:
    kdj_max: 20
    kdj_early: 30
    volume_ratio: 1.2
  sell:
    kdj_min: 80

notify:
  terminal:
    enabled: true
    sound: true
YAML
    echo "   ✅ 配置已创建"
else
    echo "   ⚠️ 配置已存在，跳过"
fi

# 完成
echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "下一步:"
echo "  1. 添加基金："
echo "     $SKILL_DIR/tools/monitor.py add 512880,513050,159915"
echo ""
echo "  2. 启动监控："
echo "     $SKILL_DIR/tools/monitor.py start"
echo ""
echo "  3. 查看状态："
echo "     $SKILL_DIR/tools/monitor.py status"
echo ""
echo "日志文件：$LOG_FILE"
echo ""
