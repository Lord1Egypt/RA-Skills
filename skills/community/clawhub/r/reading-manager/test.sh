#!/bin/bash
# 阅读管家测试脚本

echo "=== 阅读管家功能测试 ==="
echo ""

echo "1. 添加书籍"
reading book add --title "算法导论" --author "Thomas Cormen" --pages 1300
reading book add --title "设计模式" --author "GoF" --pages 400

echo ""
echo "2. 列出书籍"
reading book list

echo ""
echo "3. 更新阅读进度"
reading progress update 1 --page 200 --minutes 60

echo ""
echo "4. 添加笔记"
reading note add 1 --content "分治策略的核心思想" --page 50 --tags "algorithm,important"

echo ""
echo "5. 创建书单"
reading list create "计算机经典" --description "计算机科学经典书籍"
reading list add-book "计算机经典" 1
reading list add-book "计算机经典" 2

echo ""
echo "6. 设置年度目标"
reading goal set-yearly 24

echo ""
echo "7. 查看统计"
reading report stats

echo ""
echo "=== 测试完成 ==="
