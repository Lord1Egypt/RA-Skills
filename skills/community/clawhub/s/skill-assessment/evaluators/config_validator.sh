#!/bin/bash
# 配置友好度检查器

set -euo pipefail

SKILL_PATH="$1"

# 初始化结果
issues=()
suggestions=()
base_score=3  # 基础分

# 检查配置文件
check_config_files() {
    local config_score=0
    
    # 检查是否有配置文件示例
    if find "$SKILL_PATH" -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" -o -name "*.ini" \) \
       ! -path "*/node_modules/*" ! -path "*/.git/*" \
       -name "*example*" -o -name "*sample*" -o -name "*config*" | grep -q .; then
        config_score=$((config_score + 2))
    else
        issues+=("缺少配置文件示例")
        suggestions+=("创建 config.example.yaml 或类似文件")
    fi
    
    # 检查是否有默认配置
    if find "$SKILL_PATH" -type f \( -name "config.yaml" -o -name "config.yml" -o -name "config.json" \) \
       ! -path "*/node_modules/*" ! -path "*/.git/*" | grep -q .; then
        config_score=$((config_score + 1))
    fi
    
    return $config_score
}

# 检查环境变量支持
check_env_support() {
    local env_score=0
    
    # 检查 SKILL.md 中是否提到环境变量
    if [ -f "${SKILL_PATH}/SKILL.md" ]; then
        if grep -i "环境变量\|environment variable\|export.*=" "${SKILL_PATH}/SKILL.md" > /dev/null; then
            env_score=$((env_score + 2))
        else
            issues+=("未提及环境变量支持")
            suggestions+=("在文档中添加环境变量配置说明")
        fi
    fi
    
    # 检查代码中是否使用环境变量
    if find "$SKILL_PATH" -type f \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) \
       ! -path "*/node_modules/*" ! -path "*/.git/*" \
       -exec grep -l "\\\$\\{.*\\}\|process\.env\|os\.environ\|getenv" {} \; 2>/dev/null | grep -q .; then
        env_score=$((env_score + 1))
    fi
    
    return $env_score
}

# 检查错误提示
check_error_messages() {
    local error_score=0
    
    # 检查是否有配置验证
    if find "$SKILL_PATH" -type f -name "*.sh" \
       -exec grep -l "if.*-z.*\\$.*CONFIG\|if.*!.*-f.*\\$.*FILE" {} \; 2>/dev/null | grep -q .; then
        error_score=$((error_score + 1))
    fi
    
    # 检查是否有友好的错误提示
    if find "$SKILL_PATH" -type f \( -name "*.sh" -o -name "*.py" \) \
       -exec grep -l "echo.*错误\|echo.*error\|log_error\|print.*错误" {} \; 2>/dev/null | grep -q .; then
        error_score=$((error_score + 1))
    else
        suggestions+=("添加更友好的错误提示信息")
    fi
    
    # 检查是否有配置帮助信息
    if [ -f "${SKILL_PATH}/SKILL.md" ]; then
        if grep -i "配置示例\|configuration example" "${SKILL_PATH}/SKILL.md" > /dev/null; then
            error_score=$((error_score + 1))
        fi
    fi
    
    return $error_score
}

# 执行检查
config_score=0
check_config_files || config_score=$?

env_score=0
check_env_support || env_score=$?

error_score=0
check_error_messages || error_score=$?

# 计算总分（满分5分）
total_score=$((base_score + config_score + env_score + error_score))
if [ $total_score -gt 5 ]; then
    total_score=5
fi

# 如果分数较低，给出具体建议
if [ $total_score -lt 3 ]; then
    if [ $config_score -eq 0 ]; then
        suggestions+=("创建配置文件示例，降低用户使用门槛")
    fi
    if [ $env_score -lt 2 ]; then
        suggestions+=("添加环境变量支持，方便容器化部署")
    fi
fi

# 转换 issues 和 suggestions 为 JSON 数组
json_issues=$(printf '%s\n' "${issues[@]}" | jq -R . | jq -s .)
json_suggestions=$(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .)

# 输出结果
echo "{\"score\": $total_score, \"max_score\": 5, \"issues\": $json_issues, \"suggestions\": $json_suggestions}"