#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/local"

JWT_TOKEN=$(cd "$SCRIPT_DIR" && node gen-jwt.mjs)
API_HOST=$(cd "$SCRIPT_DIR" && node gen-jwt.mjs --host)

CITY="杭州"
MODE="forecast"  # forecast | now
DAYS="3"
FORMAT="brief"

usage() {
  cat <<'EOF'
Usage: qweather.sh [city|locationId] [options]

Options:
  --now               Real-time weather
  --days 3|7          Forecast days (default: 3)
  --brief             Human-readable summary (default)
  --json              Raw JSON output
  --trip              Travel-oriented summary
  -h, --help          Show help

Examples:
  bash ./scripts/qweather.sh 杭州 --now
  bash ./scripts/qweather.sh 杭州
  bash ./scripts/qweather.sh 杭州 --trip
  bash ./scripts/qweather.sh 杭州 --days 7 --json
  bash ./scripts/qweather.sh 101210101
EOF
}

LOCAL_CITY_MAP="$LOCAL_DIR/cities.json"
LOCATION_CSV="$LOCAL_DIR/China-City-List-latest.csv"

api_get() {
  local url="$1"
  curl -sS --compressed -H "Authorization: Bearer $JWT_TOKEN" "$url"
}

# 城市解析：三级优先级链
# 1. local/cities.json 用户自定义映射
# 2. LocationList CSV 离线查询
# 3. GeoAPI 兜底
resolve_location() {
  local input="$1"

  # 纯数字直接当 LocationID
  if [[ "$input" =~ ^[0-9]+$ ]]; then
    echo "$input"
    return 0
  fi

  # 第一级：local/cities.json
  if [[ -f "$LOCAL_CITY_MAP" ]]; then
    local local_loc
    local_loc=$(node -e '
      const m = JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"));
      console.log(m[process.argv[2]] || "")
    ' "$LOCAL_CITY_MAP" "$input" 2>/dev/null || true)
    if [[ -n "$local_loc" ]]; then
      echo "$local_loc"
      return 0
    fi
  fi

  # 第二级：LocationList CSV
  if [[ -f "$LOCATION_CSV" ]]; then
    local csv_results
    csv_results=$(node -e '
      const fs = require("fs");
      const keyword = process.argv[1];
      const lines = fs.readFileSync(process.argv[2], "utf8").split("\n");
      const matches = [];
      for (let i = 1; i < lines.length; i++) {
        const cols = lines[i].split(",");
        if (cols.length < 10) continue;
        if (cols[2] === keyword) {
          matches.push({ id: cols[0], name: cols[2], adm1: cols[7], adm2: cols[9] });
        }
      }
      console.log(JSON.stringify(matches));
    ' "$input" "$LOCATION_CSV" 2>/dev/null || echo "[]")

    local match_count
    match_count=$(echo "$csv_results" | node -e 'console.log(JSON.parse(require("fs").readFileSync(0,"utf8")).length)')

    if [[ "$match_count" == "1" ]]; then
      echo "$csv_results" | node -e 'console.log(JSON.parse(require("fs").readFileSync(0,"utf8"))[0].id)'
      return 0
    elif [[ "$match_count" -gt 1 ]]; then
      echo "城市 '$input' 存在多个候选（来自 LocationList），请改用 LocationID：" >&2
      echo "$csv_results" | node -e '
        JSON.parse(require("fs").readFileSync(0,"utf8")).forEach(x =>
          console.error(`  - ${x.name} / ${x.adm1} / ${x.adm2} (${x.id})`)
        )'
      exit 4
    fi
    # match_count == 0，继续走 GeoAPI
  fi

  # 第三级：GeoAPI 兜底
  local encoded
  encoded=$(python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1]))" "$input")
  local geo
  geo=$(api_get "https://$API_HOST/geo/v2/city/lookup?location=$encoded&number=5&lang=zh")
  local code
  code=$(echo "$geo" | node -e 'console.log(JSON.parse(require("fs").readFileSync(0,"utf8")).code || "")')

  if [[ "$code" != "200" ]]; then
    echo "GeoAPI 错误: $code" >&2
    exit 2
  fi

  local count
  count=$(echo "$geo" | node -e 'console.log((JSON.parse(require("fs").readFileSync(0,"utf8")).location||[]).length)')

  if [[ "$count" == "0" ]]; then
    echo "未找到城市: $input" >&2
    exit 3
  fi
  if [[ "$count" != "1" ]]; then
    echo "城市 '$input' 存在多个候选，请改用更具体的城市名或 LocationID：" >&2
    echo "$geo" | node -e '
      (JSON.parse(require("fs").readFileSync(0,"utf8")).location||[]).forEach(x =>
        console.error(`  - ${x.name} / ${x.adm1||""} / ${x.adm2||""} (${x.id})`)
      )'
    exit 4
  fi
  echo "$geo" | node -e 'console.log(JSON.parse(require("fs").readFileSync(0,"utf8")).location[0].id)'
}

# 格式化实时天气
format_now() {
  local weather="$1" city="$2" fmt="$3"

  if [[ "$fmt" == "json" ]]; then
    echo "$weather"
    return
  fi

  echo "$weather" | node -e '
    const d = JSON.parse(require("fs").readFileSync(0, "utf8"));
    const city = process.argv[1];
    const n = d.now;
    const iconFor = (t) => t.includes("雨") ? "🌧" : t.includes("雪") ? "🌨" : t.includes("晴") ? "☀️" : t.includes("云") || t.includes("阴") ? "☁️" : "🌤";
    console.log(`📍 ${city} 实时天气`);
    console.log("");
    console.log(`${iconFor(n.text)} ${n.text}  ${n.temp}℃（体感 ${n.feelsLike}℃）`);
    console.log(`   风力: ${n.windDir} ${n.windScale}级`);
    console.log(`   湿度: ${n.humidity}%`);
    console.log(`   降水: ${n.precip}mm`);
    console.log(`   能见度: ${n.vis}km`);
    console.log("");
    console.log(`观测时间: ${n.obsTime}`);
  ' "$city"
}

# 格式化逐日预报
format_forecast() {
  local weather="$1" city="$2" fmt="$3"

  if [[ "$fmt" == "json" ]]; then
    echo "$weather"
    return
  fi

  echo "$weather" | node -e '
    const d = JSON.parse(require("fs").readFileSync(0, "utf8"));
    const city = process.argv[1];
    const fmt = process.argv[2];
    const rows = d.daily || [];
    const iconFor = (t) => t.includes("雨") ? "🌧" : t.includes("雪") ? "🌨" : t.includes("晴") ? "☀️" : t.includes("云") || t.includes("阴") ? "☁️" : "🌤";

    if (fmt === "trip") {
      console.log(`📍 ${city} 出行天气`);
      console.log("");
      rows.forEach((day) => {
        console.log(`${day.fxDate} ${iconFor(day.textDay)} ${day.textDay}/${day.textNight}，${day.tempMin}~${day.tempMax}℃，${day.windDirDay}${day.windScaleDay}级，降水 ${day.precip}mm`);
        let tip = "";
        if ((day.precip && Number(day.precip) > 0) || day.textDay.includes("雨")) tip = "建议带伞";
        else if (Number(day.windSpeedDay || 0) >= 20) tip = "注意风大";
        else tip = "适合一般出行";
        console.log(`   建议：${tip}`);
      });
    } else {
      console.log(`📍 ${city}`);
      console.log("");
      rows.forEach((day, i) => {
        console.log(`${day.fxDate} ${iconFor(day.textDay)} ${day.textDay}/${day.textNight}`);
        console.log(`   气温: ${day.tempMin}°C ~ ${day.tempMax}°C`);
        console.log(`   风力: ${day.windDirDay} ${day.windScaleDay}级`);
        console.log(`   降水: ${day.precip}mm`);
        if (i < rows.length - 1) console.log("");
      });
    }
  ' "$city" "$fmt"
}

# 解析参数
while [[ $# -gt 0 ]]; do
  case "$1" in
    --now)
      MODE="now"; shift ;;
    --days)
      DAYS="$2"; shift 2 ;;
    --brief)
      FORMAT="brief"; shift ;;
    --json)
      FORMAT="json"; shift ;;
    --trip)
      FORMAT="trip"; shift ;;
    -h|--help)
      usage; exit 0 ;;
    --*)
      echo "未知参数: $1" >&2; usage; exit 1 ;;
    *)
      CITY="$1"; shift ;;
  esac
done

if [[ "$MODE" == "forecast" && "$DAYS" != "3" && "$DAYS" != "7" ]]; then
  echo "--days 仅支持 3 或 7" >&2
  exit 1
fi

LOCATION=$(resolve_location "$CITY")

if [[ "$MODE" == "now" ]]; then
  ENDPOINT="https://$API_HOST/v7/weather/now?location=$LOCATION&lang=zh"
else
  ENDPOINT="https://$API_HOST/v7/weather/${DAYS}d?location=$LOCATION&lang=zh"
fi

WEATHER=$(api_get "$ENDPOINT")
CODE=$(echo "$WEATHER" | node -e 'console.log(JSON.parse(require("fs").readFileSync(0,"utf8")).code || "")')

if [[ "$CODE" != "200" ]]; then
  echo "天气 API 错误: $CODE" >&2
  echo "$WEATHER" >&2
  exit 5
fi

if [[ "$MODE" == "now" ]]; then
  format_now "$WEATHER" "$CITY" "$FORMAT"
else
  format_forecast "$WEATHER" "$CITY" "$FORMAT"
fi
