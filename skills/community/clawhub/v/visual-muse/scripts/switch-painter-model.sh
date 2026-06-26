#!/bin/bash
# 宿主机快捷入口：切换 painter 模型并重启
# 用法: bash ~/openclaw/switch-painter-model.sh gemini

if [ -z "$1" ]; then
  echo "用法: bash ~/openclaw/switch-painter-model.sh [模型名]"
  echo "可用模型: gemini gemini-pro gemini-lite gpt gpt-nano gpt-pro claude claude-haiku cheap best"
  exit 0
fi

echo "切换 painter 模型到: $1"
docker exec openclaw-gateway bash /home/node/.openclaw/workspace-painter/switch-model.sh "$1"

echo ""
echo "重启 openclaw-gateway..."
docker restart openclaw-gateway
sleep 15

echo ""
echo "=== 验证 ==="
docker exec openclaw-gateway python3 - <<'PY'
import json
cfg=json.load(open('/home/node/.openclaw/openclaw.json'))
items=cfg.get('agents',{}).get('items', cfg.get('agents',{}).get('list', []))
for a in items:
  if a.get('id')=='painter':
    print(f"当前 painter 模型: {a.get('model')}")
    break
PY
docker ps | grep openclaw-gateway | grep -q healthy && echo "网关状态: healthy" || echo "网关状态: 等待中..."
echo ""
echo "✅ 完成！去 Telegram @visual_muse00bot 测试吧"
