#!/bin/bash

# 技能验证工具 v1.0.11 - 简化修复版
# 无jq依赖，纯bash实现，兼容ClawHub规范检查

set -e

# 颜色定义（简化，避免干扰）
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_help() {
    echo "技能验证工具 v1.0.11"
    echo "用法: $0 <技能目录>"
    echo ""
    echo "基于ClawHub技能格式规范检查："
    echo "  1. 必需文件 (SKILL.md, package.json)"
    echo "  2. 脚本语法和权限"
    echo "  3. 文件结构完整性"
    echo ""
    echo "输出：通过/失败状态，详细检查结果"
}

check_skill() {
    local skill_dir="$1"
    local skill_name=$(basename "$skill_dir")
    
    # 检查ClawHub规范版本（占位符，后续实现完整检测）
    echo -e "${BLUE}📋 ClawHub规范版本检查：${NC}"
    echo "  ℹ️  规范版本检测功能建设中..."
    echo ""
    
    echo -e "${GREEN}🔍 验证技能: $skill_name${NC}"
    echo "路径: $skill_dir"
    echo ""
    
    # 使用关联数组跟踪结果（bash 4+）
    declare -A results
    results["passed"]=0
    results["failed"]=0
    results["warnings"]=0
    
    # 检查必需文件
    echo -e "${BLUE}📁 检查必需文件：${NC}"
    
    # SKILL.md
    if [ -f "$skill_dir/SKILL.md" ] || [ -f "$skill_dir/skill.md" ]; then
        echo -e "  ✅ SKILL.md"
        results["passed"]=$((results["passed"] + 1))
    else
        echo -e "  ❌ 缺少 SKILL.md"
        results["failed"]=$((results["failed"] + 1))
    fi
    
    # package.json
    if [ -f "$skill_dir/package.json" ]; then
        echo -e "  ✅ package.json"
        results["passed"]=$((results["passed"] + 1))
    else
        echo -e "  ⚠️  缺少 package.json（可选但推荐）"
        results["warnings"]=$((results["warnings"] + 1))
    fi
    
    # 检查可选文件
    echo ""
    echo -e "${BLUE}📁 检查可选文件：${NC}"
    
    local optional_files=("install.sh" "README.md" "LICENSE")
    for file in "${optional_files[@]}"; do
        if [ -f "$skill_dir/$file" ]; then
            echo -e "  ✅ $file"
            results["passed"]=$((results["passed"] + 1))
        else
            echo -e "  ⚠️  建议添加 $file"
            results["warnings"]=$((results["warnings"] + 1))
        fi
    done
    
    # 检查脚本
    echo ""
    echo -e "${BLUE}🔧 检查脚本：${NC}"
    
    local script_count=0
    while IFS= read -r script; do
        [ -z "$script" ] && continue
        script_count=$((script_count + 1))
        local script_name=$(basename "$script")
        
        # 执行权限
        if [ -x "$script" ]; then
            echo -e "  ✅ $script_name 有执行权限"
            results["passed"]=$((results["passed"] + 1))
        else
            echo -e "  ⚠️  $script_name 缺少执行权限"
            results["warnings"]=$((results["warnings"] + 1))
        fi
        
        # shebang
        if head -1 "$script" 2>/dev/null | grep -q "^#!/"; then
            echo -e "  ✅ $script_name 有正确的shebang"
            results["passed"]=$((results["passed"] + 1))
        else
            echo -e "  ⚠️  $script_name 缺少shebang"
            results["warnings"]=$((results["warnings"] + 1))
        fi
        
        # 语法检查（仅bash脚本）
        if [[ "$script_name" == *.sh ]]; then
            if bash -n "$script" 2>/dev/null; then
                echo -e "  ✅ $script_name 语法正确"
                results["passed"]=$((results["passed"] + 1))
            else
                echo -e "  ❌ $script_name 有语法错误"
                results["failed"]=$((results["failed"] + 1))
            fi
        fi
        
    done < <(find "$skill_dir" -name "*.sh" -type f 2>/dev/null)
    
    if [ "$script_count" -eq 0 ]; then
        echo -e "  ℹ️  未找到脚本文件"
    fi
    
    # 总结
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}           验证结果${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    local passed=${results["passed"]}
    local failed=${results["failed"]}
    local warnings=${results["warnings"]}
    
    echo -e "✅ 通过: $passed"
    echo -e "❌ 失败: $failed"
    echo -e "⚠️  警告: $warnings"
    echo ""
    
    local total=$((passed + failed + warnings))
    if [ "$total" -gt 0 ]; then
        local score=0
        if [ "$total" -gt 0 ]; then
            score=$(( (passed * 100) / total ))
        fi
        echo -e "🏆 得分: $score/100"
    fi
    
    if [ "$failed" -gt 0 ]; then
        echo -e "${RED}❌ 验证失败${NC}"
        return 1
    elif [ "$warnings" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  验证通过，但有警告${NC}"
        return 0
    else
        echo -e "${GREEN}✅ 验证通过${NC}"
        return 0
    fi
}

# 主函数
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

check_skill "$1"
exit $?