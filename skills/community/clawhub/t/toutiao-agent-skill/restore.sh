#!/bin/bash
# 头条号技能包恢复脚本
# 功能：复制知识库和记忆文件到工作区
# 安全说明：仅复制文件，不执行任何网络请求或权限提升操作

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$HOME/openclaw/workspace"

echo "🔧 开始恢复头条号技能包..."
echo "📁 源目录：$SCRIPT_DIR"
echo "📁 目标目录：$WORKSPACE_DIR"

# 复制知识库文件
if [ -d "$SCRIPT_DIR/knowledge" ]; then
    echo "📚 复制知识库文件..."
    cp -r "$SCRIPT_DIR/knowledge/"* "$WORKSPACE_DIR/knowledge/" 2>/dev/null || mkdir -p "$WORKSPACE_DIR/knowledge" && cp -r "$SCRIPT_DIR/knowledge/"* "$WORKSPACE_DIR/knowledge/"
    echo "✅ 知识库文件复制完成"
fi

# 复制记忆文件示例
if [ -d "$SCRIPT_DIR/memory" ]; then
    echo "📝 复制记忆文件示例..."
    cp -r "$SCRIPT_DIR/memory/"* "$WORKSPACE_DIR/memory/" 2>/dev/null || mkdir -p "$WORKSPACE_DIR/memory" && cp -r "$SCRIPT_DIR/memory/"* "$WORKSPACE_DIR/memory/"
    echo "✅ 记忆文件复制完成"
fi

# 复制临时文件示例
if [ -d "$SCRIPT_DIR/temp" ]; then
    echo "📄 复制内容模板..."
    cp -r "$SCRIPT_DIR/temp/"* "$WORKSPACE_DIR/temp/" 2>/dev/null || mkdir -p "$WORKSPACE_DIR/temp" && cp -r "$SCRIPT_DIR/temp/"* "$WORKSPACE_DIR/temp/"
    echo "✅ 内容模板复制完成"
fi

echo ""
echo "🎉 恢复完成！"
echo ""
echo "下一步："
echo "1. 打开头条号后台：https://mp.toutiao.com"
echo "2. 登录你的头条号账号"
echo "3. 技能会自动检测登录状态并发布内容"
echo ""
echo "发布时间："
echo "  - 06:15 早市菜价"
echo "  - 11:15 观点微头条"
echo "  - 15:45 日常笔记"
echo "  - 20:00 活动话题"
echo ""
