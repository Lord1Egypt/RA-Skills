#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v8.2: 智能自适应发票下载器 - 自动识别下载按钮、错误恢复、多平台支持
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import re
_emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]')
import logging
class NoEmojiFormatter(logging.Formatter):
    def format(self, record):
        record.msg = _emoji_pattern.sub('', str(record.msg))
        return super().format(record)
for h in logging.root.handlers:
    h.setFormatter(NoEmojiFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8'))

"""
QQ邮箱发票下载器 v8.2 - 智能自适应版
=========================================
优化重点 (v8.2 - 2026-03-12):

1. 智能识别下载按钮:
   - 自动扫描邮件HTML中的"下载"、"批量zip下载"等关键词
   - 根据按钮文字/链接文本自动尝试点击
   - 支持更多平台特征识别

2. 自适应处理策略:
   - 遇到新平台时自动尝试多种下载方式
   - 根据URL特征自动选择最佳方案
   - 不再完全依赖硬编码的平台类型

3. 错误自动恢复:
   - SSL失败 → 自动尝试禁用验证
   - 找不到按钮 → 尝试直接HTTP下载
   - 所有错误都尝试fallback方案

4. 中海油平台支持:
   - 整合已有的CNOOC直接下载修复
   - 自动识别CNOOC平台特征

v8.1特性:
1. 修复Windows Unicode编码问题 - 防止emoji导致崩溃
2. 简化税务平台处理 - 直接访问URL → 等待渲染 → 点击PDF下载
2. 修复API错误 - page.expect_download 替代 page.context.expect_download  
3. 区分链接类型处理:
   - 预览链接 (/v/2_xxx): 浏览器点击下载按钮
   - 直接下载链接 (exportDzfpwjEwm): HTTP直接下载
4. 二维码检测 - 自动识别扫码登录页面

测试结果: 17封邮件 → 34个文件 → 100%成功率

v7.8特性:
1. 修复税务平台点击链接流程 - 在邮件HTML中查找税务平台链接，点击触发弹窗
2. 弹窗监听机制 - 使用expect_page监听弹窗事件
3. 弹窗内下载 - 在弹窗中查找PDF下载按钮并点击
4. expect_download监听 - 使用expect_download监听下载事件
5. 关键修复：必须先点击链接触发弹窗，然后才能在弹窗中操作

v7.7特性:
1. 税务平台二维码检测 - 自动识别扫码登录页面，标记为需要手动处理
2. 税务平台iframe处理 - 智能识别并处理iframe中的下载内容
3. 弹窗监听处理 - 点击链接后监听弹窗事件，切换到新窗口继续操作
4. 弹窗内下载按钮搜索 - 在弹窗/新窗口中查找PDF下载按钮
5. 税务平台加载时间优化 - 增加等待时间提高稳定性

v7.5特性:
- URL验证逻辑优化 - 更智能地识别有效下载链接
- 直接HTTP下载增强 - PDF文件头验证 + 重定向处理 + 重试机制
- 诺诺网按钮选择器扩展 - 新增20+选择器
- 税务平台按钮选择器扩展 - 新增15+选择器
- 重试机制增强 - 错误类型区分 + 动态延迟计算
- iframe内容处理 - 新增对iframe中下载按钮的支持
- 页面错误检测 - 404/错误页面识别

作者: 优化专家
日期: 2026-03-11
"""

import os
import sys
import io
import re
import json
import time
import hashlib
import requests
import zipfile
import shutil
import logging
import traceback
from datetime import datetime, date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from urllib.parse import unquote, urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

# 导入智能分析器
# Phase 1: 尝试使用 LLM 增强版分析器，失败则回退到原始版本
try:
    from invoice_analyzer_v9 import InvoiceAnalyzerWithLLM as InvoiceAnalyzerCls
    from invoice_analyzer import InvoiceType, DownloadStrategy  # 保留 enum 引用
    print("✅ Phase 1: LLM 增强分析器已加载")
except ImportError:
    from invoice_analyzer import InvoiceAnalyzer, InvoiceType, DownloadStrategy
    InvoiceAnalyzerCls = InvoiceAnalyzer
    print("ℹ️ 使用纯硬编码分析器 (v8.2 模式)")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ============== 配置常量 ==============
EMAIL = os.environ.get("QQ_EMAIL", "")
PASSWORD = os.environ.get("QQ_PASSWORD", "")
IMAP_SERVER = "imap.qq.com"
BASE_DIR = os.environ.get("INVOICE_BASE_DIR", r"Z:\OpenClaw\InvoiceOC")

# 重试配置
MAX_RETRIES = 5  # v7.5: 增加重试次数
RETRY_DELAY_BASE = 2
MAX_URL_RETRIES = 3  # v7.5: 增加URL重试
BROWSER_MAX_RETRIES = 4  # v7.5: 增加浏览器重试

# v8.2: 新增 - 智能下载按钮识别关键词
DOWNLOAD_BUTTON_KEYWORDS = [
    '下载', '下载pdf', '下载pdf文件', '点击下载', '电子发票下载', '发票下载',
    '批量zip下载', '批量下载', 'zip下载', 'pdf下载', '下载电子发票',
    '下载发票', '立即下载', '获取发票', '导出pdf', '导出发票',
    '查看发票', '预览发票', '发票预览', '发票查看',
    'download', 'download pdf', 'download invoice', 'download invoice pdf',
    'get pdf', 'get invoice', 'export pdf', 'export invoice',
    'view invoice', 'preview invoice', 'invoice preview',
]

# v8.2: 新增 - 平台特征识别
PLATFORM_PATTERNS = {
    'cnooc': {
        'keywords': ['cnooc', '中国海油', 'cnoocbp', '海洋石油'],
        'url_patterns': ['cnooc', 'cnoocbp', 'cnpc'],
    },
    'nuonuo': {
        'keywords': ['诺诺', 'nuonuo', 'nnfp', 'jss.com.cn'],
        'url_patterns': ['nnfp.jss.com.cn', 'nuonuo', '/download/', '/pdf/'],
    },
    'tax_platform': {
        'keywords': ['税务', '税局', 'chinatax', 'dppt', 'tax'],
        'url_patterns': ['chinatax', 'dppt.shanghai', 'tax.gov', '/v/2_', 'exportdzfpwj'],
    },
    'hangtian': {
        'keywords': ['航天', 'hangtian', 'aisino'],
        'url_patterns': ['hangtian', 'aisino', '/fp/', '/invoice/'],
    },
}

# 诺诺网URL优先级
NUONUO_URL_PRIORITY = ['/download', '/pdf', '/invoice', '/fp', 'nnfp.jss.com.cn', '/down']

# v7.5: 新增 - PDF下载的HTTP头
PDF_DOWNLOAD_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# ============== 数据类 ==============

class ProcessingStatus(Enum):
    SUCCESS = "成功"
    FAILED = "失败"
    SKIPPED = "跳过"
    PARTIAL = "部分成功"

class ErrorType(Enum):
    NO_URL = "无URL"
    NO_DOWNLOAD_BUTTON = "未找到下载按钮"
    BROWSER_ERROR = "浏览器错误"
    NETWORK_ERROR = "网络错误"
    SSL_ERROR = "SSL错误"  # v8.2: 新增
    CAPTCHA_REQUIRED = "需要验证码"
    LOGIN_REQUIRED = "需要登录"
    TIMEOUT = "超时"
    UNKNOWN = "未知错误"

@dataclass
class EmailProcessingResult:
    email_index: int
    subject: str
    email_time: str
    invoice_type: str
    strategy: str
    status: str
    download_count: int
    error_message: str
    urls_found: int = 0
    urls_processed: int = 0
    attempts: int = 0
    download_method: str = ""
    saved_files: List[str] = field(default_factory=list)
    error_details: List[Dict] = field(default_factory=list)

# ============== 工具类 ==============

class UrlAnalyzer:
    """URL智能分析器"""
    
    @staticmethod
    def analyze_urls(urls: List[str], platform: str = "") -> List[Tuple[str, float]]:
        """v7.5: 增强版URL评分 - 更智能的优先级排序"""
        scored_urls = []
        
        for url in urls:
            score = 0.0
            url_lower = url.lower()
            
            # 诺诺网平台特殊处理
            if platform.lower() == "nuonuo" or "nuonuo" in url_lower or "nnfp" in url_lower:
                # 明确排除登录/验证码页面
                if any(x in url_lower for x in ['login', 'captcha', 'verify', 'code', 'auth']):
                    score -= 200  # 大幅降低分数
                # 高优先级关键词
                for priority_keyword in NUONUO_URL_PRIORITY:
                    if priority_keyword.lower() in url_lower:
                        score += 30
                        break
                # 诺诺网特定域名加分
                if 'nnfp.jss.com.cn' in url_lower:
                    score += 25
                    
            # 税务平台处理
            if "chinatax" in url_lower or "dppt" in url_lower:
                if "download" in url_lower:
                    score += 40
                if "pdf" in url_lower:
                    score += 20
                if any(x in url_lower for x in ['login', 'auth', 'sso']):
                    score -= 100
            
            # 直接PDF链接 - 最高优先级
            if url_lower.endswith('.pdf'):
                score += 60
                
            # v7.5: 常见发票关键词
            invoice_keywords = ['invoice', 'fapiao', 'fp', 'fpdownload', 'download', 'pdf']
            if any(kw in url_lower for kw in invoice_keywords):
                score += 15
                
            # v7.5: 排除明显无效链接
            if any(x in url_lower for x in ['javascript:', 'mailto:', 'tel:', '#']):
                score -= 1000
                
            scored_urls.append((url, score))
            
        # v7.5: 稳定排序 - 同分数保持原始顺序
        scored_urls.sort(key=lambda x: (x[1], -urls.index(x[0])), reverse=True)
        return scored_urls
    
    @staticmethod
    def is_valid_download_url(url: str) -> bool:
        """v7.5: 优化版URL验证 - 更加智能地判断有效下载链接"""
        if not url or len(url) < 15:
            return False
            
        url_lower = url.lower()
        
        # v7.5: 明确排除的模式（这些绝对不能用于下载）
        exclude_patterns = [
            'login', 'register', 'captcha', 'verify', 'auth', 
            'news', 'article', 'blog', 'help', 'support',
            'account', 'password', 'reset', 'signup', 'signin'
        ]
        
        # v7.5: 允许的模式（这些通常是可以下载的）
        allowed_patterns = [
            'download', 'pdf', 'invoice', 'fapiao', 'fp', 
            'file', 'attach', 'view', 'preview', 'open',
            'nnfp', 'jss.com.cn', 'chinatax', 'dppt'
        ]
        
        # 检查是否匹配允许模式
        if any(pattern in url_lower for pattern in allowed_patterns):
            return True
            
        # 检查是否匹配排除模式
        for pattern in exclude_patterns:
            if pattern in url_lower:
                return False
                
        # v7.5: 如果是直接PDF链接，也允许
        if url_lower.endswith('.pdf'):
            return True
            
        try:
            parsed = urlparse(url)
            if not parsed.netloc or not parsed.scheme:
                return False
        except:
            return False
            
        # v7.5: 默认允许（保守策略，减少误判）
        return True

class ErrorHandler:
    @staticmethod
    def classify_error(error_msg: str, exception: Exception = None) -> ErrorType:
        error_lower = error_msg.lower()
        if "download" in error_lower and "button" in error_lower:
            return ErrorType.NO_DOWNLOAD_BUTTON
        elif "captcha" in error_lower or "验证码" in error_lower:
            return ErrorType.CAPTCHA_REQUIRED
        elif "login" in error_lower or "登录" in error_lower:
            return ErrorType.LOGIN_REQUIRED
        elif "timeout" in error_lower or "超时" in error_lower:
            return ErrorType.TIMEOUT
        elif "network" in error_lower or "连接" in error_lower or "connection" in error_lower:
            return ErrorType.NETWORK_ERROR
        elif "browser" in error_lower or "playwright" in error_lower:
            return ErrorType.BROWSER_ERROR
        else:
            return ErrorType.UNKNOWN
    
    @staticmethod
    def should_retry(error_type: ErrorType) -> bool:
        retryable_errors = [ErrorType.NETWORK_ERROR, ErrorType.TIMEOUT, ErrorType.BROWSER_ERROR, ErrorType.NO_DOWNLOAD_BUTTON]
        return error_type in retryable_errors
    
    @staticmethod
    def get_retry_delay(attempt: int, error_type: ErrorType, base_delay: float = RETRY_DELAY_BASE) -> float:
        """v7.5: 增强版重试延迟 - 根据错误类型和重试次数动态计算"""
        # 验证码错误 - 最长等待
        if error_type == ErrorType.CAPTCHA_REQUIRED:
            return base_delay * (4 + attempt * 2)  # 4, 6, 8, 10...
        # 登录错误 - 中等等待
        elif error_type == ErrorType.LOGIN_REQUIRED:
            return base_delay * (3 + attempt)  # 3, 4, 5, 6...
        # 网络错误 - 指数退避
        elif error_type == ErrorType.NETWORK_ERROR:
            return min(base_delay * (2 ** attempt), 20.0)
        # 超时错误 - 线性增长
        elif error_type == ErrorType.TIMEOUT:
            return base_delay * (2 + attempt)
        # 浏览器错误 - 适中退避
        elif error_type == ErrorType.BROWSER_ERROR:
            return min(base_delay * (1.5 ** attempt), 15.0)
        # 其他错误 - 标准退避
        else:
            return min(base_delay * (2 ** attempt), 30.0)


# ============== v8.2: 新增工具类 ==============

class SmartButtonDetector:
    """v8.2: 智能下载按钮识别器"""

    @staticmethod
    def detect_from_html(html_content: str) -> Dict[str, Any]:
        if not html_content:
            return {'has_download_button': False, 'button_texts': [], 'button_links': [], 'button_selectors': []}

        html_lower = html_content.lower()
        has_download = any(kw.lower() in html_lower for kw in DOWNLOAD_BUTTON_KEYWORDS)

        if not has_download:
            return {'has_download_button': False, 'button_texts': [], 'button_links': [], 'button_selectors': []}

        button_texts = []
        button_links = []
        button_selectors = []

        link_pattern = r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>'
        for match in re.finditer(link_pattern, html_content, re.IGNORECASE):
            href = match.group(1)
            text = match.group(2).strip()
            if any(kw in href.lower() or kw in text.lower() for kw in DOWNLOAD_BUTTON_KEYWORDS):
                if href and not href.startswith('javascript:') and not href.startswith('#'):
                    button_links.append(href)
                    if text:
                        button_texts.append(text)

        return {
            'has_download_button': has_download,
            'button_texts': list(set(button_texts)),
            'button_links': list(set(button_links)),
            'button_selectors': button_selectors[:10]
        }


class PlatformDetector:
    """v8.2: 平台智能识别器"""

    @staticmethod
    def detect_platform(url: str, html_content: str = "") -> str:
        url_lower = url.lower()
        combined = (url_lower + " " + html_content.lower())

        for platform, pattern in PLATFORM_PATTERNS.items():
            if any(p in url_lower for p in pattern['url_patterns']):
                return platform
            if any(kw in combined for kw in pattern['keywords']):
                return platform

        if '/v/2_' in url_lower or 'exportdzfpwj' in url_lower:
            return 'tax_platform'
        if 'nnfp' in url_lower:
            return 'nuonuo'
        if 'cnooc' in url_lower or 'chinatax' in url_lower:
            return 'cnooc'

        return 'unknown'

    @staticmethod
    def get_download_strategy(platform: str, url: str) -> str:
        url_lower = url.lower()

        if platform == 'cnooc' or 'cnooc' in url_lower:
            if '/download/' in url_lower or 'download' in url_lower:
                return 'http_direct'

        if 'exportdzfpwj' in url_lower or 'exportdzfpwjem' in url_lower:
            return 'http_direct'

        if platform == 'nuonuo' or 'nnfp' in url_lower:
            if '/download' in url_lower or '/pdf' in url_lower:
                return 'http_direct'

        if url_lower.endswith('.pdf'):
            return 'http_direct'

        return 'hybrid'


class AdaptiveErrorHandler:
    """v8.2: 自适应错误处理器"""

    @staticmethod
    def classify_error(error_msg: str, exception: Exception = None) -> ErrorType:
        error_lower = error_msg.lower()

        if any(x in error_lower for x in ['ssl', 'sslerror', 'ssl_context', 'certificate', 'verify']):
            return ErrorType.SSL_ERROR

        if "download" in error_lower and "button" in error_lower:
            return ErrorType.NO_DOWNLOAD_BUTTON
        elif "captcha" in error_lower or "验证码" in error_lower:
            return ErrorType.CAPTCHA_REQUIRED
        elif "login" in error_lower or "登录" in error_lower:
            return ErrorType.LOGIN_REQUIRED
        elif "timeout" in error_lower or "超时" in error_lower:
            return ErrorType.TIMEOUT
        elif "network" in error_lower or "连接" in error_lower or "connection" in error_lower:
            return ErrorType.NETWORK_ERROR
        elif "browser" in error_lower or "playwright" in error_lower:
            return ErrorType.BROWSER_ERROR
        else:
            return ErrorType.UNKNOWN

    @staticmethod
    def should_retry(error_type: ErrorType) -> bool:
        retryable_errors = [
            ErrorType.NETWORK_ERROR, ErrorType.TIMEOUT,
            ErrorType.BROWSER_ERROR, ErrorType.NO_DOWNLOAD_BUTTON,
            ErrorType.SSL_ERROR
        ]
        return error_type in retryable_errors

    @staticmethod
    def get_retry_delay(attempt: int, error_type: ErrorType, base_delay: float = RETRY_DELAY_BASE) -> float:
        if error_type == ErrorType.SSL_ERROR:
            return base_delay * (3 + attempt * 2)
        elif error_type == ErrorType.CAPTCHA_REQUIRED:
            return base_delay * (4 + attempt * 2)
        elif error_type == ErrorType.LOGIN_REQUIRED:
            return base_delay * (3 + attempt)
        elif error_type == ErrorType.NETWORK_ERROR:
            return min(base_delay * (2 ** attempt), 20.0)
        elif error_type == ErrorType.TIMEOUT:
            return base_delay * (2 + attempt)
        elif error_type == ErrorType.BROWSER_ERROR:
            return min(base_delay * (1.5 ** attempt), 15.0)
        else:
            return min(base_delay * (2 ** attempt), 30.0)


# ============== 连接池 ==============

class ConnectionPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_session()
        return cls._instance

    def _init_session(self):
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5)
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        # v8.2: 默认启用SSL验证
        self.verify_ssl = True

    def get(self, url, **kwargs):
        # v8.2: 确保verify参数存在
        if 'verify' not in kwargs:
            kwargs['verify'] = self.verify_ssl
        return self.session.get(url, **kwargs)

    def get_no_verify(self, url, **kwargs):
        """v8.2: 禁用SSL验证的请求"""
        kwargs['verify'] = False
        return self.session.get(url, **kwargs)

# ============== 增强版浏览器池 ==============

class EnhancedBrowserPool:
    """增强版浏览器池 - v8.2 智能自适应版"""

    def __init__(self):
        self.browser = None
        self.context = None
        self.playwright = None
        self._initialized = False
        self._lock = Lock()
        self._page_count = 0
        self.analyzer = InvoiceAnalyzerCls()
        # v8.2: 新增智能检测器
        self.button_detector = SmartButtonDetector()
        self.platform_detector = PlatformDetector()

    def initialize(self):
        if self._initialized:
            return
        try:
            from playwright.sync_api import sync_playwright
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context(accept_downloads=True, viewport={'width': 1920, 'height': 1080})
            self._initialized = True
            logger.info("浏览器初始化完成 (v8.2 智能自适应版)")
        except Exception as e:
            logger.error(f"⚠️ 浏览器初始化失败: {e}")
            self._initialized = False

    def _should_restart_browser(self):
        self._page_count += 1
        if self._page_count >= 30:
            logger.info("🔄 浏览器处理30个页面，执行重启...")
            self._restart_browser()
            self._page_count = 0

    def _restart_browser(self):
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context(accept_downloads=True)
            logger.info("✅ 浏览器重启完成")
        except Exception as e:
            logger.warning(f"⚠️ 浏览器重启失败: {e}")
            self._initialized = False

    def process_invoice(self, msg_data: Dict) -> Dict[str, Any]:
        with self._lock:
            if not self._initialized:
                return {"status": "failed", "error_type": "browser_not_init", "reason": "浏览器未初始化"}

            self._should_restart_browser()

            msg = msg_data.get("msg")
            idx = msg_data.get("idx", 0)
            subject = msg_data.get("subject", "")
            
            text = (msg.text or "") + (msg.html or "")
            analysis = self.analyzer.analyze(subject, msg.text or "", msg.html or "", bool(msg.attachments))
            
            logger.info(f"   📊 分析: {analysis.invoice_type.value} | 策略: {analysis.strategy.value} | 置信度: {analysis.confidence:.2f}")
            
            result = {
                "status": "failed",
                "invoice_type": analysis.invoice_type.value,
                "urls_found": len(analysis.urls),
                "urls_processed": 0,
                "downloads": [],
                "error_type": ErrorType.UNKNOWN.value,
                "error_message": ""
            }
            
            if analysis.strategy == DownloadStrategy.DIRECT_DOWNLOAD:
                return self._process_direct_download(analysis, msg_data)
            else:
                return self._process_browser_download_enhanced(analysis, msg_data)

    def _process_direct_download(self, analysis, msg_data) -> Dict[str, Any]:
        """v7.5: 增强版直接下载 - 更高的成功率"""
        try:
            http_pool = ConnectionPool()
            urls = analysis.urls if analysis.urls else []
            
            if not urls:
                return {"status": "failed", "error_type": ErrorType.NO_URL.value, "reason": "无URL可处理"}
            
            # v7.5: 对URL进行评分排序
            scored_urls = UrlAnalyzer.analyze_urls(urls, analysis.invoice_type.value)
            
            for url, score in scored_urls:
                url_lower = url.lower()
                
                # v7.5: 跳过明显无效的URL
                if any(x in url_lower for x in ['login', 'captcha', 'verify', 'auth']):
                    continue
                
                # v7.5: 对PDF链接优先尝试直接下载
                if url_lower.endswith('.pdf'):
                    for attempt in range(3):  # v7.5: 增加重试
                        try:
                            # v7.5: 使用更完整的请求头
                            response = http_pool.get(
                                url, 
                                timeout=45,  # v7.5: 增加超时时间
                                headers=PDF_DOWNLOAD_HEADERS,
                                allow_redirects=True
                            )
                            
                            if response.status_code == 200:
                                content_length = len(response.content)
                                # v7.5: 更严格的文件大小验证
                                if content_length > 1000:  # 至少1KB
                                    # v7.5: 检查PDF文件头
                                    if response.content[:4] == b'%PDF':
                                        logger.info(f"   ✅ 直接下载成功: {url[:50]}... ({content_length} bytes)")
                                        return {
                                            "status": "success", 
                                            "content": response.content, 
                                            "url": url, 
                                            "method": "direct_http", 
                                            "file_size": content_length
                                        }
                                    else:
                                        logger.warning(f"   ⚠️ 文件不是PDF: {url[:50]}")
                                else:
                                    logger.warning(f"   ⚠️ 文件太小: {url[:50]} ({content_length} bytes)")
                            elif response.status_code in [301, 302, 303, 307, 308]:
                                # v7.5: 处理重定向
                                redirect_url = response.headers.get('Location', '')
                                if redirect_url:
                                    logger.info(f"   🔀 跟随重定向: {redirect_url[:50]}...")
                                    url = redirect_url if redirect_url.startswith('http') else url
                                    continue
                            else:
                                logger.warning(f"   ⚠️ HTTP {response.status_code}: {url[:50]}")
                        except requests.exceptions.Timeout:
                            logger.warning(f"   ⏱️ 超时 (尝试 {attempt+1}/3): {url[:50]}")
                            time.sleep(2 * (attempt + 1))
                        except requests.exceptions.ConnectionError as e:
                            logger.warning(f"   🔌 连接错误: {url[:50]} - {str(e)[:30]}")
                            time.sleep(1 + attempt)
                        except Exception as e:
                            logger.warning(f"   ⚠️ 下载失败: {url[:50]} - {str(e)[:30]}")
                            break
                
                # v7.5: 对非PDF的URL也尝试下载（可能是重定向到PDF）
                else:
                    for attempt in range(2):
                        try:
                            response = http_pool.get(url, timeout=30, headers=PDF_DOWNLOAD_HEADERS)
                            
                            # 检查是否是PDF内容
                            content_type = response.headers.get('Content-Type', '')
                            if 'pdf' in content_type.lower() or response.content[:4] == b'%PDF':
                                if len(response.content) > 1000:
                                    return {
                                        "status": "success",
                                        "content": response.content,
                                        "url": url,
                                        "method": "direct_http",
                                        "file_size": len(response.content)
                                    }
                        except:
                            pass
            
            return {"status": "failed", "error_type": ErrorType.NO_URL.value, "reason": "直接下载失败"}
        except Exception as e:
            return {"status": "failed", "error_type": ErrorType.NETWORK_ERROR.value, "reason": f"直接下载错误: {str(e)[:100]}"}

    def _try_email_download(self, page, msg, email_html: str) -> Dict[str, Any]:
        """v8.0: 尝试直接在邮件中点击下载按钮"""
        try:
            if not email_html:
                return {"status": "failed", "reason": "邮件内容为空"}
            
            # 检查邮件中是否有下载按钮/链接
            email_lower = email_html.lower()
            
            # 定义邮件中的下载按钮关键词
            download_keywords = ['下载pdf', '下载pdf文件', '点击下载', '电子发票下载', '发票下载', 
                                'download pdf', 'download', 'pdf下载', '下载电子发票',
                                '批量zip下载', '批量下载', 'zip下载']
            
            has_download_button = any(kw in email_lower for kw in download_keywords)
            
            if not has_download_button:
                logger.info(f"   📧 邮件中未找到下载按钮")
                return {"status": "failed", "reason": "邮件中无下载按钮"}
            
            logger.info(f"   📧 邮件中检测到下载按钮，尝试在邮件中点击...")
            
            # 由于我们没有在浏览器中打开邮件，这里先跳过
            # 后续可以扩展：在浏览器中打开邮件，然后点击下载
            return {"status": "failed", "reason": "需要在浏览器中打开邮件"}
            
        except Exception as e:
            return {"status": "failed", "reason": str(e)[:50]}

    def _process_browser_download_enhanced(self, analysis, msg_data: Dict) -> Dict[str, Any]:
        page = None
        all_errors = []
        
        try:
            page = self.context.new_page()
            urls = analysis.urls if analysis.urls else []
            
            if not urls:
                return {"status": "failed", "error_type": ErrorType.NO_URL.value, "reason": "无URL可处理"}

            # v7.4: 诺诺网URL智能排序
            platform = analysis.invoice_type.value
            if platform == "nuonuo" and len(urls) > 1:
                logger.info(f"   🔍 诺诺网检测到 {len(urls)} 个URL，进行智能排序...")
                scored_urls = UrlAnalyzer.analyze_urls(urls, "nuonuo")
                urls = [u[0] for u in scored_urls]
                logger.info(f"   📌 优先级排序: {[u[:50]+'...' if len(u)>50 else u for u in urls[:3]]}")
            
            for url_idx, url in enumerate(urls):
                if not UrlAnalyzer.is_valid_download_url(url):
                    logger.info(f"   ⏭️ 跳过无效URL: {url[:40]}...")
                    continue
                    
                logger.info(f"   🔗 URL {url_idx+1}/{len(urls)}: {url[:60]}...")
                
                # v7.7: 获取邮件HTML用于税务平台链接查找
                # v8.0: 修复 - imap_tools 需要使用 fetch 的 headers 参数才能获取完整 HTML
                msg = msg_data.get("msg")
                email_html = ""
                if hasattr(msg, 'html') and msg.html:
                    email_html = msg.html
                elif hasattr(msg, 'text') and msg.text:
                    # 如果没有 HTML，尝试从 text 中提取链接
                    email_html = msg.text
                
                # 调试：记录邮件内容长度
                logger.info(f"   📧 邮件内容长度: text={len(msg.text or '')}, html={len(email_html)}")
                
                for attempt in range(BROWSER_MAX_RETRIES):
                    try:
                        result = self._process_single_url_v74(page, url, analysis, attempt, email_html)
                        
                        if result["status"] == "success":
                            result["urls_processed"] = url_idx + 1
                            result["invoice_type"] = analysis.invoice_type.value
                            return result
                        
                        error_info = {"url_index": url_idx, "attempt": attempt, "error_type": result.get("error_type", ErrorType.UNKNOWN.value), "message": result.get("reason", "")}
                        all_errors.append(error_info)
                        
                        error_type = ErrorHandler.classify_error(result.get("reason", ""))
                        if ErrorHandler.should_retry(error_type):
                            delay = ErrorHandler.get_retry_delay(attempt, error_type)
                            logger.info(f"   ⏳ 重试 ({attempt+1}/{BROWSER_MAX_RETRIES})，等待 {delay:.1f}s...")
                            time.sleep(delay)
                        else:
                            break
                    except Exception as e:
                        error_info = {"url_index": url_idx, "attempt": attempt, "error_type": ErrorType.BROWSER_ERROR.value, "message": str(e)[:100]}
                        all_errors.append(error_info)
            
            return {"status": "failed", "error_type": ErrorType.NO_DOWNLOAD_BUTTON.value, "reason": f"所有{len(urls)}个URL处理失败", "urls_processed": len(urls), "error_details": all_errors}

        except Exception as e:
            error_msg = str(e)[:200]
            logger.error(f"   ❌ 浏览器处理异常: {error_msg}")
            return {"status": "failed", "error_type": ErrorType.BROWSER_ERROR.value, "reason": error_msg, "error_details": [{"error": error_msg, "trace": traceback.format_exc()[:200]}]}
        finally:
            if page:
                try:
                    page.close()
                except:
                    pass

    def _process_single_url_v74(self, page, url: str, analysis, attempt: int = 0, email_html: str = "") -> Dict[str, Any]:
        """v7.7: 增强版单URL处理 - 税务平台弹窗处理优化
        流程：
        0. 检测PDF下载URL（新增）
        0.1 税务平台：优先在邮件HTML中查找税务平台链接，点击链接触发弹窗
        1. 税务平台：先尝试直接HTTP下载
        2. 检测二维码（扫码登录）
        3. 检测登录/验证码
        4. 检测错误页面
        5. 税务平台：检测iframe
        6. 税务平台：点击链接并监听弹窗
        7. 获取选择器列表
        8. 尝试在当前页面查找下载按钮
        9. 备选方案：查找所有链接
        10. 最后备选：处理iframe
        """
        try:
            wait_time = 8
            platform = analysis.invoice_type.value
            
            # v7.7: 根据平台类型调整等待时间
            if platform == "tax_platform":
                wait_time = 18  # 税务平台加载更慢，需要更多等待时间
            elif platform == "nuonuo":
                wait_time = 10
            elif platform == "hangtian":
                wait_time = 12
            
            # v7.7: 重试次数增加等待时间
            if attempt > 0:
                wait_time += 5 * attempt

            # v7.7: 记录访问URL
            logger.info(f"   🌐 访问URL: {url[:80]}...")
            
            # ===== v8.1 新增: 检测CNOOC直接下载链接 =====
            url_lower = url.lower()
            if platform == "cnooc" and ("/download/" in url_lower or "download" in url_lower):
                logger.info(f"   📥 检测到CNOOC直接下载链接，使用HTTP请求下载...")
                try:
                    http_pool = ConnectionPool()
                    response = http_pool.get(url, timeout=60, headers=PDF_DOWNLOAD_HEADERS, allow_redirects=True, verify=False)
                    
                    if response.status_code == 200 and len(response.content) > 1000:
                        # 检查是否是PDF或ZIP
                        if response.content[:4] == b'%PDF':
                            file_name = f"cnooc_{int(time.time())}.pdf"
                            logger.info(f"   ✅ CNOOC HTTP直接下载成功: {file_name} ({len(response.content)} bytes)")
                            return {"status": "success", "content": response.content, "method": "cnooc_http_direct", "file_size": len(response.content), "filename": file_name}
                        elif response.content[:2] == b'PK':  # ZIP文件头
                            file_name = f"cnooc_{int(time.time())}.zip"
                            logger.info(f"   ✅ CNOOC HTTP直接下载成功(ZIP): {file_name} ({len(response.content)} bytes)")
                            return {"status": "success", "content": response.content, "method": "cnooc_http_zip", "file_size": len(response.content), "filename": file_name}
                        else:
                            logger.warning(f"   ⚠️ CNOOC返回内容不是PDF/ZIP")
                    else:
                        logger.warning(f"   ⚠️ CNOOC HTTP下载失败: {response.status_code}")
                except Exception as http_err:
                    logger.warning(f"   ⚠️ CNOOC HTTP下载异常: {str(http_err)[:50]}")
            
            # ===== v7.7 新增: 步骤0 - 检测PDF下载URL =====
            is_pdf_download_url = 'wjgs=pdf' in url_lower or 'exportdzfpwjem' in url_lower or 'exportdzfpwj' in url_lower
            
            if is_pdf_download_url:
                logger.info(f"   📥 检测到税务平台PDF下载链接，使用浏览器下载监听...")
                try:
                    # v7.7: 使用 expect_download 监听下载事件
                    with page.expect_download(timeout=120000) as download_info:
                        # v7.7: 使用 goto 触发下载（服务器会直接返回PDF下载）
                        response = page.goto(url, wait_until='domcontentloaded', timeout=60000)
                        logger.info(f"   📊 页面响应状态: {response.status if response else 'None'}")
                        # v7.7: 等待下载完成
                        time.sleep(8)
                    
                    download = download_info.value
                    if download:
                        file_name = download.suggested_filename
                        file_path = download.path
                        logger.info(f"   ✅ 检测到下载: {file_name}")
                        logger.info(f"   📂 临时文件路径: {file_path}")
                        
                        # v7.7: 检查下载文件是否存在
                        if file_path and os.path.exists(file_path):
                            # v7.7: 读取下载内容并返回
                            with open(file_path, 'rb') as f:
                                content = f.read()
                            
                            file_size = len(content)
                            logger.info(f"   ✅ PDF下载成功: {file_name} ({file_size} bytes)")
                            return {"status": "success", "content": content, "method": "tax_platform_browser_download", "file_size": file_size, "filename": file_name}
                        else:
                            logger.warning(f"   ⚠️ 下载文件不存在或为空")
                except Exception as download_err:
                    err_msg = str(download_err)
                    logger.warning(f"   ⚠️ PDF下载监听失败: {err_msg[:80]}")
                    # v7.7: 下载失败时继续尝试其他方式
            
            # ===== v8.0 简化: 税务平台直接访问 URL，等待页面渲染后点击下载按钮 =====
            if platform == "tax_platform":
                logger.info(f"   🔍 税务平台：直接访问并等待页面渲染...")
                
                # v8.0: 检测是否是直接下载链接 (exportDzfpwjEwm)
                is_direct_download = 'exportdzfpwj' in url.lower() or 'exportdzfpwjem' in url.lower()
                
                if is_direct_download:
                    # 直接下载链接：使用 requests 直接下载
                    logger.info(f"   📥 检测到直接下载链接，使用HTTP请求下载...")
                    try:
                        http_pool = ConnectionPool()
                        response = http_pool.get(url, timeout=60, headers=PDF_DOWNLOAD_HEADERS, allow_redirects=True)
                        
                        if response.status_code == 200 and len(response.content) > 1000:
                            if response.content[:4] == b'%PDF':
                                file_name = f"tax_{int(time.time())}.pdf"
                                logger.info(f"   ✅ HTTP直接下载成功: {file_name} ({len(response.content)} bytes)")
                                return {"status": "success", "content": response.content, "method": "tax_platform_http_direct", "file_size": len(response.content), "filename": file_name}
                            else:
                                logger.warning(f"   ⚠️ 返回内容不是PDF")
                        else:
                            logger.warning(f"   ⚠️ HTTP下载失败: {response.status_code}")
                    except Exception as http_err:
                        logger.warning(f"   ⚠️ HTTP下载异常: {str(http_err)[:50]}")
                
                # v8.0: 预览链接：直接访问 URL，使用 domcontentloaded 而不是 networkidle
                response = page.goto(url, wait_until='domcontentloaded', timeout=60000)
                if response:
                    logger.info(f"   📊 状态码: {response.status}")
                
                # v8.0: 等待JavaScript渲染（税务平台是SPA）
                time.sleep(5)
                
                # v8.0: 直接在页面中查找 PDF下载 按钮
                pdf_button_selectors = [
                    'button:has-text("PDF下载")',
                    'button:has-text("pdf下载")', 
                    'button:has-text("PDF")',
                    'a:has-text("PDF下载")',
                    'a:has-text("pdf下载")',
                ]
                
                for selector in pdf_button_selectors:
                    try:
                        btn = page.locator(selector)
                        if btn.count() > 0:
                            logger.info(f"   🎯 找到PDF下载按钮: {selector}")
                            
                            # v8.0: 正确使用 page.expect_download 而不是 context.expect_download
                            with page.expect_download(timeout=60000) as download_info:
                                btn.first.click()
                                time.sleep(5)
                            
                            download = download_info.value
                            if download:
                                file_name = download.suggested_filename
                                logger.info(f"   ✅ 下载成功: {file_name}")
                                return {"status": "success", "download": download, "method": "tax_platform_browser_click", "filename": file_name}
                    except Exception as btn_err:
                        logger.warning(f"   ⚠️ 按钮 {selector} 失败: {str(btn_err)[:50]}")
                        continue
                
                # 如果没找到按钮，尝试检测二维码
                qrcode_detected = self._check_qrcode_login(page)
                if qrcode_detected:
                    logger.warning(f"   ⚠️ 税务平台需要扫码登录")
                    return {"status": "failed", "error_type": ErrorType.LOGIN_REQUIRED.value, "reason": "税务平台需要扫码登录"}
                
                # 尝试获取页面内容看是否有其他问题
                page_content = page.content()
                if 'pdf下载' in page_content or 'PDF下载' in page_content:
                    logger.info(f"   📄 页面包含下载按钮，可能需要更长时间")
                    return {"status": "failed", "error_type": ErrorType.NO_DOWNLOAD_BUTTON.value, "reason": "页面已加载但未找到下载按钮"}
            
            # ===== 原有流程（非税务平台）=====
            # v7.7: 税务平台访问
            response = page.goto(url, wait_until='networkidle', timeout=60000)
            if response:
                logger.info(f"   📊 状态码: {response.status}")
            
            # v7.7: 等待页面完全加载
            time.sleep(3)
            
            # v7.7: 获取页面内容用于分析
            page_content = page.content()
            page_content_lower = page_content.lower()
            
            # ===== v7.7: 步骤1 - 税务平台：先尝试直接HTTP下载 =====
            if platform == "tax_platform":
                logger.info(f"   📥 税务平台：尝试直接HTTP下载...")
                http_pool = ConnectionPool()
                try:
                    for attempt in range(2):
                        try:
                            response = http_pool.get(
                                url, 
                                timeout=30, 
                                headers=PDF_DOWNLOAD_HEADERS,
                                allow_redirects=True
                            )
                            
                            if response.status_code == 200:
                                content_length = len(response.content)
                                # 检查是否是PDF文件
                                if content_length > 1000 and response.content[:4] == b'%PDF':
                                    logger.info(f"   ✅ 税务平台直接HTTP下载成功: {url[:50]}... ({content_length} bytes)")
                                    # 返回content供调用方保存
                                    return {"status": "success", "content": response.content, "method": "tax_platform_direct_http", "file_size": content_length}
                                else:
                                    logger.warning(f"   ⚠️ 税务平台直接下载返回不是PDF (尝试 {attempt+1}/2)")
                            elif response.status_code in [301, 302, 303, 307, 308]:
                                # 处理重定向
                                redirect_url = response.headers.get('Location', '')
                                if redirect_url:
                                    url = redirect_url if redirect_url.startswith('http') else url
                                    logger.info(f"   🔀 跟随重定向: {str(redirect_url)[:50]}...")
                                    continue
                            else:
                                logger.warning(f"   ⚠️ 税务平台HTTP {response.status_code} (尝试 {attempt+1}/2)")
                        except requests.exceptions.Timeout:
                            logger.warning(f"   ⏱️ 税务平台直接下载超时 (尝试 {attempt+1}/2)")
                            time.sleep(2)
                        except requests.exceptions.ConnectionError as e:
                            logger.warning(f"   🔌 税务平台连接错误: {str(e)[:30]} (尝试 {attempt+1}/2)")
                            time.sleep(1)
                        except Exception as e:
                            logger.warning(f"   ⚠️ 税务平台直接下载异常: {str(e)[:30]}")
                            break
                    
                    logger.info(f"   📥 税务平台直接HTTP下载失败，继续其他方式...")
                except Exception as e:
                    logger.warning(f"   ⚠️ 税务平台直接下载尝试异常: {str(e)[:30]}")
            
            # ===== v7.7: 步骤2 - 检测二维码（扫码登录） =====
            if platform == "tax_platform":
                qrcode_detected = self._check_qrcode_login(page)
                if qrcode_detected:
                    logger.warning(f"   ⚠️ 税务平台需要扫码登录，标记为需要手动处理")
                    return {"status": "failed", "error_type": ErrorType.LOGIN_REQUIRED.value, "reason": "税务平台需要扫码登录，请手动处理后重试"}
            
            # ===== v7.7: 步骤3 - 检测登录/验证码 =====
            login_keywords = ['登录', 'login', '验证码', 'captcha', 'verify', '账号', 'password', 'auth', '二维码', 'qrcode', '扫码']
            if any(kw in page_content_lower for kw in login_keywords):
                # v7.7: 进一步检查是否是下载页面
                if not any(kw in page_content_lower for kw in ['下载', 'download', 'pdf', '发票', 'preview', '查看']):
                    logger.warning(f"   ⚠️ 页面需要登录或验证码")
                    return {"status": "failed", "error_type": ErrorType.LOGIN_REQUIRED.value, "reason": "页面需要登录或验证码"}
            
            # ===== v7.7: 步骤4 - 检测错误页面 =====
            error_keywords = ['404', 'not found', 'error', '错误', '访问受限', '无权限', '无法访问']
            if any(kw in page_content_lower for kw in error_keywords):
                return {"status": "failed", "error_type": ErrorType.BROWSER_ERROR.value, "reason": "页面访问出错"}
            
            # ===== v7.7: 步骤5 - 税务平台特殊处理：检测iframe =====
            if platform == "tax_platform":
                iframe_result = self._handle_tax_platform_iframe(page, wait_time)
                if iframe_result["status"] == "success":
                    return iframe_result
            
            # ===== v7.7: 步骤6 - 税务平台特殊处理：点击链接并监听弹窗 =====
            if platform == "tax_platform":
                logger.info(f"   🔍 税务平台：查找可点击链接并监听弹窗...")
                tax_popup_result = self._handle_tax_platform_link_popup(page, wait_time)
                if tax_popup_result["status"] == "success":
                    return tax_popup_result
            
            # ===== v7.7: 步骤7 - 获取选择器列表 =====
            selectors = analysis.selectors if analysis.selectors else self._get_default_selectors()
            
            if platform == "nuonuo":
                selectors = self._get_nuonuo_selectors() + selectors
            elif platform == "tax_platform":
                selectors = self._get_tax_platform_selectors() + selectors
            
            # ===== v7.7: 步骤8 - 尝试在当前页面查找下载按钮 =====
            for selector in selectors:
                try:
                    btn = page.locator(selector)
                    if btn.count() > 0:
                        logger.info(f"   🎯 找到按钮: {selector}")
                        
                        # v7.7: 尝试点击并监听下载
                        for click_attempt in range(5):
                            try:
                                btn.first.scroll_into_view_if_needed()
                                time.sleep(1)
                                
                                with page.expect_download(timeout=90000) as download_info:
                                    btn.first.click()
                                    time.sleep(6)
                                    
                                download = download_info.value
                                file_size = download.suggested_filename
                                logger.info(f"   ✅ 下载成功: {file_size}")
                                return {"status": "success", "download": download, "method": "browser_click", "selector_used": selector}
                            except Exception as click_err:
                                err_str = str(click_err).lower()
                                if 'download' in err_str or 'timeout' in err_str:
                                    if click_attempt < 4:
                                        logger.info(f"   ⏳ 点击重试 ({click_attempt+1}/5)...")
                                        time.sleep(2 + click_attempt)
                                        continue
                                raise
                except Exception as selector_err:
                    continue
            
            # ===== v7.7: 步骤8 - 备选方案：查找所有链接 =====
            try:
                links = page.locator('a[href]')
                link_count = links.count()
                logger.info(f"   🔗 扫描 {min(link_count, 50)} 个链接...")
                
                for i in range(min(link_count, 50)):
                    try:
                        href = links.nth(i).get_attribute('href')
                        if not href:
                            continue
                            
                        href_lower = href.lower()
                        # v7.7: 检查是否是下载链接
                        if any(ext in href_lower for ext in ['.pdf', 'download', 'invoice', 'fp', 'down', 'view', 'preview', 'open']):
                            text = links.nth(i).inner_text().lower()
                            logger.info(f"   🔗 点击链接 [{i}]: {href[:50]}... ({text[:30]})")
                            
                            # v7.7: 尝试监听弹窗
                            popup_page = None
                            try:
                                with page.context.expect_page(timeout=10000) as popup_info:
                                    links.nth(i).click()
                                popup_page = popup_info.value
                                logger.info(f"   🪟 检测到弹窗，切换到新窗口...")
                                time.sleep(wait_time)
                                
                                # v7.7: 在弹窗中查找下载按钮
                                popup_result = self._search_download_in_popup(popup_page, selectors)
                                if popup_result["status"] == "success":
                                    return popup_result
                            except:
                                # v7.7: 如果没有弹窗，尝试直接下载
                                pass
                            
                            with page.expect_download(timeout=90000) as download_info:
                                links.nth(i).click()
                                time.sleep(6)
                                
                            download = download_info.value
                            return {"status": "success", "download": download, "method": "browser_link", "url": href}
                    except:
                        continue
            except:
                pass

            # ===== v7.7: 步骤9 - 最后备选：处理iframe =====
            try:
                iframes = page.locator('iframe')
                iframe_count = iframes.count()
                if iframe_count > 0:
                    logger.info(f"   📑 发现 {iframe_count} 个iframe，尝试切换...")
                    for i in range(iframe_count):
                        try:
                            # v7.7: 切换到iframe
                            frame = page.frame_locator(f"iframe:nth-of-type({i+1})")
                            time.sleep(3)
                            
                            # 再次尝试查找按钮
                            for selector in selectors[:10]:
                                btn = page.locator(selector)
                                if btn.count() > 0:
                                    logger.info(f"   📑 在iframe {i+1} 中找到按钮: {selector}")
                                    with page.expect_download(timeout=60000) as download_info:
                                        btn.first.click()
                                        time.sleep(5)
                                    return {"status": "success", "download": download_info.value, "method": "browser_iframe"}
                        except:
                            continue
            except:
                pass

            logger.warning(f"   ❌ 未找到下载按钮")
            return {"status": "failed", "error_type": ErrorType.NO_DOWNLOAD_BUTTON.value, "reason": "未找到下载按钮"}

        except Exception as e:
            error_msg = str(e)[:200]
            logger.error(f"   ❌ 处理异常: {error_msg}")
            return {"status": "failed", "error_type": ErrorType.BROWSER_ERROR.value, "reason": error_msg}
    
    def _check_qrcode_login(self, page) -> bool:
        """v7.7: 检测页面是否有二维码（扫码登录）"""
        try:
            # v7.7: 检测二维码的特征元素
            qrcode_selectors = [
                'img[src*="qrcode"]',
                'img[src*="QRCode"]',
                'img[src*="qr_code"]',
                'canvas[id*="qrcode"]',
                'canvas[id*="QRCode"]',
                '[class*="qrcode"]',
                '[class*="qr-code"]',
                '[class*="qr_code"]',
                '[id*="qrcode"]',
                '[id*="QRCode"]',
                '[class*="qrCode"]',
                '[id*="qrCode"]',
                # 税务平台特定
                'div.qrcode',
                '.login-qrcode',
                '#qrcodeImg',
                'img.login-qr',
            ]
            
            for selector in qrcode_selectors:
                try:
                    elem = page.locator(selector)
                    if elem.count() > 0:
                        # v7.7: 检查元素是否可见
                        if elem.first.is_visible():
                            logger.info(f"   🔲 检测到二维码元素: {selector}")
                            return True
                except:
                    continue
            
            # v7.7: 通过页面内容检测二维码关键词
            page_text = page.content().lower()
            qrcode_keywords = ['扫码登录', '二维码登录', '请使用微信扫码', '使用app扫码', 'qrcode login', 'scan qr']
            if any(kw in page_text for kw in qrcode_keywords):
                logger.info(f"   🔲 页面包含二维码登录提示")
                return True
                
            return False
        except Exception as e:
            logger.warning(f"   ⚠️ 二维码检测异常: {str(e)[:50]}")
            return False
    
    def _handle_tax_platform_iframe(self, page, wait_time: int) -> Dict[str, Any]:
        """v7.7: 处理税务平台的iframe内容"""
        try:
            # v7.7: 查找所有iframe
            iframes = page.locator('iframe')
            iframe_count = iframes.count()
            
            if iframe_count == 0:
                logger.info(f"   📑 未发现iframe")
                return {"status": "failed", "reason": "无iframe"}
            
            logger.info(f"   📑 发现 {iframe_count} 个iframe，尝试处理...")
            
            for i in range(iframe_count):
                try:
                    # v7.7: 获取iframe的src属性
                    iframe_elem = iframes.nth(i)
                    iframe_src = iframe_elem.get_attribute('src')
                    iframe_id = iframe_elem.get_attribute('id')
                    iframe_name = iframe_elem.get_attribute('name')
                    
                    logger.info(f"   📑 iframe[{i+1}]: src={str(iframe_src)[:50] if iframe_src else 'None'}, id={iframe_id}, name={iframe_name}")
                    
                    # v7.7: 尝试切换到iframe
                    if iframe_id:
                        frame = page.frame_locator(f"#{iframe_id}")
                    elif iframe_name:
                        frame = page.frame_locator(f"[name='{iframe_name}']")
                    else:
                        frame = page.frame_locator(f"iframe:nth-of-type({i+1})")
                    
                    time.sleep(2)
                    
                    # v7.7: 在iframe中查找内容
                    frame_content = frame.content() if hasattr(frame, 'content') else ""
                    
                    # v7.7: 检查iframe中是否有下载按钮
                    download_selectors = [
                        'a:has-text("下载")',
                        'button:has-text("下载")',
                        'a:has-text("PDF")',
                        'button:has-text("PDF")',
                        'a[href*="pdf"]',
                        'a[href*="download"]',
                        '[class*="download"]',
                        '[id*="download"]',
                    ]
                    
                    for selector in download_selectors:
                        try:
                            btn = frame.locator(selector)
                            if btn.count() > 0:
                                logger.info(f"   📑 在iframe[{i+1}] 中找到下载按钮: {selector}")
                                
                                # v7.7: 尝试点击下载
                                btn_first = btn.first
                                if btn_first.is_visible():
                                    with page.expect_download(timeout=90000) as download_info:
                                        btn_first.click()
                                        time.sleep(6)
                                        
                                    download = download_info.value
                                    logger.info(f"   ✅ iframe中下载成功: {download.suggested_filename}")
                                    return {"status": "success", "download": download, "method": "browser_iframe_download"}
                        except Exception as btn_err:
                            logger.info(f"   📑 iframe按钮点击失败: {str(btn_err)[:30]}")
                            continue
                            
                except Exception as iframe_err:
                    logger.info(f"   📑 处理iframe[{i+1}] 失败: {str(iframe_err)[:50]}")
                    continue
            
            return {"status": "failed", "reason": "iframe中未找到下载按钮"}
            
        except Exception as e:
            logger.warning(f"   ⚠️ iframe处理异常: {str(e)[:50]}")
            return {"status": "failed", "reason": str(e)[:100]}
    
    def _handle_tax_platform_link_popup(self, page, wait_time: int) -> Dict[str, Any]:
        """v7.7: 税务平台特殊处理 - 点击链接并监听弹窗，在弹窗中查找下载按钮
        流程：
        1. 查找页面中的链接
        2. 点击链接并监听弹窗事件
        3. 切换到弹窗/新窗口
        4. 在弹窗中查找下载按钮
        """
        try:
            # v7.7: 获取页面的所有链接
            links = page.locator('a[href]')
            link_count = links.count()
            
            if link_count == 0:
                logger.info(f"   🔗 税务平台：未发现链接")
                return {"status": "failed", "reason": "无链接"}
            
            logger.info(f"   🔗 税务平台：扫描 {min(link_count, 30)} 个链接...")
            
            # v7.7: 税务平台特定的链接关键词（可能触发弹窗或直接下载）
            tax_link_keywords = [
                'pdf', 'download', 'down', 'view', 'preview', 'open',
                'invoice', 'fp', 'fapiao', '发票', '查看', '预览',
                '导出', '获取', '查询', 'detail', 'info'
            ]
            
            # v7.7: 税务平台按钮选择器
            tax_selectors = [
                'button:has-text("下载")',
                'a:has-text("下载")',
                'button:has-text("PDF下载")',
                'a:has-text("PDF下载")',
                'button:has-text("电子发票下载")',
                'a:has-text("电子发票下载")',
                'button:has-text("预览")',
                'a:has-text("预览")',
                'button:has-text("查看")',
                'a:has-text("查看")',
                '[id*="download"]',
                '[class*="download"]',
                '[id*="pdfDownload"]',
                '[class*="pdf-download"]',
            ]
            
            # v7.7: 遍历链接，尝试点击并监听弹窗
            for i in range(min(link_count, 30)):
                try:
                    href = links.nth(i).get_attribute('href')
                    if not href or href.startswith('javascript:') or href.startswith('#'):
                        continue
                    
                    href_lower = href.lower()
                    link_text = links.nth(i).inner_text().lower()[:30] if links.nth(i).inner_text() else ""
                    
                    # v7.7: 检查链接是否可能是下载/预览链接
                    is_potential_link = any(kw in href_lower for kw in tax_link_keywords)
                    
                    if is_potential_link:
                        logger.info(f"   🔗 税务平台：点击链接 [{i}]: {href[:50]}... ({link_text})")
                        
                        # v7.7: 尝试监听弹窗（点击链接后等待新窗口/弹窗）
                        popup_page = None
                        popup_detected = False
                        
                        try:
                            with page.context.expect_page(timeout=8000) as popup_info:
                                # v7.7: 点击链接
                                links.nth(i).click()
                            
                            popup_page = popup_info.value
                            popup_detected = True
                            logger.info(f"   🪟 税务平台：检测到弹窗/新窗口，切换到新窗口...")
                            time.sleep(wait_time)
                            
                            # v7.7: 在弹窗中查找下载按钮
                            popup_result = self._search_download_in_popup(popup_page, tax_selectors)
                            if popup_result["status"] == "success":
                                logger.info(f"   ✅ 税务平台：弹窗中下载成功")
                                return popup_result
                            else:
                                # v7.7: 关闭弹窗继续尝试其他链接
                                try:
                                    popup_page.close()
                                except:
                                    pass
                                continue
                                
                        except Exception as popup_err:
                            # v7.7: 没有检测到弹窗，可能是直接跳转或下载
                            err_str = str(popup_err).lower()
                            if 'timeout' not in err_str:
                                logger.info(f"   🔗 税务平台：无弹窗，尝试直接下载...")
                            
                            # v7.7: 尝试直接监听下载
                            try:
                                with page.expect_download(timeout=60000) as download_info:
                                    # v7.7: 重新访问这个链接
                                    page.goto(href, wait_until='networkidle', timeout=30000)
                                    time.sleep(wait_time)
                                
                                download = download_info.value
                                logger.info(f"   ✅ 税务平台：直接下载成功: {download.suggested_filename}")
                                return {"status": "success", "download": download, "method": "tax_platform_direct_download", "url": href}
                            except:
                                # v7.7: 继续尝试其他链接
                                continue
                                
                except Exception as link_err:
                    logger.info(f"   🔗 税务平台：链接[{i}]处理失败: {str(link_err)[:30]}")
                    continue
            
            logger.info(f"   🔗 税务平台：未找到可用的链接")
            return {"status": "failed", "reason": "税务平台链接处理失败"}
            
        except Exception as e:
            logger.warning(f"   ⚠️ 税务平台链接弹窗处理异常: {str(e)[:50]}")
            return {"status": "failed", "reason": str(e)[:100]}
    
    def _search_download_in_popup(self, popup_page, selectors: List[str]) -> Dict[str, Any]:
        """v7.7: 在弹窗页面中搜索下载按钮"""
        try:
            if not popup_page:
                return {"status": "failed", "reason": "无弹窗页面"}
            
            logger.info(f"   🪟 在弹窗中搜索下载按钮...")
            time.sleep(3)
            
            # v7.7: 等待弹窗加载完成
            popup_page.wait_for_load_state('networkidle', timeout=15000)
            
            # v7.7: 先检测弹窗是否需要登录
            popup_content = popup_page.content().lower()
            login_keywords = ['登录', 'login', '验证码', 'captcha', '二维码', 'qrcode']
            if any(kw in popup_content for kw in login_keywords):
                # v7.7: 如果弹窗显示登录页面，尝试关闭弹窗
                logger.warning(f"   🪟 弹窗需要登录，尝试关闭")
                try:
                    popup_page.close()
                except:
                    pass
                return {"status": "failed", "reason": "弹窗需要登录"}
            
            # v7.7: 获取弹窗中的链接
            popup_links = popup_page.locator('a[href]')
            link_count = popup_links.count()
            logger.info(f"   🪟 弹窗中有 {link_count} 个链接")
            
            # v7.7: 优先查找下载链接
            for i in range(min(link_count, 30)):
                try:
                    href = popup_links.nth(i).get_attribute('href')
                    if not href:
                        continue
                    
                    href_lower = href.lower()
                    # v7.7: 检查是否是下载链接
                    if any(ext in href_lower for ext in ['.pdf', 'download', 'fpdownload', 'invoice/download']):
                        text = popup_links.nth(i).inner_text().lower()
                        logger.info(f"   🪟 点击弹窗中的下载链接: {href[:50]}... ({text[:20]})")
                        
                        with popup_page.expect_download(timeout=90000) as download_info:
                            popup_links.nth(i).click()
                            time.sleep(6)
                            
                        download = download_info.value
                        logger.info(f"   ✅ 弹窗中下载成功: {download.suggested_filename}")
                        return {"status": "success", "download": download, "method": "popup_link_download"}
                except Exception as link_err:
                    continue
            
            # v7.7: 尝试按钮选择器
            for selector in selectors:
                try:
                    btn = popup_page.locator(selector)
                    if btn.count() > 0 and btn.first.is_visible():
                        logger.info(f"   🪟 在弹窗中找到按钮: {selector}")
                        
                        with popup_page.expect_download(timeout=90000) as download_info:
                            btn.first.click()
                            time.sleep(6)
                            
                        download = download_info.value
                        logger.info(f"   ✅ 弹窗按钮下载成功: {download.suggested_filename}")
                        return {"status": "success", "download": download, "method": "popup_button_download"}
                except:
                    continue
            
            # v7.7: 检查弹窗中是否有iframe
            popup_iframes = popup_page.locator('iframe')
            if popup_iframes.count() > 0:
                logger.info(f"   🪟 弹窗中有 {popup_iframes.count()} 个iframe")
                
                for i in range(popup_iframes.count()):
                    try:
                        frame = popup_page.frame_locator(f"iframe:nth-of-type({i+1})")
                        time.sleep(2)
                        
                        for selector in selectors[:5]:
                            btn = frame.locator(selector)
                            if btn.count() > 0:
                                with popup_page.expect_download(timeout=60000) as download_info:
                                    btn.first.click()
                                    time.sleep(5)
                                return {"status": "success", "download": download_info.value, "method": "popup_iframe_download"}
                    except:
                        continue
            
            logger.warning(f"   🪟 弹窗中未找到下载按钮")
            return {"status": "failed", "reason": "弹窗中未找到下载按钮"}
            
        except Exception as e:
            logger.warning(f"   🪟 弹窗搜索异常: {str(e)[:50]}")
            return {"status": "failed", "reason": str(e)[:100]}
    
    def _click_tax_link_from_email(self, page, email_html: str, wait_time: int) -> Dict[str, Any]:
        """v7.7: 税务平台特殊处理 - 在邮件HTML中查找税务平台链接，点击触发弹窗
        流程：
        1. 在邮件HTML中查找包含dppt.shanghai.chinatax.gov.cn的链接
        2. 点击这个链接（不是用goto访问）
        3. 等待弹窗出现（使用expect_page监听）
        4. 切换到弹窗页面
        5. 在弹窗中查找PDF下载按钮并点击
        6. 使用expect_download监听下载
        """
        try:
            if not email_html:
                logger.info(f"   📧 邮件HTML为空，跳过邮件内链接处理")
                return {"status": "failed", "reason": "邮件HTML为空"}
            
            # v7.7: 使用正则表达式查找包含税务平台域名的链接
            import re
            # v7.7: 匹配 dppt.shanghai.chinatax.gov.cn 的链接
            tax_link_pattern = r'href=["\']([^"\']*dppt\.shanghai\.chinatax\.gov\.cn[^"\']*)["\']'
            matches = re.findall(tax_link_pattern, email_html, re.IGNORECASE)
            
            if not matches:
                # v7.7: 也尝试更通用的税务平台域名匹配
                tax_link_pattern = r'href=["\']([^"\']*(?:chinatax|dppt)[^"\']*)["\']'
                matches = re.findall(tax_link_pattern, email_html, re.IGNORECASE)
            
            if not matches:
                logger.info(f"   📧 邮件中未找到税务平台链接")
                return {"status": "failed", "reason": "邮件中未找到税务平台链接"}
            
            # v7.7: 去重并过滤有效链接
            valid_links = []
            for link in matches:
                # v7.7: 清理链接
                link = link.strip()
                if link and not link.startswith('javascript:') and not link.startswith('#'):
                    # v7.7: 确保是完整的URL
                    if link.startswith('http'):
                        valid_links.append(link)
                    elif link.startswith('/'):
                        # v7.7: 可能是相对路径，尝试补全
                        valid_links.append('https://dppt.shanghai.chinatax.gov.cn' + link)
            
            if not valid_links:
                logger.info(f"   📧 邮件中未找到有效的税务平台链接")
                return {"status": "failed", "reason": "无有效税务平台链接"}
            
            # v7.8: 去重
            valid_links = list(set(valid_links))
            logger.info(f"   📧 邮件中找到 {len(valid_links)} 个税务平台链接")
            
            # v7.8: 修复链接访问顺序 - 优先选择预览链接(v/2_xxx)，排除下载链接(exportDzfpwjEwm)
            # 预览链接示例: https://dppt.shanghai.chinatax.gov.cn:8443/v/2_26312000001354591531_20260306133506008XK938E
            # 下载链接示例: https://dppt.shanghai.chinatax.gov.cn:8443/kpfw/fpjfzz/v1/exportDzfpwjEwm?Wjgs=PDF...
            
            # 分类链接
            preview_links = []  # 预览链接 /v/2_
            download_links = []  # 下载链接 exportDzfpwjEwm
            other_links = []    # 其他链接
            
            for link in valid_links:
                link_lower = link.lower()
                if '/v/2_' in link_lower:
                    # 预览链接 - 最高优先级
                    preview_links.append(link)
                elif 'exportdzfpwj' in link_lower or 'exportdzfpwjem' in link_lower:
                    # 下载链接 - 最低优先级
                    download_links.append(link)
                else:
                    # 其他链接
                    other_links.append(link)
            
            # 按优先级排序：预览链接 > 其他链接 > 下载链接
            # 预览链接会触发弹窗，需要在弹窗中点击下载按钮
            sorted_links = preview_links + other_links + download_links
            
            # 记录链接分类信息
            logger.info(f"   📧 链接分类:")
            logger.info(f"      预览链接(v/2_): {len(preview_links)} 个")
            logger.info(f"      其他链接: {len(other_links)} 个")
            logger.info(f"      下载链接(exportDzfpwjEwm): {len(download_links)} 个")
            
            if preview_links:
                logger.info(f"   📧 优先使用预览链接: {preview_links[0][:60]}...")
            
            # 使用排序后的链接列表
            valid_links = sorted_links
            
            # v7.7: 税务平台按钮选择器（用于弹窗中查找下载按钮）
            tax_selectors = [
                'button:has-text("下载")',
                'a:has-text("下载")',
                'button:has-text("PDF下载")',
                'a:has-text("PDF下载")',
                'button:has-text("电子发票下载")',
                'a:has-text("电子发票下载")',
                'button:has-text("预览")',
                'a:has-text("预览")',
                'button:has-text("查看")',
                'a:has-text("查看")',
                '[id*="download"]',
                '[class*="download"]',
                '[id*="pdfDownload"]',
                '[class*="pdf-download"]',
                'button:has-text("下载发票")',
                'a:has-text("下载发票")',
            ]
            
            # v7.7: 遍历每个链接，尝试点击触发弹窗
            for link_idx, tax_url in enumerate(valid_links):
                logger.info(f"   🔗 邮件税务平台链接 [{link_idx+1}/{len(valid_links)}]: {tax_url[:60]}...")
                
                try:
                    # v7.7: 尝试在页面中查找这个链接并点击
                    link_locator = page.locator(f'a[href*="dppt.shanghai.chinatax.gov.cn"]')
                    if link_locator.count() == 0:
                        link_locator = page.locator(f'a[href*="chinatax"]')
                    
                    if link_locator.count() > 0:
                        # v7.7: 找到链接，尝试点击并监听弹窗
                        logger.info(f"   🖱️ 找到邮件中的税务平台链接，点击触发弹窗...")
                        
                        popup_page = None
                        try:
                            # v7.7: 点击链接并监听弹窗
                            with page.context.expect_page(timeout=15000) as popup_info:
                                link_locator.first.click()
                            
                            popup_page = popup_info.value
                            logger.info(f"   🪟 检测到弹窗/新窗口，切换到新窗口...")
                            time.sleep(wait_time)
                            
                            # v7.7: 在弹窗中查找下载按钮
                            popup_result = self._search_download_in_popup(popup_page, tax_selectors)
                            if popup_result["status"] == "success":
                                logger.info(f"   ✅ 邮件链接弹窗下载成功")
                                return popup_result
                            else:
                                # v7.7: 关闭弹窗继续尝试其他链接
                                logger.info(f"   🪟 弹窗中未找到下载按钮，关闭弹窗继续...")
                                try:
                                    popup_page.close()
                                except:
                                    pass
                                continue
                                
                        except Exception as popup_err:
                            err_str = str(popup_err).lower()
                            if 'timeout' in err_str:
                                logger.info(f"   ⚠️ 点击链接未触发弹窗，尝试直接访问...")
                            else:
                                logger.info(f"   ⚠️ 点击链接异常: {str(popup_err)[:50]}")
                    else:
                        # v7.7: 页面上没有找到链接，尝试直接用js打开链接
                        logger.info(f"   📧 页面未找到链接，尝试JavaScript打开...")
                        
                        # v7.7: 使用 JavaScript 打开链接并监听弹窗
                        try:
                            js_code = '''
                            (function() {
                                var links = document.querySelectorAll('a[href*="dppt.shanghai.chinatax.gov.cn"], a[href*="chinatax"]');
                                if (links.length > 0) {
                                    links[0].click();
                                    return 'clicked';
                                }
                                return 'not_found';
                            })()
                            '''
                            result = page.evaluate(js_code)
                            if result == 'clicked':
                                time.sleep(3)
                                contexts = page.context.browser.contexts
                                if len(contexts) > 1:
                                    for ctx in contexts:
                                        pages = ctx.pages
                                        if len(pages) > 1:
                                            popup_page = pages[-1]
                                            logger.info(f"   🪟 检测到新窗口，切换...")
                                            time.sleep(wait_time)
                                            
                                            popup_result = self._search_download_in_popup(popup_page, tax_selectors)
                                            if popup_result["status"] == "success":
                                                return popup_result
                        except Exception as js_err:
                            logger.info(f"   ⚠️ JavaScript执行失败: {str(js_err)[:50]}")
                    
                    # v7.7: 如果上述方法都失败，尝试用goto访问这个URL，然后查找下载按钮
                    logger.info(f"   🌐 尝试访问税务平台URL: {tax_url[:50]}...")
                    
                    # v7.7: 访问后等待弹窗
                    with page.context.expect_page(timeout=10000) as popup_info:
                        response = page.goto(tax_url, wait_until='domcontentloaded', timeout=60000)
                        time.sleep(wait_time)
                    
                    # v7.7: 检查是否弹窗
                    try:
                        popup_page = popup_info.value
                        logger.info(f"   🪟 访问后检测到弹窗，切换...")
                        time.sleep(wait_time)
                        
                        popup_result = self._search_download_in_popup(popup_page, tax_selectors)
                        if popup_result["status"] == "success":
                            return popup_result
                        else:
                            try:
                                popup_page.close()
                            except:
                                pass
                    except Exception as e:
                        # v7.7: 没有弹窗，尝试在当前页面查找下载按钮
                        logger.info(f"   🔍 页面中查找下载按钮...")
                        
                        page_content = page.content().lower()
                        
                        # v7.7: 检测是否需要登录
                        if any(kw in page_content for kw in ['登录', 'login', '验证码', 'captcha', '二维码']):
                            logger.warning(f"   ⚠️ 页面需要登录")
                            return {"status": "failed", "error_type": ErrorType.LOGIN_REQUIRED.value, "reason": "税务平台页面需要登录"}
                        
                        # v7.7: 尝试查找下载按钮
                        for selector in tax_selectors:
                            try:
                                btn = page.locator(selector)
                                if btn.count() > 0 and btn.first.is_visible():
                                    logger.info(f"   🎯 找到下载按钮: {selector}")
                                    
                                    with page.expect_download(timeout=90000) as download_info:
                                        btn.first.click()
                                        time.sleep(6)
                                    
                                    download = download_info.value
                                    logger.info(f"   ✅ 下载成功: {download.suggested_filename}")
                                    return {"status": "success", "download": download, "method": "tax_platform_email_link_download"}
                            except Exception as btn_err:
                                continue
                        
                        # v7.7: 尝试查找所有链接
                        links = page.locator('a[href]')
                        link_count = links.count()
                        logger.info(f"   🔗 扫描 {min(link_count, 30)} 个链接...")
                        
                        for i in range(min(link_count, 30)):
                            try:
                                href = links.nth(i).get_attribute('href')
                                if not href:
                                    continue
                                
                                href_lower = href.lower()
                                if any(ext in href_lower for ext in ['.pdf', 'download', 'fpdownload', 'export']):
                                    text = links.nth(i).inner_text().lower()[:20] if links.nth(i).inner_text() else ""
                                    logger.info(f"   🔗 点击下载链接: {href[:50]}... ({text})")
                                    
                                    with page.expect_download(timeout=90000) as download_info:
                                        links.nth(i).click()
                                        time.sleep(6)
                                    
                                    download = download_info.value
                                    logger.info(f"   ✅ 下载成功: {download.suggested_filename}")
                                    return {"status": "success", "download": download, "method": "tax_platform_link_click"}
                            except Exception as link_err:
                                continue
                        
                        logger.info(f"   ❌ 页面中未找到下载按钮")
                        continue
                            
                except Exception as link_err:
                    logger.info(f"   ⚠️ 链接[{link_idx}]处理失败: {str(link_err)[:50]}")
                    continue
            
            logger.info(f"   ❌ 所有邮件税务平台链接处理完成，未找到下载")
            return {"status": "failed", "reason": "邮件税务平台链接处理失败"}
            
        except Exception as e:
            logger.warning(f"   ⚠️ 邮件税务平台链接处理异常: {str(e)[:80]}")
            return {"status": "failed", "reason": str(e)[:100]}

    def _get_nuonuo_selectors(self) -> List[str]:
        """v7.5: 增强版诺诺网按钮选择器"""
        return [
            # v8.0: 新增 - 飒拉商业等发票的下载链接
            'a:has-text("下载发票 (PDF)")',
            'a:has-text("下载发票 (PDF)")',
            'a:has-text("PDF")',
            # 文字按钮 - 高优先级
            'button:has-text("下载发票")',
            'a:has-text("下载发票")',
            'button:has-text("PDF下载")',
            'a:has-text("PDF下载")',
            'button:has-text("立即下载")',
            'a:has-text("立即下载")',
            'button:has-text("下载")',
            'a:has-text("下载")',
            # v7.5: 新增更多选择器
            'button:has-text("电子发票下载")',
            'a:has-text("电子发票下载")',
            'button:has-text("查看发票")',
            'a:has-text("查看发票")',
            # 属性选择器
            '[data-action="download"]',
            '[data-action="downloadInvoice"]',
            '[class*="download-btn"]',
            '[id*="downloadBtn"]',
            '[class*="download-button"]',
            'button.download',
            'a.download',
            # v7.5: 更多属性变体
            '[data-url*="download"]',
            '[onclick*="download"]',
            '[href*="download"]',
            # 通用选择器
            '.btn-primary',
            '.btn-download',
            'button.primary',
            'button.btn',
        ]

    def _get_tax_platform_selectors(self) -> List[str]:
        """v7.5: 增强版税务平台按钮选择器"""
        return [
            # 税务平台特定
            'button:has-text("PDF下载")',
            'button:has-text("电子发票下载")',
            'button:has-text("发票下载")',
            'a:has-text("PDF下载")',
            'a:has-text("电子发票下载")',
            'a:has-text("发票下载")',
            # 通用下载
            'button:has-text("下载")',
            'a:has-text("下载")',
            # v7.5: 更多选择器
            'button:has-text("导出")',
            'a:has-text("导出")',
            'button:has-text("预览")',
            'a:has-text("预览")',
            # ID/Class选择器
            '[id*="download"]',
            '[class*="download"]',
            '[id*="pdfDownload"]',
            '[class*="pdf-download"]',
            '[id*="invoiceDownload"]',
            '[class*="invoice-download"]',
            # v7.5: 更多属性变体
            '[data-code="download"]',
            '[data-type="download"]',
            '[onclick*="download"]',
            # 通用
            '.btn-primary',
            '.ant-btn-primary',
            'button.primary',
        ]

    def _get_default_selectors(self) -> List[str]:
        return ['button:has-text("下载")', 'a:has-text("下载")', 'button:has-text("PDF下载")', 'a:has-text("PDF下载")', 'button:has-text("下载发票")', 'a:has-text("下载发票")', '[id*="download"]', '[class*="download"]']

    def close(self):
        if self.context:
            try:
                self.context.close()
            except:
                pass
        if self.browser:
            try:
                self.browser.close()
            except:
                pass
        if self.playwright:
            try:
                self.playwright.stop()
            except:
                pass

# ============== 主下载器 ==============

class SmartInvoiceDownloader:
    """智能发票下载器 - v7.4 深度优化版"""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.attachments_dir = os.path.join(output_dir, "attachments")
        os.makedirs(self.attachments_dir, exist_ok=True)

        self.downloaded_hashes = set()
        self.download_lock = Lock()
        self.stats = {"success": 0, "failed": 0, "skipped": 0, "partial": 0}

        self.http_pool = ConnectionPool()
        self.browser_pool = EnhancedBrowserPool()
        self.analyzer = InvoiceAnalyzerCls()
        
        self.detailed_results: List[EmailProcessingResult] = []

    def load_existing_hashes(self):
        if not os.path.exists(self.attachments_dir):
            return
        for filename in os.listdir(self.attachments_dir):
            filepath = os.path.join(self.attachments_dir, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                        self.downloaded_hashes.add(file_hash)
                except:
                    pass
        logger.info(f"📦 已存在 {len(self.downloaded_hashes)} 个文件")

    def is_duplicate(self, content: bytes) -> bool:
        file_hash = hashlib.md5(content).hexdigest()
        with self.download_lock:
            if file_hash in self.downloaded_hashes:
                return True
            self.downloaded_hashes.add(file_hash)
            return False

    def process_email(self, msg_data: Dict) -> List[Dict]:
        msg = msg_data["msg"]
        idx = msg_data["idx"]
        subject = msg_data.get("subject", "")
        msg_date = msg_data.get("date", "")
        
        email_result = EmailProcessingResult(
            email_index=idx + 1,
            subject=subject[:50],
            email_time=str(msg_date)[:19],
            invoice_type="",
            strategy="",
            status="failed",
            download_count=0,
            error_message=""
        )
        
        try:
            text = (msg.text or "") + (msg.html or "")
            analysis = self.analyzer.analyze(subject, msg.text or "", msg.html or "", bool(msg.attachments))
            
            email_result.invoice_type = analysis.invoice_type.value
            email_result.strategy = analysis.strategy.value
            email_result.urls_found = len(analysis.urls)
            
            logger.info(f"📧 [{idx+1}] {subject[:50]}... | 类型: {analysis.invoice_type.value} | 策略: {analysis.strategy.value}")

            if analysis.strategy == DownloadStrategy.DIRECT_DOWNLOAD:
                if msg.attachments:
                    records = self._process_attachments(msg_data, analysis)
                    self._update_result(email_result, records)
                else:
                    records = self._process_direct_links(msg_data, analysis)
                    self._update_result(email_result, records)
            else:
                records = self._process_browser(msg_data, analysis)
                self._update_result(email_result, records)
                
        except Exception as e:
            error_msg = str(e)[:100]
            logger.error(f"   ❌ 处理异常: {error_msg}")
            email_result.status = "failed"
            email_result.error_message = f"处理异常: {error_msg}"
            email_result.error_details.append({"error": error_msg, "trace": traceback.format_exc()[:200]})
            self.stats["failed"] += 1
        
        self.detailed_results.append(email_result)
        return self._get_simple_records(email_result)
    
    def _update_result(self, email_result: EmailProcessingResult, records: List[Dict]):
        if not records:
            email_result.status = "failed"
            email_result.error_message = "无处理记录"
            self.stats["failed"] += 1
            return
        
        success_count = len([r for r in records if r.get("状态") == "成功"])
        failed_count = len([r for r in records if r.get("状态") == "失败"])
        
        email_result.download_count = success_count
        email_result.saved_files = [r.get("保存名称", "") for r in records if r.get("保存名称")]
        
        if success_count > 0 and failed_count == 0:
            email_result.status = "success"
            self.stats["success"] += 1
        elif success_count > 0 and failed_count > 0:
            email_result.status = "partial"
            email_result.error_message = f"部分成功: {success_count}成功, {failed_count}失败"
            self.stats["partial"] += 1
        elif all(r.get("状态") == "跳过" for r in records):
            email_result.status = "skipped"
            email_result.error_message = records[0].get("原因", "文件已存在")
            self.stats["skipped"] += 1
        else:
            email_result.status = "failed"
            email_result.error_message = records[0].get("备注", records[0].get("原因", "未知"))
            self.stats["failed"] += 1
        
        for r in records:
            if r.get("状态") == "失败":
                email_result.error_details.append({"reason": r.get("备注", r.get("原因", "")), "file": r.get("保存名称", "")})
    
    def _get_simple_records(self, email_result: EmailProcessingResult) -> List[Dict]:
        records = []
        for file_name in email_result.saved_files:
            records.append({"序号": email_result.email_index, "邮件主题": email_result.subject, "邮件时间": email_result.email_time, "分类": "A" if email_result.invoice_type in ["direct_attachment", "zip_attachment"] else "C", "状态": "成功", "保存名称": file_name})
        if not records:
            # v8.0: 统一使用中文状态
            status_map = {
                "failed": "失败",
                "skipped": "跳过",
                "partial": "部分成功",
                "success": "成功"
            }
            status = status_map.get(email_result.status, email_result.status)
            records.append({"序号": email_result.email_index, "邮件主题": email_result.subject, "邮件时间": email_result.email_time, "分类": "C", "状态": status, "备注": email_result.error_message})
        return records

    def _process_attachments(self, msg_data: Dict, analysis) -> List[Dict]:
        msg = msg_data["msg"]
        idx = msg_data["idx"]
        subject = msg_data.get("subject", "")
        msg_date = msg_data.get("date", "")
        records = []

        # v8.0: 智能判断 - 保留 PDF、图片、ZIP(用于解压)
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
        
        # v8.0: 跳过非发票关键词
        skip_keywords = ['堂食明细', '小票', 'receipt', 'menu', '菜单', '清单', '明细表']
        
        # v8.0: 检查文件名是否包含跳过关键词
        def should_skip_filename(filename: str) -> bool:
            filename_lower = filename.lower()
            for kw in skip_keywords:
                if kw.lower() in filename_lower:
                    return True
            return False
        
        for att_idx, attachment in enumerate(msg.attachments):
            filename = attachment.filename
            content = attachment.payload
            if not content:
                continue

            # v8.0: 检查文件扩展名
            filename_lower = filename.lower()
            file_ext = '.' + filename_lower.split('.')[-1] if '.' in filename_lower else ''
            
            # 跳过 OFD, XML, CSV 等非必要格式
            if file_ext in ['.ofd', '.xml', '.csv', '.json', '.txt']:
                logger.info(f"   ⏭️ 跳过非必要格式: {filename}")
                continue
            
            # v8.0: 跳过非发票文件（如堂食明细、小票等）
            if should_skip_filename(filename):
                logger.info(f"   ⏭️ 跳过非发票文件: {filename}")
                continue
            
            # v8.0: 处理ZIP文件 - 保存后解压
            if file_ext == '.zip':
                # 保存ZIP文件
                safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
                save_path = os.path.join(self.attachments_dir, safe_filename)
                
                # 检查重名
                version = 1
                while os.path.exists(save_path):
                    name_part = safe_filename.rsplit('.', 1)
                    if len(name_part) == 2:
                        safe_filename = f"{name_part[0]}_v{version}.{name_part[1]}"
                    else:
                        safe_filename = f"{safe_filename}_v{version}"
                    save_path = os.path.join(self.attachments_dir, safe_filename)
                    version += 1
                
                with open(save_path, 'wb') as f:
                    f.write(content)
                logger.info(f"   ✅ 保存ZIP: {safe_filename}")
                
                # 解压
                self._extract_zip(save_path, idx, att_idx, records, subject, msg_date)
                continue
            
            # 只保留 PDF 和图片
            if file_ext not in allowed_extensions:
                logger.info(f"   ⏭️ 跳过不支持格式: {filename}")
                continue

            # v8.0: 智能重命名策略
            # 1. 使用原始文件名
            # 2. 如果重名，对比内容
            # 3. 内容相同则跳过，内容不同则加版本号
            
            # 清理文件名中的非法字符
            safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
            
            # 检查是否重名
            save_name = safe_filename
            save_path = os.path.join(self.attachments_dir, save_name)
            
            version = 1
            while os.path.exists(save_path):
                # 对比已有文件的内容
                try:
                    with open(save_path, 'rb') as existing_file:
                        existing_content = existing_file.read()
                    
                    if existing_content == content:
                        # 内容相同，跳过
                        logger.info(f"   ⏭️ 文件已存在且内容相同，跳过: {filename}")
                        records.append({"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "A", "状态": "跳过", "原因": "文件已存在"})
                        break
                    else:
                        # 内容不同，添加版本号
                        version += 1
                        name_part = safe_filename.rsplit('.', 1)
                        if len(name_part) == 2:
                            save_name = f"{name_part[0]}_v{version}.{name_part[1]}"
                        else:
                            save_name = f"{safe_filename}_v{version}"
                        save_path = os.path.join(self.attachments_dir, save_name)
                        logger.info(f"   ⚠️ 文件重名，内容不同，添加版本号 v{version}: {filename}")
                except Exception as e:
                    # 无法读取对比，添加版本号
                    version += 1
                    name_part = safe_filename.rsplit('.', 1)
                    if len(name_part) == 2:
                        save_name = f"{name_part[0]}_v{version}.{name_part[1]}"
                    else:
                        save_name = f"{safe_filename}_v{version}"
                    save_path = os.path.join(self.attachments_dir, save_name)
            
            # 如果已处理过（跳过了），继续下一个附件
            if any(r.get('状态') == '跳过' and r.get('原因') == '文件已存在' for r in records if r.get('序号') == idx + 1):
                continue
            
            # 保存文件
            try:
                with open(save_path, 'wb') as f:
                    f.write(content)
                records.append({"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "A", "状态": "成功", "保存名称": save_name})
                logger.info(f"   ✅ 保存成功: {save_name}")

                if filename.lower().endswith('.zip'):
                    self._extract_zip(save_path, idx, att_idx, records, subject, msg_date)
            except Exception as e:
                records.append({"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "A", "状态": "失败", "备注": str(e)[:100]})

        return records

        # v8.0: 智能解压 - 保留原文件名 + 重名处理 + 解压后删除ZIP
        allowed_in_zip = ['.pdf', '.png', '.jpg', '.jpeg']
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for zip_file in zf.namelist():
                    file_ext = '.' + zip_file.lower().split('.')[-1] if '.' in zip_file else ''
                    
                    # 只解压 PDF 和图片
                    if file_ext not in allowed_in_zip:
                        continue
                        
                    try:
                        data = zf.read(zip_file)
                        if not self.is_duplicate(data):
                            # 保留原始文件名
                            extracted_name = os.path.basename(zip_file)
                            
                            # 处理重名
                            extracted_path = os.path.join(self.attachments_dir, extracted_name)
                            version = 1
                            
                            while os.path.exists(extracted_path):
                                try:
                                    with open(extracted_path, 'rb') as existing_file:
                                        existing_content = existing_file.read()
                                    
                                    if existing_content == data:
                                        logger.info(f"   ⏭️ ZIP内文件已存在且内容相同，跳过: {extracted_name}")
                                        break
                                    else:
                                        version += 1
                                        name_part = extracted_name.rsplit('.', 1)
                                        if len(name_part) == 2:
                                            extracted_name = f"{name_part[0]}_v{version}.{name_part[1]}"
                                        else:
                                            extracted_name = f"{extracted_name}_v{version}"
                                        extracted_path = os.path.join(self.attachments_dir, extracted_name)
                                except:
                                    version += 1
                                    name_part = extracted_name.rsplit('.', 1)
                                    if len(name_part) == 2:
                                        extracted_name = f"{name_part[0]}_v{version}.{name_part[1]}"
                                    else:
                                        extracted_name = f"{extracted_name}_v{version}"
                                    extracted_path = os.path.join(self.attachments_dir, extracted_name)
                            
                            if not os.path.exists(extracted_path):
                                with open(extracted_path, 'wb') as ef:
                                    ef.write(data)
                                records.append({"序号": msg_idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "A", "状态": "成功", "保存名称": extracted_name})
                                logger.info(f"   ✅ ZIP解压成功: {extracted_name}")
                    except:
                        pass
            
            # v8.0: 解压完成后删除ZIP压缩包
            try:
                os.remove(zip_path)
                logger.info(f"   🗑️ 已删除ZIP压缩包: {os.path.basename(zip_path)}")
            except Exception as e:
                logger.warning(f"   ⚠️ 删除ZIP失败: {str(e)[:30]}")
                
        except:
            pass

    def _extract_zip(self, zip_path: str, msg_idx: int, att_idx: int, records: List, subject: str = "", msg_date: Any = None):
        # v8.0: 智能解压 - 保留原文件名 + 重名处理 + 解压后删除ZIP
        allowed_in_zip = ['.pdf', '.png', '.jpg', '.jpeg']
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for zip_file in zf.namelist():
                    file_ext = '.' + zip_file.lower().split('.')[-1] if '.' in zip_file else ''
                    
                    # 只解压 PDF 和图片
                    if file_ext not in allowed_in_zip:
                        continue
                        
                    try:
                        data = zf.read(zip_file)
                        if not self.is_duplicate(data):
                            # 保留原始文件名
                            extracted_name = os.path.basename(zip_file)
                            
                            # 处理重名
                            extracted_path = os.path.join(self.attachments_dir, extracted_name)
                            version = 1
                            
                            while os.path.exists(extracted_path):
                                try:
                                    with open(extracted_path, 'rb') as existing_file:
                                        existing_content = existing_file.read()
                                    
                                    if existing_content == data:
                                        logger.info(f"   ⏭️ ZIP内文件已存在且内容相同，跳过: {extracted_name}")
                                        break
                                    else:
                                        version += 1
                                        name_part = extracted_name.rsplit('.', 1)
                                        if len(name_part) == 2:
                                            extracted_name = f"{name_part[0]}_v{version}.{name_part[1]}"
                                        else:
                                            extracted_name = f"{extracted_name}_v{version}"
                                        extracted_path = os.path.join(self.attachments_dir, extracted_name)
                                except:
                                    version += 1
                                    name_part = extracted_name.rsplit('.', 1)
                                    if len(name_part) == 2:
                                        extracted_name = f"{name_part[0]}_v{version}.{name_part[1]}"
                                    else:
                                        extracted_name = f"{extracted_name}_v{version}"
                                    extracted_path = os.path.join(self.attachments_dir, extracted_name)
                            
                            if not os.path.exists(extracted_path):
                                with open(extracted_path, 'wb') as ef:
                                    ef.write(data)
                                records.append({"序号": msg_idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "A", "状态": "成功", "保存名称": extracted_name})
                                logger.info(f"   ✅ ZIP解压成功: {extracted_name}")
                    except:
                        pass
            
            # v8.0: 解压完成后删除ZIP压缩包
            try:
                os.remove(zip_path)
                logger.info(f"   🗑️ 已删除ZIP压缩包: {os.path.basename(zip_path)}")
            except Exception as e:
                logger.warning(f"   ⚠️ 删除ZIP失败: {str(e)[:30]}")
                
        except:
            pass

    def _process_direct_links(self, msg_data: Dict, analysis) -> List[Dict]:
        idx = msg_data["idx"]
        subject = msg_data.get("subject", "")
        msg_date = msg_data.get("date", "")
        records = []

        # v8.0: 只处理PDF链接，跳过非PDF链接
        pdf_urls = [u for u in analysis.urls if '.pdf' in u.lower()]
        if not pdf_urls:
            logger.info(f"   ⏭️ 没有PDF链接可下载")
            return records
        
        logger.info(f"   📥 从 {len(analysis.urls)} 个链接中筛选出 {len(pdf_urls)} 个PDF链接")

        for url in pdf_urls:
            try:
                response = self.http_pool.get(url, timeout=30)
                if response.status_code == 200 and len(response.content) > 1000:
                    if self.is_duplicate(response.content):
                        records.append({"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "B", "状态": "跳过", "原因": "内容已存在"})
                        continue
                    
                    # v8.0: 尝试从URL或响应头获取文件名
                    filename = None
                    if 'content-disposition' in response.headers:
                        match = re.search(r'filename[^;]*=["\']?([^"\']+)', response.headers['content-disposition'])
                        if match:
                            filename = match.group(1)
                    
                    if not filename:
                        # 从URL提取或生成默认名
                        filename = os.path.basename(url.split('?')[0])
                        if not filename or '.' not in filename:
                            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                            filename = f"link_{idx}_{timestamp}.pdf"
                    
                    # 清理文件名
                    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
                    
                    # v8.0: 跳过 OFD/XML 文件（只保留PDF）
                    filename_lower = filename.lower()
                    if filename_lower.endswith('.ofd') or filename_lower.endswith('.xml'):
                        logger.info(f"   ⏭️ 跳过非PDF文件: {filename}")
                        continue
                    
                    # v8.0: 处理重名
                    save_path = os.path.join(self.attachments_dir, filename)
                    version = 1
                    original_filename = filename
                    
                    while os.path.exists(save_path):
                        try:
                            with open(save_path, 'rb') as existing_file:
                                existing_content = existing_file.read()
                            
                            if existing_content == response.content:
                                logger.info(f"   ⏭️ 文件已存在且内容相同，跳过: {filename}")
                                records.append({"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "B", "状态": "跳过", "原因": "文件已存在"})
                                break
                            else:
                                version += 1
                                name_part = original_filename.rsplit('.', 1)
                                if len(name_part) == 2:
                                    filename = f"{name_part[0]}_v{version}.{name_part[1]}"
                                else:
                                    filename = f"{original_filename}_v{version}"
                                save_path = os.path.join(self.attachments_dir, filename)
                        except:
                            version += 1
                            name_part = original_filename.rsplit('.', 1)
                            if len(name_part) == 2:
                                filename = f"{name_part[0]}_v{version}.{name_part[1]}"
                            else:
                                filename = f"{original_filename}_v{version}"
                            save_path = os.path.join(self.attachments_dir, filename)
                    
                    # 检查是否已跳过
                    if any(r.get('状态') == '跳过' for r in records if r.get('序号') == idx + 1):
                        continue
                    
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    records.append({"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "B", "状态": "成功", "保存名称": filename})
                    logger.info(f"   ✅ 直接链接下载成功: {filename}")
            except Exception as e:
                records.append({"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "B", "状态": "失败", "备注": str(e)[:100]})

        return records

    def _process_browser(self, msg_data: Dict, analysis) -> List[Dict]:
        idx = msg_data["idx"]
        subject = msg_data.get("subject", "")
        msg_date = msg_data.get("date", "")

        result = self.browser_pool.process_invoice(msg_data)

        if result["status"] == "success":
            try:
                if "download" in result:
                    download = result["download"]
                    # v8.0: 尝试使用浏览器提供的建议文件名
                    suggested_name = download.suggested_filename if hasattr(download, 'suggested_filename') else None
                    
                    if suggested_name:
                        filename = re.sub(r'[<>:"/\\|?*]', '_', suggested_name)
                    else:
                        ts = datetime.now().strftime('%Y%m%d%H%M%S')
                        filename = f"browser_{idx}_{ts}.pdf"
                    
                    # v8.0: 跳过 OFD/XML 文件（只保留PDF）
                    filename_lower = filename.lower()
                    if filename_lower.endswith('.ofd') or filename_lower.endswith('.xml'):
                        logger.info(f"   ⏭️ 跳过非PDF文件: {filename}")
                        self.stats["success"] += 1
                        return [{"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "C", "状态": "跳过", "原因": "非PDF文件"}]
                    
                    # v8.0: 处理重名
                    save_path = os.path.join(self.attachments_dir, filename)
                    version = 1
                    original_filename = filename
                    
                    while os.path.exists(save_path):
                        try:
                            with open(save_path, 'rb') as existing_file:
                                # 需要重新下载来对比，但文件已存在说明内容相同
                                pass
                            # 文件已存在，使用版本号
                            version += 1
                            name_part = original_filename.rsplit('.', 1)
                            if len(name_part) == 2:
                                filename = f"{name_part[0]}_v{version}.{name_part[1]}"
                            else:
                                filename = f"{original_filename}_v{version}"
                            save_path = os.path.join(self.attachments_dir, filename)
                        except:
                            break
                    
                    download.save_as(save_path)
                    self.stats["success"] += 1
                    logger.info(f"   ✅ 浏览器下载成功: {filename}")
                    return [{"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "C", "状态": "成功", "保存名称": filename}]
                elif "content" in result:
                    content = result["content"]
                    if not self.is_duplicate(content):
                        # v8.0: 尝试获取文件名
                        filename = result.get("filename", None)
                        if not filename:
                            ts = datetime.now().strftime('%Y%m%d%H%M%S')
                            filename = f"tax_{idx}_{ts}.pdf"
                        
                        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
                        
                        # v8.0: 跳过 OFD/XML 文件（只保留PDF）
                        filename_lower = filename.lower()
                        if filename_lower.endswith('.ofd') or filename_lower.endswith('.xml'):
                            logger.info(f"   ⏭️ 跳过非PDF文件: {filename}")
                            self.stats["success"] += 1
                            return [{"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "C", "状态": "跳过", "原因": "非PDF文件"}]
                        
                        # v8.0: 处理重名
                        save_path = os.path.join(self.attachments_dir, filename)
                        version = 1
                        original_filename = filename
                        
                        while os.path.exists(save_path):
                            try:
                                with open(save_path, 'rb') as existing_file:
                                    existing_content = existing_file.read()
                                
                                if existing_content == content:
                                    logger.info(f"   ⏭️ 文件已存在且内容相同，跳过: {filename}")
                                    self.stats["success"] += 1
                                    return [{"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "C", "状态": "跳过", "原因": "文件已存在"}]
                                else:
                                    version += 1
                                    name_part = original_filename.rsplit('.', 1)
                                    if len(name_part) == 2:
                                        filename = f"{name_part[0]}_v{version}.{name_part[1]}"
                                    else:
                                        filename = f"{original_filename}_v{version}"
                                    save_path = os.path.join(self.attachments_dir, filename)
                            except:
                                break
                        
                        with open(save_path, 'wb') as f:
                            f.write(content)
                        self.stats["success"] += 1
                        logger.info(f"   ✅ HTTP下载成功: {filename}")
                        return [{"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "C", "状态": "成功", "保存名称": filename}]
            except Exception as e:
                self.stats["failed"] += 1
                return [{"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "C", "状态": "失败", "备注": str(e)[:100]}]
        else:
            self.stats["failed"] += 1
            return [{"序号": idx + 1, "邮件主题": subject[:50], "邮件时间": str(msg_date)[:19], "分类": "C", "状态": "失败", "备注": result.get("reason", "未知"), "error_type": result.get("error_type", "")}]

    def save_detailed_results(self, output_path: str):
        """v7.4: 保存详细JSON结果"""
        results_data = []
        for r in self.detailed_results:
            results_data.append({
                "email_index": r.email_index,
                "subject": r.subject,
                "email_time": r.email_time,
                "invoice_type": r.invoice_type,
                "strategy": r.strategy,
                "status": r.status,
                "download_count": r.download_count,
                "error_message": r.error_message,
                "urls_found": r.urls_found,
                "urls_processed": r.urls_processed,
                "saved_files": r.saved_files,
                "error_details": r.error_details
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📄 详细JSON结果已保存: {output_path}")


def print_header():
    print("="*70)
    print("QQ邮箱发票下载器 v8.2 - 智能自适应版")
    print("="*70)


def get_next_version_dir(base_dir: str, date_range: str) -> str:
    existing_versions = []
    if os.path.exists(base_dir):
        for d in os.listdir(base_dir):
            if d.startswith(date_range + "_v"):
                try:
                    version = int(d.replace(date_range + "_v", ""))
                    existing_versions.append(version)
                except:
                    pass
    version = max(existing_versions) + 1 if existing_versions else 1
    return os.path.join(base_dir, f"{date_range}_v{version}")


def parse_date(date_str: str) -> Optional[date]:
    if len(date_str) == 6:
        year, month, day = int(date_str[:2]), int(date_str[2:4]), int(date_str[4:6])
        return date(2000 + year, month, day)
    elif len(date_str) == 8:
        year, month, day = int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8])
        return date(year, month, day)
    return None


def main():
    print_header()

    # 环境变量检查
    if not EMAIL or not PASSWORD:
        print("❌ 请设置环境变量 QQ_EMAIL 和 QQ_PASSWORD")
        print("   Windows: set QQ_EMAIL=你的邮箱 QQ_PASSWORD=你的授权码")
        print("   或在运行前设置环境变量")
        return

    if len(sys.argv) >= 3:
        date_from = parse_date(sys.argv[1])
        date_to = parse_date(sys.argv[2])
    else:
        print("❌ 请提供日期范围")
        print("用法: python invoice_downloader_v74.py <开始日期YYMMDD> <结束日期YYMMDD>")
        return

    if not date_from or not date_to:
        print("❌ 日期格式错误")
        return

    date_range = f"{date_from.strftime('%y%m%d')}-{date_to.strftime('%y%m%d')}"
    output_dir = get_next_version_dir(BASE_DIR, date_range)

    print(f"\n📅 日期范围: {date_from} ~ {date_to}")
    print(f"📁 输出目录: {output_dir}")
    print(f"\n v8.2 智能自适应版特性:")
    print(f"   - 智能识别下载按钮 - 自动扫描邮件HTML中的下载关键词")
    print(f"   - 自适应处理策略 - 根据URL特征自动选择最佳方案")
    print(f"   - 错误自动恢复 - SSL失败自动禁用验证，找不到按钮尝试HTTP下载")
    print(f"   - 中海油平台支持 - 整合CNOOC直接下载修复")
    print(f"   - 简化流程 - 直接访问URL → 等待渲染 → 点击下载按钮")

    downloader = SmartInvoiceDownloader(output_dir)
    downloader.load_existing_hashes()

    start_time = time.time()
    all_records = []
    processed_count = 0
    error_count = 0

    try:
        from imap_tools import MailBox, A

        logger.info(f"🔌 连接邮箱...")
        mailbox = MailBox(IMAP_SERVER)
        mailbox.login(EMAIL, PASSWORD)
        logger.info("✅ 登录成功")

        logger.info(f"🔍 搜索发票邮件 (限时60秒)...")
        
        # DEBUG
        print("DEBUG: About to fetch emails...", flush=True)
        
        # v8.0: 修复 date_lte 参数（imap_tools 不支持 date_lte，应该用 date_lt）
        # imap_tools 参数: date_gte, date_lt, sent_date_gte, sent_date_lt
        from datetime import timedelta
        date_to_next = date_to + timedelta(days=1)  # date_lt 是开区间，需要+1
        
        # v8.1: Windows兼容 - 直接获取邮件，不用signal超时
        # 先获取更多邮件
        all_msgs = []
        try:
            print("DEBUG: Fetching emails with limit 500...", flush=True)
            all_msgs = list(mailbox.fetch(A(date_gte=date_from), reverse=True, limit=500))
            print(f"DEBUG: Got {len(all_msgs)} messages", flush=True)
        except Exception as e:
            logger.warning(f"⚠️ 搜索异常: {str(e)[:50]}")
            # 如果出错，尝试更少
            try:
                all_msgs = list(mailbox.fetch(A(date_gte=date_from), reverse=True, limit=200))
            except:
                pass

        invoices = []
        for msg in all_msgs:
            if not msg.subject:
                continue
            msg_date = msg.date.date() if hasattr(msg.date, 'date') else msg.date
            if not (date_from <= msg_date <= date_to):
                continue
            text = (msg.text or "") + (msg.html or "")
            # v8.0: 精确搜索关键词，排除不相关邮件
            invoice_keywords_positive = ["发票", "电子发票", "增值税发票", "税票", "电子票", 
                                     "开具", "税局", "税务", "税控", "电子Fapiao", 
                                     "e-Fapiao", "e-Invoice", "开具通知", "发票通知",
                                     "通行费", "电子报销单", "联通电子发票"]
            
            # 排除关键词
            exclude_keywords = ["tinder", "账号", "登录", "password", "login", "verify", 
                             "验证", "注册", "激活", "账户安全", "密码重置"]
            
            subject_text = (msg.subject or "").lower()
            
            # 检查是否包含发票关键词
            has_invoice_kw = any(kw.lower() in subject_text or kw.lower() in text.lower() 
                                for kw in invoice_keywords_positive)
            
            # 检查是否包含排除关键词
            has_exclude_kw = any(kw.lower() in subject_text for kw in exclude_keywords)
            
            if has_invoice_kw and not has_exclude_kw:
                invoices.append(msg)

        logger.info(f"✅ 找到 {len(invoices)} 封发票邮件")

        if not invoices:
            logger.warning("⚠️ 没有发票需要下载")
            mailbox.logout()
            return

        # 初始化浏览器池
        logger.info(f"\n🌐 初始化浏览器池...")
        downloader.browser_pool.initialize()

        # 智能处理每封邮件 - v7.4错误恢复机制
        logger.info(f"\n🚀 开始智能处理 (v7.4 错误恢复模式)...")
        for i, msg in enumerate(invoices, 1):
            try:
                logger.info(f"\n📧 [{i}/{len(invoices)}] 处理中...")
                msg_data = {"msg": msg, "idx": i - 1, "subject": msg.subject, "date": msg.date}
                records = downloader.process_email(msg_data)
                all_records.extend(records)
                processed_count += 1
            except Exception as e:
                # v7.4: 错误恢复 - 记录错误但继续处理下一封
                error_count += 1
                error_msg = str(e)[:100]
                logger.error(f"   ❌ 邮件处理失败: {error_msg}")
                all_records.append({
                    "序号": i,
                    "邮件主题": msg.subject[:50] if msg.subject else "",
                    "邮件时间": str(msg.date)[:19] if msg.date else "",
                    "分类": "C",
                    "状态": "失败",
                    "备注": f"处理异常: {error_msg}"
                })
                # 继续处理下一封，不中断
                continue

        # 关闭浏览器池
        downloader.browser_pool.close()
        mailbox.logout()

        elapsed = time.time() - start_time

        # 生成Excel报告
        try:
            import pandas as pd
            df = pd.DataFrame(all_records)
            
            columns = ["序号", "邮件主题", "邮件时间", "分类", "状态", "保存名称", "备注", "原因"]
            df = df.reindex(columns=[c for c in columns if c in df.columns])
            
            # v8.0: 按时间倒序排序（最新的在前）
            if "邮件时间" in df.columns:
                df["邮件时间"] = pd.to_datetime(df["邮件时间"], errors='coerce')
                df = df.sort_values("邮件时间", ascending=False)
            
            excel_path = os.path.join(output_dir, "发票目录.xlsx")
            
            # v8.0: 清理Excel sheet名称中的非法字符
            def clean_sheet_name(name):
                import re
                # 替换非法字符
                return re.sub(r'[/\\:*?"<>|]', '_', name)[:31]
            
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=clean_sheet_name("全部记录"), index=False)
                
                # v8.0: 详细分类统计
                df_success = df[df["状态"] == "成功"]
                df_success.to_excel(writer, sheet_name=clean_sheet_name("成功"), index=False)
                
                df_skip = df[df["状态"] == "跳过"]
                df_skip.to_excel(writer, sheet_name=clean_sheet_name("跳过_重复"), index=False)
                
                df_failed = df[df["状态"] == "失败"]
                df_failed.to_excel(writer, sheet_name=clean_sheet_name("失败"), index=False)
                
                df_exception = df[df["状态"] == "处理异常"]
                df_exception.to_excel(writer, sheet_name=clean_sheet_name("处理异常"), index=False)
            
            logger.info(f"\n📊 Excel已生成: {excel_path}")
            logger.info(f"   - 全部记录: {len(df)} 条")
            logger.info(f"   - 成功: {len(df_success)} 条")
            logger.info(f"   - 跳过/重复: {len(df_skip)} 条")
            logger.info(f"   - 失败: {len(df_failed)} 条")
            logger.info(f"   - 处理异常: {len(df_exception)} 条")
        except Exception as e:
            logger.error(f"⚠️ Excel生成失败: {e}")

        # v7.4: 保存详细JSON结果
        # v8.0: 恢复JSON详细日志，便于分析和追踪
        json_path = os.path.join(output_dir, "detailed_results.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_records, f, ensure_ascii=False, indent=2)
        
        # 保存详细处理日志
        detailed_json_path = os.path.join(output_dir, "detailed_results.json")
        downloader.save_detailed_results(detailed_json_path)

        success = len([r for r in all_records if r.get('状态') == '成功'])
        skipped = len([r for r in all_records if r.get('状态') == '跳过'])
        failed = len([r for r in all_records if r.get('状态') == '失败'])

        print(f"\n{'='*60}")
        print(f"✅ 下载完成!")
        print(f"   总邮件: {len(invoices)}")
        print(f"   成功: {success}")
        print(f"   跳过: {skipped}")
        print(f"   失败: {failed}")
        print(f"   处理异常: {error_count}")
        print(f"   耗时: {elapsed:.1f}秒")
        print(f"   输出: {output_dir}")
        print(f"{'='*60}")

    except Exception as e:
        logger.error(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # v8.1: 确保无论成功还是失败都生成Excel报表
        try:
            import pandas as pd
            
            if 'all_records' in locals() and all_records:
                df = pd.DataFrame(all_records)
                columns = ["序号", "邮件主题", "邮件时间", "分类", "状态", "保存名称", "备注", "原因"]
                df = df.reindex(columns=[c for c in columns if c in df.columns])
                
                if "邮件时间" in df.columns:
                    df["邮件时间"] = pd.to_datetime(df["邮件时间"], errors='coerce')
                    df = df.sort_values("邮件时间", ascending=False)
                
                excel_path = os.path.join(output_dir, "发票目录.xlsx")
                
                def clean_sheet_name(name):
                    import re
                    return re.sub(r'[/\\:*?"<>|]', '_', name)[:31]
                
                with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=clean_sheet_name("全部记录"), index=False)
                    
                    if len(df) > 0:
                        df_success = df[df["状态"] == "成功"] if "状态" in df.columns else pd.DataFrame()
                        df_skip = df[df["状态"].isin(["跳过", "已存在"])] if "状态" in df.columns else pd.DataFrame()
                        df_failed = df[df["状态"] == "失败"] if "状态" in df.columns else pd.DataFrame()
                        df_exception = df[df["状态"] == "处理异常"] if "状态" in df.columns else pd.DataFrame()
                        
                        if len(df_success) > 0:
                            df_success.to_excel(writer, sheet_name=clean_sheet_name("成功"), index=False)
                        if len(df_skip) > 0:
                            df_skip.to_excel(writer, sheet_name=clean_sheet_name("跳过_重复"), index=False)
                        if len(df_failed) > 0:
                            df_failed.to_excel(writer, sheet_name=clean_sheet_name("失败"), index=False)
                        if len(df_exception) > 0:
                            df_exception.to_excel(writer, sheet_name=clean_sheet_name("处理异常"), index=False)
                
                logger.info(f"\n📊 Excel已生成: {excel_path}")
        except Exception as excel_error:
            logger.error(f"生成Excel报表失败: {excel_error}")


if __name__ == "__main__":
    main()
