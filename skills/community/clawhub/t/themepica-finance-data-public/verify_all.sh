#!/bin/bash
# 验证所有25个公开API
cd /home/ecs-user/.openclaw/workspace/skills/themepica-finance-data-public

echo "=========================================="
echo "  themepica-finance-data-public 全量验证"
echo "=========================================="
echo ""

PASS=0
FAIL=0
FAILED_APIS=""

run_test() {
  local name="$1"
  local cmd="$2"
  echo -n "[测试] $name ... "
  result=$(eval "$cmd" 2>&1)
  
  # 检查HTTP 200
  http_ok=$(echo "$result" | grep -c '"statusCode":200')
  # 检查业务成功（errCode=0 或 code=0）
  err_ok=$(echo "$result" | grep -cE '"(errCode|code)":\s*0')
  # 取响应体前几行用于调试
  preview=$(echo "$result" | head -3)
  
  if [ "$http_ok" -gt 0 ] && [ "$err_ok" -gt 0 ]; then
    echo "✅ OK"
    PASS=$((PASS+1))
  elif [ "$http_ok" -gt 0 ]; then
    # HTTP 200 but business error - show preview
    echo "⚠️  HTTP 200 但业务异常"
    echo "   $preview"
    FAIL=$((FAIL+1))
    FAILED_APIS="$FAILED_APIS $name"
  else
    echo "❌ 非200响应"
    echo "   $preview"
    FAIL=$((FAIL+1))
    FAILED_APIS="$FAILED_APIS $name"
  fi
}

# ===== 1. 主题分析 (7个) =====
echo "=== 1. 主题分析 (7个) ==="
run_test "themes" 'node call-node.js themes "{\"pageNum\":1,\"pageSize\":3}" 2>/dev/null'
run_test "theme_indices" 'node call-node.js theme_indices "{\"themeId\":\"3\"}" 2>/dev/null'
run_test "theme_etfs" 'node call-node.js theme_etfs "{\"themeId\":\"3\"}" 2>/dev/null'
run_test "theme_diagnose" 'node call-node.js theme_diagnose "{\"themeId\":\"1477062244\"}" 2>/dev/null'
run_test "theme_subs_diagnose" 'node call-node.js theme_subs_diagnose "{\"themeId\":\"3\"}" 2>/dev/null'
run_test "theme_narratives" 'node call-node.js theme_narratives "{\"themeId\":\"5900\",\"startDate\":\"2026-08-01\",\"endDate\":\"2026-08-13\"}" 2>/dev/null'
run_test "theme_contents" 'node call-node.js theme_contents "{\"themeId\":8,\"pageSize\":3,\"pageNum\":1}" 2>/dev/null'

# ===== 2. 榜单 (4个) =====
echo "=== 2. 榜单 (4个) ==="
run_test "board_hotspots" 'node call-node.js board_hotspots "{\"pageNum\":\"1\",\"pageSize\":\"3\"}" 2>/dev/null'
run_test "board_hotspots_detail" 'node call-node.js board_hotspots_detail "{\"startTime\":\"2026-08-24\",\"endTime\":\"2026-08-24\"}" 2>/dev/null'
run_test "board_hotspots_latest_detail" 'node call-node.js board_hotspots_latest_detail 2>/dev/null'
run_test "board_indices" 'node call-node.js board_indices "{\"startDate\":\"2026-08-03\",\"endDate\":\"2026-08-03\"}" 2>/dev/null'

# ===== 3. 热点 (10个) =====
echo "=== 3. 热点 (10个) ==="
run_test "hotspot_heats" 'node call-node.js hotspot_heats "{\"keywords\":[\"英伟达\"],\"startTime\":\"2026-08-03 00:00:00\",\"endTime\":\"2026-08-12 12:34:32\"}" 2>/dev/null'
run_test "hotspot_emotions" 'node call-node.js hotspot_emotions "{\"keywords\":[\"AI\"],\"startTime\":\"2026-08-13 00:00:00\",\"endTime\":\"2026-08-17 13:34:32\"}" 2>/dev/null'
run_test "hotspot_news" 'node call-node.js hotspot_news "{\"startTime\":\"2026-08-21\",\"endTime\":\"2026-08-21\",\"keywords\":\"消费贷\",\"category\":\"事件\"}" 2>/dev/null'
run_test "hotspot_viewpoints" 'node call-node.js hotspot_viewpoints "{\"startTime\":\"2026-07-09\",\"endTime\":\"2026-07-14\",\"keywords\":\"石油\"}" 2>/dev/null'
run_test "hotspot_securities" 'node call-node.js hotspot_securities "{\"startTime\":\"2026-08-17\",\"endTime\":\"2026-08-17\",\"keywords\":\"AI\",\"start\":\"0\",\"end\":\"5\"}" 2>/dev/null'
run_test "hotspot_indices" 'node call-node.js hotspot_indices "{\"startTime\":\"2026-07-17\",\"endTime\":\"2026-07-23\",\"keywords\":\"标普石油\"}" 2>/dev/null'
run_test "hotspot_themes" 'node call-node.js hotspot_themes "{\"startTime\":\"2025-05-09\",\"endTime\":\"2025-05-21\",\"keywords\":\"华为\"}" 2>/dev/null'
run_test "hotspot_etfs" 'node call-node.js hotspot_etfs "{\"startTime\":\"2026-08-19\",\"endTime\":\"2026-08-19\",\"keywords\":\"眼镜\"}" 2>/dev/null'
run_test "hotspot_policies" 'node call-node.js hotspot_policies "{\"startTime\":\"2026-01-17\",\"endTime\":\"2026-01-21\",\"keywords\":\"AI\"}" 2>/dev/null'
run_test "hotspot_funds" 'node call-node.js hotspot_funds "{\"startTime\":\"2026-08-17\",\"endTime\":\"2026-08-17\",\"keywords\":\"智能机器人\"}" 2>/dev/null'

# ===== 4. 基金 (1个) =====
echo "=== 4. 基金 (1个) ==="
run_test "fund_narratives" 'node call-node.js fund_narratives "{\"fundTicker\":\"516090\"}" 2>/dev/null'

# ===== 5. 指数 (2个) =====
echo "=== 5. 指数 (2个) ==="
run_test "index_detail" 'node call-node.js index_detail "{\"indexTicker\":\"HSTECH.HK\"}" 2>/dev/null'
run_test "index_daily" 'node call-node.js index_daily "{\"indexTickers\":\"000001.SH,000300.SH\",\"startDate\":\"2026-06-01\",\"endDate\":\"2026-06-05\"}" 2>/dev/null'

# ===== 6. ETF (1个) =====
echo "=== 6. ETF (1个) ==="
run_test "etf_narratives" 'node call-node.js etf_narratives "{\"etfTicker\":\"159994\"}" 2>/dev/null'

# ===== 结果汇总 =====
echo ""
echo "=========================================="
echo "  验证完成: ✅ $PASS 通过 | ❌ $FAIL 失败"
echo "=========================================="
if [ $FAIL -gt 0 ]; then
  echo "失败接口: $FAILED_APIS"
fi