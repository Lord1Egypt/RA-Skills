from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ai_search_web(
    query: str,
    engine: Optional[str] = "baidu",
    count: Optional[float] = 10.0
) -> Dict[str, Any]:
    """
    🔍 网络搜索 - 通用网络搜索（Google/Bing/百度/搜狗）

【重要】此工具会返回搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        engine: 搜索引擎，默认baidu
        count: 期望的结果数量，默认10
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "engine": engine,
        "count": count
    }
    
    return call_api("1777316659826691", "ai_search_web", arguments)

def ai_search_github(
    query: str,
    type: Optional[str] = "repositories",
    language: Optional[str] = None,
    sort: Optional[str] = "stars"
) -> Dict[str, Any]:
    """
    🐙 GitHub搜索 - 搜索GitHub仓库、代码、问题和用户

【重要】此工具会返回GitHub搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        type: 搜索类型，默认repositories
        language: 编程语言筛选（可选）
        sort: 排序方式，默认stars
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "type": type,
        "language": language,
        "sort": sort
    }
    
    return call_api("1777316659826691", "ai_search_github", arguments)

def ai_search_stackoverflow(
    query: str,
    tags: Optional[str] = None,
    sort: Optional[str] = "relevance"
) -> Dict[str, Any]:
    """
    💬 StackOverflow搜索 - 搜索技术问题和解决方案

【重要】此工具会返回StackOverflow搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词或问题描述
        tags: 标签筛选（如：javascript,react）
        sort: 排序方式，默认relevance
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "tags": tags,
        "sort": sort
    }
    
    return call_api("1777316659826691", "ai_search_stackoverflow", arguments)

def ai_search_npm(
    query: str,
    size: Optional[float] = 10.0
) -> Dict[str, Any]:
    """
    📦 NPM包搜索 - 搜索NPM包和相关文档

【重要】此工具会返回NPM搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 包名或关键词
        size: 返回结果数量，默认10
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "size": size
    }
    
    return call_api("1777316659826691", "ai_search_npm", arguments)

def ai_search_docs(
    query: str,
    framework: Optional[str] = "general"
) -> Dict[str, Any]:
    """
    📚 技术文档搜索 - 搜索常见框架和工具的官方文档（React、Vue、Node.js等）

【重要】此工具会返回文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        framework: 指定框架，默认general
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "framework": framework
    }
    
    return call_api("1777316659826691", "ai_search_docs", arguments)

def ai_search_api_reference(
    api_name: str,
    platform: str
) -> Dict[str, Any]:
    """
    🔗 API参考搜索 - 快速查找API文档和使用示例

【重要】此工具会返回API文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        api_name: API名称或方法名
        platform: 平台或库名称（如：express、axios、lodash）
    
    Returns:
        
    """
    arguments = {
        "api_name": api_name,
        "platform": platform
    }
    
    return call_api("1777316659826691", "ai_search_api_reference", arguments)

def ai_search_wechat_docs(
    query: str,
    platform: Optional[str] = "all"
) -> Dict[str, Any]:
    """
    📱 微信开发者文档搜索 - 搜索微信小程序、公众号、开放平台文档

【重要】此工具会返回微信文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        platform: 平台类型
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "platform": platform
    }
    
    return call_api("1777316659826691", "ai_search_wechat_docs", arguments)

def ai_search_csdn(
    query: str,
    type: Optional[str] = "all"
) -> Dict[str, Any]:
    """
    📝 CSDN搜索 - 搜索CSDN技术博客和问答

【重要】此工具会返回CSDN搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        type: 搜索类型
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "type": type
    }
    
    return call_api("1777316659826691", "ai_search_csdn", arguments)

def ai_search_juejin(
    query: str,
    sort: Optional[str] = "hot"
) -> Dict[str, Any]:
    """
    💎 掘金搜索 - 搜索掘金技术社区文章

【重要】此工具会返回掘金搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        sort: 排序方式
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "sort": sort
    }
    
    return call_api("1777316659826691", "ai_search_juejin", arguments)

def ai_search_segmentfault(
    query: str,
    tags: Optional[str] = None
) -> Dict[str, Any]:
    """
    🔧 SegmentFault搜索 - 搜索思否技术问答和文章

【重要】此工具会返回SegmentFault搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        tags: 标签筛选（可选）
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "tags": tags
    }
    
    return call_api("1777316659826691", "ai_search_segmentfault", arguments)

def ai_search_cnblogs(
    query: str
) -> Dict[str, Any]:
    """
    📚 博客园搜索 - 搜索博客园技术博客

【重要】此工具会返回博客园搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
    
    Returns:
        
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777316659826691", "ai_search_cnblogs", arguments)

def ai_search_oschina(
    query: str,
    type: Optional[str] = "all"
) -> Dict[str, Any]:
    """
    🌐 开源中国搜索 - 搜索开源中国技术资讯和项目

【重要】此工具会返回开源中国搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        type: 搜索类型
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "type": type
    }
    
    return call_api("1777316659826691", "ai_search_oschina", arguments)

def ai_search_aliyun_docs(
    query: str,
    product: Optional[str] = None
) -> Dict[str, Any]:
    """
    ☁️ 阿里云文档搜索 - 搜索阿里云产品文档和API

【重要】此工具会返回阿里云文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        product: 产品名称（如：ecs、oss、rds等）
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "product": product
    }
    
    return call_api("1777316659826691", "ai_search_aliyun_docs", arguments)

def ai_search_tencent_docs(
    query: str,
    product: Optional[str] = None
) -> Dict[str, Any]:
    """
    ☁️ 腾讯云文档搜索 - 搜索腾讯云产品文档和API

【重要】此工具会返回腾讯云文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
    
    Args:
        query: 搜索关键词
        product: 产品名称（如：cvm、cos、cdn等）
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "product": product
    }
    
    return call_api("1777316659826691", "ai_search_tencent_docs", arguments)

