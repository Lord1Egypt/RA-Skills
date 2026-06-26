# Workflow: 抓取列出今日中國宏觀新聞消息

本工作流程說明如何使用腳本抓取並篩選中國宏觀經濟新聞。

## Step 1: 執行抓取腳本

**基本用法：**

```bash
# 從華爾街日報抓取宏觀新聞（預設使用宏觀關鍵字）
python scripts/fetch_china_macro_news.py --source wallstreetcn --limit 15

# 多源掃描
python scripts/fetch_china_macro_news.py --source all --limit 10

# 深度抓取（下載文章正文）
python scripts/fetch_china_macro_news.py --source wallstreetcn --limit 10 --deep
```

**自訂關鍵字：**

```bash
# 只看央行相關
python scripts/fetch_china_macro_news.py --keyword "央行,PBOC,利率,LPR,MLF"

# 只看數據相關
python scripts/fetch_china_macro_news.py --keyword "PMI,CPI,PPI,GDP"
```

## Step 2: 解析輸出

腳本輸出 JSON 陣列，每個項目包含：

```json
{
  "source": "Wall Street CN",
  "title": "央行今日開展 5000 億 MLF 操作",
  "url": "https://wallstreetcn.com/articles/...",
  "time": "09:45",
  "content": "（深度抓取時才有）文章正文內容..."
}
```

## Step 3: AI 解讀與報告生成

根據抓取結果，生成財經雜誌風格的報告：

1. **分類整理**：
   - 頭條焦點（最重要的 3-5 條）
   - 央行與貨幣政策
   - 經濟數據解讀
   - 市場動態

2. **單條新聞格式**：
   - 標題（Markdown 連結）
   - Metadata（來源、時間）
   - 一句話摘要
   - 深度解讀（2-3 bullet points）

3. **儲存報告**：
   - 存到 `reports/china_macro_YYYYMMDD_HHMM.md`

## 預設宏觀關鍵字

腳本預設使用以下關鍵字：

```
央行,PBOC,利率,LPR,MLF,降息,降準,
GDP,PMI,CPI,PPI,通膨,通縮,
經濟,宏觀,財政,貨幣政策,
貿易,進出口,順差,逆差,
就業,失業,消費,零售,
房地產,樓市,投資,基建,
人民幣,匯率,外匯,
債券,國債,信貸,社融,M2
```

## 成功標準

- [ ] 成功從至少一個來源抓取新聞
- [ ] 篩選出宏觀相關新聞（至少 5 條）
- [ ] 輸出格式正確（JSON 陣列）
- [ ] 報告以財經雜誌風格呈現
- [ ] 每條新聞都有原文連結
