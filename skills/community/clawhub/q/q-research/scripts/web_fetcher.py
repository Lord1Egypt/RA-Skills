"""
WebFetcher - 高级网页抓取工具
===============================

功能特性:
- Token Bucket 限速器 - 防止请求过快被封
- Stealth 请求头 - 伪装成真实浏览器
- curl_cffi 模拟浏览器指纹 - 高级反反爬
- BeautifulSoup + lxml 解析 - 高效 HTML 解析
- 代理支持 - 灵活配置代理
- 自动提取文本和JSON数据

依赖安装:
    pip install curl_cffi beautifulsoup4 lxml fake-useragent

Author: AI Assistant
"""

import time
import json
import random
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List, Union
from urllib.parse import urlparse, parse_qs
from threading import Lock
from contextlib import contextmanager

from bs4 import BeautifulSoup

try:
    from curl_cffi import requests as curl_requests
    CURL_CFFI_AVAILABLE = True
except ImportError:
    CURL_CFFI_AVAILABLE = False
    curl_requests = None

import requests

try:
    from fake_useragent import UserAgent
    FAKE_UA_AVAILABLE = True
except ImportError:
    FAKE_UA_AVAILABLE = False


# ============================================================================
# 配置与常量
# ============================================================================

DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

BROWSER_PROFILES = [
    "chrome110", "chrome116", "chrome120", "chrome124",
    "chrome126", "edge101", "edge117", "edge120",
    "safari15_5", "safari16_5", "safari17_0"
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Token Bucket 限速器
# ============================================================================

class TokenBucket:
    """
    Token Bucket 算法实现限速器
    
    原理：
    - 桶的容量为 burst_size，代表最大突发请求数
    - 以 constant_rate 速率向桶中添加 token
    - 每次请求消耗一个 token
    - 如果桶中没有足够的 token，则需要等待
    """
    
    def __init__(self, rate: float = 5.0, burst: int = 10):
        """
        初始化限速器
        
        Args:
            rate: 每秒产生的 token 数量（每秒请求数上限）
            burst: 令牌桶容量（最大突发请求数）
        """
        self.rate = rate  # tokens per second
        self.burst = burst  # max bucket size
        self.tokens = burst
        self.last_update = time.time()
        self.lock = Lock()
        
    def _refill(self):
        """自动补充 token"""
        now = time.time()
        elapsed = now - self.last_update
        # 根据流逝的时间补充 token
        new_tokens = elapsed * self.rate
        self.tokens = min(self.burst, self.tokens + new_tokens)
        self.last_update = now
        
    def acquire(self, tokens: int = 1, blocking: bool = True, timeout: float = None) -> bool:
        """
        获取 token
        
        Args:
            tokens: 需要获取的 token 数量
            blocking: 是否阻塞等待
            timeout: 阻塞超时时间（秒）
            
        Returns:
            bool: 是否成功获取 token
        """
        start_time = time.time()
        
        while True:
            with self.lock:
                self._refill()
                
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True
                
                if not blocking:
                    return False
                
                # 计算需要等待的时间
                wait_time = (tokens - self.tokens) / self.rate
                
                # 检查超时
                if timeout is not None:
                    elapsed = time.time() - start_time
                    if elapsed + wait_time > timeout:
                        return False
                    
            # 释放锁并等待
            time.sleep(min(wait_time, 0.1))
            
    def __enter__(self):
        """上下文管理器入口"""
        self.acquire()
        return self
        
    def __exit__(self, *args):
        pass


# ============================================================================
# 数据类定义
# ============================================================================

@dataclass
class FetchResult:
    """
    网页抓取结果封装类
    
    Attributes:
        url: 请求的 URL
        status_code: HTTP 状态码
        headers: 响应头
        content: 原始 HTML 内容
        text: 提取的文本内容
        json_data: 自动检测并解析的 JSON 数据（如果存在）
        cookies: 响应的 cookies
        error: 错误信息（如果有）
        elapsed: 请求耗时（秒）
        is_success: 是否成功
    """
    url: str
    status_code: int = 0
    headers: Dict[str, str] = field(default_factory=dict)
    content: str = ""
    text: str = ""
    json_data: Any = None
    cookies: Dict[str, str] = field(default_factory=dict)
    error: Optional[str] = None
    elapsed: float = 0.0
    is_success: bool = False
    
    def __post_init__(self):
        """后处理：尝试解析 JSON"""
        if self.is_success and self.json_data is None:
            self._try_parse_json()
            
    def _try_parse_json(self):
        """尝试从内容中解析 JSON"""
        # 检查是否看起来像 JSON
        content = self.content.strip()
        
        # 检查是否以 { 或 [ 开头
        if content.startswith('{') or content.startswith('['):
            try:
                self.json_data = json.loads(content)
            except json.JSONDecodeError:
                pass
                
    @property
    def soup(self) -> Optional[BeautifulSoup]:
        """返回 BeautifulSoup 对象"""
        if self.content:
            return BeautifulSoup(self.content, 'lxml')
        return None
        
    def find(self, *args, **kwargs) -> Optional[BeautifulSoup]:
        """使用 BeautifulSoup 查找元素"""
        if self.soup:
            return self.soup.find(*args, **kwargs)
        return None
        
    def find_all(self, *args, **kwargs) -> List[BeautifulSoup]:
        """使用 BeautifulSoup 查找所有匹配元素"""
        if self.soup:
            return self.soup.find_all(*args, **kwargs)
        return []
        
    def select(self, selector: str) -> List[BeautifulSoup]:
        """使用 CSS 选择器"""
        if self.soup:
            return self.soup.select(selector)
        return []
        
    def get_text_content(self, selector: str = None) -> str:
        """
        获取文本内容
        
        Args:
            selector: CSS 选择器，如果为 None 则返回全部文本
            
        Returns:
            str: 提取的文本
        """
        if selector:
            elements = self.select(selector)
            return '\n'.join(elem.get_text(strip=True) for elem in elements)
        return self.text


# ============================================================================
# WebFetcher 主类
# ============================================================================

class WebFetcher:
    """
    高级网页抓取工具
    
    功能特性:
    - Token Bucket 限速 - 可配置请求频率
    - Stealth 请求头 - 模拟真实浏览器
    - curl_cffi 指纹 - 高级浏览器模拟
    - 代理支持 - HTTP/HTTPS/SOCKS 代理
    - 自动重试 - 失败自动重试
    - 代理池支持 - 自动切换代理
    
    使用示例:
        >>> fetcher = WebFetcher(rate=5, burst=10)
        >>> result = fetcher.fetch("https://example.com")
        >>> if result.is_success:
        ...     print(result.text)
        ...     print(result.json_data)
        
        # 带代理
        >>> fetcher = WebFetcher(proxy="http://127.0.0.1:7890")
        >>> result = fetcher.fetch("https://example.com")
        
        # 使用代理池
        >>> fetcher = WebFetcher(proxies=[
        ...     "http://proxy1:8080",
        ...     "http://proxy2:8080"
        ... ])
    """
    
    def __init__(
        self,
        rate: float = 5.0,
        burst: int = 10,
        proxy: str = None,
        proxies: List[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        browser_profile: str = "chrome120",
        follow_redirects: bool = True,
        verify_ssl: bool = True,
        extra_headers: Dict[str, str] = None,
    ):
        """
        初始化 WebFetcher
        
        Args:
            rate: 每秒请求数限制（默认 5）
            burst: 令牌桶容量（默认 10）
            proxy: 单个代理地址（格式: http://host:port 或 socks5://host:port）
            proxies: 代理池列表，会自动随机切换
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
            browser_profile: 浏览器指纹配置文件
            follow_redirects: 是否跟随重定向
            verify_ssl: 是否验证 SSL 证书
            extra_headers: 额外的请求头
        """
        self.rate = rate
        self.burst = burst
        self.timeout = timeout
        self.max_retries = max_retries
        self.browser_profile = browser_profile if browser_profile in BROWSER_PROFILES else "chrome120"
        self.follow_redirects = follow_redirects
        self.verify_ssl = verify_ssl
        
        # 初始化 Token Bucket
        self.token_bucket = TokenBucket(rate=rate, burst=burst)
        
        # 代理配置
        self.proxy = proxy
        self.proxies = proxies or []
        self._proxy_index = 0
        
        # 请求头
        self.extra_headers = extra_headers or {}
        self._user_agent = None
        
        # 检查 curl_cffi
        if not CURL_CFFI_AVAILABLE:
            logger.warning(
                "curl_cffi 未安装，将使用 requests 库。"
                "建议安装: pip install curl_cffi"
            )
        
        logger.info(
            f"WebFetcher 初始化完成 | "
            f"限速: {rate} req/s | "
            f"Burst: {burst} | "
            f"代理: {self._get_proxy_info()}"
        )
        
    def _get_proxy_info(self) -> str:
        """获取代理信息"""
        if self.proxy:
            return f"单代理 {self.proxy}"
        elif self.proxies:
            return f"代理池 ({len(self.proxies)} 个)"
        return "无代理"
        
    def _get_user_agent(self) -> str:
        """获取 User-Agent"""
        if FAKE_UA_AVAILABLE:
            if self._user_agent is None:
                ua = UserAgent()
                self._user_agent = ua.random
            return self._user_agent
        else:
            return (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
            
    def _get_headers(self, url: str = None) -> Dict[str, str]:
        """
        生成请求头
        
        Args:
            url: 请求的 URL（用于生成 Referer）
        """
        headers = DEFAULT_HEADERS.copy()
        
        # 添加随机 User-Agent
        headers["User-Agent"] = self._get_user_agent()
        
        # 添加 Referer（如果提供了 URL）
        if url:
            parsed = urlparse(url)
            headers["Referer"] = f"{parsed.scheme}://{parsed.netloc}/"
            
        # 添加额外的请求头
        headers.update(self.extra_headers)
        
        return headers
        
    def _get_current_proxy(self) -> Optional[str]:
        """获取当前代理"""
        if self.proxy:
            return self.proxy
        elif self.proxies:
            proxy = self.proxies[self._proxy_index]
            
            return proxy
        return None
        
    def _rotate_proxy(self):
        """轮换代理"""
        if self.proxies:
            self._proxy_index = (self._proxy_index + 1) % len(self.proxies)
            
    def _extract_text(self, html: str) -> str:
        """
        从 HTML 中提取文本内容
        
        Args:
            html: HTML 字符串
            
        Returns:
            str: 提取的文本
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # 移除脚本和样式
        for script in soup(["script", "style", "noscript"]):
            script.decompose()
            
        # 获取文本
        text = soup.get_text(separator='\n', strip=True)
        
        # 清理空行
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        return '\n'.join(lines)
        
    @contextmanager
    def _get_session(self):
        """
        获取 HTTP Session
        
        使用上下文管理器确保资源正确释放
        """
        if CURL_CFFI_AVAILABLE and curl_requests:
            session = curl_requests.Session(
                impersonate=self.browser_profile,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
            try:
                yield session
            finally:
                session.close()
        else:
            # 使用标准 requests 库
            with requests.Session() as session:
                yield session
            
    def fetch(
        self,
        url: str,
        method: str = "GET",
        data: Any = None,
        headers: Dict[str, str] = None,
        proxy: str = None,
        timeout: int = None,
        retries: int = None,
    ) -> FetchResult:
        """
        抓取网页
        
        Args:
            url: 目标 URL
            method: 请求方法（GET/POST）
            data: 请求数据（POST 请求体或参数）
            headers: 额外的请求头
            proxy: 覆盖默认代理
            timeout: 覆盖默认超时
            retries: 当前重试次数
            
        Returns:
            FetchResult: 抓取结果
        """
        retries = retries if retries is not None else self.max_retries
        timeout = timeout or self.timeout
        request_headers = self._get_headers(url)
        
        # 合并额外请求头
        if headers:
            request_headers.update(headers)
            
        # 获取代理
        current_proxy = proxy or self._get_current_proxy()
        
        # Token Bucket 限速
        self.token_bucket.acquire()
        
        start_time = time.time()
        
        for attempt in range(retries):
            try:
                with self._get_session() as session:
                    # 设置请求头
                    for key, value in request_headers.items():
                        session.headers[key] = value
                        
                    # 发送请求
                    if method.upper() == "POST":
                        response = session.post(
                            url,
                            data=data,
                            proxies={"http": current_proxy, "https": current_proxy} if current_proxy else None,
                            timeout=timeout,
                            allow_redirects=self.follow_redirects,
                        )
                    else:
                        response = session.get(
                            url,
                            params=data,
                            proxies={"http": current_proxy, "https": current_proxy} if current_proxy else None,
                            timeout=timeout,
                            allow_redirects=self.follow_redirects,
                        )
                        
                    elapsed = time.time() - start_time
                    
                    # 提取 cookies
                    cookies = {}
                    if hasattr(response, 'cookies'):
                        cookies = {k: v for k, v in response.cookies.items()}
                        
                    # 获取内容
                    content = response.text
                    
                    # 提取文本
                    text = self._extract_text(content)
                    
                    # 构建结果
                    result = FetchResult(
                        url=url,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        content=content,
                        text=text,
                        cookies=cookies,
                        elapsed=elapsed,
                        is_success=response.ok,
                    )
                    
                    logger.info(
                        f"请求成功: {url} | "
                        f"状态: {response.status_code} | "
                        f"耗时: {elapsed:.2f}s | "
                        f"代理: {current_proxy or '无'}"
                    )
                    
                    return result
                    
            except Exception as e:
                elapsed = time.time() - start_time
                error_msg = str(e)
                
                logger.warning(
                    f"请求失败 (尝试 {attempt + 1}/{retries}): {url} | "
                    f"错误: {error_msg}"
                )
                
                # 如果还有重试次数
                if attempt < retries - 1:
                    # 轮换代理
                    self._rotate_proxy()
                    current_proxy = self._get_current_proxy()
                    
                    # 指数退避
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
                    continue
                    
                # 返回错误结果
                return FetchResult(
                    url=url,
                    error=error_msg,
                    elapsed=elapsed,
                    is_success=False,
                )
                
        # 理论上不会到达这里
        return FetchResult(
            url=url,
            error="最大重试次数耗尽",
            elapsed=time.time() - start_time,
            is_success=False,
        )
        
    def fetch_multiple(
        self,
        urls: List[str],
        method: str = "GET",
        data: Any = None,
        max_concurrent: int = 5,
    ) -> List[FetchResult]:
        """
        批量抓取多个 URL
        
        Args:
            urls: URL 列表
            method: 请求方法
            data: 请求数据
            max_concurrent: 最大并发数（注意：这里是串行执行，只是限制同时在桶中的请求数）
            
        Returns:
            List[FetchResult]: 结果列表
        """
        results = []
        
        for url in urls:
            result = self.fetch(url, method, data)
            results.append(result)
            
        return results
        
    def head(self, url: str, **kwargs) -> FetchResult:
        """
        发送 HEAD 请求（只获取响应头）
        """
        return self.fetch(url, method="HEAD", **kwargs)
        
    def post(self, url: str, data: Any = None, **kwargs) -> FetchResult:
        """
        发送 POST 请求
        """
        return self.fetch(url, method="POST", data=data, **kwargs)
        
    @property
    def total_requests(self) -> int:
        """获取 Token Bucket 已发出的请求数（估算）"""
        return self.burst - int(self.token_bucket.tokens)


# ============================================================================
# 便捷函数
# ============================================================================

def quick_fetch(url: str, **kwargs) -> str:
    """
    快速抓取网页（便捷函数）
    
    Args:
        url: 目标 URL
        **kwargs: WebFetcher 的其他参数
        
    Returns:
        str: 抓取结果
    """
    fetcher = WebFetcher(**kwargs)
    result = fetcher.fetch(url)
    if result.is_success:
        print(f"状态码: {result.status_code}")
        print(f"内容长度: {len(result.content)} 字符")
        return result.text
    else:
        print("web fetch failed")
    
    return ""



def fetch_and_parse(url: str, selector: str, **kwargs) -> List[str]:
    """
    快速抓取并提取指定元素文本
    
    Args:
        url: 目标 URL
        selector: CSS 选择器
        **kwargs: WebFetcher 的其他参数
        
    Returns:
        List[str]: 提取的文本列表
    """
    result = quick_fetch(url, **kwargs)
    if result.is_success:
        return result.get_text_content(selector).split('\n')
    return []


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    # 示例 1: 基本使用
    print("=" * 60)
    print("示例 1: 基本抓取")
    print("=" * 60)
    
    fetcher = WebFetcher(rate=2, burst=5)
    result = fetcher.fetch("https://github.com/goog?tab=repositories")
    
    if result.is_success:
        print(f"状态码: {result.status_code}")
        print(f"内容长度: {len(result.content)} 字符")
        print(f"提取文本前200字:\n{result.text}...")
    else:
        print(f"抓取失败: {result.error}")
        
    print()
    result = quick_fetch("https://github.com/goog?tab=repositories")
    print(f"my fetch: {result}")
    
    # 示例 2: 带代理抓取
    print("=" * 60)
    print("示例 2: 带代理抓取（需要配置有效代理）")
    print("=" * 60)
    
    # fetcher = WebFetcher(proxy="http://127.0.0.1:7890")
    # result = fetcher.fetch("https://httpbin.org/ip")
    # print(f"代理IP响应: {result.json_data}")
    
    # 示例 3: POST 请求
    print("=" * 60)
    print("示例 3: POST 请求")
    print("=" * 60)
    
    result = fetcher.post(
        "https://httpbin.org/post",
        data={"key": "value", "number": 42}
    )
    
    if result.is_success:
        print(f"POST 响应: {result.json_data}")
    else:
        print(f"POST 失败: {result.error}")
        
    print()
    
    # 示例 4: 使用 CSS 选择器提取内容
    print("=" * 60)
    print("示例 4: CSS 选择器提取")
    print("=" * 60)
    
    result = fetcher.fetch("https://httpbin.org/html")
    
    if result.is_success:
        # 查找所有标题
        titles = result.select("h1, h2, h3")
        for title in titles:
            print(f"标题: {title.get_text(strip=True)}")
            
    print()
    
    # 示例 5: 批量抓取
    print("=" * 60)
    print("示例 5: 批量抓取")
    print("=" * 60)
    
    urls = [
        "https://httpbin.org/headers",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/get",
    ]
    
    results = fetcher.fetch_multiple(urls)
    
    for i, res in enumerate(results):
        status = "✓" if res.is_success else "✗"
        print(f"{status} {urls[i]}: {res.status_code}")
        
    print()
    
    # 示例 6: 快速抓取函数
    print("=" * 60)
    print("示例 6: 快速抓取")
    print("=" * 60)
    
    result = quick_fetch(
        "https://httpbin.org/json",
        rate=1,
        burst=2,
    )
    
    if result.is_success:
        print(f"JSON 数据: {result.json_data}")
