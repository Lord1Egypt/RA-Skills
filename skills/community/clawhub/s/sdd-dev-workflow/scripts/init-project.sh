#!/bin/bash
# SDD 开发工作流 - 项目初始化脚本
# 快速创建新项目并应用公共宪法模板

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONSTITUTION_DEFAULT="enterprise"
CONSTITUTION_DIR="$SKILL_DIR/templates"

# 🆕 标准项目路径
WORKSPACE_ROOT="$HOME/openclaw/workspace"
PROJECTS_DIR="$WORKSPACE_ROOT/projects"

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_help() {
    cat << EOF
SDD 开发工作流 - 项目初始化脚本

用法: $0 <项目名称> [选项]

选项:
  -c, --constitution <名称>   指定宪法模板（默认: enterprise）
                              可选: enterprise, lite
  -d, --dir <目录>            指定创建目录（默认: ~/openclaw/workspace/projects/）
  --tmp                       创建临时项目（创建于 tmp/ 目录）
  --no-git                    不初始化 Git 仓库
  --no-speckit                不初始化 Speckit
  -h, --help                  显示帮助

宪法模板:
  enterprise   完整的企业级宪法（推荐）
  lite         基础精简宪法

项目类型:
  正式项目     创建于 projects/ 目录（长期维护）
  临时项目     创建于 tmp/ 目录（验证、测试，可随时清理）

标准路径规范:
  所有项目必须在 projects/ 或 tmp/ 目录下创建
  
示例:
  $0 my-project                    # 正式项目: projects/my-project/
  $0 test-xyz --tmp                # 临时项目: tmp/test-xyz/
  $0 my-project --constitution=lite
  $0 my-project -d /tmp/test       # 自定义目录（不推荐）

宪法模板位置:
  $CONSTITUTION_DIR
EOF
}

# 解析参数
PROJECT_NAME=""
TARGET_DIR=""  # 留空表示使用默认路径
CONSTITUTION="$CONSTITUTION_DEFAULT"
INIT_GIT=true
INIT_SPECKIT=true
IS_TMP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--constitution)
            CONSTITUTION="$2"
            shift 2
            ;;
        -d|--dir)
            TARGET_DIR="$2"
            shift 2
            ;;
        --tmp)
            IS_TMP=true
            shift
            ;;
        --no-git)
            INIT_GIT=false
            shift
            ;;
        --no-speckit)
            INIT_SPECKIT=false
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            log_error "未知选项: $1"
            show_help
            exit 1
            ;;
        *)
            if [ -z "$PROJECT_NAME" ]; then
                PROJECT_NAME="$1"
            fi
            shift
            ;;
    esac
done

# 验证项目名称
if [ -z "$PROJECT_NAME" ]; then
    log_error "请指定项目名称"
    show_help
    exit 1
fi

# 🆕 设置默认路径
if [ -z "$TARGET_DIR" ]; then
    if [ "$IS_TMP" = true ]; then
        TARGET_DIR="$WORKSPACE_ROOT/tmp"
        log_info "临时项目路径: $TARGET_DIR"
    else
        TARGET_DIR="$PROJECTS_DIR"
        log_info "正式项目路径: $TARGET_DIR"
    fi
fi

# 🆕 路径规范检查
if [[ "$TARGET_DIR" != *"/projects"* ]] && [[ "$TARGET_DIR" != *"/tmp"* ]] && [[ "$TARGET_DIR" != "/tmp"* ]]; then
    log_warn "⚠️  项目不在标准路径下"
    log_warn "   正式项目: $PROJECTS_DIR"
    log_warn "   临时项目: $WORKSPACE_ROOT/tmp"
    log_warn "   当前路径: $TARGET_DIR"
    echo ""
    read -p "继续在非标准路径创建？[y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "已取消"
        exit 0
    fi
fi

# 确定宪法模板文件
case "$CONSTITUTION" in
    enterprise|full)
        CONSTITUTION_FILE="$CONSTITUTION_DIR/constitution-enterprise.md"
        ;;
    lite|basic|simple)
        CONSTITUTION_FILE="$CONSTITUTION_DIR/constitution-lite.md"
        ;;
    *)
        # 检查是否是文件路径
        if [ -f "$CONSTITUTION" ]; then
            CONSTITUTION_FILE="$CONSTITUTION"
        else
            log_error "未找到宪法模板: $CONSTITUTION"
            echo "可用模板: enterprise, lite"
            exit 1
        fi
        ;;
esac

PROJECT_DIR="$TARGET_DIR/$PROJECT_NAME"

log_info "创建项目: $PROJECT_NAME"
log_info "宪法模板: $CONSTITUTION"
echo ""

# 检查目录是否已存在
if [ -d "$PROJECT_DIR" ]; then
    log_error "目录已存在: $PROJECT_DIR"
    exit 1
fi

# 创建项目目录
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
log_info "项目目录: $PROJECT_DIR"

# 初始化 Git
if [ "$INIT_GIT" = true ]; then
    log_info "初始化 Git 仓库..."
    git init
    echo ""
fi

# 初始化 Speckit
if [ "$INIT_SPECKIT" = true ]; then
    log_info "初始化 Speckit..."
    if command -v specify &> /dev/null; then
        # 使用 --here --force 跳过交互式确认
        # 使用 --ai claude 指定 AI 助手
        # 使用 --no-git 避免重复初始化 Git
        log_info "下载 Speckit 模板（从 GitHub，可能需要几秒）..."
        
        # 使用 timeout 命令限制等待时间（90秒），避免网络卡死
        if timeout 90 specify init . --here --force --ai claude --no-git 2>&1; then
            log_info "Speckit 初始化成功"
        else
            EXIT_CODE=$?
            if [ $EXIT_CODE -eq 124 ]; then
                log_warn "Speckit 初始化超时（90秒），可能网络问题"
            else
                log_warn "Speckit 初始化失败（退出码: $EXIT_CODE）"
            fi
            # 创建基本的 Speckit 目录结构作为降级方案
            log_info "使用降级方案：手动创建 Speckit 目录结构"
            mkdir -p .specify/memory .specify/templates .specify/scripts
            mkdir -p specs
            log_info "已创建基本 Speckit 目录结构"
        fi
    else
        log_warn "specify-cli 未安装，跳过 Speckit 初始化"
        log_warn "安装命令: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
        # 创建基本的 Speckit 目录结构
        mkdir -p .specify/memory .specify/templates .specify/scripts
        mkdir -p specs
    fi
    echo ""
fi

# 复制宪法模板
log_info "应用宪法模板..."
mkdir -p .specify/memory
cp "$CONSTITUTION_FILE" .specify/memory/constitution.md
log_info "宪法已复制到: .specify/memory/constitution.md"
echo ""

# 创建基本目录结构
log_info "创建目录结构..."
mkdir -p specs docs tests src
log_info "已创建: specs/, docs/, tests/, src/"
echo ""

# 创建 README
if [ ! -f README.md ]; then
    cat > README.md << EOF
# $PROJECT_NAME

## 项目说明

TODO: 添加项目说明

## 开发指南

本项目遵循 SDD（规范驱动开发）工作流，请阅读 \`.specify/memory/constitution.md\` 了解工程原则。

## 快速开始

\`\`\`bash
# 安装依赖
# TODO

# 运行测试
# TODO

# 启动服务
# TODO
\`\`\`

## 文档

- [项目宪法](.specify/memory/constitution.md)
- [API 文档](docs/api-documentation.md)
EOF
    log_info "已创建: README.md"
fi

# 创建 .gitignore
if [ ! -f .gitignore ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

# Node
node_modules/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local

# Build
dist/
build/

# Test
.pytest_cache/
.coverage
htmlcov/

# Temp
*.tmp
*.temp
temp-*
tmp-*
EOF
    log_info "已创建: .gitignore"
fi

# 🆕 自动创建长时间运行任务上下文（透明化，所有项目默认支持断点续传）
log_info "创建任务上下文（断点续传支持）..."
mkdir -p .task-context

cat > .task-context/progress.json << EOF
{
  "projectId": "$PROJECT_NAME",
  "projectName": "$PROJECT_NAME",
  "status": "pending",
  "currentPhase": "constitution",
  "phases": {},
  "currentTask": {},
  "artifacts": {},
  "startTime": "$(date -Iseconds)",
  "lastUpdate": "$(date -Iseconds)",
  "checkpoints": []
}
EOF

cat > .task-context/checkpoint.md << 'EOF'
# 检查点

## 📍 当前位置
- 阶段：初始化
- 状态：待开始

## ✅ 已完成
（无）

## 🔄 进行中
（无）

## 📋 待办
（待 tasks.md 生成后填写）

## 🚨 遇到的问题
（无）

## 🤔 需要的决策
（无）

## 💡 下次恢复指令
```
开始执行 SDD 工作流
/speckit.constitution 创建项目宪法
```
EOF

cat > .task-context/session-log.md << EOF
# 会话日志

## $(date '+%Y-%m-%d %H:%M') - 初始化
- 项目初始化完成
- 支持长时间运行（断点续传）

EOF

log_info "已创建: .task-context/"
echo ""

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  项目初始化完成！${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "项目位置: $PROJECT_DIR"
echo "宪法模板: $CONSTITUTION_FILE"
echo ""
echo "下一步:"
echo "  1. cd $PROJECT_DIR"
echo "  2. 阅读 .specify/memory/constitution.md 了解工程原则"
echo "  3. 开始 Speckit 工作流:"
echo "     /speckit.specify [功能描述]"
echo ""
echo ""
