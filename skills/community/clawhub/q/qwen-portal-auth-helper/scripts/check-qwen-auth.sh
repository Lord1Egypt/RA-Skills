#!/bin/bash
# qwen-portal 认证状态检查脚本
# 定期检查认证状态，预警过期风险

set -e

echo "🔍 qwen-portal 认证状态检查"
echo "========================================"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "基于 2026-03-09 实战经验"
echo

# 配置
CHECK_INTERVAL_DAYS=7  # 建议每周检查一次
WARNING_THRESHOLD=3    # 连续错误预警阈值
LOG_FILE="/tmp/qwen-auth-check-$(date +%Y%m%d).log"
REPORT_FILE="/tmp/qwen-auth-report-$(date +%Y%m%d).md"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 函数：记录日志
log() {
    local message="$1"
    local level="${2:-INFO}"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo -e "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# 函数：检查 cron 任务状态
check_cron_tasks() {
    log "检查 cron 任务状态..."
    
    local error_tasks=()
    local warning_tasks=()
    
    # 获取使用 qwen-portal 的任务
    openclaw cron list 2>/dev/null | while read -r line; do
        if echo "$line" | grep -q "qwen-portal"; then
            local task_id=$(echo "$line" | awk '{print $1}')
            local task_name=$(echo "$line" | awk '{print $2}')
            local status=$(echo "$line" | awk '{print $6}')
            local errors=$(echo "$line" | awk '{print $7}')
            
            if [ "$status" = "error" ]; then
                error_tasks+=("$task_id:$task_name:$errors")
                log "❌ 错误任务: $task_name (ID: $task_id, 错误: $errors)" "ERROR"
            elif [ "$errors" -gt "$WARNING_THRESHOLD" ] 2>/dev/null; then
                warning_tasks+=("$task_id:$task_name:$errors")
                log "⚠️  警告任务: $task_name (连续错误: $errors)" "WARNING"
            else
                log "✅ 正常任务: $task_name" "SUCCESS"
            fi
        fi
    done
    
    echo "${#error_tasks[@]}|${#warning_tasks[@]}"
}

# 函数：检查错误详情
check_error_details() {
    local task_id="$1"
    
    log "检查任务 $task_id 的错误详情..."
    
    local error=$(openclaw cron runs --id "$task_id" 2>/dev/null | \
        grep -i "oauth\|token\|error" | \
        head -3 | \
        tr '\n' ' ' | \
        sed 's/  */ /g')
    
    if [ -n "$error" ]; then
        echo "$error"
    else
        echo "未知错误"
    fi
}

# 函数：生成报告
generate_report() {
    local error_count="$1"
    local warning_count="$2"
    
    log "生成检查报告..."
    
    cat > "$REPORT_FILE" << EOF
# qwen-portal 认证状态检查报告

**检查时间**: $(date '+%Y-%m-%d %H:%M:%S')
**检查周期**: 每 $CHECK_INTERVAL_DAYS 天
**预警阈值**: 连续错误 > $WARNING_THRESHOLD 次

## 📊 检查摘要

- **错误任务**: $error_count 个
- **警告任务**: $warning_count 个  
- **检查状态**: $(if [ $error_count -eq 0 ] && [ $warning_count -eq 0 ]; then echo "✅ 全部正常"; else echo "⚠️  需要关注"; fi)

## 🔍 详细检查结果

EOF
    
    # 如果有错误任务，添加到报告
    if [ "$error_count" -gt 0 ]; then
        echo "### ❌ 错误任务" >> "$REPORT_FILE"
        echo >> "$REPORT_FILE"
        
        openclaw cron list 2>/dev/null | grep "error" | while read -r line; do
            if echo "$line" | grep -q "qwen-portal"; then
                local task_id=$(echo "$line" | awk '{print $1}')
                local task_name=$(echo "$line" | awk '{print $2}')
                local errors=$(echo "$line" | awk '{print $7}')
                local error_detail=$(check_error_details "$task_id")
                
                echo "#### $task_name" >> "$REPORT_FILE"
                echo "- **任务ID**: \`$task_id\`" >> "$REPORT_FILE"
                echo "- **连续错误**: $errors 次" >> "$REPORT_FILE"
                echo "- **错误信息**: $error_detail" >> "$REPORT_FILE"
                echo "- **建议操作**: 运行 \`openclaw models auth login --provider qwen-portal\`" >> "$REPORT_FILE"
                echo >> "$REPORT_FILE"
            fi
        done
    fi
    
    # 添加建议操作
    cat >> "$REPORT_FILE" << EOF
## 🛠️ 建议操作

### 情况1: 有错误任务
1. 获取 OAuth 链接: \`~/.openclaw/get-qwen-oauth-link.sh\`
2. 在浏览器中完成授权
3. 验证修复: \`openclaw cron run <任务ID>\`
4. 检查结果: \`openclaw cron runs --id <任务ID>\`

### 情况2: 只有警告任务
1. 监控连续错误次数
2. 准备 OAuth 重新登录
3. 考虑预防性刷新认证

### 情况3: 全部正常
1. 继续保持每周检查
2. 记录认证持续时间
3. 更新 qwen-portal 过期频率数据

## 📋 维护检查清单

- [ ] 检查所有使用 qwen-portal 的任务状态
- [ ] 分析错误任务的详细错误信息
- [ ] 准备 OAuth 重新登录（如果需要）
- [ ] 验证修复后的任务状态
- [ ] 更新维护记录

## 🔗 相关资源

1. **OAuth 链接获取**: \`~/.openclaw/get-qwen-oauth-link.sh\`
2. **认证管理指南**: \`~/openclaw/workspace/MODEL_AUTH_MANAGEMENT.md\`
3. **快速参考**: \`~/openclaw/workspace/QWEN_PORTAL_QUICK_REFERENCE.md\`
4. **学习记录**: \`~/openclaw/workspace/.learnings/LEARNINGS.md\`

---

**下次检查建议**: $(date -v +${CHECK_INTERVAL_DAYS}d '+%Y-%m-%d')
**备注**: qwen-portal OAuth 通常每1-2周过期，建议每周检查一次。

EOF
    
    log "报告已生成: $REPORT_FILE" "SUCCESS"
}

# 主函数
main() {
    log "开始 qwen-portal 认证状态检查"
    
    # 检查 openclaw 命令
    if ! command -v openclaw &> /dev/null; then
        log "错误: openclaw 命令未找到" "ERROR"
        exit 1
    fi
    
    # 检查 cron 任务状态
    log "步骤1: 检查 cron 任务状态"
    local task_status=$(check_cron_tasks)
    local error_count=$(echo "$task_status" | cut -d'|' -f1)
    local warning_count=$(echo "$task_status" | cut -d'|' -f2)
    
    # 显示摘要
    echo
    echo "📊 检查摘要:"
    echo "================"
    echo -e "错误任务: ${RED}$error_count${NC} 个"
    echo -e "警告任务: ${YELLOW}$warning_count${NC} 个"
    echo "================"
    echo
    
    # 生成详细报告
    generate_report "$error_count" "$warning_count"
    
    # 显示报告位置
    echo -e "${GREEN}✅ 检查完成${NC}"
    echo "日志文件: $LOG_FILE"
    echo "详细报告: $REPORT_FILE"
    echo
    
    # 根据检查结果提供建议
    if [ "$error_count" -gt 0 ]; then
        echo -e "${RED}⚠️  需要立即处理${NC}"
        echo "有 $error_count 个任务处于错误状态"
        echo "建议运行: ~/.openclaw/get-qwen-oauth-link.sh"
    elif [ "$warning_count" -gt 0 ]; then
        echo -e "${YELLOW}📋 需要关注${NC}"
        echo "有 $warning_count 个任务接近预警阈值"
        echo "建议准备 OAuth 重新登录"
    else
        echo -e "${GREEN}🎉 全部正常${NC}"
        echo "所有使用 qwen-portal 的任务状态正常"
        echo "建议继续保持每周检查"
    fi
    
    log "检查完成" "SUCCESS"
}

# 显示帮助
show_help() {
    echo "使用: $0 [选项]"
    echo
    echo "选项:"
    echo "  -h, --help     显示此帮助信息"
    echo "  -d, --days N   设置检查间隔天数（默认: 7）"
    echo "  -t, --threshold N 设置预警阈值（默认: 3）"
    echo
    echo "示例:"
    echo "  $0             默认检查（每周一次，阈值3）"
    echo "  $0 -d 3 -t 2   每3天检查，阈值2次错误"
    echo
    echo "基于 2026-03-09 qwen-portal OAuth 实战经验"
    echo "建议添加到每周 cron 任务:"
    echo "  0 9 * * 1 $HOME/.openclaw/check-qwen-auth.sh"
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--days)
            CHECK_INTERVAL_DAYS="$2"
            shift 2
            ;;
        -t|--threshold)
            WARNING_THRESHOLD="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            show_help
            exit 1
            ;;
    esac
done

# 运行主函数
main "$@"

echo
echo "📝 下次检查建议: $(date -v +${CHECK_INTERVAL_DAYS}d '+%Y-%m-%d %H:%M')"