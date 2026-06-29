#!/usr/bin/env bash
# fix-caffeinate.sh —— 修坑 3：加 caffeinate 防闲置睡眠
# 把 launchd plist 的 ProgramArguments 包一层 caffeinate -i
set -euo pipefail

PLIST=~/Library/LaunchAgents/com.wechat-claude-code.bridge.plist

if [ ! -f "$PLIST" ]; then
  echo "❌ 没找到 launchd plist。先跑 install.sh + 起 daemon"
  exit 1
fi

echo "🔧 修坑 3：加 caffeinate -i 防闲置睡眠"

# 备份
BAK="${PLIST}.bak.$(date +%Y%m%d-%H%M%S)"
cp "$PLIST" "$BAK"
echo "   备份: $BAK"

python3 <<PY
import plistlib, os
p = os.path.expanduser("$PLIST")
with open(p, 'rb') as f: d = plistlib.load(f)

if d['ProgramArguments'][0] == '/usr/bin/caffeinate':
    print("   ✅ 已经包过 caffeinate，跳过")
else:
    d['ProgramArguments'] = ['/usr/bin/caffeinate', '-i', '--', *d['ProgramArguments']]
    with open(p, 'wb') as f: plistlib.dump(d, f)
    print("   ✅ 已加 caffeinate -i")
    print("      命令: ", d['ProgramArguments'])
PY

# 重新加载
echo ""
echo "   重新加载 launchd..."
launchctl unload "$PLIST" 2>/dev/null || true
sleep 1
launchctl load "$PLIST"
sleep 2

# 验证
if launchctl list | grep -q "com.wechat-claude-code.bridge"; then
  echo "   ✅ daemon 已重启"
  if pgrep -f "caffeinate.*wechat-claude-code" >/dev/null; then
    echo "   ✅ caffeinate 进程在跑"
  fi
fi

echo ""
echo "   说明："
echo "   - -i 阻止系统闲置睡眠（不动键鼠也不睡）"
echo "   - 屏幕黑屏 daemon 还在跑"
echo "   - 手动合盖还是会睡（要合盖也不睡换 -id，注意发热）"
echo "   - 拔电源默认还是会睡（macOS 电源策略）"
