#!/bin/bash
# 安装 wechat-formatter 技能

echo "📦 正在安装 wechat-formatter..."

# 复制文件
mkdir -p ~/.openclaw/skills/wechat-formatter
cp wechat_formatter.py ~/.openclaw/skills/wechat-formatter/
cp SKILL.md ~/.openclaw/skills/wechat-formatter/

chmod +x ~/.openclaw/skills/wechat-formatter/wechat_formatter.py

# 创建符号链接到 ~/.openclaw/bin（如果存在）
if [ -d ~/.openclaw/bin ]; then
    ln -sf ~/.openclaw/skills/wechat-formatter/wechat_formatter.py ~/.openclaw/bin/wechat-formatter
    echo "✅ 已创建命令: wechat-formatter"
fi

echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  wechat-formatter article.md"
echo "  cat article.md | wechat-formatter --stdin"