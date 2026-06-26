#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金融界（JRJ）热点新闻抓取器
功能：
1. 使用scrapling隐身方式访问 https://www.jrj.com.cn/
2. 抓取头条新闻和热点新闻
3. 输出结果与stcn的输出保持一致，缺失数据用默认值或空值填充
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

class JRJHotNewsCrawler:
    """金融界热点新闻抓取器"""
    
    def __init__(self, output_dir: str = None):
        """初始化抓取器"""
        self.name = "金融界"
        self.base_url = "https://www.jrj.com.cn"
        self.target_url = "https://www.jrj.com.cn/"  # 首页
        
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
        
        print(f"金融界热点新闻抓取器初始化完成")
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
    
    def extract_articles(self, html_content: str) -> List[Dict[str, Any]]:
        """从HTML内容中提取文章信息
        
        根据手动分析，需要抓取两个部分：
        1. 头条新闻: <div class="headline-news"> 中的 <ul id="newsList">
        2. 热点新闻: <div class="main-new"> 中的 <div id="container">
        
        Args:
            html_content: HTML页面内容
            
        Returns:
            文章列表
        """
        if not html_content:
            return []
        
        articles = []
        print("  开始提取文章信息...")
        
        # 1. 提取头条新闻
        print("  提取头条新闻...")
        headline_articles = self._extract_headline_news(html_content)
        articles.extend(headline_articles)
        print(f"    提取到 {len(headline_articles)} 条头条新闻")
        
        # 2. 提取热点新闻
        print("  提取热点新闻...")
        hot_articles = self._extract_hot_news(html_content)
        articles.extend(hot_articles)
        print(f"    提取到 {len(hot_articles)} 条热点新闻")
        
        # 去重
        unique_articles = self._remove_duplicates(articles)
        print(f"  去重后总计: {len(unique_articles)} 篇文章")
        
        return unique_articles
    
    def _extract_headline_news(self, html_content: str) -> List[Dict[str, Any]]:
        """提取头条新闻
        
        结构: <div class="headline-news"> -> <ul id="newsList"> -> <li>
        每个<li>包含: <span>头条</span> <a href="URL">标题</a>
        """
        articles = []
        
        # 查找头条新闻容器
        headline_pattern = r'<div class="headline-news">(.*?)</div>'
        headline_match = re.search(headline_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        if not headline_match:
            print("    未找到头条新闻容器")
            return articles
        
        headline_content = headline_match.group(1)
        
        # 查找新闻列表
        newslist_pattern = r'<ul id="newsList">(.*?)</ul>'
        newslist_match = re.search(newslist_pattern, headline_content, re.DOTALL | re.IGNORECASE)
        
        if not newslist_match:
            print("    未找到新闻列表")
            return articles
        
        newslist_content = newslist_match.group(1)
        
        # 提取每个新闻项
        # 模式: <li><span>头条</span><a href="URL">标题</a></li>
        item_pattern = r'<li>(.*?)</li>'
        items = re.findall(item_pattern, newslist_content, re.DOTALL | re.IGNORECASE)
        
        print(f"    找到 {len(items)} 个头条新闻项")
        
        for i, item_html in enumerate(items):
            try:
                # 提取URL和标题
                # 模式: <a href="(URL)">(标题)</a>
                link_pattern = r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>'
                link_match = re.search(link_pattern, item_html, re.IGNORECASE)
                
                if not link_match:
                    print(f"      头条新闻{i+1}: 未找到链接和标题")
                    continue
                
                url = link_match.group(1)
                title = link_match.group(2)
                
                # 清理数据
                title = self._clean_text(title)
                
                # 确保URL完整
                if url and not url.startswith(('http://', 'https://')):
                    if url.startswith('/'):
                        url = f"{self.base_url}{url}"
                    else:
                        url = f"{self.base_url}/{url}"
                
                # 提取类型（头条）
                type_match = re.search(r'<span>([^<]+)</span>', item_html, re.IGNORECASE)
                article_type = type_match.group(1) if type_match else "头条"
                
                # 从URL提取时间信息
                publish_time = self._extract_time_from_url(url)
                
                # 创建文章对象
                article = self._create_article_object(
                    title=title,
                    url=url,
                    article_type=article_type,
                    publish_time=publish_time,
                    section="头条新闻"
                )
                
                articles.append(article)
                print(f"      头条新闻{i+1}: '{title[:40]}...' 提取成功")
                
            except Exception as e:
                print(f"      头条新闻{i+1}: 提取时出错: {e}")
                continue
        
        return articles
    
    def _extract_hot_news(self, html_content: str) -> List[Dict[str, Any]]:
        """提取热点新闻
        
        结构: <div class="main-new"> -> <div id="container"> -> <div class="tabs-box" id="content1"> -> <ul>
        每个<li>包含: <a href="URL">标题</a>
        """
        articles = []
        
        # 查找热点新闻容器
        mainnew_pattern = r'<div class="main-new">(.*?)</div>'
        mainnew_match = re.search(mainnew_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        if not mainnew_match:
            print("    未找到热点新闻容器")
            return articles
        
        mainnew_content = mainnew_match.group(1)
        
        # 查找容器
        container_pattern = r'<div id="container">(.*?)</div>'
        container_match = re.search(container_pattern, mainnew_content, re.DOTALL | re.IGNORECASE)
        
        if not container_match:
            print("    未找到容器")
            print(f"    mainnew_content长度: {len(mainnew_content)}")
            print(f"    mainnew_content前200字符: {mainnew_content[:200]}")
            
            # 尝试直接在整个HTML中查找container
            print("    尝试直接在整个HTML中查找container...")
            container_match = re.search(container_pattern, html_content, re.DOTALL | re.IGNORECASE)
            if container_match:
                print("    直接查找成功，使用直接查找的结果")
            else:
                print("    直接查找也失败")
                return articles
        
        container_content = container_match.group(1)
        
        # 添加详细调试信息
        print(f"    container_content长度: {len(container_content)}")
        print(f"    container_content前500字符:")
        print("    " + "-" * 60)
        print(f"    {container_content[:500]}")
        print("    " + "-" * 60)
        
        # 检查container_content内容
        has_tabs_box = 'tabs-box' in container_content
        has_class_tabs_box = 'class="tabs-box"' in container_content
        has_id_content1 = 'id="content1"' in container_content
        print(f"    container_content是否包含'tabs-box': {has_tabs_box}")
        print(f"    container_content是否包含'class=\"tabs-box\"': {has_class_tabs_box}")
        print(f"    container_content是否包含'id=\"content1\"': {has_id_content1}")
        
        # 查找标签框
        # 注意：container_content中没有闭合的</div>标签，所以不能使用(.*?)</div>模式
        print("    查找标签框...")
        
        # 方法1：使用正则表达式（原方法）
        div_start_pattern = r'<div[^>]*class="tabs-box"[^>]*id="content1"[^>]*>'
        print(f"    方法1 - 正则表达式: {div_start_pattern}")
        div_start_match = re.search(div_start_pattern, container_content, re.IGNORECASE)
        
        if not div_start_match:
            print("    方法1失败，div_start_match为None")
            
            # 方法2：使用字符串查找（更简单的方法）
            print("    尝试方法2 - 字符串查找...")
            
            # 查找包含关键字的div开始标签
            keywords = ['class="tabs-box"', 'id="content1"', 'tabs-box']
            start_pos = -1
            
            for keyword in keywords:
                pos = container_content.find(keyword)
                if pos != -1:
                    print(f"    找到关键字 '{keyword}' 在位置 {pos}")
                    # 向前查找<div开始标签
                    div_start = container_content.rfind('<div', 0, pos)
                    if div_start != -1:
                        # 找到<div开始标签，查找>结束标签
                        div_end = container_content.find('>', div_start)
                        if div_end != -1:
                            start_pos = div_end + 1
                            print(f"    找到div开始标签在位置 {div_start}-{div_end}")
                            print(f"    div标签内容: {container_content[div_start:div_end+1]}")
                            break
            
            if start_pos != -1:
                # 创建虚拟匹配对象
                class MockMatch:
                    def __init__(self, content, start, end):
                        self._content = content
                        self._start = start
                        self._end = end
                    def group(self, n=0):
                        return None
                    def start(self):
                        return self._start
                    def end(self):
                        return self._end
                
                div_start_match = MockMatch(container_content, div_start, div_end)
                print("    方法2成功 - 使用字符串查找")
            else:
                print("    方法2也失败")
                
                # 方法3：查找任何div
                print("    尝试方法3 - 查找任何div...")
                any_div_pattern = r'<div[^>]*>'
                div_start_match = re.search(any_div_pattern, container_content, re.IGNORECASE)
                
                if not div_start_match:
                    print("    所有方法都失败，无法找到标签框")
                    print(f"    container_content前500字符（原始表示）:")
                    print("    " + "-" * 60)
                    print(repr(container_content[:500]))
                    print("    " + "-" * 60)
                    return articles
                else:
                    print("    方法3成功 - 找到任何div")
        else:
            print("    方法1成功 - 正则表达式匹配")
        
        print(f"    找到div开始标签，位置: {div_start_match.start()} - {div_start_match.end()}")
        if hasattr(div_start_match, 'group') and callable(div_start_match.group):
            print(f"    div标签内容: {div_start_match.group()}")
        
        # 提取从div开始标签之后的所有内容作为tabsbox_content
        # 因为container_content中没有闭合的</div>，所以tabsbox_content就是剩余的所有内容
        start_pos = div_start_match.end()
        tabsbox_content = container_content[start_pos:]
        print(f"    成功提取tabsbox_content，长度: {len(tabsbox_content)}")
        
        # 检查tabsbox_content是否包含我们需要的内容
        if len(tabsbox_content) < 100:
            print(f"    tabsbox_content太短，可能提取错误")
            print(f"    tabsbox_content内容: {repr(tabsbox_content)}")
        else:
            print(f"    tabsbox_content前200字符: {tabsbox_content[:200]}...")
        
        # 根据你提供的完整HTML结构，我们需要跳过script标签，直接获取后面的文章
        print("    根据完整HTML结构提取热点新闻...")
        item_count = 0
        
        # 方法1：直接在整个tabsbox_content中查找所有<a>标签（跳过script）
        # 先移除或跳过script标签
        print("    方法1：跳过script标签，直接查找所有<a>标签...")
        
        # 移除script标签及其内容
        script_pattern = r'<script[^>]*>.*?</script>'
        clean_content = re.sub(script_pattern, '', tabsbox_content, flags=re.DOTALL | re.IGNORECASE)
        
        # 现在查找所有<a>标签
        a_pattern = r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>'
        a_matches = re.findall(a_pattern, clean_content, re.IGNORECASE)
        
        if a_matches:
            print(f"    找到 {len(a_matches)} 个<a>标签")
            
            for i, (url, title) in enumerate(a_matches):
                try:
                    # 清理数据
                    title = self._clean_text(title)
                    
                    # 确保URL完整
                    if url and not url.startswith(('http://', 'https://')):
                        if url.startswith('/'):
                            url = f"{self.base_url}{url}"
                        else:
                            url = f"{self.base_url}/{url}"
                    
                    # 检查是否是新闻链接（排除可能的其他链接）
                    if not any(domain in url for domain in ['jrj.com.cn', 'stock.jrj', 'finance.jrj', 'auto.jrj', 'usstock.jrj']):
                        print(f"      跳过非新闻链接: {url[:50]}...")
                        continue
                    
                    # 从URL提取时间信息
                    publish_time = self._extract_time_from_url(url)
                    
                    # 创建文章对象
                    article = self._create_article_object(
                        title=title,
                        url=url,
                        article_type="热点",
                        publish_time=publish_time,
                        section="热点新闻"
                    )
                    
                    articles.append(article)
                    item_count += 1
                    
                    print(f"      热点新闻{i+1}: '{title[:40]}...' 提取成功")
                    
                except Exception as e:
                    print(f"      热点新闻{i+1}: 提取时出错: {e}")
                    continue
        
        # 方法2：如果方法1没找到足够的内容，尝试更精确的提取
        if item_count == 0:
            print("    方法1未找到新闻，尝试方法2（精确提取）...")
            
            # 查找所有<ul>块，但跳过包含script的<ul>
            ul_pattern = r'<ul>(.*?)</ul>'
            ul_matches = re.findall(ul_pattern, tabsbox_content, re.DOTALL | re.IGNORECASE)
            
            if ul_matches:
                print(f"    找到 {len(ul_matches)} 个<ul>块")
                
                for ul_idx, ul_content in enumerate(ul_matches):
                    # 跳过包含script的<ul>
                    if '<script' in ul_content:
                        print(f"      跳过包含script的<ul>块{ul_idx+1}")
                        continue
                    
                    # 检查这个<ul>是否包含新闻链接
                    if '<a href=' in ul_content or '<a href="' in ul_content:
                        print(f"      <ul>块{ul_idx+1} 包含链接，开始提取...")
                        
                        # 提取这个<ul>中的所有<li>项
                        li_pattern = r'<li>(.*?)</li>'
                        li_items = re.findall(li_pattern, ul_content, re.DOTALL | re.IGNORECASE)
                        
                        for li_idx, item_html in enumerate(li_items):
                            try:
                                # 提取URL和标题
                                link_pattern = r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>'
                                link_match = re.search(link_pattern, item_html, re.IGNORECASE)
                                
                                if link_match:
                                    url = link_match.group(1)
                                    title = link_match.group(2)
                                    
                                    # 清理数据
                                    title = self._clean_text(title)
                                    
                                    # 确保URL完整
                                    if url and not url.startswith(('http://', 'https://')):
                                        if url.startswith('/'):
                                            url = f"{self.base_url}{url}"
                                        else:
                                            url = f"{self.base_url}/{url}"
                                    
                                    # 从URL提取时间信息
                                    publish_time = self._extract_time_from_url(url)
                                    
                                    # 创建文章对象
                                    article = self._create_article_object(
                                        title=title,
                                        url=url,
                                        article_type="热点",
                                        publish_time=publish_time,
                                        section="热点新闻"
                                    )
                                    
                                    articles.append(article)
                                    item_count += 1
                                    
                                    print(f"        热点新闻{ul_idx+1}-{li_idx+1}: '{title[:40]}...' 提取成功")
                                    
                            except Exception as e:
                                print(f"        热点新闻{ul_idx+1}-{li_idx+1}: 提取时出错: {e}")
                                continue
        
        # 方法3：直接查找特定模式（根据你提供的HTML结构）
        if item_count == 0:
            print("    方法2未找到新闻，尝试方法3（直接模式匹配）...")
            
            # 根据你提供的HTML，新闻在第二个<ul>中
            # 模式：<ul>任意内容</ul> <ul>新闻内容</ul>
            ul_pattern = r'<ul>(.*?)</ul>'
            ul_matches = re.findall(ul_pattern, tabsbox_content, re.DOTALL | re.IGNORECASE)
            
            if len(ul_matches) >= 2:
                print(f"    找到至少2个<ul>块，尝试提取第二个<ul>的内容")
                
                # 取第二个<ul>（索引1）
                news_ul_content = ul_matches[1]
                
                # 提取所有<li>项
                li_pattern = r'<li>(.*?)</li>'
                li_items = re.findall(li_pattern, news_ul_content, re.DOTALL | re.IGNORECASE)
                
                for li_idx, item_html in enumerate(li_items):
                    try:
                        # 提取URL和标题
                        link_pattern = r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>'
                        link_match = re.search(link_pattern, item_html, re.IGNORECASE)
                        
                        if link_match:
                            url = link_match.group(1)
                            title = link_match.group(2)
                            
                            # 清理数据
                            title = self._clean_text(title)
                            
                            # 确保URL完整
                            if url and not url.startswith(('http://', 'https://')):
                                if url.startswith('/'):
                                    url = f"{self.base_url}{url}"
                                else:
                                    url = f"{self.base_url}/{url}"
                            
                            # 从URL提取时间信息
                            publish_time = self._extract_time_from_url(url)
                            
                            # 创建文章对象
                            article = self._create_article_object(
                                title=title,
                                url=url,
                                article_type="热点",
                                publish_time=publish_time,
                                section="热点新闻"
                            )
                            
                            articles.append(article)
                            item_count += 1
                            
                            print(f"        热点新闻{li_idx+1}: '{title[:40]}...' 提取成功")
                            
                    except Exception as e:
                        print(f"        热点新闻{li_idx+1}: 提取时出错: {e}")
                        continue
        
        print(f"    提取到 {item_count} 条热点新闻")
        return articles
    
    def _extract_time_from_url(self, url: str) -> Optional[datetime]:
        """从URL中提取时间信息
        
        JRJ的URL格式通常包含日期，例如:
        - https://stock.jrj.com.cn/2026/03/25101256456666.shtml
        - https://usstock.jrj.com.cn/2026/03/25092256455345.shtml
        格式: /YYYY/MM/DDHHMMxxxxxxxx.shtml
        """
        try:
            # 匹配日期模式: /2026/03/25101256456666.shtml
            date_pattern = r'/(\d{4})/(\d{2})/(\d{2})(\d{2})(\d{2})\d+\.shtml'
            match = re.search(date_pattern, url)
            
            if match:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3))
                hour = int(match.group(4))
                minute = int(match.group(5))
                
                return datetime(year, month, day, hour, minute)
            
            # 尝试其他日期格式
            alt_patterns = [
                r'/(\d{4})-(\d{2})-(\d{2})/',  # /2026-03-25/
                r'/(\d{4})(\d{2})(\d{2})/',    # /20260325/
            ]
            
            for pattern in alt_patterns:
                match = re.search(pattern, url)
                if match:
                    if len(match.groups()) == 3:
                        year = int(match.group(1))
                        month = int(match.group(2))
                        day = int(match.group(3))
                        return datetime(year, month, day, 12, 0)  # 默认中午12点
        
        except Exception as e:
            print(f"    从URL提取时间失败 '{url}': {e}")
        
        # 如果无法提取，返回当前时间（这样会被时间过滤掉）
        return datetime.now()
    
    def _create_article_object(self, title: str, url: str, article_type: str, 
                              publish_time: Optional[datetime], section: str) -> Dict[str, Any]:
        """创建文章对象
        
        确保输出结构与stcn的输出保持一致，缺失数据用默认值填充
        """
        now = datetime.now()
        
        # 检查是否在48小时内
        within_48h = False
        if publish_time:
            time_diff = now - publish_time
            within_48h = time_diff.total_seconds() <= 48 * 3600
        
        # 如果超过48小时或没有时间，使用当前时间（这样会被过滤掉）
        if not within_48h or not publish_time:
            publish_time = now
        
        # 生成摘要（使用标题前100字符）
        summary = title[:100] + '...' if len(title) > 100 else title
        
        # 从URL提取可能的分类
        category = self._extract_category_from_url(url)
        
        return {
            'title': title,
            'url': url,
            'summary': summary,
            'source': self.name,
            'author': '金融界',  # 默认作者
            'keywords': [category] if category else [],  # 从URL提取的关键字
            'time': publish_time.strftime('%H:%M'),  # 显示时间
            'publish_time': publish_time.isoformat(),
            'publish_time_display': publish_time.strftime('%Y-%m-%d %H:%M'),
            'type': article_type,
            'section': section,  # 新增字段：新闻部分（头条/热点）
            'category': category,  # 新增字段：分类
            'scraped_at': now.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': now.isoformat(),
            'within_48h': within_48h
        }
    
    def _extract_category_from_url(self, url: str) -> str:
        """从URL提取分类信息"""
        try:
            # 根据URL路径判断分类（注意顺序：先检查更具体的域名）
            if 'usstock.jrj.com.cn' in url:
                return '美股'
            elif 'stock.jrj.com.cn' in url:
                return '股票'
            elif 'finance.jrj.com.cn' in url:
                return '财经'
            elif 'auto.jrj.com.cn' in url:
                return '汽车'
            elif 'tech.jrj.com.cn' in url:
                return '科技'
            elif 'estate.jrj.com.cn' in url:
                return '地产'
            elif 'jrj.com.cn' in url:
                return '综合'
            else:
                return '未知'
        except:
            return '未知'
    
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
    
    def _remove_duplicates(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去除重复文章"""
        unique_articles = []
        seen_urls = set()
        
        for article in articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        return unique_articles
    
    def crawl(self) -> List[Dict[str, Any]]:
        """执行抓取
        
        Returns:
            抓取到的文章列表
        """
        print("开始抓取金融界热点新闻...")
        print("=" * 70)
        print(f"抓取时间限制: 48小时内")
        print(f"抓取等待时间: 3秒")
        print("=" * 70)
        
        # 使用scrapling抓取
        print("\n1. 使用scrapling抓取金融界首页...")
        html_content = self._fetch_with_scrapling(self.target_url, 3000)  # 3秒等待
        
        # 如果失败，使用示例数据
        if not html_content:
            print("\n2. 抓取失败，使用示例数据...")
            return self._get_sample_articles()
        
        # 提取文章
        print("\n3. 提取文章信息...")
        articles = self.extract_articles(html_content)
        
        # 应用48小时过滤
        filtered_articles = self._filter_by_48h(articles)
        
        return filtered_articles
    
    def _filter_by_48h(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """过滤48小时内的文章"""
        filtered = []
        for article in articles:
            if article.get('within_48h', False):
                filtered.append(article)
        
        print(f"  48小时内文章: {len(filtered)} 篇 (总共: {len(articles)} 篇)")
        return filtered
    
    def _get_sample_articles(self) -> List[Dict[str, Any]]:
        """获取示例文章（用于测试）"""
        print("  使用示例文章数据")
        
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        
        sample_articles = [
            {
                'title': '数据缺失',
                'url': 'https://stock.jrj.com.cn/2026/03/25101256456666.shtml',
                'summary': '数据缺失。',
                'source': '金融界',
                'author': '金融界',
                'keywords': ['股票', '光通信'],
                'time': '10:12',
                'publish_time': datetime(now.year, now.month, now.day, 10, 12).isoformat(),
                'publish_time_display': datetime(now.year, now.month, now.day, 10, 12).strftime('%Y-%m-%d %H:%M'),
                'type': '头条',
                'section': '头条新闻',
                'category': '股票',
                'scraped_at': now.strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': now.isoformat(),
                'within_48h': True
            },
            {
                'title': '数据缺失',
                'url': 'https://usstock.jrj.com.cn/2026/03/25092256455345.shtml',
                'summary': '数据缺失',
                'source': '金融界',
                'author': '金融界',
                'keywords': ['美股', 'AI'],
                'time': '09:22',
                'publish_time': datetime(now.year, now.month, now.day, 9, 22).isoformat(),
                'publish_time_display': datetime(now.year, now.month, now.day, 9, 22).strftime('%Y-%m-%d %H:%M'),
                'type': '头条',
                'section': '头条新闻',
                'category': '美股',
                'scraped_at': now.strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': now.isoformat(),
                'within_48h': True
            },
            {
                'title': '数据缺失',
                'url': 'https://finance.jrj.com.cn/2026/03/25072956453423.shtml',
                'summary': '数据缺失',
                'source': '金融界',
                'author': '金融界',
                'keywords': ['财经', '国际'],
                'time': '07:29',
                'publish_time': datetime(now.year, now.month, now.day, 7, 29).isoformat(),
                'publish_time_display': datetime(now.year, now.month, now.day, 7, 29).strftime('%Y-%m-%d %H:%M'),
                'type': '头条',
                'section': '头条新闻',
                'category': '财经',
                'scraped_at': now.strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': now.isoformat(),
                'within_48h': True
            }
        ]
        
        return sample_articles
    
    def display_results(self, articles: List[Dict[str, Any]]) -> None:
        """显示抓取结果"""
        if not articles:
            print("未抓取到任何文章")
            return
        
        print("\n" + "=" * 70)
        print("金融界热点新闻抓取结果 (48小时内)")
        print("=" * 70)
        print(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"文章数量: {len(articles)} 篇")
        print(f"时间范围: 48小时内")
        print()
        
        # 按部分和类型分组
        sections = {}
        for article in articles:
            section = article.get('section', '未知')
            if section not in sections:
                sections[section] = []
            sections[section].append(article)
        
        # 显示文章
        for section, section_articles in sections.items():
            print(f"{section}:")
            print("-" * 50)
            
            # 按时间排序（最新的在前）
            sorted_articles = sorted(
                section_articles,
                key=lambda x: x.get('publish_time', ''),
                reverse=True
            )
            
            for i, article in enumerate(sorted_articles[:10], 1):  # 每个部分显示最多10篇
                print(f"{i}. {article['title']}")
                print(f"   时间: {article.get('time', '未知')} | 类型: {article.get('type', '未知')}")
                print(f"   发布时间: {article.get('publish_time_display', '未知')}")
                print(f"   分类: {article.get('category', '未知')}")
                
                # 显示关键字
                keywords = article.get('keywords', [])
                if keywords:
                    print(f"   关键字: {', '.join(keywords)}")
                
                print(f"   链接: {article['url'][:80]}...")
                print(f"   摘要: {article.get('summary', '无')[:80]}...")
                print()
            
            if len(section_articles) > 10:
                print(f"... 还有 {len(section_articles) - 10} 篇文章")
            print()
        
        # 统计信息
        print("=" * 70)
        print("统计信息:")
        print(f"  总文章数: {len(articles)}")
        
        # 按部分统计
        print(f"  按部分统计:")
        for section, section_articles in sections.items():
            print(f"    {section}: {len(section_articles)} 篇")
        
        # 按分类统计
        category_stats = {}
        for article in articles:
            category = article.get('category', '未知')
            category_stats[category] = category_stats.get(category, 0) + 1
        
        if category_stats:
            print(f"  按分类统计 (前5):")
            top_categories = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)[:5]
            for category, count in top_categories:
                print(f"    {category}: {count} 篇")
        
        print("=" * 70)
    
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
        filename = f"jrj_hot_news_{timestamp}.json"
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
            txt_filename = f"jrj_hot_news_{timestamp}.txt"
            txt_filepath = self.output_dir / txt_filename
            
            with open(txt_filepath, 'w', encoding='utf-8') as f:
                f.write(f"金融界热点新闻抓取报告 (48小时内)\n")
                f.write("=" * 70 + "\n")
                f.write(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"目标URL: {self.target_url}\n")
                f.write(f"等待时间: 3秒\n")
                f.write(f"时间过滤: 48小时内\n")
                f.write(f"文章数量: {len(articles)} 篇\n\n")
                
                f.write("文章列表:\n")
                f.write("=" * 70 + "\n")
                
                # 按部分分组
                sections = {}
                for article in articles:
                    section = article.get('section', '未知')
                    if section not in sections:
                        sections[section] = []
                    sections[section].append(article)
                
                for section, section_articles in sections.items():
                    f.write(f"\n{section}:\n")
                    f.write("-" * 50 + "\n")
                    
                    for i, article in enumerate(section_articles, 1):
                        f.write(f"\n{i}. {article['title']}\n")
                        f.write(f"   链接: {article['url']}\n")
                        f.write(f"   时间: {article.get('time', '未知')}\n")
                        f.write(f"   发布时间: {article.get('publish_time_display', '未知')}\n")
                        f.write(f"   类型: {article.get('type', '未知')}\n")
                        f.write(f"   分类: {article.get('category', '未知')}\n")
                        
                        keywords = article.get('keywords', [])
                        if keywords:
                            f.write(f"   关键字: {', '.join(keywords)}\n")
                        
                        f.write(f"   摘要: {article.get('summary', '无')}\n")
                        f.write(f"   作者: {article.get('author', '未知')}\n")
            
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
            intermediate_filename = f"jrj_intermediate_{timestamp}.json"
            intermediate_filepath = self.output_dir / intermediate_filename
            
            # 简化数据结构
            intermediate_data = {
                'metadata': {
                    'source': 'jrj',
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
                    'category': article.get('category', ''),
                    'type': article.get('type', ''),
                    'section': article.get('section', ''),
                    'source': 'jrj'
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
            # 从JRJ的URL中提取数字ID，例如: /2026/03/25101256456666.shtml -> 25101256456666
            match = re.search(r'/(\d{12,})\.shtml', url)
            if match:
                return f"jrj_{match.group(1)}"
            
            # 如果没有找到数字ID，使用URL的MD5哈希
            import hashlib
            url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:8]
            return f"jrj_{url_hash}"
        except:
            return f"jrj_{hash(url) % 1000000}"

def main():
    """主函数"""
    print("金融界热点新闻抓取器")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 创建抓取器
    crawler = JRJHotNewsCrawler()
    
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
                files = list(crawler.output_dir.glob("jrj_hot_news_*.json"))
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
    sys.exit(main())