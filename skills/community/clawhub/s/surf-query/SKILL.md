---
name: 台灣衝浪浪點查詢
description: 查詢台灣全島衝浪浪點資訊，含即時潮汐、風況、颱風動態、日出日落，可附帶查詢附近停車場。支援 Telegram、LINE、iMessage。
---

# surf_query

透過 Telegram、LINE 或 iMessage 查詢台灣衝浪浪點，即時顯示潮汐、風向風速、颱風動態與日出時間。

## 功能

- **浪點搜尋**：依名稱（東河、蜜月灣...）或地區（宜蘭、台東、墾丁...）搜尋
- **附近浪點**：傳送定位點，查詢 30km 內所有已知浪點
- **即時潮汐**：今日高低潮時間（CWA 中央氣象署）
- **即時風況**：風速、風向，並判斷是否為離岸風（好浪）
- **颱風動態**：顯示距台灣 2000km 內的活動颱風位置與強度
- **日出日落**：依浪點座標計算今日日出日沒時間
- **季節判斷**：自動標示現在是否為最佳浪季
- **一鍵導航**：Apple Maps + Google Maps 連結
- **串接停車查詢**：選用，需搭配 parking_query skill

## 使用情境

```
用戶：東河附近有什麼浪點？

回覆：
🏄 東河 (Donghe)
   📍 台東縣 東河鄉
   🟡 難度：中階　浪型：河口浪
   ✅ 現在（秋季）是好浪季節
   🌅 日出 05:52　🌇 日沒 17:48
   🌊 潮汐：🔽乾潮 02:14（-87cm）　🔼滿潮 08:28（59cm）...
   💨 風況：偏北風 3級（4m/s）　✅ 離岸風，浪面整潔
   ⛅ 天氣：晴時多雲
   📝 台灣浪況最一致的浪點之一，東河溪口，冬季長浪穩定，礁石底
   🍎 Apple Maps → https://maps.apple.com/?ll=23.0767,121.3424&q=東河
   🗺 Google Maps → https://www.google.com/maps/search/?api=1&query=23.0767,121.3424
```

適用頻道：Telegram、LINE、iMessage（BlueBubbles）、及其他 OpenClaw 支援的頻道

## 前置需求

### 1. 申請 CWA API Key（免費，即時潮汐/風況用）

前往 [opendata.cwa.gov.tw](https://opendata.cwa.gov.tw) 註冊帳號，取得授權碼。

在 OpenClaw 的 `openclaw.json` 中加入：

```json
{
  "env": {
    "vars": {
      "CWA_API_KEY": "CWA-你的授權碼"
    }
  }
}
```

> 不設定也能使用，只是不會顯示即時潮汐與風況。

### 2. 安裝 Python 套件

```bash
pip3 install requests
```

## 安裝

```bash
git clone https://github.com/Harperbot/openclaw-surf-query.git \
  ~/.openclaw/skills/surf_query

openclaw restart
```

## 資料來源

| 用途 | API |
|---|---|
| 浪點資料庫（30 個） | swelleye.com + outdoorfun.com.tw（手動整理） |
| 即時潮汐 | CWA `F-A0021-001` |
| 風況天氣 | CWA `F-D0047-091` |
| 颱風動態 | CWA `W-C0034-005` |
| 日出日落 | 天文公式計算 |

## 覆蓋範圍

北部（新北）、東北部（宜蘭）、東部（花蓮、台東）、南部（屏東、墾丁）、西部（高雄、台南、台中、苗栗）
