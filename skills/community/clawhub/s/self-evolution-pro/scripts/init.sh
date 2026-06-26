#!/bin/bash
# Self Evolution Pro - 初始化脚本
# 创建所需目录结构

WORKSPACE="${HOME}/.openclaw/workspace"

echo "初始化 Self Evolution Pro..."
echo ""

mkdir -p "${WORKSPACE}/.learnings"
mkdir -p "${WORKSPACE}/.skills"
mkdir -p "${WORKSPACE}/.evolution"

# 初始化 LEARNINGS.md
if [ ! -f "${WORKSPACE}/.learnings/LEARNINGS.md" ]; then
    cat > "${WORKSPACE}/.learnings/LEARNINGS.md" << 'EOF'
# 学习记录

记录在会话中发现的重要学习、纠正和最佳实践。

## 格式

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601
**Priority**: low | medium | high | critical
**Status**: pending | resolved | promoted | promoted_to_skill
**Area**: frontend | backend | infra | tests | docs | config
**Recurrence-Count**: 1

### Summary
### Details
### Suggested Action
### Metadata
```

## 使用说明

当发现重要的学习、纠正或最佳实践时，使用上述格式添加到本文
```
fi
echo "✓ LEARNINGS.md"

# 初始化 ERRORS.md
if [ ! -f "${WORKSPACE}/.learnings/ERRORS.md" ]; then
    cat > "${WORKSPACE}/.learnings/ERRORS.md" << 'EOF'
# 错误记录

记录命令失败、异常和意外行为。

## 格式

```markdown
## [ERR-YYYYMMDD-XXX] name

**Logged**: ISO-8601
**Priority**: high | critical
**Status**: pending | resolved
**Area**: ...

### Summary
### Error
### Context
### Suggested Fix
```
EOF
echo "✓ ERRORS.md"

# 初始化 FEATURE_REQUESTS.md
if [ ! -f "${WORKSPACE}/.learnings/FEATURE_REQUESTS.md" ]; then
    cat > "${WORKSPACE}/.learnings/FEATURE_REQUESTS.md" << 'EOF'
# 功能请求

记录用户请求的功能或能力。

## 格式

```markdown
## [FEAT-YYYYMMDD-XXX] name

**Logged**: ISO-8601
**Priority**: medium
**Status**: pending | resolved
**Area**: ...

### Requested Capability
### Complexity Estimate
```
EOF
echo "✓ FEATURE_REQUESTS.md"

# 初始化 KNOWLEDGE_GRAPH.md
if [ ! -f "${WORKSPACE}/.learnings/KNOWLEDGE_GRAPH.md" ]; then
    cat > "${WORKSPACE}/.learnings/KNOWLEDGE_GRAPH.md" << 'EOF'
# 知识图谱

链接相关的学习、错误和技能。

## 节点

| ID | 类型 | 标题 | 关联 |
|----|------|------|------|
| N001 | learning | [标题] | N002 |
| N002 | error | [标题] | N001, skill:docker-fixes |

## 关系

- N001 → related_to → N002
- N002 → solved_by → skill:docker-fixes

## 说明

节点ID格式: N + 3位数字 (如 N001)
类型: learning | error | skill | concept
关联格式: NXXX | skill:skill-name | concept:name
EOF
echo "✓ KNOWLEDGE_GRAPH.md"

# 初始化进化目录
if [ ! -f "${WORKSPACE}/.evolution/metrics.md" ]; then
    cat > "${WORKSPACE}/.evolution/metrics.md" << 'EOF'
# 进化指标

追踪学习记录的效果和价值。

## 统计

| 日期 | 新增 | 已解决 | 已晋级 | 技能提取 |
|------|------|--------|--------|----------|
| YYYY-MM-DD | 0 | 0 | 0 | 0 |

## 效果追踪

| 学习 | 首次出现 | 复发次数 | 节省估计 |
|------|----------|----------|----------|
| [标题] | YYYY-MM-DD | 0 | 0分钟 |
EOF
echo "✓ metrics.md"

if [ ! -f "${WORKSPACE}/.evolution/version-history.md" ]; then
    cat > "${WORKSPACE}/.evolution/version-history.md" << 'EOF'
# 版本历史

记录技能提取和晋级的历史。

## 技能提取记录

| 技能 | 版本 | 来源 | 日期 | 已发布 |
|------|------|------|------|--------|
| skill-name | 1.0.0 | LRN-YYYYMMDD-XXX | YYYY-MM-DD | 是/否 |

## 晋级记录

| 学习ID | 晋级到 | 日期 |
|--------|---------|------|
| LRN-YYYYMMDD-XXX | SOUL.md | YYYY-MM-DD |
EOF
echo "✓ version-history.md"

if [ ! -f "${WORKSPACE}/.evolution/review-schedule.md" ]; then
    cat > "${WORKSPACE}/.evolution/review-schedule.md" << 'EOF'
# 审查计划

## 每日 (Heartbeat)
- 检查高优先级待处理项
- 检查新复发的模式

## 每周
- 完整审查所有pending项
- 识别可晋级项
- 更新知识图谱

## 每月
- 技能版本更新
- 效果指标复盘
- 清理过时项
EOF
echo "✓ review-schedule.md"

echo ""
echo "初始化完成！"
echo ""
echo "目录结构:"
echo "  ~/.openclaw/workspace/"
echo "    ├── .learnings/"
echo "    │   ├── LEARNINGS.md"
echo "    │   ├── ERRORS.md"
echo "    │   ├── FEATURE_REQUESTS.md"
echo "    │   └── KNOWLEDGE_GRAPH.md"
echo "    ├── .skills/"
echo "    └── .evolution/"
echo "        ├── metrics.md"
echo "        ├── version-history.md"
echo "        └── review-schedule.md"
