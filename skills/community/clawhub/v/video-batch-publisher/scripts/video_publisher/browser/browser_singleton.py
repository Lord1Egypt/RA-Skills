import os
import logging
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

logger = logging.getLogger(__name__)

class BrowserSingleton:
    """浏览器单例管理器 - 全局唯一浏览器实例，登录态持久化，多标签页管理"""
    
    _instance = None
    _browser: Browser = None
    _context: BrowserContext = None
    _page: Page = None
    _pages: dict = {}
    _playwright = None
    _debug_keep_browser = False
    
    PLATFORM_LIST = ["抖音", "小红书", "快手", "B站", "视频号"]
    
    PLATFORM_LOGIN_DETECTION = {
        "视频号": {
            "url_keywords": ["login.html", "/login"],
            "element_selectors": []
        },
        "抖音": {
            "url_keywords": [],
            "element_selectors": ["text=扫码登录", "text=我是创作者"]
        },
        "小红书": {
            "url_keywords": ["/login", "/signin"],
            "element_selectors": []
        },
        "快手": {
            "url_keywords": [],
            "element_selectors": ["text=立即登录", "text=登录"]
        },
        "B站": {
            "url_keywords": ["/login", "/signin"],
            "element_selectors": []
        }
    }
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserSingleton, cls).__new__(cls)
        return cls._instance
    
    def _validate_user_data_dir(self, user_data_dir):
        """校验用户数据目录的读写权限"""
        abs_dir = os.path.abspath(user_data_dir)
        os.makedirs(abs_dir, exist_ok=True)
        
        test_file = os.path.join(abs_dir, "test_write.tmp")
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write("test")
            os.remove(test_file)
            logger.info(f"用户数据目录校验通过: {abs_dir}")
            return abs_dir
        except Exception as e:
            raise RuntimeError(f"用户数据目录无读写权限: {abs_dir}, 错误: {str(e)}")
    
    def _is_context_healthy(self):
        """检查上下文是否健康"""
        if self._context is None:
            return False
        try:
            pages = self._context.pages
            return True
        except Exception as e:
            logger.warning(f"上下文检测失败，需要重建: {str(e)}")
            return False
    
    def _destroy_context(self):
        """销毁上下文"""
        try:
            if self._pages:
                for platform, page in list(self._pages.items()):
                    try:
                        page.close()
                    except:
                        pass
                self._pages = {}
            
            if self._page:
                try:
                    self._page.close()
                except:
                    pass
                self._page = None
            
            if self._context:
                try:
                    self._context.close()
                except:
                    pass
                self._context = None
            
            if self._browser:
                try:
                    self._browser.close()
                except:
                    pass
                self._browser = None
            
            logger.info("上下文已销毁")
        except Exception as e:
            logger.error(f"销毁上下文失败: {str(e)}")
    
    def init_browser(self, browser_config=None):
        """初始化浏览器实例（使用持久化上下文）"""
        if self._context is not None:
            if self._is_context_healthy():
                logger.info("浏览器上下文已初始化且健康，跳过重复初始化")
                return
            else:
                logger.warning("浏览器上下文已失效，正在重建...")
                self._destroy_context()
        
        if browser_config is None:
            browser_config = {
                "engine": "chromium",
                "headless": False,
                "user_data_dir": os.path.join(os.path.dirname(os.path.abspath(__file__)), "../browser_profile"),
                "timeout": 60000
            }
        
        try:
            self._playwright = sync_playwright().start()
            
            engine = browser_config.get("engine", "chromium")
            headless = browser_config.get("headless", False)
            user_data_dir = browser_config.get("user_data_dir", "./browser_profile")
            
            user_data_dir = self._validate_user_data_dir(user_data_dir)

            # 调试模式：发布完成后是否保留浏览器进程（默认 False=自动关闭）
            # 可在 browser_config.debug_keep_browser=true 时开启，便于手动排查
            self._debug_keep_browser = bool(browser_config.get("debug_keep_browser", self._debug_keep_browser))
            
            if engine == "chromium":
                self._context = self._playwright.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=headless,
                    viewport=None,
                    args=[
                        "--start-maximized",
                        "--disable-blink-features=AutomationControlled",
                        "--disable-extensions",
                        "--no-first-run",
                        "--no-default-browser-check",
                        "--disable-features=ChromeRefresh2023"
                    ],
                    slow_mo=50,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                self._browser = self._context.browser
            elif engine == "firefox":
                self._context = self._playwright.firefox.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=headless,
                    viewport=None,
                    args=["--start-maximized"]
                )
                self._browser = self._context.browser
            elif engine == "webkit":
                self._context = self._playwright.webkit.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=headless,
                    viewport=None
                )
                self._browser = self._context.browser
            else:
                raise ValueError(f"不支持的浏览器引擎：{engine}")
            
            try:
                browser = self._context.browser
                if browser:
                    for window in browser.windows:
                        window.maximize()
                    logger.info("浏览器窗口已最大化")
            except Exception as e:
                logger.warning(f"最大化浏览器窗口失败: {e}")
            
            logger.info(f"浏览器初始化成功，引擎: {engine}, 无头模式: {headless}")
            logger.info(f"用户数据目录: {user_data_dir}")
            
        except Exception as e:
            logger.error(f"浏览器初始化失败：{str(e)}")
            self.close_browser()
            raise
    
    def get_page(self) -> Page:
        if self._page is None:
            raise RuntimeError("浏览器未初始化，请先调用 init_browser()")
        return self._page
    
    def _create_adaptive_page(self):
        """创建自适应视口的页面"""
        page = self._context.new_page()
        page.set_default_timeout(60000)
        return page
    
    def get_platform_page(self, platform: str, force_new: bool = False) -> Page:
        """获取平台页面（支持强制重新创建）
        
        Args:
            platform: 平台名称
            force_new: 是否强制重新创建页面（用于批量发布时清理上一次发布后的页面状态）
        
        Returns:
            Page: 平台对应的页面对象
        """
        if force_new:
            if platform in self._pages:
                try:
                    self._pages[platform].close()
                    logger.info(f"已关闭 {platform} 旧标签页")
                except Exception as e:
                    logger.warning(f"关闭 {platform} 旧标签页失败: {str(e)}")
                del self._pages[platform]
            
            logger.info(f"为 {platform} 创建新标签页（强制）")
            page = self._create_adaptive_page()
            self._pages[platform] = page
            page.bring_to_front()
            return page
        
        if platform not in self._pages:
            logger.info(f"为 {platform} 创建新标签页")
            page = self._create_adaptive_page()
            self._pages[platform] = page
            page.bring_to_front()
            return page
        
        existing_page = self._pages[platform]
        try:
            _ = existing_page.url
        except Exception as e:
            logger.warning(f"{platform} 页面已关闭，重新创建: {str(e)}")
            page = self._create_adaptive_page()
            self._pages[platform] = page
            page.bring_to_front()
            return page
        
        existing_page.bring_to_front()
        return existing_page
    
    def is_login_state_valid(self, platform: str, bring_to_front: bool = True):
        """检查平台登录状态
        
        Args:
            platform: 平台名称
            bring_to_front: 是否切换到前台（默认True，检测时设为False避免频繁切换）
        """
        page = self.get_platform_page(platform)
        
        if not bring_to_front:
            pass
        else:
            page.bring_to_front()
        
        detection = self.PLATFORM_LOGIN_DETECTION.get(platform, {})
        
        # URL检测
        url_keywords = detection.get("url_keywords", [])
        current_url = page.url.lower()
        for keyword in url_keywords:
            if keyword.lower() in current_url:
                logger.warning(f"{platform} 登录态失效（URL包含: {keyword}）")
                return False
        
        # 元素检测
        element_selectors = detection.get("element_selectors", [])
        for selector in element_selectors:
            if page.locator(selector).count() > 0:
                logger.warning(f"{platform} 登录态失效（页面存在: {selector}）")
                return False
        
        return True   
        
    def get_context(self) -> BrowserContext:
        if self._context is None:
            raise RuntimeError("浏览器未初始化，请先调用 init_browser()")
        return self._context
    
    def get_browser(self) -> Browser:
        if self._browser is None:
            raise RuntimeError("浏览器未初始化，请先调用 init_browser()")
        return self._browser
    
    def new_page(self) -> Page:
        if self._context is None:
            raise RuntimeError("浏览器未初始化，请先调用 init_browser()")
        return self._create_adaptive_page()
    
    def close_browser(self):
        """关闭浏览器（带调试开关）"""
        if self._debug_keep_browser:
            logger.info("【调试模式】清空页面引用，释放上下文，保留浏览器进程")
            try:
                if self._pages:
                    for platform, page in list(self._pages.items()):
                        try:
                            page.close()
                        except:
                            pass
                    self._pages = {}
                
                if self._page:
                    try:
                        self._page.close()
                    except:
                        pass
                    self._page = None
                
                if self._context:
                    try:
                        self._context.close()
                    except:
                        pass
                    self._context = None
                
                if self._browser:
                    try:
                        self._browser.close()
                    except:
                        pass
                    self._browser = None
                
                logger.info("【调试模式】页面和上下文已释放，浏览器进程由用户手动关闭")
            except Exception as e:
                logger.error(f"调试模式释放资源失败: {str(e)}")
            return
        
        try:
            if self._page:
                self._page.close()
                self._page = None
            
            if self._context:
                self._context.close()
                self._context = None
            
            if self._browser:
                self._browser.close()
                self._browser = None
            
            if self._playwright:
                self._playwright.stop()
                self._playwright = None
            
            logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器时出错：{str(e)}")
    
    def set_debug_keep_browser(self, keep: bool):
        self._debug_keep_browser = keep
        logger.info(f"浏览器调试模式已设置为：{'常驻不关闭' if keep else '正常关闭'}")
    
    def wait_for_element(self, selector, timeout=30000):
        page = self.get_page()
        try:
            page.wait_for_selector(selector, timeout=timeout)
            logger.debug(f"元素 {selector} 已出现")
            return True
        except Exception as e:
            logger.error(f"等待元素 {selector} 超时：{str(e)}")
            return False
    
    def wait_for_element_visible(self, selector, timeout=30000):
        page = self.get_page()
        try:
            page.wait_for_selector(selector, state="visible", timeout=timeout)
            logger.debug(f"元素 {selector} 已可见")
            return True
        except Exception as e:
            logger.error(f"等待元素 {selector} 可见超时：{str(e)}")
            return False
    
    def wait_for_element_hidden(self, selector, timeout=30000):
        page = self.get_page()
        try:
            page.wait_for_selector(selector, state="hidden", timeout=timeout)
            logger.debug(f"元素 {selector} 已隐藏")
            return True
        except Exception as e:
            logger.error(f"等待元素 {selector} 隐藏超时：{str(e)}")
            return False
    
    def wait_for_navigation(self, timeout=5000):
        page = self.get_page()
        try:
            page.wait_for_load_state("domcontentloaded", timeout=timeout)
            logger.debug("页面DOM加载完成")
            return True
        except Exception as e:
            logger.warning(f"等待页面导航超时：{str(e)}")
            return False
    
    def select_option_by_text(self, selector, text, timeout=30000):
        page = self.get_page()
        try:
            page.click(selector, timeout=timeout)
            
            option_selector = f"{selector} option, .el-select-dropdown__item, .ant-select-dropdown-menu-item, .dropdown-option"
            page.wait_for_selector(option_selector, timeout=timeout)
            
            page.click(f'//*[text()="{text}"]', timeout=timeout)
            logger.debug(f"成功选择下拉选项：{text}")
            return True
        except Exception as e:
            logger.error(f"选择下拉选项 '{text}' 失败：{str(e)}")
            return False
    
    def handle_modal_dialog(self, accept=True, timeout=10000):
        page = self.get_page()
        try:
            dialog = page.wait_for_event("dialog", timeout=timeout)
            if accept:
                dialog.accept()
            else:
                dialog.dismiss()
            logger.debug(f"处理弹窗：{'接受' if accept else '拒绝'}")
            return True
        except Exception as e:
            logger.warning(f"未检测到弹窗或处理失败：{str(e)}")
            return False
    
    def take_screenshot(self, path=None):
        page = self.get_page()
        try:
            if path is None:
                import time
                path = f"./screenshots/screenshot_{int(time.time())}.png"
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            page.screenshot(path=path, full_page=True)
            logger.info(f"截图已保存：{path}")
            return path
        except Exception as e:
            logger.error(f"截图失败：{str(e)}")
            return None

browser_singleton = BrowserSingleton()

def init_browser(browser_config=None):
    return browser_singleton.init_browser(browser_config)

def get_page():
    return browser_singleton.get_page()

def get_browser_page():
    return browser_singleton.get_page()

def get_platform_page(platform: str, force_new: bool = False):
    return browser_singleton.get_platform_page(platform, force_new=force_new)

def is_login_state_valid(platform: str, bring_to_front: bool = True):
    return browser_singleton.is_login_state_valid(platform, bring_to_front=bring_to_front)

def get_context():
    return browser_singleton.get_context()

def get_browser():
    return browser_singleton.get_browser()

def new_page():
    return browser_singleton.new_page()

def close_browser():
    return browser_singleton.close_browser()

def set_debug_keep_browser(keep: bool):
    return browser_singleton.set_debug_keep_browser(keep)

def wait_for_element(selector, timeout=30000):
    return browser_singleton.wait_for_element(selector, timeout)

def wait_for_element_visible(selector, timeout=30000):
    return browser_singleton.wait_for_element_visible(selector, timeout)

def wait_for_element_hidden(selector, timeout=30000):
    return browser_singleton.wait_for_element_hidden(selector, timeout)

def wait_for_navigation(timeout=5000):
    return browser_singleton.wait_for_navigation(timeout)

def select_option_by_text(selector, text, timeout=30000):
    return browser_singleton.select_option_by_text(selector, text, timeout)

def handle_modal_dialog(accept=True, timeout=10000):
    return browser_singleton.handle_modal_dialog(accept, timeout)

def take_screenshot(path=None):
    return browser_singleton.take_screenshot(path)