#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块1：主力网站热点新闻爬取
专门爬取CLS、JRJ、STCN三个主力网站
统一输出格式，去重处理，保存到临时目录供module2使用
"""

import os
import sys
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Set, Optional
import hashlib

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入三个主力网站的抓取器
try:
    from cls_hot_news import CLSHotNewsCrawler
    from jrj_hot_news import JRJHotNewsCrawler
    from stcn_hot_news import STCNHotNewsCrawler
    CRAWLERS_AVAILABLE = True
except ImportError as e:
    print(f"[ERROR] 无法导入抓取器: {e}")
    CRAWLERS_AVAILABLE = False

# 尝试导入scrapling用于通用网站爬取
try:
    import scrapling
    SCRAPLING_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] 无法导入scrapling: {e}")
    SCRAPLING_AVAILABLE = False

# 导入scrapling工具模块
try:
    from scrapling_util import ScraplingUtil, fetch, fetch_wheel
    SCRAPLING_UTIL_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] 无法导入scrapling_util: {e}")
    SCRAPLING_UTIL_AVAILABLE = False


class MainSitesCrawler:
    """主力网站爬取器"""
    
    def __init__(self):
        """初始化爬取器"""
        self.name = "主力网站热点新闻爬取器"
        
        # 加载配置文件获取路径
        config = self.load_config()
        if config:
            system_settings = config.get('system_settings', {})
            temp_dir = system_settings.get('temp_dir', 'c:/SelfData/claw_temp/temp')
            self.output_dir = Path(temp_dir) / "title_news_crawl"
            print(f"[INFO] 从配置文件加载输出目录: {self.output_dir}")
        else:
            self.output_dir = Path("c:/SelfData/claw_temp/temp/title_news_crawl")
            print(f"[WARNING] 配置文件加载失败，使用默认输出目录: {self.output_dir}")
        
        self.temp_dir = self.output_dir / "temp"
        
        # 创建目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # 主力网站配置
        self.main_sites = [
            {
                'name': '财联社',
                'crawler_class': CLSHotNewsCrawler,
                'url': 'https://www.cls.cn/depth?id=1000',
                'priority': 1  # 最高优先级
            },
            {
                'name': '金融界',
                'crawler_class': JRJHotNewsCrawler,
                'url': 'https://www.jrj.com.cn/',
                'priority': 2
            },
            {
                'name': '证券时报网',
                'crawler_class': STCNHotNewsCrawler,
                'url': 'https://www.stcn.com/',
                'priority': 3
            }
        ]
        
        # 辅助网站（可选）
        self.aux_sites = []  # 可以后续添加
        
        # 加载url_config.json配置，添加其他6个网站（用户要求全部开启）
        # self.other_sites = []  # 暂时清空，先恢复主力网站稳定（已注释，启用其他网站）
        self.other_sites = self.load_other_sites_config()  # 启用其他网站配置
        
        print(f"{self.name} 初始化完成")
        print(f"输出目录: {self.output_dir}")
        print(f"临时目录: {self.temp_dir}")
        print(f"主力网站: {len(self.main_sites)} 个")
        print(f"其他网站: {len(self.other_sites)} 个")
        print("-" * 70)
    
    def load_config(self) -> Optional[Dict[str, Any]]:
        """加载配置文件"""
        try:
            config_path = Path(__file__).parent / "url_config.json"
            if not config_path.exists():
                print(f"[WARNING] 配置文件不存在: {config_path}")
                return None
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"[INFO] 配置文件加载成功")
            return config
            
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败: {e}")
            return None
    
    def load_other_sites_config(self) -> List[Dict[str, Any]]:
        """从url_config.json加载其他网站配置"""
        other_sites = []
        try:
            # 加载配置文件
            config_path = Path(__file__).parent / "url_config.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 获取网站列表
            websites = config.get('websites', [])
            
            # 主力网站名称（用于过滤）
            main_site_names = [site['name'] for site in self.main_sites]
            
            # 过滤出其他网站（排除主力网站）
            for site_config in websites:
                site_name = site_config.get('name', '')
                if site_name not in main_site_names and site_config.get('enabled', True):
                    # 只选择前6个其他网站（根据用户要求）
                    if len(other_sites) < 6:
                        other_sites.append({
                            'name': site_name,
                            'url': site_config.get('url', ''),
                            'adapter': site_config.get('adapter', 'generic'),
                            'priority': site_config.get('priority', 99),
                            'max_articles': site_config.get('max_articles', 15),
                            'wait_time': site_config.get('wait_time', 3000),
                            'timeout': site_config.get('timeout', 10),
                            'description': site_config.get('description', '')
                        })
            
            print(f"[INFO] 从配置加载了 {len(other_sites)} 个其他网站")
            for site in other_sites:
                print(f"  - {site['name']} ({site['url']})")
            
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败: {e}")
        
        return other_sites
    
    def _generate_article_id(self, url: str, title: str) -> str:
        """生成文章唯一ID"""
        # 使用URL和标题的hash作为ID
        content = f"{url}|{title}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _normalize_article(self, article: Dict[str, Any], site_name: str) -> Dict[str, Any]:
        """标准化文章格式"""
        # 确保必要字段存在
        title = article.get('title', '').strip()
        url = article.get('url', '').strip()
        
        if not title or not url:
            return None
        
        # 生成唯一ID
        article_id = self._generate_article_id(url, title)
        
        # 标准化字段
        normalized = {
            'id': article_id,
            'title': title,
            'url': url,
            'source': site_name,
            'summary': article.get('summary', '').strip(),
            'category': article.get('category', '').strip() or '综合',
            'type': article.get('type', '').strip() or '新闻',
            'publish_time': article.get('publish_time', ''),
            'publish_time_display': article.get('publish_time_display', '未知'),
            'keywords': article.get('keywords', []),
            'within_48h': article.get('within_48h', False),
            'crawl_time': datetime.now().isoformat()
        }
        
        # 清理空值
        for key in list(normalized.keys()):
            if normalized[key] in [None, '', [], {}]:
                del normalized[key]
        
        return normalized
    
    def crawl_site(self, site_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """爬取单个网站"""
        site_name = site_config['name']
        crawler_class = site_config['crawler_class']
        
        print(f"爬取 {site_name}...")
        print(f"  URL: {site_config['url']}")
        
        try:
            # 创建抓取器实例，传递输出目录
            output_dir_str = str(self.output_dir)
            crawler = crawler_class(output_dir=output_dir_str)
            
            # 运行抓取（不同抓取器可能有不同方法名和参数）
            if hasattr(crawler, 'crawl'):
                # 检查crawl方法是否需要参数
                import inspect
                params = inspect.signature(crawler.crawl).parameters
                if 'use_sample' in params:
                    articles = crawler.crawl(use_sample=False)
                else:
                    articles = crawler.crawl()
            elif hasattr(crawler, 'run'):
                articles = crawler.run()
            else:
                print(f"  [ERROR] 抓取器没有crawl或run方法")
                return []
            
            if not articles:
                print(f"  [WARNING] 未抓取到文章")
                return []
            
            print(f"  [SUCCESS] 抓取到 {len(articles)} 篇文章")
            
            # 标准化文章格式
            normalized_articles = []
            for article in articles:
                normalized = self._normalize_article(article, site_name)
                if normalized:
                    normalized_articles.append(normalized)
            
            print(f"  [INFO] 标准化后: {len(normalized_articles)} 篇文章")
            return normalized_articles
            
        except Exception as e:
            print(f"  [ERROR] 爬取失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def crawl_generic_site(self, site_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """使用scrapling爬取通用网站（隐身模式）"""
        site_name = site_config['name']
        url = site_config['url']
        
        print(f"使用scrapling爬取 {site_name}...")
        print(f"  URL: {url}")
        
        if not SCRAPLING_AVAILABLE:
            print(f"  [WARNING] scrapling不可用，跳过 {site_name}")
            return []
        
        # 检查适配器类型，非generic适配器可能有专门处理
        adapter_type = site_config.get('adapter', 'generic')
        if adapter_type != 'generic':
            print(f"  [INFO] 网站 {site_name} 使用专门适配器: {adapter_type}")
            
            # 尝试使用专门适配器
            try:
                from website_adapters_final import create_adapter
                adapter = create_adapter(adapter_type, name=site_name, url=url)
                
                # 调用适配器的scrape方法
                print(f"  [INFO] 使用专门适配器抓取...")
                articles = adapter.scrape()
                
                if not articles:
                    print(f"  [WARNING] 专门适配器未抓取到文章")
                    return []
                
                print(f"  [SUCCESS] 专门适配器抓取到 {len(articles)} 篇文章")
                
                # 标准化文章格式
                normalized_articles = []
                for article in articles:
                    normalized = self._normalize_article(article, site_name)
                    if normalized:
                        normalized_articles.append(normalized)
                
                print(f"  [INFO] 标准化后: {len(normalized_articles)} 篇文章")
                return normalized_articles
                
            except ImportError as e:
                print(f"  [WARNING] 无法导入专门适配器: {e}")
                print(f"  [INFO] 跳过 {site_name}，建议检查适配器模块")
                return []
            except Exception as e:
                print(f"  [ERROR] 专门适配器抓取失败: {type(e).__name__}: {e}")
                return []
        
        try:
            # 根据配置设置参数
            timeout = site_config.get('timeout', 10)
            
            # scrapling的timeout参数单位是毫秒，配置中是秒，需要转换
            timeout_ms = timeout * 1000
            # 从配置中获取原始的等待时间（毫秒）
            wait_time_ms = site_config.get('wait_time', 3000)  # 单位：毫秒
            
            print(f"  [INFO] 使用scrapling_util爬取 (timeout={timeout}s/{timeout_ms}ms, wait={wait_time_ms}ms)")
            
            html_content = None
            
            # 根据网站调整等待时间
            adjusted_wait_time = wait_time_ms  # 单位：毫秒
            
            # 财新网需要更长等待时间（根据测试结果）
            if 'caixin' in url.lower() or site_name == '财新网':
                adjusted_wait_time = max(adjusted_wait_time, 8000)  # 至少8秒
                print(f"  [INFO] 财新网，调整等待时间为: {adjusted_wait_time}ms")
            
            # 确保最小等待时间为5秒（用户要求）
            if adjusted_wait_time < 5000:
                adjusted_wait_time = 5000
                print(f"  [INFO] 调整等待时间为最小5秒: {adjusted_wait_time}ms")
            
            # 尝试使用scrapling_util.fetch
            if SCRAPLING_UTIL_AVAILABLE:
                try:
                    html_content = fetch(url, wait=adjusted_wait_time, timeout=timeout_ms)
                    if not html_content:
                        print(f"  [WARNING] scrapling_util.fetch返回空内容，尝试命令行版本")
                        # 使用工具类中的命令行版本
                        util = ScraplingUtil()
                        html_content = util.fetch_with_cli(url, wait=adjusted_wait_time, timeout=timeout_ms)
                except Exception as e:
                    print(f"  [WARNING] scrapling_util.fetch异常: {e}")
                    html_content = None
            
            # 如果scrapling_util不可用或失败，使用命令行版本
            if not html_content:
                print(f"  [INFO] 使用scrapling命令行版本...")
                try:
                    # 创建临时文件
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
                        tmp_file = tmp.name
                    
                    # 构建命令
                    cmd = [
                        'scrapling', 'extract', 'fetch',
                        url,
                        tmp_file,
                        '--wait', str(adjusted_wait_time),
                        '--timeout', str(timeout_ms)
                    ]
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        timeout=timeout_ms/1000 + 5
                    )
                    
                    if result.returncode == 0:
                        with open(tmp_file, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        # 清理临时文件
                        os.unlink(tmp_file)
                    else:
                        print(f"  [ERROR] 命令行抓取失败，返回码: {result.returncode}")
                        if result.stderr:
                            print(f"        错误: {result.stderr[:200]}")
                except Exception as e:
                    print(f"  [ERROR] 命令行抓取异常: {type(e).__name__}: {e}")
            
            if not html_content:
                print(f"  [WARNING] 未获取到页面内容")
                return []
            
            # 注意：抓取时已经包含了等待时间，无需额外延迟
            
            # 获取最大文章数配置
            max_articles = site_config.get('max_articles', 15)
            
            # 解析HTML提取文章
            articles = self._extract_articles_from_html(html_content, url, site_name, max_articles)
            
            if not articles:
                print(f"  [WARNING] 未提取到文章")
                return []
            
            print(f"  [SUCCESS] 提取到 {len(articles)} 篇文章")
            
            # 标准化文章格式
            normalized_articles = []
            for article in articles:
                normalized = self._normalize_article(article, site_name)
                if normalized:
                    # 添加within_48h标记
                    normalized['within_48h'] = self._check_within_48h(normalized.get('publish_time', ''))
                    normalized_articles.append(normalized)
            
            print(f"  [INFO] 标准化后: {len(normalized_articles)} 篇文章")
            return normalized_articles
            
        except Exception as e:
            print(f"  [ERROR] 爬取失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _extract_articles_from_html(self, html_content: str, base_url: str, site_name: str, max_articles: int = 15) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章信息
        Args:
            html_content: HTML内容
            base_url: 基础URL用于解析相对链接
            site_name: 网站名称
            max_articles: 最大提取文章数
        """
        articles = []
        
        try:
            # 尝试使用BeautifulSoup如果可用
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # 常见的文章标题和链接选择器
                # 这需要根据具体网站调整，这里提供通用模式
                selectors = [
                    'a[href*="article"]', 'a[href*="news"]', 'a[href*="content"]',
                    'h1 a', 'h2 a', 'h3 a', '.title a', '.news-title a',
                    '.article-title a', '.news-list a', '.article-list a'
                ]
                
                seen_urls = set()
                # 使用参数max_articles，默认15
                
                for selector in selectors:
                    elements = soup.select(selector)
                    for element in elements:
                        if len(articles) >= max_articles:
                            break
                        
                        # 提取链接和标题
                        href = element.get('href', '')
                        if not href:
                            continue
                        
                        # 处理相对URL
                        if href.startswith('/'):
                            from urllib.parse import urljoin
                            href = urljoin(base_url, href)
                        elif not href.startswith(('http://', 'https://')):
                            # 可能是相对路径但不是以/开头
                            href = base_url.rstrip('/') + '/' + href.lstrip('/')
                        
                        # 去重
                        if href in seen_urls:
                            continue
                        seen_urls.add(href)
                        
                        # 提取标题
                        title = element.get_text(strip=True)
                        if not title or len(title) < 5:
                            # 如果没有文本，尝试获取父元素的文本或属性
                            title = element.get('title', '') or element.get('alt', '')
                        
                        if not title or len(title) < 5:
                            continue
                        
                        # 创建文章对象
                        article = {
                            'title': title,
                            'url': href,
                            'source': site_name,
                            'summary': '',
                            'category': '综合',
                            'type': '新闻',
                            'publish_time': '',  # 需要从页面进一步提取
                            'publish_time_display': '未知',
                            'keywords': [],
                            'within_48h': False
                        }
                        
                        articles.append(article)
                        
                    if articles:
                        break  # 如果找到文章，停止尝试其他选择器
                
                # 如果BeautifulSoup没有找到，尝试简单正则
                if not articles:
                    import re
                    # 查找标题和链接模式
                    title_patterns = [
                        r'<h[1-3][^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?</h[1-3]>',
                        r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</a>',
                        r'<a[^>]*href="([^"]+)"[^>]*title="([^"]*)"[^>]*>'
                    ]
                    
                    for pattern in title_patterns:
                        matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
                        for match in matches:
                            if len(articles) >= max_articles:
                                break
                            
                            href, title = match if len(match) == 2 else (match[0], '')
                            if not href or not title:
                                continue
                            
                            # 处理相对URL
                            if href.startswith('/'):
                                from urllib.parse import urljoin
                                href = urljoin(base_url, href)
                            elif not href.startswith(('http://', 'https://')):
                                continue
                            
                            if href in seen_urls:
                                continue
                            seen_urls.add(href)
                            
                            # 清理标题
                            title = re.sub(r'<[^>]+>', '', title).strip()
                            if len(title) < 5:
                                continue
                            
                            article = {
                                'title': title,
                                'url': href,
                                'source': site_name,
                                'summary': '',
                                'category': '综合',
                                'type': '新闻',
                                'publish_time': '',
                                'publish_time_display': '未知',
                                'keywords': [],
                                'within_48h': False
                            }
                            
                            articles.append(article)
                        
                        if articles:
                            break
            
            except ImportError:
                # BeautifulSoup不可用，使用正则表达式
                print(f"  [INFO] BeautifulSoup不可用，使用正则表达式提取")
                import re
                
                # 简单提取所有链接和标题
                link_pattern = r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>'
                matches = re.findall(link_pattern, html_content, re.IGNORECASE | re.DOTALL)
                
                seen_urls = set()
                # 检查前 N 个链接，N = max_articles * 2
                limit = max_articles * 2 if max_articles > 0 else 30
                for href, title_html in matches[:limit]:  # 只检查前 limit 个链接
                    if not href or not title_html:
                        continue
                    
                    # 过滤非新闻链接
                    if not any(keyword in href.lower() for keyword in ['article', 'news', 'content', 'story', 'report']):
                        continue
                    
                    # 处理相对URL
                    if href.startswith('/'):
                        from urllib.parse import urljoin
                        href = urljoin(base_url, href)
                    elif not href.startswith(('http://', 'https://')):
                        continue
                    
                    if href in seen_urls:
                        continue
                    seen_urls.add(href)
                    
                    # 提取纯文本标题
                    title = re.sub(r'<[^>]+>', '', title_html).strip()
                    if len(title) < 10:  # 标题太短可能不是文章
                        continue
                    
                    # 过滤掉非中文标题（可选）
                    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', title))
                    if chinese_chars < 3:  # 至少3个中文字符
                        continue
                    
                    article = {
                        'title': title[:200],  # 截断长标题
                        'url': href,
                        'source': site_name,
                        'summary': '',
                        'category': '综合',
                        'type': '新闻',
                        'publish_time': '',
                        'publish_time_display': '未知',
                        'keywords': [],
                        'within_48h': False
                    }
                    
                    articles.append(article)
                    if len(articles) >= max_articles:
                        break
            
            return articles
            
        except Exception as e:
            print(f"  [WARNING] 提取文章失败: {e}")
            return []
    
    def _check_within_48h(self, publish_time_str: str) -> bool:
        """检查发布时间是否在48小时内"""
        if not publish_time_str:
            return False
        
        try:
            # 尝试解析发布时间
            time_formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y/%m/%d %H:%M:%S',
                '%Y/%m/%d %H:%M',
                '%Y年%m月%d日 %H:%M:%S',
                '%Y年%m月%d日 %H:%M',
                '%Y-%m-%d',
                '%Y/%m/%d'
            ]
            
            publish_time = None
            for fmt in time_formats:
                try:
                    publish_time = datetime.strptime(publish_time_str, fmt)
                    break
                except:
                    continue
            
            if not publish_time:
                return False
            
            # 计算时间差
            time_diff = datetime.now() - publish_time
            return time_diff.total_seconds() <= 48 * 3600
            
        except:
            return False
    
    def remove_duplicates(self, all_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去除重复文章（基于标题和URL）"""
        seen_ids = set()
        unique_articles = []
        
        for article in all_articles:
            article_id = article.get('id')
            if article_id and article_id not in seen_ids:
                seen_ids.add(article_id)
                unique_articles.append(article)
        
        print(f"去重: {len(all_articles)} → {len(unique_articles)} 篇文章")
        return unique_articles
    
    def filter_by_time(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """过滤48小时内的文章"""
        filtered = [article for article in articles if article.get('within_48h', False)]
        print(f"时间过滤: {len(articles)} → {len(filtered)} 篇文章 (48小时内)")
        return filtered
    
    def save_to_temp(self, articles: List[Dict[str, Any]]) -> Path:
        """保存到临时目录供module2使用"""
        if not articles:
            print("没有文章可保存")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"main_sites_news_{timestamp}.json"
        filepath = self.temp_dir / filename
        
        # 准备数据
        data = {
            'metadata': {
                'source': '主力网站爬取器',
                'crawl_time': datetime.now().isoformat(),
                'site_count': len(self.main_sites),
                'article_count': len(articles),
                'time_filter': '48小时',
                'version': '1.0'
            },
            'articles': articles
        }
        
        try:
            # 保存JSON文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"保存到临时目录: {filepath}")
            print(f"文章数量: {len(articles)} 篇")
            
            # 同时保存文本格式
            txt_filename = f"main_sites_news_{timestamp}.txt"
            txt_filepath = self.temp_dir / txt_filename
            
            with open(txt_filepath, 'w', encoding='utf-8') as f:
                f.write("主力网站热点新闻汇总\n")
                f.write("=" * 70 + "\n")
                f.write(f"爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"网站数量: {len(self.main_sites)} 个\n")
                f.write(f"文章数量: {len(articles)} 篇 (48小时内)\n")
                f.write(f"数据文件: {filename}\n")
                f.write("\n" + "=" * 70 + "\n\n")
                
                # 按来源分组
                sources = {}
                for article in articles:
                    source = article.get('source', '未知')
                    if source not in sources:
                        sources[source] = []
                    sources[source].append(article)
                
                # 按优先级排序来源
                source_order = ['财联社', '金融界', '证券时报']
                for source in source_order:
                    if source in sources:
                        f.write(f"\n{source}:\n")
                        f.write("-" * 50 + "\n")
                        
                        for i, article in enumerate(sources[source][:15], 1):  # 每个来源最多显示15篇
                            f.write(f"{i}. {article['title']}\n")
                            f.write(f"   类型: {article.get('type', '新闻')} | ")
                            f.write(f"分类: {article.get('category', '综合')}\n")
                            f.write(f"   时间: {article.get('publish_time_display', '未知')}\n")
                            f.write(f"   URL: {article['url']}\n")
                            
                            if article.get('summary'):
                                f.write(f"   摘要: {article['summary'][:100]}...\n")
                            
                            f.write("\n")
                
                # 统计信息
                f.write("\n" + "=" * 70 + "\n")
                f.write("统计信息:\n")
                f.write("-" * 50 + "\n")
                for source, source_articles in sources.items():
                    f.write(f"{source}: {len(source_articles)} 篇\n")
                
                # 分类统计
                categories = {}
                for article in articles:
                    category = article.get('category', '综合')
                    categories[category] = categories.get(category, 0) + 1
                
                if categories:
                    f.write("\n分类统计:\n")
                    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
                        f.write(f"  {category}: {count} 篇\n")
            
            print(f"文本报告: {txt_filepath}")
            
            return filepath
            
        except Exception as e:
            print(f"保存文件时出错: {type(e).__name__}: {e}")
            return None
    
    def run(self) -> List[Dict[str, Any]]:
        """运行爬取器"""
        print("=" * 70)
        print(f"{self.name}")
        print("=" * 70)
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"主力网站: {', '.join([site['name'] for site in self.main_sites])}")
        print("-" * 70)
        
        if not CRAWLERS_AVAILABLE:
            print("[ERROR] 抓取器不可用，请检查导入")
            return []
        
        all_articles = []
        
        # 爬取每个主力网站
        for site_config in self.main_sites:
            site_articles = self.crawl_site(site_config)
            all_articles.extend(site_articles)
            print()  # 空行分隔
        
        if not all_articles:
            print("[WARNING] 没有从主力网站抓取到任何文章")
        
        # 其他网站的通用抓取方案
        print("\n" + "=" * 70)
        print("开始爬取其他网站...")
        print("=" * 70)
        
        # 爬取其他6个网站
        original_count = len(all_articles)  # 记录爬取其他网站前的文章数量
        if self.other_sites:
            print(f"准备爬取 {len(self.other_sites)} 个其他网站...")
            
            for site_config in self.other_sites:
                site_name = site_config['name']
                print(f"\n爬取其他网站: {site_name}")
                
                try:
                    # 使用scrapling爬取通用网站
                    site_articles = self.crawl_generic_site(site_config)
                    
                    if site_articles:
                        all_articles.extend(site_articles)
                        print(f"  [SUCCESS] 成功添加 {len(site_articles)} 篇文章")
                    else:
                        print(f"  [WARNING] 未抓取到文章")
                        
                except Exception as e:
                    print(f"  [ERROR] 网站 {site_name} 抓取失败: {type(e).__name__}: {e}")
                    print(f"  [INFO] 跳过 {site_name}，继续下一个网站")
                    import traceback
                    traceback.print_exc()
                
                # 添加延迟，避免请求过于频繁
                time.sleep(2)
            
            print(f"\n其他网站爬取完成，共添加 {len(all_articles) - original_count} 篇文章")
        else:
            print("[INFO] 没有配置其他网站，跳过")
        
        if not all_articles:
            print("[WARNING] 没有抓取到任何文章")
            return []
        
        # 处理文章
        print("\n" + "=" * 70)
        print("处理文章...")
        print("=" * 70)
        
        # 1. 去重
        unique_articles = self.remove_duplicates(all_articles)
        
        # 2. 时间过滤
        filtered_articles = self.filter_by_time(unique_articles)
        
        # 3. 保存到临时目录
        if filtered_articles:
            saved_file = self.save_to_temp(filtered_articles)
            
            # 显示统计信息
            self.show_statistics(filtered_articles)
            
            print("\n" + "=" * 70)
            print(f"爬取完成!")
            print(f"共 {len(filtered_articles)} 篇文章 (48小时内)")
            if saved_file:
                print(f"数据已保存到临时目录供module2使用")
            print("=" * 70)
        
        return filtered_articles
    
    def show_statistics(self, articles: List[Dict[str, Any]]):
        """显示统计信息"""
        if not articles:
            return
        
        print("\n统计信息:")
        print("-" * 50)
        
        # 按来源统计
        sources = {}
        for article in articles:
            source = article.get('source', '未知')
            sources[source] = sources.get(source, 0) + 1
        
        print("按来源统计:")
        for source, count in sources.items():
            print(f"  {source}: {count} 篇")
        
        # 按分类统计
        categories = {}
        for article in articles:
            category = article.get('category', '综合')
            categories[category] = categories.get(category, 0) + 1
        
        if categories:
            print("\n按分类统计 (前10):")
            sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]
            for category, count in sorted_categories:
                print(f"  {category}: {count} 篇")
        
        # 按类型统计
        types = {}
        for article in articles:
            article_type = article.get('type', '新闻')
            types[article_type] = types.get(article_type, 0) + 1
        
        if types:
            print("\n按类型统计:")
            for article_type, count in types.items():
                print(f"  {article_type}: {count} 篇")


def main():
    """主函数"""
    try:
        print("模块1：主力网站热点新闻爬取")
        print("=" * 70)
        print("功能:")
        print("  1. 爬取CLS、JRJ、STCN三个主力网站")
        print("  2. 统一输出格式")
        print("  3. 去重处理")
        print("  4. 48小时时间过滤")
        print("  5. 保存到临时目录供module2使用")
        print("=" * 70)
        
        # 创建爬取器
        crawler = MainSitesCrawler()
        
        # 运行爬取
        articles = crawler.run()
        
        # 返回文章数量
        return len(articles)
        
    except KeyboardInterrupt:
        print("\n[INFO] 用户中断")
        return 0
    except Exception as e:
        print(f"\n[ERROR] 执行出错: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 0


if __name__ == "__main__":
    article_count = main()
    sys.exit(0 if article_count > 0 else 1)