#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版浏览器处理模块 v1.0 - Enhanced Browser Handler
用于处理各种复杂场景的发票下载页面

功能特性：
1. 智能页面分析 - 自动识别页面类型（登录/验证码/下载页）
2. 多选择器匹配 - 支持30+种下载按钮选择器
3. 智能重试机制 - 指数退避 + 智能判断
4. 异常页面处理 - 登录/验证码/弹窗等
5. 详细日志记录 - 结构化日志便于调试

支持的场景：
- 直接PDF下载
- 单页面下载
- 多层级页面
- 弹窗确认
- 验证码页面
- 登录页面
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
from urllib.parse import urlparse

# 配置日志
logger = logging.getLogger(__name__)


class PageType(Enum):
    """页面类型枚举"""
    UNKNOWN = "unknown"
    LOGIN = "login"           # 登录页面
    CAPTCHA = "captcha"       # 验证码页面
    DOWNLOAD = "download"     # 下载页面
    SUCCESS = "success"       # 成功/已完成
    ERROR = "error"          # 错误页面
    REDIRECT = "redirect"     # 重定向中
    PDF_DIRECT = "pdf_direct" # 直接PDF


class DownloadStatus(Enum):
    """下载状态"""
    SUCCESS = "success"
    FAILED = "failed"
    NEED_LOGIN = "need_login"
    NEED_CAPTCHA = "need_captcha"
    BUTTON = "no_button"
    POPUP = "popup"
    TIMEOUT = "timeout"
    RETRY_EXHAUSTED = "retry_exhausted"


@dataclass
class PageAnalysis:
    """页面分析结果"""
    page_type: PageType = PageType.UNKNOWN
    confidence: float = 0.0  # 置信度 0-1
    details: str = ""
    detected_selectors: List[str] = field(default_factory=list)
    login_form_found: bool = False
    captcha_found: bool = False
    download_button_found: bool = False
    popup_found: bool = False
    error_message: str = ""


@dataclass
class DownloadResult:
    """下载结果"""
    status: DownloadStatus = DownloadStatus.FAILED
    message: str = ""
    download_path: Optional[str] = None
    page_analysis: Optional[PageAnalysis] = None
    retry_count: int = 0
    elapsed_time: float = 0.0


class EnhancedDownloadSelectors:
    """增强版下载按钮选择器库"""
    
    # 基础选择器
    BASE_SELECTORS = [
        # 通用下载文本
        'button:has-text("下载")',
        'a:has-text("下载")',
        'button:has-text("PDF下载")',
        'a:has-text("PDF下载")',
        'button:has-text("PDF")',
        'a:has-text("PDF")',
        'button:has-text("下载PDF")',
        'a:has-text("下载PDF")',
        # 下载图标/图片
        '[class*="download"]',
        '[id*="download"]',
        '[class*="Download"]',
        '[id*="Download"]',
        '[data-action="download"]',
        '[data-type="download"]',
        '[data-testid*="download"]',
    ]
    
    # 特定平台选择器
    PLATFORM_SELECTORS = {
        # 诺诺网
        "nuonuo": [
            'button:has-text("下载发票")',
            'a:has-text("下载发票")',
            'button:has-text("电子发票下载")',
            'a:has-text("电子发票下载")',
            '.nuonuo-download-btn',
            '[class*="nuonuo"]',
        ],
        # 航天信息
        "hangtian": [
            'button:has-text("电子发票下载")',
            'a:has-text("电子发票下载")',
            'button:has-text("发票下载")',
            '.hangtian-download',
            '[class*="ht"]',
        ],
        # 百望
        "baiwang": [
            'button:has-text("下载")',
            '.bw-download-btn',
            '[class*="baiwang"]',
        ],
        # 用友
        "yonyou": [
            'button:has-text("下载")',
            '.yy-download',
            '[class*="yonyou"]',
        ],
        # 金蝶
        "kingdee": [
            'button:has-text("下载")',
            '.kd-download',
            '[class*="kingdee"]',
        ],
        # 浪潮
        "inspur": [
            'button:has-text("下载")',
            '.inspur-download',
        ],
        # 电信/联通/移动
        "telecom": [
            'button:has-text("下载")',
            '.telecom-download',
        ],
    }
    
    # PDF直接链接
    PDF_LINK_SELECTORS = [
        'a[href$=".pdf"]',
        'a[href*=".pdf?"]',
        'a[href*="/pdf/"]',
        'a[href*="/download/"]',
        'a[href*="download"]',
        'a[href*="file"]',
    ]
    
    # 图片按钮
    IMAGE_BUTTON_SELECTORS = [
        'img[src*="download"]',
        'img[alt*="下载"]',
        '[title*="下载"]',
        '[aria-label*="下载"]',
    ]
    
    # 数据属性
    DATA_ATTR_SELECTORS = [
        '[data-action="download"]',
        '[data-type="pdf"]',
        '[data-download="true"]',
        '[data-file-type="pdf"]',
        '[data-btn-type="download"]',
    ]
    
    @classmethod
    def get_all_selectors(cls) -> List[str]:
        """获取所有选择器（去重）"""
        all_selectors = set(cls.BASE_SELECTORS)
        for platform in cls.PLATFORM_SELECTORS.values():
            all_selectors.update(platform)
        all_selectors.update(cls.PDF_LINK_SELECTORS)
        all_selectors.update(cls.IMAGE_BUTTON_SELECTORS)
        all_selectors.update(cls.DATA_ATTR_SELECTORS)
        return list(all_selectors)
    
    @classmethod
    def get_platform_selectors(cls, url: str) -> List[str]:
        """根据URL获取平台特定选择器"""
        url_lower = url.lower()
        selectors = []
        
        if "nuonuo" in url_lower or "nnfp" in url_lower:
            selectors.extend(cls.PLATFORM_SELECTORS.get("nuonuo", []))
        if "hangtian" in url_lower or "ht" in url_lower:
            selectors.extend(cls.PLATFORM_SELECTORS.get("hangtian", []))
        if "baiwang" in url_lower or "bw" in url_lower:
            selectors.extend(cls.PLATFORM_SELECTORS.get("baiwang", []))
        if "yonyou" in url_lower or "yy" in url_lower:
            selectors.extend(cls.PLATFORM_SELECTORS.get("yonyou", []))
        if "kingdee" in url_lower or "kd" in url_lower:
            selectors.extend(cls.PLATFORM_SELECTORS.get("kingdee", []))
            
        return selectors


class LoginPageDetector:
    """登录页面检测器"""
    
    LOGIN_INDICATORS = {
        # 文本关键词
        "text": [
            "登录", "login", "sign in", "用户名", "密码", 
            "account", "password", "验证码", "captcha",
            "账号登录", "立即登录", "登录成功"
        ],
        # 表单元素
        "form_elements": [
            'input[type="text"]',
            'input[type="email"]',
            'input[name*="user"]',
            'input[name*="account"]',
            'input[name*="login"]',
            'input[name*="username"]',
            'input[name*="password"]',
            'input[type="password"]',
        ],
        # 登录按钮
        "buttons": [
            'button:has-text("登录")',
            'button:has-text("Login")',
            'button:has-text("登陆")',
            'a:has-text("登录")',
            'input[type="submit"]',
            'button[type="submit"]',
        ],
        # CSS类/ID
        "css": [
            '[class*="login"]',
            '[id*="login"]',
            '[class*="signin"]',
            '[id*="signin"]',
            '[class*="auth"]',
            '[id*="auth"]',
        ]
    }
    
    @classmethod
    def is_login_page(cls, page) -> Tuple[bool, float]:
        """
        检测是否为登录页面
        返回: (是否登录页, 置信度)
        """
        try:
            page_content = page.content().lower()
            
            # 1. 检查文本关键词
            text_matches = 0
            for keyword in cls.LOGIN_INDICATORS["text"]:
                if keyword.lower() in page_content:
                    text_matches += 1
            
            text_confidence = min(text_matches / 3, 1.0)  # 最多3个关键词匹配
            
            # 2. 检查表单元素
            form_matches = 0
            for selector in cls.LOGIN_INDICATORS["form_elements"]:
                try:
                    if page.locator(selector).count() > 0:
                        form_matches += 1
                except:
                    pass
            
            form_confidence = min(form_matches / 2, 1.0)
            
            # 3. 检查登录按钮
            button_matches = 0
            for selector in cls.LOGIN_INDICATORS["buttons"]:
                try:
                    if page.locator(selector).count() > 0:
                        button_matches += 1
                except:
                    pass
            
            button_confidence = min(button_matches / 1, 1.0)
            
            # 综合置信度
            confidence = (text_confidence * 0.3 + form_confidence * 0.4 + button_confidence * 0.3)
            
            return confidence > 0.3, confidence
            
        except Exception as e:
            logger.debug(f"登录页面检测异常: {e}")
            return False, 0.0


class CaptchaDetector:
    """验证码检测器"""
    
    CAPTCHA_INDICATORS = {
        # 文本
        "text": [
            "验证码", " captcha", "图形验证码", "安全验证",
            "请输入验证码", "输入验证码", "滑动验证",
            "点击验证", "人机验证", "verify", "captcha"
        ],
        # 元素
        "elements": [
            'input[name*="captcha"]',
            'input[name*="code"]',
            'input[id*="captcha"]',
            '[class*="captcha"]',
            '[id*="captcha"]',
            '[class*="verify"]',
            '[id*="verify"]',
            # 滑块验证
            '[class*="slider"]',
            '[class*="geetest"]',
            '[class*="nc_wrapper"]',  # 阿里云滑动验证
            # iframe
            'iframe[src*="captcha"]',
            'iframe[src*="geetest"]',
        ]
    }
    
    @classmethod
    def is_captcha_page(cls, page) -> Tuple[bool, float]:
        """
        检测是否有验证码
        返回: (是否有验证码, 置信度)
        """
        try:
            page_content = page.content().lower()
            
            # 1. 文本匹配
            text_matches = 0
            for keyword in cls.CAPTCHA_INDICATORS["text"]:
                if keyword.lower() in page_content:
                    text_matches += 1
            
            text_confidence = min(text_matches / 2, 1.0)
            
            # 2. 元素匹配
            element_matches = 0
            for selector in cls.CAPTCHA_INDICATORS["elements"]:
                try:
                    if page.locator(selector).count() > 0:
                        element_matches += 1
                except:
                    pass
            
            element_confidence = min(element_matches / 1, 1.0)
            
            confidence = (text_confidence * 0.5 + element_confidence * 0.5)
            
            return confidence > 0.3, confidence
            
        except Exception as e:
            logger.debug(f"验证码检测异常: {e}")
            return False, 0.0


class PopupDetector:
    """弹窗检测器"""
    
    POPUP_INDICATORS = {
        "text": [
            "确认", "确定", "提示", "注意", "警告",
            "温馨提示", "友情提示", "系统提示", "下载确认"
        ],
        "elements": [
            '[class*="modal"]',
            '[class*="popup"]',
            '[class*="dialog"]',
            '[class*="alert"]',
            '[class*="layer"]',
            '[id*="modal"]',
            '[id*="popup"]',
            '[id*="dialog"]',
            '[role="dialog"]',
            # 确认按钮
            'button:has-text("确认")',
            'button:has-text("确定")',
            'button:has-text("是")',
            'a:has-text("确认")',
            'a:has-text("确定")',
        ]
    }
    
    @classmethod
    def has_popup(cls, page) -> Tuple[bool, float]:
        """
        检测是否有弹窗
        返回: (是否有弹窗, 置信度)
        """
        try:
            page_content = page.content().lower()
            
            text_matches = sum(1 for t in cls.POPUP_INDICATORS["text"] if t.lower() in page_content)
            text_confidence = min(text_matches / 2, 1.0)
            
            element_matches = 0
            for selector in cls.POPUP_INDICATORS["elements"]:
                try:
                    if page.locator(selector).count() > 0:
                        element_matches += 1
                except:
                    pass
            
            element_confidence = min(element_matches / 2, 1.0)
            
            confidence = (text_confidence * 0.4 + element_confidence * 0.6)
            
            return confidence > 0.4, confidence
            
        except Exception as e:
            logger.debug(f"弹窗检测异常: {e}")
            return False, 0.0


class SmartPageAnalyzer:
    """智能页面分析器"""
    
    def __init__(self):
        self.login_detector = LoginPageDetector()
        self.captcha_detector = CaptchaDetector()
        self.popup_detector = PopupDetector()
    
    def analyze(self, page, url: str = "") -> PageAnalysis:
        """
        智能分析页面类型
        """
        analysis = PageAnalysis()
        
        try:
            # 1. 检测登录页面
            is_login, login_conf = self.login_detector.is_login_page(page)
            if is_login:
                analysis.page_type = PageType.LOGIN
                analysis.confidence = login_conf
                analysis.login_form_found = True
                analysis.details = f"检测到登录页面 (置信度: {login_conf:.2f})"
                return analysis
            
            # 2. 检测验证码
            is_captcha, captcha_conf = self.captcha_detector.is_captcha_page(page)
            if is_captcha:
                analysis.page_type = PageType.CAPTCHA
                analysis.confidence = captcha_conf
                analysis.captcha_found = True
                analysis.details = f"检测到验证码 (置信度: {captcha_conf:.2f})"
                return analysis
            
            # 3. 检测弹窗
            has_popup, popup_conf = self.popup_detector.has_popup(page)
            if has_popup:
                analysis.popup_found = True
                analysis.details = f"检测到弹窗 (置信度: {popup_conf:.2f})"
                # 弹窗不一定是下载页，继续检测
            
            # 4. 检测是否有下载按钮
            selectors = EnhancedDownloadSelectors.get_all_selectors()
            found_selectors = []
            
            for selector in selectors:
                try:
                    count = page.locator(selector).count()
                    if count > 0:
                        found_selectors.append(selector)
                except:
                    pass
            
            if found_selectors:
                analysis.download_button_found = True
                analysis.detected_selectors = found_selectors[:5]  # 最多记录5个
                analysis.page_type = PageType.DOWNLOAD
                analysis.confidence = min(len(found_selectors) / 3, 1.0)
                analysis.details = f"找到 {len(found_selectors)} 个下载相关元素"
                return analysis
            
            # 5. 检查是否是直接PDF链接
            page_url = page.url
            if page_url.lower().endswith('.pdf') or '.pdf?' in page_url:
                analysis.page_type = PageType.PDF_DIRECT
                analysis.confidence = 1.0
                analysis.details = "页面直接指向PDF文件"
                return analysis
            
            # 6. 检查页面内容
            page_content = page.content().lower()
            if "下载" in page_content or "download" in page_content:
                analysis.page_type = PageType.DOWNLOAD
                analysis.confidence = 0.5
                analysis.details = "页面包含下载相关内容"
                return analysis
            
            # 默认未知
            analysis.page_type = PageType.UNKNOWN
            analysis.details = "无法确定页面类型"
            
        except Exception as e:
            analysis.error_message = str(e)
            analysis.details = f"页面分析异常: {e}"
        
        return analysis


class EnhancedBrowserHandler:
    """
    增强版浏览器处理器
    
    特性：
    1. 智能页面分析
    2. 多选择器自动匹配
    3. 指数退避重试
    4. 异常处理
    5. 详细日志
    """
    
    # 重试配置
    DEFAULT_MAX_RETRIES = 3
    RETRY_DELAYS = [2, 4, 8]  # 指数退避
    
    # 等待配置
    PAGE_LOAD_TIMEOUT = 60000  # 60秒
    DOWNLOAD_WAIT_TIMEOUT = 60000  # 60秒
    
    def __init__(self, browser_pool=None):
        """
        初始化
        
        Args:
            browser_pool: 浏览器池实例（可选）
        """
        self.browser_pool = browser_pool
        self.analyzer = SmartPageAnalyzer()
        self.selectors = EnhancedDownloadSelectors()
        
        # 统计
        self.stats = {
            "total_attempts": 0,
            "success": 0,
            "failed": 0,
            "login_pages": 0,
            "captcha_pages": 0,
            "popups": 0,
        }
    
    def process(self, url: str, subject: str = "", 
                max_retries: int = DEFAULT_MAX_RETRIES,
                wait_time: int = 5) -> DownloadResult:
        """
        处理下载请求
        
        Args:
            url: 目标URL
            subject: 邮件主题（用于日志）
            max_retries: 最大重试次数
            wait_time: 页面加载额外等待时间
        
        Returns:
            DownloadResult: 下载结果
        """
        start_time = time.time()
        result = DownloadResult()
        
        logger.info(f"   📄 开始处理: {url[:60]}...")
        
        if not self.browser_pool or not self.browser_pool._initialized:
            result.status = DownloadStatus.FAILED
            result.message = "浏览器未初始化"
            return result
        
        # 获取页面
        page = None
        for retry in range(max_retries):
            self.stats["total_attempts"] += 1
            
            try:
                page = self.browser_pool.context.new_page()
                
                # 访问页面
                page.goto(url, wait_until='networkidle', timeout=self.PAGE_LOAD_TIMEOUT)
                time.sleep(wait_time)  # 额外等待
                
                # 智能页面分析
                analysis = self.analyzer.analyze(page, url)
                result.page_analysis = analysis
                
                logger.info(f"   🔍 页面分析: {analysis.page_type.value} ({analysis.confidence:.2f})")
                logger.info(f"      {analysis.details}")
                
                # 根据页面类型处理
                if analysis.page_type == PageType.LOGIN:
                    self.stats["login_pages"] += 1
                    result.status = DownloadStatus.NEED_LOGIN
                    result.message = f"需要登录认证 (置信度: {analysis.confidence:.2f})"
                    break
                
                elif analysis.page_type == PageType.CAPTCHA:
                    self.stats["captcha_pages"] += 1
                    result.status = DownloadStatus.NEED_CAPTCHA
                    result.message = f"需要验证码 (置信度: {analysis.confidence:.2f})"
                    break
                
                elif analysis.page_type == PageType.PDF_DIRECT:
                    # 直接下载PDF
                    download = self._handle_direct_pdf(page)
                    if download:
                        result.status = DownloadStatus.SUCCESS
                        result.download_path = download
                        result.message = "直接PDF下载成功"
                        break
                
                # 尝试下载
                download = self._try_download(page, analysis, url)
                
                if download:
                    result.status = DownloadStatus.SUCCESS
                    result.download_path = download
                    result.message = "下载成功"
                    self.stats["success"] += 1
                    break
                
                # 检查弹窗
                if analysis.popup_found:
                    self.stats["popups"] += 1
                    # 尝试处理弹窗
                    download = self._handle_popup(page)
                    if download:
                        result.status = DownloadStatus.SUCCESS
                        result.download_path = download
                        result.message = "弹窗确认后下载成功"
                        break
                
                # 未找到下载按钮
                result.status = DownloadStatus.NO_BUTTON
                result.message = f"未找到下载按钮: {analysis.details}"
                
                # 重试
                if retry < max_retries - 1:
                    delay = self.RETRY_DELAYS[min(retry, len(self.RETRY_DELAYS)-1)]
                    logger.warning(f"   ⚠️ 尝试 {retry+1}/{max_retries} 失败，{delay}秒后重试...")
                    time.sleep(delay)
                
            except Exception as e:
                error_msg = str(e)
                result.message = error_msg
                
                if "timeout" in error_msg.lower():
                    result.status = DownloadStatus.TIMEOUT
                elif "closed" in error_msg.lower():
                    # 浏览器可能已关闭，尝试重新初始化
                    logger.warning("   ⚠️ 浏览器连接已关闭")
                    result.status = DownloadStatus.RETRY_EXHAUSTED
                else:
                    result.status = DownloadStatus.FAILED
                
                if retry < max_retries - 1:
                    delay = self.RETRY_DELAYS[min(retry, len(self.RETRY_DELAYS)-1)]
                    logger.warning(f"   ⚠️ 错误: {error_msg}, {delay}秒后重试...")
                    time.sleep(delay)
            
            finally:
                if page:
                    try:
                        page.close()
                    except:
                        pass
        
        if result.status == DownloadStatus.FAILED and result.message:
            # 重试次数用完
            result.status = DownloadStatus.RETRY_EXHAUSTED
            self.stats["failed"] += 1
        
        result.retry_count = retry
        result.elapsed_time = time.time() - start_time
        
        # 记录最终结果
        if result.status == DownloadStatus.SUCCESS:
            logger.info(f"   ✅ 成功! ({result.elapsed_time:.1f}s)")
        else:
            logger.warning(f"   ❌ 失败: {result.message} ({result.elapsed_time:.1f}s)")
        
        return result
    
    def _try_download(self, page, analysis: PageAnalysis, url: str):
        """尝试下载"""
        
        # 1. 优先使用已检测到的选择器
        if analysis.detected_selectors:
            for selector in analysis.detected_selectors:
                try:
                    download = self._click_and_download(page, selector)
                    if download:
                        logger.info(f"   ✅ 使用检测到的选择器: {selector}")
                        return download
                except:
                    continue
        
        # 2. 尝试平台特定选择器
        platform_selectors = self.selectors.get_platform_selectors(url)
        for selector in platform_selectors:
            try:
                download = self._click_and_download(page, selector)
                if download:
                    logger.info(f"   ✅ 使用平台选择器: {selector}")
                    return download
            except:
                continue
        
        # 3. 尝试所有选择器
        all_selectors = self.selectors.get_all_selectors()
        for selector in all_selectors:
            try:
                locator = page.locator(selector)
                if locator.count() > 0:
                    download = self._click_and_download(page, selector)
                    if download:
                        logger.info(f"   ✅ 使用选择器: {selector}")
                        return download
            except:
                continue
        
        # 4. 尝试点击PDF链接
        try:
            pdf_links = page.locator('a[href$=".pdf"], a[href*=".pdf?"], a[href*="/pdf/"]')
            if pdf_links.count() > 0:
                for i in range(pdf_links.count()):
                    try:
                        with page.expect_download(timeout=self.DOWNLOAD_WAIT_TIMEOUT) as download_info:
                            pdf_links.nth(i).click()
                            time.sleep(3)
                        return download_info.value
                    except:
                        continue
        except:
            pass
        
        return None
    
    def _click_and_download(self, page, selector: str):
        """点击元素并等待下载"""
        try:
            locator = page.locator(selector)
            if locator.count() == 0:
                return None
            
            # 尝试点击
            for attempt in range(3):
                try:
                    with page.expect_download(timeout=self.DOWNLOAD_WAIT_TIMEOUT) as download_info:
                        locator.first.click()
                        time.sleep(5)  # 等待下载启动
                    
                    download = download_info.value
                    if download:
                        return download
                except Exception as click_err:
                    logger.debug(f"   点击尝试 {attempt+1}/3 失败: {click_err}")
                    time.sleep(2)
                    continue
            
            return None
        except Exception as e:
            logger.debug(f"   下载处理异常: {e}")
            return None
    
    def _handle_direct_pdf(self, page):
        """处理直接PDF"""
        try:
            page_url = page.url
            if page_url.lower().endswith('.pdf') or '.pdf?' in page_url:
                # 尝试触发下载
                with page.expect_download(timeout=self.DOWNLOAD_WAIT_TIMEOUT) as download_info:
                    page.goto(page_url)
                    time.sleep(3)
                return download_info.value
        except Exception as e:
            logger.debug(f"   直接PDF处理异常: {e}")
        return None
    
    def _handle_popup(self, page):
        """处理弹窗确认"""
        try:
            # 查找确认按钮
            confirm_selectors = [
                'button:has-text("确认")',
                'button:has-text("确定")',
                'button:has-text("是")',
                'a:has-text("确认")',
                'a:has-text("确定")',
                '[class*="confirm"]',
                '[class*="ok"]',
                'button[type="button"]:has-text("确定")',
            ]
            
            for selector in confirm_selectors:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0:
                        # 尝试在弹窗中查找
                        popup_locator = locator.first
                        
                        # 点击确认
                        with page.expect_download(timeout=self.DOWNLOAD_WAIT_TIMEOUT) as download_info:
                            popup_locator.click()
                            time.sleep(3)
                        
                        return download_info.value
                except:
                    continue
            
        except Exception as e:
            logger.debug(f"   弹窗处理异常: {e}")
        
        return None
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats.copy()


class EnhancedBrowserPool:
    """
    增强版浏览器池
    
    在原BrowserPool基础上增加了：
    1. 智能页面分析
    2. 增强的选择器匹配
    3. 更好的错误处理
    """
    
    def __init__(self):
        self.browser = None
        self.context = None
        self.playwright = None
        self._initialized = False
        self._lock = None
        self._page_count = 0
        
        # 增强处理器
        self.handler = None
    
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
            
            # 设置默认超时
            self.context.set_default_timeout(60000)
            
            self._initialized = True
            self._lock = __import__('threading').Lock()
            
            # 初始化增强处理器
            self.handler = EnhancedBrowserHandler(self)
            
            logger.info("🌐 增强版浏览器初始化完成")
            
        except Exception as e:
            logger.error(f"⚠️ 浏览器初始化失败: {e}")
            self._initialized = False
    
    def process_invoice(self, email_data: Dict, idx: int) -> Dict:
        """
        处理发票下载（增强版）
        
        Args:
            email_data: 包含 'url' 和 'subject' 的字典
            idx: 索引
        
        Returns:
            处理结果字典
        """
        with self._lock:
            if not self._initialized:
                return {"status": "failed", "reason": "浏览器未初始化"}
            
            # 检查是否需要重启
            self._should_restart_browser()
            
            url = email_data.get('url', '')
            subject = email_data.get('subject', '')
            
            if not url:
                return {"status": "failed", "reason": "无URL"}
            
            # 根据平台调整等待时间
            wait_time = 5
            url_lower = url.lower()
            if "nuonuo" in url_lower or "nnfp" in url_lower:
                wait_time = 8
            elif "hangtian" in url_lower or "航天" in subject:
                wait_time = 10
            
            # 使用增强处理器
            if self.handler:
                result = self.handler.process(url, subject, wait_time=wait_time)
                
                # 转换结果格式
                if result.status == DownloadStatus.SUCCESS:
                    return {
                        "status": "success",
                        "download": result.download_path,
                        "message": result.message,
                        "page_type": result.page_analysis.page_type.value if result.page_analysis else "unknown"
                    }
                else:
                    return {
                        "status": "failed",
                        "reason": result.message,
                        "page_type": result.page_analysis.page_type.value if result.page_analysis else "unknown"
                    }
            
            # 如果没有增强处理器，使用原来的逻辑
            return self._process_invoice_original(email_data, idx)
    
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
    
    def _process_invoice_original(self, email_data: Dict, idx: int) -> Dict:
        """原始处理逻辑（兼容）"""
        # 这里保留原来的处理逻辑作为后备
        # ... (与v7.2相同)
        return {"status": "failed", "reason": "使用增强处理器失败"}
    
    def close(self):
        """关闭浏览器"""
        logger.info("🌐 关闭增强版浏览器...")
        
        if self.handler:
            stats = self.handler.get_stats()
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
        
        logger.info("   ✅ 增强版浏览器已关闭")


# 便捷函数
def create_enhanced_handler(browser_pool) -> EnhancedBrowserHandler:
    """创建增强版处理器"""
    return EnhancedBrowserHandler(browser_pool)


def analyze_page(page, url: str = "") -> PageAnalysis:
    """分析页面类型（独立函数）"""
    analyzer = SmartPageAnalyzer()
    return analyzer.analyze(page, url)


# 测试入口
if __name__ == "__main__":
    # 简单测试
    print("Enhanced Browser Handler v1.0")
    print("=" * 50)
    print(f"可用选择器数量: {len(EnhancedDownloadSelectors.get_all_selectors())}")
    print(f"页面类型: {[t.value for t in PageType]}")
    print(f"下载状态: {[s.value for s in DownloadStatus]}")
