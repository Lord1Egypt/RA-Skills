# Weather Poster SVG Template

## Layout (400x800)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ff9a9e"/>
      <stop offset="100%" style="stop-color:#fad0c4"/>
    </linearGradient>
    <linearGradient id="tipGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#a8edea"/>
      <stop offset="100%" style="stop-color:#fed6e3"/>
    </linearGradient>
    <filter id="cardShadow">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.1"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="400" height="800" rx="24" fill="white"/>

  <!-- Header -->
  <path d="M0,24 Q0,0 24,0 L376,0 Q400,0 400,24 L400,130 L0,130 Z" fill="url(#headerGrad)"/>
  <text x="200" y="75" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="28" font-weight="bold" fill="white">{CITY}今日天气穿搭</text>
  <text x="200" y="110" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="14" fill="rgba(255,255,255,0.9)">{DATE} {WEEKDAY}</text>

  <!-- Weather Info -->
  <g transform="translate(0, 150)">
    <text x="200" y="50" text-anchor="middle" font-size="60">{WEATHER_ICON}</text>
    <text x="200" y="130" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="72" font-weight="bold" fill="#333">{TEMP}<tspan font-size="32" fill="#666">°C</tspan></text>
    <text x="200" y="170" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="20" fill="#666">{WEATHER_DESC}</text>
    <!-- Wind & Humidity -->
    <g transform="translate(0, 200)">
      <text x="100" y="15" text-anchor="middle" font-size="24">💨</text>
      <text x="100" y="40" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="14" fill="#888">微风 {WIND}km/h</text>
      <text x="300" y="15" text-anchor="middle" font-size="24">💧</text>
      <text x="300" y="40" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="14" fill="#888">{HUMIDITY}</text>
    </g>
  </g>

  <!-- Outfit Section (grey background extends to cover Tips) -->
  <rect x="0" y="400" width="400" height="300" fill="#f8f9fa"/>
  <text x="200" y="435" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="22" font-weight="bold" fill="#333">👔 今日穿搭推荐</text>
  
  <!-- Outfit Grid -->
  <g transform="translate(30, 470)">
    <!-- 4 items in 2x2 grid -->
  </g>

  <!-- Tips -->
  <rect x="0" y="700" width="400" height="45" fill="url(#tipGrad)"/>
  <text x="200" y="728" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="14" fill="#666">{TIPS}</text>

  <!-- Footer -->
  <path d="M0,745 L0,776 Q0,800 24,800 L376,800 Q400,800 400,776 L400,745 Z" fill="#667eea"/>
  <text x="200" y="772" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="12" fill="white">OpenClaw 天气穿搭助手</text>
</svg>
```

## Dynamic Values

| Variable | Description |
|----------|-------------|
| `{CITY}` | City name (default: 武汉) |
| `{DATE}` | Date in format YYYY年MM月dd日 |
| `{WEEKDAY}` | Weekday in Chinese |
| `{WEATHER_ICON}` | Weather emoji (🌧️☀️🌤️⛅🌩️❄️) |
| `{TEMP}` | Temperature number |
| `{WEATHER_DESC}` | Weather description |
| `{WIND}` | Wind speed |
| `{HUMIDITY}` | Humidity description |
| `{TIPS}` | Tip text based on weather |