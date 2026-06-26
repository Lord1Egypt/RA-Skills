#!/usr/bin/env bash

# 智能搜尋策略執行器 v1.1.0
# 根據任務類型自動選擇最佳搜尋工具

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# 預設參數
QUERY=""
URL=""
ENGINE=""
FULL_CRAWL=0
VERBOSE=0
MAX_RESULTS=10

# 幫助訊息
show_help() {
    echo "智能搜尋策略執行器 v1.1.0"
    echo ""
    echo "用法:"
    echo "  search-strategy query=\"關鍵字\""
    echo "  search-strategy url=\"URL\""
    echo ""
    echo "選項:"
    echo "  --engine=TOOL    強制使用工具 (jina|multi|brave|firecrawl|tavily|agent)"
    echo "  --max NUM        最大結果數量 (預設: 10)"
    echo "  --full-crawl     完整爬蟲"
    echo "  -v, --verbose    詳細資訊"
    echo "  -h, --help       顯示此幫助"
}

# 日誌函數（使用 if 避免 set -e 退出）
log_info() {
    if [ "$VERBOSE" -eq 1 ]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_header() { echo -e "${MAGENTA}═══ $1 ═══${NC}"; }

# 1. 解析參數
while [[ $# -gt 0 ]]; do
    case $1 in
        query=*)
            QUERY="${1#query=}"
            shift
            ;;
        url=*)
            URL="${1#url=}"
            shift
            ;;
        --engine)
            if [ $# -ge 2 ]; then
                ENGINE="$2"
                shift 2
            else
                log_error "--engine 需要tool名稱"
                show_help; exit 1
            fi
            ;;
        --engine=*)
            ENGINE="${1#--engine=}"
            shift
            ;;
        --max)
            if [ $# -ge 2 ]; then
                MAX_RESULTS="$2"
                shift 2
            else
                log_error "--max 需要數字參數"
                show_help; exit 1
            fi
            ;;
        --full-crawl)
            FULL_CRAWL=1
            shift
            ;;
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -h|--help)
            show_help; exit 0
            ;;
        *)
            log_error "未知參數: $1"
            show_help
            exit 1
            ;;
    esac
done

if [ -z "$QUERY" ] && [ -z "$URL" ]; then
    log_error "必須提供 query 或 url"
    show_help; exit 1
fi

if ! [[ "$MAX_RESULTS" =~ ^[0-9]+$ ]] || [ "$MAX_RESULTS" -lt 1 ]; then
    MAX_RESULTS=10
    log_warn "無效的結果數量，使用預設值: 10"
fi

# 2. 自動選擇工具
if [ -z "$ENGINE" ]; then
    log_info "自動分析任務類型..."
    
    if [ -n "$URL" ]; then
        ENGINE="jina"
        log_info "URL → jina.ai"
    elif [ "$FULL_CRAWL" -eq 1 ]; then
        ENGINE="firecrawl"
        log_info "完整爬蟲 → firecrawl"
    else
        case "$QUERY" in
            *完整*|*全部*|*爬蟲*|*crawl*|*site*)
                ENGINE="firecrawl"
                log_info "關鍵詞：完整爬蟲 → firecrawl"
                ;;
            *比較*|*比價*|*多個來源*|*比一下*)
                ENGINE="multi"
                log_info "關鍵詞：多源比價 → multi"
                ;;
            *研究*|*摘要*|*報告*|*analysis*|*research*)
                ENGINE="tavily"
                log_info "關鍵詞：研究摘要 → tavily"
                ;;
            *Twitter*|*YouTube*|*GitHub*|*小紅書*|*抖音*|*Reddit*|*X.com*)
                ENGINE="agent"
                log_info "關鍵詞：社群平台 → agent-reach"
                ;;
            *)
                ENGINE="jina"
                log_info "預設 → jina.ai"
                ;;
        esac
    fi
fi

echo ""
log_header "搜尋任務"
echo "關鍵字: ${QUERY:-無}"
echo "URL: ${URL:-無}"
echo "工具: $ENGINE"
echo "最大結果: $MAX_RESULTS"
log_header "═══════════════════════════════════════"
echo ""

# 3. 搜尋函數

search_with_jina() {
    local target="${1:-$QUERY}"
    log_info "使用 jina.ai..."
    
    if [[ "$target" == http* ]]; then
        local jina_url="https://r.jina.ai/http://$(echo "$target" | sed -e 's|https://||' -e 's|http://||')"
        curl -s --compressed "$jina_url" 2>/dev/null | head -200
    else
        log_warn "jina.ai 不支援直接搜尋，改用 multi"
        search_with_multi
    fi
}

search_with_multi() {
    log_info "使用 DuckDuckGo..."
    
    if [ -n "$URL" ]; then
        log_info "目標 URL: $URL"
        curl -s --compressed "$URL" 2>/dev/null | head -100 || {
            log_warn "直接存取失敗，嘗試 jina.ai 代理..."
            curl -s --compressed "https://r.jina.ai/http://$(echo "$URL" | sed -e 's|https://||' -e 's|http://||')" | head -200
        }
    elif [ -n "$QUERY" ]; then
        echo "🔍 搜尋關鍵字: $QUERY"
        echo ""
        
        local ddg_url="https://html.duckduckgo.com/html/?q=$(echo "$QUERY" | sed 's/ /+/g')"
        local ddg_html=$(curl -s --compressed -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" "$ddg_url" 2>/dev/null)
        
        if [ -z "$ddg_html" ]; then
            echo "（DuckDuckGo 搜尋暫時無法取得）"
            return
        fi
        
        # 抽取並顯示結果（保留原版邏輯）
        local count=1
        echo "$ddg_html" | grep -E 'class="result__url' | head -"$MAX_RESULTS" | sed -n 's/.*href="\([^"]*\)".*/\1/p' | while read -r link; do
            echo "$count. $link"
            ((count++))
        done
        
        if [ "$count" -eq 1 ]; then
            echo "（未找到搜尋結果）"
        else
            echo ""
            echo "---"
            echo "（以上為部分搜尋結果連結）"
        fi
    fi
}

search_with_firecrawl() {
    log_info "使用 firecrawl-cli..."
    
    if ! command -v firecrawl &> /dev/null; then
        log_error "firecrawl-cli 未安裝，請: clawhub install firecrawl"
        return 1
    fi
    
    if [ -n "$URL" ]; then
        firecrawl scrape "$URL" --wait-for 3000 2>/dev/null | head -100
    elif [ -n "$QUERY" ]; then
        firecrawl search "$QUERY" --scrape 2>/dev/null | head -100
    else
        log_error "firecrawl 需要 URL 或 query"
        return 1
    fi
}

search_with_tavily() {
    log_info "使用 Tavily..."
    
    if ! command -v tavily-search &> /dev/null; then
        log_error "tavily-search 未安裝，請: clawhub install tavily-search"
        return 1
    fi
    
    if [ -z "$TAVILY_API_KEY" ]; then
        log_warn "TAVILY_API_KEY 未設定"
    fi
    
    tavily-search query="$QUERY" max_results="$MAX_RESULTS" 2>/dev/null
}

search_with_brave() {
    log_info "使用 Brave Search..."
    curl -s "https://search.brave.com/search?q=$(echo "$QUERY" | sed 's/ /+/g')" 2>/dev/null | head -100
}

search_with_agent() {
    log_info "使用 agent-reach..."
    
    if ! command -v agent-reach &> /dev/null; then
        log_error "agent-reach 未安裝，請: clawhub install agent-reach"
        return 1
    fi
    
    local platform=""
    case "$QUERY" in
        *Twitter*|*twitter*|*X.com*) platform="twitter" ;;
        *YouTube*|*youtube*) platform="youtube" ;;
        *GitHub*|*github*) platform="github" ;;
        *) platform="twitter" ;;
    esac
    
    local clean_q="${QUERY#*:}"
    [ "$clean_q" = "$QUERY" ] && clean_q="$QUERY"
    agent-reach platform="$platform" query="$clean_q" 2>/dev/null
}

# 根據 ENGINE 執行
case "$ENGINE" in
    jina) search_with_jina ;;
    multi) search_with_multi ;;
    brave) search_with_brave ;;
    firecrawl) search_with_firecrawl ;;
    tavily) search_with_tavily ;;
    agent) search_with_agent ;;
    *) log_error "未知工具: $ENGINE"; exit 1 ;;
esac

log_success "搜尋完成（工具: $ENGINE）"
