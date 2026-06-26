#!/bin/bash
# Self Evolution Pro - 自动技能提取脚本
# 从学习记录中提取技能并发布到 ClawHub
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

WORKSPACE="${HOME}/.openclaw/workspace"
LEARNINGS_DIR="${WORKSPACE}/.learnings"
SKILLS_DIR="${WORKSPACE}/.skills"
EVOLUTION_DIR="${WORKSPACE}/.evolution"

usage() {
    cat << EOF
用法: $(basename "$0") <技能名称> [选项]

从学习记录中提取技能并发布。

选项:
  --learning-id <ID>     指定学习记录ID (如 LRN-20250115-001)
  --dry-run              预览将要创建的内容
  --publish              创建后发布到 ClawHub
  --force                覆盖已存在的技能
  -h, --help             显示帮助

示例:
  $(basename "$0") docker-m1-fixes --learning-id LRN-20250115-001
  $(basename "$0") api-timeout --publish --force
  $(basename "$0") docker-platform-fix --dry-run

EOF
}

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# 参数解析
SKILL_NAME=""
LEARNING_ID=""
DRY_RUN=false
PUBLISH=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --learning-id) LEARNING_ID="$2"; shift 2 ;;
        --dry-run) DRY_RUN=true; shift ;;
        --publish) PUBLISH=true; shift ;;
        --force) FORCE=true; shift ;;
        -h|--help) usage; exit 0 ;;
        -*)
            log_error "未知选项: $1"
            usage; exit 1 ;;
        *)
            if [ -z "$SKILL_NAME" ]; then SKILL_NAME="$1"; shift
            else log_error "意外参数: $1"; usage; exit 1; fi ;;
    esac
done

if [ -z "$SKILL_NAME" ]; then
    log_error "技能名称是必需的"
    usage; exit 1
fi

# 验证名称格式
if ! [[ "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    log_error "技能名称格式无效，只允许小写字母、数字和连字符"
    exit 1
fi

SKILL_PATH="${SKILLS_DIR}/${SKILL_NAME}"

# 检查是否已存在
if [ -d "$SKILL_PATH" ] && [ "$FORCE" = false ] && [ "$DRY_RUN" = false ]; then
    log_error "技能已存在: $SKILL_PATH"
    log_info "使用 --force 覆盖或选择不同的名称"
    exit 1
fi

# 如果指定了学习ID，读取学习内容
LEARNING_CONTENT=""
if [ -n "$LEARNING_ID" ] && [ -f "${LEARNINGS_DIR}/LEARNINGS.md" ]; then
    LEARNING_CONTENT=$(grep -A 30 "## \[${LEARNING_ID}\]" "${LEARNINGS_DIR}/LEARNINGS.md" 2>/dev/null || echo "")
fi

# 计算技能标题 (如 docker-m1-fixes -> Docker M1 Fixes)
SKILL_TITLE=$(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

# 生成 SKILL.md 内容
SKILL_MD_CONTENT="---
name: \"${SKILL_NAME}\"
version: \"1.0.0\"
description: \"[TODO: 描述这个技能做什么，何时使用]"
---

# ${SKILL_TITLE}

[TODO: 简介，说明这个技能解决的问题]

## 快速参考

| 情况 | 操作 |
|------|------|
| [触发条件] | [做什么] |

## 问题描述

[TODO: 详细描述这个问题或场景]

## 解决方案

### 步骤

1. [第一步]
2. [第二步]
3. [验证]

### 代码示例

\`\`\`
[TODO: 示例代码]
\`\`\`

## 常见变体

- **变体A**: [描述和处理方式]
- **变体B**: [描述和处理方式]

## 陷阱

- ⚠️ [警告或常见错误 #1]
- ⚠️ [警告或常见错误 #2]

## 相关

- 相关文档或技能链接

## 来源

- 学习ID: ${LEARNING_ID:-未知}
- 提取日期: $(date +%Y-%m-%d)
"

if [ "$DRY_RUN" = true ]; then
    log_info "=== 预览模式 ==="
    echo "技能路径: ${SKILL_PATH}/"
    echo "将创建文件: SKILL.md"
    echo ""
    echo "=== SKILL.md 内容预览 ==="
    echo "${SKILL_MD_CONTENT}" | head -30
    echo "...(省略 ${#SKILL_MD_CONTENT} 字符)..."
    exit 0
fi

# 创建目录结构
log_step "创建技能目录"
mkdir -p "${SKILL_PATH}"

# 写入 SKILL.md
log_step "写入 SKILL.md"
cat > "${SKILL_PATH}/SKILL.md" << EOF
---
name: "${SKILL_NAME}"
version: "1.0.0"
description: "[TODO: 描述这个技能做什么，何时使用]"
---

# ${SKILL_TITLE}

[TODO: 简介，说明这个技能解决的问题]

## 快速参考

| 情况 | 操作 |
|------|------|
| [触发条件] | [做什么] |

## 问题描述

[TODO: 详细描述这个问题或场景]

## 解决方案

### 步骤

1. [第一步]
2. [第二步]
3. [验证]

### 代码示例

\`\`\`
[TODO: 示例代码]
\`\`\`

## 常见变体

- **变体A**: [描述和处理方式]
- **变体B**: [描述和处理方式]

## 陷阱

- ⚠️ [警告或常见错误 #1]
- ⚠️ [警告或常见错误 #2]

## 相关

- 相关文档或技能链接

## 来源

- 学习ID: ${LEARNING_ID:-手动提取}
- 提取日期: $(date +%Y-%m-%d)
EOF

log_info "创建: ${SKILL_PATH}/SKILL.md"

# 创建版本历史
log_step "更新版本历史"
mkdir -p "${EVOLUTION_DIR}"
EVOLUTION_FILE="${EVOLUTION_DIR}/version-history.md"
echo "" >> "${EVOLUTION_FILE}" 2>/dev/null || touch "${EVOLUTION_FILE}"
cat >> "${EVOLUTION_FILE}" << EOF

## ${SKILL_NAME} - $(date +%Y-%m-%d)

- 版本: 1.0.0
- 来源: ${LEARNING_ID:-手动提取}
- 发布: 否
EOF

# 更新知识图谱
if [ -f "${LEARNINGS_DIR}/KNOWLEDGE_GRAPH.md" ]; then
    log_step "更新知识图谱"
    # 添加节点引用（如果存在）
    if [ -n "$LEARNING_ID" ]; then
        sed -i '' "s/## 节点/## 节点\n| ${LEARNING_ID} | learning | ${SKILL_TITLE} | skill:${SKILL_NAME} |/" "${LEARNINGS_DIR}/KNOWLEDGE_GRAPH.md" 2>/dev/null || true
    fi
fi

log_info "=== 技能提取完成 ==="
echo ""
echo "接下来:"
echo "  1. 编辑 ${SKILL_PATH}/SKILL.md 填入实际内容"
echo "  2. 测试: 阅读技能确保完整"
echo "  3. 发布: clawhub publish ${SKILL_NAME}"
echo "  4. 标记学习: 设置状态为 promoted_to_skill"

if [ "$PUBLISH" = true ]; then
    log_step "发布到 ClawHub"
    cd "${WORKSPACE}" && clawhub publish ".skills/${SKILL_NAME}" --version 1.0.0 2>&1
fi
