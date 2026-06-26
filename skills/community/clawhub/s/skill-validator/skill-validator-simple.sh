#!/bin/bash

# 简化版技能验证工具
# 无jq依赖，使用纯bash实现

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_help() {
    echo "简化版技能验证工具"
    echo "用法: $0 <技能目录>"
    echo ""
    echo "检查内容："
    echo "  1. 必需文件 (SKILL.md, package.json)"
    echo "  2. 脚本语法"
    echo "  3. 文件权限"
}

check_skill() {
    local skill_dir="$1"
    
    echo -e "${GREEN}🔍 验证技能: $(basename "$skill_dir")${NC}"
    echo "路径: $skill_dir"
    echo ""
    
    local passed=0
    local failed=0
    local warnings=0
    
    # 检查必需文件
    echo -e "${BLUE}📁 检查必需文件：${NC}"
    for file in "SKILL.md" "package.json"; do
        if [ -f "$skill_dir/$file" ]; then
            echo -e "  ✅ $file"
            ((passed++))
        else
            echo -e "  ❌ 缺少 $file"
            ((failed++))
        fi
    done
    
    # 检查可选文件
    echo ""
    echo -e "${BLUE}📁 检查可选文件：${NC}"
    for file in "install.sh" "README.md" "LICENSE"; do
        if [ -f "$skill_dir/$file" ]; then
            echo -e "  ✅ $file"
            ((passed++))
        else
            echo -e "  ⚠️  建议添加 $file"
            ((warnings++))
        fi
    done
    
    # 检查脚本
    echo ""
    echo -e "${BLUE}🔧 检查脚本：${NC}"
    find "$skill_dir" -name "*.sh" -type f | while read -r script; do
        local script_name=$(basename "$script")
        
        # 执行权限
        if [ -x "$script" ]; then
            echo -e "  ✅ $script_name 有执行权限"
            ((passed++))
        else
            echo -e "  ⚠️  $script_name 缺少执行权限"
            ((warnings++))
        fi
        
        # shebang
        if head -1 "$script" | grep -q "^#!/"; then
            echo -e "  ✅ $script_name 有正确的shebang"
            ((passed++))
        else
            echo -e "  ⚠️  $script_name 缺少shebang"
            ((warnings++))
        fi
        
        # 语法检查
        if bash -n "$script" 2>/dev/null; then
            echo -e "  ✅ $script_name 语法正确"
            ((passed++))
        else
            echo -e "  ❌ $script_name 有语法错误"
            ((failed++))
        fi
    done
    
    # 总结
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}           验证结果${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "✅ 通过: $passed"
    echo -e "❌ 失败: $failed"
    echo -e "⚠️  警告: $warnings"
    echo ""
    
    local total=$((passed + failed + warnings))
    if [ "$total" -gt 0 ]; then
        local score=$(( (passed * 100) / total ))
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
