#!/bin/bash
# 维护活跃度检查器

set -euo pipefail

SKILL_PATH="$1"

# 初始化结果
issues=()
suggestions=()
base_score=2  # 基础分

# 检查版本号
check_version() {
    local version_score=0
    
    # 检查是否有版本文件
    if [ -f "${SKILL_PATH}/VERSION" ] || [ -f "${SKILL_PATH}/version.txt" ]; then
        version_score=$((version_score + 1))
        
        # 检查版本号格式
        if grep -q -E "^v?[0-9]+\.[0-9]+\.[0-9]+" "${SKILL_PATH}/VERSION" 2>/dev/null || \
           grep -q -E "^v?[0-9]+\.[0-9]+\.[0-9]+" "${SKILL_PATH}/version.txt" 2>/dev/null; then
            version_score=$((version_score + 1))
        fi
    fi
    
    # 检查 SKILL.md 中的版本号
    if [ -f "${SKILL_PATH}/SKILL.md" ]; then
        if grep -q -E "版本.*v?[0-9]+\.[0-9]+\.[0-9]+\|Version.*v?[0-9]+\.[0-9]+\.[0-9]+" "${SKILL_PATH}/SKILL.md"; then
            version_score=$((version_score + 1))
        fi
    fi
    
    if [ $version_score -eq 0 ]; then
        issues+=("未发现版本号信息")
        suggestions+=("添加 VERSION 文件或版本号标识")
    fi
    
    return $version_score
}

# 检查更新记录
check_changelog() {
    local changelog_score=0
    
    # 检查是否有变更日志文件
    if [ -f "${SKILL_PATH}/CHANGELOG.md" ] || [ -f "${SKILL_PATH}/changelog.md" ] || \
       [ -f "${SKILL_PATH}/CHANGELOG" ] || [ -f "${SKILL_PATH}/changelog.txt" ]; then
        changelog_score=$((changelog_score + 2))
    fi
    
    # 检查 SKILL.md 中是否有更新记录章节
    if [ -f "${SKILL_PATH}/SKILL.md" ]; then
        if grep -i "^#.*更新\|^#.*change\|^#.*history\|^#.*版本历史" "${SKILL_PATH}/SKILL.md" > /dev/null; then
            changelog_score=$((changelog_score + 1))
        fi
    fi
    
    if [ $changelog_score -eq 0 ]; then
        issues+=("缺少更新记录或变更日志")
        suggestions+=("添加 CHANGELOG.md 或更新记录章节")
    fi
    
    return $changelog_score
}

# 检查最后更新时间
check_last_update() {
    local update_score=0
    local current_time
    current_time=$(date +%s)
    
    # 查找最新修改的文件
    local latest_file
    latest_file=$(find "$SKILL_PATH" -type f ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/.DS_Store" \
        -exec stat -f "%m %N" {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
    
    if [ -n "$latest_file" ]; then
        local file_mtime
        file_mtime=$(stat -f "%m" "$latest_file" 2>/dev/null || stat -c "%Y" "$latest_file" 2>/dev/null)
        
        if [ -n "$file_mtime" ]; then
            local days_diff=$(( (current_time - file_mtime) / 86400 ))
            
            # 根据最后更新时间评分
            if [ $days_diff -le 30 ]; then
                update_score=3  # 1个月内，优秀
            elif [ $days_diff -le 90 ]; then
                update_score=2  # 3个月内，良好
            elif [ $days_diff -le 180 ]; then
                update_score=1  # 6个月内，一般
            else
                issues+=("最后更新在 $days_diff 天前，可能已不再维护")
                suggestions+=("定期更新技能，修复问题，添加新功能")
            fi
        fi
    fi
    
    return $update_score
}

# 检查依赖声明
check_dependencies() {
    local dep_score=0
    
    # 检查是否有依赖声明文件
    if [ -f "${SKILL_PATH}/requirements.txt" ] || [ -f "${SKILL_PATH}/package.json" ] || \
       [ -f "${SKILL_PATH}/Pipfile" ] || [ -f "${SKILL_PATH}/Gemfile" ]; then
        dep_score=$((dep_score + 1))
    fi
    
    # 检查 SKILL.md 中是否有依赖说明
    if [ -f "${SKILL_PATH}/SKILL.md" ]; then
        if grep -i "依赖\|dependencies\|requirements\|安装需求" "${SKILL_PATH}/SKILL.md" > /dev/null; then
            dep_score=$((dep_score + 1))
        else
            suggestions+=("在文档中明确声明依赖项")
        fi
    fi
    
    return $dep_score
}

# 执行检查
version_score=0
check_version || version_score=$?

changelog_score=0
check_changelog || changelog_score=$?

update_score=0
check_last_update || update_score=$?

dep_score=0
check_dependencies || dep_score=$?

# 计算总分（满分5分）
# 版本:0-3分，变更日志:0-3分，更新:0-3分，依赖:0-2分，但需要归一化到5分制
total_score=$((base_score + version_score + changelog_score + update_score + dep_score))

# 归一化到 0-5 分
if [ $total_score -gt 8 ]; then
    total_score=5
elif [ $total_score -gt 6 ]; then
    total_score=4
elif [ $total_score -gt 4 ]; then
    total_score=3
elif [ $total_score -gt 2 ]; then
    total_score=2
elif [ $total_score -gt 0 ]; then
    total_score=1
fi

# 如果维护状态良好，给正面反馈
if [ $total_score -ge 4 ]; then
    suggestions+=("维护状态良好，继续保持")
fi

# 转换 issues 和 suggestions 为 JSON 数组
json_issues=$(printf '%s\n' "${issues[@]}" | jq -R . | jq -s .)
json_suggestions=$(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .)

# 输出结果
echo "{\"score\": $total_score, \"max_score\": 5, \"issues\": $json_issues, \"suggestions\": $json_suggestions}"