#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财联社（CLS）热点新闻抓取器 - 简化版
"""

import os
import sys
import json
import re
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin

# 导入scrapling工具模块
try:
    from scrapling_util import fetch, fetch_wheel
    SCRAPLING_UTIL_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] 无法导入scrapling_util: {e}")
    SCRAPLING_UTIL_AVAILABLE = False


class CLSHotNewsCrawler:
    def __init__(self, output_dir: str = None):
        self.name = "财联社"
        self.base_url = "https://www.cls.cn"
        self.target_url = "https://www.cls.cn/depth?id=1000"
        
        # 设置输出目录
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # 默认路径（兼容新配置结构）
            self.output_dir = Path("c:/SelfData/claw_temp/temp/title_news_crawl")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查scrapling
        self.scrapling_available = self._check_scrapling()
        print(f"财联社抓取器初始化完成")
        print(f"目标: {self.target_url}")
        print(f"输出目录: {self.output_dir}")
        print(f"Scrapling: {'可用' if self.scrapling_available else '不可用'}")
        print("-" * 70)
    
    def _check_scrapling(self):
        """检查scrapling是否可用（包括scrapling_util）"""
        # 首先检查scrapling_util是否可用
        if SCRAPLING_UTIL_AVAILABLE:
            return True
        
        # 如果scrapling_util不可用，检查命令行版本
        try:
            result = subprocess.run(["scrapling", "--help"], capture_output=True, text=True, timeout=5)
            return result.returncode == 0 or "Usage:" in result.stdout or "Usage:" in result.stderr
        except:
            return False
    
    def _fetch_with_scrapling(self, url, wait_time=3000):
        if not self.scrapling_available:
            print("  Scrapling不可用")
            return None
        
        print(f"  抓取: {url}")
        print(f"  等待时间: {wait_time}ms")
        
        # 优先使用scrapling_util.fetch
        if SCRAPLING_UTIL_AVAILABLE:
            try:
                html_content = fetch(url, wait=wait_time, timeout=15000)
                if html_content:
                    print(f"  成功: {len(html_content)} 字节")
                    return html_content
                else:
                    print(f"  [WARNING] scrapling_util.fetch返回空内容，尝试命令行版本")
            except Exception as e:
                print(f"  [WARNING] scrapling_util.fetch异常: {e}")
        
        # 如果scrapling_util不可用或失败，使用命令行版本
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
                tmp_file = tmp.name
            
            cmd = ['scrapling', 'extract', 'fetch', url, tmp_file, '--wait', str(wait_time), '--timeout', '15000']
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=30)
            
            if result.returncode == 0:
                with open(tmp_file, 'r', encoding='utf-8') as f:
                    html = f.read()
                print(f"  成功: {len(html)} 字节")
                os.unlink(tmp_file)
                return html
            else:
                print(f"  失败: {result.stderr[:100]}")
                if os.path.exists(tmp_file):
                    os.unlink(tmp_file)
                return None
        except Exception as e:
            print(f"  错误: {e}")
            return None
    
    def _create_article(self, title, url, article_type="要闻", summary="", time_text=""):
        now = datetime.now()
        publish_time = None
        
        # 解析时间
        if "分钟前" in time_text:
            try:
                minutes = int(re.search(r'(\d+)', time_text).group(1))
                publish_time = now - timedelta(minutes=minutes)
            except:
                pass
        elif "小时前" in time_text:
            try:
                hours = int(re.search(r'(\d+)', time_text).group(1))
                publish_time = now - timedelta(hours=hours)
            except:
                pass
        
        within_48h = False
        if publish_time:
            time_diff = now - publish_time
            within_48h = time_diff.total_seconds() <= 48 * 3600
        
        return {
            'title': title,
            'url': url,
            'summary': summary,
            'type': article_type,
            'publish_time': publish_time.isoformat() if publish_time else "",
            'within_48h': within_48h,
            'source': '财联社'
        }
    
    def extract_articles(self, html):
        articles = []
        
        if not html:
            return articles
        
        print("提取文章...")
        
        # 1. 提取头条
        print("查找头条...")
        headline_pattern = r'<div class="depth-top-article-list">(.*?)</div>\s*</div>'
        headline_match = re.search(headline_pattern, html, re.DOTALL)
        
        if headline_match:
            headline_content = headline_match.group(1)
            main_pattern = r'<a class="f-s-23 f-w-b c-ef9524"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
            main_match = re.search(main_pattern, headline_content, re.DOTALL)
            
            if main_match:
                href = main_match.group(1).strip()
                title = main_match.group(2).strip()
                url = urljoin(self.base_url, href)
                
                # 提取摘要
                summary = ""
                summary_pattern = r'<ul class="clearfix depth-top-article-rec">(.*?)</ul>'
                summary_match = re.search(summary_pattern, headline_content, re.DOTALL)
                if summary_match:
                    summary_content = summary_match.group(1)
                    item_pattern = r'<a[^>]*>([^<]+)</a>'
                    items = re.findall(item_pattern, summary_content, re.DOTALL)
                    if items:
                        summary = " | ".join([item.strip() for item in items if item.strip()])
                
                article = self._create_article(title, url, "头条", summary)
                articles.append(article)
                print(f"  头条: {title[:50]}...")
        
        # 2. 提取要闻
        print("查找要闻...")
        hot_pattern = r'<div class="clearfix b-c-e6e7ea subject-interest-list">(.*?)</div>\s*</div>'
        hot_matches = re.findall(hot_pattern, html, re.DOTALL)
        
        print(f"  找到 {len(hot_matches)} 个要闻项目")
        
        for i, hot_content in enumerate(hot_matches, 1):
            try:
                # 提取标题
                title_pattern = r'<a class="f-w-b c-222 link-hover"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
                title_match = re.search(title_pattern, hot_content, re.DOTALL)
                
                if not title_match:
                    title_pattern2 = r'<a[^>]*class="[^"]*f-w-b[^"]*"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
                    title_match = re.search(title_pattern2, hot_content, re.DOTALL)
                
                if title_match:
                    href = title_match.group(1).strip()
                    title = title_match.group(2).strip()
                    url = urljoin(self.base_url, href)
                    
                    # 提取摘要
                    summary = ""
                    summary_pattern = r'<div class="f-s-14 c-666 line2 subject-interest-brief">([^<]+)</div>'
                    summary_match = re.search(summary_pattern, hot_content, re.DOTALL)
                    if summary_match:
                        summary = summary_match.group(1).strip()
                    
                    # 提取时间
                    time_text = ""
                    time_pattern = r'<span[^>]*>(\d+[分钟小]时前)</span>'
                    time_match = re.search(time_pattern, hot_content, re.DOTALL)
                    if time_match:
                        time_text = time_match.group(1)
                    
                    article = self._create_article(title, url, "要闻", summary, time_text)
                    articles.append(article)
                    
                    if i <= 5:  # 只显示前5个
                        print(f"  要闻{i}: {title[:50]}...")
                    
            except Exception as e:
                print(f"  要闻{i}错误: {e}")
                continue
        
        # 去重
        unique_articles = []
        seen_urls = set()
        for article in articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        print(f"去重后: {len(unique_articles)} 篇")
        return unique_articles
    
    def run(self):
        print("=" * 70)
        print("财联社热点新闻抓取")
        print("=" * 70)
        
        # 抓取
        html = self._fetch_with_scrapling(self.target_url)
        if not html:
            print("抓取失败")
            return []
        
        # 提取
        articles = self.extract_articles(html)
        
        # 过滤48小时内
        filtered = [a for a in articles if a.get('within_48h', False)]
        print(f"48小时内: {len(filtered)} 篇 (总计: {len(articles)} 篇)")
        
        # 保存
        if filtered:
            self._save_results(filtered)
        
        return filtered
    
    def _save_results(self, articles):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON文件
        json_file = self.output_dir / f"cls_hot_news_{timestamp}.json"
        data = {
            'source': '财联社',
            'crawl_time': datetime.now().isoformat(),
            'total': len(articles),
            'articles': articles
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"保存到: {json_file}")
        
        # 文本文件
        txt_file = self.output_dir / f"cls_hot_news_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"财联社热点新闻\n")
            f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"数量: {len(articles)} 篇\n\n")
            
            for i, article in enumerate(articles, 1):
                f.write(f"{i}. {article['title']}\n")
                f.write(f"   URL: {article['url']}\n")
                f.write(f"   类型: {article['type']}\n")
                if article['summary']:
                    f.write(f"   摘要: {article['summary']}\n")
                f.write(f"   48小时内: {'是' if article.get('within_48h') else '否'}\n\n")
        
        print(f"文本报告: {txt_file}")
        return json_file


def main():
    crawler = CLSHotNewsCrawler()
    articles = crawler.run()
    
    if articles:
        print("\n抓取完成!")
        print(f"共 {len(articles)} 篇文章")
    else:
        print("\n没有抓取到文章")
    
    return len(articles)


if __name__ == "__main__":
    try:
        count = main()
        sys.exit(0 if count > 0 else 1)
    except KeyboardInterrupt:
        print("\n用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)