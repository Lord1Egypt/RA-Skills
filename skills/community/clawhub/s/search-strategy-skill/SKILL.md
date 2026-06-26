---
name: search-strategy
version: 1.1.0
description: "智能搜尋策略執行器 - 自動選擇最佳搜尋工具，無需手動判斷。"
homepage: https://github.com/openclaw/openclaw
---

# 搜尋策略技能 (search-strategy)

## 技術架構與流程

### 核心設計理念
- **智慧決策層**：根據任務類型自動選擇最佳工具
- **工具適配層**：統一不同搜尋工具的輸出格式
- **錯誤恢復層**：多級 fallback 確保任務完成
- **效能優化層**：避免不必要的 API 調用

### 決策樹算法（實作細節）

```bash
# 主要判斷邏輯（from_task_type 函數）
if [ -n "$URL" ]; then
    # URL 模式：單篇文章閱讀
    tool="jina"
    
    # 檢查是否需要瀏覽器自動化
    if [ "$FORCE_BROWSER" = "1" ] || needs_browser_automation "$URL"; then
        tool="browser"
    fi
elif echo "$QUERY" | grep -qiE "完整|全部|爬蟲|網站|crawl"; then
    tool="firecrawl"
elif echo "$QUERY" | grep -qiE "\.tw|\.com|股價|股價|[0-9]+\.?[0-9]*"; then
    # 特定模式：台灣市場資料
    tool="multi"
elif echo "$QUERY" | grep -qiE "研究|報告|摘要|分析|AI"; then
    tool="tavily"
elif echo "$QUERY" | grep -qiE "Twitter|YouTube|GitHub|Facebook|IG|小紅書"; then
    tool="agent"
elif echo "$QUERY" | grep -qiE "中文|中國|台灣|大陸"; then
    # 中文搜尋优先用 Brave（廣告少、無追蹤）
    tool="brave"
else
    # 預設：jina.ai 快速摘要
    tool="jina"
fi
```

### 各工具調用方式

#### 1. jina.ai 摘要模式（url 模式）
```bash
# 基本原理：利用 jina.ai 的 Reader API 提取網頁乾淨內容
# API: https://r.jina.ai/http://目標URL
result=$(curl -s -H "Accept: text/markdown" "https://r.jina.ai/http://${URL}" 2>/dev/null)

# 優點：
# - 無需 API Key
# - 自動移除廣告、腳本、追蹤碼
# - 支援 JavaScript 渲染頁面（jina.ai 內部有 headless browser）
# - 輸出乾淨的 Markdown 格式
```

#### 2. Multi-Search-Engine（多引擎比價）
```bash
# 原始方法（已棄用）：直接 curl Google/Bing（會動態渲染，失效）
# curl -s "https://www.google.com/search?q=$QUERY"

# 新方法（優化後）：使用自建代理或 fearless 替代方案
for engine in "duckduckgo" "brave" "startpage"; do
    case $engine in
        duckduckgo)
            # DuckDuckGo HTML 解析 logic
            curl -s "https://html.duckduckgo.com/html/?q=$QUERY" |
                grep -E 'class="result__url"' |
                sed -n 's/.*class="result__url"[^>]*>\([^<]*\)<\/div>.*/\1/p'
            ;;
        brave)
            # 自建 Brave Search 代理
            curl -s "https://search.brave.com/search?q=$QUERY" \
                 -H "User-Agent: Mozilla/5.0..."
            ;;
    esac
done

# 解析各引擎結果，统一格式為:
# === 搜尋引擎名稱 ===
# 1. 標題
#    链接: https://...
#    摘要: ...
```

#### 3. Firecrawl 完整爬蟲
```bash
# 使用 firecrawl-cli（Node.js 工具）
# 功能：完整爬取網站、支援 JS 渲染、提取結構化資料

firecrawl scrape "$URL" \
  --wait-for 3000 \          # 等待 3 秒確保動態內容載入
  --limit 100 \              # 最多爬 100 個頁面
  --output-format markdown   # 輸出 Markdown

# 或使用 API 模式（FIRECRAWL_API_KEY）
firecrawl search "$QUERY" \
  --scrape \                 # 自動爬取搜尋結果頁面
  --json \                   # 輸出結構化 JSON
  --limit 50
```

#### 4. Tavily AI 最佳化搜尋
```bash
# Tavily 专為 LLM 設計的搜尋 API
# 特色：一次搜尋返回多個來源的摘要，適合 research 任務

tavily-search query="$QUERY" \
  max_results=10 \            # --max 參數控制結果數
  include_answer=true \       # 包含 AI 生成的摘要
  search_depth="advanced" \   # 深度搜尋模式
  include_raw_content=false   # 只返回 cleaned content

# 輸出格式：
# {
#   "answer": "AI 生成的綜合摘要...",
#   "results": [
#     { "title": "...", "url": "...", "content": "..." }
#   ]
# }
```

#### 5. Browser-Automation（瀏覽器自動化）
```bash
# 基於 Playwright，支援 Chromium/Firefox/WebKit
# 實作函數: search_with_browser()

# 主要流程：
# 1. 啟動瀏覽器（复用現有 page）
# 2. 導航到目標 URL
# 3. 等待元素載入（智能等待）
# 4. 提取內容或截圖
# 5. 關閉瀏覽器（可選是否保持）

# 實作例子：
node -e "
const browserAuto = require('$BROWSER_SKILL_PATH/index.js');
browserAuto.navigate({
    url: process.env.TARGET_URL,
    waitUntil: 'networkidle',
    timeout: 30000
}).then(page => {
    const content = page.mainFrame().content();
    console.log(content);
    if (process.env.TAKE_SCREENSHOT === '1') {
        return page.screenshot({ path: './screenshot.png' });
    }
});
"
```

### 錯誤處理與 Fallback 機制

#### Set -e 問題及解決方案
```bash
# 問題：set -e 在 log_debug 函數中會因 [ "$VERBOSE" -eq 1 ] 返回 1 而退出
# 解法：改用 if 結構避免 set -e 中斷

log_debug() {
    if [ "$VERBOSE" -eq 1 ]; then
        echo "[DEBUG] $*" >&2
    fi
}

# 另一個陷阱：函數外的 local 變數声明
# 錯誤：local STATUS   ← 在函數外使用
# 修正：移除函數外的 local，只在函數內使用
```

#### 多級 Fallback 策略
```bash
# 當主要工具失敗時，按順序嘗試備用方案
fallback_chain() {
    local primary=$1
    local url=$2
    
    case $primary in
        jina)
            # jina 失效時：嘗試 multi-search-engine
            search_with_multi "$url" && return 0
            # 再不成就用 browser
            search_with_browser "$url" && return 0
            ;;
        brave)
            # Brave API 失效：換 DuckDuckGo
            search_with_duckduckgo "$url" && return 0
            ;;
        multi)
            # Multi 失效：直接 brave-search 命令
            brave-search query="$QUERY" && return 0
            ;;
        *)
            # 最後手段：curl + grep 粗暴抓取
            curl -s "$url" | lynx -stdin
            ;;
    esac
    
    return 1  # 所有方案都失敗
}
```

### 輸出格式美化

```bash
# 彩色輸出（ANSI escape codes）
RED='\033[0;31m'      # 錯誤/警示
GREEN='\033[0;32m'    # 成功
YELLOW='\033[1;33m'   # 警告/提示
BLUE='\033[0;34m'     # 資訊
NC='\033[0m'          # 重置顏色

# 輸出示例：
echo -e "${BLUE}[INFO]${NC} 自動分析任務類型..."
echo -e "${YELLOW}[WARN]${NC} jina.ai 不支援直接搜尋，改用 multi-search-engine"
echo -e "${GREEN}[SUCCESS]${NC} 搜尋完成（工具: $tool）"

# 分隔線與圖示
echo "🔍 搜尋關鍵字: $QUERY"
echo "=== Google 搜尋 ==="
echo "=== Bing 搜尋 ==="
```

### 參數解析流程

```bash
# 1. 解析所有參數
while [[ $# -gt 0 ]]; do
    case $1 in
        query=*)
            QUERY="${1#query=}"
            ;;
        url=*)
            URL="${1#url=}"
            ;;
        --engine=*)
            ENGINE="${1#--engine=}"
            ;;
        --full-crawl)
            FULL_CRAWL=1
            ;;
        --browser)
            FORCE_BROWSER=1
            ;;
        --screenshot)
            TAKE_SCREENSHOT=1
            ;;
        --max=*)
            MAX_RESULTS="${1#--max=}"
            ;;
        --verbose)
            VERBOSE=1
            ;;
        --json)
            JSON_OUTPUT=1
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            log_error "未知參數: $1"
            exit 1
            ;;
    esac
    shift
done

# 2. 參數驗證
if [ -z "$QUERY" ] && [ -z "$URL" ]; then
    log_error "必須提供 query 或 url 參數"
    show_help
    exit 1
fi

# 3. 決定工具
if [ -n "$ENGINE" ]; then
    # 強制使用指定引擎
    tool="$ENGINE"
else
    # 智慧決策
    tool=$(from_task_type "$QUERY" "$URL")
fi

# 4. 調用對應函數
case $tool in
    jina)        search_with_jina "$URL" ;;
    multi)       search_with_multi "$QUERY" ;;
    firecrawl)   search_with_firecrawl "$URL" ;;
    tavily)      search_with_tavily "$QUERY" ;;
    brave)       search_with_brave "$QUERY" ;;
    agent)       search_with_agent "$QUERY" ;;
    browser)     search_with_browser "$URL" ;;
    *)           log_error "不支援的工具: $tool"; exit 1 ;;
esac
```

### 效能優化技巧

1. **並行搜尋**（multi 模式）：
```bash
# 同時發送多個引擎請求，等待最快的結果
for engine in "${ENGINES[@]}"; do
    {
        result=$(search_$engine "$QUERY" 2>/dev/null)
        if [ -n "$result" ]; then
            echo "$result"
            break
        fi
    } &
done
wait
```

2. **快取機制**：
```bash
CACHE_KEY=$(echo "$QUERY" | md5sum | cut -d' ' -f1)
CACHE_FILE="/tmp/search-cache-$CACHE_KEY.json"

if [ -f "$CACHE_FILE" ] && [ $(($(date +%s) - $(stat -c %Y "$CACHE_FILE"))) -lt 3600 ]; then
    cat "$CACHE_FILE"  # 使用 1 小時內的快取
else
    # ... 執行搜尋 ...
    echo "$result" > "$CACHE_FILE"
fi
```

3. **限流保護**：
```bash
# 記錄 API 調用次數，避免超過免費額度
CALL_COUNT_FILE="/tmp/api-call-count.json"
# 每日重置計數
```

## 调试與监控

### 開啟 debug 模式
```bash
search-strategy query="test" --verbose
# 會顯示：
# [DEBUG] 參數解析: QUERY="test", URL="", ENGINE=""
# [DEBUG] 工具選擇: jina
# [DEBUG] 調用函數: search_with_jina
# [DEBUG] API 請求: https://r.jina.ai/http://...
```

### 查看執行時間
```bash
time search-strategy query="OpenClaw AI"
# real    0m2.345s
# user    0m0.123s
# sys     0m0.045s
```

### 日誌位置
- 腳本內部 debug：輸出到 stderr
- 執行歷史：`~/.openclaw/logs/search-strategy-YYYY-MM-DD.log`
- 錯誤報告：单独捕捉到 `~/.openclaw/workspace/search-errors.log`

## 最佳實踐建議

1. **小批量測試**：先用 `--verbose` 確認工具選擇正確
2. **混合使用**：重大資料用 `multi` 交叉驗證，一般閱讀用 `jina`
3. **尊重額度**：firecrawl/tavily 有付费限制，先用免費工具
4. **錯誤報告**：如果 fallback 到瀏覽器模式，表示該網站需要特殊處理，可回報給技能作者優化

## 未来規劃（Roadmap）

- [ ] 支援更多搜尋引擎（Yahoo、Yandex、搜狗）
- [ ] 自動化瀏覽器爬蟲的隊列管理（避免 ProcessSingleton 衝突）
- [ ] 整合 ocr 功能（識別圖片中的文字）
- [ ] 結構化輸出（CSV、Excel、Notion API）
- [ ] 語音朗讀整合（使用 TTS 技能）
- [ ] 批量搜尋（從檔案讀取多個 query）
- [ ] 訂閱式搜尋（定期執行並推送更新）

---

## 附錄：工具對比表

| 工具 | 適用場景 | 速度 | 免費額度 | 缺點 |
|------|---------|------|---------|------|
| jina.ai | 單篇文章閱讀 | ⚡⚡⚡ | 2k/月 | 不能直接搜尋 |
| multi | 多源比價 | ⚡⚡ | 無限制 | 需解析 HTML，可能失效 |
| firecrawl | 完整網站爬蟲 | ⚡ | 500k credits | 需 API Key |
| tavily | AI 研究摘要 | ⚡⚡ | 1k/月 | 付费后才好用 |
| brave | 乾淨搜尋 | ⚡⚡⚡ | 2k/月 | 需 API Key |
| browser | 動態/登入頁面 | ⚡ | 無限制 | 資源消耗大 |
| agent | 社群平台 | ⚡⚡ | 依平台 | 需 OAuth 設定 |
