#!/bin/bash

# 技能验证工具 - 修复版 v1.0.1
# 作者: puppetcat-fire (柏然)
# GitHub: https://github.com/puppetcat-fire/openclaw-skills

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 帮助信息
show_help() {
    cat << EOF
技能验证工具 - 修复版 v1.0.1

用法: $0 [选项] <技能目录>

选项:
  --help, -h     显示帮助信息
  --verbose, -v  详细输出模式
  --json         输出JSON格式结果
  --quick, -q    快速检查模式

示例:
  $0 ~/my-skill           # 验证指定技能
  $0 .                    # 验证当前目录技能
  $0 --json ~/my-skill    # 输出JSON格式结果
  $0 --quick ~/my-skill   # 快速检查

验证内容:
  1. 文件结构检查
  2. 必需文件检查
  3. 脚本语法检查
  4. 配置检查
EOF
}

# 初始化结果
init_results() {
    cat << EOF
{
  "skill": "",
  "path": "",
  "timestamp": "$(date -Iseconds)",
  "version": "1.0.1",
  "checks": [],
  "summary": {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "warnings": 0,
    "score": 0
  }
}
EOF
}

# 添加检查结果
add_check() {
    local results="$1"
    local name="$2"
    local status="$3"
    local message="$4"
    local file="${5:-}"
    
    local check_json
    if [ -n "$file" ]; then
        check_json="{\"name\":\"$name\",\"status\":\"$status\",\"message\":\"$message\",\"file\":\"$file\"}"
    else
        check_json="{\"name\":\"$name\",\"status\":\"$status\",\"message\":\"$message\"}"
    fi
    
    echo "$results" | jq --argjson check "$check_json" '.checks += [$check]'
}

# 更新摘要
update_summary() {
    local results="$1"
    local checks=$(echo "$results" | jq '.checks | length')
    local passed=$(echo "$results" | jq '[.checks[] | select(.status == "passed")] | length')
    local failed=$(echo "$results" | jq '[.checks[] | select(.status == "failed")] | length')
    local warnings=$(echo "$results" | jq '[.checks[] | select(.status == "warning")] | length')
    
    local score=0
    if [ "$checks" -gt 0 ]; then
        score=$(( (passed * 100) / checks ))
    fi
    
    echo "$results" | jq \
        --argjson total "$checks" \
        --argjson passed "$passed" \
        --argjson failed "$failed" \
        --argjson warnings "$warnings" \
        --argjson score "$score" \
        '.summary.total = $total | .summary.passed = $passed | .summary.failed = $failed | .summary.warnings = $warnings | .summary.score = $score'
}

# 文件结构检查
check_file_structure() {
    local skill_dir="$1"
    local results="$2"
    
    echo -e "${BLUE}📁 检查文件结构...${NC}"
    
    # 检查必需文件
    local required_files=("SKILL.md" "package.json")
    for file in "${required_files[@]}"; do
        if [ -f "$skill_dir/$file" ]; then
            results=$(add_check "$results" "必需文件检查" "passed" "找到 $file" "$file")
        else
            results=$(add_check "$results" "必需文件检查" "failed" "缺少 $file" "$file")
        fi
    done
    
    # 检查可选文件
    local optional_files=("install.sh" "README.md" "LICENSE")
    for file in "${optional_files[@]}"; do
        if [ -f "$skill_dir/$file" ]; then
            results=$(add_check "$results" "可选文件检查" "passed" "找到 $file" "$file")
        else
            results=$(add_check "$results" "可选文件检查" "warning" "建议添加 $file" "$file")
        fi
    done
    
    echo "$results"
}

# 脚本语法检查
check_script_syntax() {
    local skill_dir="$1"
    local results="$2"
    
    echo -e "${BLUE}🔧 检查脚本语法...${NC}"
    
    # 检查所有.sh文件
    find "$skill_dir" -name "*.sh" -type f | while read -r script; do
        local script_name=$(basename "$script")
        
        # 检查执行权限
        if [ -x "$script" ]; then
            results=$(add_check "$results" "脚本执行权限" "passed" "$script_name 有执行权限" "$script_name")
        else
            results=$(add_check "$results" "脚本执行权限" "warning" "$script_name 缺少执行权限" "$script_name")
        fi
        
        # 检查shebang
        if head -1 "$script" | grep -q "^#!/"; then
            results=$(add_check "$results" "脚本shebang" "passed" "$script_name 有正确的shebang" "$script_name")
        else
            results=$(add_check "$results" "脚本shebang" "warning" "$script_name 缺少shebang" "$script_name")
        fi
        
        # 检查bash语法
        if bash -n "$script" 2>/dev/null; then
            results=$(add_check "$results" "脚本语法检查" "passed" "$script_name 语法正确" "$script_name")
        else
            results=$(add_check "$results" "脚本语法检查" "failed" "$script_name 有语法错误" "$script_name")
        fi
    done
    
    echo "$results"
}

# 配置检查
check_configuration() {
    local skill_dir="$1"
    local results="$2"
    
    echo -e "${BLUE}⚙️  检查配置...${NC}"
    
    # 检查package.json
    if [ -f "$skill_dir/package.json" ]; then
        if jq empty "$skill_dir/package.json" 2>/dev/null; then
            results=$(add_check "$results" "package.json格式" "passed" "JSON格式正确" "package.json")
            
            # 检查必需字段
            local required_fields=("name" "version" "description")
            for field in "${required_fields[@]}"; do
                if jq -e ".$field" "$skill_dir/package.json" >/dev/null 2>&1; then
                    results=$(add_check "$results" "package.json字段" "passed" "包含 $field 字段" "package.json")
                else
                    results=$(add_check "$results" "package.json字段" "failed" "缺少 $field 字段" "package.json")
                fi
            done
        else
            results=$(add_check "$results" "package.json格式" "failed" "JSON格式错误" "package.json")
        fi
    fi
    
    # 检查SKILL.md的YAML前部
    if [ -f "$skill_dir/SKILL.md" ]; then
        if head -10 "$skill_dir/SKILL.md" | grep -q "^---"; then
            results=$(add_check "$results" "SKILL.md格式" "passed" "有YAML前部" "SKILL.md")
        else
            results=$(add_check "$results" "SKILL.md格式" "warning" "建议添加YAML前部" "SKILL.md")
        fi
    fi
    
    echo "$results"
}

# 主函数
main() {
    # 解析参数
    local skill_dir=""
    local output_json=false
    local verbose=false
    local quick_mode=false
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help|-h)
                show_help
                exit 0
                ;;
            --json)
                output_json=true
                shift
                ;;
            --verbose|-v)
                verbose=true
                shift
                ;;
            --quick|-q)
                quick_mode=true
                shift
                ;;
            *)
                skill_dir="$1"
                shift
                ;;
        esac
    done
    
    # 检查参数
    if [ -z "$skill_dir" ]; then
        echo -e "${RED}错误: 需要指定技能目录${NC}"
        show_help
        exit 1
    fi
    
    if [ ! -d "$skill_dir" ]; then
        echo -e "${RED}错误: 目录不存在: $skill_dir${NC}"
        exit 1
    fi
    
    # 初始化结果
    local results=$(init_results)
    results=$(echo "$results" | jq --arg skill "$(basename "$skill_dir")" --arg path "$skill_dir" '.skill = $skill | .path = $path')
    
    echo -e "${GREEN}🔍 开始验证技能: $(basename "$skill_dir")${NC}"
    echo -e "路径: $skill_dir"
    echo ""
    
    # 执行检查
    results=$(check_file_structure "$skill_dir" "$results")
    results=$(check_script_syntax "$skill_dir" "$results")
    
    if [ "$quick_mode" = false ]; then
        results=$(check_configuration "$skill_dir" "$results")
    fi
    
    # 更新摘要
    results=$(update_summary "$results")
    
    # 输出结果
    if [ "$output_json" = true ]; then
        echo "$results"
    else
        local total=$(echo "$results" | jq '.summary.total')
        local passed=$(echo "$results" | jq '.summary.passed')
        local failed=$(echo "$results" | jq '.summary.failed')
        local warnings=$(echo "$results" | jq '.summary.warnings')
        local score=$(echo "$results" | jq '.summary.score')
        
        echo ""
        echo -e "${BLUE}========================================${NC}"
        echo -e "${BLUE}           验证结果摘要${NC}"
        echo -e "${BLUE}========================================${NC}"
        echo ""
        echo -e "📊 总计检查: $total"
        echo -e "✅ 通过: $passed"
        echo -e "❌ 失败: $failed"
        echo -e "⚠️  警告: $warnings"
        echo -e "🏆 得分: $score/100"
        echo ""
        
        if [ "$failed" -gt 0 ]; then
            echo -e "${RED}❌ 验证失败，请修复上述问题${NC}"
            exit 1
        elif [ "$warnings" -gt 0 ]; then
            echo -e "${YELLOW}⚠️  验证通过，但有警告需要关注${NC}"
            exit 0
        else
            echo -e "${GREEN}✅ 验证通过，所有检查项都符合要求${NC}"
            exit 0
        fi
    fi
}

# 运行主函数
main "$@"