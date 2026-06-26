#!/bin/bash
# wechat-push-skill installer
#
# 装上后就能用：
#   ~/.openclaw/skills/wechat-push-skill/bin/wechat-push "消息"
#   ~/.openclaw/skills/wechat-push-skill/bin/wechat-push-verify
#
# 同时把可执行文件链接到 ~/.local/bin/（如果该目录在 PATH 里）

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/wechat-push"
CONFIG_FILE="${CONFIG_DIR}/config"
LOCAL_BIN="$HOME/.local/bin"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}========================================"
echo "  微信主动推送 skill 安装"
echo "========================================${NC}"
echo ""

# 1. 检查 openclaw
echo -e "${BLUE}1. 检查 openclaw CLI${NC}"
if ! command -v openclaw >/dev/null 2>&1; then
    echo -e "${RED}❌ openclaw 不在 PATH${NC}"
    echo "  请先安装 OpenClaw: npm i -g openclaw"
    exit 1
fi
echo -e "  ${GREEN}✅ openclaw: $(which openclaw)${NC}"

# 2. 检查微信插件账号
echo ""
echo -e "${BLUE}2. 检查 OpenClaw 微信插件${NC}"
ACCOUNTS_DIR="$HOME/.openclaw/openclaw-weixin/accounts"
if [ ! -d "$ACCOUNTS_DIR" ]; then
    echo -e "${RED}❌ 微信插件账号目录不存在：$ACCOUNTS_DIR${NC}"
    echo "  请先在 OpenClaw 微信插件完成首次扫码绑定"
    echo "  详见: http://127.0.0.1:18888/dashboard"
    exit 1
fi
BOT_COUNT=$(find "$ACCOUNTS_DIR" -maxdepth 1 -name "*@im.bot.json" -not -name "*-*" 2>/dev/null | wc -l | tr -d ' ')
if [ "$BOT_COUNT" -eq 0 ]; then
    echo -e "${RED}❌ 没找到任何 bot 账号${NC}"
    echo "  请先扫码绑定 OpenClaw 微信插件"
    exit 1
fi
echo -e "  ${GREEN}✅ 找到 $BOT_COUNT 个 bot 账号${NC}"

# 3. 探测活跃账号（仅看 sync.json mtime 作初步判断）
echo ""
echo -e "${BLUE}3. 探测活跃 bot 账号（初步）${NC}"
ACTIVE_BOT=$(python3 "${SKILL_DIR}/lib/wechat_push.py" --detect-account)
echo -e "  初步探测：${GREEN}$ACTIVE_BOT${NC}"
echo "  （最终推荐账号会在配置 openid 后重新探测）"

# 4. 引导 openid 配置
echo ""
echo -e "${BLUE}4. 配置 openid${NC}"
mkdir -p "$CONFIG_DIR"

if [ -f "$CONFIG_FILE" ] && grep -q "^openid=" "$CONFIG_FILE"; then
    EXISTING=$(grep "^openid=" "$CONFIG_FILE" | cut -d= -f2)
    echo -e "  已有配置：$EXISTING"
    read -p "  复用现有配置? [Y/n] " -n 1 -r REPLY
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]] && [ -n "$REPLY" ]; then
        rm -f "$CONFIG_FILE"
    fi
fi

if [ ! -f "$CONFIG_FILE" ]; then
    cp "${SKILL_DIR}/templates/config.example" "$CONFIG_FILE"
    chmod 600 "$CONFIG_FILE"
    echo ""
    echo "  配置文件已创建：$CONFIG_FILE"
    echo "  请编辑填入你的 openid（问 OpenClaw 微信插件拿）"
    echo ""
    read -p "  现在就编辑? [Y/n] " -n 1 -r REPLY
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        ${EDITOR:-nano} "$CONFIG_FILE"
    fi
fi

# 配置里有 openid/account，权限收紧到仅当前用户可读写
chmod 600 "$CONFIG_FILE"

# 验证配置
if grep -q "^openid=" "$CONFIG_FILE"; then
    OPENID=$(grep "^openid=" "$CONFIG_FILE" | cut -d= -f2)
    # 拒接占位符 + 空值
    if [ -z "$OPENID" ] || [[ "$OPENID" == *"<"*">"* ]]; then
        echo -e "  ${RED}❌ openid 是占位符或空值：$OPENID${NC}"
        echo "  请打开 $CONFIG_FILE 填入你的真实 openid"
        echo "  形如 oXXXXXXXXXXXXXXXXX@im.wechat"
        exit 1
    fi
    echo -e "  ${GREEN}✅ openid：$OPENID${NC}"
else
    echo -e "  ${RED}❌ 配置文件缺少 openid${NC}"
    exit 1
fi

# 默认推荐：只配置 openid，不写死 account；每次发送前按 openid 动态匹配 bot。
if grep -q "^account=" "$CONFIG_FILE"; then
    EXISTING_ACCOUNT=$(grep "^account=" "$CONFIG_FILE" | cut -d= -f2)
    echo ""
    echo -e "  ${YELLOW}⚠️ 当前 config 写死了 account=$EXISTING_ACCOUNT${NC}"
    echo "  这会跳过每次发送前的动态账号选择。"
    read -p "  是否移除 account=，改为运行时动态选择？[Y/n] " -n 1 -r REPLY
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        sed -i.bak '/^account=/d' "$CONFIG_FILE"
        echo -e "  ${GREEN}✅ 已移除 account=，之后会每次发送前自动选择 bot${NC}"
    fi
fi

# 4.5. 重探测活跃账号（按 openid 查 context_token，能选对 bot）
echo ""
echo -e "${BLUE}4.5 重探测活跃账号（按 openid 查 context_token）${NC}"
ACTIVE_BOT=$(python3 "${SKILL_DIR}/lib/wechat_push.py" --detect-account --to "$OPENID")
if [ -n "$ACTIVE_BOT" ]; then
    echo -e "  本次动态探测结果：${GREEN}$ACTIVE_BOT${NC}"
    CT_FILE="$HOME/.openclaw/openclaw-weixin/accounts/${ACTIVE_BOT}.context-tokens.json"
    if [ -f "$CT_FILE" ] && grep -q "$OPENID" "$CT_FILE" 2>/dev/null; then
        echo -e "  ${GREEN}✅ 跟你有 context；之后每次发送前都会按 openid 重新选择 bot${NC}"
    else
        echo -e "  ${YELLOW}⚠️ 探测到的是 sync mtime 最高的，不一定跟你有 context${NC}"
        echo "  建议：先发一条消息给 bot 建立 context，然后重跑 install.sh"
    fi
fi

# 5. 链接到 ~/.local/bin
echo ""
echo -e "${BLUE}5. 链接到 ~/.local/bin/${NC}"
mkdir -p "$LOCAL_BIN"
for cmd in wechat-push wechat-push-verify wechat-push-doctor; do
    ln -sf "${SKILL_DIR}/bin/${cmd}" "${LOCAL_BIN}/${cmd}"
    echo -e "  ${GREEN}✅ ${LOCAL_BIN}/${cmd}${NC}"
done

# 检查 PATH
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    echo ""
    echo -e "  ${YELLOW}⚠️ $LOCAL_BIN 不在 PATH 里${NC}"
    echo "  加这一行到 ~/.zshrc 或 ~/.bashrc:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# 6. 验证
echo ""
echo -e "${BLUE}6. 跑一次 verify 验证链路${NC}"
"${SKILL_DIR}/bin/wechat-push-verify"

echo ""
echo -e "${BLUE}7. 可选：发送一条非 silent 测试消息${NC}"
echo "  最终成功标准：你的手机微信实际收到这条消息"
read -p "  现在发送可见测试消息？[Y/n] " -n 1 -r REPLY
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    "${SKILL_DIR}/bin/wechat-push" "wechat-push-skill install test"
fi

echo ""
echo -e "${GREEN}========================================"
echo "  安装完成！"
echo "========================================${NC}"
echo ""
echo "  用法："
echo "    wechat-push \"你好\"           # 推消息"
echo "    wechat-push-verify            # 链路自检"
echo "    wechat-push-doctor            # 故障排查"
echo ""
