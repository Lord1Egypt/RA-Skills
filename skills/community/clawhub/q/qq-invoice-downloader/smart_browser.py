#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能浏览器处理模块 v1.0 - Smart Browser Handler
专门优化处理诺诺网等复杂页面的多URL下载场景

核心功能：
1. URL智能评分 - 分析URL特征，优先选择包含download/invoice/pdf的链接
2. 多URL智能尝试 - 按优先级逐个尝试，直到成功
3. 弹窗自动处理 - 自动检测并点击确认按钮
4. 自适应等待 - 根据页面类型调整等待时间

解决问题：
- v7.3处理诺诺网时有12个URL但不知道哪个是正确的下载链接
- 需要智能识别真正的下载链接
"""

import os
import sys
import time
import re
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlparse, urljoin, parse_qs
from datetime import datetime

# 配置日志
logger = logging.getLogger(__name__)


class URLType(Enum):
    """URL类型枚举"""
    UNKNOWN = "unknown"
    DIRECT_PDF = "direct_pdf"          # 直接PDF
    DOWNLOAD_PAGE = "download_page"     # 下载页面
    INVOICE_VIEW = "invoice_view"       # 发票查看
    LOGIN_PAGE = "login_page"           # 登录页面
    REDIRECT = "redirect"               # 重定向
    API = "api"                         # API接口
    AD = "ad"                           # 广告/推广
    NAVIGATION = "navigation"           # 导航链接
    IMAGE = "image"                     # 图片


class DownloadStatus(Enum):
    """下载状态"""
    SUCCESS = "success"
    FAILED = "failed"
    NEED_LOGIN = "need_login"
    NEED_CAPTCHA = "need_captcha"
    POPUP = "popup"
    TIMEOUT = "timeout"
    INVALID_URL = "invalid_url"
    TRIED_ALL = "tried_all"
    NO_DOWNLOAD = "no_download"


@dataclass
class URLScore:
    """URL评分结果"""
    url: str
    score: float = 0.0
    url_type: URLType = URLType.UNKNOWN
    reasons: List[str] = field(default_factory=list)
    is_pdf: bool = False
    has_download_keyword: bool = False
    has_invoice_keyword: bool = False
    is_direct_link: bool = False
    domain: str = ""
    path: str = ""


@dataclass
class SmartDownloadResult:
    """智能下载结果"""
    status: DownloadStatus = DownloadStatus.FAILED
    message: str = ""
    download_path: Optional[str] = None
    tried_urls: List[str] = field(default_factory=list)
    successful_url: Optional[str] = None
    popup_handled: bool = False
    final_page_type: str = ""
    elapsed_time: float = 0.0


class SmartURLAnalyzer:
    """
    智能URL分析器
    
    核心功能：
    1. URL特征提取
    2. 智能评分
    3. 类型识别
    """
    
    # 评分权重配置
    WEIGHTS = {
        "pdf_extension": 30,        # .pdf后缀
        "download_keyword": 25,      # download关键词
        "invoice_keyword": 20,      # invoice关键词
        "direct_link": 15,           # 直接链接（非重定向）
        "view_action": 10,          # 查看/预览动作
        "api_negative": -20,         # API接口负面
        "ad_negative": -30,          # 广告负面
        "nav_negative": -10,         # 导航负面
    }
    
    # 关键词匹配
    DOWNLOAD_KEYWORDS = [
        "download", "downLoad", "DOWNLOAD",
        "downloadpdf", "download_pdf",
        "getpdf", "get_pdf", "getfile",
        "export", "exportpdf",
        "filedownload", "file-download"
    ]
    
    INVOICE_KEYWORDS = [
        "invoice", "Invoice", "INVOICE",
        "fp", "fpdm",  # 发票代码
        "fpmx",        # 发票明细
        "bill", "Bill",
        "receipt",
        "电子发票", "增值税", "发票",
    ]
    
    # 广告/无效URL特征
    AD_PATTERNS = [
        r"ad\.", r"ads\.", r"analytics",
        r"tracking", r"click\.=", r"promo",
        r"banner", r"sponsor",
        r"doubleclick", r"googlesyndication",
    ]
    
    # API特征
    API_PATTERNS = [
        r"/api/", r"/apis/", r"\.json$", 
        r"\.xml$", r"callback=", r"jsonp",
        r"/ajax/", r"/rest/", r"/rpc/",
    ]
    
    # 导航特征
    NAV_PATTERNS = [
        r"/index\.html?", r"/home", r"/portal",
        r"/user/", r"/account/", r"/center/",
        r"/menu", r"/nav", r"/header", r"/footer",
    ]
    
    @classmethod
    def analyze_url(cls, url: str) -> URLScore:
        """
        分析单个URL并返回评分
        
        Args:
            url: 待分析的URL
        
        Returns:
            URLScore: 评分结果
        """
        score_obj = URLScore(url=url)
        
        if not url:
            return score_obj
        
        try:
            parsed = urlparse(url)
            score_obj.domain = parsed.netloc
            score_obj.path = parsed.path.lower()
            
            # 提取查询参数
            query_params = parse_qs(parsed.query) if parsed.query else {}
            
            # 1. PDF文件检测（高优先级）
            path = parsed.path.lower()
            if path.endswith('.pdf') or '.pdf?' in url.lower():
                score_obj.is_pdf = True
                score_obj.score += cls.WEIGHTS["pdf_extension"]
                score_obj.reasons.append(f"PDF文件: {os.path.basename(path)}")
                score_obj.url_type = URLType.DIRECT_PDF
                return score_obj
            
            # 2. 下载关键词检测
            url_lower = url.lower()
            for keyword in cls.DOWNLOAD_KEYWORDS:
                if keyword.lower() in url_lower:
                    score_obj.has_download_keyword = True
                    score_obj.score += cls.WEIGHTS["download_keyword"]
                    score_obj.reasons.append(f"包含下载关键词: {keyword}")
                    if score_obj.url_type == URLType.UNKNOWN:
                        score_obj.url_type = URLType.DOWNLOAD_PAGE
                    break
            
            # 3. 发票关键词检测
            for keyword in cls.INVOICE_KEYWORDS:
                if keyword.lower() in url_lower:
                    score_obj.has_invoice_keyword = True
                    score_obj.score += cls.WEIGHTS["invoice_keyword"]
                    score_obj.reasons.append(f"包含发票关键词: {keyword}")
                    if score_obj.url_type == URLType.UNKNOWN:
                        score_obj.url_type = URLType.INVOICE_VIEW
                    break
            
            # 4. 直接链接检测（非API/广告）
            is_direct = True
            for pattern in cls.API_PATTERNS:
                if re.search(pattern, url_lower):
                    score_obj.score += cls.WEIGHTS["api_negative"]
                    score_obj.reasons.append(f"API接口: 扣分")
                    is_direct = False
                    if score_obj.url_type == URLType.UNKNOWN:
                        score_obj.url_type = URLType.API
            
            for pattern in cls.AD_PATTERNS:
                if re.search(pattern, url_lower):
                    score_obj.score += cls.WEIGHTS["ad_negative"]
                    score_obj.reasons.append(f"广告链接: 大幅扣分")
                    is_direct = False
                    if score_obj.url_type == URLType.UNKNOWN:
                        score_obj.url_type = URLType.AD
            
            for pattern in cls.NAV_PATTERNS:
                if re.search(pattern, url_lower):
                    score_obj.score += cls.WEIGHTS["nav_negative"]
                    score_obj.reasons.append(f"导航链接: 扣分")
                    is_direct = False
                    if score_obj.url_type == URLType.UNKNOWN:
                        score_obj.url_type = URLType.NAVIGATION
            
            if is_direct and score_obj.url_type in [URLType.UNKNOWN, URLType.DOWNLOAD_PAGE]:
                score_obj.is_direct_link = True
                score_obj.score += cls.WEIGHTS["direct_link"]
                score_obj.reasons.append("直接链接（非重定向）")
            
            # 5. 动作检测
            action_patterns = [
                (r"/view/", "查看页面", URLType.INVOICE_VIEW),
                (r"/show/", "显示页面", URLType.INVOICE_VIEW),
                (r"/preview/", "预览", URLType.INVOICE_VIEW),
                (r"/get/", "获取文件", URLType.DOWNLOAD_PAGE),
                (r"/fetch/", "获取文件", URLType.DOWNLOAD_PAGE),
                (r"/request/", "请求", URLType.API),
            ]
            
            for pattern, action, url_type in action_patterns:
                if re.search(pattern, url_lower):
                    score_obj.score += cls.WEIGHTS["view_action"]
                    score_obj.reasons.append(f"动作: {action}")
                    if score_obj.url_type == URLType.UNKNOWN:
                        score_obj.url_type = url_type
            
            # 6. 登录页面检测
            if any(kw in url_lower for kw in ["login", "signin", "/login/", "/auth/"]):
                score_obj.score -= 50
                score_obj.reasons.append("登录页面: 排除")
                score_obj.url_type = URLType.LOGIN_PAGE
            
            # 7. 文件名检测
            filename = os.path.basename(path)
            if filename and '.' in filename:
                ext = filename.rsplit('.', 1)[-1].lower()
                # 支持的图片格式（可能是发票图片）
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'tiff']:
                    score_obj.score += 5
                    score_obj.reasons.append(f"图片文件: .{ext}")
            
            # 8. 域名信任度加分
            trusted_domains = [
                "nuonuo.com", "nnfp.com",     # 诺诺网
                "hangtian.cn", "aisino.com",  # 航天信息
                "baiwang.com",                # 百望
                "yonyou.com",                 # 用友
                "kingdee.com",                # 金蝶
                "e-inv.cn", "fapiao.com",     # 其他发票平台
            ]
            
            for domain in trusted_domains:
                if domain in url_lower:
                    score_obj.score += 10
                    score_obj.reasons.append(f"可信域名: {domain}")
                    break
            
        except Exception as e:
            logger.debug(f"URL分析异常 {url}: {e}")
        
        return score_obj
    
    @classmethod
    def rank_urls(cls, urls: List[str], top_n: int = 5) -> List[URLScore]:
        """
        对URL列表进行智能排序
        
        Args:
            urls: URL列表
            top_n: 返回前N个
        
        Returns:
            排序后的URL评分列表
        """
        # 过滤无效URL
        valid_urls = [u for u in urls if u and isinstance(u, str) and len(u) > 10]
        
        if not valid_urls:
            return []
        
        # 分析每个URL
        scored_urls = [cls.analyze_url(url) for url in valid_urls]
        
        # 按分数降序排序
        scored_urls.sort(key=lambda x: x.score, reverse=True)
        
        # 记录日志
        logger.info(f"   📊 URL分析完成，共{len(scored_urls)}个URL")
        for i, s in enumerate(scored_urls[:5]):  # 只显示前5个
            logger.info(f"      [{i+1}] 分数:{s.score:+.1f} - {s.url[:60]}...")
            if s.reasons:
                logger.info(f"          原因: {', '.join(s.reasons[:2])}")
        
        return scored_urls[:top_n]


class SmartPopupHandler:
    """
    智能弹窗处理器
    
    功能：
    1. 多种弹窗类型检测
    2. 自动确认处理
    3. 下载确认对话框
    """
    
    # 弹窗确认按钮选择器
    CONFIRM_BUTTONS = [
        # 中文确认
        'button:has-text("确认")',
        'button:has-text("确定")',
        'button:has-text("是")',
        'button:has-text("下载")',
        'button:has-text("立即下载")',
        'button:has-text("开始下载")',
        'a:has-text("确认")',
        'a:has-text("确定")',
        'a:has-text("下载")',
        # 英文确认
        'button:has-text("Confirm")',
        'button:has-text("OK")',
        'button:has-text("Download")',
        'button:has-text("Yes")',
        # 通用
        '.confirm', '.ok', '.download-btn',
        '[class*="confirm"]',
        '[class*="dialog-ok"]',
        'button[type="button"]:nth-child(1)',  # 常见弹窗第一个按钮
        'button.primary',                       # 主要按钮
    ]
    
    # 取消/关闭按钮（优先级低）
    CANCEL_BUTTONS = [
        'button:has-text("取消")',
        'button:has-text("关闭")',
        'button:has-text("Close")',
        '[class*="close"]',
        '[class*="cancel"]',
    ]
    
    # 弹窗容器检测
    POPUP_CONTAINERS = [
        '[class*="modal"]',
        '[class*="popup"]',
        '[class*="dialog"]',
        '[class*="layer"]',
        '[class*="alert"]',
        '[role="dialog"]',
        '#modal',
        '.popup',
    ]
    
    @classmethod
    def has_popup(cls, page) -> Tuple[bool, Optional[str]]:
        """
        检测页面是否有弹窗
        
        Returns:
            (是否有弹窗, 弹窗类型描述)
        """
        try:
            page_content = page.content().lower()
            
            # 1. 检查弹窗容器
            for selector in cls.POPUP_CONTAINERS:
                try:
                    if page.locator(selector).count() > 0:
                        # 检查是否可见
                        for i in range(page.locator(selector).count()):
                            el = page.locator(selector).nth(i)
                            if el.is_visible():
                                return True, selector
                except:
                    pass
            
            # 2. 检查确认按钮存在（说明有弹窗）
            for selector in cls.CONFIRM_BUTTONS:
                try:
                    if page.locator(selector).count() > 0:
                        return True, f"确认按钮: {selector}"
                except:
                    pass
            
            # 3. 检查特定文本
            popup_texts = ["确认", "确定", "提示", "下载确认", "温馨提示"]
            for text in popup_texts:
                if text in page_content:
                    # 检查附近是否有按钮
                    pattern = f".*{text}.*"
                    if re.search(pattern, page_content):
                        return True, f"包含文本: {text}"
            
            return False, None
            
        except Exception as e:
            logger.debug(f"弹窗检测异常: {e}")
            return False, None
    
    @classmethod
    def handle_popup(cls, page, timeout: int = 10000) -> bool:
        """
        处理弹窗，点击确认按钮
        
        Args:
            page: Playwright page对象
            timeout: 等待超时时间(毫秒)
        
        Returns:
            是否成功处理
        """
        try:
            # 等待弹窗出现
            time.sleep(1)  # 短暂等待
            
            # 查找确认按钮
            for selector in cls.CONFIRM_BUTTONS:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0:
                        # 查找可见的按钮
                        for i in range(locator.count()):
                            btn = locator.nth(i)
                            if btn.is_visible():
                                # 点击确认按钮
                                btn.click()
                                logger.info(f"   ✅ 弹窗已确认: {selector}")
                                time.sleep(2)  # 等待处理
                                return True
                except Exception as e:
                    logger.debug(f"尝试选择器 {selector} 失败: {e}")
                    continue
            
            # 如果没找到确认按钮，尝试按ESC关闭
            try:
                page.keyboard.press("Escape")
                time.sleep(0.5)
            except:
                pass
            
            return False
            
        except Exception as e:
            logger.debug(f"弹窗处理异常: {e}")
            return False


class SmartWaitManager:
    """
    智能等待管理器
    
    根据页面类型和场景动态调整等待时间
    """
    
    # 基础等待时间（秒）
    BASE_WAIT = {
        "page_load": 3,         # 页面加载基础等待
        "dynamic_content": 5,  # 动态内容加载
        "popup": 2,             # 弹窗出现
        "download_start": 3,    # 下载开始
        "redirect": 4,         # 重定向等待
    }
    
    # 平台特定等待时间
    PLATFORM_WAIT = {
        "nuonuo": {
            "page_load": 5,
            "dynamic_content": 8,
            "popup": 3,
            "download_start": 5,
        },
        "hangtian": {
            "page_load": 6,
            "dynamic_content": 10,
            "popup": 3,
            "download_start": 5,
        },
        "baiwang": {
            "page_load": 4,
            "dynamic_content": 6,
            "popup": 2,
            "download_start": 4,
        },
    }
    
    @classmethod
    def get_wait_times(cls, url: str = "", page_type: str = "") -> Dict[str, float]:
        """
        获取等待时间配置
        
        Args:
            url: 页面URL
            page_type: 页面类型
        
        Returns:
            等待时间字典
        """
        wait_times = cls.BASE_WAIT.copy()
        
        # 检测平台
        url_lower = url.lower()
        platform = None
        
        if "nuonuo" in url_lower or "nnfp" in url_lower:
            platform = "nuonuo"
        elif "hangtian" in url_lower or "ht" in url_lower:
            platform = "hangtian"
        elif "baiwang" in url_lower or "bw" in url_lower:
            platform = "baiwang"
        
        # 应用平台特定等待
        if platform and platform in cls.PLATFORM_WAIT:
            for key, value in cls.PLATFORM_WAIT[platform].items():
                wait_times[key] = value
        
        # 根据页面类型调整
        if page_type == "login":
            wait_times["page_load"] = 2
            wait_times["dynamic_content"] = 3
        elif page_type == "download":
            wait_times["page_load"] += 1
        
        return wait_times


class SmartBrowserHandler:
    """
    智能浏览器处理器
    
    整合所有智能功能，专门解决多URL下载问题
    """
    
    def __init__(self, browser_pool=None):
        self.browser_pool = browser_pool
        self.url_analyzer = SmartURLAnalyzer()
        self.popup_handler = SmartPopupHandler()
        self.wait_manager = SmartWaitManager()
        
        # 配置
        self.max_url_attempts = 5      # 最多尝试的URL数量
        self.max_retries = 3          # 每个URL的重试次数
        self.download_timeout = 60000  # 下载超时 60秒
        
        # 统计
        self.stats = {
            "total_urls_processed": 0,
            "successful_downloads": 0,
            "popup_handled": 0,
            "login_pages": 0,
            "failed_downloads": 0,
        }
    
    def process_urls(self, urls: List[str], subject: str = "") -> SmartDownloadResult:
        """
        智能处理多个URL
        
        Args:
            urls: URL列表（可能有12个或更多）
            subject: 邮件主题（用于日志）
        
        Returns:
            SmartDownloadResult: 处理结果
        """
        start_time = time.time()
        result = SmartDownloadResult()
        
        if not urls:
            result.status = DownloadStatus.INVALID_URL
            result.message = "URL列表为空"
            return result
        
        logger.info(f"   📋 收到 {len(urls)} 个URL，开始智能分析...")
        
        # 1. URL智能评分排序
        ranked_urls = self.url_analyzer.rank_urls(urls, top_n=self.max_url_attempts)
        
        if not ranked_urls:
            result.status = DownloadStatus.INVALID_URL
            result.message = "无可用URL"
            return result
        
        # 2. 按优先级逐个尝试
        for idx, url_score in enumerate(ranked_urls):
            url = url_score.url
            result.tried_urls.append(url)
            
            logger.info(f"   🔗 尝试 [{idx+1}/{len(ranked_urls)}] 分数:{url_score.score:.1f}")
            logger.info(f"      URL: {url[:80]}...")
            
            # 跳过登录页面
            if url_score.url_type == URLType.LOGIN_PAGE:
                logger.info(f"      ⏭️ 跳过：登录页面")
                continue
            
            # 处理单个URL
            url_result = self._process_single_url(url, url_score, subject)
            
            # 检查结果
            if url_result["status"] == "success":
                result.status = DownloadStatus.SUCCESS
                result.message = "下载成功"
                result.download_path = url_result.get("download_path")
                result.successful_url = url
                result.final_page_type = url_result.get("page_type", "unknown")
                result.popup_handled = url_result.get("popup_handled", False)
                self.stats["successful_downloads"] += 1
                break
            
            elif url_result["status"] == "need_login":
                result.status = DownloadStatus.NEED_LOGIN
                result.message = "需要登录"
                self.stats["login_pages"] += 1
                # 登录页面不继续尝试其他URL
                break
            
            else:
                # 记录失败原因，继续尝试下一个
                logger.warning(f"      ❌ 失败: {url_result.get('message', '未知错误')}")
                continue
        
        # 所有URL都尝试完毕
        if result.status != DownloadStatus.SUCCESS:
            if result.status != DownloadStatus.NEED_LOGIN:
                result.status = DownloadStatus.TRIED_ALL
                result.message = f"已尝试{len(result.tried_urls)}个URL，全部失败"
                self.stats["failed_downloads"] += 1
        
        result.elapsed_time = time.time() - start_time
        self.stats["total_urls_processed"] += 1
        
        # 记录结果
        if result.status == DownloadStatus.SUCCESS:
            logger.info(f"   ✅ 下载成功! ({result.elapsed_time:.1f}s)")
            logger.info(f"      使用URL: {result.successful_url[:60]}...")
        else:
            logger.warning(f"   ❌ 下载失败: {result.message} ({result.elapsed_time:.1f}s)")
        
        return result
    
    def _process_single_url(self, url: str, url_score: URLScore, 
                           subject: str) -> Dict[str, Any]:
        """处理单个URL"""
        
        # 获取等待时间配置
        wait_times = self.wait_manager.get_wait_times(url)
        
        if not self.browser_pool or not self.browser_pool._initialized:
            return {"status": "failed", "message": "浏览器未初始化"}
        
        page = None
        
        for retry in range(self.max_retries):
            try:
                page = self.browser_pool.context.new_page()
                
                # 访问页面
                logger.debug(f"      访问页面... (尝试 {retry+1}/{self.max_retries})")
                page.goto(url, wait_until='networkidle', timeout=self.download_timeout)
                time.sleep(wait_times["page_load"])
                
                # 检测弹窗
                has_popup, popup_info = self.popup_handler.has_popup(page)
                if has_popup:
                    logger.debug(f"      检测到弹窗: {popup_info}")
                    # 尝试处理弹窗
                    popup_handled = self.popup_handler.handle_popup(page)
                    if popup_handled:
                        self.stats["popup_handled"] += 1
                        logger.debug(f"      ✅ 弹窗已处理")
                        time.sleep(wait_times["popup"])
                
                # 尝试下载
                download = self._try_download(page, url, url_score)
                
                if download:
                    return {
                        "status": "success",
                        "download_path": download,
                        "page_type": url_score.url_type.value,
                        "popup_handled": has_popup,
                    }
                
                # 检查是否需要登录
                page_content = page.content().lower()
                if "登录" in page_content and ("username" in page_content or "password" in page_content):
                    return {"status": "need_login", "message": "需要登录"}
                
                # 检查是否有下载按钮
                download_btn_count = page.locator('button:has-text("下载"), a:has-text("下载"), [class*="download"]').count()
                if download_btn_count == 0:
                    return {"status": "failed", "message": "未找到下载入口"}
                
                # 重试
                if retry < self.max_retries - 1:
                    delay = 2 ** retry  # 指数退避
                    time.sleep(delay)
                
            except Exception as e:
                error_msg = str(e)
                logger.debug(f"      处理异常: {error_msg}")
                
                if retry < self.max_retries - 1:
                    time.sleep(2 ** retry)
            finally:
                if page:
                    try:
                        page.close()
                    except:
                        pass
        
        return {"status": "failed", "message": "重试次数用完"}
    
    def _try_download(self, page, url: str, url_score: URLScore):
        """尝试下载"""
        
        try:
            # 1. 直接PDF下载
            if url_score.is_pdf or url_score.url_type == URLType.DIRECT_PDF:
                try:
                    with page.expect_download(timeout=self.download_timeout) as download_info:
                        page.goto(url)
                        time.sleep(3)
                    return download_info.value.path if download_info.value else None
                except Exception as e:
                    logger.debug(f"      直接PDF下载失败: {e}")
            
            # 2. 查找下载按钮
            download_selectors = [
                # 下载按钮
                'button:has-text("下载")',
                'a:has-text("下载")',
                'button:has-text("PDF下载")',
                'a:has-text("PDF下载")',
                'button:has-text("电子发票下载")',
                'a:has-text("电子发票下载")',
                # 下载链接
                'a[href$=".pdf"]',
                'a[href*="download"]',
                # 通用下载
                '[class*="download"]',
                '[data-action="download"]',
            ]
            
            for selector in download_selectors:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0:
                        # 找到第一个可见的
                        for i in range(locator.count()):
                            btn = locator.nth(i)
                            if btn.is_visible():
                                with page.expect_download(timeout=self.download_timeout) as download_info:
                                    btn.click()
                                    time.sleep(5)
                                if download_info.value:
                                    return download_info.value.path
                except Exception as e:
                    logger.debug(f"      选择器 {selector} 失败: {e}")
                    continue
            
            return None
            
        except Exception as e:
            logger.debug(f"      下载尝试异常: {e}")
            return None
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats.copy()


class SmartBrowserPool:
    """
    智能浏览器池
    
    在EnhancedBrowserPool基础上增加智能URL处理能力
    """
    
    def __init__(self):
        self.browser = None
        self.context = None
        self.playwright = None
        self._initialized = False
        self._lock = None
        self._page_count = 0
        
        # 智能处理器
        self.smart_handler = None
    
    def initialize(self):
        """初始化浏览器"""
        if self._initialized:
            return
        
        try:
            from playwright.sync_api import sync_playwright
            
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context(
                accept_downloads=True,
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            
            self.context.set_default_timeout(60000)
            self._initialized = True
            self._lock = __import__('threading').Lock()
            
            # 初始化智能处理器
            self.smart_handler = SmartBrowserHandler(self)
            
            logger.info("🌐 智能浏览器初始化完成")
            
        except Exception as e:
            logger.error(f"⚠️ 浏览器初始化失败: {e}")
            self._initialized = False
    
    def process_invoice_urls(self, urls: List[str], subject: str = "") -> SmartDownloadResult:
        """
        智能处理发票下载（支持多URL）
        
        Args:
            urls: URL列表（可能有多个）
            subject: 邮件主题
        
        Returns:
            SmartDownloadResult: 处理结果
        """
        with self._lock:
            if not self._initialized:
                result = SmartDownloadResult()
                result.status = DownloadStatus.FAILED
                result.message = "浏览器未初始化"
                return result
            
            # 检查是否需要重启
            self._should_restart_browser()
            
            if not urls:
                result = SmartDownloadResult()
                result.status = DownloadStatus.INVALID_URL
                result.message = "无URL"
                return result
            
            # 使用智能处理器
            if self.smart_handler:
                return self.smart_handler.process_urls(urls, subject)
            
            # 后备处理
            return self._fallback_process(urls[0])
    
    def _should_restart_browser(self):
        """检查是否需要重启"""
        self._page_count += 1
        if self._page_count >= 50:
            logger.info("🔄 浏览器处理50个页面，执行重启...")
            self._restart_browser()
            self._page_count = 0
    
    def _restart_browser(self):
        """重启浏览器"""
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context(
                accept_downloads=True,
                viewport={"width": 1920, "height": 1080}
            )
            logger.info("✅ 浏览器重启完成")
        except Exception as e:
            logger.error(f"⚠️ 浏览器重启失败: {e}")
    
    def _fallback_process(self, url: str) -> SmartDownloadResult:
        """后备处理（单个URL）"""
        result = SmartDownloadResult()
        result.status = DownloadStatus.FAILED
        result.message = "智能处理器未初始化"
        return result
    
    def close(self):
        """关闭浏览器"""
        logger.info("🌐 关闭智能浏览器...")
        
        if self.smart_handler:
            stats = self.smart_handler.get_stats()
            logger.info(f"   📊 处理统计: {stats}")
        
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            logger.debug(f"   关闭异常: {e}")
        
        logger.info("   ✅ 智能浏览器已关闭")


# 便捷函数
def analyze_urls(urls: List[str]) -> List[URLScore]:
    """分析URL列表"""
    return SmartURLAnalyzer.rank_urls(urls)


def select_best_url(urls: List[str]) -> Optional[str]:
    """选择最佳URL"""
    ranked = SmartURLAnalyzer.rank_urls(urls, top_n=1)
    return ranked[0].url if ranked else None


# 测试入口
if __name__ == "__main__":
    print("Smart Browser Handler v1.0")
    print("=" * 50)
    
    # 测试URL分析
    test_urls = [
        "https://www.nuonuo.com/invoice/download/123456.pdf",
        "https://www.nuonuo.com/api/invoice/get?fpdm=123",
        "https://www.nuonuo.com/user/login",
        "https://ads.example.com/banner.jpg",
        "https://www.nuonuo.com/invoice/view/789",
    ]
    
    print("\n📊 URL评分测试:")
    results = analyze_urls(test_urls)
    for i, r in enumerate(results):
        print(f"  [{i+1}] 分数:{r.score:+.1f} - {r.url_type.value}")
        print(f"      原因: {r.reasons}")
    
    print(f"\n🏆 最佳URL: {select_best_url(test_urls)}")
