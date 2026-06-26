#!/bin/bash
#
# code-quality-analyzer.sh - 代码质量分析模块
# 技术债务评分 + 设计模式识别 (Linux/macOS)
#

set -e

# 配置
MAX_FILE_LINES=500
MAX_FUNCTION_LINES=100
MIN_COMMENT_RATIO=0.05

# 全局统计
TOTAL_FILES=0
TOTAL_LINES=0
CODE_LINES=0
COMMENT_LINES=0
BLANK_LINES=0
VAR_COUNT=0
LET_COUNT=0
CONST_COUNT=0

# 技术债务扣分
DEBT_ISSUES=()

# 设计模式检测
declare -A PATTERN_FILES

# 解析参数
PROJECT_PATH="$1"
OUTPUT_PATH="$2"
PROJECT_TYPE="${3:-uniapp}"

if [[ -z "$PROJECT_PATH" ]] || [[ -z "$OUTPUT_PATH" ]]; then
    echo "Usage: $0 <project_path> <output_path> [project_type]"
    exit 1
fi

# 初始化 JSON 输出
JQ_AVAILABLE=false
if command -v jq &> /dev/null; then
    JQ_AVAILABLE=true
fi

# 数组转 JSON 数组
array_to_json() {
    local arr=("$@")
    local result="["
    local first=true
    for item in "${arr[@]}"; do
        if [[ "$first" == true ]]; then
            first=false
        else
            result+=","
        fi
        # 转义特殊字符并用引号包裹
        local escaped=$(printf '%s' "$item" | sed 's/\\/\\\\/g; s/"/\\"/g')
        result+="\"$escaped\""
    done
    result+="]"
    echo "$result"
}

# 分析单个文件
analyze_file() {
    local file="$1"
    local lines=()
    local line_count=0
    local code_line_count=0
    local comment_line_count=0
    local blank_line_count=0
    local in_block_comment=false
    local functions=()
    local current_function=""
    local function_lines=0
    local brace_count=0
    
    # 读取文件内容
    while IFS= read -r line || [[ -n "$line" ]]; do
        line_count=$((line_count + 1))
        local trimmed=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        
        # 空行
        if [[ -z "$trimmed" ]]; then
            blank_line_count=$((blank_line_count + 1))
            continue
        fi
        
        # 块注释 /* */
        if [[ "$in_block_comment" == true ]]; then
            comment_line_count=$((comment_line_count + 1))
            if [[ "$trimmed" == *"*/*"* ]]; then
                in_block_comment=false
            fi
            continue
        fi
        
        if [[ "$trimmed" =~ ^/\* ]]; then
            comment_line_count=$((comment_line_count + 1))
            if [[ "$trimmed" =~ \*/ ]]; then
                in_block_comment=false
            else
                in_block_comment=true
            fi
            continue
        fi
        
        # 行注释 //
        if [[ "$trimmed" =~ ^// ]]; then
            comment_line_count=$((comment_line_count + 1))
            continue
        fi
        
        # HTML 注释 <!-- -->
        if [[ "$trimmed" =~ ^\<!-- ]]; then
            comment_line_count=$((comment_line_count + 1))
            continue
        fi
        
        # 代码行
        code_line_count=$((code_line_count + 1))
        
        # 检测函数定义
        if [[ "$trimmed" =~ ^(function[[:space:]]+([a-zA-Z_][a-zA-Z0-9_]*)|([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{|([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(async\s+)?function|([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*async) ]]; then
            if [[ -n "$current_function" ]] && [[ $function_lines -gt 0 ]]; then
                functions+=("{\"name\":\"$current_function\",\"lines\":$function_lines}")
            fi
            
            if [[ -n "${BASH_REMATCH[2]}" ]]; then
                current_function="${BASH_REMATCH[2]}"
            elif [[ -n "${BASH_REMATCH[3]}" ]]; then
                current_function="${BASH_REMATCH[3]}"
            elif [[ -n "${BASH_REMATCH[4]}" ]]; then
                current_function="${BASH_REMATCH[4]}"
            elif [[ -n "${BASH_REMATCH[6]}" ]]; then
                current_function="${BASH_REMATCH[6]}"
            else
                current_function="anonymous"
            fi
            function_lines=1
        elif [[ -n "$current_function" ]]; then
            function_lines=$((function_lines + 1))
            # 检测函数结束
            local open=$(echo "$line" | grep -o '{' | wc -l)
            local close=$(echo "$line" | grep -o '}' | wc -l)
            brace_count=$((brace_count + open - close))
            
            if [[ $brace_count -le 0 ]] && [[ "$line" =~ ^[[:space:]]*\} ]]; then
                functions+=("{\"name\":\"$current_function\",\"lines\":$function_lines}")
                current_function=""
                function_lines=0
                brace_count=0
            fi
        fi
    done < "$file"
    
    # 检测 var/let/const 使用
    local var_count=$(grep -oE '\bvar[[:space:]]+' "$file" 2>/dev/null | wc -l)
    local let_count=$(grep -oE '\blet[[:space:]]+' "$file" 2>/dev/null | wc -l)
    local const_count=$(grep -oE '\bconst[[:space:]]+' "$file" 2>/dev/null | wc -l)
    
    # 累加到全局统计
    TOTAL_FILES=$((TOTAL_FILES + 1))
    TOTAL_LINES=$((TOTAL_LINES + line_count))
    CODE_LINES=$((CODE_LINES + code_line_count))
    COMMENT_LINES=$((COMMENT_LINES + comment_line_count))
    BLANK_LINES=$((BLANK_LINES + blank_line_count))
    VAR_COUNT=$((VAR_COUNT + var_count))
    LET_COUNT=$((LET_COUNT + let_count))
    CONST_COUNT=$((CONST_COUNT + const_count))
    
    # 计算注释比例
    local comment_ratio=0
    if [[ $line_count -gt 0 ]]; then
        comment_ratio=$(echo "scale=4; $comment_line_count / $line_count" | bc 2>/dev/null || echo "0")
    fi
    
    # 输出文件分析结果
    local relative_path="${file#$PROJECT_PATH/}"
    echo "FILE:$relative_path|$line_count|$code_line_count|$comment_line_count|$comment_ratio|${functions[*]}"
    
    # 技术债务检测
    if [[ $line_count -gt $MAX_FILE_LINES ]]; then
        local deduction=$(( (line_count - MAX_FILE_LINES) / 100 ))
        if [[ $deduction -gt 5 ]]; then deduction=5; fi
        DEBT_ISSUES+=("{\"category\":\"LargeFile\",\"file\":\"$relative_path\",\"message\":\"$line_count lines (threshold: $MAX_FILE_LINES)\",\"deduction\":$deduction}")
    fi
    
    if [[ $(echo "$comment_ratio < $MIN_COMMENT_RATIO" | bc 2>/dev/null || echo "0") -eq 1 ]] && [[ $line_count -gt 50 ]]; then
        DEBT_ISSUES+=("{\"category\":\"LowComments\",\"file\":\"$relative_path\",\"message\":\"Ratio: $(echo "$comment_ratio * 100" | bc 2>/dev/null)% (min: 5%)\",\"deduction\":1}")
    fi
    
    # 检测设计模式
    detect_patterns "$file" "$relative_path"
}

# 检测设计模式
detect_patterns() {
    local file="$1"
    local relative="$2"
    
    # Singleton
    if grep -qE 'getInstance|instance\s*=|static\s+instance' "$file" 2>/dev/null; then
        PATTERN_FILES["Singleton"]+="$relative,"
    fi
    
    # Factory
    if grep -qE 'create[A-Z]|factory|new\s+\w+\(' "$file" 2>/dev/null; then
        PATTERN_FILES["Factory"]+="$relative,"
    fi
    
    # Observer
    if grep -qE '\.on\s*\(|\.emit\s*\(|subscribe|addEventListener|\$on\s*\(|\$emit\s*\(' "$file" 2>/dev/null; then
        PATTERN_FILES["Observer"]+="$relative,"
    fi
    
    # Module
    if grep -qE 'export\s+default|module\.exports|exports\.|import\s+.*\s+from' "$file" 2>/dev/null; then
        PATTERN_FILES["Module"]+="$relative,"
    fi
}

# 主分析流程
echo "Running code quality analysis..."

# 查找所有 JS/Vue 文件（兼容旧版 bash 和无 mapfile 的系统）
find_js_files() {
    find "$PROJECT_PATH" -name "*.js" -type f 2>/dev/null | grep -Ev '(node_modules|unpackage|uni_modules|\.git)' || true
}

find_vue_files() {
    find "$PROJECT_PATH" -name "*.vue" -type f 2>/dev/null | grep -Ev '(node_modules|unpackage|uni_modules|\.git)' || true
}

# 尝试使用 mapfile，不支持时使用备用方案
if declare -f mapfile > /dev/null 2>&1; then
    mapfile -t js_files < <(find_js_files)
    mapfile -t vue_files < <(find_vue_files)
else
    # 备用方案：使用 while read
    js_files=()
    while IFS= read -r file; do
        js_files+=("$file")
    done < <(find_js_files)
    vue_files=()
    while IFS= read -r file; do
        vue_files+=("$file")
    done < <(find_vue_files)
fi

file_count=$((${#js_files[@]} + ${#vue_files[@]}))
echo "  Found $file_count files to analyze"

# 分析每个文件
file_analyses=()
for file in "${js_files[@]}" "${vue_files[@]}"; do
    if [[ -f "$file" ]]; then
        result=$(analyze_file "$file")
        file_analyses+=("$result")
    fi
done

# 计算技术债务评分
debt_score=100
deductions_json="[]"

# var 使用扣分
total_declarations=$((VAR_COUNT + LET_COUNT + CONST_COUNT))
if [[ $total_declarations -gt 0 ]]; then
    var_ratio=$(echo "scale=4; $VAR_COUNT / $total_declarations" | bc 2>/dev/null || echo "0")
    if [[ $(echo "$var_ratio > 0.3" | bc 2>/dev/null || echo "0") -eq 1 ]]; then
        deduction=$(echo "$var_ratio * 10" | bc 2>/dev/null | cut -d. -f1)
        if [[ $deduction -gt 10 ]]; then deduction=10; fi
        debt_score=$((debt_score - deduction))
        DEBT_ISSUES+=("{\"category\":\"VarUsage\",\"file\":\"Multiple\",\"message\":\"var ratio: $(echo "$var_ratio * 100" | bc 2>/dev/null)%\",\"deduction\":$deduction}")
    fi
fi

if [[ $debt_score -lt 0 ]]; then debt_score=0; fi

# 生成评分等级
if [[ $debt_score -ge 90 ]]; then grade="A"
elif [[ $debt_score -ge 80 ]]; then grade="B"
elif [[ $debt_score -ge 70 ]]; then grade="C"
elif [[ $debt_score -ge 60 ]]; then grade="D"
else grade="F"
fi

# 构建 JSON 报告
report_file="$OUTPUT_PATH/code_quality.json"

# 生成 design patterns JSON（兼容无 jq 环境）
generate_pattern_json() {
    local pattern_name="$1"
    local files_str="${PATTERN_FILES[$pattern_name]}"
    local detected="false"
    local files_json="[]"
    
    if [[ -n "$files_str" ]]; then
        detected="true"
        if [[ "$JQ_AVAILABLE" == true ]]; then
            files_json=$(echo "$files_str" | sed 's/,$//' | tr ',' '\n' | jq -R . 2>/dev/null | jq -s .) || files_json="[]"
        else
            # 无 jq 时的简单处理
            local cleaned=$(echo "$files_str" | sed 's/,$//' | tr ',' '\n' | grep -v '^$' | sed "s/\"/\\\\\"/g")
            if [[ -n "$cleaned" ]]; then
                files_json="[$(echo "$cleaned" | while IFS= read -r f; do echo "\"$f\""; done | tr '\n' ',' | sed 's/,$//')]"
            fi
        fi
    fi
    
    echo "{ \"detected\": $detected, \"files\": $files_json }"
}

SINGLETON_JSON=$(generate_pattern_json "Singleton")
FACTORY_JSON=$(generate_pattern_json "Factory")
OBSERVER_JSON=$(generate_pattern_json "Observer")
MODULE_JSON=$(generate_pattern_json "Module")

cat > "$report_file" << EOF
{
  "timestamp": "$(date +%Y-%m-%dT%H:%M:%S)",
  "projectPath": "$PROJECT_PATH",
  "projectType": "$PROJECT_TYPE",
  "summary": {
    "totalFiles": $TOTAL_FILES,
    "totalLines": $TOTAL_LINES,
    "codeLines": $CODE_LINES,
    "commentLines": $COMMENT_LINES,
    "blankLines": $BLANK_LINES,
    "commentRatio": $(echo "scale=4; $COMMENT_LINES / $TOTAL_LINES" | bc 2>/dev/null || echo "0"),
    "declarations": {
      "var": $VAR_COUNT,
      "let": $LET_COUNT,
      "const": $CONST_COUNT
    }
  },
  "debtScore": {
    "score": $debt_score,
    "grade": "$grade",
    "issues": ${#DEBT_ISSUES[@]}
  },
  "designPatterns": {
    "Singleton": $SINGLETON_JSON,
    "Factory": $FACTORY_JSON,
    "Observer": $OBSERVER_JSON,
    "Module": $MODULE_JSON
  },
  "deductions": [
    $(IFS=,; echo "${DEBT_ISSUES[*]}")
  ]
}
EOF

echo "  Code quality analysis complete"
echo "  Debt Score: $debt_score/100 (Grade: $grade)"
echo "  Issues found: ${#DEBT_ISSUES[@]}"

echo "$report_file"
