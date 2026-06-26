#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 3: 华尔街见闻快讯采集模块

功能：
1. 从华尔街见闻重要快讯页面采集实时快讯
2. 使用滚动抓取技术获取更多内容
3. 过滤财经相关重要快讯
4. 保存为JSON格式

移植自: /skills/qhot-news/scripts/scroll_crawler_final.py
"""

import os
import sys
import json
import re
import subprocess
import tempfile
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

# 导入scrapling工具模块
try:
    from scrapling_util import fetch_wheel, ScraplingUtil
    SCRAPLING_UTIL_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] 无法导入scrapling_util: {e}")
    SCRAPLING_UTIL_AVAILABLE = False

# 导入playwright（可选）
try:
    import asyncio
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError as e:
    PLAYWRIGHT_AVAILABLE = False


class WallStreetCrawler:
    """华尔街见闻快讯采集器"""
    
    def __init__(self, cookie_path: str = None):
        """初始化采集器
        
        Args:
            cookie_path: QQ浏览器User Data目录路径，用于加载登录cookie
        """
        self.name = "华尔街见闻快讯采集器"
        
        # 初始化logger
        self.logger = logging.getLogger('wallstreet_crawler')
        
        # 加载完整配置
        full_config = self.load_config()
        
        # 提取华尔街见闻模块配置和系统设置
        self.wallstreet_config = full_config.get('wallstreetcn_module', {})
        self.system_settings = full_config.get('system_settings', {})
        
        # 从华尔街见闻配置获取参数
        self.base_url = self.wallstreet_config.get('base_url', 'https://wallstreetcn.com/live/global')
        
        # 输出目录 - 优先使用wallstreetcn_module中的配置，否则从system_settings构建
        output_dir_str = self.wallstreet_config.get('output_directory')
        if not output_dir_str:
            # 从系统设置构建默认路径
            temp_dir = self.system_settings.get('temp_dir', 'c:/SelfData/claw_temp/temp')
            output_dir_str = str(Path(temp_dir) / "wallstreetcn_news")
            print(f"[INFO] 使用系统temp_dir构建输出目录: {output_dir_str}")
        
        self.output_dir = Path(output_dir_str)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 从配置获取关键词
        filter_config = self.wallstreet_config.get('filter_keywords', {})
        self.finance_keywords = filter_config.get('finance', [
            '原油', '石油', '天然气', '煤炭', '黄金', '白银', '铜', '铝', '铁矿石',
            'GDP', 'CPI', 'PPI', 'PMI', '通胀', '通缩', '利率', '汇率', '货币政策',
            '股市', 'A股', '港股', '美股', '指数', '上证', '深证', '创业板', '科创板',
            '美国', '欧洲', '日本', '中国', '俄罗斯', '伊朗', '以色列', '制裁', '贸易战',
            '财报', '业绩', '上市', '退市', '并购', '重组', '特斯拉', '苹果', '微软',
            '政策', '监管', '法规', '改革', '开放', '试点', '自贸区',
            'AI', '人工智能', '芯片', '半导体', '5G', '新能源', '电动车', '自动驾驶',
            '战争', '冲突', '导弹', '战机', '军事', '攻击', '核', '军演'
        ])
        
        self.important_keywords = filter_config.get('important', [
            '重要', '紧急', '突发', '重磅', '重大', '关键', '突破', '首次',
            '伊朗', '以色列', '战争', '冲突', '导弹', '核', '制裁', '禁令'
        ])
        
        # 抓取设置
        self.crawl_settings = self.wallstreet_config.get('crawl_settings', {})
        
        # Cookie设置
        # 优先级：配置文件 > 传入参数 > 默认路径 > 无cookie
        config_cookie_path = self.wallstreet_config.get('cookie_path')
        
        # 检查配置文件中的cookie_path是否有效（不是占位符且非空）
        if config_cookie_path and config_cookie_path.strip() and config_cookie_path != "你的cookie地址":
            self.cookie_path = config_cookie_path.strip()
            print(f"[INFO] 使用配置文件中的Cookie路径: {self.cookie_path}")
        elif cookie_path:
            # 使用传入的参数
            self.cookie_path = cookie_path
            print(f"[INFO] 使用传入的Cookie路径: {self.cookie_path}")
        else:
            # 尝试默认QQ浏览器User Data目录
            default_cookie_path = "C:/Users/13620/AppData/Local/Tencent/QQBrowser/User Data"
            if Path(default_cookie_path).exists():
                self.cookie_path = default_cookie_path
                print(f"[INFO] 使用默认QQ浏览器User Data目录: {self.cookie_path}")
            else:
                self.cookie_path = None
                print(f"[WARNING] 默认QQ浏览器目录不存在: {default_cookie_path}")
                print(f"[WARNING] 将以无cookie模式运行，可能导致访问受限")
        
        # 检查cookie路径是否存在（如果已设置）
        if self.cookie_path:
            if Path(self.cookie_path).exists():
                print(f"[INFO] Cookie路径验证成功: {self.cookie_path}")
            else:
                print(f"[WARNING] Cookie路径不存在: {self.cookie_path}")
                print(f"[WARNING] 将以无cookie模式运行，可能导致访问受限")
                self.cookie_path = None
        
        print(f"{self.name} 初始化完成")
        print(f"目标URL: {self.base_url}")
        print(f"输出目录: {self.output_dir}")
        if self.cookie_path:
            print(f"Cookie路径: {self.cookie_path} (已启用)")
        else:
            print(f"Cookie路径: 无 (无cookie模式)")
        print(f"财经关键词: {len(self.finance_keywords)} 个")
        print(f"重要关键词: {len(self.important_keywords)} 个")
        print(f"配置加载: {'成功' if self.wallstreet_config else '失败，使用默认值'}")
        print("-" * 70)
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            config_path = Path(__file__).parent / "url_config.json"
            if not config_path.exists():
                print(f"[WARNING] 配置文件不存在: {config_path}")
                return {}
            
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"[INFO] 配置文件加载成功")
            return config
            
        except Exception as e:
            print(f"[WARNING] 配置文件加载失败: {e}")
            return {}



    def parse_wallstreet_important_news(self, html_content: str) -> List[Dict]:
        """解析华尔街见闻重要快讯HTML"""
        try:
            import re

            articles = []

            # 查找所有live-item
            pattern = r'<div[^>]*class="live-item"[^>]*>.*?</div>\s*</div>'
            matches = re.findall(pattern, html_content, re.DOTALL)

            if not matches:
                return []

            self.logger.info(f"找到 {len(matches)} 个快讯项目")

            for match in matches:
                try:
                    # 提取时间
                    time_match = re.search(r'<time[^>]*class="live-item_created[^"]*"[^>]*>(.*?)</time>', match)
                    time_text = time_match.group(1).strip() if time_match else ''

                    # 提取标题
                    title_match = re.search(r'<div[^>]*class="live-item_title"[^>]*>(.*?)</div>', match)
                    title = title_match.group(1).strip() if title_match else ''

                    # 提取内容
                    content_match = re.search(r'<div[^>]*class="live-item_html"[^>]*>(.*?)</div>', match, re.DOTALL)
                    content_html = content_match.group(1).strip() if content_match else ''

                    # 清理HTML标签
                    content = re.sub(r'<[^>]+>', '', content_html).strip()

                    # 判断是否重要快讯（点击复选框后应该都是重要的）
                    is_important = 'importance' in match or True  # 假设都是重要的

                    articles.append({
                        'title': title[:100] if len(title) > 100 else title,
                        'content': content[:500],  # 限制内容长度，与parse_articles_with_regex保持一致
                        'summary': content[:150] + "..." if len(content) > 150 else content,
                        'source': '华尔街见闻重要快讯',
                        'url': 'https://wallstreetcn.com/live',
                        'timestamp': time_text,
                        'importance': is_important,  # 统一使用'importance'键名
                        'important': is_important,   # 保留向后兼容
                        'full_content': content,
                        'extracted_time': datetime.now().isoformat()
                    })

                except Exception as e:
                    self.logger.warning(f"解析快讯失败: {e}")
                    continue

            # 按时间排序（最新的在前）
            articles.sort(key=lambda x: x['timestamp'], reverse=True)

            # 返回所有重要快讯
            return articles

        except Exception as e:
            self.logger.error(f"解析重要快讯失败: {e}")
            return []

    def fetch_with_scrapling(self, url: str, wait_time: int = None, scroll_times: int = None) -> Optional[str]:
        """使用scrapling获取网页内容（支持滚动）
        
        Args:
            url: 目标URL
            wait_time: 等待时间（毫秒），如果为None则从配置读取
            scroll_times: 滚动次数，默认为1（不滚动），如果为None则从配置读取
        """
        # 如果未提供参数，从配置读取默认值
        if wait_time is None:
            scroll_config = self.crawl_settings.get('scroll', {})
            wait_time = scroll_config.get('wait_time', 5000)
        
        if scroll_times is None:
            scroll_config = self.crawl_settings.get('scroll', {})
            scroll_times = scroll_config.get('scroll_times', 1)
        
        # 获取超时配置（使用playwright配置或默认值）
        playwright_config = self.crawl_settings.get('playwright', {})
        timeout_ms = playwright_config.get('timeout_ms', 15000)
        try:
            print(f"  获取: {url}")
            print(f"  等待时间: {wait_time}ms, 滚动次数: {scroll_times}")
            
            html_content = None
            
            # 尝试使用scrapling_util.fetch_wheel
            if SCRAPLING_UTIL_AVAILABLE:
                try:
                    # 根据滚动次数决定使用fetch还是fetch_wheel
                    if scroll_times <= 1:
                        # 使用fetch（无滚动）
                        from scrapling_util import fetch
                        html_content = fetch(url, wait=wait_time, timeout=timeout_ms)
                    else:
                        # 使用fetch_wheel，从配置获取滚动延迟
                        scroll_config = self.crawl_settings.get('scroll', {})
                        scroll_delay = scroll_config.get('scroll_delay', 5.0)
                        html_content = fetch_wheel(url, scroll_times=scroll_times, 
                                                  scroll_delay=scroll_delay, 
                                                  wait=wait_time, timeout=timeout_ms)
                    
                    if html_content:
                        print(f"  获取成功，长度: {len(html_content)} 字符")
                        return html_content
                    else:
                        print(f"  [WARNING] scrapling_util返回空内容")
                except Exception as e:
                    print(f"  [WARNING] scrapling_util异常: {e}")
                    html_content = None
            
            # 如果scrapling_util不可用或失败，使用命令行版本
            if not html_content:
                print(f"  [INFO] 使用scrapling命令行版本...")
                
                # 创建临时文件
                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
                    tmp_file = tmp.name
                
                # 构建scrapling命令
                cmd = f'scrapling extract fetch "{url}" "{tmp_file}" --wait {wait_time}'
                
                # 计算超时时间（秒），使用配置的超时时间
                timeout_seconds = timeout_ms / 1000 + 5  # 增加5秒缓冲
                
                result = subprocess.run(
                    cmd, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    encoding='utf-8',
                    timeout=timeout_seconds
                )
                
                if result.returncode == 0:
                    # 读取HTML内容
                    with open(tmp_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    # 清理临时文件
                    os.unlink(tmp_file)
                    
                    if html_content:
                        print(f"  获取成功，长度: {len(html_content)} 字符")
                        return html_content
                    else:
                        print(f"  [WARNING] 获取的HTML内容为空")
                        return None
                else:
                    print(f"  [ERROR] scrapling失败，返回码: {result.returncode}")
                    if result.stderr:
                        print(f"  错误信息: {result.stderr[:200]}")
                    return None
                
        except subprocess.TimeoutExpired:
            print(f"  [ERROR] 获取超时")
            return None
        except Exception as e:
            print(f"  [ERROR] 获取异常: {e}")
            return None
    
    def parse_articles_with_regex(self, html: str) -> List[Dict[str, Any]]:
        """使用正则表达式解析快讯（基于playwright_scroll_crawler.py）"""
        if not html:
            return []
        
        articles = []
        
        print(f"  使用正则表达式解析HTML，长度: {len(html)} 字符")
        
        try:
            # 查找所有live-item元素
            pattern = r'<div[^>]*class="live-item"[^>]*>.*?</div>\s*</div>'
            matches = re.findall(pattern, html, re.DOTALL)
            
            if not matches:
                print(f"  未找到live-item元素")
                return []
            
            print(f"  找到 {len(matches)} 个live-item元素")
            
            important_count = 0
            
            for match in matches:
                try:
                    # 检查是否是重要快讯
                    if 'importance' not in match:
                        continue
                    
                    # 提取时间
                    time_match = re.search(r'<time[^>]*class="live-item_created[^"]*"[^>]*>(.*?)</time>', match)
                    time_text = time_match.group(1).strip() if time_match else ''
                    
                    # 提取标题
                    title_match = re.search(r'<div[^>]*class="live-item_title"[^>]*>(.*?)</div>', match)
                    title = title_match.group(1).strip() if title_match else ''
                    
                    # 提取内容
                    content_match = re.search(r'<div[^>]*class="live-item_html"[^>]*>(.*?)</div>', match, re.DOTALL)
                    content_html = content_match.group(1).strip() if content_match else ''
                    
                    # 清理HTML标签
                    content = re.sub(r'<[^>]+>', '', content_html).strip()
                    
                    # 检查是否包含财经关键词
                    has_finance = any(keyword in title or keyword in content for keyword in self.finance_keywords)
                    
                    # 检查是否重要快讯（基于关键词）
                    is_important = any(keyword in title or keyword in content for keyword in self.important_keywords)
                    
                    if not has_finance:
                        continue
                    
                    articles.append({
                        'timestamp': time_text,
                        'title': title[:100] if len(title) > 100 else title,
                        'content': content[:500],  # 限制内容长度
                        'summary': content[:150] + "..." if len(content) > 150 else content,
                        'source': '华尔街见闻重要快讯',
                        'url': 'https://wallstreetcn.com/live',
                        'importance': is_important,
                        'has_finance': has_finance,
                        'important': True,  # 表示从importance类提取
                        'full_content': content,
                        'extracted_time': datetime.now().isoformat()
                    })
                    
                    important_count += 1
                    
                    if is_important and important_count <= 5:
                        print(f"   发现重要快讯: [{time_text}] {title[:50]}...")
                        
                except Exception as e:
                    print(f"   解析live-item失败: {e}")
                    continue
            
            print(f"  解析到 {important_count} 条重要快讯")
            
            if important_count == 0 and len(matches) > 0:
                print(f"  警告: 找到{len(matches)}个live-item但未找到importance标记")
            
            return articles
            
        except Exception as e:
            print(f"  正则表达式解析失败: {e}")
            return []

    
    def remove_duplicates(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去除重复的快讯"""
        if not articles:
            return []
        
        unique_articles = []
        seen_keys = set()
        
        for article in articles:
            # 使用时间戳和标题前30字符作为唯一键
            key = f"{article['timestamp']}_{article['title'][:30]}"
            
            if key not in seen_keys:
                seen_keys.add(key)
                unique_articles.append(article)
            else:
                print(f"   去重: 跳过重复快讯 [{article['timestamp']}] {article['title'][:30]}...")
        
        print(f"  去重后: {len(unique_articles)} 条快讯")
        return unique_articles
    
    def sort_articles_by_time(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """按时间排序（最新的在前）"""
        def parse_time(timestamp_str):
            try:
                if ':' in timestamp_str:
                    hour, minute = map(int, timestamp_str.split(':'))
                    return hour * 60 + minute
                return 0
            except:
                return 0
        
        sorted_articles = sorted(
            articles, 
            key=lambda x: parse_time(x['timestamp']), 
            reverse=True
        )
        
        return sorted_articles
    
    def filter_important_articles(self, articles: List[Dict[str, Any]], max_count: int = 20) -> List[Dict[str, Any]]:
        """过滤重要快讯"""
        important_articles = [a for a in articles if a.get('importance', False)]
        
        if important_articles:
            print(f"  重要快讯: {len(important_articles)} 条")
            return important_articles[:max_count]
        else:
            print(f"  无重要快讯，返回所有快讯")
            return articles[:max_count]
    
    def save_results(self, articles: List[Dict[str, Any]], crawl_type: str = "single"):
        """保存抓取结果"""
        if not articles:
            print("[WARNING] 无快讯可保存")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. 保存为JSON
        json_file = self.output_dir / f'wallstreetcn_{crawl_type}_{timestamp}.json'
        
        output_data = {
            'metadata': {
                'module': self.name,
                'crawl_time': datetime.now().isoformat(),
                'url': self.base_url,
                'article_count': len(articles),
                'important_count': sum(1 for a in articles if a.get('importance', False))
            },
            'articles': articles
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        # 2. 保存为文本报告
        txt_file = self.output_dir / f'wallstreetcn_{crawl_type}_{timestamp}.txt'
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"华尔街见闻快讯采集报告\n")
            f.write(f"采集时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"URL: {self.base_url}\n")
            f.write(f"快讯数量: {len(articles)} 条\n")
            f.write(f"重要快讯: {sum(1 for a in articles if a.get('importance', False))} 条\n")
            f.write("=" * 70 + "\n\n")
            
            for i, article in enumerate(articles, 1):
                importance = "[重要] " if article.get('importance', False) else ""
                f.write(f"{i}. [{article['timestamp']}] {importance}{article['title']}\n")
                
                # 获取内容，优先使用'content'，其次使用'full_content'，最后使用'summary'
                content = article.get('content') 
                if not content:
                    content = article.get('full_content', '')
                if not content:
                    content = article.get('summary', '')
                    
                f.write(f"   内容: {content[:100]}...\n")
                f.write(f"   来源: {article.get('source', '华尔街见闻')}\n")
                f.write(f"   提取时间: {article.get('extracted_time', '未知')}\n")
                f.write("\n")
        
        print(f"\n结果已保存:")
        print(f"  JSON文件: {json_file}")
        print(f"  文本报告: {txt_file}")
        
        return json_file, txt_file
    
    async def crawl_with_playwright_async(self, url: str = None) -> List[Dict[str, Any]]:
        """使用Playwright异步抓取重要快讯（优化版）
        
        核心逻辑：
        1. 打开华尔街见闻快讯页面 (https://wallstreetcn.com/live/global)
        2. 点击"只看重要的"选择框
        3. 获取页面HTML并解析快讯
        4. 如果快讯不足10条，滚动一次滚轮，等待5秒，再次抓取
        5. 返回解析到的快讯
        """
        if not PLAYWRIGHT_AVAILABLE:
            print("[ERROR] Playwright不可用，请安装: pip install playwright")
            return []
        
        # 使用默认URL或传入的URL
        target_url = url or self.base_url
        
        # 从配置获取参数
        playwright_config = self.crawl_settings.get('playwright', {})
        timeout_ms = playwright_config.get('timeout_ms', 30000)  # 增加超时时间
        
        print(f"\n{'='*70}")
        print(f"开始Playwright抓取")
        print(f"{'='*70}")
        print(f"目标URL: {target_url}")
        print(f"超时设置: {timeout_ms} 毫秒")
        
        start_time = time.time()
        
        try:
            async with async_playwright() as p:
                # 启动浏览器（如果cookie_path存在，则使用用户数据目录）
                if self.cookie_path:
                    print(f"[INFO] 使用User Data目录启动浏览器: {self.cookie_path}")
                    # 使用persistent context以保持登录状态
                    context = await p.chromium.launch_persistent_context(
                        user_data_dir=self.cookie_path,
                        headless=True,
                        viewport={'width': 1200, 'height': 800}
                    )
                    browser = context.browser
                    page = context.pages[0] if context.pages else await context.new_page()
                else:
                    print("[INFO] 以无cookie模式启动浏览器")
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        viewport={'width': 1200, 'height': 800}
                    )
                    page = await context.new_page()
                
                try:
                    # 访问页面
                    print("\n1. 访问页面...")
                    await page.goto(target_url, timeout=timeout_ms)
                    
                    # 等待页面加载
                    await page.wait_for_load_state('networkidle')
                    print("  页面加载完成")
                    
                    # 等待并点击"只看重要的"复选框
                    print("\n2. 点击'只看重要的'复选框...")
                    try:
                        # 等待复选框出现
                        await page.wait_for_selector('#importance', timeout=10000)
                        print("  找到复选框")
                        
                        # 点击复选框
                        await page.click('#importance')
                        print("  已点击复选框")
                        
                        # 等待重要快讯加载
                        await page.wait_for_timeout(3000)
                        print("  重要快讯加载完成")
                    except Exception as e:
                        print(f"  点击复选框失败: {e}")
                        # 继续执行，可能页面已经显示了重要快讯
                    
                    # 初始获取页面内容
                    print("\n3. 获取页面内容...")
                    html_content = await page.content()
                    
                    # 解析快讯
                    articles = []
                    if html_content and len(html_content) > 1000:
                        articles = self.parse_wallstreet_important_news(html_content)
                        if not articles:
                            # 尝试后备解析方法
                            articles = self.parse_articles_with_regex(html_content)
                    
                    print(f"  初始解析到 {len(articles)} 条快讯")
                    
                    # 第四步：滚动逻辑 - 如果快讯不足10条，滚动一次滚轮，等待5秒，再次抓取
                    if len(articles) < 10:
                        print(f"\n4. 快讯不足10条（当前{len(articles)}条），执行滚动加载...")
                        
                        # 滚动一次滚轮
                        print("  滚动页面到底部...")
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        
                        # 等待5秒让新内容加载
                        print("  等待5秒让新内容加载...")
                        await page.wait_for_timeout(5000)
                        
                        # 再次获取页面内容
                        print("  重新获取页面内容...")
                        html_content = await page.content()
                        
                        # 再次解析快讯
                        if html_content and len(html_content) > 1000:
                            new_articles = self.parse_wallstreet_important_news(html_content)
                            if not new_articles:
                                new_articles = self.parse_articles_with_regex(html_content)
                            
                            if new_articles:
                                # 合并文章，去重
                                all_articles = articles + new_articles
                                unique_articles = self.remove_duplicates(all_articles)
                                articles = unique_articles
                                print(f"  滚动后新增 {len(new_articles)} 条快讯，总计 {len(articles)} 条快讯")
                            else:
                                print("  滚动后未解析到新快讯")
                        else:
                            print("  滚动后获取的页面内容无效")
                    
                    # 截图保存（可选）
                    try:
                        screenshot_dir = self.output_dir / "screenshots"
                        screenshot_dir.mkdir(exist_ok=True)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        screenshot_path = screenshot_dir / f'wallstreet_playwright_{timestamp}.png'
                        await page.screenshot(path=str(screenshot_path), full_page=True)
                        print(f"\n截图已保存: {screenshot_path}")
                    except Exception as e:
                        print(f"\n截图失败: {e}")
                    
                    elapsed_time = time.time() - start_time
                    
                    print(f"\n{'='*70}")
                    print(f"Playwright抓取完成!")
                    print(f"{'='*70}")
                    print(f"统计:")
                    print(f"  抓取方式: Playwright (点击复选框+滚动)")
                    print(f"  最终快讯: {len(articles)} 条")
                    print(f"  耗时: {elapsed_time:.2f} 秒")
                    print(f"{'='*70}")
                    
                    # 显示前10条快讯
                    if articles:
                        print(f"\n前10条快讯:")
                        for i, article in enumerate(articles[:10], 1):
                            importance = "[重要] " if article.get('importance', False) else ""
                            print(f"{i}. [{article['timestamp']}] {importance}{article['title'][:50]}...")
                    
                    return articles
                    
                finally:
                    # 关闭浏览器/context
                    if self.cookie_path:
                        # 使用persistent context的情况，关闭context
                        await context.close()
                    else:
                        # 普通模式，关闭browser
                        await browser.close()
                        
        except Exception as e:
            print(f"\n[ERROR] Playwright抓取失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 尝试使用scrapling作为后备方式
            print("\n[INFO] 尝试使用scrapling作为后备方式爬取...")
            try:
                scrapling_available = globals().get('SCRAPLING_UTIL_AVAILABLE', False)
                if scrapling_available and hasattr(self, 'fetch_with_scrapling'):
                    html_content = self.fetch_with_scrapling(target_url, wait_time=3000)
                    if html_content and len(html_content) > 1000:
                        print(f"  scrapling成功获取HTML，长度: {len(html_content)} 字符")
                        articles = self.parse_wallstreet_important_news(html_content)
                        if not articles:
                            articles = self.parse_articles_with_regex(html_content)
                        
                        if articles:
                            print(f"  scrapling解析到 {len(articles)} 条快讯")
                            # 去重和排序
                            articles = self.remove_duplicates(articles)
                            articles = self.sort_articles_by_time(articles)
                            return articles
                        else:
                            print("  scrapling解析失败，未找到快讯")
                    else:
                        print("  scrapling爬取失败，页面内容无效")
                else:
                    print("  scrapling不可用，跳过后备方式")
            except Exception as scrapling_error:
                print(f"  scrapling后备方式也失败: {scrapling_error}")
            
            return []
    
    def score_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """对文章进行打分和排序（简化版）"""
        if not articles:
            return []
        
        scored_articles = []
        for article in articles:
            score = 0
            
            # 基础分
            score += 10
            
            # 关键词加分
            important_keywords = [
                '美国', '伊朗', '核', '战争', '冲突', '制裁', '紧急', '突发',
                '重大', '重磅', '首次', '突破', '危机', '警报', '警告'
            ]
            
            title = article.get('title', '').lower()
            content = article.get('content', '').lower()
            
            for keyword in important_keywords:
                if keyword in title or keyword in content:
                    score += 5
            
            # 时间加分（最近的时间）
            time_text = article.get('timestamp', '')
            if time_text:
                try:
                    if ':' in time_text:
                        hour, minute = map(int, time_text.split(':'))
                        current_hour = datetime.now().hour
                        if current_hour == hour or (current_hour - hour) <= 1:
                            score += 3
                except:
                    pass
            
            article['score'] = score
            scored_articles.append(article)
        
        # 按分数降序排序
        scored_articles.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return scored_articles
    
    def crawl_with_playwright(self) -> List[Dict[str, Any]]:
        """使用Playwright抓取（同步接口）"""
        if not PLAYWRIGHT_AVAILABLE:
            print("[ERROR] Playwright不可用")
            return []
        
        print(f"\n{'='*70}")
        print(f"开始Playwright抓取")
        print(f"{'='*70}")
        
        try:
            # 运行异步抓取
            articles = asyncio.run(self.crawl_with_playwright_async())
            
            if not articles:
                print("[WARNING] Playwright未抓取到快讯")
                
                # 尝试使用scrapling作为后备方式
                print("\n[INFO] 尝试使用scrapling作为后备方式爬取...")
                try:
                    scrapling_available = globals().get('SCRAPLING_UTIL_AVAILABLE', False)
                    if scrapling_available and hasattr(self, 'fetch_with_scrapling'):
                        html_content = self.fetch_with_scrapling(self.base_url, wait_time=3000)
                        if html_content and len(html_content) > 1000:
                            print(f"  scrapling成功获取HTML，长度: {len(html_content)} 字符")
                            articles = self.parse_wallstreet_important_news(html_content)
                            if not articles:
                                articles = self.parse_articles_with_regex(html_content)
                            
                            if articles:
                                print(f"  scrapling解析到 {len(articles)} 条快讯")
                                # 去重和排序
                                articles = self.remove_duplicates(articles)
                                articles = self.sort_articles_by_time(articles)
                                
                                # 保存结果
                                print("\n保存结果...")
                                self.save_results(articles, "scrapling_backup")
                                
                                print(f"\n采集完成，共获取 {len(articles)} 条快讯")
                                print(f"输出目录: {self.output_dir}")
                                return articles
                            else:
                                print("  scrapling解析失败，未找到快讯")
                        else:
                            print("  scrapling爬取失败，页面内容无效")
                    else:
                        print("  scrapling不可用，跳过后备方式")
                except Exception as scrapling_error:
                    print(f"  scrapling后备方式也失败: {scrapling_error}")
                
                return []
            
            # 保存结果
            print("\n保存结果...")
            self.save_results(articles, "playwright")
            
            print(f"\n采集完成，共获取 {len(articles)} 条快讯")
            print(f"输出目录: {self.output_dir}")
            
            return articles
            
        except Exception as e:
            print(f"\n[ERROR] Playwright抓取失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 尝试使用scrapling作为后备方式
            print("\n[INFO] 尝试使用scrapling作为后备方式爬取...")
            try:
                scrapling_available = globals().get('SCRAPLING_UTIL_AVAILABLE', False)
                if scrapling_available and hasattr(self, 'fetch_with_scrapling'):
                    html_content = self.fetch_with_scrapling(self.base_url, wait_time=3000)
                    if html_content and len(html_content) > 1000:
                        print(f"  scrapling成功获取HTML，长度: {len(html_content)} 字符")
                        articles = self.parse_wallstreet_important_news(html_content)
                        if not articles:
                            articles = self.parse_articles_with_regex(html_content)
                        
                        if articles:
                            print(f"  scrapling解析到 {len(articles)} 条快讯")
                            # 去重和排序
                            articles = self.remove_duplicates(articles)
                            articles = self.sort_articles_by_time(articles)
                            
                            # 保存结果
                            print("\n保存结果...")
                            self.save_results(articles, "scrapling_backup")
                            
                            print(f"\n采集完成，共获取 {len(articles)} 条快讯")
                            print(f"输出目录: {self.output_dir}")
                            return articles
                        else:
                            print("  scrapling解析失败，未找到快讯")
                    else:
                        print("  scrapling爬取失败，页面内容无效")
                else:
                    print("  scrapling不可用，跳过后备方式")
            except Exception as scrapling_error:
                print(f"  scrapling后备方式也失败: {scrapling_error}")
            
            return []
    
    def _is_same_article(self, article1: Dict[str, Any], article2: Dict[str, Any]) -> bool:
        """检查两个快讯是否相同"""
        return (article1['timestamp'] == article2['timestamp'] and 
                article1['title'][:30] == article2['title'][:30])
    
    def run(self, mode: str = "playwright"):
        """运行采集器（只支持playwright模式）"""
        print(f"\n{'='*70}")
        print(f"运行 {self.name}")
        print(f"{'='*70}")
        
        # 只支持playwright模式
        if mode != "playwright":
            print(f"[INFO] 只支持playwright模式，将使用playwright模式运行")
            mode = "playwright"
        
        if PLAYWRIGHT_AVAILABLE:
            return self.crawl_with_playwright()
        else:
            print("[ERROR] Playwright不可用，请安装: pip install playwright")
            print("[ERROR] 无法运行采集器")
            return []


def main():
    """主函数"""
    import argparse
    from pathlib import Path
    import json
    
    # 加载配置文件，获取默认cookie_path
    default_cookie_path = None
    try:
        config_path = Path(__file__).parent / "url_config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            wallstreet_config = config.get('wallstreetcn_module', {})
            config_cookie_path = wallstreet_config.get('cookie_path')
            # 检查是否为有效路径（不是占位符且非空）
            if config_cookie_path and config_cookie_path.strip() and config_cookie_path != "你的cookie地址":
                default_cookie_path = config_cookie_path.strip()
                print(f"[INFO] 从配置文件读取默认Cookie路径: {default_cookie_path}")
    except Exception as e:
        print(f"[WARNING] 加载配置文件失败: {e}")
    
    parser = argparse.ArgumentParser(description='华尔街见闻快讯采集器（Playwright模式）')
    parser.add_argument('--output-dir', type=str, 
                       help='指定输出目录路径')
    parser.add_argument('--cookie-path', type=str, default=default_cookie_path,
                       help='QQ浏览器User Data目录路径，用于加载登录cookie（默认从配置文件读取，如未配置则无默认值）')

    args = parser.parse_args()
    
    # 创建采集器
    crawler = WallStreetCrawler(cookie_path=args.cookie_path)
    
    # 如果指定了输出目录，则使用指定目录
    if args.output_dir:
        crawler.output_dir = Path(args.output_dir)
        crawler.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"使用指定输出目录: {args.output_dir}")
    
    # 运行采集器（只支持playwright模式）
    articles = crawler.run()
    
    if not articles:
        print("\n采集失败或无快讯")
        sys.exit(1)
    
    print(f"\n采集完成，共获取 {len(articles)} 条快讯")
    print(f"输出目录: {crawler.output_dir}")


if __name__ == "__main__":
    main()