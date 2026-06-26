#!/bin/bash
# openclaw-weixin-fix 安装脚本
# 修复 @tencent-weixin/openclaw-weixin@2.4.1 在 OpenClaw 2026.5.4+ 上的 bug

set -e

PLUGIN_DIR="$HOME/.openclaw/npm/node_modules/@tencent-weixin/openclaw-weixin"
CHANNEL_JS="$PLUGIN_DIR/dist/src/channel.js"
MONITOR_JS="$PLUGIN_DIR/dist/src/monitor/monitor.js"
API_JS="$PLUGIN_DIR/dist/src/api/api.js"

echo "🔧 openclaw-weixin-fix 安装中..."

# 检查插件是否存在
if [ ! -d "$PLUGIN_DIR" ]; then
    echo "❌ 未找到微信插件，请先安装："
    echo "   openclaw plugins install @tencent-weixin/openclaw-weixin"
    exit 1
fi

# 备份原文件
echo "📦 备份原文件..."
cp "$CHANNEL_JS" "$CHANNEL_JS.bak" 2>/dev/null || true
cp "$MONITOR_JS" "$MONITOR_JS.bak" 2>/dev/null || true
cp "$API_JS" "$API_JS.bak" 2>/dev/null || true

# 修复1: channel.js - 添加 channelRuntime 传递
echo "🔧 修复 channel.js..."
if ! grep -q "channelRuntime: ctx.channelRuntime" "$CHANNEL_JS"; then
    sed -i 's/setStatus: ctx.setStatus,$/setStatus: ctx.setStatus,\n                channelRuntime: ctx.channelRuntime,/' "$CHANNEL_JS"
    echo "   ✅ 已添加 channelRuntime 传递"
else
    echo "   ⏭️  已修复，跳过"
fi

# 修复2: monitor.js - 优先使用传入的 channelRuntime
echo "🔧 修复 monitor.js..."
if ! grep -q "opts.channelRuntime" "$MONITOR_JS"; then
    # 使用 python 进行复杂的文本替换
    python3 << 'PYTHON_SCRIPT'
import re

with open("$MONITOR_JS", "r") as f:
    content = f.read()

old_code = """    let channelRuntime;
    try {
        const pluginRuntime = await waitForWeixinRuntime();
        channelRuntime = pluginRuntime.channel;
        aLog.info(`Weixin runtime acquired, channelRuntime type: ${typeof channelRuntime}`);
    }
    catch (err) {
        aLog.error(`waitForWeixinRuntime() failed: ${String(err)}`);
        throw err;
    }"""

new_code = """    let channelRuntime;
    if (opts.channelRuntime) {
        channelRuntime = opts.channelRuntime;
        aLog.info(`Using provided channelRuntime from Gateway`);
    } else {
        try {
            const pluginRuntime = await waitForWeixinRuntime();
            channelRuntime = pluginRuntime.channel;
            aLog.info(`Weixin runtime acquired, channelRuntime type: ${typeof channelRuntime}`);
        }
        catch (err) {
            aLog.error(`waitForWeixinRuntime() failed: ${String(err)}`);
            throw err;
        }
    }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("$MONITOR_JS", "w") as f:
        f.write(content)
    print("   ✅ 已添加 channelRuntime 优先逻辑")
else:
    print("   ⏭️  已修复或代码不匹配，跳过")
PYTHON_SCRIPT
else
    echo "   ⏭️  已修复，跳过"
fi

# 修复3: api.js - 删除 Content-Length 头
echo "🔧 修复 api.js..."
if grep -q "Content-Length" "$API_JS"; then
    sed -i '/Content-Length/d' "$API_JS"
    echo "   ✅ 已删除 Content-Length 头"
else
    echo "   ⏭️  已修复，跳过"
fi

echo ""
echo "✅ 修复完成！"
echo "请重启 Gateway：openclaw gateway restart"
