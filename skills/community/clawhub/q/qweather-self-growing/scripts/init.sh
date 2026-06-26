#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/local"
CSV_URL="https://raw.githubusercontent.com/qwd/LocationList/master/China-City-List-latest.csv"
CSV_PATH="$LOCAL_DIR/China-City-List-latest.csv"

echo "=== qweather 初始化 ==="

# 确保 local 目录存在
mkdir -p "$LOCAL_DIR"

# 下载 LocationList
echo ""
echo "📥 下载中国城市列表..."
if curl -fsSL "$CSV_URL" -o "$CSV_PATH"; then
  LINE_COUNT=$(wc -l < "$CSV_PATH" | tr -d ' ')
  echo "   ✅ 已下载 ($LINE_COUNT 条记录) → local/China-City-List-latest.csv"
else
  echo "   ⚠️  下载失败，城市解析将依赖 GeoAPI 兜底"
fi

# 验证配置
echo ""
echo "🔑 检查认证配置..."
CONFIG_OK=true

if [[ -f "$LOCAL_DIR/qweather.json" ]]; then
  echo "   找到 local/qweather.json"
  # 检查必要字段
  MISSING=$(node -e '
    const c = JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"));
    const missing = ["kid","projectId","privateKeyPath","apiHost"].filter(k => !c[k]);
    if (missing.length) console.log(missing.join(", "));
  ' "$LOCAL_DIR/qweather.json" 2>/dev/null || echo "解析失败")
  if [[ -n "$MISSING" ]]; then
    echo "   ⚠️  缺少字段: $MISSING"
    CONFIG_OK=false
  else
    echo "   ✅ 配置完整"
  fi
elif [[ -n "${QWEATHER_KID:-}" && -n "${QWEATHER_PROJECT_ID:-}" && -n "${QWEATHER_PRIVATE_KEY_PATH:-}" && -n "${QWEATHER_API_HOST:-}" ]]; then
  echo "   ✅ 环境变量配置完整"
else
  echo "   ⚠️  未找到配置。请设置环境变量或创建 local/qweather.json"
  echo "   详见 references/setup.md"
  CONFIG_OK=false
fi

# 验证连通性
if [[ "$CONFIG_OK" == "true" ]]; then
  echo ""
  echo "🌤  测试 API 连通性..."
  JWT_TOKEN=$(cd "$SCRIPT_DIR" && node gen-jwt.mjs)
  API_HOST=$(cd "$SCRIPT_DIR" && node gen-jwt.mjs --host)
  RESP=$(curl -sS --compressed -H "Authorization: Bearer $JWT_TOKEN" "https://$API_HOST/v7/weather/now?location=101210101&lang=zh" 2>/dev/null || echo '{"code":"error"}')
  CODE=$(echo "$RESP" | node -e 'const d=JSON.parse(require("fs").readFileSync(0,"utf8")); console.log(d.code || "error")')
  if [[ "$CODE" == "200" ]]; then
    echo "   ✅ API 连通正常"
  else
    echo "   ⚠️  API 返回 code=$CODE，请检查配置"
  fi
fi

echo ""
echo "=== 初始化完成 ==="
