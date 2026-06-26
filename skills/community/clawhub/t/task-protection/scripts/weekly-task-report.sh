#!/bin/bash
# 任务周报统计脚本
# 每周日 23:00 执行，统计本周任务执行情况

source /home/admin/.openclaw/workspace/scripts/task-utils.sh

WORKSPACE="/home/admin/.openclaw/workspace"
REPORT_FILE="$WORKSPACE/articles/任务周报-$(date +%Y-W%V).md"
TASKS_DIR="$WORKSPACE/memory/tasks"
REGISTRY="$WORKSPACE/memory/task-registry.json"

echo "📊 生成任务周报..."
echo "=================="

# 统计本周任务
TOTAL_TASKS=0
SUCCESS_TASKS=0
FAILED_TASKS=0
TOTAL_DURATION=0

# 遍历所有任务状态文件
for state_file in "$TASKS_DIR"/*.json; do
    if [ -f "$state_file" ]; then
        ((TOTAL_TASKS++))
        
        status=$(jq -r '.status' "$state_file")
        if [ "$status" == "success" ]; then
            ((SUCCESS_TASKS++))
            duration=$(jq -r '.duration // 0' "$state_file")
            TOTAL_DURATION=$((TOTAL_DURATION + duration))
        elif [ "$status" == "failed" ]; then
            ((FAILED_TASKS++))
        fi
    fi
done

# 计算成功率
if [ "$TOTAL_TASKS" -gt 0 ]; then
    SUCCESS_RATE=$((SUCCESS_TASKS * 100 / TOTAL_TASKS))
    AVG_DURATION=$((TOTAL_DURATION / (SUCCESS_TASKS > 0 ? SUCCESS_TASKS : 1)))
else
    SUCCESS_RATE=0
    AVG_DURATION=0
fi

# 生成报告
cat > "$REPORT_FILE" << EOF
# 📊 任务周报 - $(date +%Y)"年第%V周"

**生成时间**: $(date '+%Y-%m-%d %H:%M')  
**统计周期**: $(date -d 'last sunday' '+%Y-%m-%d') 至 $(date '+%Y-%m-%d')

---

## 📈 核心指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 任务总数 | $TOTAL_TASKS | 本周登记的任务总数 |
| 成功完成 | $SUCCESS_TASKS | 成功执行的任务 |
| 执行失败 | $FAILED_TASKS | 失败的任务 |
| **成功率** | **${SUCCESS_RATE}%** | 成功/总数 |
| 平均耗时 | ${AVG_DURATION}s | 成功任务平均执行时间 |

---

## 📋 任务分类统计

### 按优先级

| 优先级 | 数量 | 成功率 |
|--------|------|--------|
| 高优先级 | - | - |
| 中优先级 | - | - |
| 低优先级 | - | - |

### 按类型

| 类型 | 数量 | 说明 |
|------|------|------|
| 周期性任务 | - | 定时执行的任务 |
| 一次性任务 | - | Alfred 委托的任务 |
| 系统任务 | - | 系统维护类任务 |

---

## ⚠️ 失败任务分析

EOF

# 添加失败任务详情
if [ "$FAILED_TASKS" -gt 0 ]; then
    echo "### 失败列表" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    for state_file in "$TASKS_DIR"/*.json; do
        if [ -f "$state_file" ]; then
            status=$(jq -r '.status' "$state_file")
            if [ "$status" == "failed" ]; then
                task_name=$(jq -r '.name' "$state_file")
                errors=$(jq -r '.errors[] | "• \(.type): \(.message)"' "$state_file" 2>/dev/null)
                echo "**$task_name**:" >> "$REPORT_FILE"
                echo "$errors" >> "$REPORT_FILE"
                echo "" >> "$REPORT_FILE"
            fi
        fi
    done
else
    echo "✅ 本周无失败任务" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

---

## 🔍 故障类型分布

| 故障类型 | 次数 | 占比 |
|----------|------|------|
| command_not_found | - | - |
| authentication_failed | - | - |
| network_error | - | - |
| timeout | - | - |
| 其他 | - | - |

---

## 💡 改进建议

EOF

# 根据成功率给出建议
if [ "$SUCCESS_RATE" -ge 90 ]; then
    echo "✅ **系统运行稳定**，继续保持！" >> "$REPORT_FILE"
elif [ "$SUCCESS_RATE" -ge 70 ]; then
    echo "⚠️ **成功率有待提升**，建议：" >> "$REPORT_FILE"
    echo "1. 检查失败任务的根本原因" >> "$REPORT_FILE"
    echo "2. 优化重试机制" >> "$REPORT_FILE"
    echo "3. 加强监控告警" >> "$REPORT_FILE"
else
    echo "🚨 **成功率偏低**，需要立即改进：" >> "$REPORT_FILE"
    echo "1. 全面排查失败原因" >> "$REPORT_FILE"
    echo "2. 修复系统性问题" >> "$REPORT_FILE"
    echo "3. 考虑增加冗余方案" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

---

## 📅 下周计划

- [ ] 持续监控系统稳定性
- [ ] 优化失败率高的任务
- [ ] 根据需求新增必要任务

---

_报告生成者：虾球 🦐_  
_任务闭环管理系统 v1.0_
EOF

echo ""
echo "✅ 周报生成完成！"
echo ""
echo "📄 报告位置：$REPORT_FILE"
echo ""
echo "📊 核心数据:"
echo "   任务总数：$TOTAL_TASKS"
echo "   成功：$SUCCESS_TASKS"
echo "   失败：$FAILED_TASKS"
echo "   成功率：${SUCCESS_RATE}%"
echo "   平均耗时：${AVG_DURATION}s"
echo ""

# 更新注册表统计
if [ -f "$REGISTRY" ]; then
    TEMP_FILE=$(mktemp)
    jq --argjson total "$TOTAL_TASKS" --argjson success "$SUCCESS_TASKS" --argjson failed "$FAILED_TASKS" \
        '.stats.completedToday = $success | .stats.failedToday = $failed' \
        "$REGISTRY" > "$TEMP_FILE" && mv "$TEMP_FILE" "$REGISTRY"
    echo "✅ 注册表统计已更新"
fi
