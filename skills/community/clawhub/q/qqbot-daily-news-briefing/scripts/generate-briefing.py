#!/usr/bin/env python3
"""
Daily News Generator - v6.0 (Baidu + DuckDuckGo Fallback)
Supports both Baidu API (preferred) and DuckDuckGo web search (fallback).
Automatically falls back to DuckDuckGo if Baidu API key is not configured.
"""

import json
import subprocess
import datetime
import os
import sys
import urllib.request
import re

WORKSPACE = '/root/.openclaw/workspace'
NEWS_FILE = f"{WORKSPACE}/daily-news-2026{datetime.date.today().strftime('%m%d')}.md"
LOG_FILE = '/var/log/daily-news.log'

def log(message):
    """Log to both console and file"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line + '\n')
    except:
        pass

def search_baidu(query, count=5, freshness="pd"):
    """Search using Baidu API (requires BAIDU_API_KEY env var)"""
    try:
        api_key = os.environ.get('BAIDU_API_KEY', '')
        
        if not api_key or len(api_key) < 20:
            log(f"⚠️ Baidu API key not set or invalid (length: {len(api_key)})")
            return None, "no_api_key"
        
        search_payload = json.dumps({
            "query": query,
            "count": count,
            "freshness": freshness
        }, ensure_ascii=False)
        
        env = os.environ.copy()
        env['BAIDU_API_KEY'] = api_key
        log(f"🔍 Baidu search: '{query[:50]}...' (API key length: {len(api_key)})")
        
        result = subprocess.run(
            ['python3', f'{WORKSPACE}/skills/baidu-search/scripts/search.py', search_payload],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout.strip():
            results = json.loads(result.stdout)
            if isinstance(results, list) and len(results) > 0:
                log(f"✅ Found {len(results)} results from Baidu")
                return results, "success"
        
        error_msg = result.stderr[:200] if result.stderr else "Unknown error"
        log(f"⚠️ Baidu search failed: {error_msg}")
        return [], "api_error"
        
    except subprocess.TimeoutExpired:
        log(f"⏱️ Baidu search timed out for '{query}'")
        return [], "timeout"
    except json.JSONDecodeError as e:
        log(f"❌ JSON decode error in Baidu search: {e}")
        return [], "json_error"
    except Exception as e:
        log(f"❌ Error in Baidu search: {e}")
        return [], "unknown_error"


def search_duckduckgo(query, count=5):
    """Search using DuckDuckGo HTML API (no API key required)"""
    try:
        import urllib.parse
        
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}&kl=us-en"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
        
        results = []
        
        # Pattern for DuckDuckGo result links and titles
        pattern = r'<a\s+rel="nofollow"\s+class="result__a"\s+href="([^"]+)">([^<]+)</a>'
        matches = re.findall(pattern, html_content)
        
        for href, title in matches[:count]:
            # Decode URL-encoded characters in title
            try:
                title = urllib.parse.unquote(title)
            except:
                pass
            
            title = title.strip()
            if not title or len(title) < 5:
                continue
            
            results.append({
                'title': title,
                'url': href,
                'content': f"搜索关键词：{query}. 点击查看完整报道。",
                'website': 'DuckDuckGo',
                'date': datetime.date.today().strftime('%Y-%m-%d')
            })
        
        if results:
            log(f"✅ Found {len(results)} results from DuckDuckGo for '{query[:30]}...'")
        
        return results, "success" if results else "no_results"
        
        if results:
            log(f"✅ Found {len(results)} results from DuckDuckGo for '{query[:30]}...'")
        
        return results, "success" if results else "no_results"
        
    except Exception as e:
        log(f"❌ DuckDuckGo search failed for '{query}': {e}")
        return [], "error"


def smart_search(query, count=5, freshness="pd"):
    """
    Intelligent search with automatic fallback.
    Priority: Baidu API (if configured) → DuckDuckGo (always available)
    """
    log(f"🔍 Searching for: '{query}'")
    
    # Try Baidu first
    baidu_results, baidu_status = search_baidu(query, count, freshness)
    
    if baidu_status == "success":
        return baidu_results, "baidu"
    elif baidu_status == "no_api_key":
        log(f"ℹ️ No Baidu API key configured, falling back to DuckDuckGo")
    else:
        log(f"⚠️ Baidu search failed ({baidu_status}), trying DuckDuckGo...")
    
    # Fall back to DuckDuckGo
    ddg_results, ddg_status = search_duckduckgo(query, count)
    
    if ddg_status == "success":
        return ddg_results, "duckduckgo"
    
    # Both failed - return empty with fallback content indicator
    log(f"⚠️ All search methods failed for '{query}'")
    return [], "both_failed"


def _generate_tech_commentary(news_item):
    """Generate professional AI commentary for tech news."""
    title = news_item.get('title', '').lower()
    content = (news_item.get('content', '') or '').lower()
    
    rules = [
        (['英伟达', 'nvidia', 'gpu', '芯片'], 
         "产业链影响分析：建议关注台積電產能變化對 AI 芯片供應鏈的影響。作為金融 IT 架構師，可提前評估相關硬件成本對數據中心預算的潛在影響。"),
        (['小米', '雷軍', 'xiaomi'], 
         "企業戰略解讀：2000 億研發投入體現小米從消費電子向硬核科技的轉型決心。芯片+AI+ 汽車三線並進，生態護城河戰略清晰。"),
        (['tesla', 'spacex', '马斯克'], 
         "算力佈局信號：Tesla+SpaceX 聯合建廠意味著 Musk 正在構建獨立於英偉達的算力生態。太空計算 + 自動駕駛雙輪驅動，可能重塑 AI 芯片格局。"),
        (['openai', '聚變', 'fusion', '能源'], 
         "能源×AI 交叉點：算力的瓶頸正在從芯片轉向電力。OpenAI 布局聚變能源預示着 AI 產業鏈的下一波競爭焦點。"),
        (['ai', '人工智能', '大模型', 'llm'], 
         "產業化領先信號：中國 AI 從追趕者變為定義者。應用層爆發背後是工程化能力和場景優勢的體現。"),
        (['芯片', '半導體', 'semiconductor', '台積電'], 
         "硬件層面動態，建議關注供應鏈和資本層面的後續影響。"),
        (['broadcom', '博通'], 
         "美國 AI 芯片巨頭表現強勁，顯示全球 AI 基礎設施投資持續增長。"),
    ]
    
    for keywords, commentary in rules:
        if any(k in title or k in content for k in keywords):
            return commentary
    
    return "科技動態追蹤中...此新聞值得持續關注後續發展及產業影響。"


def _generate_finance_commentary(news_item):
    """Generate professional AI commentary for finance news."""
    title = news_item.get('title', '').lower()
    content = (news_item.get('content', '') or '').lower()
    
    rules = [
        (['a 股', '上證', '滬深'], 
         "市場觀測：關注成交量和板塊輪動，重視持續性和驅動力。建議結合宏觀環境綜合判斷。"),
        (['跌', '調整', '回調', '大跌'], 
         "市場觀測：調整伴隨資金輪動，深調往往是中長期配置機會。注意區分正常回調和趨勢反轉。"),
        (['中金', '國泰君安', '券商'], 
         "機構觀點：券商研究偏中長期視角，注意利益衝突。建議交叉驗證多個來源。"),
        (['美股', '納斯', 'nasdaq', '道瓊斯'], 
         "全球市場聯動：美股表現影響 A 股情緒，關注科技巨頭動向和宏觀數據。"),
        (['美联储', 'fed', '利率', '加息', '降息'], 
         "宏觀政策信號：美联储政策直接影響全球流動性和風險資產定價。密切關注 FOMC 會議。"),
        (['比特幣', 'crypto', '加密'], 
         "數字資產動態：加密市場波動性高，建議作為分散投資組合的一部分而非核心持倉。"),
    ]
    
    for keywords, commentary in rules:
        if any(k in title or k in content for k in keywords):
            return commentary
    
    return "財經資訊追蹤，建議結合宏觀環境和個人風險偏好綜合判斷。"


def generate_news():
    """Main news generation function with smart search fallback."""
    today = datetime.date.today()
    
    # Track which search method is being used
    search_method = None
    
    log("=" * 60)
    log(f"🚀 Starting news generation for {today} (v6.0 with Baidu/DuckDuckGo)")
    log("=" * 60)
    
    try:
        with open(NEWS_FILE, 'w', encoding='utf-8') as f:
            f.write("# 📰 Daily Briefing - Tech & Financial News\n")
            f.write(f"*Generated by Jarvis • {today.strftime('%Y年%m月%d日')}*\n\n")
            f.write("---\n\n")
            
            # === 1. CHINA TECH NEWS ===
            f.write("## 🖥️ 中国科技新闻\n\n")
            china_tech, method = smart_search('科技新闻 人工智能 芯片 AI 华为', count=3)
            search_method = method if search_method is None else search_method
            
            if china_tech:
                for i, item in enumerate(china_tech, 1):
                    f.write(f"### {i}. **{item['title']}**\n")
                    f.write(f"- **Source:** {item.get('website', 'Unknown')} | **Date:** {item.get('date', today)}\n\n")
                    
                    content = item.get('content', '')[:600]
                    if content:
                        paragraphs = [p.strip() for p in content.split('\n') if p.strip()][:3]
                        f.write('\n\n'.join(paragraphs))
                    
                    f.write("\n\n> 💡 **Jarvis 點評:** ")
                    f.write(_generate_tech_commentary(item))
                    
                    if item.get('url'):
                        f.write(f"\n\n🔗 [Read more]({item['url']})")
                    
                    f.write("\n\n---\n\n")
            else:
                f.write("⚠️ *中國科技新聞暫不可獲取，請檢查網絡連接*\n\n")
            
            # === 2. INTERNATIONAL TECH NEWS ===
            f.write("\n## 🌍 国际科技新闻\n\n")
            intl_tech, _ = smart_search('NVIDIA Broadcom Apple Microsoft AI 美股科技股', count=3)
            
            if intl_tech:
                for i, item in enumerate(intl_tech, 1):
                    f.write(f"### {i}. **{item['title']}**\n")
                    f.write(f"- **Source:** {item.get('website', 'Unknown')} | **Date:** {item.get('date', today)}\n\n")
                    
                    content = item.get('content', '')[:600]
                    if content:
                        paragraphs = [p.strip() for p in content.split('\n') if p.strip()][:3]
                        f.write('\n\n'.join(paragraphs))
                    
                    f.write("\n\n> 💡 **Jarvis 點評:** ")
                    f.write(_generate_tech_commentary(item))
                    
                    if item.get('url'):
                        f.write(f"\n\n🔗 [Read more]({item['url']})")
                    
                    f.write("\n\n---\n\n")
            else:
                f.write("⚠️ *國際科技新聞暫不可獲取*\n\n")
            
            # === 3. CHINA FINANCIAL NEWS ===
            f.write("\n## 📈 中国金融市场\n\n")
            china_finance, _ = smart_search('A 股 上证指数 港股 财经', count=3)
            
            if china_finance:
                for i, item in enumerate(china_finance, 1):
                    f.write(f"### {i}. **{item['title']}**\n")
                    f.write(f"- **Source:** {item.get('website', 'Unknown')} | **Date:** {item.get('date', today)}\n\n")
                    
                    content = item.get('content', '')[:600]
                    if content:
                        paragraphs = [p.strip() for p in content.split('\n') if p.strip()][:3]
                        f.write('\n\n'.join(paragraphs))
                    
                    f.write("\n\n> 💡 **Jarvis 點評:** ")
                    f.write(_generate_finance_commentary(item))
                    
                    if item.get('url'):
                        f.write(f"\n\n🔗 [Read more]({item['url']})")
                    
                    f.write("\n\n---\n\n")
            else:
                f.write("⚠️ *中國財經新聞暫不可獲取*\n\n")
            
            # === 4. INTERNATIONAL FINANCE NEWS ===
            f.write("\n## 💹 国际金融市场\n\n")
            intl_finance, _ = smart_search('美股 纳斯达克 道琼斯 美联储 原油 比特币', count=3)
            
            if intl_finance:
                for i, item in enumerate(intl_finance, 1):
                    f.write(f"### {i}. **{item['title']}**\n")
                    f.write(f"- **Source:** {item.get('website', 'Unknown')} | **Date:** {item.get('date', today)}\n\n")
                    
                    content = item.get('content', '')[:600]
                    if content:
                        paragraphs = [p.strip() for p in content.split('\n') if p.strip()][:3]
                        f.write('\n\n'.join(paragraphs))
                    
                    f.write("\n\n> 💡 **Jarvis 點評:** ")
                    f.write(_generate_finance_commentary(item))
                    
                    if item.get('url'):
                        f.write(f"\n\n🔗 [Read more]({item['url']})")
                    
                    f.write("\n\n---\n\n")
            else:
                f.write("⚠️ *國際財經新聞暫不可獲取*\n\n")
            
            # Footer with search method info
            f.write("---\n\n")
            method_note = "Baidu API" if search_method == "baidu" else "DuckDuckGo"
            f.write(f"*Delivered by Jarvis • {today.strftime('%m月%d日')}*\n")
            f.write(f"*Search source: {method_note}*\n")
            f.write("*Next briefing: Tomorrow at scheduled time*\n")
        
        file_size = os.path.getsize(NEWS_FILE)
        log(f"✅ News file created: {NEWS_FILE} ({file_size:,} bytes)")
        log(f"📊 Search method used: {search_method}")
        return True
        
    except Exception as e:
        log(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = generate_news()
    sys.exit(0 if success else 1)
