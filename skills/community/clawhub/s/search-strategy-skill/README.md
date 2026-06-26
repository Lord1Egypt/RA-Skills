# 智能搜尋策略 (search-strategy)

自動選擇最佳搜尋工具的 OpenClaw 技能 - 無需再煩惱用哪個搜尋工具！

## ✨ 功能特色

- 🎯 **智能工具選擇**：根據搜尋需求自動判斷最佳工具
- 🔄 **自動 Fallback**：工具失敗時自動切換備援方案
- 🛠 **強制指定引擎**：支援 `--engine` 參數覆寫自動判斷
- 📊 **多種輸出格式**：支援 `--json` 選項
- 🎨 **彩色終端輸出**：清晰的狀態提示

## 📦 安裝

### 方法一：ClawHub 安裝（推薦）
```bash
clawhub install search-strategy
```

### 方法二：手動安裝
1. 將技能資料夾複製到 `~/.openclaw/workspace/skills/`
2. 設定執行權限：
```bash
chmod +x ~/.openclaw/workspace/skills/search-strategy/scripts/search-strategy
```

## 🔧 所需 API Keys

| 工具 | API Key | 用途 |
|------|---------|------|
| jina.ai | 無 | 單篇文章快速讀（免費，每月約 2k 次） |
| firecrawl-cli | `FIRECRAWL_API_KEY` | JS 網站完整爬蟲（免費 500k credits） |
| tavily-search | `TAVILY_API_KEY` | AI 最佳化研究摘要（每月 1k 次） |
| brave-search | `BRAVE_API_KEY` | 隱私搜尋 |
| agent-reach | 各平台 OAuth | Twitter/YouTube/GitHub 等社群媒體 |

**設定環境變數：**
```bash
export FIRECRAWL_API_KEY="your-key"
export TAVILY_API_KEY="your-key"
export BRAVE_API_KEY="your-key"
```

## 🚀 使用方法

### 基本搜尋（自動選擇工具）
```bash
search-strategy query="OpenClaw AI 工具介紹"
```

### 單篇文章閱讀
```bash
search-strategy url="https://example.com/article"
```

### 強制使用特定引擎
```bash
search-strategy query="科技新聞" --engine=jina
search-strategy query="完整網站資料" --engine=firecrawl
```

### 完整爬蟲模式
```bash
search-strategy query="股市行情" --full-crawl
```

### JSON 輸出
```bash
search-strategy query="比特幣價格" --json
```

### 詳細模式
```bash
search-strategy query="AI 新聞" --verbose
```

## 🧠 內部決策邏輯

```
開始
  ├─ 有 URL 參數？
  │     → 是 → jina.ai（單篇文章快速讀）
  │
  ├─ 使用 --full-crawl flag？
  │     → 是 → firecrawl（完整爬蟲）
  │
  ├─ query 包含 "完整"、"全部"、"爬蟲"？
  │     → 是 → firecrawl
  │
  ├─ query 包含 "比較"、"比價"、"多個來源"？
  │     → 是 → multi-search-engine
  │
  ├─ query 包含 "研究"、"摘要"、"報告"？
  │     → 是 → tavily-search
  │
  ├─ query 包含平台名稱（Twitter/YouTube/GitHub）？
  │     → 是 → agent-reach
  │
  └─ 其他 → jina.ai（預設）
```

## 📊 工具對照表

| 工具 | API Key | 最佳場景 | 限制 |
|------|---------|----------|------|
| jina.ai | ❌ 無需 | 單篇文章快速讀 | 每月約 2k 次 |
| firecrawl-cli | 🔑 Firecrawl | JS 網站、完整爬蟲 | 免費 500k credits |
| tavily-search | 🔑 Tavily | AI 最佳化研究摘要 | 每月 1k 次 |
| multi-search-engine | ❌ 無需 | 多引擎比價 | 前端渲染可能被 block |
| brave-search | 🔑 Brave | 隱私搜尋、乾淨結果 | 需設定 BRAVE_API_KEY |
| agent-reach | 🔑 各平台 | 社群媒體（Twitter/YouTube） | 安全風險高 |

## 🔍 搜尋技巧

### 關鍵字策略
- 🔄 **搜尋失敗 → 換關鍵字，不要一直 retry**
- 🇨🇳 **中文搜尋**：優先用百度、必應中國、360、Sogou
- 🇺🇸 **英文搜尋**：優先用 Google、DuckDuckGo、Startpage
- ⏰ **時間濾波**：`tbs=qdr:d/w/m`（過去1天/1周/1月）
- 🔍 **站點限定**：`site:example.com keyword`

### jina.ai 快捷方式
```bash
# 取得任何網頁乾淨內容
https://r.jina.ai/http://URL
https://r.jina.ai/http://github.com/.../releases
```

## 📝 示例

```bash
# 快速讀取新聞
search-strategy url="https://technews.tw/2026/03/16/ai-news"

# 研究某主題
search-strategy query="2026 AI 趨勢報告" --engine=tavily

# 比價商品
search-strategy query="iPhone 16 價格 比較" --engine=multi

# 爬取完整網站
search-strategy url="https://blog.example.com" --engine=firecrawl

# 社群媒體搜尋
search-strategy query="YouTube: OpenClaw 介紹" --engine=agent
```

## ⚠️ 注意事項

1. **全文閱讀原則**：重要新聞一定要看全文，避免 AI 幻覺
2. **多管道驗證**：重大事件請交叉檢查 2-3 個來源
3. **額度管理**：jina.ai 每月約 2k 次免費額度，大量使用請切換 firecrawl
4. **API Key 安全**：不要將 API Key 提交到版本控制系統

## 🐛 問題回報

如有問題，請提交 Issue 到技能倉庫，或聯繫作者。

## 📄 授權

MIT License - 詳見 [LICENSE](LICENSE) 文件

---

**版本：** 1.0.0  
**作者：** Shuttle AI (OpenClaw)  
**更新日期：** 2026-03-16
