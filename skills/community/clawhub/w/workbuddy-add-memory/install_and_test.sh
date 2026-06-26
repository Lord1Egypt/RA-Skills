#!/bin/bash
# WorkBuddy智能记忆管理系统 v3.0 安装和测试脚本
# 作者: zcg007
# 日期: 2026-03-15

set -e

echo "=================================================="
echo "WorkBuddy智能记忆管理系统 v3.0 安装和测试"
echo "作者: zcg007"
echo "=================================================="

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$SCRIPT_DIR"

echo "📁 技能目录: $SKILL_DIR"
echo ""

# 检查Python版本
echo "🔍 检查Python环境..."
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "   Python版本: $python_version"

if [[ $(echo "$python_version < 3.8" | bc -l) -eq 1 ]]; then
    echo "❌ 需要Python 3.8或更高版本"
    exit 1
fi

# 检查依赖
echo ""
echo "🔍 检查依赖包..."
required_packages=(
    "scikit-learn"
    "numpy"
    "pandas"
    "scipy"
    "openpyxl"
    "watchdog"
    "pyyaml"
    "toml"
    "joblib"
)

missing_packages=()
for package in "${required_packages[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -eq 0 ]; then
    echo "✅ 所有依赖包已安装"
else
    echo "⚠️  缺少依赖包: ${missing_packages[*]}"
    echo ""
    echo "📦 安装缺失依赖..."
    
    # 使用国内镜像加速
    pip_cmd="pip3 install -i https://mirrors.aliyun.com/pypi/simple/"
    
    for package in "${missing_packages[@]}"; do
        echo "   安装: $package"
        $pip_cmd "$package" || {
            echo "❌ 安装失败: $package"
            exit 1
        }
    done
    
    echo "✅ 依赖包安装完成"
fi

# 创建配置目录
echo ""
echo "⚙️  设置配置目录..."
CONFIG_DIR="$SKILL_DIR/config"
if [ ! -d "$CONFIG_DIR" ]; then
    mkdir -p "$CONFIG_DIR"
    echo "   创建配置目录: $CONFIG_DIR"
fi

# 创建示例配置文件
CONFIG_FILE="$CONFIG_DIR/main.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" << 'EOF'
# WorkBuddy智能记忆管理系统配置
# 作者: zcg007
# 日期: 2026-03-15

# 记忆源配置
memory_sources:
  - "~/.workbuddy/global_summaries/"
  - "~/.workbuddy/unified_memory/"
  - "~/.workbuddy/skills/"
  - "~/.workbuddy/learnings/"

# 检索配置
retrieval_config:
  max_results: 15
  min_relevance: 0.3
  weight_keyword: 0.6
  weight_semantic: 0.4
  boost_recent: 0.2
  boost_importance: 0.3
  cache_size: 1000
  cache_ttl: 3600  # 1小时

# 检测配置
detection_config:
  task_keywords:
    excel: ["excel", "表格", "报表", "预算", "财务", "数据"]
    analysis: ["分析", "统计", "报告", "总结", "评估"]
    skill: ["技能", "skill", "安装", "开发", "创建"]
    memory: ["记忆", "经验", "学习", "总结"]
    workflow: ["工作流", "流程", "自动化", "任务"]
  min_confidence: 0.5
  context_window: 5
  enable_intent_detection: true

# UI配置
ui_config:
  output_format: "markdown"
  max_display_items: 10
  show_relevance_scores: true
  group_by_category: true
  color_scheme: "default"

# 系统配置
system_config:
  auto_update_interval: 300  # 5分钟
  max_file_size: 10485760  # 10MB
  enable_logging: true
  log_level: "INFO"
  backup_enabled: true
  backup_count: 5
EOF
    echo "   创建示例配置文件: $CONFIG_FILE"
else
    echo "   配置文件已存在: $CONFIG_FILE"
fi

# 创建缓存目录
echo ""
echo "🗃️  设置缓存目录..."
CACHE_DIR="$HOME/.workbuddy/cache/memory_retriever"
if [ ! -d "$CACHE_DIR" ]; then
    mkdir -p "$CACHE_DIR"
    echo "   创建缓存目录: $CACHE_DIR"
else
    echo "   缓存目录已存在: $CACHE_DIR"
fi

# 运行测试
echo ""
echo "🧪 运行单元测试..."
cd "$SKILL_DIR"
if python3 -m pytest tests/test_basic.py -v; then
    echo "✅ 单元测试通过"
else
    echo "❌ 单元测试失败"
    echo "   跳过测试继续安装..."
fi

# 运行示例
echo ""
echo "📚 运行使用示例..."
if python3 examples/example_usage.py; then
    echo "✅ 示例运行成功"
else
    echo "❌ 示例运行失败"
    echo "   跳过示例继续安装..."
fi

# 测试启动脚本
echo ""
echo "🚀 测试启动脚本..."
if python3 start_work.py --status; then
    echo "✅ 启动脚本测试通过"
else
    echo "❌ 启动脚本测试失败"
fi

# 设置执行权限
echo ""
echo "🔧 设置执行权限..."
chmod +x "$SKILL_DIR/start_work.py"
chmod +x "$SKILL_DIR/examples/example_usage.py"
chmod +x "$SKILL_DIR/tests/test_basic.py"
echo "✅ 执行权限设置完成"

# 创建符号链接（可选）
echo ""
echo "🔗 创建全局访问链接（可选）..."
read -p "是否创建全局符号链接到 ~/.local/bin? (y/n): " create_link
if [[ "$create_link" =~ ^[Yy]$ ]]; then
    LINK_PATH="$HOME/.local/bin/workbuddy-memory"
    mkdir -p "$HOME/.local/bin"
    
    if [ -L "$LINK_PATH" ]; then
        rm "$LINK_PATH"
    fi
    
    ln -s "$SKILL_DIR/start_work.py" "$LINK_PATH"
    echo "✅ 符号链接已创建: $LINK_PATH -> $SKILL_DIR/start_work.py"
    echo "   现在可以通过 'workbuddy-memory' 命令使用"
fi

# 显示使用说明
echo ""
echo "=================================================="
echo "🎉 安装完成！"
echo "=================================================="
echo ""
echo "📖 使用说明:"
echo ""
echo "1. 开始新工作:"
echo "   python start_work.py \"任务描述\""
echo "   例如: python start_work.py \"制作Excel预算表\""
echo ""
echo "2. 交互式模式:"
echo "   python start_work.py --interactive"
echo ""
echo "3. 检查系统状态:"
echo "   python start_work.py --status"
echo ""
echo "4. 查看示例:"
echo "   python examples/example_usage.py"
echo ""
echo "5. 运行测试:"
echo "   python -m pytest tests/test_basic.py -v"
echo ""
echo "📁 重要目录:"
echo "   技能目录: $SKILL_DIR"
echo "   配置目录: $CONFIG_DIR"
echo "   缓存目录: $CACHE_DIR"
echo ""
echo "⚙️  配置说明:"
echo "   1. 编辑 $CONFIG_FILE 自定义配置"
echo "   2. 在 memory_sources 中添加您的记忆源路径"
echo "   3. 修改 retrieval_config 调整检索参数"
echo ""
echo "📞 支持:"
echo "   作者: zcg007"
echo "   版本: v3.0 (2026-03-15)"
echo "   如有问题，请检查日志文件: $SKILL_DIR/workbuddy_add_memory.log"
echo ""
echo "=================================================="
echo "祝您使用愉快！🎯"
echo "=================================================="