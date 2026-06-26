#!/bin/bash
# tests/validate_skill.sh
# 用法: bash tests/validate_skill.sh [SKILL.md路径]
# 验证 SKILL.md 是否符合 ClawHub 规范

set -euo pipefail

SKILL_FILE="${1:-}"
if [[ -z "$SKILL_FILE" ]]; then
    echo "❌ 验证失败：未指定 SKILL.md 路径"
    echo "用法: bash $0 [SKILL.md路径]"
    exit 1
fi

if [[ ! -f "$SKILL_FILE" ]]; then
    echo "❌ 验证失败：文件不存在 ($SKILL_FILE)"
    exit 1
fi

# 读取文件内容
content=$(cat "$SKILL_FILE")
first_line=$(echo "$content" | head -n 1)

# ─── 1. frontmatter 存在性 ───

# 文件第一行必须是 ---
if [[ "$first_line" != "---" ]]; then
    echo "❌ 验证失败：文件第一行不是 '---'（实际内容: '$first_line'）"
    exit 1
fi

# 查找第二个 ---
# frontmatter 格式要求：第一行 ---，之后若干行，再一行 ---
# 找到第二个 --- 的行号
second_delim_line=$(echo "$content" | awk 'NR>1 && $0=="---" {print NR; exit}')

if [[ -z "$second_delim_line" ]]; then
    echo "❌ 验证失败：缺少结束的 '---'（frontmatter 未正确关闭）"
    exit 1
fi

if [[ "$second_delim_line" -lt 2 ]]; then
    echo "❌ 验证失败：frontmatter 为空（第二行就是 '---'）"
    exit 1
fi

# frontmatter 必须在文件最开头 — 已通过检查第一行是 --- 保证

# 提取 frontmatter 内容（第一行 --- 到第二行 --- 之间）
frontmatter=$(echo "$content" | sed -n "2,$((second_delim_line - 1))p")

# ─── 2. name 字段 ───

name_line=$(echo "$frontmatter" | grep -E '^[[:space:]]*name:' || true)

if [[ -z "$name_line" ]]; then
    echo "❌ 验证失败：frontmatter 中缺少 'name:' 字段"
    exit 1
fi

# 提取 name 值（去掉 "name:" 前缀和前后空白/引号）
name_value=$(echo "$name_line" | sed 's/^[[:space:]]*name:[[:space:]]*//' | sed 's/^["'\''"]//;s/["'\''"]$//' | tr -d '[:space:]')

if [[ -z "$name_value" ]]; then
    echo "❌ 验证失败：name 字段值为空"
    exit 1
fi

# 蛇形命名检查：只允许小写字母、数字、下划线，且以字母开头
if ! echo "$name_value" | grep -qE '^[a-z][a-z0-9_]*$'; then
    echo "❌ 验证失败：name '$name_value' 不符合蛇形命名（需小写+下划线，如 personal_ledger）"
    exit 1
fi

# ─── 3. description 字段 ───

desc_line=$(echo "$frontmatter" | grep -E '^[[:space:]]*description:' || true)

if [[ -z "$desc_line" ]]; then
    echo "❌ 验证失败：frontmatter 中缺少 'description:' 字段"
    exit 1
fi

# 提取 description 值
desc_value=$(echo "$desc_line" | sed 's/^[[:space:]]*description:[[:space:]]*//' | sed 's/^["'\''"]//;s/["'\''"]$//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

if [[ -z "$desc_value" ]]; then
    echo "❌ 验证失败：description 字段值为空"
    exit 1
fi

# ─── 4. metadata 格式 ───

meta_line=$(echo "$frontmatter" | grep -E '^[[:space:]]*metadata:' || true)

if [[ -n "$meta_line" ]]; then
    meta_value=$(echo "$meta_line" | sed 's/^[[:space:]]*metadata:[[:space:]]*//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    if [[ -z "$meta_value" ]]; then
        echo "❌ 验证失败：metadata 字段值为空"
        exit 1
    fi

    # 检查是否包含 { （单行 JSON 格式）
    if echo "$meta_value" | grep -q '{'; then
        # 单行 JSON — 检查是否是有效的 JSON
        if ! echo "$meta_value" | python3 -c "import sys,json; json.loads(sys.stdin.read())" 2>/dev/null; then
            echo "❌ 验证失败：metadata 不是合法的 JSON"
            exit 1
        fi
    else
        # 检查是否是多行 YAML 字典（错误格式）
        # 检查 metadata 下一行是否有缩进内容
        meta_line_num=$(echo "$frontmatter" | grep -n '^[[:space:]]*metadata:' | head -1 | cut -d: -f1)
        meta_next_line=$(echo "$frontmatter" | sed -n "$((meta_line_num + 1))p" || true)

        if [[ -n "$meta_next_line" ]] && echo "$meta_next_line" | grep -qE '^[[:space:]]+'; then
            # 下一行有缩进 → 多行 YAML 字典
            echo "❌ 验证失败：metadata 使用了多行 YAML 字典格式，请使用单行 JSON 格式"
            exit 1
        fi

        # 既不是 JSON 也不是多行 YAML → 可能是简单值（如字符串），允许通过
        # 或者是空值（已在上面检查过）
    fi
fi

# ─── 5. 完整性检查 ───

# frontmatter 必须在前几行就结束（不超过第 20 行）
if [[ "$second_delim_line" -gt 20 ]]; then
    echo "❌ 验证失败：frontmatter 过长（结束于第 $second_delim_line 行，建议不超过 20 行）"
    exit 1
fi

# frontmatter 之后的正文中不应再出现孤立的 ---
body=$(echo "$content" | tail -n +"$((second_delim_line + 1))")
# 允许正文中出现 --- 作为分隔符，但检查是否有多余的 --- 对（可能是嵌套 frontmatter）
# 这里只做一个基本检查：确保第二个 --- 之后有实际内容
body_nonempty=$(echo "$body" | grep -v '^[[:space:]]*$' | head -1 || true)

if [[ -z "$body_nonempty" ]]; then
    echo "❌ 验证失败：frontmatter 之后没有正文内容"
    exit 1
fi

# ─── 全部通过 ───
echo "✅ SKILL.md 格式验证通过"
echo "  name: $name_value"
echo "  description: $(echo "$desc_value" | head -c 80)..."
exit 0
