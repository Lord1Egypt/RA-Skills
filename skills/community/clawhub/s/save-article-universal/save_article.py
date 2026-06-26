#!/usr/bin/env python3
"""
save_article_universal.py — 通用微信公众号文章保存工具
支持多种笔记应用：Obsidian、Miaoyan、Notion、本地文件夹
"""

import os
import re
import sys
import json
import subprocess
import argparse
from datetime import datetime
from urllib.parse import urlparse

# ============== 配置 ==============
DEFAULT_CONFIG = {
    "save_method": "local",
    "save_path": os.path.expanduser("~/Documents/Articles"),
    "obsidian_vault_path": None,
    "notion_api_key": None,
    "notion_database_id": None,
    "file_naming": "title_date",
    "include_summary": True,
    "include_full_content": True,
    "include_metadata": True,
    "summary_length": 500
}

# ============== 工具函数 ==============
def load_config():
    """加载配置文件"""
    config = DEFAULT_CONFIG.copy()
    
    # 读取环境变量
    env_mappings = {
        "SAVE_METHOD": "save_method",
        "SAVE_PATH": "save_path",
        "OBSIDIAN_VAULT_PATH": "obsidian_vault_path",
        "NOTION_API_KEY": "notion_api_key",
        "NOTION_DATABASE_ID": "notion_database_id",
        "FILE_NAMING": "file_naming",
        "INCLUDE_SUMMARY": "include_summary",
        "INCLUDE_FULL_CONTENT": "include_full_content",
        "SUMMARY_LENGTH": "summary_length"
    }
    
    for env_key, config_key in env_mappings.items():
        value = os.environ.get(env_key)
        if value is not None:
            if value.lower() in ("true", "false"):
                config[config_key] = value.lower() == "true"
            elif value.isdigit():
                config[config_key] = int(value)
            else:
                config[config_key] = value
    
    # 读取配置文件
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            file_config = json.load(f)
            config.update(file_config)
    
    return config

def clean_html(html: str) -> str:
    """清理 HTML 标签，保留段落结构"""
    text = re.sub(r'</p>', '\n\n', html)
    text = re.sub(r'</div>', '\n', text)
    text = re.sub(r'<br[^>]*>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def generate_summary(content: str, max_length: int = 500) -> str:
    """生成要点摘要"""
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    summary_lines = []
    
    keywords = ['首先', '其次', '第一', '第二', '总结', '结论', '建议', '要点', '核心', '什么是', '如何', '怎么']
    
    for line in lines[:20]:
        if 10 < len(line) < 150:
            if any(kw in line for kw in keywords) or re.search(r'\d+', line):
                summary_lines.append(line)
        if len(summary_lines) >= 5:
            break
    
    if not summary_lines:
        summary_lines = [l for l in lines[:3] if 20 < len(line) < 200]
    
    summary = '\n\n'.join(summary_lines)
    if len(summary) > max_length:
        summary = summary[:max_length] + "..."
    
    return summary or content[:max_length] + "..."

# ============== 抓取函数 ==============
def fetch_article(url: str) -> dict:
    """抓取文章内容"""
    cmd = [
        "curl", "-s", "-L", "--max-time", "15",
        "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to fetch: {result.stderr}")
    
    html = result.stdout
    
    # 提取标题
    title_match = re.search(r'<h1[^>]*class="rich_media_title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if title_match:
        title = clean_html(title_match.group(1))
    else:
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = clean_html(title_match.group(1)) if title_match else "未命名文章"
    
    # 提取正文
    content_match = re.search(r'<div[^>]*class="rich_media_content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*<script', html, re.DOTALL)
    if not content_match:
        content_match = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
    
    content = clean_html(content_match.group(1)) if content_match else ""
    
    return {
        "title": title,
        "content": content,
        "url": url,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

# ============== 保存处理器 ==============
class SaveHandler:
    def __init__(self, config: dict):
        self.config = config
    
    def get_save_path(self) -> str:
        """获取保存路径"""
        method = self.config["save_method"]
        
        if method == "obsidian":
            path = self.config.get("obsidian_vault_path")
            if not path:
                raise ValueError("OBSIDIAN_VAULT_PATH not configured")
            return path
        
        elif method == "miaoyan":
            # Miaoyan 默认路径
            return os.path.expanduser(
                "~/Library/Mobile Documents/iCloud~com~tw93~miaoyan/Documents/待学习"
            )
        
        elif method == "local":
            path = self.config.get("save_path")
            if not path:
                raise ValueError("SAVE_PATH not configured")
            return path
        
        else:
            raise ValueError(f"Unknown save method: {method}")
    
    def generate_filename(self, title: str) -> str:
        """生成文件名"""
        naming = self.config.get("file_naming", "title_date")
        date = datetime.now().strftime("%Y-%m-%d")
        
        # 清理文件名
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)[:50]
        
        if naming == "title":
            return f"{safe_title}.md"
        elif naming == "title_date":
            return f"{safe_title}_{date}.md"
        elif naming == "date_title":
            return f"{date}_{safe_title}.md"
        elif naming == "timestamp":
            ts = int(datetime.now().timestamp())
            return f"{ts}_{safe_title}.md"
        else:
            return f"{safe_title}.md"
    
    def generate_markdown(self, article: dict) -> str:
        """生成 Markdown 内容"""
        parts = []
        
        # 元数据（YAML frontmatter）
        if self.config.get("include_metadata", True):
            parts.append(f"""---
title: {article['title']}
url: {article['url']}
date: {article['date']}
---

""")
        
        # 标题
        parts.append(f"# {article['title']}\n")
        
        # 要点摘要
        if self.config.get("include_summary", True):
            summary = generate_summary(article['content'], self.config.get("summary_length", 500))
            parts.append(f"## 📌 要点\n\n{summary}\n\n---\n")
        
        # 完整正文
        if self.config.get("include_full_content", True):
            parts.append(f"## 正文\n\n{article['content']}\n\n---\n")
        
        # 源链接
        parts.append(f"## 原文\n\n[{article['title']}]({article['url']})\n\n")
        parts.append(f"*保存时间: {article['date']}*\n")
        
        return '\n'.join(parts)
    
    def save(self, article: dict) -> str:
        """保存文章"""
        save_dir = self.get_save_path()
        filename = self.generate_filename(article['title'])
        filepath = os.path.join(save_dir, filename)
        
        # 创建目录
        os.makedirs(save_dir, exist_ok=True)
        
        # 生成内容
        content = self.generate_markdown(article)
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath

# ============== 主函数 ==============
def main():
    parser = argparse.ArgumentParser(description="通用微信公众号文章保存工具")
    parser.add_argument("url", help="文章链接")
    parser.add_argument("--output", "-o", help="保存目录（覆盖配置）")
    parser.add_argument("--method", "-m", choices=["local", "obsidian", "miaoyan", "notion"], help="保存方法")
    parser.add_argument("--config", "-c", help="配置文件路径")
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    
    # 命令行参数覆盖
    if args.output:
        config["save_path"] = args.output
        config["save_method"] = "local"
    if args.method:
        config["save_method"] = args.method
    
    print(f"🔄 正在处理: {args.url}")
    
    try:
        # 抓取文章
        article = fetch_article(args.url)
        print(f"✅ 已获取: {article['title']}")
        
        # 保存
        handler = SaveHandler(config)
        filepath = handler.save(article)
        print(f"✅ 已保存: {filepath}")
        
        print(f"\n🎉 完成!")
        return 0
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
