#!/usr/bin/env python3
"""
mptext API 客户端 - https://wechat.faiz-world.com
用于微信公众号文章获取的替代 API

API 端点:
- /api/public/v1/account     - 根据关键字搜索公众号
- /api/public/v1/accountbyurl - 根据文章链接查询公众号
- /api/public/v1/article     - 获取公众号文章列表
- /api/public/v1/download   - 获取文章内容
- /api/public/beta/authorinfo - 查询公众号主体信息
- /api/public/beta/aboutbiz - 查询公众号详细信息（需要 x-wechat-key）
"""

import os
import sys
import json
import urllib.parse
from typing import Optional, List, Dict, Any
import os
import re
import requests
from dataclasses import dataclass
from dotenv import load_dotenv

# 路径配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# API 基础配置
API_BASE_URL = "https://wechat.faiz-world.com"
NO_SNI_API_BASE = "https://wechat.faiz-world.com"


@dataclass
class AccountInfo:
    """公众号信息"""
    fakeid: str
    nickname: str
    alias: str = ""
    round_head_img: str = ""
    service_type: int = 0
    verified: bool = False
    signature: str = ""
    description: str = ""
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AccountInfo':
        return cls(
            fakeid=data.get('fakeid', ''),
            nickname=data.get('nickname', ''),
            alias=data.get('alias', ''),
            round_head_img=data.get('round_head_img', ''),
            service_type=data.get('service_type', 0),
            verified=bool(data.get('verified', False)),
            signature=data.get('signature', ''),
            description=data.get('description', ''),
        )


@dataclass
class ArticleInfo:
    """文章信息"""
    aid: str  # article id
    title: str
    link: str
    digest: str = ""
    cover: str = ""
    create_time: int = 0
    update_time: int = 0
    author: str = ""
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ArticleInfo':
        return cls(
            aid=data.get('aid', ''),
            title=data.get('title', ''),
            link=data.get('link', ''),
            digest=data.get('digest', ''),
            cover=data.get('cover', ''),
            create_time=data.get('create_time', 0),
            update_time=data.get('update_time', 0),
            author=data.get('author', ''),
        )


class MpTextAPI:
    """mptext API 客户端"""
    
    def __init__(self, api_key: str = None):
        """
        初始化 API 客户端
        
        Args:
            api_key: API 密钥（从环境变量 MPTEXT_API_KEY 获取）
        """
        self.api_key = api_key or os.getenv('MPTEXT_API_KEY', '')
        self.api_base = API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        })
        
        if self.api_key:
            self.session.headers['X-Auth-Key'] = self.api_key
    
    def _make_params(self, params: dict) -> dict:
        """添加认证参数（通过 Header 已处理）"""
        return params
    
    def _request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> dict:
        """发送请求"""
        url = f"{API_BASE_URL}{endpoint}"
        if params:
            params = self._make_params(params)
        
        try:
            if method.upper() == 'GET':
                r = self.session.get(url, params=params, timeout=30)
            else:
                r = self.session.post(url, json=data, params=params, timeout=30)
            
            result = r.json()
            
            # 检查错误
            base_resp = result.get('base_resp', {})
            if base_resp.get('ret', 0) != 0:
                err_msg = base_resp.get('err_msg', '未知错误')
                raise Exception(f"API 错误: {err_msg}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"响应解析失败: {e}")
    
    def search_account(self, keyword: str, begin: int = 0, size: int = 5) -> List[AccountInfo]:
        """
        根据关键字搜索公众号
        
        Args:
            keyword: 关键字
            begin: 起始索引
            size: 返回条数（最大20）
            
        Returns:
            公众号列表
        """
        if size > 20:
            size = 20
            
        result = self._request('GET', '/api/public/v1/account', {
            'keyword': keyword,
            'begin': begin,
            'size': size,
        })
        
        accounts = []
        for item in result.get('list', []):
            accounts.append(AccountInfo.from_dict(item))
        
        return accounts
    
    def get_account_by_url(self, url: str) -> Optional[AccountInfo]:
        """
        根据文章链接查询公众号
        
        Args:
            url: 文章链接
            
        Returns:
            公众号信息
        """
        result = self._request('GET', '/api/public/v1/accountbyurl', {
            'url': url,
        })
        
        # API 返回 'list' 数组格式，不是 'account'
        items = result.get('list', [])
        if items:
            return AccountInfo.from_dict(items[0])
        return None
    
    def get_articles(self, fakeid: str, begin: int = 0, size: int = 5) -> List[ArticleInfo]:
        """
        获取公众号文章列表
        
        Args:
            fakeid: 公众号 ID
            begin: 起始索引
            size: 返回条数（最大20）
            
        Returns:
            文章列表
        """
        if size > 20:
            size = 20
            
        result = self._request('GET', '/api/public/v1/article', {
            'fakeid': fakeid,
            'begin': begin,
            'size': size,
        })
        
        articles = []
        # API 返回 'articles' 字段
        for item in result.get('articles', []):
            articles.append(ArticleInfo.from_dict(item))
        
        return articles
        """
        获取公众号文章列表
        
        Args:
            fakeid: 公众号 ID
            begin: 起始索引
            size: 返回条数（最大20）
            
        Returns:
            文章列表
        """
        if size > 20:
            size = 20
            
        result = self._request('GET', '/api/public/v1/article', {
            'fakeid': fakeid,
            'begin': begin,
            'size': size,
        })
        
        articles = []
        # API 返回 'articles' 字段
        for item in result.get('articles', []):
            articles.append(ArticleInfo.from_dict(item))
        
        return articles
    
    def download_article(self, url: str, format: str = 'text') -> str:
        """
        获取文章内容
        
        Args:
            url: 文章链接
            format: 输出格式（html/markdown/text/json）
            
        Returns:
            文章内容
        """
        import urllib.parse
        import json as _json

        params_text = {'url': url, 'format': 'text'}
        params_json = {'url': url, 'format': 'json'}

        content = ''
        try:
            # text/markdown 格式：mptext text/plain 返回空，实际内容在 json 格式里
            if format in ('text', 'markdown'):
                r_text = self.session.get(f"{self.api_base}/api/public/v1/download", params=params_text, timeout=60)
                raw_text = r_text.text
                if raw_text.strip():
                    # 有内容则解析
                    try:
                        parsed = _json.loads(raw_text)
                        content = parsed.get('content_noencode', '') or parsed.get('title', '') or raw_text
                    except _json.JSONDecodeError:
                        content = raw_text.strip()
                else:
                    # text 格式返回空，fallback 到 json 格式提取 content_noencode / title
                    r_json = self.session.get(f"{self.api_base}/api/public/v1/download", params=params_json, timeout=60)
                    try:
                        parsed = _json.loads(r_json.text)
                        content = parsed.get('content_noencode', '') or parsed.get('title', '')
                    except _json.JSONDecodeError:
                        content = ''
            else:
                # json/html 格式返回 JSON
                result = self._request('GET', '/api/public/v1/download', params_json)
                # 优先 content_noencode（完整正文），其次 title（摘要/开头），最后 content
                content = (result.get('content_noencode', '')
                           or result.get('title', '')
                           or result.get('content', ''))
            
            # text/markdown 格式可能包含 CSS 前缀，需要去掉（仅对原始 raw text 有效）
            if format in ('text', 'markdown') and content.startswith('#js_'):
                # 找到第一个真正的内容行
                lines = content.split('\n')
                content_lines = []
                in_content = False
                for line in lines:
                    if not in_content and (line.startswith('#') or line.startswith('!') or (line and not line.startswith('#'))):
                        # 检查是否还包含 CSS
                        if 'max-width: 667px' in line or 'sns_opr_btn' in line:
                            continue
                        in_content = True
                    if in_content:
                        content_lines.append(line)
                content = '\n'.join(content_lines)
            
            return content.strip()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network request failed: {e}")

    def get_author_info(self, fakeid: str) -> dict:
        """
        查询公众号主体信息
        
        Args:
            fakeid: 公众号 ID
            
        Returns:
            主体信息
        """
        result = self._request('GET', '/api/public/beta/authorinfo', {
            'fakeid': fakeid,
        })
        
        return {
            'identity_name': result.get('identity_name', ''),
            'is_verify': result.get('is_verify', 0),
            'original_article_count': result.get('original_article_count', 0),
        }
    
    def get_about_biz(self, fakeid: str, wechat_key: str = None) -> dict:
        """
        查询公众号详细信息
        
        Args:
            fakeid: 公众号 ID
            wechat_key: 微信密钥（可选）
            
        Returns:
            详细信息
        """
        params = {'fakeid': fakeid}
        if wechat_key:
            params['key'] = wechat_key
            
        result = self._request('GET', '/api/public/beta/aboutbiz', params)
        
        return result


# 全局客户端实例（延迟初始化）
_client: Optional[MpTextAPI] = None


def get_client() -> MpTextAPI:
    """获取全局 API 客户端"""
    global _client
    if _client is None:
        # 确保 env 已加载
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill.env")
        load_dotenv(env_file)
        _client = MpTextAPI()
    return _client


# 命令行接口
def cmd_search(keyword: str, size: int = 5):
    """搜索公众号"""
    client = get_client()
    
    try:
        accounts = client.search_account(keyword, size=size)
        
        if not accounts:
            print(f"No accounts found for keyword '{keyword}'")
            return
        
        print(f"Found {len(accounts)} accounts:\n")
        for i, acc in enumerate(accounts, 1):
            verified_mark = "[V]" if acc.verified else ""
            print(f"{i}. {acc.nickname} {verified_mark}")
            if acc.alias:
                print(f"   Alias: {acc.alias}")
            print(f"   ID: {acc.fakeid}")
            if acc.signature:
                print(f"   Bio: {acc.signature}")
            print()
            
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")
        sys.exit(1)


def cmd_articles(fakeid: str, size: int = 5):
    """获取文章列表"""
    client = get_client()
    
    try:
        articles = client.get_articles(fakeid, size=size)
        
        if not articles:
            print("No articles found")
            return
        
        print(f"Found {len(articles)} articles:\n")
        for i, art in enumerate(articles, 1):
            print(f"{i}. {art.title}")
            print(f"   Link: {art.link}")
            if art.digest:
                print(f"   Digest: {art.digest}")
            print()
            
    except Exception as e:
        print(f"[ERROR] Get articles failed: {e}")
        sys.exit(1)


def cmd_download(url: str, format: str = 'text'):
    """下载文章"""
    client = get_client()
    
    try:
        content = client.download_article(url, format=format)
        
        if not content:
            print("[WARN] Article content is empty, may need auth or article doesn't exist")
            sys.exit(1)
        
        print(content)
        
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        sys.exit(1)


def cmd_authorinfo(fakeid: str):
    """查询主体信息"""
    client = get_client()
    
    try:
        info = client.get_author_info(fakeid)
        
        print(f"主体名称: {info.get('identity_name', '未知')}")
        print(f"是否认证: {'是' if info.get('is_verify') else '否'}")
        print(f"原创文章数: {info.get('original_article_count', 0)}")
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法:")
        print("  python3 mptext_api.py search <关键字> [数量]   # 搜索公众号")
        print("  python3 mptext_api.py articles <fakeid> [数量]  # 获取文章列表")
        print("  python3 mptext_api.py download <url> [格式]     # 下载文章")
        print("  python3 mptext_api.py authorinfo <fakeid>      # 查询主体信息")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "search" and len(sys.argv) >= 3:
        keyword = sys.argv[2]
        size = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        cmd_search(keyword, size)
        
    elif cmd == "articles" and len(sys.argv) >= 3:
        fakeid = sys.argv[2]
        size = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        cmd_articles(fakeid, size)
        
    elif cmd == "download" and len(sys.argv) >= 3:
        url = sys.argv[2]
        format = sys.argv[3] if len(sys.argv) > 3 else 'text'
        cmd_download(url, format)
        
    elif cmd == "authorinfo" and len(sys.argv) >= 3:
        fakeid = sys.argv[2]
        cmd_authorinfo(fakeid)
        
    else:
        print("未知命令")
        main()


if __name__ == "__main__":
    main()