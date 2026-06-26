"""
Toutiao Article Reader - 增强版
支持多平台、错误处理、内容清洗、AI 总结
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
import json
import sys
import time
import re
from datetime import datetime
from pathlib import Path
from ai_summarizer import AISummarizer
from cache import ArticleCache
from exporter import ArticleExporter

# 平台配置
PLATFORM_CONFIG = {
    'toutiao.com': {
        'name': '今日头条',
        'title_selectors': ['h1.article-title', 'h1.title', 'h1', '.article-title'],
        'author_selectors': ['.author-name', '.article-author', '[class*="author"]'],
        'time_selectors': ['.publish-time', '.article-time', 'time', '[datetime]'],
        'content_selectors': ['.article-content', '.article-body', '#content'],
    },
    'mp.weixin.qq.com': {
        'name': '微信公众号',
        'title_selectors': ['#activity-name', 'h1', 'h2'],
        'author_selectors': ['#js_author_name', '.rich_media_meta_nickname'],
        'time_selectors': ['#publish_time', '.rich_media_meta_text'],
        'content_selectors': ['#js_content', '.rich_media_content'],
    },
    'zhihu.com': {
        'name': '知乎',
        'title_selectors': ['h1.QuestionHeader-title', 'h1'],
        'author_selectors': ['.AuthorInfo', '.Post-Author'],
        'time_selectors': ['.QuestionHeader-time', '.content-time'],
        'content_selectors': ['.QuestionRichContent', '.Post-RichText'],
    },
    'xueqiu.com': {
        'name': '雪球',
        'title_selectors': ['h1.article__title'],
        'author_selectors': ['.article__author'],
        'time_selectors': ['.article__time'],
        'content_selectors': ['.article__content'],
    }
}


class ArticleReader:
    """文章阅读器"""
    
    def __init__(self, timeout=30000, headless=True, use_cache=True):
        self.timeout = timeout
        self.headless = headless
        self.use_cache = use_cache
        self.browser = None
        self.page = None
        self.cache = ArticleCache() if use_cache else None
    
    def _get_platform(self, url):
        """识别平台"""
        for domain, config in PLATFORM_CONFIG.items():
            if domain in url:
                return domain, config
        return None, None
    
    def _clean_text(self, text):
        """清洗文本"""
        if not text:
            return ''
        
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        
        # 去除常见广告词
        ad_patterns = [
            r'广告',
            r'推广',
            r'赞助',
            r'点击.*?查看详情',
            r'下载 APP',
            r'扫码.*?关注',
        ]
        for pattern in ad_patterns:
            text = re.sub(pattern, '', text)
        
        # 去除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fa5，。！？；：""''、·…—]', '', text)
        
        return text.strip()
    
    def _extract_with_selectors(self, page, selectors):
        """使用多个选择器提取内容"""
        for selector in selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    text = element.text_content().strip()
                    if text and len(text) > 2:
                        return text
            except:
                continue
        return ''
    
    def _extract_content(self, page, soup, selectors):
        """提取正文内容"""
        content_parts = []
        
        for selector in selectors:
            try:
                content_el = page.query_selector(selector)
                if content_el:
                    paragraphs = content_el.query_selector_all('p')
                    for p in paragraphs:
                        text = p.text_content().strip()
                        # 过滤太短或太长的段落
                        if 10 < len(text) < 2000:
                            cleaned = self._clean_text(text)
                            if cleaned:
                                content_parts.append(cleaned)
                    
                    if content_parts:
                        break
            except:
                continue
        
        # 如果没有找到，尝试从 HTML 中提取
        if not content_parts:
            main = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if main:
                paragraphs = main.find_all('p')
                for p in paragraphs:
                    text = p.get_text().strip()
                    if 10 < len(text) < 2000:
                        cleaned = self._clean_text(text)
                        if cleaned:
                            content_parts.append(cleaned)
        
        return '\n\n'.join(content_parts)
    
    def read(self, url):
        """读取文章"""
        result = {
            'success': False,
            'platform': '',
            'title': '',
            'author': '',
            'publish_time': '',
            'source': '',
            'content': '',
            'word_count': 0,
            'reading_time': 0,
            'url': url,
            'error': '',
            'timestamp': datetime.now().isoformat(),
            'from_cache': False
        }
        
        # 尝试从缓存获取
        if self.cache:
            cached = self.cache.get(url)
            if cached:
                print(f"从缓存读取：{url}", file=sys.stderr)
                cached['from_cache'] = True
                return cached
        
        try:
            # 识别平台
            domain, platform_config = self._get_platform(url)
            if platform_config:
                result['platform'] = platform_config['name']
                print(f"识别平台：{result['platform']}", file=sys.stderr)
            else:
                result['platform'] = '未知平台'
                print(f"未知平台，使用通用规则", file=sys.stderr)
            
            with sync_playwright() as p:
                # 启动浏览器
                print("启动浏览器...", file=sys.stderr)
                self.browser = p.chromium.launch(
                    headless=self.headless,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-extensions',
                    ]
                )
                
                # 创建新页面
                self.page = self.browser.new_page(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                # 设置超时
                self.page.set_default_timeout(self.timeout)
                
                # 访问页面
                print(f"访问：{url}", file=sys.stderr)
                start_time = time.time()
                response = self.page.goto(url, wait_until='domcontentloaded')
                load_time = time.time() - start_time
                print(f"页面加载时间：{load_time:.2f}秒", file=sys.stderr)
                
                # 检查响应状态
                if response and response.status != 200:
                    result['error'] = f"页面加载失败：HTTP {response.status}"
                    return result
                
                # 等待内容加载
                print("等待内容加载...", file=sys.stderr)
                time.sleep(2)
                
                # 获取页面内容
                html = self.page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                # 使用平台特定规则或通用规则
                if platform_config:
                    title_selectors = platform_config['title_selectors']
                    author_selectors = platform_config['author_selectors']
                    time_selectors = platform_config['time_selectors']
                    content_selectors = platform_config['content_selectors']
                else:
                    # 通用选择器
                    title_selectors = ['h1', 'h2', 'title']
                    author_selectors = ['.author', '[class*="author"]', 'meta[name="author"]']
                    time_selectors = ['time', '[datetime]', '[class*="time"]']
                    content_selectors = ['article', '.content', '#content', 'main']
                
                # 提取标题
                result['title'] = self._extract_with_selectors(self.page, title_selectors)
                if not result['title']:
                    title_tag = soup.find('title')
                    if title_tag:
                        result['title'] = title_tag.get_text().strip()
                
                # 提取作者
                result['author'] = self._extract_with_selectors(self.page, author_selectors)
                
                # 提取发布时间
                result['publish_time'] = self._extract_with_selectors(self.page, time_selectors)
                
                # 提取来源
                source_el = self.page.query_selector('.source, .article-source, [class*="source"]')
                if source_el:
                    result['source'] = source_el.text_content().strip()
                
                # 提取正文
                result['content'] = self._extract_content(self.page, soup, content_selectors)
                
                # 计算统计信息
                result['word_count'] = len(result['content'])
                result['reading_time'] = max(1, result['word_count'] // 300)  # 按每分钟 300 字计算
                
                # AI 总结
                print("正在生成 AI 总结...", file=sys.stderr)
                summarizer = AISummarizer()
                summary_result = summarizer.summarize(result['content'], result['title'], result['platform'])
                result['ai_summary'] = summary_result
                
                # 关闭浏览器
                self.browser.close()
                
                result['success'] = True
                print(f"成功提取：{result['word_count']} 字", file=sys.stderr)
                
                # 保存到缓存
                if self.cache:
                    self.cache.set(url, result)
                    
        except PlaywrightTimeout:
            result['error'] = '页面加载超时，请检查网络连接'
        except Exception as e:
            result['error'] = f'读取失败：{str(e)}'
            print(f"错误：{e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        finally:
            if self.browser:
                try:
                    self.browser.close()
                except:
                    pass
        
        return result
    
    def summarize(self, content, max_length=500):
        """生成摘要（简化版，实际应该调用 AI）"""
        if not content:
            return ''
        
        # 简单提取前几句
        sentences = re.split(r'[。！？.!?]', content)
        summary = '。'.join([s for s in sentences[:3] if s.strip()])
        
        if len(summary) > max_length:
            summary = summary[:max_length] + '...'
        
        return summary


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Toutiao Article Reader - 文章阅读工具')
    parser.add_argument('url', help='文章 URL')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--summary', action='store_true', help='生成摘要')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    parser.add_argument('--timeout', type=int, default=30000, help='超时时间（毫秒）')
    parser.add_argument('--no-headless', action='store_true', help='显示浏览器窗口')
    parser.add_argument('--export', choices=['markdown', 'txt', 'json', 'html'], help='导出为指定格式')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--cache-stats', action='store_true', help='显示缓存统计')
    parser.add_argument('--clear-cache', action='store_true', help='清空缓存')
    
    args = parser.parse_args()
    
    # 处理缓存命令
    if args.cache_stats or args.clear_cache:
        cache = ArticleCache()
        if args.cache_stats:
            stats = cache.stats()
            print(f"缓存统计:")
            print(f"  缓存项数：{stats['total_items']}")
            print(f"  缓存文件大小：{stats['cache_file_size']} 字节")
            print(f"  有效期：{stats['ttl_hours']} 小时")
            sys.exit(0)
        elif args.clear_cache:
            cache.clear()
            print("已清空缓存")
            sys.exit(0)
    
    if not args.url:
        parser.print_help()
        sys.exit(1)
    
    print(f"开始读取文章：{args.url}", file=sys.stderr)
    
    reader = ArticleReader(timeout=args.timeout, headless=not args.no_headless, use_cache=True)
    result = reader.read(args.url)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result['success']:
            print("\n" + "="*60)
            print(f"📰 {result['title']}")
            print("="*60)
            print(f"平台：{result['platform']}")
            print(f"作者：{result['author'] or '未知'}")
            print(f"时间：{result['publish_time'] or '未知'}")
            print(f"字数：{result['word_count']} 字")
            print(f"阅读时间：约{result['reading_time']}分钟")
            print("\n" + "-"*60)
            print("【内容摘要】")
            print("-"*60)
            
            if args.summary:
                summary = reader.summarize(result['content'])
                print(summary)
            else:
                # 显示前 1000 字
                preview = result['content'][:1000]
                print(preview)
                if len(result['content']) > 1000:
                    print(f"\n... (还有 {len(result['content']) - 1000} 字)")
            
            print("\n" + "="*60)
            print("✅ 阅读完成")
            print("="*60)
        else:
            print(f"\n❌ 阅读失败：{result['error']}")
            sys.exit(1)


if __name__ == '__main__':
    main()
