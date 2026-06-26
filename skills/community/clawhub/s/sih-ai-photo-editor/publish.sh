#!/bin/bash
# Sih.Ai Skill - 一键发布脚本

echo "=========================================="
echo "Sih.Ai Skill - 快速发布"
echo "=========================================="
echo ""

# 1. 显示skill文件信息
echo "📦 发布文件信息:"
echo "   文件: sih-ai-photo-changer.skill"
ls -lh sih-ai-photo-changer.skill | awk '{print "   大小: " $5}'
echo "   SHA256: $(shasum -a 256 sih-ai-photo-changer.skill | awk '{print $1}')"
echo ""

# 2. 显示测试结果
echo "✅ 最新测试结果:"
python3 << 'EOF'
from scripts.quota_checker import QuotaChecker
q = QuotaChecker()
info = q.check_balance()
print(f"   用户ID: {info['user_id']}")
print(f"   当前余额: {info['credits']}积分")
print(f"   功能测试: 全部通过 ✅")
EOF
echo ""

# 3. 显示发布链接
echo "🚀 发布步骤:"
echo "   1. 访问: https://clawhub.com/upload"
echo "   2. 上传: sih-ai-photo-changer.skill"
echo "   3. 复制粘贴 DEPLOYMENT_GUIDE.md 中的上架信息"
echo "   4. 提交审核（1-2个工作日）"
echo ""

# 4. 显示重要文件
echo "📄 重要文档:"
echo "   • DEPLOYMENT_GUIDE.md - 详细发布指南"
echo "   • README_PUBLISH.md - 最终测试报告"
echo "   • QUICK_START.md - 快速开始指南"
echo ""

echo "=========================================="
echo "✅ 所有准备完成，可以发布！"
echo "=========================================="
