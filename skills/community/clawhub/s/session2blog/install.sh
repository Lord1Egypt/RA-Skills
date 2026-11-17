#!/bin/bash
# Session2Blog 安装脚本
# 把 skill 安装到 ~/.openclaw/skills/session2blog/

set -euo pipefail

echo "=== Session2Blog 安装 ==="

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/skills}"
TARGET="$SKILLS_DIR/session2blog"

mkdir -p "$SKILLS_DIR"

# 复制 skill 文件
echo "  复制 SKILL.md, s2b.sh ..."
mkdir -p "$TARGET"
cp "$SCRIPT_DIR/SKILL.md" "$TARGET/"
cp "$SCRIPT_DIR/s2b.sh" "$TARGET/"
chmod +x "$TARGET/s2b.sh"

# 运行时目录
S2B_DIR="$HOME/.openclaw/session2blog"
mkdir -p "$S2B_DIR/articles" "$S2B_DIR/logs"

# 创建配置文件（如果不存在）
# 注意: 配置文件直接在 S2B_DIR 下, 即 ~/.openclaw/session2blog/config.yaml
if [ ! -f "$S2B_DIR/config.yaml" ]; then
  cat > "$S2B_DIR/config.yaml" << 'EOF'
default_template: auto      # auto | tech-review | learning-notes | troubleshooting
default_platform: none      # none | wechat | juejin | csdn | zhihu | all
language: zh-CN
author: ""
articles_dir: ~/.openclaw/session2blog/articles

# === 发布平台 Cookie（Pro 版功能）===
# 仅本地保存, 权限 600, 不会随 skill 包发出。
# 获取方式: 浏览器登录对应平台 → 开发者工具 → Network/Storage 复制 Cookie 整串
# 例: juejin_cookie: "sessionid=xxx; sid_tt=yyy; ..."
# 当前已实现: juejin (发草稿)。微信/CSDN/知乎待后续更新。
juejin_cookie:
EOF
  chmod 600 "$S2B_DIR/config.yaml"
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "  已安装到: $TARGET"
echo "  运行时目录: $S2B_DIR"
echo ""
echo "  下一步:"
echo "    1. 重启 OpenClaw 会话（或新开一个）"
echo "    2. 在会话中输入: /s2b"
echo "    3. 博文会保存到: $S2B_DIR/articles/"
echo ""
echo "  其他命令:"
echo "    /s2b --list                 # 列出可用会话"
echo "    /s2b -n 3                   # 处理第 3 个会话"
echo "    /s2b --template learning-notes  # 指定模板"
