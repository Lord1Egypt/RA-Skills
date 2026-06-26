#!/bin/bash
# WorkTracker 基础使用示例

echo "=== WorkTracker 基础使用示例 ==="
echo ""

# 1. 开始工作
echo "1. 开始工作："
echo "worktracker start \"小新\" \"修复系统问题\" \"今天完成\""
worktracker start "小新" "修复系统问题" "今天完成"
echo ""

# 等待2秒
sleep 2

# 2. 更新进展
echo "2. 更新进展："
echo "worktracker update \"小新\" 50 \"已找到问题原因，正在修复\""
worktracker update "小新" 50 "已找到问题原因，正在修复"
echo ""

# 等待2秒
sleep 2

# 3. 完成工作
echo "3. 完成工作："
echo "worktracker complete \"小新\" \"成功修复系统问题\" \"需要测试其他功能\""
worktracker complete "小新" "成功修复系统问题" "需要测试其他功能"
echo ""

# 4. 查看状态
echo "4. 查看状态："
echo "worktracker status"
worktracker status
echo ""

# 5. 查看日志
echo "5. 查看日志："
echo "worktracker log --limit 3"
worktracker log --limit 3
echo ""

echo "=== 示例完成 ==="