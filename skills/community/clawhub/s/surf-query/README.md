# 🏄 surf_query

台灣衝浪浪點查詢 OpenClaw Skill，透過 Telegram、LINE 或 iMessage 搜尋浪點，即時顯示潮汐、風況、颱風動態與日出時間，並附一鍵導航連結。

## 功能示範

```
你：東河附近有什麼浪點？

助理：
🏄 東河 (Donghe)
   📍 台東縣 東河鄉
   🟡 難度：中階　浪型：河口浪
   ✅ 現在（秋季）是好浪季節
   🌅 日出 05:52　🌇 日沒 17:48
   🌊 潮汐：🔽乾潮 02:14（-87cm）　🔼滿潮 08:28（59cm）　🔽乾潮 14:06（-64cm）　🔼滿潮 20:18（80cm）
   💨 風況：偏北風 3級（4m/s）　✅ 離岸風，浪面整潔
   ⛅ 天氣：晴時多雲
   📝 台灣浪況最一致的浪點之一，東河溪口，冬季長浪穩定，礁石底
   🍎 Apple Maps → https://maps.apple.com/?ll=23.0767,121.3424&q=東河
   🗺 Google Maps → https://www.google.com/maps/search/?api=1&query=23.0767,121.3424
```

## 特色

- **30 個浪點資料庫**：北部、東北部（宜蘭）、東部（花蓮、台東）、南部（屏東、墾丁）、西部
- **多種查詢方式**：浪點名稱、地區名稱、GPS 座標（附近 30km 內）
- **即時潮汐**：CWA 中央氣象署今日高低潮時間（高精度，依浪點配對最近測站）
- **即時風況**：風速、風向，自動判斷離岸風（好浪）或向岸風（浪面雜亂）
- **颱風動態**：顯示距台灣 2000km 內的活動颱風，超出範圍自動隱藏
- **日出日落**：依浪點座標以天文公式精確計算
- **難度分級**：🟢 初學者 / 🟡 初中階・中階 / 🟠 中進階 / 🔴 進階
- **季節判斷**：自動標示現在是否為最佳浪季
- **一鍵導航**：Apple Maps + Google Maps 導航連結
- **串接停車查詢**：選用，需搭配 [parking_query](https://github.com/Harperbot/openclaw-parking-query) skill

## 前置需求

### 1. OpenClaw

請先安裝並設定 [OpenClaw](https://github.com/openclaw/openclaw)。

### 2. CWA API Key（免費）

前往 [opendata.cwa.gov.tw](https://opendata.cwa.gov.tw) 註冊帳號，取得授權碼。

在 `~/.openclaw/openclaw.json` 的 `env.vars` 加入：

```json
{
  "env": {
    "vars": {
      "CWA_API_KEY": "CWA-你的授權碼"
    }
  }
}
```

> 不設定也能使用，只是不會顯示即時潮汐、風況與颱風動態。

### 3. Python 套件

```bash
pip3 install requests
```

## 安裝

```bash
# 1. Clone 到 OpenClaw skills 目錄
git clone https://github.com/Harperbot/openclaw-surf-query.git \
  ~/.openclaw/skills/surf_query

# 2. 設定 CWA API Key（見上方說明）

# 3. 重啟 gateway
openclaw restart
```

或透過 ClawHub 安裝：

```bash
clawhub install openclaw-surf-query
```

## 直接執行（測試用）

```bash
# 依名稱搜尋
python3 ~/.openclaw/skills/surf_query/surf_query.py --query 東河

# 依地區搜尋
python3 ~/.openclaw/skills/surf_query/surf_query.py --query 宜蘭

# 依座標查詢附近浪點（30km 內）
python3 ~/.openclaw/skills/surf_query/surf_query.py --lat 24.87 --lon 121.83

# 浪點 + 附近停車場
python3 ~/.openclaw/skills/surf_query/surf_query.py --query 東河 --mode parking

# 列出所有浪點
python3 ~/.openclaw/skills/surf_query/surf_query.py --list

# 不查即時資料（純離線，速度快）
python3 ~/.openclaw/skills/surf_query/surf_query.py --query 金樽 --no-live
```

## 更新

```bash
bash ~/.openclaw/skills/surf_query/update.sh
```

或手動：

```bash
cd ~/.openclaw/skills/surf_query && git pull
```

## 浪點資料庫

| 地區 | 浪點 |
|---|---|
| 北部（新北） | 沙崙、白沙灣、中角灣、金山、翡翠灣、萬里 |
| 東北（宜蘭） | 福隆、大溪蜜月灣、外澳、烏石港北堤、烏石港南堤、梗枋、蘇澳無尾港 |
| 東部（花蓮） | 和仁礫灘、花蓮北濱、鹽寮漁港、磯崎 |
| 東部（台東） | 八仙洞、成功、東河、金樽、都蘭、台東市區 |
| 南部（屏東） | 九棚、佳樂水、南灣、杉板灣（小琉球） |
| 西部 | 旗津、漁光島、外埔漁港、竹南 |

## 資料來源

| 用途 | 來源 | 狀態 |
|---|---|---|
| 浪點資料庫 | swelleye.com + outdoorfun.com.tw | 手動整理，內建 JSON |
| 即時潮汐 | CWA opendata `F-A0021-001` | 需 CWA_API_KEY |
| 風況天氣預報 | CWA opendata `F-D0047-091` | 需 CWA_API_KEY |
| 颱風動態 | CWA opendata `W-C0034-005` | 需 CWA_API_KEY |
| 日出日落 | 天文公式計算 | 免費，不需 API |
| 停車場即時空位 | TDX parking_query skill | 選用 |

## 與 parking_query 串接

安裝 [parking_query](https://github.com/Harperbot/openclaw-parking-query) 後，加上 `--mode parking` 可同時查詢浪點附近停車場：

```bash
python3 surf_query.py --query 東河 --mode parking
```

```
🏄 東河 (Donghe)
   ...（浪點資訊）

🅿️ 附近停車：
🅿️ 附近 500 公尺 有空位的停車場（Taitung）

1. 東河停車場
   空位：28 個　距離：210 公尺
   🍎 Apple Maps → ...
   🗺 Google Maps → ...
```

---

## 進階整合（選用）

以下為可選的進階功能，適合想要主動通知的使用者自行串接。所有頻道（Telegram、LINE、iMessage）均透過 OpenClaw 的 channel bindings 設定路由，不需個別修改程式碼。

### 颱風警報推播

CWA `W-C0034-005` 提供即時颱風動態，可在 cron 排程中定期查詢，颱風進入指定距離時自動推播：

```python
import requests, os

KEY = os.environ["CWA_API_KEY"]
r = requests.get(
    "https://opendata.cwa.gov.tw/api/v1/rest/datastore/W-C0034-005",
    params={"Authorization": KEY},
    verify=False  # CWA 憑證缺 SKI，Python 3.12+ 需加此參數
)
data = r.json()
cyclones = data["records"]["TropicalCyclones"]["TropicalCyclone"]
for tc in cyclones:
    fixes = tc["AnalysisData"]["Fix"]
    last = fixes[-1] if isinstance(fixes, list) else fixes
    # 計算距台灣距離，決定是否發送通知
```

搭配 OpenClaw cron 每小時執行，有警報時發送至 **Telegram / iMessage / LINE**。

### 長浪警戒通知

> ⚠️ `W-C0051-001` 可能需要進階 CWA 帳號權限，免費帳號目前無法存取。

若您的帳號有權限，可加入每日維護排程：

```python
r = requests.get(
    "https://opendata.cwa.gov.tw/api/v1/rest/datastore/W-C0051-001",
    params={"Authorization": KEY},
    verify=False
)
```

### 每日浪報推播（Telegram / iMessage / LINE）

結合 surf_query 與 CWA API，透過 OpenClaw cron 每日定時推播至任意已串接頻道：

```
🌅 今日浪報（東台灣）

🏄 東河：偏北風 3 級，中潮 09:30
         現在漲潮中，預計 09:00 附近最佳
🏄 金樽：偏北風 3 級，大潮 09:20

⛅ 今日天氣：晴時多雲，氣溫 22-28°C
🌀 颱風動態：無（距台灣 2000km 以上）
🌅 今日日出：05:52
```

**設定方式**（以 Telegram 為例）：

1. 在 `~/.openclaw/cron/jobs.json` 加入排程
2. 排程腳本呼叫 `surf_query.py` 並取得輸出
3. 透過 OpenClaw 的 `sendMessage` 工具發送至目標頻道

iMessage（BlueBubbles）與 LINE 的設定方式相同，只需在 OpenClaw agent bindings 中切換頻道。

---

## License

MIT
