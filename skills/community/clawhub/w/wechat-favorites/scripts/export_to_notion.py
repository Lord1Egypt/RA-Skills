#!/usr/bin/env python3
"""
微信收藏导出到 Notion
通过 Notion API 将微信收藏文章导入到指定的 Notion 数据库

使用方法:
1. 创建 Notion Integration: https://www.notion.so/my-integrations
2. 获取 API Key (Internal Integration Token)
3. 创建数据库并分享给 Integration
4. 运行脚本: python export_to_notion.py --token YOUR_TOKEN --database_id DATABASE_ID --input articles.csv

环境变量:
- NOTION_API_KEY: Notion Integration Token
- NOTION_DATABASE_ID: 目标数据库 ID
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Notion API 配置
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_API_VERSION = "2022-06-28"


class NotionClient:
    """Notion API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION
        }
        self.rate_limit_delay = 0.4  # Notion API 3 requests per second
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """发送 API 请求"""
        url = f"{NOTION_API_BASE}/{endpoint}"
        body = json.dumps(data).encode('utf-8') if data else None
        
        request = Request(url, data=body, headers=self.headers, method=method)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                time.sleep(self.rate_limit_delay)  # 限速
                response = urlopen(request)
                return json.loads(response.read().decode('utf-8'))
            except HTTPError as e:
                if e.code == 429:  # Rate limit
                    wait_time = int(e.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                elif e.code >= 500:  # Server error
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                error_body = e.read().decode('utf-8')
                raise Exception(f"Notion API error {e.code}: {error_body}")
            except URLError as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception(f"Network error: {e}")
        
        raise Exception("Max retries exceeded")
    
    def create_database_page(self, database_id: str, properties: Dict) -> Dict:
        """在数据库中创建新页面"""
        return self._request("POST", f"databases/{database_id}/query", 
                           {"filter": {"property": "Title", "title": {"is_empty": True}}})
    
    def create_page(self, parent_id: str, properties: Dict, children: Optional[List] = None) -> Dict:
        """创建页面"""
        data = {
            "parent": {"database_id": parent_id},
            "properties": properties
        }
        if children:
            data["children"] = children
        return self._request("POST", "pages", data)
    
    def query_database(self, database_id: str, filter_query: Optional[Dict] = None) -> List[Dict]:
        """查询数据库"""
        data = {"page_size": 100}
        if filter_query:
            data["filter"] = filter_query
        
        results = []
        has_more = True
        start_cursor = None
        
        while has_more:
            if start_cursor:
                data["start_cursor"] = start_cursor
            response = self._request("POST", f"databases/{database_id}/query", data)
            results.extend(response.get("results", []))
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")
        
        return results
    
    def get_database(self, database_id: str) -> Dict:
        """获取数据库信息"""
        return self._request("GET", f"databases/{database_id}")


class WechatFavorite:
    """微信收藏数据模型"""
    
    def __init__(self, data: Dict):
        self.title = data.get('title', '无标题')
        self.url = data.get('url', '')
        self.summary = data.get('summary', '')
        self.category = data.get('category', '未分类')
        self.tags = data.get('tags', '').split(',') if isinstance(data.get('tags'), str) else data.get('tags', [])
        self.create_time = data.get('create_time', '')
        self.author = data.get('author', '')
        self.source = data.get('source', '')
        self.content = data.get('content', '')
    
    @classmethod
    def from_csv_row(cls, row: Dict) -> 'WechatFavorite':
        """从 CSV 行创建"""
        return cls({
            'title': row.get('title', row.get('Title', '')),
            'url': row.get('url', row.get('URL', '')),
            'summary': row.get('summary', row.get('Summary', '')),
            'category': row.get('category', row.get('Category', '未分类')),
            'tags': row.get('tags', row.get('Tags', '')),
            'create_time': row.get('create_time', row.get('CreateTime', '')),
            'author': row.get('author', row.get('Author', '')),
            'source': row.get('source', row.get('Source', '微信公众号')),
            'content': row.get('content', row.get('Content', ''))
        })
    
    @classmethod
    def from_json(cls, data: Dict) -> 'WechatFavorite':
        """从 JSON 创建"""
        return cls(data)


def load_favorites_from_csv(csv_path: str) -> List[WechatFavorite]:
    """从 CSV 文件加载收藏数据"""
    favorites = []
    encoding = 'utf-8-sig'  # 支持 BOM
    
    # 尝试不同编码
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


def create_notion_properties(favorite: WechatFavorite) -> Dict:
    """创建 Notion 页面属性"""
    properties = {
        "Name": {
            "title": [{"text": {"content": favorite.title[:100]}}]  # Notion 标题限制
        }
    }
    
    # URL
    if favorite.url:
        properties["URL"] = {"url": favorite.url}
    
    # 分类 (Select)
    if favorite.category:
        properties["Category"] = {"select": {"name": favorite.category}}
    
    # 标签 (Multi-select)
    if favorite.tags:
        tags_list = [{"name": tag.strip()} for tag in favorite.tags if tag.strip()][:10]  # 最多10个标签
        if tags_list:
            properties["Tags"] = {"multi_select": tags_list}
    
    # 作者
    if favorite.author:
        properties["Author"] = {"rich_text": [{"text": {"content": favorite.author[:100]}}]}
    
    # 来源
    if favorite.source:
        properties["Source"] = {"rich_text": [{"text": {"content": favorite.source[:100]}}]}
    
    # 摘要
    if favorite.summary:
        properties["Summary"] = {"rich_text": [{"text": {"content": favorite.summary[:2000]}}]}
    
    # 创建时间 (Date)
    if favorite.create_time:
        try:
            # 尝试解析日期
            dt = datetime.fromisoformat(favorite.create_time.replace('Z', '+00:00'))
            properties["Created"] = {"date": {"start": dt.isoformat()}}
        except:
            pass
    
    return properties


def create_notion_content(favorite: WechatFavorite) -> List[Dict]:
    """创建 Notion 页面内容块"""
    children = []
    
    # 添加 URL 书签块
    if favorite.url:
        children.append({
            "object": "block",
            "type": "bookmark",
            "bookmark": {"url": favorite.url}
        })
    
    # 添加分隔线
    children.append({
        "object": "block",
        "type": "divider",
        "divider": {}
    })
    
    # 添加摘要
    if favorite.summary:
        children.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": favorite.summary[:2000]}}],
                "icon": {"emoji": "📝"}
            }
        })
    
    # 添加正文内容（如果有的话）
    if favorite.content:
        # 分段处理长文本
        content = favorite.content[:2000]  # Notion API 单块文本限制
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": content}}]
            }
        })
    
    return children


def export_to_notion(
    favorites: List[WechatFavorite],
    database_id: str,
    client: NotionClient,
    batch_size: int = 10,
    dry_run: bool = False
) -> Dict[str, int]:
    """导出收藏到 Notion"""
    stats = {
        'total': len(favorites),
        'success': 0,
        'failed': 0,
        'skipped': 0
    }
    
    # 获取已有文章 URL（用于去重）
    logger.info("检查已有数据...")
    existing_urls = set()
    try:
        existing_pages = client.query_database(database_id)
        for page in existing_pages:
            url_prop = page.get('properties', {}).get('URL', {})
            if url_prop.get('url'):
                existing_urls.add(url_prop['url'])
        logger.info(f"数据库中已有 {len(existing_urls)} 条记录")
    except Exception as e:
        logger.warning(f"获取已有数据失败: {e}，将跳过去重")
    
    for i, favorite in enumerate(favorites):
        # 去重检查
        if favorite.url and favorite.url in existing_urls:
            stats['skipped'] += 1
            logger.debug(f"跳过重复: {favorite.title}")
            continue
        
        if dry_run:
            logger.info(f"[DRY RUN] 将创建: {favorite.title}")
            stats['success'] += 1
            continue
        
        try:
            properties = create_notion_properties(favorite)
            children = create_notion_content(favorite)
            
            client.create_page(database_id, properties, children if children else None)
            stats['success'] += 1
            logger.info(f"[{i+1}/{stats['total']}] 成功: {favorite.title}")
            
            # 批次暂停
            if (i + 1) % batch_size == 0:
                logger.info(f"已处理 {i+1} 条，暂停 5 秒...")
                time.sleep(5)
                
        except Exception as e:
            stats['failed'] += 1
            logger.error(f"[{i+1}/{stats['total']}] 失败: {favorite.title} - {e}")
    
    return stats


def main():
    parser = argparse.ArgumentParser(description='微信收藏导出到 Notion')
    parser.add_argument('--input', '-i', required=True, help='输入文件 (CSV 或 JSON)')
    parser.add_argument('--token', '-t', help='Notion API Token (或设置 NOTION_API_KEY 环境变量)')
    parser.add_argument('--database-id', '-d', help='Notion 数据库 ID (或设置 NOTION_DATABASE_ID 环境变量)')
    parser.add_argument('--batch-size', '-b', type=int, default=10, help='批次大小 (默认: 10)')
    parser.add_argument('--dry-run', '-n', action='store_true', help='模拟运行，不实际创建')
    parser.add_argument('--limit', '-l', type=int, help='限制导出数量')
    parser.add_argument('--category', '-c', help='只导出指定分类')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 获取 API 配置
    api_key = args.token or os.environ.get('NOTION_API_KEY')
    database_id = args.database_id or os.environ.get('NOTION_DATABASE_ID')
    
    if not api_key:
        logger.error("缺少 Notion API Token，请通过 --token 参数或 NOTION_API_KEY 环境变量提供")
        sys.exit(1)
    
    if not database_id:
        logger.error("缺少 Notion 数据库 ID，请通过 --database-id 参数或 NOTION_DATABASE_ID 环境变量提供")
        sys.exit(1)
    
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
    
    # 创建客户端并导出
    client = NotionClient(api_key)
    
    # 验证数据库
    try:
        db_info = client.get_database(database_id)
        logger.info(f"目标数据库: {db_info.get('title', [{}])[0].get('plain_text', 'Unknown')}")
    except Exception as e:
        logger.error(f"无法访问数据库: {e}")
        sys.exit(1)
    
    # 执行导出
    logger.info(f"开始导出 {len(favorites)} 条收藏到 Notion...")
    stats = export_to_notion(favorites, database_id, client, args.batch_size, args.dry_run)
    
    # 输出统计
    logger.info("=" * 50)
    logger.info(f"导出完成: 总计 {stats['total']} 条")
    logger.info(f"  成功: {stats['success']}")
    logger.info(f"  失败: {stats['failed']}")
    logger.info(f"  跳过: {stats['skipped']} (重复)")
    
    if args.dry_run:
        logger.info("(模拟运行，未实际创建)")


if __name__ == '__main__':
    main()
