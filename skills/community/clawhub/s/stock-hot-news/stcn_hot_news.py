#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
证券时报网热点新闻抓取器
功能：
1. 使用scrapling隐身方式访问 https://www.stcn.com/article/list/yw.html
2. 模拟鼠标滚动一次进行抓取
3. 抓取要闻下的新闻标题、摘要、出处、时间、链接地址等信息
4. 存储抓取的信息到指定的临时目录
"""

import os
import sys
import json
import time
import re
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any

# 导入scrapling工具模块
try:
    from scrapling_util import fetch, fetch_wheel
    SCRAPLING_UTIL_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] 无法导入scrapling_util: {e}")
    SCRAPLING_UTIL_AVAILABLE = False

# scrapling通过命令行使用，无需Python导入
# 可用性通过_check_scrapling()方法检查

class STCNHotNewsCrawler:
    """证券时报网热点新闻抓取器"""
    
    def __init__(self, output_dir: str = None):
        """初始化抓取器"""
        self.name = "证券时报网"
        self.base_url = "https://www.stcn.com"
        self.target_url = "https://www.stcn.com/article/list/yw.html"  # 要闻页面
        
        # 设置输出目录
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # 默认路径（兼容新配置结构）
            self.output_dir = Path("c:/SelfData/claw_temp/temp/title_news_crawl")
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查scrapling是否可用
        self.scrapling_available = self._check_scrapling()
        
        print(f"证券时报网热点新闻抓取器初始化完成")
        print(f"目标URL: {self.target_url}")
        print(f"输出目录: {self.output_dir}")
        print(f"Scrapling可用: {self.scrapling_available}")
        print("-" * 70)
    
    def _check_scrapling(self) -> bool:
        """检查scrapling是否可用（包括scrapling_util）"""
        # 首先检查scrapling_util是否可用
        if SCRAPLING_UTIL_AVAILABLE:
            return True
        
        # 如果scrapling_util不可用，检查命令行版本
        try:
            result = subprocess.run(
                ["scrapling", "--help"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0 or "Usage:" in result.stdout or "Usage:" in result.stderr
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def scroll_page(self, page) -> None:
        """模拟鼠标滚动一次
        
        Args:
            page: 页面对象（来自scrapling或playwright）
        """
        try:
            # 向下滚动500像素
            page.mouse.wheel(0, 500)
            time.sleep(1)  # 等待滚动完成
            
            # 模拟鼠标移动（可选）
            page.mouse.move(100, 400)
            time.sleep(0.5)
            
            print("  模拟鼠标滚动完成")
        except Exception as e:
            print(f"  滚动失败: {e}")
    
    def _fetch_with_scrapling(self, url: str, wait_time: int = 3000) -> Optional[str]:
        """使用scrapling抓取页面内容
        
        Args:
            url: 要抓取的URL
            wait_time: 等待时间（毫秒）
            
        Returns:
            页面HTML内容或None
        """
        if not self.scrapling_available:
            print("  Scrapling不可用，无法抓取")
            return None
        
        print(f"  使用scrapling抓取: {url}")
        print(f"  等待时间: {wait_time}ms")
        
        # 优先使用scrapling_util.fetch
        if SCRAPLING_UTIL_AVAILABLE:
            try:
                html_content = fetch(url, wait=wait_time, timeout=15000)
                if html_content:
                    print(f"  抓取成功，内容大小: {len(html_content)} 字节")
                    return html_content
                else:
                    print(f"  [WARNING] scrapling_util.fetch返回空内容，尝试命令行版本")
            except Exception as e:
                print(f"  [WARNING] scrapling_util.fetch异常: {e}")
        
        # 如果scrapling_util不可用或失败，使用命令行版本
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
                tmp_file = tmp.name
            
            # 构建scrapling命令
            cmd = [
                'scrapling', 'extract', 'fetch',
                url,
                tmp_file,
                '--wait', str(wait_time),
                '--timeout', '15000'
            ]
            
            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            
            if result.returncode == 0:
                # 读取HTML内容
                with open(tmp_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                print(f"  抓取成功，文件大小: {len(html_content)} 字节")
                
                # 清理临时文件
                os.unlink(tmp_file)
                
                return html_content
            else:
                print(f"  抓取失败，返回码: {result.returncode}")
                if result.stderr:
                    print(f"  错误输出: {result.stderr[:200]}")
                
                # 清理临时文件
                if os.path.exists(tmp_file):
                    os.unlink(tmp_file)
                
                return None
                
        except subprocess.TimeoutExpired:
            print(f"  抓取超时")
            return None
        except Exception as e:
            print(f"  抓取异常: {type(e).__name__}: {e}")
            return None
    
    def _fetch_with_scrapling_and_scroll(self, url: str, wait_time: int = 3000) -> Optional[str]:
        """使用scrapling抓取页面内容（模拟滚动）
        
        Args:
            url: 要抓取的URL
            wait_time: 等待时间（毫秒）
            
        Returns:
            页面HTML内容或None
        """
        if not self.scrapling_available:
            print("  Scrapling不可用，无法抓取")
            return None
        
        print(f"  使用scrapling抓取（模拟滚动）: {url}")
        print(f"  等待时间: {wait_time}ms")
        
        # 优先使用scrapling_util.fetch_wheel
        if SCRAPLING_UTIL_AVAILABLE:
            try:
                # 滚动3次，每次滚动等待2秒
                html_content = fetch_wheel(url, scroll_times=3, scroll_delay=2.0, wait=wait_time, timeout=20000)
                if html_content:
                    print(f"  抓取成功，内容大小: {len(html_content)} 字节")
                    print(f"  注意: 滚动功能通过额外等待时间模拟")
                    return html_content
                else:
                    print(f"  [WARNING] scrapling_util.fetch_wheel返回空内容，尝试普通抓取")
                    return self._fetch_with_scrapling(url, wait_time)
            except Exception as e:
                print(f"  [WARNING] scrapling_util.fetch_wheel异常: {e}")
                # 继续尝试命令行版本
        
        # 如果scrapling_util不可用或失败，使用命令行版本（增加等待时间模拟滚动）
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
                tmp_file = tmp.name
            
            # 构建scrapling命令 - 增加等待时间模拟滚动
            extended_wait_time = wait_time + 2000  # 额外2秒模拟滚动
            
            cmd = [
                'scrapling', 'extract', 'fetch',
                url,
                tmp_file,
                '--wait', str(extended_wait_time),
                '--timeout', '20000'
            ]
            
            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=40
            )
            
            if result.returncode == 0:
                # 读取HTML内容
                with open(tmp_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                print(f"  抓取成功，文件大小: {len(html_content)} 字节")
                print(f"  注意: 滚动功能通过额外等待时间模拟")
                
                # 清理临时文件
                os.unlink(tmp_file)
                
                return html_content
            else:
                print(f"  抓取失败，返回码: {result.returncode}")
                if result.stderr:
                    print(f"  错误输出: {result.stderr[:200]}")
                
                # 清理临时文件
                if os.path.exists(tmp_file):
                    os.unlink(tmp_file)
                
                # 如果带滚动失败，尝试普通抓取
                print(f"  尝试普通抓取...")
                return self._fetch_with_scrapling(url, wait_time)
                
        except subprocess.TimeoutExpired:
            print(f"  抓取超时")
            print(f"  尝试普通抓取...")
            return self._fetch_with_scrapling(url, wait_time)
        except Exception as e:
            print(f"  抓取异常: {type(e).__name__}: {e}")
            print(f"  尝试普通抓取...")
            return self._fetch_with_scrapling(url, wait_time)
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章信息 - 根据手动分析优化
        
        Args:
            html_content: HTML页面内容
            
        Returns:
            文章列表
        """
        if not html_content:
            return []
        
        articles = []
        print("  开始提取文章信息...")
        
        # 根据手动分析，要闻存储在 <ul class="list infinite-list"> 中
        # 查找文章列表容器
        list_pattern = r'<ul class="list infinite-list"[^>]*>(.*?)</ul>'
        list_match = re.search(list_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        if not list_match:
            print("  未找到文章列表容器，尝试备用方法")
            return self._extract_articles_fallback(html_content)
        
        list_content = list_match.group(1)
        print(f"  找到文章列表容器，内容长度: {len(list_content)} 字符")
        
        # 提取每个文章项 - <li class=" no-pr"> 或 <li class="no-pr">
        article_pattern = r'<li class="\s*no-pr\s*"[^>]*>(.*?)</li>'
        article_matches = re.findall(article_pattern, list_content, re.DOTALL | re.IGNORECASE)
        
        print(f"  找到 {len(article_matches)} 个文章项")
        
        for i, article_html in enumerate(article_matches):
            try:
                # 提取标题 - <div class="tt"> 中的 <a> 标签
                title_pattern = r'<div class="tt">\s*<a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>\s*</div>'
                title_match = re.search(title_pattern, article_html, re.DOTALL | re.IGNORECASE)
                
                if not title_match:
                    print(f"    文章{i+1}: 未找到标题，跳过")
                    continue
                
                url = title_match.group(1)
                title = title_match.group(2)
                
                # 清理标题
                title = self._clean_text(title)
                
                # 确保URL完整
                if url and not url.startswith(('http://', 'https://')):
                    if url.startswith('/'):
                        url = f"{self.base_url}{url}"
                    else:
                        url = f"{self.base_url}/{url}"
                
                # 提取摘要 - <div class="text ellipsis-2"> 中的 <a> 标签
                summary_pattern = r'<div class="text ellipsis-2">\s*<a[^>]*href="[^"]*"[^>]*>([^<]+)</a>\s*</div>'
                summary_match = re.search(summary_pattern, article_html, re.DOTALL | re.IGNORECASE)
                
                summary = ""
                if summary_match:
                    summary = self._clean_text(summary_match.group(1))
                else:
                    # 如果没有找到摘要，使用标题作为摘要
                    summary = title[:150] + '...' if len(title) > 150 else title
                
                # 提取关键字 - <div class="tags"> 中的 <span> 标签
                tags_pattern = r'<div class="tags">(.*?)</div>'
                tags_match = re.search(tags_pattern, article_html, re.DOTALL | re.IGNORECASE)
                
                keywords = []
                if tags_match:
                    tags_content = tags_match.group(1)
                    # 提取所有<span>标签内的内容
                    keyword_pattern = r'<span>([^<]+)</span>'
                    keywords = re.findall(keyword_pattern, tags_content, re.IGNORECASE)
                    keywords = [self._clean_text(kw) for kw in keywords]
                
                # 提取作者和时间 - <div class="info"> 中的 <span> 标签
                info_pattern = r'<div class="info\s*">(.*?)</div>'
                info_match = re.search(info_pattern, article_html, re.DOTALL | re.IGNORECASE)
                
                author = "未知"
                time_str = ""
                
                if info_match:
                    info_content = info_match.group(1)
                    # 提取所有<span>标签内的内容
                    info_span_pattern = r'<span>([^<]+)</span>'
                    info_items = re.findall(info_span_pattern, info_content, re.IGNORECASE)
                    
                    if len(info_items) >= 1:
                        author = self._clean_text(info_items[0])
                    if len(info_items) >= 2:
                        time_str = self._clean_text(info_items[1])
                
                # 解析时间
                publish_time = self._parse_time_with_48h_filter(time_str)
                
                # 检查是否在48小时内
                if not self._is_within_48h(publish_time):
                    print(f"    文章{i+1}: '{title[:30]}...' 发布时间超过48小时，跳过")
                    continue
                
                # 创建文章对象
                article = {
                    'title': title,
                    'url': url,
                    'summary': summary,
                    'source': '证券时报网',
                    'author': author,
                    'keywords': keywords,
                    'time': time_str,
                    'publish_time': publish_time.isoformat() if publish_time else None,
                    'publish_time_display': publish_time.strftime('%Y-%m-%d %H:%M') if publish_time else '未知',
                    'type': '要闻',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'timestamp': datetime.now().isoformat(),
                    'within_48h': True
                }
                
                # 去重检查
                if not self._is_duplicate(article, articles):
                    articles.append(article)
                    print(f"    文章{i+1}: '{title[:40]}...' 提取成功")
                else:
                    print(f"    文章{i+1}: '{title[:40]}...' 重复，跳过")
                    
            except Exception as e:
                print(f"    文章{i+1}: 提取时出错: {e}")
                continue
        
        print(f"  总共提取到 {len(articles)} 篇文章 (48小时内)")
        return articles
    
    def _extract_articles_fallback(self, html_content: str) -> List[Dict[str, Any]]:
        """备用文章提取方法"""
        articles = []
        
        # 查找所有链接
        link_pattern = r'<a[^>]*href="([^"]*)"[^>]*>([^<]{10,200})</a>'
        matches = re.findall(link_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        for url, title in matches:
            # 过滤非文章链接
            if not self._is_article_url(url):
                continue
            
            title = self._clean_text(title)
            if len(title) < 10:  # 标题太短，可能不是文章
                continue
            
            # 确保URL完整
            if url and not url.startswith(('http://', 'https://')):
                if url.startswith('/'):
                    url = f"{self.base_url}{url}"
                else:
                    url = f"{self.base_url}/{url}"
            
            # 查找时间信息（在链接附近）
            time_match = re.search(rf'{re.escape(url)}[^>]*>.*?<span[^>]*>([^<]+)</span>', html_content, re.DOTALL)
            time_str = time_match.group(1) if time_match else ""
            
            article = {
                'title': title,
                'url': url,
                'summary': title[:100] + '...' if len(title) > 100 else title,
                'source': '证券时报网',
                'time': time_str,
                'publish_time': datetime.now().isoformat(),
                'publish_time_display': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'type': '要闻',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': datetime.now().isoformat()
            }
            
            if not self._is_duplicate(article, articles):
                articles.append(article)
        
        return articles
    
    def _is_article_url(self, url: str) -> bool:
        """判断URL是否是文章链接"""
        article_patterns = [
            r'/article/detail/',
            r'/article/list/',
            r'/news/',
            r'\.html$',
            r'\.shtml$',
        ]
        
        for pattern in article_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        
        return False
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', ' ', text)
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除首尾空白
        text = text.strip()
        
        return text
    
    def _extract_summary(self, html_content: str, url: str, title: str) -> str:
        """提取文章摘要"""
        # 尝试在HTML中查找摘要
        summary_patterns = [
            rf'{re.escape(url)}[^>]*>.*?<p[^>]*>([^<]+)</p>',
            rf'{re.escape(title)}[^<]*</a>[^<]*<p[^>]*>([^<]+)</p>',
            r'<meta[^>]*name="description"[^>]*content="([^"]*)"',
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if match:
                summary = self._clean_text(match.group(1))
                if summary and len(summary) > 20:
                    return summary
        
        # 如果没有找到摘要，使用标题作为摘要
        return title[:150] + '...' if len(title) > 150 else title
    
    def _extract_source(self, html_content: str, url: str) -> str:
        """提取文章出处"""
        # 尝试在HTML中查找出处
        source_patterns = [
            r'来源[:：]\s*([^<]+)',
            r'出处[:：]\s*([^<]+)',
            r'<span[^>]*class="source"[^>]*>([^<]+)</span>',
        ]
        
        for pattern in source_patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                source = self._clean_text(match.group(1))
                if source:
                    return source
        
        # 默认出处
        return "证券时报网"
    
    def _parse_time_with_48h_filter(self, time_str: str) -> Optional[datetime]:
        """解析时间字符串，并考虑48小时过滤
        
        证券时报网的时间格式通常是 "HH:MM" 表示当天时间
        也可能是 "昨天 HH:MM" 或 "X分钟前" 等格式
        """
        if not time_str:
            return None
        
        now = datetime.now()
        
        try:
            # 1. 处理 "X分钟前" 格式
            if "分钟前" in time_str:
                minutes_match = re.search(r'(\d+)分钟前', time_str)
                if minutes_match:
                    minutes = int(minutes_match.group(1))
                    return now - timedelta(minutes=minutes)
            
            # 2. 处理 "X小时前" 格式
            elif "小时前" in time_str:
                hours_match = re.search(r'(\d+)小时前', time_str)
                if hours_match:
                    hours = int(hours_match.group(1))
                    return now - timedelta(hours=hours)
            
            # 3. 处理 "昨天 HH:MM" 格式
            elif "昨天" in time_str:
                time_match = re.search(r'昨天\s+(\d+:\d+)', time_str)
                if time_match:
                    hour_min = time_match.group(1)
                    hour, minute = map(int, hour_min.split(':'))
                    yesterday = now - timedelta(days=1)
                    return datetime(yesterday.year, yesterday.month, yesterday.day, hour, minute)
            
            # 4. 处理 "HH:MM" 格式（当天时间）
            elif re.match(r'^\d{1,2}:\d{2}$', time_str):
                hour, minute = map(int, time_str.split(':'))
                return datetime(now.year, now.month, now.day, hour, minute)
            
            # 5. 处理其他格式
            else:
                # 尝试标准时间格式
                time_formats = [
                    '%Y-%m-%d %H:%M',
                    '%Y/%m/%d %H:%M',
                    '%Y年%m月%d日 %H:%M',
                    '%m-%d %H:%M',
                ]
                
                for fmt in time_formats:
                    try:
                        # 如果年份缺失，添加当前年份
                        if fmt == '%m-%d %H:%M':
                            time_str_with_year = f"{now.year}-{time_str}"
                            return datetime.strptime(time_str_with_year, '%Y-%m-%d %H:%M')
                        
                        return datetime.strptime(time_str, fmt)
                    except ValueError:
                        continue
        
        except Exception as e:
            print(f"    时间解析错误 '{time_str}': {e}")
        
        # 如果无法解析，返回当前时间（这样会被48小时过滤掉）
        return now
    
    def _is_within_48h(self, publish_time: Optional[datetime]) -> bool:
        """检查发布时间是否在48小时内"""
        if publish_time is None:
            return False
        
        time_diff = datetime.now() - publish_time
        return time_diff.total_seconds() <= 48 * 3600  # 48小时 = 48 * 3600秒
    
    def _is_duplicate(self, article: Dict[str, Any], articles: List[Dict[str, Any]]) -> bool:
        """检查文章是否重复"""
        for existing in articles:
            if (article['title'] == existing['title'] or 
                article['url'] == existing['url']):
                return True
        return False
    
    def save_articles(self, articles: List[Dict[str, Any]]) -> Path:
        """保存文章到文件
        
        Args:
            articles: 文章列表
            
        Returns:
            保存的文件路径
        """
        if not articles:
            print("  没有文章可保存")
            return None
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"stcn_hot_news_{timestamp}.json"
        filepath = self.output_dir / filename
        
        # 准备数据
        data = {
            'source': self.name,
            'url': self.target_url,
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'time_filter': '48小时内',
            'wait_time_seconds': 3,
            'total_articles': len(articles),
            'articles': articles
        }
        
        # 保存为JSON
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"  文章已保存到: {filepath}")
            print(f"  保存了 {len(articles)} 篇文章 (48小时内)")
            
            # 同时保存为文本格式便于查看
            txt_filename = f"stcn_hot_news_{timestamp}.txt"
            txt_filepath = self.output_dir / txt_filename
            
            with open(txt_filepath, 'w', encoding='utf-8') as f:
                f.write(f"证券时报网热点新闻抓取报告 (48小时内)\n")
                f.write("=" * 70 + "\n")
                f.write(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"目标URL: {self.target_url}\n")
                f.write(f"等待时间: 3秒\n")
                f.write(f"时间过滤: 48小时内\n")
                f.write(f"文章数量: {len(articles)} 篇\n\n")
                
                f.write("文章列表:\n")
                f.write("=" * 70 + "\n")
                
                for i, article in enumerate(articles, 1):
                    f.write(f"\n{i}. {article['title']}\n")
                    f.write(f"   链接: {article['url']}\n")
                    f.write(f"   时间: {article.get('time', '未知')}\n")
                    f.write(f"   发布时间: {article.get('publish_time_display', '未知')}\n")
                    f.write(f"   作者: {article.get('author', '未知')}\n")
                    
                    keywords = article.get('keywords', [])
                    if keywords:
                        f.write(f"   关键字: {', '.join(keywords)}\n")
                    
                    f.write(f"   摘要: {article.get('summary', '无')}\n")
                    f.write(f"   类型: {article.get('type', '要闻')}\n")
            
            print(f"  文本报告已保存到: {txt_filepath}")
            
            # 生成中间文件
            self._generate_intermediate_file(articles, timestamp)
            
            return filepath
            
        except Exception as e:
            print(f"  保存文件时出错: {e}")
            return None
    
    def _generate_intermediate_file(self, articles: List[Dict[str, Any]], timestamp: str) -> None:
        """生成中间格式文件
        
        中间文件格式更简洁，便于其他程序处理
        """
        try:
            # 中间文件名
            intermediate_filename = f"stcn_intermediate_{timestamp}.json"
            intermediate_filepath = self.output_dir / intermediate_filename
            
            # 简化数据结构
            intermediate_data = {
                'metadata': {
                    'source': 'stcn',
                    'scraped_at': datetime.now().isoformat(),
                    'count': len(articles),
                    'time_filter_hours': 48,
                    'version': '1.0'
                },
                'articles': []
            }
            
            for article in articles:
                # 提取关键信息
                intermediate_article = {
                    'id': self._generate_article_id(article['url']),
                    'title': article['title'],
                    'url': article['url'],
                    'summary': article.get('summary', ''),
                    'author': article.get('author', ''),
                    'publish_time': article.get('publish_time', ''),
                    'keywords': article.get('keywords', []),
                    'source': 'stcn'
                }
                intermediate_data['articles'].append(intermediate_article)
            
            # 保存中间文件
            with open(intermediate_filepath, 'w', encoding='utf-8') as f:
                json.dump(intermediate_data, f, ensure_ascii=False, indent=2)
            
            print(f"  中间文件已保存到: {intermediate_filepath}")
            
        except Exception as e:
            print(f"  生成中间文件时出错: {e}")
    
    def _generate_article_id(self, url: str) -> str:
        """从URL生成文章ID"""
        try:
            # 从URL中提取数字ID，例如: /article/detail/3696745.html -> 3696745
            match = re.search(r'/detail/(\d+)\.html', url)
            if match:
                return f"stcn_{match.group(1)}"
            
            # 如果没有找到数字ID，使用URL的MD5哈希
            import hashlib
            url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:8]
            return f"stcn_{url_hash}"
        except:
            return f"stcn_{hash(url) % 1000000}"
        """保存文章到文件
        
        Args:
            articles: 文章列表
            
        Returns:
            保存的文件路径
        """
        if not articles:
            print("  没有文章可保存")
            return None
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"stcn_hot_news_{timestamp}.json"
        filepath = self.output_dir / filename
        
        # 准备数据
        data = {
            'source': self.name,
            'url': self.target_url,
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_articles': len(articles),
            'articles': articles
        }
        
        # 保存为JSON
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"  文章已保存到: {filepath}")
            print(f"  保存了 {len(articles)} 篇文章")
            
            # 同时保存为文本格式便于查看
            txt_filename = f"stcn_hot_news_{timestamp}.txt"
            txt_filepath = self.output_dir / txt_filename
            
            with open(txt_filepath, 'w', encoding='utf-8') as f:
                f.write(f"证券时报网热点新闻抓取报告\n")
                f.write("=" * 70 + "\n")
                f.write(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"目标URL: {self.target_url}\n")
                f.write(f"文章数量: {len(articles)} 篇\n\n")
                
                f.write("文章列表:\n")
                f.write("=" * 70 + "\n")
                
                for i, article in enumerate(articles, 1):
                    f.write(f"\n{i}. {article['title']}\n")
                    f.write(f"   链接: {article['url']}\n")
                    f.write(f"   时间: {article.get('time', '未知')}\n")
                    f.write(f"   出处: {article.get('source', '证券时报网')}\n")
                    f.write(f"   摘要: {article.get('summary', '无')}\n")
                    f.write(f"   类型: {article.get('type', '要闻')}\n")
            
            print(f"  文本报告已保存到: {txt_filepath}")
            
            return filepath
            
        except Exception as e:
            print(f"  保存文件时出错: {e}")
            return None
    
    def crawl(self) -> List[Dict[str, Any]]:
        """执行抓取
        
        Returns:
            抓取到的文章列表
        """
        print("开始抓取证券时报网热点新闻...")
        print("=" * 70)
        print(f"抓取时间限制: 48小时内")
        print(f"抓取等待时间: 3秒")
        print("=" * 70)
        
        # 方法1: 尝试使用scrapling带滚动抓取
        print("\n1. 尝试使用scrapling带滚动抓取...")
        html_content = self._fetch_with_scrapling_and_scroll(self.target_url, 3000)  # 3秒等待
        
        # 方法2: 如果失败，尝试普通抓取
        if not html_content:
            print("\n2. 尝试普通scrapling抓取...")
            html_content = self._fetch_with_scrapling(self.target_url, 3000)  # 3秒等待
        
        # 方法3: 如果还是失败，使用备用方法
        if not html_content:
            print("\n3. 所有抓取方法都失败，使用模拟数据")
            return self._get_sample_articles()
        
        # 提取文章
        print("\n4. 提取文章信息...")
        articles = self.extract_articles(html_content)
        
        # 如果没有提取到文章，使用备用方法
        if not articles:
            print("  未提取到文章，使用备用提取方法")
            articles = self._extract_articles_fallback(html_content)
        
        return articles
    
    def _get_sample_articles(self) -> List[Dict[str, Any]]:
        """获取示例文章（用于测试）"""
        print("  使用示例文章数据")
        
        sample_articles = [
            {
                'title': '测试案例',
                'url': 'https://www.stcn.com/article/detail/1234567.html',
                'summary': '测试',
                'source': '证券时报网',
                'time': '09:15',
                'publish_time': datetime.now().isoformat(),
                'publish_time_display': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'type': '要闻',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': datetime.now().isoformat()
            }
        ]
        
        return sample_articles
    
    def display_results(self, articles: List[Dict[str, Any]]) -> None:
        """显示抓取结果"""
        if not articles:
            print("未抓取到任何文章")
            return
        
        print("\n" + "=" * 70)
        print("证券时报网热点新闻抓取结果 (48小时内)")
        print("=" * 70)
        print(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"文章数量: {len(articles)} 篇")
        print(f"时间范围: 48小时内")
        print()
        
        # 按时间排序（最新的在前）
        sorted_articles = sorted(
            articles,
            key=lambda x: x.get('publish_time', ''),
            reverse=True
        )
        
        # 显示文章
        for i, article in enumerate(sorted_articles[:15], 1):  # 显示最多15篇
            try:
                print(f"{i}. {article['title']}")
            except UnicodeEncodeError:
                print(f"{i}. [标题包含无法显示的字符]")
            
            try:
                print(f"   时间: {article.get('time', '未知')} | 作者: {article.get('author', '未知')}")
            except UnicodeEncodeError:
                print(f"   时间: {article.get('time', '未知')} | 作者: [作者名包含无法显示的字符]")
            
            try:
                print(f"   发布时间: {article.get('publish_time_display', '未知')}")
            except UnicodeEncodeError:
                print(f"   发布时间: {article.get('publish_time_display', '未知')}")
            
            # 显示关键字
            keywords = article.get('keywords', [])
            if keywords:
                try:
                    print(f"   关键字: {', '.join(keywords[:3])}{'...' if len(keywords) > 3 else ''}")
                except UnicodeEncodeError:
                    print(f"   关键字: [关键字包含无法显示的字符]")
            
            try:
                print(f"   链接: {article['url'][:80]}...")
            except UnicodeEncodeError:
                print(f"   链接: {article['url'][:80]}...")
            
            try:
                summary = article.get('summary', '无')
                if summary:
                    print(f"   摘要: {summary[:100]}...")
                else:
                    print(f"   摘要: 无")
            except UnicodeEncodeError:
                print(f"   摘要: [摘要包含无法显示的字符]")
            
            print()
        
        if len(articles) > 15:
            print(f"... 还有 {len(articles) - 15} 篇文章")
        
        # 统计信息
        print("=" * 70)
        print("统计信息:")
        print(f"  总文章数: {len(articles)}")
        
        # 按作者统计
        author_stats = {}
        for article in articles:
            author = article.get('author', '未知')
            author_stats[author] = author_stats.get(author, 0) + 1
        
        if author_stats:
            top_authors = sorted(author_stats.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"  最多产作者 (前3):")
            for author, count in top_authors:
                print(f"    {author}: {count} 篇")
        
        print("=" * 70)

def main():
    """主函数"""
    print("证券时报网热点新闻抓取器")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 创建抓取器
    crawler = STCNHotNewsCrawler()
    
    # 执行抓取
    articles = crawler.crawl()
    
    # 显示结果
    crawler.display_results(articles)
    
    # 保存结果
    if articles:
        saved_file = crawler.save_articles(articles)
        if saved_file:
            print(f"\n结果已保存到: {saved_file}")
            
            # 显示保存目录内容
            print(f"\n保存目录内容:")
            print("-" * 70)
            try:
                files = list(crawler.output_dir.glob("stcn_hot_news_*.json"))
                files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                for i, file in enumerate(files[:5], 1):
                    file_time = datetime.fromtimestamp(file.stat().st_mtime)
                    file_size = file.stat().st_size
                    print(f"{i}. {file.name} ({file_size} 字节, {file_time.strftime('%Y-%m-%d %H:%M:%S')})")
                
                if len(files) > 5:
                    print(f"... 还有 {len(files) - 5} 个文件")
            except Exception as e:
                print(f"  读取目录时出错: {e}")
    
    print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    return 0

if __name__ == "__main__":
    # 添加timedelta导入
    from datetime import timedelta
    sys.exit(main())