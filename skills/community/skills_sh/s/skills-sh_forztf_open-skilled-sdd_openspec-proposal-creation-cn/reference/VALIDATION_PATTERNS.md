# 验证模式

使用 grep 与 bash 的模式，在不依赖外部 CLI 工具的情况下验证提案结构。

## 目录
- 目录结构验证
- 提案文件验证
- 规范差异验证
- 需求格式验证
- 常用验证工作流

## 目录结构验证

### 检查变更目录是否存在

```bash
# 验证变更目录是否已创建
test -d spec/changes/{change-id} && echo "✓ 目录存在" || echo "✗ 目录缺失"
```

### 列出所有变更

```bash
# 显示所有进行中的变更
ls -1 spec/changes/ | grep -v "archive"
```

### 检查是否有冲突

```bash
# 搜索相似的变更 ID
ls spec/changes/ | grep -i "{search-term}"
```

## 提案文件验证

### 检查必需章节

```bash
# 验证 proposal.md 是否包含必需章节
grep -c "## Why" spec/changes/{change-id}/proposal.md
grep -c "## What Changes" spec/changes/{change-id}/proposal.md
grep -c "## Impact" spec/changes/{change-id}/proposal.md
```

**预期**：每个 grep 返回 1（如果有子章节则可能大于 1）

### 验证任务文件

```bash
# 统计任务数量
grep -c '"task":' spec/changes/{change-id}/tasks.json

# 显示任务列表
grep '"task":' spec/changes/{change-id}/tasks.json
```

**预期**：通常为 5-15 个任务

## 规范差异验证

### 检查差异操作是否存在

```bash
# 统计差异操作标题数量
grep -c "## ADDED\|MODIFIED\|REMOVED" spec/changes/{change-id}/specs/**/*.md
```

**预期**：至少 1 个匹配

### 列出差异操作

```bash
# 以行号显示所有差异操作
grep -n "## ADDED\|MODIFIED\|REMOVED" spec/changes/{change-id}/specs/**/*.md
```

**示例输出**：
```
spec/changes/add-auth/specs/authentication/spec-delta.md:3:## ADDED Requirements
spec/changes/add-auth/specs/authentication/spec-delta.md:45:## MODIFIED Requirements
```

### 验证各部分是否有内容

```bash
# 检查 ADDED 部分是否包含需求
awk '/## ADDED/,/^## [A-Z]/ {if (/### Requirement:/) count++} END {print count}' \
    spec/changes/{change-id}/specs/**/*.md
```

## 需求格式验证

### 检查需求标题

```bash
# 列出所有需求标题
grep -n "### Requirement:" spec/changes/{change-id}/specs/**/*.md
```

**期望格式**：`### Requirement: 描述性名称`

### 验证场景格式

```bash
# 检查场景（必须使用四个井号）
grep -n "#### Scenario:" spec/changes/{change-id}/specs/**/*.md
```

**期望格式**：`#### Scenario: 描述性名称`

### 统计需求与场景数量

```bash
# 统计需求数量
REQS=$(grep -c "### Requirement:" spec/changes/{change-id}/specs/**/*.md)

# 统计场景数量
SCENARIOS=$(grep -c "#### Scenario:" spec/changes/{change-id}/specs/**/*.md)

echo "需求数：$REQS"
echo "场景数：$SCENARIOS"
echo "比率：$(echo "scale=1; $SCENARIOS/$REQS" | bc)"
```

**预期**：比率 >= 2.0（每个需求至少 2 个场景）

### 检查 SHALL 关键字

```bash
# 验证需求中是否使用 SHALL（具约束性的要求指示）
grep -c "SHALL" spec/changes/{change-id}/specs/**/*.md
```

**预期**：SHALL 的数量至少与需求数量相当

## 完整验证工作流

### 预提交验证脚本

```bash
#!/bin/bash
# 验证变更提案结构

CHANGE_ID="$1"
BASE_PATH="spec/changes/$CHANGE_ID"

echo "正在验证提案：$CHANGE_ID"
echo "================================"

# 1. 目录存在
if [ ! -d "$BASE_PATH" ]; then
    echo "✗ 变更目录未找到"
    exit 1
fi
echo "✓ 变更目录存在"

# 2. 必需文件存在
for file in proposal.md tasks.json; do
    if [ ! -f "$BASE_PATH/$file" ]; then
        echo "✗ 缺少 $file"
        exit 1
    fi
    echo "✓ 找到 $file"
done

# 3. 提案包含必需章节
for section in "## Why" "## What Changes" "## Impact"; do
    if ! grep -q "$section" "$BASE_PATH/proposal.md"; then
        echo "✗ proposal.md 缺少章节：$section"
        exit 1
    fi
done
echo "✓ proposal.md 包含所需章节"

# 4. 任务文件包含 'task' 键
TASK_COUNT=$(grep -c '"task":' "$BASE_PATH/tasks.json" || echo "0")
if [ "$TASK_COUNT" -lt 3 ]; then
    echo "✗ tasks.json 任务数量不足（$TASK_COUNT）"
    exit 1
fi
echo "✓ 找到 $TASK_COUNT 个任务"

# 5. 存在规范差异文件
DELTA_COUNT=$(find "$BASE_PATH/specs" -name "*.md" 2>/dev/null | wc -l)
if [ "$DELTA_COUNT" -eq 0 ]; then
    echo "✗ 未找到规范差异文件"
    exit 1
fi
echo "✓ 找到 $DELTA_COUNT 个规范差异文件"

# 6. 存在差异操作
OPERATIONS=$(grep -h "## ADDED\|MODIFIED\|REMOVED" "$BASE_PATH/specs"/**/*.md 2>/dev/null | wc -l)
if [ "$OPERATIONS" -eq 0 ]; then
    echo "✗ 未发现差异操作"
    exit 1
fi
echo "✓ 找到 $OPERATIONS 个差异操作"

# 7. 需求具备场景
REQ_COUNT=$(grep -h "### Requirement:" "$BASE_PATH/specs"/**/*.md 2>/dev/null | wc -l)
SCENARIO_COUNT=$(grep -h "#### Scenario:" "$BASE_PATH/specs"/**/*.md 2>/dev/null | wc -l)

if [ "$REQ_COUNT" -eq 0 ]; then
    echo "✗ 未找到任何需求"
    exit 1
fi

if [ "$SCENARIO_COUNT" -lt "$REQ_COUNT" ]; then
    echo "⚠ 警告：场景数（$SCENARIO_COUNT）少于需求数（$REQ_COUNT）"
    echo "  建议：每个需求至少包含 2 个场景"
else
    echo "✓ 找到 $REQ_COUNT 个需求，包含 $SCENARIO_COUNT 个场景"
fi

echo "================================"
echo "✓ 验证通过"
```

**用法**：
```bash
bash validate-proposal.sh add-user-auth
```

## 常见问题与修复

### 问题：缺少场景

**检测**：
```bash
# 查找没有场景的需求
awk '/### Requirement:/ {req=$0; getline; if ($0 !~ /#### Scenario:/) print req}' \
    spec/changes/{change-id}/specs/**/*.md
```

**修复**：为每个需求添加场景

### 问题：场景标题层级错误

**检测**：
```bash
# 查找场景标题井号数量错误（不完全等于 4）
grep -n "^###\? Scenario:\|^#####+ Scenario:" spec/changes/{change-id}/specs/**/*.md
```

**修复**：场景必须使用恰好 4 个井号：`#### Scenario:`

### 问题：缺少差异操作

**检测**：
```bash
# 检查文件存在需求但无差异操作头
for file in spec/changes/{change-id}/specs/**/*.md; do
    if grep -q "### Requirement:" "$file" && \
       ! grep -q "## ADDED\|MODIFIED\|REMOVED" "$file"; then
        echo "缺少差异操作：$file"
    fi
done
```

**修复**：添加适当的差异操作标题（ADDED/MODIFIED/REMOVED）

## 快速验证命令

### 一行命令：完整结构检查

```bash
# 快速验证变更结构
CHANGE_ID="add-user-auth" && \
test -f spec/changes/$CHANGE_ID/proposal.md && \
test -f spec/changes/$CHANGE_ID/tasks.json && \
grep -q "## ADDED\|MODIFIED\|REMOVED" spec/changes/$CHANGE_ID/specs/**/*.md && \
grep -q "### Requirement:" spec/changes/$CHANGE_ID/specs/**/*.md && \
grep -q "#### Scenario:" spec/changes/$CHANGE_ID/specs/**/*.md && \
echo "✓ 所有验证通过" || echo "✗ 验证失败"
```

### 显示提案摘要

```bash
# 展示提案概览
CHANGE_ID="add-user-auth"
echo "提案：$CHANGE_ID"
echo "文件数：$(find spec/changes/$CHANGE_ID -type f | wc -l)"
echo "任务数：$(grep -c '\"task\":' spec/changes/$CHANGE_ID/tasks.json)"
echo "需求数：$(grep -h \"### Requirement:\" spec/changes/$CHANGE_ID/specs/**/*.md | wc -l)"
echo "场景数：$(grep -h \"#### Scenario:\" spec/changes/$CHANGE_ID/specs/**/*.md | wc -l)"
```

## 验证清单

在面向用户展示提案之前：

```markdown
手动检查：
- [ ] 变更 ID 描述性且唯一
- [ ] proposal.md 的 Why 部分解释问题
- [ ] proposal.md 的 What 部分列出具体变更
- [ ] proposal.md 的 Impact 部分标识受影响区域
- [ ] tasks.json 含 5-15 个具体、可测试的任务
- [ ] 任务按依赖顺序排列

自动检查：
- [ ] 目录结构存在
- [ ] 必需文件存在（proposal.md、tasks.json、spec-delta.md）
- [ ] 差异操作存在（ADDED/MODIFIED/REMOVED）
- [ ] 需求遵循格式：`### Requirement: 名称`
- [ ] 场景遵循格式：`#### Scenario: 名称`
- [ ] 每个需求至少包含 2 个场景
- [ ] 需求使用 SHALL 关键字
```

运行所有自动检查：
```bash
# 执行验证脚本
bash validate-proposal.sh {change-id}
```
