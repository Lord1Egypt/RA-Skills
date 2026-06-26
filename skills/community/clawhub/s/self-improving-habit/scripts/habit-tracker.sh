#!/bin/bash
# 习惯追踪脚本
# 帮助用户追踪习惯养成进展

if [ $# -lt 1 ]; then
    echo "用法: $0 <习惯名称> [完成状态]"
    echo "示例: $0 晨间冥想 yes"
    echo "示例: $0 晨间冥想 no"
    echo "示例: $0 晨间冥想 (查看状态)"
    exit 1
fi

HABIT_NAME="$1"
STATUS="${2:-check}"
HABIT_FILE=".learnings/habits/${HABIT_NAME}.md"
DATE=$(date +%Y-%m-%d)

# 创建习惯文件（如果不存在）
if [ ! -f "$HABIT_FILE" ]; then
    mkdir -p "$(dirname "$HABIT_FILE")"
    cat > "$HABIT_FILE" << EOF
# 习惯追踪: $HABIT_NAME

**开始日期**: $(date +%Y-%m-%d)
**目标频率**: [填写]
**当前阶段**: 启动期

## 每日记录

EOF
    echo "✅ 创建新习惯文件: $HABIT_FILE"
    echo "📝 请编辑文件填写习惯详细信息"
fi

case $STATUS in
    "yes"|"y"|"完成")
        # 记录完成
        if grep -q "### $DATE" "$HABIT_FILE"; then
            echo "⚠️  今天已经记录过此习惯"
        else
            cat >> "$HABIT_FILE" << EOF
### $DATE ✅
- **完成时间**: $(date +%H:%M)
- **质量评分**: [1-10]
- **备注**: [填写]

EOF
            echo "✅ 记录习惯完成: $HABIT_NAME"
            
            # 计算连续天数
            streak=1
            prev_date=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d "yesterday" +%Y-%m-%d)
            while grep -q "### $prev_date ✅" "$HABIT_FILE"; do
                ((streak++))
                prev_date=$(date -v-${streak}d +%Y-%m-%d 2>/dev/null || date -d "$streak days ago" +%Y-%m-%d)
            done
            
            echo "🔥 连续完成: $streak 天"
        fi
        ;;
    
    "no"|"n"|"未完成")
        # 记录未完成
        if grep -q "### $DATE" "$HABIT_FILE"; then
            echo "⚠️  今天已经记录过此习惯"
        else
            cat >> "$HABIT_FILE" << EOF
### $DATE ❌
- **原因**: [填写]
- **计划**: [明天如何改进]
- **备注**: [填写]

EOF
            echo "❌ 记录习惯未完成: $HABIT_NAME"
            echo "💡 分析原因并制定改进计划"
        fi
        ;;
    
    "check"|"状态")
        # 检查状态
        echo "📊 习惯状态: $HABIT_NAME"
        echo "========================="
        
        if [ ! -f "$HABIT_FILE" ]; then
            echo "习惯文件不存在"
            exit 1
        fi
        
        # 计算统计数据
        total_days=$(grep -c "### 2" "$HABIT_FILE" || echo "0")
        completed_days=$(grep -c "✅" "$HABIT_FILE")
        completion_rate=0
        if [ "$total_days" -gt 0 ]; then
            completion_rate=$((completed_days * 100 / total_days))
        fi
        
        # 查找最后记录
        last_entry=$(grep "### 2" "$HABIT_FILE" | tail -1)
        
        # 计算连续天数
        streak=0
        current_date=$(date +%Y-%m-%d)
        check_date="$current_date"
        
        while grep -q "### $check_date ✅" "$HABIT_FILE"; do
            ((streak++))
            check_date=$(date -v-${streak}d +%Y-%m-%d 2>/dev/null || date -d "$streak days ago" +%Y-%m-%d)
        done
        
        echo ""
        echo "📈 统计数据:"
        echo "  • 总记录天数: $total_days"
        echo "  • 完成天数: $completed_days"
        echo "  • 完成率: $completion_rate%"
        echo "  • 当前连续: $streak 天"
        echo ""
        
        if [ -n "$last_entry" ]; then
            echo "📝 最后记录: $last_entry"
        fi
        
        # 阶段建议
        if [ "$streak" -ge 7 ]; then
            echo "🎉 阶段: 巩固期 (坚持7天以上)"
            echo "建议: 关注习惯质量，尝试增加难度"
        elif [ "$streak" -ge 1 ]; then
            echo "🌱 阶段: 启动期 (正在建立)"
            echo "建议: 保持连续性，建立触发机制"
        else
            echo "🌱 阶段: 开始期"
            echo "建议: 从今天开始，建立第一个记录"
        fi
        ;;
    
    *)
        echo "错误: 未知状态 '$STATUS'"
        echo "可用状态: yes, no, check"
        exit 1
        ;;
esac

echo ""
echo "📖 详细记录查看: $HABIT_FILE"
echo "🚀 使用 self-improving-habit 获取科学习惯养成指导。"