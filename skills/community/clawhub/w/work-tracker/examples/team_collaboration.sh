#!/bin/bash
# WorkTracker 团队协作示例

echo "=== WorkTracker 团队协作示例 ==="
echo ""

# 模拟团队协作场景
echo "场景：四助手团队协作完成一个项目"
echo ""

# 小新：项目协调
echo "小新开始项目协调工作："
worktracker start "小新" "协调四助手团队完成市场分析项目" "本周五完成"
echo ""

sleep 1

# 小雅：市场分析
echo "小雅开始市场分析工作："
worktracker start "小雅" "完成竞品分析和市场趋势报告" "明天完成"
echo ""

sleep 1

# 小锐：销售数据
echo "小锐开始销售数据分析："
worktracker start "小锐" "整理Q1销售数据并分析" "今天完成"
echo ""

sleep 1

# 小暖：客户反馈
echo "小暖开始客户反馈收集："
worktracker start "小暖" "收集客户反馈并整理报告" "今天完成"
echo ""

sleep 2

# 更新进展
echo "=== 工作进展更新 ==="
echo ""

echo "小雅更新市场分析进展："
worktracker update "小雅" 60 "已完成3个竞品分析，正在整理市场趋势"
echo ""

echo "小锐更新销售数据分析进展："
worktracker update "小锐" 80 "已完成数据整理，正在生成分析报告"
echo ""

echo "小暖更新客户反馈进展："
worktracker update "小暖" 40 "已收集50份客户反馈，正在分类整理"
echo ""

sleep 2

# 完成部分工作
echo "=== 部分工作完成 ==="
echo ""

echo "小锐完成销售数据分析："
worktracker complete "小锐" "完成Q1销售数据分析报告，发现3个增长机会" "需要与市场团队讨论"
echo ""

sleep 2

# 查看团队状态
echo "=== 团队当前状态 ==="
echo ""
worktracker status
echo ""

# 查看工作日志
echo "=== 最近工作日志 ==="
echo ""
worktracker log --limit 5
echo ""

echo "=== 团队协作示例完成 ==="
echo ""
echo "通过这个示例，可以看到："
echo "1. 各助手工作状态清晰可见"
echo "2. 工作进展实时更新"
echo "3. 工作完成有完整记录"
echo "4. 团队协作透明度高"