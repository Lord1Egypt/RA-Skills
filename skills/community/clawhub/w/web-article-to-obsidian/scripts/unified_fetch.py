#!/usr/bin/env python3
"""
Web Article Unified Fetcher - 网页文章一体化抓取器
集成 Playwright / Tavily / Firecrawl / HTTP 多级回退
自动平台识别、行业分类、内容清理、Obsidian双层存储

用法:
  python3 unified_fetch.py <URL> [--industry 行业] [--method playwright|tavily|firecrawl|http] [--dry-run]
"""

import asyncio
import sys
import os
import re
import time
import json
import argparse
import subprocess
from datetime import datetime
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

# ─── 配置 ──────────────────────────────────────────────

VAULT_BASE = "/root/Documents/Obsidian Vault/llm-wiki"
VAULT_RAW = os.path.join(VAULT_BASE, "raw")
VAULT_SOURCES = os.path.join(VAULT_BASE, "sources")

# 行业分类关键词
INDUSTRY_KEYWORDS = {
    'AI芯片': ['AI芯片', 'GPU', 'GPGPU', '寒武纪', '壁仞', '海光', '摩尔线程', '芯片设计', '半导体', '英伟达', 'NVIDIA'],
    'AI大模型': ['大模型', 'LLM', 'GPT', 'Claude', '通义', '文心', 'DeepSeek', 'AGI', 'OpenAI', 'Gemini'],
    '新能源': ['新能源', '宁德时代', '动力电池', '锂电池', '光伏', '风电', '储能', '电动车', '比亚迪'],
    '消费': ['消费', '白酒', '五粮液', '茅台', '啤酒', '重庆啤酒', '食品饮料', '调味品', '零售'],
    '医药': ['医药', '创新药', '医疗器械', 'CXO', '生物科技', '疫苗', '中药', '医疗'],
    '金融': ['金融', '银行', '保险', '证券', '券商', '摩根大通', '财通', '投行', '资管'],
    '互联网': ['互联网', '电商', '腾讯', '阿里', '字节', '美团', '拼多多', '软件', 'SaaS'],
    '军工': ['军工', '国防', '航天', '航空', '导弹', '雷达'],
    '汽车': ['汽车', '整车', '乘用车', '车企', '吉利', '长城', '长安'],
    '能源': ['能源', '电力', '煤炭', '石油', '天然气', '华能', '三峡'],
    '原材料': ['化工', '钢铁', '有色', '水泥', '万华', 'MDI'],
    '地产': ['地产', '房地产', '保利', '万科', '碧桂园'],
    '宏观经济': ['宏观', 'GDP', 'CPI', 'PMI', '央行', '货币政策', '财政政策', '降息', '降准'],
}

# 平台配置
PLATFORMS = {
    'wechat': {
        'pattern': r'mp\.weixin\.qq\.com',
        'scene_param': True,
        'content_selector': '#js_content',
        'title_selector': 'h1.rich_media_title',
        'author_selector': '#js_name',
        'time_selector': '#publish_time',
        'clean_nav': False,
        'display_name': '微信公众号',
    },
    'futu': {
        'pattern': r'news\.futunn\.com',
        'scene_param': False,
        'strip_tracking_params': True,  # 富途URL带大量跟踪参数，需清理
        'content_selector': '.inner.origin_content',
        'title_selector': 'h1, .news-title',
        'author_selector': '[class*="time"]',  # 包含"来源 · 时间"
        'time_selector': '[class*="time"]',
        'clean_nav': True,
        'display_name': '富途牛牛',
    },
    'xueqiu': {
        'pattern': r'xueqiu\.com',
        'scene_param': False,
        'content_selector': '.article__bd__detail',
        'title_selector': '.article__bd__title',
        'author_selector': '.user__name',
        'time_selector': '.article__bd__from',
        'clean_nav': True,
        'display_name': '雪球',
    },
    'eastmoney': {
        'pattern': r'(eastmoney\.com|finance\.sina\.com\.cn)',
        'scene_param': False,
        'content_selector': '.txtinfos, .newsContent, #ContentBody',
        'title_selector': 'h1, .title',
        'author_selector': '.source, .author',
        'time_selector': '.time, .date',
        'clean_nav': True,
        'display_name': '财经网站',
    },
    'general': {
        'pattern': r'.*',
        'fallback': True,
        'content_selector': None,
        'title_selector': 'h1',
        'author_selector': None,
        'time_selector': None,
        'clean_nav': True,
        'display_name': '网页文章',
    },
}

# 导航清理关键词
NAV_KEYWORDS = [
    "行情工具", "报价", "股票报价", "期权报价", "期货报价", "外汇报价",
    "投资工具", "模拟交易", "选股器", "热力图", "业绩日历", "机构追踪", "概念板块",
    "资讯及牛牛圈", "新闻", "焦点新闻", "7×24快讯", "财经日历", "热门专题",
    "财经直播", "投资教育", "股市术语百科", "投资策略", "投资讲座",
    "牛牛圈", "牛友交流", "热议话题",
    "关于我们", "帮助", "English", "繁體中文", "简体中文",
    "注册/登入", "新客限时", "高达千元奖赏", "立即领取",
    "返回", "Futu 富途", "刷新", "加载中", "历史记录", "热门资讯",
    "行情", "资讯", "课堂", "港股", "美股", "沪深", "新加坡", "澳洲", "日股",
    "公告", "研报", "操作过于频繁", "请检查网络设置后重试",
    "深色", "浅色", "清空", "全部", "暂无匹配内容",
]


# ─── 工具函数 ──────────────────────────────────────────

def detect_platform(url):
    """识别文章来源平台"""
    for platform, config in PLATFORMS.items():
        if platform == 'general':
            continue
        if re.search(config['pattern'], url):
            return platform, config
    return 'general', PLATFORMS['general']


def detect_industry(title, content):
    """识别文章所属行业"""
    text = title + " " + content[:1000]
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return industry
    return '其他行业'


def normalize_wechat_url(url):
    """规范化微信URL，确保带有scene=1参数"""
    if 'mp.weixin.qq.com' not in url:
        return url
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if 'scene' not in params:
        params['scene'] = ['1']
    new_query = urlencode(params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def strip_tracking_params(url, platform_config):
    """清理URL中的跟踪参数，只保留核心路径
    
    富途URL典型格式: https://news.futunn.com/post/72187172?futusource=...&data_ticket=...
    清理后: https://news.futunn.com/post/72187172
    """
    if not platform_config.get('strip_tracking_params'):
        return url
    parsed = urlparse(url)
    # 只保留 scheme + netloc + path，去掉所有查询参数和fragment
    clean = urlunparse(parsed._replace(query='', fragment=''))
    return clean


def clean_navigation_content(content):
    """清理导航和冗余内容"""
    lines = content.split('\n')
    clean_lines = []
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            if clean_lines and clean_lines[-1].strip():
                clean_lines.append('')
            continue
        is_nav = False
        for keyword in NAV_KEYWORDS:
            if keyword in line_stripped and len(line_stripped) < 30:
                is_nav = True
                break
        if not is_nav:
            clean_lines.append(line)
    # 移除连续空行
    result = []
    prev_empty = False
    for line in clean_lines:
        if not line.strip():
            if not prev_empty:
                result.append(line)
            prev_empty = True
        else:
            result.append(line)
            prev_empty = False
    return '\n'.join(result)


def clean_futu_stock_quotes(content):
    """清理富途文章中嵌入的行情组件数据
    
    富途页面在正文中嵌入股票实时行情，格式如：
    CRWV CoreWeave\n106.210\n-5.850\n-5.22%\n盘前时段\n04/28 06:20 (美东)
    需要识别并移除这些行情块，但保留正文（含股票名称引用的段落）。
    """
    lines = content.split('\n')
    clean_lines = []
    skip_mode = False
    stock_ticker_pattern = re.compile(
        r'^[A-Z]{1,5}\s'  # 股票代码 + 空格 (如 "CRWV CoreWeave")
        r'|^\d+\.\d{1,3}$'  # 价格如 106.210
        r'|^[+-]\d+\.\d{1,3}$'  # 涨跌额
        r'|^[+-]?\d+\.\d{1,2}%$'  # 涨跌幅
        r'|^盘前时段|^盘后时段|^交易时段|^休市'
        r'|^\d{2}/\d{2}\s\d{2}:\d{2}'  # 时间戳 04/28 06:20
        r'|^\(美东\)$'  # 时区标注
    )
    
    # 检测行情块开始：连续出现股票代码行
    consecutive_ticker_lines = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        # 行情块特征：股票代码行 + 价格 + 涨跌 + 百分比 + 时间
        if stock_ticker_pattern.match(stripped):
            consecutive_ticker_lines += 1
            if consecutive_ticker_lines >= 3:
                # 找到行情块起点，只回溯删除匹配行情模式的行（保留正文）
                while clean_lines and consecutive_ticker_lines > 0:
                    popped = clean_lines.pop()
                    # 如果弹出的行不匹配行情模式，说明是正文，放回去
                    if not stock_ticker_pattern.match(popped.strip()):
                        clean_lines.append(popped)
                        break  # 正文行不放回计数器，停止回溯
                    consecutive_ticker_lines -= 1
                skip_mode = True
                continue
        else:
            consecutive_ticker_lines = 0
        
        if skip_mode:
            # 检查是否行情块结束（遇到正常文本行，>20字符）
            if stripped and not stock_ticker_pattern.match(stripped) and len(stripped) > 20:
                skip_mode = False
                clean_lines.append(line)
            continue
        
        clean_lines.append(line)
    
    return '\n'.join(clean_lines)


def clean_futu_stock_markers(content):
    """清理富途正文中残留的 $股票名称 (代码)$ 标记和碎片化行
    
    富途页面中股票引用在 get_text() 后变成：
    $软银集团 (9984.JP)$\n在东京一度跌近11%，\n$CoreWeave (CRWV.US)$\n、
    需要移除 $ 符号，合并碎片行为连贯段落。
    """
    # 1. 移除 $ 符号但保留股票名称和代码
    content = re.sub(r'\$', '', content)
    
    # 2. 合并被股票引用打断的碎片行
    #    股票引用行特征：仅含"名称 (代码)"或"名称 (代码)标点"
    stock_ref_pattern = re.compile(
        r'^.{1,30}\([A-Z]{1,5}\.[A-Z]{2,4}\)[、，。]?$'
    )
    
    lines = content.split('\n')
    merged = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if merged and merged[-1].strip():
                merged.append('')
            continue
        
        # 碎片行判断
        is_stock_ref = bool(stock_ref_pattern.match(stripped))
        is_short_connector = (
            len(stripped) < 15
            and merged
            and merged[-1].strip()
            and (
                stripped.startswith(('、', '，', '。', '；', '：', '）', ')'))
                or stripped.endswith(('、', '，'))
            )
        )
        is_futu_fragment = is_stock_ref or is_short_connector
        
        if is_futu_fragment and merged and merged[-1].strip():
            # 合并到上一行
            merged[-1] = merged[-1].rstrip() + stripped
        else:
            merged.append(line)
    
    # 3. 清理连续空行
    result = []
    prev_empty = False
    for line in merged:
        if not line.strip():
            if not prev_empty:
                result.append('')
            prev_empty = True
        else:
            result.append(line)
            prev_empty = False
    
    return '\n'.join(result)


def safe_filename(title, max_len=60):
    """生成安全文件名"""
    safe = re.sub(r'[<>:"/\\|?*\n\r\t]', '', title)[:max_len]
    safe = safe.strip(' .')
    return safe or 'unnamed_article'


# ─── 提取引擎 ──────────────────────────────────────────

async def fetch_with_playwright(url, platform_name, platform_config):
    """方法2: Playwright headless 抓取"""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return None, "Playwright 未安装"

    # URL规范化
    if platform_config.get('scene_param'):
        url = normalize_wechat_url(url)
    url = strip_tracking_params(url, platform_config)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )
        page = await browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        try:
            print(f"  [Playwright] 正在访问: {url[:80]}...")
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(3000)

            html = await page.content()
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # 提取标题
            title = ""
            title_sel = platform_config.get('title_selector', 'h1')
            if title_sel:
                for sel in title_sel.split(', '):
                    elem = soup.select_one(sel.strip())
                    if elem and elem.get_text(strip=True):
                        title = elem.get_text(strip=True)
                        break
            if not title:
                for sel in ['h1', '.title', '[class*="title"]']:
                    elem = soup.select_one(sel)
                    if elem:
                        text = elem.get_text(strip=True)
                        if len(text) > 5:
                            title = text
                            break

            # 提取作者
            author = ""
            author_sel = platform_config.get('author_selector')
            if author_sel:
                elem = soup.select_one(author_sel)
                if elem:
                    author = elem.get_text(strip=True)
                    # 富途特殊处理：分离作者和时间（格式："来源·时间"）
                    if platform_name == 'futu' and '·' in author:
                        parts = author.split('·', 1)
                        author = parts[0].strip()
                        # 时间部分已在下方单独提取

            # 提取时间
            publish_time = ""
            time_sel = platform_config.get('time_selector')
            if time_sel:
                for sel in time_sel.split(', '):
                    elem = soup.select_one(sel.strip())
                    if elem:
                        time_text = elem.get_text(strip=True)
                        if any(c.isdigit() for c in time_text):
                            # 富途特殊处理：时间元素可能包含"来源·时间"，分离之
                            if platform_name == 'futu' and '·' in time_text:
                                parts = time_text.rsplit('·', 1)
                                publish_time = parts[-1].strip()
                                # 如果作者未被之前提取到，用前半部分补充
                                if not author and len(parts) > 1:
                                    author = parts[0].strip()
                            else:
                                publish_time = time_text
                            break

            # 提取内容
            content_text = ""
            content_sel = platform_config.get('content_selector')
            if content_sel:
                for sel in content_sel.split(', '):
                    elem = soup.select_one(sel.strip())
                    if elem:
                        content_text = elem.get_text(separator='\n', strip=True)
                        if len(content_text) > 100:
                            break

            # 备用：提取body
            if not content_text or len(content_text) < 100:
                body = soup.find('body')
                if body:
                    content_text = body.get_text(separator='\n', strip=True)

            # 清理
            if platform_config.get('clean_nav'):
                content_text = clean_navigation_content(content_text)
            
            # 富途特殊清理：移除嵌入的行情组件数据
            if platform_name == 'futu':
                content_text = clean_futu_stock_quotes(content_text)
                content_text = clean_futu_stock_markers(content_text)
            
            content_text = '\n'.join([line for line in content_text.split('\n') if line.strip()])

            # 反爬验证码检测
            captcha_signals = ['Access Verification', 'slide to verify', '请完成验证',
                               'verify you are human', 'cf-browser-verification']
            if any(sig in content_text[:500] for sig in captcha_signals):
                return None, f"检测到反爬验证码，内容不可用"

            return {
                'success': True,
                'url': url,
                'title': title or '未命名文章',
                'author': author,
                'publish_time': publish_time,
                'platform': platform_name,
                'content_text': content_text,
                'fetch_method': 'playwright',
            }, None

        except Exception as e:
            return None, f"Playwright 错误: {str(e)}"
        finally:
            await browser.close()


def fetch_with_tavily(url, api_key=None, platform_config=None):
    """方法3: Tavily API 提取"""
    api_key = api_key or os.getenv('TAVILY_API_KEY')
    if not api_key:
        return None, "TAVILY_API_KEY 未配置"

    try:
        import requests as req
        print(f"  [Tavily] 正在通过API提取: {url[:80]}...")
        normalized_url = normalize_wechat_url(url) if 'mp.weixin.qq.com' in url else url
        if platform_config:
            normalized_url = strip_tracking_params(normalized_url, platform_config)
        response = req.post(
            'https://api.tavily.com/search',
            json={
                'api_key': api_key,
                'query': normalized_url,
                'search_depth': 'advanced',
                'include_answer': True,
                'max_results': 1,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        content = data.get('answer', '') or (data.get('results', [{}])[0].get('content', '') if data.get('results') else '')
        if not content:
            return None, "Tavily 返回内容为空"

        # 解析元数据
        title = ''
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()

        author = ''
        author_match = re.search(r'Original(.+?)(?:\n|$)', content, re.IGNORECASE)
        if author_match:
            author = author_match.group(1).strip()

        publish_time = ''
        date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', content)
        if date_match:
            y, m, d = date_match.groups()
            publish_time = f"{y}-{m.zfill(2)}-{d.zfill(2)}"

        return {
            'success': True,
            'url': normalized_url,
            'title': title or '未命名文章',
            'author': author,
            'publish_time': publish_time,
            'platform': 'wechat' if 'mp.weixin.qq.com' in url else 'general',
            'content_text': content,
            'fetch_method': 'tavily',
        }, None
    except Exception as e:
        return None, f"Tavily 错误: {str(e)}"


def fetch_with_firecrawl(url, platform_config=None):
    """方法4: Firecrawl CLI 提取"""
    try:
        print(f"  [Firecrawl] 正在通过CLI提取: {url[:80]}...")
        normalized_url = normalize_wechat_url(url) if 'mp.weixin.qq.com' in url else url
        if platform_config:
            normalized_url = strip_tracking_params(normalized_url, platform_config)
        output_file = f'/tmp/firecrawl_{int(time.time())}.md'
        cmd = ['firecrawl', 'scrape', normalized_url, '--only-main-content', '-o', output_file]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, timeout=60)
        if result.returncode != 0:
            return None, f"Firecrawl 失败: {result.stderr[:200]}"

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content or len(content.strip()) < 50:
            return None, "Firecrawl 返回内容为空"

        # 解析元数据
        title = ''
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()

        return {
            'success': True,
            'url': normalized_url,
            'title': title or '未命名文章',
            'author': '',
            'publish_time': '',
            'platform': 'wechat' if 'mp.weixin.qq.com' in url else 'general',
            'content_text': content,
            'fetch_method': 'firecrawl',
        }, None
    except FileNotFoundError:
        return None, "Firecrawl 未安装"
    except Exception as e:
        return None, f"Firecrawl 错误: {str(e)}"


def fetch_with_http(url):
    """方法5: 纯HTTP提取（最后兜底）"""
    try:
        import requests as req
        print(f"  [HTTP] 正在直接HTTP提取: {url[:80]}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        resp = req.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 提取标题
        title = ''
        for sel in ['h1', '.title', '[class*="title"]', 'title']:
            elem = soup.select_one(sel)
            if elem and elem.get_text(strip=True):
                title = elem.get_text(strip=True)
                break

        # 提取内容
        content_text = ''
        for sel in ['article', 'main', '.content', '#content', '.article-body']:
            elem = soup.select_one(sel)
            if elem and len(elem.get_text(strip=True)) > 100:
                content_text = elem.get_text(separator='\n', strip=True)
                break
        if not content_text:
            body = soup.find('body')
            if body:
                content_text = body.get_text(separator='\n', strip=True)

        content_text = clean_navigation_content(content_text)
        content_text = '\n'.join([line for line in content_text.split('\n') if line.strip()])

        return {
            'success': True,
            'url': url,
            'title': title or '未命名文章',
            'author': '',
            'publish_time': '',
            'platform': 'general',
            'content_text': content_text,
            'fetch_method': 'http',
        }, None
    except Exception as e:
        return None, f"HTTP 错误: {str(e)}"


# ─── 存储引擎 ──────────────────────────────────────────

def save_to_obsidian(article, platform_name):
    """双层存储到Obsidian知识库"""
    if not article.get('success'):
        print(f"❌ 文章数据无效，跳过存储")
        return None

    title = article.get('title', '未命名文章')
    safe_title = safe_filename(title)
    timestamp = int(time.time())

    # 识别行业
    industry = detect_industry(title, article.get('content_text', ''))
    print(f"  🏷️  识别行业: {industry}")

    platform_display = PLATFORMS.get(platform_name, PLATFORMS['general']).get('display_name', platform_name)

    # ── 1. 原始内容存储 (raw/) ──
    raw_dir = os.path.join(VAULT_RAW, platform_name, industry)
    os.makedirs(raw_dir, exist_ok=True)
    raw_filename = f"{platform_name}_{safe_title}_{timestamp}.txt"
    raw_path = os.path.join(raw_dir, raw_filename)

    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(f"原始链接: {article.get('url', '')[:200]}\n")
        f.write(f"文章标题: {title}\n")
        f.write(f"平台: {platform_display}\n")
        f.write(f"行业分类: {industry}\n")
        if article.get('author'):
            f.write(f"作者/来源: {article['author']}\n")
        if article.get('publish_time'):
            f.write(f"发布时间: {article['publish_time']}\n")
        f.write(f"抓取方法: {article.get('fetch_method', 'unknown')}\n")
        f.write(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(article.get('content_text', ''))

    print(f"  ✅ 原始内容: {industry}/{raw_filename}")

    # ── 2. 结构化来源页 (sources/) ──
    source_dir = os.path.join(VAULT_SOURCES, industry)
    os.makedirs(source_dir, exist_ok=True)
    source_filename = f"{platform_display}_{safe_title}.md"
    source_path = os.path.join(source_dir, source_filename)

    author_field = article.get('author', '') or platform_display
    content_for_md = article.get('content_text', '')[:10000]  # 限制长度
    tags = f"#{platform_name} #{industry.replace(' ', '_')} #文章 #知识库"

    source_content = f"""---
source_type: {platform_name}_article
url: {article.get('url', '')[:200]}
title: {title}
source: {platform_display}
industry: {industry}
author: {author_field}
publish_date: {article.get('publish_time', '')}
fetched_date: {datetime.now().strftime('%Y-%m-%d')}
content_length: {len(article.get('content_text', ''))}
fetch_method: {article.get('fetch_method', 'unknown')}
---

# {title}

## 基本信息

| 字段 | 内容 |
|------|------|
| 来源 | {platform_display} |
| 行业 | {industry} |
| 作者 | {author_field} |
| 发布时间 | {article.get('publish_time', '')} |
| 原文链接 | [{platform_display}]({article.get('url', '')[:200]}) |
| 抓取方法 | {article.get('fetch_method', 'unknown')} |
| 抓取时间 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |

## 文章内容

{content_for_md}

## 关键词

{tags}
"""

    with open(source_path, 'w', encoding='utf-8') as f:
        f.write(source_content)

    print(f"  ✅ 结构化页: {industry}/{source_filename}")

    return {
        'raw_path': raw_path,
        'source_path': source_path,
        'raw_filename': raw_filename,
        'source_filename': source_filename,
        'industry': industry,
    }


# ─── 主流程 ──────────────────────────────────────────

async def fetch_article(url, method='auto', industry=None, dry_run=False):
    """
    统一文章抓取入口
    method: auto | playwright | tavily | firecrawl | http
    """
    print("=" * 60)
    print("📚 网页文章一体化抓取器 v2.0")
    print("=" * 60)

    # Step 1: 平台识别 + URL规范化
    platform_name, platform_config = detect_platform(url)
    print(f"\n🔎 识别平台: {platform_config.get('display_name', platform_name)}")

    if platform_config.get('scene_param'):
        url = normalize_wechat_url(url)
        print(f"  🔗 URL已规范化: {url[:80]}...")
    url_before_strip = url
    url = strip_tracking_params(url, platform_config)
    if url != url_before_strip:
        print(f"  🧹 URL已清理跟踪参数: {url}")

    # Step 2: 按优先级提取
    article = None
    fetch_methods = []

    if method == 'auto':
        # 按优先级排列
        fetch_methods = ['playwright', 'tavily', 'firecrawl', 'http']
    else:
        fetch_methods = [method]

    for m in fetch_methods:
        print(f"\n⏳ 尝试方法: {m}")
        error = None

        if m == 'playwright':
            article, error = await fetch_with_playwright(url, platform_name, platform_config)
        elif m == 'tavily':
            article, error = fetch_with_tavily(url, platform_config=platform_config)
        elif m == 'firecrawl':
            article, error = fetch_with_firecrawl(url, platform_config=platform_config)
        elif m == 'http':
            article, error = fetch_with_http(url)
        else:
            print(f"  ⚠️ 未知方法: {m}")
            continue

        if article and article.get('success') and len(article.get('content_text', '')) > 100:
            print(f"  ✅ {m} 提取成功!")
            break
        else:
            reason = error or (f"内容过短({len(article.get('content_text', ''))}字符)" if article else "未知错误")
            print(f"  ❌ {m} 失败: {reason}")
            article = None
            continue

    if not article:
        print("\n❌ 所有提取方法均失败，请尝试手动复制内容")
        return None

    # Step 3: 结果摘要
    print(f"\n📝 标题: {article.get('title', '未命名')}")
    if article.get('author'):
        print(f"👤 作者: {article['author']}")
    if article.get('publish_time'):
        print(f"⏰ 发布时间: {article['publish_time']}")
    print(f"📄 内容长度: {len(article.get('content_text', ''))} 字符")
    print(f"🔧 提取方法: {article.get('fetch_method', 'unknown')}")

    # 内容质量检查
    content_len = len(article.get('content_text', ''))
    if content_len < 200:
        print(f"⚠️  警告: 内容过短({content_len}字符)，可能提取不完整")

    if dry_run:
        print("\n🏃 Dry-run模式，跳过存储")
        preview = article.get('content_text', '')[:400]
        print(f"\n📋 内容预览:\n{preview}...")
        return article

    # Step 4: 行业分类 + 存储
    if industry:
        # 用户手动指定行业，覆盖自动检测
        article['manual_industry'] = industry

    saved = save_to_obsidian(article, platform_name)

    if saved:
        print("\n" + "=" * 60)
        print("✅ 完成! 文章已成功存入Obsidian知识库")
        print("=" * 60)
        print(f"  📂 行业分类: {saved['industry']}")
        print(f"  📄 原始文件: raw/{platform_name}/{saved['industry']}/{saved['raw_filename']}")
        print(f"  📋 结构化页: sources/{saved['industry']}/{saved['source_filename']}")

    return {**article, **saved} if saved else article


def main():
    parser = argparse.ArgumentParser(description='网页文章一体化抓取器')
    parser.add_argument('url', help='文章URL')
    parser.add_argument('--industry', default=None, help='指定行业分类（覆盖自动检测）')
    parser.add_argument('--method', default='auto',
                        choices=['auto', 'playwright', 'tavily', 'firecrawl', 'http'],
                        help='提取方法（默认auto=按优先级回退）')
    parser.add_argument('--dry-run', action='store_true', help='仅提取不存储')

    args = parser.parse_args()
    result = asyncio.run(fetch_article(args.url, method=args.method,
                                        industry=args.industry, dry_run=args.dry_run))
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
