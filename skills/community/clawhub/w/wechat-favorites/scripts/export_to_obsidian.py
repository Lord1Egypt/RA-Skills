#!/usr/bin/env python3
r"""
微信收藏导出到 Obsidian
将微信收藏文章转换为 Markdown 文件，保存到 Obsidian vault 目录

使用方法:
1. 指定 Obsidian vault 路径
2. 运行脚本: python export_to_obsidian.py --input articles.csv --vault "D:\Obsidian\MyVault"

特性:
- 按年/月分类存储
- 自动生成 YAML frontmatter
- 支持标签、分类、时间元数据
- 支持增量同步（跳过已存在文件）
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse
import hashlib

# Windows stdout UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WechatFavorite:
    """微信收藏数据模型"""
    
    def __init__(self, data: Dict):
        self.title = data.get('title', '无标题')
        self.url = data.get('url', '')
        self.summary = data.get('summary', '')
        self.category = data.get('category', '未分类')
        self.tags = self._parse_tags(data.get('tags', ''))
        self.create_time = data.get('create_time', '')
        self.author = data.get('author', '')
        self.source = data.get('source', '')
        self.content = data.get('content', '')
        self.nickname = data.get('nickname', '')  # 公众号名称
    
    def _parse_tags(self, tags) -> List[str]:
        """解析标签"""
        if isinstance(tags, list):
            return [t.strip() for t in tags if t.strip()]
        if isinstance(tags, str):
            return [t.strip() for t in tags.split(',') if t.strip()]
        return []
    
    @classmethod
    def from_csv_row(cls, row: Dict) -> 'WechatFavorite':
        """从 CSV 行创建"""
        return cls({
            'title': row.get('title', row.get('Title', '')),
            'url': row.get('url', row.get('URL', '')),
            'summary': row.get('summary', row.get('Summary', '')),
            'category': row.get('category', row.get('Category', '未分类')),
            'tags': row.get('tags', row.get('Tags', '')),
            'create_time': row.get('create_time', row.get('CreateTime', row.get('createTime', ''))),
            'author': row.get('author', row.get('Author', '')),
            'source': row.get('source', row.get('Source', '微信公众号')),
            'content': row.get('content', row.get('Content', '')),
            'nickname': row.get('nickname', row.get('Nickname', ''))
        })
    
    @classmethod
    def from_json(cls, data: Dict) -> 'WechatFavorite':
        """从 JSON 创建"""
        return cls(data)


def load_favorites_from_csv(csv_path: str) -> List[WechatFavorite]:
    """从 CSV 文件加载收藏数据"""
    favorites = []
    encoding = 'utf-8-sig'
    
    for enc in ['utf-8-sig', 'utf-8', 'gbk', 'gb18030']:
        try:
            with open(csv_path, 'r', encoding=enc) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    favorites.append(WechatFavorite.from_csv_row(row))
            logger.info(f"使用 {enc} 编码成功加载 {len(favorites)} 条收藏")
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logger.error(f"加载 CSV 失败: {e}")
            break
    
    return favorites


def load_favorites_from_json(json_path: str) -> List[WechatFavorite]:
    """从 JSON 文件加载收藏数据"""
    favorites = []
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                favorites = [WechatFavorite.from_json(item) for item in data]
            elif isinstance(data, dict):
                favorites = [WechatFavorite.from_json(data)]
        logger.info(f"从 JSON 加载 {len(favorites)} 条收藏")
    except Exception as e:
        logger.error(f"加载 JSON 失败: {e}")
    
    return favorites


def sanitize_filename(name: str) -> str:
    """清理文件名，移除非法字符"""
    # Windows 非法字符
    illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'
    name = re.sub(illegal_chars, '_', name)
    # 移除首尾空格和点
    name = name.strip('. ')
    # 限制长度
    return name[:100] if name else 'Untitled'


def generate_filename(favorite: WechatFavorite, use_hash: bool = False) -> str:
    """生成文件名"""
    if use_hash and favorite.url:
        # 使用 URL hash 作为文件名（避免重复）
        url_hash = hashlib.md5(favorite.url.encode()).hexdigest()[:8]
        return f"{url_hash}.md"
    
    # 使用标题作为文件名
    title = sanitize_filename(favorite.title)
    
    # 添加时间前缀（如果有的话）
    if favorite.create_time:
        try:
            dt = datetime.fromisoformat(favorite.create_time.replace('Z', '+00:00'))
            date_prefix = dt.strftime('%Y%m%d')
            return f"{date_prefix}_{title}.md"
        except:
            pass
    
    return f"{title}.md"


def generate_frontmatter(favorite: WechatFavorite) -> str:
    """生成 YAML frontmatter"""
    fm_lines = ['---']
    fm_lines.append(f'title: "{favorite.title.replace(chr(34), chr(92)+chr(34))}"')
    
    if favorite.url:
        fm_lines.append(f'url: "{favorite.url}"')
    
    if favorite.category:
        fm_lines.append(f'category: "{favorite.category}"')
    
    if favorite.tags:
        tags_str = ', '.join([f'"{t}"' for t in favorite.tags])
        fm_lines.append(f'tags: [{tags_str}]')
    
    if favorite.author:
        fm_lines.append(f'author: "{favorite.author}"')
    
    if favorite.source:
        fm_lines.append(f'source: "{favorite.source}"')
    
    if favorite.nickname:
        fm_lines.append(f'nickname: "{favorite.nickname}"')
    
    if favorite.create_time:
        try:
            dt = datetime.fromisoformat(favorite.create_time.replace('Z', '+00:00'))
            fm_lines.append(f'created: {dt.strftime("%Y-%m-%d %H:%M")}')
        except:
            fm_lines.append(f'created: "{favorite.create_time}"')
    
    fm_lines.append(f'imported: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    fm_lines.append('---')
    
    return '\n'.join(fm_lines)


def generate_markdown_content(favorite: WechatFavorite, include_content: bool = True) -> str:
    """生成完整的 Markdown 内容"""
    parts = [generate_frontmatter(favorite), '']
    
    # 标题
    parts.append(f'# {favorite.title}')
    parts.append('')
    
    # 元信息
    meta_parts = []
    if favorite.author:
        meta_parts.append(f'**作者**: {favorite.author}')
    if favorite.nickname:
        meta_parts.append(f'**公众号**: {favorite.nickname}')
    if favorite.source:
        meta_parts.append(f'**来源**: {favorite.source}')
    
    if meta_parts:
        parts.append(' | '.join(meta_parts))
        parts.append('')
    
    # URL
    if favorite.url:
        parts.append(f'🔗 [原文链接]({favorite.url})')
        parts.append('')
    
    # 摘要
    if favorite.summary:
        parts.append('## 摘要')
        parts.append('')
        parts.append(f'> {favorite.summary}')
        parts.append('')
    
    # 正文内容
    if include_content and favorite.content:
        parts.append('## 正文')
        parts.append('')
        parts.append(favorite.content)
        parts.append('')
    
    # 标签
    if favorite.tags:
        parts.append('---')
        parts.append('')
        tags_str = ' '.join([f'#{t}' for t in favorite.tags])
        parts.append(tags_str)
    
    return '\n'.join(parts)


def get_output_path(
    favorite: WechatFavorite,
    vault_path: Path,
    organize_by: str = 'date',
    flat: bool = False
) -> Path:
    """确定输出路径"""
    if flat:
        return vault_path / sanitize_filename(favorite.title) / '.md'
    
    if organize_by == 'date' and favorite.create_time:
        try:
            dt = datetime.fromisoformat(favorite.create_time.replace('Z', '+00:00'))
            year = dt.strftime('%Y')
            month = dt.strftime('%m')
            filename = generate_filename(favorite)
            return vault_path / year / month / filename
        except:
            pass
    elif organize_by == 'category':
        category = sanitize_filename(favorite.category) if favorite.category else '未分类'
        filename = generate_filename(favorite)
        return vault_path / category / filename
    elif organize_by == 'source' and favorite.nickname:
        source = sanitize_filename(favorite.nickname)
        filename = generate_filename(favorite)
        return vault_path / source / filename
    
    # 默认按年月组织
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    return vault_path / year / month / generate_filename(favorite)


def export_to_obsidian(
    favorites: List[WechatFavorite],
    vault_path: Path,
    organize_by: str = 'date',
    include_content: bool = True,
    skip_existing: bool = True,
    dry_run: bool = False
) -> Dict[str, int]:
    """导出收藏到 Obsidian vault"""
    stats = {
        'total': len(favorites),
        'success': 0,
        'failed': 0,
        'skipped': 0
    }
    
    # 获取已存在文件（用于去重）
    existing_files = set()
    if skip_existing:
        for md_file in vault_path.rglob('*.md'):
            existing_files.add(md_file.name)
        logger.info(f"Vault 中已有 {len(existing_files)} 个文件")
    
    for i, favorite in enumerate(favorites):
        try:
            output_path = get_output_path(favorite, vault_path, organize_by)
            filename = output_path.name
            
            # 去重检查
            if skip_existing and filename in existing_files:
                stats['skipped'] += 1
                logger.debug(f"跳过已存在: {favorite.title}")
                continue
            
            if dry_run:
                logger.info(f"[DRY RUN] 将创建: {output_path}")
                stats['success'] += 1
                continue
            
            # 创建目录
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入文件
            content = generate_markdown_content(favorite, include_content)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            stats['success'] += 1
            logger.info(f"[{i+1}/{stats['total']}] 创建: {favorite.title[:50]}")
            
        except Exception as e:
            stats['failed'] += 1
            logger.error(f"[{i+1}/{stats['total']}] 失败: {favorite.title[:30]} - {e}")
    
    return stats


def create_obsidian_templates(vault_path: Path):
    """创建 Obsidian 模板文件"""
    templates_dir = vault_path / 'Templates'
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # 微信收藏模板
    wechat_template = templates_dir / '微信收藏模板.md'
    if not wechat_template.exists():
        template_content = '''---
title: "{{title}}"
url: "{{url}}"
category: "{{category}}"
tags: [{{tags}}]
author: "{{author}}"
source: "{{source}}"
created: {{created}}
imported: {{imported}}
---

# {{title}}

**作者**: {{author}} | **公众号**: {{nickname}}

🔗 [原文链接]({{url}})

## 摘要

> {{summary}}

## 正文

{{content}}

---

{{#each tags}}#{{this}} {{/each}}
'''
        wechat_template.write_text(template_content, encoding='utf-8')
        logger.info(f"创建模板: {wechat_template}")


def main():
    parser = argparse.ArgumentParser(description='微信收藏导出到 Obsidian')
    parser.add_argument('--input', '-i', required=True, help='输入文件 (CSV 或 JSON)')
    parser.add_argument('--vault', '-v', required=True, help='Obsidian vault 路径')
    parser.add_argument('--organize', '-o', choices=['date', 'category', 'source', 'flat'], 
                       default='date', help='组织方式 (默认: date)')
    parser.add_argument('--no-content', action='store_true', help='不包含正文内容')
    parser.add_argument('--skip-existing', action='store_true', default=True, 
                       help='跳过已存在文件 (默认: True)')
    parser.add_argument('--force', '-f', action='store_true', help='强制覆盖已存在文件')
    parser.add_argument('--dry-run', '-n', action='store_true', help='模拟运行')
    parser.add_argument('--limit', '-l', type=int, help='限制导出数量')
    parser.add_argument('--category', '-c', help='只导出指定分类')
    parser.add_argument('--create-templates', action='store_true', help='创建 Obsidian 模板')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 验证 vault 路径
    vault_path = Path(args.vault)
    if not vault_path.exists():
        logger.error(f"Obsidian vault 路径不存在: {args.vault}")
        sys.exit(1)
    
    # 创建模板
    if args.create_templates:
        create_obsidian_templates(vault_path)
    
    # 加载数据
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"文件不存在: {args.input}")
        sys.exit(1)
    
    if input_path.suffix.lower() == '.csv':
        favorites = load_favorites_from_csv(str(input_path))
    elif input_path.suffix.lower() == '.json':
        favorites = load_favorites_from_json(str(input_path))
    else:
        logger.error(f"不支持的文件格式: {input_path.suffix}")
        sys.exit(1)
    
    if not favorites:
        logger.error("没有可导出的数据")
        sys.exit(1)
    
    # 过滤分类
    if args.category:
        favorites = [f for f in favorites if f.category == args.category]
        logger.info(f"筛选分类 '{args.category}'，共 {len(favorites)} 条")
    
    # 限制数量
    if args.limit:
        favorites = favorites[:args.limit]
        logger.info(f"限制导出 {args.limit} 条")
    
    # 执行导出
    logger.info(f"开始导出 {len(favorites)} 条收藏到 Obsidian...")
    stats = export_to_obsidian(
        favorites,
        vault_path,
        organize_by=args.organize,
        include_content=not args.no_content,
        skip_existing=not args.force,
        dry_run=args.dry_run
    )
    
    # 输出统计
    logger.info("=" * 50)
    logger.info(f"导出完成: 总计 {stats['total']} 条")
    logger.info(f"  成功: {stats['success']}")
    logger.info(f"  失败: {stats['failed']}")
    logger.info(f"  跳过: {stats['skipped']} (已存在)")
    
    if args.dry_run:
        logger.info("(模拟运行，未实际创建文件)")


if __name__ == '__main__':
    main()
