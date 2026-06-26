#!/bin/bash
# 安装脚本

echo "安装微信公众号草稿删除工具..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要Python3"
    exit 1
fi

# 安装依赖
echo "安装Python依赖..."
pip3 install requests --quiet

# 设置执行权限
chmod +x scripts/delete_drafts.py

# 创建符号链接
echo "创建命令行工具..."
ln -sf "$(pwd)/scripts/delete_drafts.py" /usr/local/bin/wechat-draft-delete 2>/dev/null || true

echo "✅ 安装完成！"
echo ""
echo "使用方法："
echo "1. 设置环境变量："
echo "   export WECHAT_APP_ID='你的AppID'"
echo "   export WECHAT_APP_SECRET='你的AppSecret'"
echo ""
echo "2. 删除单个草稿："
echo "   wechat-draft-delete --media-id 'DgrVBScHsvTZOSzU4Wcna...'"
echo ""
echo "3. 批量删除："
echo "   wechat-draft-delete --media-ids 'id1,id2,id3'"
echo ""
echo "4. 从文件删除："
echo "   wechat-draft-delete --file media_ids.txt"