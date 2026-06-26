#!/bin/bash
# 代码规范性检查器

set -euo pipefail

SKILL_PATH="$1"

# 初始化结果
issues=()
suggestions=()
base_score=5  # 起始满分，发现问题扣分

# 检查文件结构
check_file_structure() {
    local structure_score=1
    
    # 检查是否有合理的目录结构
    if [ -d "${SKILL_PATH}/scripts" ] || [ -d "${SKILL_PATH}/bin" ]; then
        structure_score=2
    else
        suggestions+=("考虑创建 scripts/ 或 bin/ 目录存放脚本")
    fi
    
    if [ -d "${SKILL_PATH}/templates" ]; then
        structure_score=$((structure_score + 1))
    fi
    
    if [ -d "${SKILL_PATH}/examples" ]; then
        structure_score=$((structure_score + 1))
    fi
    
    if [ -d "${SKILL_PATH}/config" ]; then
        structure_score=$((structure_score + 1))
    fi
    
    return $structure_score
}

# 安全检查
check_security() {
    local security_issues=0
    
    # 检查硬编码密钥
    if find "$SKILL_PATH" -type f \( -name "*.sh" -o -name "*.py" -o -name "*.js" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) \
       ! -path "*/node_modules/*" ! -path "*/.git/*" \
       -exec grep -l -i "password.*=.*['\"].\{8,\}['\"]\|token.*=.*['\"].\{8,\}['\"]\|secret.*=.*['\"].\{8,\}['\"]\|key.*=.*['\"].\{8,\}['\"]" {} \; 2>/dev/null | grep -q .; then
        issues+=("发现可能的硬编码密钥")
        suggestions+=("使用环境变量或配置文件存储敏感信息")
        security_issues=$((security_issues + 1))
    fi
    
    # 检查危险权限
    if find "$SKILL_PATH" -type f -name "*.sh" \
       -exec grep -l "chmod.*777\|chmod.*a+rwx" {} \; 2>/dev/null | grep -q .; then
        issues+=("发现过度权限设置 (chmod 777)")
        suggestions+=("使用最小权限原则，如 chmod 755 或 chmod 644")
        security_issues=$((security_issues + 1))
    fi
    
    # 检查危险操作
    if find "$SKILL_PATH" -type f -name "*.sh" \
       -exec grep -l "rm.*-rf.*\\s*/\\|rm.*-rf.*\\$" {} \; 2>/dev/null | grep -q .; then
        issues+=("发现危险删除操作 (rm -rf /)")
        suggestions+=("避免使用 rm -rf 删除根目录或变量路径")
        security_issues=$((security_issues + 2))  # 严重问题，扣分更多
    fi
    
    # 检查远程脚本执行
    if find "$SKILL_PATH" -type f -name "*.sh" \
       -exec grep -l "curl.*|.*sh\|wget.*|.*sh" {} \; 2>/dev/null | grep -q .; then
        issues+=("发现远程脚本执行模式")
        suggestions+=("下载脚本后先验证再执行，或使用可信源")
        security_issues=$((security_issues + 1))
    fi
    
    return $security_issues
}

# 检查错误处理
check_error_handling() {
    local error_score=0
    
    # 检查 shell 脚本的错误处理
    for file in $(find "$SKILL_PATH" -type f -name "*.sh"); do
        if head -10 "$file" | grep -q "set -e\|set -o errexit"; then
            error_score=$((error_score + 1))
            break
        fi
    done
    
    # 检查是否有清理机制
    if find "$SKILL_PATH" -type f -name "*.sh" \
       -exec grep -l "trap.*cleanup\|trap.*exit" {} \; 2>/dev/null | grep -q .; then
        error_score=$((error_score + 1))
    else
        suggestions+=("考虑添加 trap 清理临时文件")
    fi
    
    # 检查是否有输入验证
    if find "$SKILL_PATH" -type f -name "*.sh" \
       -exec grep -l "\\$\\{.*:-.*\\}\|\\$\\{.*:?.*\\}\|if.*-z.*\\$" {} \; 2>/dev/null | grep -q .; then
        error_score=$((error_score + 1))
    else
        suggestions+=("添加输入参数验证")
    fi
    
    return $error_score
}

# 检查工具使用合理性
check_tool_usage() {
    local tool_score=2  # 基础分
    
    # 检查是否有过度权限申请
    if [ -f "${SKILL_PATH}/SKILL.md" ]; then
        if grep -i "工具.*权限" "${SKILL_PATH}/SKILL.md" | grep -i "所有\|全部\|all" > /dev/null; then
            issues+=("可能申请了过度工具权限")
            suggestions+=("按需申请最小必要工具权限")
            tool_score=$((tool_score - 1))
        fi
    fi
    
    return $tool_score
}

# 执行检查
structure_score=0
check_file_structure || structure_score=$?

security_issues=0
check_security || security_issues=$?

error_score=0
check_error_handling || error_score=$?

tool_score=0
check_tool_usage || tool_score=$?

# 计算总分（满分5分）
# 结构分：0-2分，安全分：扣分制，错误处理：0-3分，工具使用：0-2分
structure_normalized=$((structure_score * 2 / 5))  # 将5分制转换为2分制
error_normalized=$((error_score * 3 / 3))  # 3分制保持

total_score=$((structure_normalized + error_normalized + tool_score))
# 安全扣分
total_score=$((total_score - security_issues))

# 确保分数在 0-5 范围内
if [ $total_score -lt 0 ]; then
    total_score=0
elif [ $total_score -gt 5 ]; then
    total_score=5
fi

# 如果没有问题，给点正面反馈
if [ ${#issues[@]} -eq 0 ] && [ $total_score -ge 4 ]; then
    suggestions+=("代码结构良好，安全措施到位")
fi

# 转换 issues 和 suggestions 为 JSON 数组
json_issues=$(printf '%s\n' "${issues[@]}" | jq -R . | jq -s .)
json_suggestions=$(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .)

# 输出结果
echo "{\"score\": $total_score, \"max_score\": 5, \"issues\": $json_issues, \"suggestions\": $json_suggestions}"