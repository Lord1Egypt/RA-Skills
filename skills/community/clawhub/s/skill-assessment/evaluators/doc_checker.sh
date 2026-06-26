#!/bin/bash
# 文档完整性检查器

set -euo pipefail

SKILL_PATH="$1"
SKILL_MD="${SKILL_PATH}/SKILL.md"

# 初始化结果
declare -A result
result["score"]=0
result["max_score"]=5
result["issues"]="[]"
result["suggestions"]="[]"

issues=()
suggestions=()

# 检查 SKILL.md 是否存在
if [ ! -f "$SKILL_MD" ]; then
    issues+=("缺少 SKILL.md 文件")
    echo '{"score": 0, "max_score": 5, "issues": ["缺少 SKILL.md 文件"], "suggestions": ["创建 SKILL.md 文件，包含技能名称、描述、使用示例等"]}'
    exit 0
fi

# 基础分：有 SKILL.md 得 1分
base_score=1

# 检查必填章节
required_sections=("name" "description" "triggers" "usage" "installation" "configuration")
section_score=0
max_section_score=${#required_sections[@]}

for section in "${required_sections[@]}"; do
    if grep -i "^\s*#.*${section}" "$SKILL_MD" > /dev/null || \
       grep -i "^\s*##.*${section}" "$SKILL_MD" > /dev/null || \
       grep -i "^\s*###.*${section}" "$SKILL_MD" > /dev/null; then
        section_score=$((section_score + 1))
    else
        issues+=("缺少 '${section}' 章节")
        suggestions+=("在 SKILL.md 中添加 '${section}' 章节")
    fi
done

# 章节得分（占3分）
section_normalized=$((section_score * 3 / max_section_score))

# 检查示例质量
example_score=0
if grep -i "```bash" "$SKILL_MD" > /dev/null || \
   grep -i "```shell" "$SKILL_MD" > /dev/null; then
    example_score=1
    # 检查是否有输入输出说明
    if grep -i "输入\|input\|参数\|argument" "$SKILL_MD" > /dev/null && \
       grep -i "输出\|output\|结果\|result" "$SKILL_MD" > /dev/null; then
        example_score=2
    else
        suggestions+=("为示例添加输入输出说明")
    fi
else
    issues+=("缺少代码示例")
    suggestions+=("添加 ```bash ... ``` 格式的使用示例")
fi

# 检查配置说明
config_score=0
if grep -i "配置\|configuration\|config" "$SKILL_MD" > /dev/null; then
    config_score=1
    if grep -i "环境变量\|environment variable" "$SKILL_MD" > /dev/null || \
       grep -i "export.*=" "$SKILL_MD" > /dev/null; then
        config_score=2
    else
        suggestions+=("添加环境变量配置说明")
    fi
else
    issues+=("缺少配置说明")
    suggestions+=("添加配置选项说明")
fi

# 计算总分（满分5分）
total_score=$((base_score + section_normalized + example_score + config_score))
if [ $total_score -gt 5 ]; then
    total_score=5
fi

# 转换 issues 和 suggestions 为 JSON 数组
json_issues=$(printf '%s\n' "${issues[@]}" | jq -R . | jq -s .)
json_suggestions=$(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .)

# 输出结果
echo "{\"score\": $total_score, \"max_score\": 5, \"issues\": $json_issues, \"suggestions\": $json_suggestions}"