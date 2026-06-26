# Virtual Desktop Browser Skill

在 **Xvfb 虛擬顯示器（固定 1200x720x24）** 啟動 **Chromium 非無頭模式**，並用 **PyAutoGUI** 進行模擬人類操作（點擊、輸入、滾動、截圖）。  
適合對抗強反爬蟲網站（小紅書、X/Twitter 等），讓 AI Agent 能像真人一樣操作瀏覽器。

[English](docs/en.md) | [Español](docs/es.md) | [العربية](docs/ar.md)

---

## 功能

| 功能 | 說明 |
|------|------|
| 虛擬顯示器 | Xvfb 啟動獨立 X Server，顯示 1200x720x24 |
| 非無頭瀏覽器 | Chromium 帶 GUI 介面跑在虛擬螢幕上 |
| 滑鼠模擬 | 移動、點擊（左/右/中/雙擊）、拖曳 |
| 鍵盤模擬 | 輸入文字、快捷鍵、按鍵組合 |
| 滾動 | 垂直與水平滾動 |
| 截圖 | 全螢幕或指定區域截圖，回傳 Base64 PNG |
| 圖像匹配 | 用 OpenCV 在螢幕上找圖片模板 |
| 像素取色 | 讀取指定座標的 RGB 顏色 |
| 視窗管理 | 根據標題切換聚焦視窗 |
| 自動分配 DISPLAY | 避免多會話衝突（:99 ~ :199） |
| 安全中止 | 滑鼠移到右下角立即中止（PyAutoGUI Failsafe） |

---

## 安裝

### 系統依賴（Ubuntu/Debian）

```bash
apt-get update
apt-get install -y xvfb chromium-browser \
  libnss3 libgconf-2-4 libxss1 libasound2 \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libgbm1 libgtk-3-0 libxshmfence1 x11-utils
```

### Python 依賴

```bash
pip install -r requirements.txt
```

### 安裝技能

```bash
npx skills add https://github.com/NHZallen/virtual-desktop-browser-skill
```

---

## 工具參考

### `browser_start(url=None, display=None)`

啟動 Xvfb 與 Chromium。

| 參數 | 類型 | 說明 |
|------|------|------|
| `url` | str (optional) | 初始網址，留空為 about:blank |
| `display` | str (optional) | X display，如 `:99`。留空自動分配 |

**回傳：**
```json
{
  "status": "started",
  "display": ":99",
  "xvfb_pid": 12345,
  "chrome_pid": 12346,
  "resolution": "1200x720x24"
}
```

---

### `browser_stop()`

關閉 Chromium 與 Xvfb，釋放資源。

**回傳：** `{ "status": "stopped" }`

---

### `browser_snapshot(region=None)`

截取虛擬螢幕畫面，回傳 Base64 PNG。

| 參數 | 類型 | 說明 |
|------|------|------|
| `region` | tuple (optional) | `(left, top, width, height)` 指定截圖區域 |

**回傳：**
```json
{
  "image_base64": "iVBORw0KGgo...",
  "width": 1200,
  "height": 720
}
```

---

### `browser_click(x, y, button='left', clicks=1, duration=0.5)`

移動滑鼠並點擊。

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| `x` | int | 必填 | X 座標 |
| `y` | int | 必填 | Y 座標 |
| `button` | str | `left` | 按鈕：`left` / `right` / `middle` |
| `clicks` | int | `1` | 點擊次數（1=單擊，2=雙擊） |
| `duration` | float | `0.5` | 滑鼠移動時間（秒，0=瞬間） |

---

### `browser_type(text, interval=0.05, wpm=None)`

在當前焦點元素輸入文字。

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| `text` | str | 必填 | 要輸入的文字 |
| `interval` | float | `0.05` | 按鍵間隔（秒） |
| `wpm` | int (optional) | — | 每分鐘字數，模擬真人打字速度 |

---

### `browser_hotkey(keys, interval=0.05)`

按下組合鍵。

| 參數 | 類型 | 說明 |
|------|------|------|
| `keys` | list[str] | 鍵名列表，如 `["ctrl", "c"]` |
| `interval` | float | 按鍵間隔（秒） |

**範例：** `browser_hotkey(["ctrl", "a"])`、`browser_hotkey(["ctrl", "shift", "t"])`

---

### `browser_scroll(clicks=1, direction='vertical', x=None, y=None)`

模擬滑鼠滾輪。

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| `clicks` | int | `1` | 滾動格數（正=上/左，負=下/右） |
| `direction` | str | `vertical` | `vertical` 或 `horizontal` |
| `x`, `y` | int (optional) | — | 滾動位置（留空用當前滑鼠位置） |

---

### `browser_find_image(image_path, confidence=0.8)`

在螢幕上尋找圖片模板。

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| `image_path` | str | 必填 | 模板圖片路徑（PNG/JPG） |
| `confidence` | float | `0.8` | 匹配置信度（0.0 ~ 1.0） |

**回傳：**
```json
{ "found": true, "x": 100, "y": 200, "width": 50, "height": 50 }
```
或 `{ "found": false }`

---

### `browser_get_pixel_color(x, y)`

取得指定座標的像素 RGB 顏色。

**回傳：** `{ "r": 255, "g": 255, "b": 255 }`

---

### `browser_activate_window(title_substring)`

根據視窗標題切換焦點。

| 參數 | 類型 | 說明 |
|------|------|------|
| `title_substring` | str | 視窗標題部分匹配 |

---

## 生命週期

```
browser_start() → 操作中 → browser_stop()
```

- 啟動一次後可執行多次操作（點擊、輸入、截圖等）
- 不會自動關閉，由 Agent 手動控制
- 多會話請使用不同 `display` 編號（如 `:99`、`:100`）

---

## 使用範例

### 瀏覽小紅書並截圖

```python
browser_start(url="https://www.xiaohongshu.com/explore")
time.sleep(3)  # 等待頁面載入
browser_scroll(clicks=-3)  # 往下滾
browser_snapshot()  # 截圖
browser_stop()
```

### 搜尋並點擊 X/Twitter

```python
browser_start(url="https://x.com")
time.sleep(2)
browser_click(600, 200)  # 點擊搜尋框
browser_type("AI news", wpm=60)
browser_hotkey(["enter"])
time.sleep(3)
browser_snapshot()
browser_stop()
```

---

## 安全

- **Failsafe：** 滑鼠移動到右下角（1199, 719）會立即中止所有操作
- **不自動關閉：** 瀏覽器保持開啟直到明確呼叫 `browser_stop()`
- **獨立顯示：** 每個會話獨立 X Server，互不干擾

---

## 故障排除

| 問題 | 解決方法 |
|------|----------|
| `Missing system dependencies: Xvfb` | `apt-get install -y xvfb` |
| `Missing system dependencies: chromium-browser` | `apt-get install -y chromium-browser` |
| PyAutoGUI 報錯（DISPLAY 未設置） | 確認 `browser_start()` 已呼叫且 Xvfb 正在執行 |
| 圖像匹配失敗 | 使用高對比度模板圖，調整 `confidence` 降低閾值 |
| Chromium 無法啟動 | 確認 `libnss3`、`libgconf-2-4` 等圖形依賴已安裝 |

---

## 倉庫結構

```
virtual-desktop-browser-skill/
├── README.md          # 主說明文件（中文）
├── docs/
│   ├── en.md          # English
│   ├── es.md          # Español
│   └── ar.md          # العربية
├── SKILL.md           # 技能觸發描述
├── skill.py           # 核心實作
├── requirements.txt   # Python 依賴
└── .gitignore
```

---

## 作者

Creator: **Allen Niu**

## 授權

MIT-0（自由使用、修改、再發佈，不需署名）
