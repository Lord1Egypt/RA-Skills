# 數據來源參考

本文件說明 Skill 使用的新聞來源及其技術細節。

## 華爾街日報（主要來源）

| 項目 | 說明                                   |
|------|----------------------------------------|
| 網站 | https://wallstreetcn.com/              |
| 類型 | 中國頂級財經媒體                       |
| 特色 | 宏觀/市場新聞即時性強，24 小時滾動更新 |
| 適用 | 央行政策、市場動態、數據解讀           |

### API 端點

```
GET https://api-one.wallstcn.com/apiv1/content/information-flow
```

**參數：**
- `channel=global-channel` - 全球頻道
- `accept=article` - 只要文章
- `limit=30` - 數量限制

**回傳欄位：**
```json
{
  "data": {
    "items": [
      {
        "resource": {
          "title": "新聞標題",
          "content_short": "摘要",
          "uri": "https://wallstreetcn.com/articles/...",
          "display_time": 1705737600
        }
      }
    ]
  }
}
```

### 時間處理

- `display_time` 是 Unix 時間戳
- 轉換為 HH:MM 格式顯示

---

## 36氪（輔助來源）

| 項目 | 說明                         |
|------|------------------------------|
| 網站 | https://36kr.com/            |
| 類型 | 科技財經媒體                 |
| 特色 | 涵蓋科技、創投、經濟政策快訊 |
| 適用 | 經濟政策、產業動態           |

### 抓取頁面

```
GET https://36kr.com/newsflashes
```

### 選擇器

```python
SELECTORS = {
    "items": ".newsflash-item",
    "title": ".item-title",
    "time": ".time"
}
```

---

## 關鍵字篩選規則

### 預設宏觀關鍵字

```python
DEFAULT_MACRO_KEYWORDS = [
    # 央行與貨幣政策
    "央行", "PBOC", "利率", "LPR", "MLF", "降息", "降準",
    # 經濟數據
    "GDP", "PMI", "CPI", "PPI", "通膨", "通縮",
    # 財政與政策
    "經濟", "宏觀", "財政", "貨幣政策",
    # 貿易
    "貿易", "進出口", "順差", "逆差",
    # 就業與消費
    "就業", "失業", "消費", "零售",
    # 房地產與投資
    "房地產", "樓市", "投資", "基建",
    # 外匯
    "人民幣", "匯率", "外匯",
    # 債券與信貸
    "債券", "國債", "信貸", "社融", "M2"
]
```

### 智慧擴展規則

| 用戶輸入 | 自動擴展                         |
|----------|----------------------------------|
| 利率     | 利率,LPR,MLF,降息,加息,PBOC,央行 |
| 通膨     | 通膨,CPI,PPI,物價,通縮           |
| 貿易     | 貿易,進出口,順差,關稅,海關       |
| PMI      | PMI,製造業,服務業,採購經理人     |
| 房地產   | 房地產,樓市,房價,房貸,限購       |

---

## 深度抓取

使用 `--deep` 參數時，腳本會：

1. 訪問每篇文章的原始 URL
2. 下載 HTML 並提取正文
3. 移除 script、style、nav、footer 等元素
4. 截取前 3000 字元

### 內容提取函數

```python
def fetch_url_content(url):
    response = requests.get(url, headers=HEADERS, timeout=5)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 移除不需要的元素
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.extract()

    # 提取文字
    text = soup.get_text(separator=' ', strip=True)
    return text[:3000]
```

---

## 請求標頭

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
```

---

## 錯誤處理

| 情況         | 處理方式                   |
|--------------|----------------------------|
| API 請求失敗 | 返回空陣列，繼續下一個來源 |
| 解析失敗     | 跳過該項目，繼續處理       |
| 深度抓取超時 | content 設為空字串         |
