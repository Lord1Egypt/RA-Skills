#!/bin/bash

# Token Tracker 智能推荐示例脚本

echo "=========================================="
echo "  🧠 Token Tracker 智能推荐示例"
echo "=========================================="
echo ""

# 示例 1: 查看模型分析报告
echo "1️⃣  查看模型分析报告"
echo "------------------------------------------"
cd /home/seelong/.openclaw/skills/token-tracker
npm run token:models
echo ""

# 示例 2: 推荐100 tokens的简单任务
echo "2️⃣  推荐100 tokens的简单任务"
echo "------------------------------------------"
npm run token:recommend 100
echo ""

# 示例 3: 推荐500 tokens的代码生成
echo "3️⃣  推荐500 tokens的代码生成"
echo "------------------------------------------"
npm run token:recommend 500 code-generation
echo ""

# 示例 4: 推荐1000 tokens的数据分析
echo "4️⃣  推荐1000 tokens的数据分析"
echo "------------------------------------------"
npm run token:recommend 1000 data-analysis
echo ""

# 示例 5: 分析成本优化
echo "5️⃣  分析成本优化"
echo "------------------------------------------"
npm run token:optimize
echo ""

# 示例 6: 查看不同场景的推荐
echo "6️⃣  不同场景的推荐"
echo "------------------------------------------"
echo "简单查询:"
npm run token:recommend 200 simple-query
echo ""
echo "翻译任务:"
npm run token:recommend 300 translation
echo ""
echo "复杂推理:"
npm run token:recommend 5000 complex-reasoning
echo ""

# 示例 7: 查看交互式菜单
echo "7️⃣  启动交互式菜单"
echo "------------------------------------------"
echo "运行命令: npm run token:i"
echo "然后选择 10 (模型分析)、11 (模型推荐) 或 12 (成本优化)"
echo ""

# 示例 8: 导出报告
echo "8️⃣  导出报告"
echo "------------------------------------------"
echo "运行命令:"
echo "  npm run token:models > model-analysis.txt"
echo "  npm run token:optimize > cost-optimization.txt"
echo ""

echo "=========================================="
echo "  ✅ 示例完成"
echo "=========================================="
echo ""
echo "💡 提示:"
echo "  - 定期查看模型分析报告"
echo "  - 根据任务类型选择合适的模型"
echo "  - 使用成本优化功能跟踪节省效果"
echo "  - 通过交互式菜单更方便地探索功能"
echo ""
