#!/bin/bash
# 完整天气预报脚本
# 用法: weather-full.sh <城市> [天数]

# 加载环境变量
if [ -f ~/.openclaw/.env ]; then
    source ~/.openclaw/.env
fi

CITY="${1:-Shanghai}"
DAYS="${2:-1}"

# 天气数据（WeatherAPI 支持中英文）
WEATHER_JSON=$(curl -s "https://api.weatherapi.com/v1/forecast.json?key=${WEATHERAPI_KEY}&q=${CITY}&days=${DAYS}&lang=zh&aqi=yes")

# 检查是否成功获取天气
if [ -z "$WEATHER_JSON" ] || echo "$WEATHER_JSON" | jq -e '.error' >/dev/null 2>&1; then
    echo "❌ 无法获取 ${CITY} 的天气数据"
    exit 1
fi

# 从天气数据提取坐标
LAT=$(echo "$WEATHER_JSON" | jq -r '.location.lat')
LON=$(echo "$WEATHER_JSON" | jq -r '.location.lon')

# 解析天气
echo "$WEATHER_JSON" | jq -r '
    "[\(.location.name)]天气 \(.forecast.forecastday[0].date)
    
🌡️ 温度：\(.forecast.forecastday[0].day.mintemp_c) ~ \(.forecast.forecastday[0].day.maxtemp_c)°C
🌬️ 风力：\(.current.wind_dir)风 \(.current.wind_kph)km/h
☁️ 天况：\(.current.condition.text)
💧 湿度：\(.current.humidity)%
🌫️ 空气质量：PM2.5 \(.current.air_quality.pm2_5 | floor)

🌅 日出：\(.forecast.forecastday[0].astro.sunrise)
🌇 日落：\(.forecast.forecastday[0].astro.sunset)"'

DATE=$(date +%Y-%m-%d)

# 朝霞
SUNRISE_JSON=$(curl -s "https://api.sunsethue.com/event?latitude=${LAT}&longitude=${LON}&date=${DATE}&type=sunrise&key=${SUNSETHUE_KEY}")
SUNRISE_QUALITY=$(echo "$SUNRISE_JSON" | jq -r '.data.quality * 100 | floor // 0')
SUNRISE_RATING=$(echo "$SUNRISE_JSON" | jq -r '.data.quality_text // "N/A"')

# 晚霞
SUNSET_JSON=$(curl -s "https://api.sunsethue.com/event?latitude=${LAT}&longitude=${LON}&date=${DATE}&type=sunset&key=${SUNSETHUE_KEY}")
SUNSET_QUALITY=$(echo "$SUNSET_JSON" | jq -r '.data.quality * 100 | floor // 0')
SUNSET_RATING=$(echo "$SUNSET_JSON" | jq -r '.data.quality_text // "N/A"')

# 提取 Golden/Blue Hour（UTC 时间，+8 转北京时间）
MORNING_GOLDEN_START=$(echo "$SUNRISE_JSON" | jq -r '.data.magics.golden_hour[0] // empty' | sed 's/.*T\([0-9:]*\).*/\1/')
MORNING_GOLDEN_END=$(echo "$SUNRISE_JSON" | jq -r '.data.magics.golden_hour[1] // empty' | sed 's/.*T\([0-9:]*\).*/\1/')
MORNING_BLUE_START=$(echo "$SUNRISE_JSON" | jq -r '.data.magics.blue_hour[0] // empty' | sed 's/.*T\([0-9:]*\).*/\1/')
MORNING_BLUE_END=$(echo "$SUNRISE_JSON" | jq -r '.data.magics.blue_hour[1] // empty' | sed 's/.*T\([0-9:]*\).*/\1/')

EVENING_GOLDEN_START=$(echo "$SUNSET_JSON" | jq -r '.data.magics.golden_hour[0] // empty' | sed 's/.*T\([0-9:]*\).*/\1/')
EVENING_GOLDEN_END=$(echo "$SUNSET_JSON" | jq -r '.data.magics.golden_hour[1] // empty' | sed 's/.*T\([0-9:]*\).*/\1/')
EVENING_BLUE_START=$(echo "$SUNSET_JSON" | jq -r '.data.magics.blue_hour[0] // empty' | sed 's/.*T\([0-9:]*\).*/\1/')
EVENING_BLUE_END=$(echo "$SUNSET_JSON" | jq -r '.data.magics.blue_hour[1] // empty' | sed 's/.*T\([0-9:]*\).*/\1/')

# UTC 时间转北京时间（+8小时）
utc_to_bj() {
    local time=$1
    if [ -z "$time" ]; then
        echo "N/A"
        return
    fi
    local hour=$(echo $time | cut -d: -f1 | sed 's/^0//')
    local min=$(echo $time | cut -d: -f2 | sed 's/^0//')
    hour=${hour:-0}
    min=${min:-0}
    local bj_hour=$(( (hour + 8) % 24 ))
    printf "%02d:%02d" $bj_hour $min
}

echo ""
echo "✨ 早晨 Golden Hour：$(utc_to_bj "$MORNING_GOLDEN_START") - $(utc_to_bj "$MORNING_GOLDEN_END")"
echo "✨ 傍晚 Golden Hour：$(utc_to_bj "$EVENING_GOLDEN_START") - $(utc_to_bj "$EVENING_GOLDEN_END")"
echo "💙 早晨 Blue Hour：$(utc_to_bj "$MORNING_BLUE_START") - $(utc_to_bj "$MORNING_BLUE_END")"
echo "💙 傍晚 Blue Hour：$(utc_to_bj "$EVENING_BLUE_START") - $(utc_to_bj "$EVENING_BLUE_END")"
echo ""
echo "🌅 朝霞质量：${SUNRISE_QUALITY}% (${SUNRISE_RATING})"
echo "🌇 晚霞质量：${SUNSET_QUALITY}% (${SUNSET_RATING})"
