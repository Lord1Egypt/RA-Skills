# -*- coding: utf-8 -*-
"""
精选联盟达人广场自动筛选脚本 v2.0
支持自动登录、网络拦截、达人数量控制
"""

import time
import json
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd


class DarenSearcher:
    """达人搜索器类"""

    # Chrome 用户数据目录，用于跨会话保持 cookie/session
    USER_DATA_DIR = os.path.join(os.path.expanduser('~'), '.daren_searcher_chrome_profile')

    def __init__(self):
        self.driver = None
        self.base_url = 'https://buyin.jinritemai.com/dashboard/servicehall/daren-square'
        self.login_url = 'https://buyin.jinritemai.com/union/sso/login'
        self.role_select_url = 'https://buyin.jinritemai.com/mpa/account/institution-role-select'
        self.api_url = 'https://buyin.jinritemai.com/api/authorStatData/seekAuthor'
        self.last_response_data = None
        self.all_authors = []
        self.filters = {}
        self._author_id_set = set()  # 去重用

    def setup_driver(self):
        """配置并启动浏览器（优先 Chrome，若未安装则使用系统默认浏览器）"""
        print('[INFO] 正在尝试启动 Chrome 浏览器...')

        # 确保用户数据目录存在
        os.makedirs(self.USER_DATA_DIR, exist_ok=True)

        chrome_options = Options()
        chrome_options.add_argument(
            f'--user-data-dir={self.USER_DATA_DIR}'
        )
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print('[INFO] Chrome 浏览器启动成功')
        except Exception as e:
            print(f'[WARN] Chrome 浏览器启动失败：{e}')
            print('[INFO] 尝试启动系统默认浏览器...')
            
            # 尝试使用 Edge 浏览器（基于 Chromium）
            try:
                from selenium.webdriver.edge.service import Service as EdgeService
                from selenium.webdriver.edge.options import Options as EdgeOptions
                
                edge_options = EdgeOptions()
                edge_options.add_argument('--disable-blink-features=AutomationControlled')
                edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
                edge_options.add_experimental_option('useAutomationExtension', False)
                
                self.driver = webdriver.Edge(options=edge_options)
                print('[INFO] Edge 浏览器启动成功（作为默认浏览器）')
            except Exception as edge_error:
                print(f'[WARN] Edge 浏览器启动失败：{edge_error}')
                
                # 尝试使用 Firefox 浏览器
                try:
                    from selenium.webdriver.firefox.service import Service as FirefoxService
                    from selenium.webdriver.firefox.options import Options as FirefoxOptions
                    
                    firefox_options = FirefoxOptions()
                    self.driver = webdriver.Firefox(options=firefox_options)
                    print('[INFO] Firefox 浏览器启动成功（作为默认浏览器）')
                except Exception as firefox_error:
                    print(f'[ERROR] Firefox 浏览器启动失败：{firefox_error}')
                    raise Exception('无法启动任何浏览器，请确保已安装 Chrome、Edge 或 Firefox 浏览器')
        
        self.driver.maximize_window()
        print('[INFO] 浏览器启动完成（cookie 将跨会话保留）')

    def _inject_early_interceptor(self):
        """通过 CDP 在新文档加载前注入 XHR 拦截器
        
        关键策略：
        - 页面的请求 SDK 覆盖了 XHR.prototype.open 和 send
        - 我们用更底层的 Object.defineProperty 来拦截 responseText getter
        - 这样无论 SDK 如何处理响应，我们都能拿到数据
        """
        interceptor_code = """
        window.__seekAuthorReqs = [];
        window.__seekAuthorResps = [];
        window.__darenInterceptorReady = true;
        (function() {
            // Hook open 以捕获 URL（比 send 更可靠，因为 SDK 可能在 open 中设置 _apiOptions）
            var origOpen = XMLHttpRequest.prototype.open;
            var origSend = XMLHttpRequest.prototype.send;
            
            XMLHttpRequest.prototype.open = function(method, url) {
                var self = this;
                try {
                    if (String(url).indexOf('seekAuthor') !== -1) {
                        self.__darenSeekUrl = url;
                    }
                } catch(e) {}
                return origOpen.apply(this, arguments);
            };
            
            XMLHttpRequest.prototype.send = function(body) {
                var self = this;
                var isSeekAuthor = false;
                try {
                    var url = (self._apiOptions && self._apiOptions.url) || self.__darenSeekUrl || '';
                    isSeekAuthor = String(url).indexOf('seekAuthor') !== -1;
                    if (isSeekAuthor) {
                        window.__seekAuthorReqs.push({url: url, time: Date.now()});
                    }
                } catch(e) {}
                
                if (isSeekAuthor) {
                    var checkInterval = setInterval(function() {
                        if (self.readyState === 4) {
                            clearInterval(checkInterval);
                            try {
                                window.__seekAuthorResps.push({
                                    url: (self._apiOptions && self._apiOptions.url) || self.__darenSeekUrl || '',
                                    status: self.status,
                                    body: self.responseText,
                                    time: Date.now()
                                });
                            } catch(e) {}
                        }
                    }, 50);
                }
                
                return origSend.apply(this, arguments);
            };
        })();
        """
        try:
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': interceptor_code})
            print('[INFO] CDP 早期拦截器已注册')
        except Exception as e:
            print(f'[WARN] 注册 CDP 拦截器失败: {e}')

    def _inject_network_interceptor(self):
        """在当前页面注入 XHR 拦截器（兼容旧流程）"""
        self._inject_early_interceptor()
        try:
            self.driver.execute_script("""
                if (!window.__darenInterceptorReady) {
                    window.__seekAuthorReqs = window.__seekAuthorReqs || [];
                    window.__seekAuthorResps = window.__seekAuthorResps || [];
                    var origAddEventListener = XMLHttpRequest.prototype.addEventListener;
                    XMLHttpRequest.prototype.addEventListener = function(type, listener, options) {
                        if (type === 'load') {
                            var wrappedListener = function(event) {
                                try {
                                    var url = (this._apiOptions && this._apiOptions.url) || this.__darenUrl || '';
                                    if (String(url).indexOf('seekAuthor') !== -1) {
                                        window.__seekAuthorResps.push({url: url, status: this.status, body: this.responseText});
                                    }
                                } catch(e) {}
                                return listener.call(this, event);
                            };
                            wrappedListener.__darenOriginal = listener;
                            return origAddEventListener.call(this, type, wrappedListener, options);
                        }
                        return origAddEventListener.call(this, type, listener, options);
                    };
                    var origSend = XMLHttpRequest.prototype.send;
                    XMLHttpRequest.prototype.send = function(body) {
                        try {
                            var url = (this._apiOptions && this._apiOptions.url) || this.__darenUrl || '';
                            if (String(url).indexOf('seekAuthor') !== -1) {
                                window.__seekAuthorReqs.push({url: url, time: Date.now()});
                            }
                        } catch(e) {}
                        return origSend.apply(this, arguments);
                    };
                    window.__darenInterceptorReady = true;
                }
            """)
        except Exception:
            pass

    def _get_intercepted_responses(self):
        """获取所有拦截到的 seekAuthor 响应"""
        try:
            resps = self.driver.execute_script('return window.__seekAuthorResps || [];')
            return resps or []
        except Exception:
            return []

    def _get_last_intercepted_response(self):
        """获取最后一次拦截到的 seekAuthor 响应数据"""
        try:
            resps = self.driver.execute_script('return window.__seekAuthorResps || [];')
            if resps:
                last = resps[-1]
                return json.loads(last['body'])
        except Exception:
            pass
        return None

    def _get_intercepted_data(self):
        """兼容旧接口"""
        return self._get_last_intercepted_response()

    def _clear_intercepted_data(self):
        """清除拦截到的请求和响应"""
        try:
            self.driver.execute_script("""
                window.__seekAuthorReqs = [];
                window.__seekAuthorResps = [];
            """)
        except Exception:
            pass

    def check_login_status(self):
        """检测当前是否已登录
        
        严格判定：只有检测到达人广场的核心业务内容才算已登录。
        落地页（douyinec.com）即使包含"招商""精选联盟"等营销文案，
        也不代表已登录——未登录的落地页也有这些文字。
        """
        current_url = self.driver.current_url.lower()

        # 未登录的URL标志
        login_indicators = ['login', 'sso', 'institution-role-select', 'passport']
        for indicator in login_indicators:
            if indicator in current_url:
                print(f'[INFO] 登录检测: URL包含"{indicator}"，判定为未登录')
                return False

        # 检查页面标题
        try:
            title = self.driver.title
            if '登录' in title:
                print(f'[INFO] 登录检测: 页面标题包含"登录"，判定为未登录')
                return False
        except Exception:
            pass

        # 检查页面内容 - 未登录标志
        page_source = self.driver.page_source
        login_text_indicators = ['请登录', '立即登录', '账号登录', '密码登录', '验证码登录',
                                  '请输入邮箱', '请输入密码', '请输入账号']
        for indicator in login_text_indicators:
            if indicator in page_source:
                print(f'[INFO] 登录检测: 页面包含"{indicator}"，判定为未登录')
                return False

        # 已登录的可靠标志：达人广场的核心业务UI元素
        # 这些元素只有在真正登录进入后台后才会出现，落地页不会有
        square_ui_indicators = ['daren-square', 'seekAuthor', '达人广场']
        has_square_ui = any(ind in page_source for ind in square_ui_indicators)
        if has_square_ui:
            print('[INFO] 登录检测: 检测到达人广场业务内容，判定为已登录')
            return True

        # 其他已登录页面的可靠标志（后台业务页面特有元素，非落地页营销文案）
        backend_indicators = ['筛选达人', '服务市场', '我的主页', '商品管理', '数据中心']
        has_backend = any(ind in page_source for ind in backend_indicators)
        if has_backend:
            print('[INFO] 登录检测: 检测到后台业务内容，判定为已登录')
            return True

        # 无法确定 → 未登录，走登录流程更安全
        print(f'[INFO] 登录检测: 未检测到已登录标志，判定为未登录 (URL: {self.driver.current_url[:80]})')
        return False

    def _check_session_valid(self):
        """检测 session 是否真正有效（cookie 存在但 session 过期的情况）

        检测方式：
        1. 页面是否有"用户未登录"弹窗/提示
        2. 检查网络请求是否返回 401/未登录错误
        3. 检查页面关键筛选器是否真实可交互（非空壳页面）
        """
        page_source = self.driver.page_source

        # 检测常见的 session 过期提示文案（必须是面向用户可见的提示，不是代码变量名）
        session_expired_indicators = [
            '用户未登录', '登录已过期', '登录失效', '请重新登录',
            'unauthorized',
            '登录状态已失效', '登录超时', '身份已过期',
        ]
        for indicator in session_expired_indicators:
            if indicator in page_source:
                print(f'[WARN] Session 校验: 页面包含"{indicator}"，session 可能已过期')
                return False

        # 检查页面是否是空壳页面（有达人广场 URL 但没有实际的筛选器/内容区域）
        try:
            has_filters = self.driver.execute_script("""
                // 检查是否有实际的筛选器 DOM 元素
                const triggers = document.querySelectorAll('[class*="dropMenuTitle"]');
                const labels = document.querySelectorAll('[class*="dropLabel"]');
                const cascader = document.querySelectorAll('[class*="selector_list_container"]');
                return (triggers.length > 0 || labels.length > 0 || cascader.length > 0);
            """)
            if not has_filters:
                print('[WARN] Session 校验: 页面无筛选器 DOM，session 可能已过期')
                return False
        except Exception:
            pass

        # 检查是否有弹窗遮罩（session 过期弹窗通常有遮罩层）
        try:
            has_modal = self.driver.execute_script("""
                const modals = document.querySelectorAll(
                    '.auxo-modal-mask, .auxo-modal-wrap, [class*="modal"], [class*="dialog"], [class*="toast"]'
                );
                for (const modal of modals) {
                    if (modal.offsetParent !== null || getComputedStyle(modal).display !== 'none') {
                        const text = modal.textContent || '';
                        if (text.includes('未登录') || text.includes('登录') || text.includes('过期') || text.includes('失效') || text.includes('重新登录')) {
                            return {found: true, text: text.substring(0, 100)};
                        }
                    }
                }
                return {found: false};
            """)
            if has_modal.get('found'):
                print(f'[WARN] Session 校验: 检测到登录弹窗："{has_modal.get("text", "")}"')
                return False
        except Exception:
            pass

        return True

    def _force_relogin(self, email, password):
        """强制重新登录：清除 cookie 后重新走完整登录流程

        当 session 过期但 cookie 仍存在时使用。清除所有相关 cookie，
        然后重新导航到登录页面完成登录。

        参数:
            email: 登录邮箱
            password: 登录密码
        返回:
            bool: 是否重新登录成功
        """
        print('[INFO] ====== 开始强制重新登录（清除 cookie）======')

        # 1. 清除所有 cookie
        try:
            self.driver.delete_all_cookies()
            print('[INFO] 已清除所有 cookie')
        except Exception as e:
            print(f'[WARN] 清除 cookie 时出错: {e}')

        # 2. 清除 localStorage 和 sessionStorage
        try:
            self.driver.execute_script("""
                try { localStorage.clear(); } catch(e) {}
                try { sessionStorage.clear(); } catch(e) {}
            """)
            print('[INFO] 已清除 localStorage/sessionStorage')
        except Exception:
            pass

        # 3. 导航到空白页，确保干净状态
        self.driver.get('about:blank')
        time.sleep(1)

        # 4. 重新注入拦截器
        self._inject_early_interceptor()

        # 5. 执行自动登录（强制走完整登录流程，跳过快捷检测）
        login_ok = self.auto_login(email, password, force_full_login=True)

        if login_ok:
            print('[INFO] 强制重新登录成功')
            time.sleep(2)

            # 6. 重新导航到达人广场
            logged_in = self.navigate_to_page()
            if logged_in:
                print('[INFO] 强制重新登录后成功到达达人广场')
                return True
            else:
                print('[ERROR] 强制重新登录后仍无法访问达人广场')
                return False
        else:
            print('[ERROR] 强制重新登录失败')
            return False

    def _ensure_logged_in(self, email, password):
        """确保处于有效登录状态，必要时自动重新登录

        综合检测：先 check_login_status（URL/页面内容），再 _check_session_valid（弹窗/session）。
        如果任何检测失败且有凭据，则执行 _force_relogin。

        参数:
            email: 登录邮箱（可选，为 None 时无法自动重登录）
            password: 登录密码（可选）
        返回:
            bool: 是否处于有效登录状态
        """
        # 第一层：基础登录状态检测
        logged_in = self.check_login_status()
        if not logged_in:
            if email and password:
                print('[INFO] 检测到未登录状态，执行强制重新登录...')
                return self._force_relogin(email, password)
            return False

        # 第二层：session 有效性检测
        session_valid = self._check_session_valid()
        if not session_valid:
            if email and password:
                print('[INFO] 检测到 session 过期，执行强制重新登录...')
                return self._force_relogin(email, password)
            print('[WARN] Session 已过期但未提供登录凭据，无法自动重新登录')
            return False

        print('[INFO] 登录状态校验通过（session 有效）')
        return True

    def _wait_page_ready(self, timeout=10):
        """等待页面 JS 渲染完成（非空 body）"""
        start = time.time()
        while time.time() - start < timeout:
            try:
                body = self.driver.find_element(By.TAG_NAME, 'body')
                if body.text.strip():
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        return False

    def auto_login(self, email, password, max_retries=3, force_full_login=False):
        """
        自动登录精选联盟
        
        完整流程：
        1. 选择招商团长身份
        1.5 检查是否直接弹出"请选择账号"（cookie有效时）或已登录成功
        2. 点击"邮箱登录"切换到邮箱登录方式
        3. 输入邮箱和密码
        4. 勾选"登录即代表同意"协议
        5. 点击登录按钮
        6. 处理"请选择账号"页面（如有）
        7. 处理验证码（如有）
        8. 等待登录成功
        """
        print('[INFO] 检测到未登录状态，开始自动登录...')

        # 先检查当前是否已经在登录页面
        current_url = self.driver.current_url.lower()
        already_on_login_page = any(kw in current_url for kw in ['login', 'sso', 'institution-role-select'])

        if not already_on_login_page:
            print('[INFO] 正在访问角色选择页面...')
            self.driver.get(self.role_select_url)
            time.sleep(3)

        # ============ 步骤1: 选择招商团长身份 ============
        if 'institution-role-select' in self.driver.current_url:
            print('[INFO] 正在选择招商团长身份...')
            role_selectors = [
                "//div[contains(text(), '招商团长')]",
                "//span[contains(text(), '招商团长')]",
                "//a[contains(text(), '招商团长')]",
                "//*[contains(@class, 'role') and contains(., '招商团长')]",
                "//*[contains(text(), '招商团长')]/ancestor::div[@role='button']",
                "//*[contains(text(), '招商团长')]/ancestor::a",
                "//*[contains(text(), '招商团长')]/ancestor::div[1]",
            ]

            role_clicked = False
            for selector in role_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for el in elements:
                        if el.is_displayed():
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                            time.sleep(0.3)
                            el.click()
                            role_clicked = True
                            print('[INFO] 已选择招商团长身份')
                            break
                    if role_clicked:
                        break
                except Exception:
                    continue

            if not role_clicked:
                print('[WARN] 未能自动选择身份，尝试继续...')

            # 等待页面跳转 & JS 渲染
            time.sleep(4)
            self._wait_page_ready(timeout=8)
            
            # 检查URL是否发生了变化
            current_url_after = self.driver.current_url
            print(f'[DEBUG] 点击招商团长后URL: {current_url_after}')
            
            # 如果还在角色选择页，再等待一段时间
            if 'institution-role-select' in current_url_after:
                print('[INFO] 仍在角色选择页，等待页面跳转...')
                time.sleep(5)
                current_url_after = self.driver.current_url
                print(f'[DEBUG] 再次等待后URL: {current_url_after}')

        # ============ 步骤1.5: 检查点击招商团长后的实际状态 ============
        # cookie 有效时，可能直接弹出"请选择账号"或已登录成功
        self.driver.switch_to.default_content()
        page_source = self.driver.page_source

        # 检查是否需要选择账号
        if '请选择账号' in page_source:
            print('[INFO] 检测到"请选择账号"页面（cookie有效，无需重新登录）')
            account_selected = self._handle_account_selection()
            if account_selected:
                print('[INFO] 已选择账号，等待进入系统...')
                time.sleep(3)
                # 等待登录完成后导航
                login_ok = self._wait_for_login_success(15)
                if login_ok:
                    print('[INFO] 登录成功！')
                    return True
            # 如果账号选择失败，继续尝试完整登录流程

        # 检查是否已经登录成功（跳过了登录步骤）
        # force_full_login=True 时跳过此检测，确保走完整登录流程
        if not force_full_login and self.check_login_status():
            print('[INFO] cookie 有效，已自动登录')
            return True

        # 检查是否有邮箱输入框（说明到了登录页）
        email_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder='请输入邮箱']")
        if not email_inputs:
            # 也检查是否已经到了达人广场等已登录页面
            current_url = self.driver.current_url
            if 'daren-square' in current_url or 'dashboard' in current_url or 'servicehall' in current_url:
                print('[INFO] 已到达业务页面，无需登录')
                return True
            # 如果页面仍然是空的或角色选择页，再等一会
            print('[INFO] 等待页面加载...')
            time.sleep(3)
            self._wait_page_ready(timeout=8)

        # ============ 步骤2: 切换到邮箱登录方式 ============
        print('[INFO] 正在切换到邮箱登录方式...')

        # 先尝试在主页面找邮箱登录tab
        email_tab_clicked = self._click_email_login_tab(self.driver)

        # 如果主页面没找到，检查iframe
        if not email_tab_clicked:
            iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
            if iframes:
                print(f'[INFO] 主页面未找到邮箱登录tab，检查 {len(iframes)} 个iframe...')
                for iframe_idx, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.default_content()
                        time.sleep(0.5)
                        WebDriverWait(self.driver, 5).until(
                            EC.frame_to_be_available_and_switch_to_it(iframe)
                        )
                        time.sleep(2)
                        email_tab_clicked = self._click_email_login_tab(self.driver)
                        if email_tab_clicked:
                            print(f'[INFO] 在iframe[{iframe_idx}]中点击了邮箱登录')
                            break
                    except Exception as ex:
                        print(f'[WARN] iframe[{iframe_idx}] 检查失败: {ex}')
                        try:
                            self.driver.switch_to.default_content()
                        except Exception:
                            pass

        if email_tab_clicked:
            print('[INFO] 已切换到邮箱登录方式')
            time.sleep(2)  # 等待邮箱输入框出现
        else:
            print('[INFO] 未找到邮箱登录tab，可能已经在邮箱登录页面')

        # ============ 步骤3: 输入邮箱和密码 ============
        print('[INFO] 正在查找登录输入框...')

        # 查找邮箱和密码输入框
        email_input, password_input = self._find_login_inputs()

        if email_input:
            email_input.clear()
            for char in email:
                email_input.send_keys(char)
                time.sleep(0.05)
            print('[INFO] 邮箱已填写')
        else:
            # 再次检查：可能页面仍在渲染，或者已经不需要登录了
            print('[WARN] 未找到邮箱输入框，检查当前状态...')
            time.sleep(3)
            self._wait_page_ready(timeout=5)
            
            # 重新检查是否已经到了"请选择账号"或已登录
            if '请选择账号' in self.driver.page_source:
                print('[INFO] 延迟检测到"请选择账号"页面')
                account_selected = self._handle_account_selection()
                if account_selected:
                    time.sleep(3)
                    login_ok = self._wait_for_login_success(15)
                    if login_ok:
                        print('[INFO] 登录成功！')
                        return True
            
            if self.check_login_status():
                print('[INFO] 检测到已登录状态')
                return True
            
            self._save_debug_screenshot('no_email_input')
            self._save_page_source('no_email_input')
            print('[ERROR] 自动登录失败，无法找到邮箱输入框')
            return False

        if password_input:
            password_input.clear()
            for char in password:
                password_input.send_keys(char)
                time.sleep(0.05)
            print('[INFO] 密码已填写')
        else:
            print('[WARN] 未找到密码输入框')
            self._save_debug_screenshot('no_password_input')
            print('[ERROR] 自动登录失败，无法找到密码输入框')
            return False

        time.sleep(0.5)

        # ============ 步骤4: 勾选"登录即代表同意"协议 ============
        print('[INFO] 正在勾选登录协议...')
        agreement_checked = self._check_agreement()
        if agreement_checked:
            print('[INFO] 已勾选登录协议')
        else:
            print('[WARN] 未找到协议勾选框，尝试继续...')

        time.sleep(0.5)

        # ============ 步骤5: 点击登录按钮 ============
        print('[INFO] 正在点击登录按钮...')
        login_clicked = self._click_login_button()

        if not login_clicked:
            # 尝试按回车键提交
            try:
                from selenium.webdriver.common.keys import Keys
                password_input.send_keys(Keys.ENTER)
                login_clicked = True
                print('[INFO] 已通过回车键提交登录')
            except Exception:
                print('[ERROR] 未找到登录按钮')
                self._save_debug_screenshot('no_login_button')
                return False

        time.sleep(3)

        # ============ 步骤6: 处理"请选择账号"页面 ============
        # 部分账号绑定了多个身份，登录后会弹出"请选择账号"让用户选择
        self.driver.switch_to.default_content()
        time.sleep(2)
        account_selected = self._handle_account_selection()
        if account_selected:
            print('[INFO] 已选择账号，继续登录流程...')
            time.sleep(3)

        # ============ 步骤7: 处理验证码 ============
        # 切回主页面检测
        self.driver.switch_to.default_content()
        time.sleep(1)

        page_after = self.driver.page_source
        # 也检查iframe中是否有验证码
        iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in iframes:
            try:
                self.driver.switch_to.default_content()
                WebDriverWait(self.driver, 3).until(
                    EC.frame_to_be_available_and_switch_to_it(iframe)
                )
                iframe_src = self.driver.page_source
                if '验证码' in iframe_src:
                    self.driver.switch_to.default_content()
                    break
            except Exception:
                self.driver.switch_to.default_content()

        page_after = self.driver.page_source
        if '验证码' in page_after:
            print('[INFO] 检测到验证码，请在弹出的浏览器中手动完成验证...')
            captcha_success = self._wait_for_login_success(120)
            if captcha_success:
                print('[INFO] 验证码验证通过，登录成功！')
                self.driver.switch_to.default_content()
                return True
            else:
                print('[ERROR] 验证码等待超时')
                return False

        # ============ 步骤8: 等待登录完成 ============
        print('[INFO] 等待登录完成...')
        login_success = self._wait_for_login_success(30)

        if login_success:
            print('[INFO] 登录成功！')
            self.driver.switch_to.default_content()
            return True
        else:
            print('[ERROR] 登录超时')
            self._save_debug_screenshot('login_timeout')
            return False

    def _click_email_login_tab(self, driver):
        """
        点击"邮箱登录"tab切换登录方式
        
        实际页面结构（通过Playwright确认）：
        - "手机登录" 和 "邮箱登录" 都是 LayoutTable 中的 StaticText
        - 需要通过JS点击包含"邮箱登录"文字的节点
        - 页面没有iframe，登录表单直接在主页面中
        """
        try:
            clicked = driver.execute_script("""
                // 查找包含"邮箱登录"文字的所有元素
                var elements = document.evaluate(
                    "//*[contains(text(), '邮箱登录')]", 
                    document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null
                );
                
                for (var i = 0; i < elements.snapshotLength; i++) {
                    var el = elements.snapshotItem(i);
                    // 优先选择文字完全匹配的（避免误点"手机登录"等）
                    if (el.textContent.trim() === '邮箱登录' || el.innerText.trim() === '邮箱登录') {
                        el.click();
                        return true;
                    }
                }
                
                // 如果没找到完全匹配，尝试点击包含该文字的父元素
                for (var i = 0; i < elements.snapshotLength; i++) {
                    var el = elements.snapshotItem(i);
                    // 找到最近的LayoutTable或可点击的父容器
                    var parent = el.closest('table') || el.closest('[role="tab"]') || el.parentElement;
                    if (parent) {
                        parent.click();
                        return true;
                    }
                }
                
                return false;
            """)
            return bool(clicked)
        except Exception as e:
            print(f'[WARN] 点击邮箱登录tab失败: {e}')
            return False

    def _find_login_inputs(self):
        """
        查找邮箱和密码输入框
        
        实际页面结构（通过Playwright确认）：
        - 页面没有iframe，登录表单直接在主页面
        - 邮箱输入框: textbox "请输入邮箱" [required]
        - 密码输入框: textbox "密码" [required]
        """
        email_input = None
        password_input = None

        # 邮箱输入框选择器（按优先级排序）
        email_selectors = [
            "input[placeholder='请输入邮箱']",
            "input[placeholder*='邮箱']",
            "input[type='email']",
            "input[name='email']",
            "input[name='account']",
            "input[name='username']",
            "#email",
        ]

        # 密码输入框选择器
        password_selectors = [
            "input[placeholder='密码']",
            "input[placeholder*='密码']",
            "input[type='password']",
            "input[name='password']",
            "#password",
        ]

        # 在主页面查找（实际页面没有iframe）
        for sel in email_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                for el in elements:
                    if el.is_displayed():
                        email_input = el
                        break
                if email_input:
                    break
            except Exception:
                continue

        for sel in password_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                for el in elements:
                    if el.is_displayed():
                        password_input = el
                        break
                if password_input:
                    break
            except Exception:
                continue

        # 如果主页面没找到，尝试iframe（兼容性）
        if not (email_input and password_input):
            iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
            if iframes:
                print(f'[INFO] 主页面未找到完整输入框，检查 {len(iframes)} 个iframe...')
                for iframe_idx, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.default_content()
                        time.sleep(0.5)
                        WebDriverWait(self.driver, 5).until(
                            EC.frame_to_be_available_and_switch_to_it(iframe)
                        )
                        time.sleep(2)

                        if not email_input:
                            for sel in email_selectors:
                                try:
                                    elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                                    for el in elements:
                                        if el.is_displayed():
                                            email_input = el
                                            print(f'[INFO] 在iframe[{iframe_idx}]中找到邮箱输入框')
                                            break
                                    if email_input:
                                        break
                                except Exception:
                                    continue

                        if not password_input:
                            for sel in password_selectors:
                                try:
                                    elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                                    for el in elements:
                                        if el.is_displayed():
                                            password_input = el
                                            print(f'[INFO] 在iframe[{iframe_idx}]中找到密码输入框')
                                            break
                                    if password_input:
                                        break
                                except Exception:
                                    continue

                        if email_input and password_input:
                            break

                    except Exception as ex:
                        print(f'[WARN] iframe[{iframe_idx}] 检查失败: {ex}')
                        try:
                            self.driver.switch_to.default_content()
                        except Exception:
                            pass
                        continue

        return email_input, password_input

    def _check_agreement(self):
        """
        勾选'登录即代表同意'协议复选框
        
        实际页面结构（通过Playwright确认）：
        - checkbox的label文本是空格" "，不是"登录即代表同意"
        - checkbox 和 "登录即代表同意" 文字是兄弟元素，不是父子关系
        - checkbox: input[type='checkbox'] [checked=false]
        - 文字: 单独的div/span包含"登录即代表同意"
        - 关键策略：直接查找页面上未勾选的第一个checkbox并点击
        """
        try:
            # 策略1：直接找页面上未勾选的checkbox（登录页面上通常只有一个）
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            for cb in checkboxes:
                if cb.is_displayed() and not cb.is_selected():
                    cb.click()
                    print('[INFO] 已通过checkbox选择器勾选协议')
                    return True
                elif cb.is_displayed() and cb.is_selected():
                    print('[INFO] 协议checkbox已勾选')
                    return True

            # 策略2：通过"登录即代表同意"文字找相邻的checkbox
            try:
                agreement_clicked = self.driver.execute_script("""
                    // 找到"登录即代表同意"文字节点
                    var nodes = document.evaluate(
                        "//*[contains(text(), '登录即代表同意')]", 
                        document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null
                    );
                    
                    for (var i = 0; i < nodes.snapshotLength; i++) {
                        var textNode = nodes.snapshotItem(i);
                        // 向上找容器，然后在容器中找checkbox
                        var parent = textNode.parentElement;
                        for (var level = 0; level < 5 && parent; level++) {
                            var cb = parent.querySelector('input[type="checkbox"]');
                            if (cb && !cb.checked) {
                                cb.click();
                                return true;
                            } else if (cb && cb.checked) {
                                return true;
                            }
                            // 也检查前面的兄弟节点
                            var prev = textNode.previousElementSibling || 
                                       (textNode.parentElement && textNode.parentElement.previousElementSibling);
                            while (prev) {
                                var prevCb = prev.querySelector ? prev.querySelector('input[type="checkbox"]') : null;
                                if (prevCb) {
                                    if (!prevCb.checked) prevCb.click();
                                    return true;
                                }
                                if (prev.tagName === 'INPUT' && prev.type === 'checkbox') {
                                    if (!prev.checked) prev.click();
                                    return true;
                                }
                                prev = prev.previousElementSibling;
                            }
                            parent = parent.parentElement;
                        }
                    }
                    return false;
                """)
                if agreement_clicked:
                    print('[INFO] 已通过JS勾选协议')
                    return True
            except Exception as e:
                print(f'[WARN] JS勾选协议失败: {e}')

        except Exception as e:
            print(f'[WARN] 查找协议checkbox失败: {e}')

        return False

    def _click_login_button(self):
        """点击登录按钮（实际页面：button "登录"，在主页面中，不在iframe内）"""
        login_selectors = [
            "//button[contains(text(), '登录')]",
            "//span[contains(text(), '登录')]/ancestor::button",
            "//div[contains(text(), '登录') and @role='button']",
            "//a[contains(text(), '登录')]",
            "button[type='submit']",
            ".login-btn",
            "#login-btn",
        ]

        for sel in login_selectors:
            try:
                if sel.startswith('//'):
                    elements = self.driver.find_elements(By.XPATH, sel)
                else:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                for el in elements:
                    if el.is_displayed():
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                        time.sleep(0.3)
                        el.click()
                        print('[INFO] 已点击登录按钮')
                        return True
            except Exception:
                continue

        return False

    def _handle_account_selection(self):
        """
        处理登录后的"请选择账号"页面

        实际DOM结构（通过debug脚本确认）：
        - 标题: <div class="index_cardTitle__xxxx">请选择账号</div>
        - 列表容器: <div class="index_roleList__xxxx">
        - 账号项: <div class="index_roleItem__xxxx">
          内含: 图标img + 介绍div(index_intro) + 名称div(index_introName) + 箭头img
        - 返回: <div class="index_backBar__xxxx">返回</div>
        - 注意：账号项没有 role="button"，不能用 role 选择器
        """
        try:
            page_source = self.driver.page_source
            if '请选择账号' not in page_source:
                return False

            print('[INFO] 检测到"请选择账号"页面，正在选择第二个账号...')

            # 等待账号列表加载
            time.sleep(2)

            # 策略1: 通过精确的 class 选择器找 roleItem（最可靠）
            # 实际 class 含有 "roleItem"，通过 CSS class 通配符匹配
            role_item_selectors = [
                "div[class*='roleItem']",
                "div[class*='index_roleItem']",
            ]

            for sel in role_item_selectors:
                try:
                    items = self.driver.find_elements(By.CSS_SELECTOR, sel)
                    visible_items = [item for item in items if item.is_displayed()]
                    # 选择第二个账号（index=1）
                    if len(visible_items) >= 2:
                        target = visible_items[1]
                    elif len(visible_items) == 1:
                        print('[WARN] 账号列表只有一个，选择第一个')
                        target = visible_items[0]
                    else:
                        print(f'[WARN] 未找到可见账号项（共{len(items)}个，0个可见）')
                        continue

                    # 获取账号名称（在 index_introName 子元素中）
                    try:
                        name_el = target.find_element(By.CSS_SELECTOR, "div[class*='introName']")
                        name = name_el.text.strip()
                    except Exception:
                        name = target.text.strip()[:20]
                    
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", target)
                    time.sleep(0.5)
                    target.click()
                    print(f'[INFO] 已选择账号: {name}')
                    return True
                except Exception:
                    continue

            # 策略2: 通过JS在 roleList 容器内找可点击的子项
            clicked = self.driver.execute_script("""
                // 找账号列表容器
                var listContainer = document.querySelector('div[class*="roleList"]');
                if (!listContainer) {
                    // 也尝试通过标题找到相邻的列表
                    var titleEl = document.querySelector('div[class*="cardTitle"]');
                    if (titleEl) {
                        var parent = titleEl.nextElementSibling;
                        if (parent) listContainer = parent;
                    }
                }
                if (!listContainer) return false;
                
                // 在列表容器中找账号项
                var items = listContainer.querySelectorAll('div[class*="roleItem"]');
                if (items.length === 0) {
                    // 回退：找所有直接子div
                    items = listContainer.children;
                }
                
                // 收集所有可见的账号项（排除返回按钮）
                var visibleItems = [];
                for (var i = 0; i < items.length; i++) {
                    var el = items[i];
                    if (el.offsetParent !== null && el.textContent.trim().length > 1) {
                        if (el.className.indexOf('backBar') !== -1) continue;
                        if (el.textContent.trim() === '返回') continue;
                        visibleItems.push(el);
                    }
                }
                if (visibleItems.length === 0) return false;
                
                // 选择第二个账号（index=1），如果只有一个则选第一个
                var target = visibleItems.length >= 2 ? visibleItems[1] : visibleItems[0];
                target.click();
                var nameEl = target.querySelector('div[class*="introName"]');
                var name = nameEl ? nameEl.textContent.trim() : target.textContent.trim().substring(0, 20);
                return name;
            """)
            
            if clicked:
                print(f'[INFO] 已通过JS选择账号: {str(clicked)[:30]}')
                return True

            # 策略3: 回退 - 找所有可见 div 中非"返回"且文字较长的
            clicked = self.driver.execute_script("""
                var EXCLUDE_TEXTS = ['返回', '取消', '关闭', '跳过', '请选择账号', '欢迎来到精选联盟', '高效撮合促增长'];
                
                function isExclude(text) {
                    var t = text.trim();
                    for (var i = 0; i < EXCLUDE_TEXTS.length; i++) {
                        if (t === EXCLUDE_TEXTS[i]) return true;
                    }
                    return false;
                }
                
                // 找所有含 roleItem class 的元素
                var allItems = document.querySelectorAll('[class*="roleItem"]');
                for (var i = 0; i < allItems.length; i++) {
                    var el = allItems[i];
                    if (el.offsetParent !== null && !isExclude(el.textContent) && el.textContent.trim().length > 1) {
                        el.click();
                        return el.textContent.trim().substring(0, 30);
                    }
                }
                
                return false;
            """)
            
            if clicked:
                print(f'[INFO] 已通过回退策略选择账号: {str(clicked)[:30]}')
                return True

            print('[WARN] 找到"请选择账号"页面但未能自动选择账号')
            self._save_debug_screenshot('account_selection')
            self._save_page_source('account_selection')
            return False

        except Exception as e:
            print(f'[WARN] 处理账号选择页面失败: {e}')
            return False

    def _wait_for_login_success(self, timeout):
        """等待登录成功（页面跳转）"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                current_url = self.driver.current_url
                if 'dashboard' in current_url or 'daren-square' in current_url:
                    return True
                if self.check_login_status():
                    return True
            except Exception:
                pass
            time.sleep(1)
        return False

    def _wait_for_manual_action(self, timeout):
        """等待用户手动操作"""
        print(f'[INFO] 等待用户手动操作（最长 {timeout} 秒）...')
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_login_status():
                print('[INFO] 检测到登录成功')
                return True
            time.sleep(2)
        return False

    def _save_debug_screenshot(self, name):
        """保存调试截图"""
        try:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            path = os.path.join(desktop, f'debug_{name}_{int(time.time())}.png')
            self.driver.save_screenshot(path)
            print(f'[INFO] 调试截图已保存: {path}')
        except Exception:
            pass

    def _save_page_source(self, name):
        """保存页面源码用于调试"""
        try:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            path = os.path.join(desktop, f'debug_{name}_{int(time.time())}.html')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            print(f'[INFO] 页面源码已保存: {path}')
        except Exception:
            pass

    def navigate_to_page(self):
        """导航到达人广场页面，并检测登录状态"""
        print('[INFO] 正在访问达人广场页面...')
        self.driver.get(self.base_url)

        # 等待页面初始加载
        wait = WebDriverWait(self.driver, 30)
        try:
            wait.until(lambda d: d.execute_script('return document.readyState;') == 'complete')
        except Exception as e:
            print('[WARN] 等待页面超时: ' + str(e))

        # 额外等待重定向完成（有些页面会先加载再redirect）
        print('[INFO] 等待页面跳转稳定...')
        time.sleep(5)

        # 多轮检测登录状态（页面可能在加载后发生变化）
        print('[INFO] 检测登录状态...')
        logged_in = self.check_login_status()

        # 如果首次检测无法确定，检查是否被重定向到落地页
        if not logged_in:
            current_url = self.driver.current_url.lower()
            # 落地页特征：douyinec.com 但不是登录页，也不是达人广场
            if ('douyinec.com' in current_url and 'login' not in current_url 
                    and 'daren' not in current_url and 'servicehall' not in current_url):
                print('[INFO] 当前在落地页，尝试重新导航到达人广场...')
                self.driver.get(self.base_url)
                time.sleep(8)
                logged_in = self.check_login_status()

        # 如果仍未确定，再等几秒重试
        if not logged_in:
            current_url = self.driver.current_url.lower()
            if 'daren' in current_url or 'servicehall' in current_url or 'buyin' in current_url:
                print('[INFO] 首次检测未确定，等待页面充分加载后重试...')
                time.sleep(5)
                logged_in = self.check_login_status()

        if logged_in:
            # 已登录，注入拦截器
            self._inject_network_interceptor()
            print('[INFO] 页面加载完成，已登录')
            return True
        else:
            print('[INFO] 检测到未登录状态')
            return False

    def apply_filters(self, filters):
        """应用筛选条件
        
        实际页面 DOM 结构（通过 debug 脚本确认）：
        - 类目选择: <span class="index__valueItem___xcGQU">服饰内衣</span> — 直接点击
        - 范围筛选(直播观看人数/粉丝量): auxo-dropdown-trigger → 弹出下拉面板 → 预设范围选项
          下拉面板: div.auxo-dropdown，选项: div.index__dropItem___2QsJG
          直播观看人数预设: 全部、100以下、100-1000、1000-1w、1w以上
          粉丝量预设: 全部、1w以下、1w-10w、10w-100w、100w以上
        - 达人等级/达人性别: auxo-dropdown-trigger → 弹出下拉面板 → 选项
        - 没有 button，所有交互都是 div/span 点击
        """
        self.filters = filters
        print('[INFO] 开始应用筛选条件...')

        # 1. 选择主推类目（直接点击 valueItem span）
        if filters.get('category'):
            self._select_category(filters['category'])
            time.sleep(2)

        # 2. 设置带货数据 - 场均销售额/场均结算额（下拉选择预设范围）
        if filters.get('avg_settlement'):
            # 先尝试场均销售额，如果找不到再尝试场均结算额
            success = self._select_dropdown_option('场均销售额', filters['avg_settlement'])
            if not success:
                print('[INFO] 场均销售额未找到，尝试场均结算额...')
                self._select_dropdown_option('场均结算额', filters['avg_settlement'])
            time.sleep(2)

        # 2b. 设置带货数据 - 直播观看人数（下拉选择预设范围）
        if filters.get('live_viewers'):
            self._select_dropdown_option('直播观看人数', filters['live_viewers'])
            time.sleep(2)

        # 2c. 设置带货数据 - 直播GPM（下拉选择预设范围）
        if filters.get('live_gpm'):
            self._select_dropdown_option('直播GPM', filters['live_gpm'])
            time.sleep(2)

        # 2d. 设置带货数据 - 直播商品均价（下拉选择预设范围）
        if filters.get('live_avg_price'):
            self._select_dropdown_option('直播商品均价', filters['live_avg_price'])
            time.sleep(2)

        # 3. 设置粉丝数据 - 粉丝数/粉丝量（下拉选择预设范围）
        # 先尝试"粉丝数"，如果页面上没有这个筛选条件，再尝试"粉丝量"
        followers_value = filters.get('followers') or filters.get('fans_count')
        if followers_value:
            success = self._select_dropdown_option('粉丝数', followers_value)
            if not success:
                print('[INFO] 页面上没有"粉丝数"筛选条件，尝试使用"粉丝量"筛选条件')
                success = self._select_dropdown_option('粉丝量', followers_value)
            if success:
                time.sleep(2)

        # 4. 设置粉丝数据 - 粉丝年龄（下拉选择）
        if filters.get('fan_age'):
            self._select_dropdown_option('粉丝年龄', filters['fan_age'])
            time.sleep(2)

        # 5. 设置粉丝数据 - 粉丝性别（下拉选择）
        if filters.get('fan_gender'):
            self._select_dropdown_option('粉丝性别', filters['fan_gender'])
            time.sleep(2)

        # 6. 设置粉丝数据 - 粉丝地区（下拉选择）
        if filters.get('fan_region'):
            self._select_dropdown_option('粉丝地区', filters['fan_region'])
            time.sleep(2)

        # 7. 设置八大人群（下拉选择）
        if filters.get('crowd'):
            self._select_dropdown_option('八大人群', filters['crowd'])
            time.sleep(2)

        # 8. 选择达人属性 - 达人等级（下拉选择）
        if filters.get('level'):
            self._select_dropdown_option('达人等级', filters['level'])
            time.sleep(2)

        # 9. 选择达人性别（下拉选择）
        if filters.get('gender'):
            self._select_dropdown_option('达人性别', filters['gender'])
            time.sleep(2)

        # 10. 选择内容类型（下拉选择）
        if filters.get('content_type'):
            self._select_dropdown_option('内容类型', filters['content_type'])
            time.sleep(2)

        # 11. 选择达人地区（级联选择器：省份 → 城市）
        if filters.get('author_region'):
            self._select_author_region(filters['author_region'])
            time.sleep(2)

        # 12. 是否签约机构（下拉选择）
        if filters.get('signed_agency'):
            self._select_dropdown_option('是否签约机构', filters['signed_agency'])
            time.sleep(2)

        # 13. 设置标签类条件（复选框勾选）
        # 标签条件映射
        tag_filters = [
            ('high_settlement_rate', filters.get('high_settlement_rate')), # 结算率高
            ('high_reply_rate', filters.get('high_reply_rate')),       # 回复率高
            ('has_contact', filters.get('has_contact')),               # 有联系方式
            ('pure_commission', filters.get('pure_commission')),       # 纯佣达人
            ('star', filters.get('star')),                             # 明星
            ('dark_horse', filters.get('dark_horse')),                 # 黑马达人
        ]
        
        for tag_key, value in tag_filters:
            if value is not None:
                TagCheckboxSelector.select_tag_checkbox(self.driver, tag_key, value)
                time.sleep(1)

        # 所有条件设置完成，等待接口响应
        print('[INFO] 所有筛选条件已应用，等待数据加载...')
        
        # 等待最后一次筛选请求完成
        time.sleep(6)
        
        # 验证拦截器是否捕获到了 seekAuthor 响应
        resps = self._get_intercepted_responses()
        if resps:
            print(f'[INFO] 拦截器已捕获 {len(resps)} 个 seekAuthor 响应')
        else:
            print('[WARN] 拦截器未捕获到 seekAuthor 响应')

    def _select_category(self, category):
        """选择主推类目
        
        DOM: <span class="index__valueItem___xcGQU">服饰内衣</span>
        直接点击文字精确匹配的 span 即可。
        注意不能用 XPath contains，否则"服饰内衣"会匹配到"服饰内衣鞋包"等。
        """
        print(f'[INFO] 正在选择类目：{category}')
        clicked = self.driver.execute_script("""
            // 精确匹配 class 含 valueItem 的 span/div
            var items = document.querySelectorAll("span[class*='valueItem'], div[class*='valueItem']");
            for (var i = 0; i < items.length; i++) {
                if (items[i].textContent.trim() === arguments[0]) {
                    items[i].click();
                    return true;
                }
            }
            return false;
        """, category)

        if clicked:
            print(f'[INFO] 已选择类目：{category}')
        else:
            print(f'[WARN] 未找到类目选项：{category}')
            self._save_debug_screenshot('category_not_found')

    def _select_author_region(self, region_name):
        """选择达人地区（级联选择器：省份 → 城市）

        达人地区的触发器是 dropLabel（不是 dropMenuTitle），点击后弹出 auxo-cascader 级联选择器。
        region_name 格式：
          - "北京" → 自动选择"北京 → 北京"（直辖市省份与城市同名时自动匹配）
          - "广东 广州" → 选择"广东 → 广州"
          - "广东" → 选择"广东 → 广州"（自动选择第一级下的第一个城市）
        注意：必须选择第二级城市，否则筛选条件不会生效。
        """
        print(f'[INFO] 正在选择 达人地区：{region_name}')

        # 1. 找到并点击"达人地区"的 dropLabel
        clicked = self.driver.execute_script("""
            const allSpans = document.querySelectorAll('span');
            for (const s of allSpans) {
                if (s.textContent.trim() === '达人地区' && s.children.length === 0) {
                    const rect = s.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        const dropLabel = s.parentElement;
                        if (dropLabel && (dropLabel.className.includes('dropLabel') || dropLabel.className.includes('droparea'))) {
                            dropLabel.scrollIntoView({block: 'center'});
                            dropLabel.click();
                            return true;
                        }
                    }
                }
            }
            return false;
        """)

        if not clicked:
            print('[WARN] 未找到达人地区触发器')
            self._save_debug_screenshot('author_region_not_found')
            return

        time.sleep(1.5)

        # 2. 解析省份和城市（支持空格和破折号分隔）
        region_name = region_name.strip().replace('-', ' ')  # 将破折号替换为空格
        parts = region_name.split(None, 1)  # 按空格分割，最多2部分
        province = parts[0]
        city = parts[1] if len(parts) > 1 else None  # 如果没指定城市，后面会自动选择第一个

        # 3. 在级联选择器中选择省份
        province_clicked = self.driver.execute_script("""
            const province = arguments[0];
            const cascader = document.querySelector('.auxo-cascader-menus');
            if (!cascader) return {success: false, error: 'cascader not found'};

            const items = cascader.querySelectorAll('li.auxo-cascader-menu-item');
            for (const item of items) {
                const title = item.getAttribute('title') || item.textContent.trim();
                if (title === province) {
                    item.click();
                    return {success: true, title: title};
                }
            }
            return {success: false, error: 'province not found', availableProvinces: Array.from(items).map(i => i.getAttribute('title') || i.textContent.trim())};
        """, province)

        if not province_clicked.get('success'):
            print(f'[WARN] 未找到省份选项：{province}，可用省份：{province_clicked.get("availableProvinces", [])[:10]}')
            # 关闭 cascader
            self.driver.execute_script("document.body.click();")
            return

        print(f'[INFO] 已选择省份：{province_clicked["title"]}')
        time.sleep(1.5)

        # 4. 选择第二级城市（必须选择，否则筛选不生效）
        city_clicked = self.driver.execute_script("""
            const city = arguments[0];  // 可能为 null
            const cascader = document.querySelector('.auxo-cascader-menus');
            if (!cascader) return {success: false, error: 'cascader not found after province click'};

            // 查找所有菜单列，取第二列（城市列）
            const menus = cascader.querySelectorAll('.auxo-cascader-menu');
            if (menus.length < 2) return {success: false, error: 'no city menu found', menuCount: menus.length};

            const cityMenu = menus[menus.length - 1]; // 最后一列
            const items = cityMenu.querySelectorAll('li.auxo-cascader-menu-item');

            // 如果指定了城市名，精确匹配；否则自动选第一个
            let targetItem = null;
            if (city) {
                for (const item of items) {
                    const title = item.getAttribute('title') || item.textContent.trim();
                    if (title === city) {
                        targetItem = item;
                        break;
                    }
                }
            } else {
                // 未指定城市，选第一个
                targetItem = items[0];
            }

            if (targetItem) {
                targetItem.click();
                const title = targetItem.getAttribute('title') || targetItem.textContent.trim();
                return {success: true, title: title, autoSelected: !city};
            }

            return {
                success: false,
                error: 'city not found',
                availableCities: Array.from(items).map(i => i.getAttribute('title') || i.textContent.trim())
            };
        """, city)

        if not city_clicked.get('success'):
            print(f'[WARN] 未找到城市选项：{city or "(自动)"}，可用城市：{city_clicked.get("availableCities", [])[:10]}')
        else:
            auto_tag = "（自动选择）" if city_clicked.get('autoSelected') else ""
            print(f'[INFO] 已选择城市：{city_clicked["title"]}{auto_tag}')

        # 5. 关闭 cascader（点击页面其他位置）
        time.sleep(0.5)
        self.driver.execute_script("document.body.click();")
        time.sleep(0.5)

        print(f'[INFO] 已选择 达人地区：{province} → {city_clicked.get("title", "未知")}')

    def _select_dropdown_option(self, trigger_text, value):
        """通用下拉选择方法
        
        交互流程：
        1. 找到 auxo-dropdown-trigger（class 含 dropMenuTitle）并点击
        2. 等待下拉面板出现（class 含 auxo-dropdown）
        3. 在面板中找到匹配的选项并点击
        
        参数:
            trigger_text: 下拉触发器的文字（如"直播观看人数"、"达人等级"）
            value: 要选择的值，支持多种格式:
                - 字符串: "LV2"、"女" — 精确匹配选项文字
                - 列表 [min, max]: [100, 1000] — 自动匹配预设范围
                  预设范围映射: 100以下、100-1000、1000-1w、1w以上（直播观看人数）
                               10w以下、10w-100w、100w-300w、300w-500w、500w-1000w、1000w以上（粉丝量/粉丝数）
        """
        # 确定 options 文本
        if isinstance(value, list) and len(value) == 2:
            option_text = self._range_to_option_text(trigger_text, value[0], value[1])
        else:
            option_text = str(value)
        
        # 去除空格，处理"1w 以下"和"1w以下"的差异
        option_text = option_text.replace(' ', '')

        print(f'[INFO] 正在选择 {trigger_text}：{option_text}')

        # 步骤1: 点击下拉触发器
        trigger_clicked = self.driver.execute_script("""
            var triggers = document.querySelectorAll("div[class*='dropMenuTitle']");
            for (var i = 0; i < triggers.length; i++) {
                var t = triggers[i];
                // 精确匹配触发器文字（避免"达人性别"匹配到"粉丝性别"）
                var textSpan = t.querySelector("span[class*='dropMenuTitleText']") || t;
                var text = textSpan.textContent.trim();
                if (text === arguments[0] || text.indexOf(arguments[0]) === 0) {
                    t.click();
                    return true;
                }
            }
            return false;
        """, trigger_text)

        if not trigger_clicked:
            print(f'[WARN] 未找到下拉触发器：{trigger_text}')
            self._save_debug_screenshot(f'trigger_not_found_{trigger_text}')
            return False

        # 步骤2: 等待下拉面板出现（最多3秒）
        panel_found = False
        for wait_i in range(6):
            time.sleep(0.5)
            panel_found = self.driver.execute_script("""
                // 查找可见的下拉面板（auxo-dropdown 且有实际内容）
                var dropdowns = document.querySelectorAll("div[class*='auxo-dropdown']");
                for (var i = 0; i < dropdowns.length; i++) {
                    var d = dropdowns[i];
                    var rect = d.getBoundingClientRect();
                    // 排除触发器本身（高度约24-34px），只找面板（高度>50px）
                    // y 阈值设为 100（原来 200 可能在某些布局下不满足）
                    if (rect.width > 50 && rect.height > 50 && rect.y > 100) {
                        return true;
                    }
                }
                // 也检查是否有 auxo-dropdown-open 标记
                var openEl = document.querySelector("div.auxo-dropdown-open");
                if (openEl) {
                    var r = openEl.getBoundingClientRect();
                    if (r.width > 50 && r.height > 50) return true;
                }
                // 也检查 slide-up-appear 动画状态（面板正在打开）
                var appearEl = document.querySelector("div[class*='slide-up-appear']");
                if (appearEl) {
                    var ra = appearEl.getBoundingClientRect();
                    if (ra.width > 50 && ra.height > 50) return true;
                }
                return false;
            """)
            if panel_found:
                break

        if not panel_found:
            # 调试输出
            debug_info = self.driver.execute_script("""
                var dropdowns = document.querySelectorAll("div[class*='auxo-dropdown']");
                var info = [];
                for (var i = 0; i < dropdowns.length; i++) {
                    var d = dropdowns[i];
                    var rect = d.getBoundingClientRect();
                    info.push({
                        class: d.className.substring(0, 80),
                        w: Math.round(rect.width),
                        h: Math.round(rect.height),
                        y: Math.round(rect.y),
                        text: d.textContent.trim().substring(0, 100)
                    });
                }
                // 也查找 dropMenuTitle 的状态
                var triggers = document.querySelectorAll("div[class*='dropMenuTitle']");
                var triggerInfo = [];
                for (var j = 0; j < triggers.length; j++) {
                    var t = triggers[j];
                    triggerInfo.push({
                        text: t.textContent.trim().substring(0, 20),
                        class: t.className.substring(0, 80),
                        isOpen: t.className.indexOf('open') !== -1
                    });
                }
                return JSON.stringify({dropdowns: info, triggers: triggerInfo});
            """)
            if debug_info:
                import json as _json
                try:
                    dbg = _json.loads(debug_info)
                    print(f'[DEBUG] Dropdowns: {_json.dumps(dbg.get("dropdowns", [])[:5], ensure_ascii=False)[:300]}')
                    print(f'[DEBUG] Triggers: {_json.dumps(dbg.get("triggers", [])[:5], ensure_ascii=False)[:300]}')
                except:
                    pass
            print(f'[WARN] 下拉面板未出现：{trigger_text}')
            self.driver.find_element(By.TAG_NAME, 'body').click()
            return False

        # 步骤3: 在下拉面板中选择选项
        option_clicked = self.driver.execute_script("""
            var targetText = arguments[0];
            
            // 查找所有可见的下拉面板
            var dropdowns = document.querySelectorAll("div[class*='auxo-dropdown']");
            var panels = [];
            for (var i = 0; i < dropdowns.length; i++) {
                var d = dropdowns[i];
                var rect = d.getBoundingClientRect();
                if (rect.width > 50 && rect.height > 50 && rect.y > 100) {
                    panels.push(d);
                }
            }
            
            for (var p = 0; p < panels.length; p++) {
                var panel = panels[p];
                
                // 查找选项 — 支持两种面板类型:
                // 1. 单选面板: div[class*='dropItem'] (达人等级、达人性别等)
                // 2. 多选面板: div[class*='dropMultiItem'] (直播观看人数、粉丝量等)
                var items = panel.querySelectorAll(
                    "div[class*='dropItem'], div[class*='dropMultiItem'], " +
                    "li, [class*='option'], [class*='menu-item']"
                );
                
                // 策略1: 精确匹配选项中的 span 文字
                for (var i = 0; i < items.length; i++) {
                    var item = items[i];
                    var innerSpan = item.querySelector('span');
                    var text = innerSpan ? innerSpan.textContent.trim() : item.textContent.trim();
                    if (text === targetText) {
                        item.click();
                        return 'exact: ' + text;
                    }
                }
                
                // 策略2: 精确匹配整个 item 文字
                for (var i = 0; i < items.length; i++) {
                    var item = items[i];
                    var text = item.textContent.trim();
                    if (text === targetText) {
                        item.click();
                        return 'exact-full: ' + text;
                    }
                }
                
                // 策略3: 包含匹配
                for (var i = 0; i < items.length; i++) {
                    var item = items[i];
                    var text = item.textContent.trim();
                    if (text.indexOf(targetText) !== -1 && text.length < 30) {
                        item.click();
                        return 'contains: ' + text;
                    }
                }
            }
            
            // 策略4: 在整个文档中查找可见的匹配选项
            var allItems = document.querySelectorAll(
                "div[class*='dropItem'], div[class*='dropMultiItem']"
            );
            for (var j = 0; j < allItems.length; j++) {
                var el = allItems[j];
                var rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0 && rect.y > 200) {
                    var innerSpan = el.querySelector('span');
                    var text = innerSpan ? innerSpan.textContent.trim() : el.textContent.trim();
                    if (text === targetText || (text.indexOf(targetText) !== -1 && text.length < 30)) {
                        el.click();
                        return 'global: ' + text;
                    }
                }
            }
            
            return null;
        """, option_text)

        if option_clicked:
            print(f'[INFO] 已选择 {trigger_text}：{option_clicked}')
            time.sleep(0.5)  # 等待下拉面板关闭
        else:
            print(f'[WARN] 未找到选项：{option_text}（在 {trigger_text} 下拉中）')
            # 调试：输出面板中的所有选项文字
            debug_info = self.driver.execute_script("""
                var dropdowns = document.querySelectorAll("div[class*='auxo-dropdown']");
                var result = {panels: []};
                for (var i = 0; i < dropdowns.length; i++) {
                    var d = dropdowns[i];
                    var rect = d.getBoundingClientRect();
                    if (rect.width > 50 && rect.height > 50 && rect.y > 200) {
                        result.panels.push({
                            class: d.className.substring(0, 100),
                            y: Math.round(rect.y),
                            h: Math.round(rect.height),
                            fullHTML: d.innerHTML
                        });
                    }
                }
                return JSON.stringify(result);
            """)
            if debug_info:
                import json as _json
                try:
                    dbg = _json.loads(debug_info)
                    for panel in dbg.get('panels', []):
                        html = panel['fullHTML']
                        # 保存到桌面
                        import os
                        path = os.path.join(os.path.expanduser('~'), 'Desktop', 'debug_panel_html.txt')
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(html)
                        print(f'[DEBUG] Panel HTML saved to {path} (len={len(html)})')
                        # 提取文字节点
                        texts = []
                        divs = _json.loads('[]')  # placeholder
                except:
                    pass
            # 关闭下拉面板（点击空白处）
            self.driver.find_element(By.TAG_NAME, 'body').click()
            self._save_debug_screenshot(f'option_not_found_{option_text}')

    def _range_to_option_text(self, trigger_text, min_val, max_val):
        """将数值范围转换为下拉面板中的预设选项文字
        
        直播观看人数预设: 全部、100以下、100-1000、1000-1w、1w以上
        粉丝量预设: 全部、10w以下、10w-100w、100w-300w、300w-500w、500w-1000w、1000w以上
        直播GPM预设: 全部、10以下、10-50、50-100、100-500、500-1000、1000以上
        直播商品均价预设: 全部、10以下、10-50、50-100、100-500、500-1000、1000以上
        场均销售额预设: 全部、1w以下、1w-10w、10w-100w、100w-500w、500w-1000w、1000w以上
        """
        if trigger_text == '场均销售额':
            ranges = [
                ((0, 10000), '1w以下'),
                ((10000, 100000), '1w-10w'),
                ((100000, 1000000), '10w-100w'),
                ((1000000, 5000000), '100w-500w'),
                ((5000000, 10000000), '500w-1000w'),
                ((10000000, float('inf')), '1000w以上'),
            ]
        elif trigger_text == '直播观看人数':
            ranges = [
                ((0, 100), '100以下'),
                ((100, 1000), '100-1000'),
                ((1000, 10000), '1000-1w'),
                ((10000, float('inf')), '1w以上'),
            ]
        elif trigger_text == '直播GPM':
            ranges = [
                ((0, 10), '10以下'),
                ((10, 50), '10-50'),
                ((50, 100), '50-100'),
                ((100, 500), '100-500'),
                ((500, 1000), '500-1000'),
                ((1000, float('inf')), '1000以上'),
            ]
        elif trigger_text == '直播商品均价':
            ranges = [
                ((0, 10), '10以下'),
                ((10, 50), '10-50'),
                ((50, 100), '50-100'),
                ((100, 500), '100-500'),
                ((500, 1000), '500-1000'),
                ((1000, float('inf')), '1000以上'),
            ]
        elif trigger_text == '粉丝量' or trigger_text == '粉丝数':
            ranges = [
                ((0, 100000), '10w以下'),
                ((100000, 1000000), '10w-100w'),
                ((1000000, 3000000), '100w-300w'),
                ((3000000, 5000000), '300w-500w'),
                ((5000000, 10000000), '500w-1000w'),
                ((10000000, float('inf')), '1000w以上'),
            ]
        else:
            # 通用：直接拼接
            return f'{min_val}-{max_val}'

        for (r_min, r_max), text in ranges:
            if min_val >= r_min and max_val <= r_max and min_val < max_val:
                return text

        # 如果没有精确匹配，找最接近的范围
        print(f'[WARN] 范围 {min_val}-{max_val} 没有精确匹配的预设，尝试最接近的...')
        # 如果 min_val 正好等于某个范围的下界
        for (r_min, r_max), text in ranges:
            if min_val == r_min:
                return text

        return f'{min_val}-{max_val}'

    def _click_confirm_button(self):
        """尝试点击确认/确定按钮（保留兼容性）"""
        confirm_selectors = [
            "//button[contains(text(), '确定')]",
            "//span[contains(text(), '确定')]/ancestor::button",
            "//button[contains(text(), '确认')]",
        ]

        for sel in confirm_selectors:
            try:
                if sel.startswith('//'):
                    elements = self.driver.find_elements(By.XPATH, sel)
                else:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                for el in elements:
                    if el.is_displayed():
                        el.click()
                        print('[INFO] 已点击确认按钮')
                        time.sleep(1)
                        return True
            except Exception:
                continue
        return False

    def _parse_authors(self, data):
        """从接口数据中解析达人列表"""
        authors_list = []

        if isinstance(data, dict):
            if 'data' in data:
                inner = data['data']
                if isinstance(inner, dict):
                    authors_list = (
                        inner.get('authorList', [])
                        or inner.get('list', [])
                        or inner.get('authors', [])
                        or inner.get('author_list', [])
                        or inner.get('records', [])
                        or inner.get('items', [])
                        or inner.get('resultList', [])
                    )
                elif isinstance(inner, list):
                    authors_list = inner
            elif 'authorList' in data:
                authors_list = data['authorList']
            elif 'list' in data:
                authors_list = data['list']
            elif 'records' in data:
                authors_list = data['records']
            elif 'items' in data:
                authors_list = data['items']

        if not authors_list and isinstance(data, dict):
            # 尝试遍历所有值，找第一个是列表且元素是字典的字段
            for key, val in data.items():
                if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                    # 检查是否包含达人特征字段
                    sample = val[0]
                    if any(k in sample for k in ['authorId', 'author_id', 'uid', 'nickname', 'name', 'author_base']):
                        authors_list = val
                        print(f'[DEBUG] 从字段 "{key}" 找到达人列表（{len(val)} 条）')
                        break

        if not authors_list and isinstance(data, dict) and 'data' in data:
            inner = data['data']
            if isinstance(inner, dict):
                # 深层遍历 data 中的所有值
                for key, val in inner.items():
                    if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                        sample = val[0]
                        if any(k in sample for k in ['authorId', 'author_id', 'uid', 'nickname', 'name', 'author_base']):
                            authors_list = val
                            print(f'[DEBUG] 从 data.{key} 找到达人列表（{len(val)} 条）')
                            break

        print(f'[INFO] 解析到 {len(authors_list)} 个达人数据')
        return authors_list

    def export_to_excel(self, authors_data, output_path, recommended_count=None):
        """将达人数据导出为Excel文件"""
        if not authors_data:
            print('[WARN] 没有数据可导出')
            return False

        # 按推荐数量截取
        if recommended_count and len(authors_data) > recommended_count:
            authors_data = authors_data[:recommended_count]
            print(f'[INFO] 按推荐数量截取前 {recommended_count} 个达人')

        flattened_data = []
        for idx, author in enumerate(authors_data, 1):
            flat_record = {'序号': idx}

            # === 基础信息 (author_base) ===
            base = author.get('author_base', {}) or {}
            flat_record['达人昵称'] = base.get('nickname', '')
            flat_record['达人ID'] = base.get('uid', '')
            flat_record['头像URL'] = base.get('avatar', '') or base.get('avatar_big', '')
            flat_record['抖音号'] = base.get('aweme_id', '')
            flat_record['城市'] = base.get('city', '')
            flat_record['粉丝量'] = base.get('fans_num', 0) or 0
            
            # 达人等级 (author_base.author_level)
            level_val = base.get('author_level', '')
            if level_val is not None and level_val != '':
                flat_record['达人等级'] = f'LV{level_val}'
            else:
                flat_record['达人等级'] = 'LV0'
            
            # 性别 (author_base.gender: 1=男, 2=女)
            gender_val = base.get('gender', '')
            if isinstance(gender_val, int):
                gender_map = {0: '未知', 1: '男', 2: '女'}
                flat_record['性别'] = gender_map.get(gender_val, str(gender_val))
            else:
                flat_record['性别'] = str(gender_val) if gender_val else ''

            # === 类目标签 (author_tag) ===
            tag = author.get('author_tag', {}) or {}
            main_cate = tag.get('main_cate', [])
            work_cate = tag.get('work_cate', [])
            flat_record['主推类目'] = ', '.join(main_cate) if isinstance(main_cate, list) else str(main_cate)
            flat_record['内容'] = ', '.join(work_cate) if isinstance(work_cate, list) else str(work_cate)

            # === 直播数据 (author_live) ===
            live = author.get('author_live', {}) or {}
            flat_record['直播观看人数'] = live.get('watching_number', 0) or 0
            flat_record['直播带货区间(低)'] = live.get('sale_low', 0) or 0
            flat_record['直播带货区间(高)'] = live.get('sale_high', 0) or 0
            flat_record['直播GPM(低)'] = live.get('GPM_low', 0) or 0
            flat_record['直播GPM(高)'] = live.get('GPM_high', 0) or 0

            # === 视频数据 (author_video) ===
            video = author.get('author_video', {}) or {}
            flat_record['视频播放中位数'] = video.get('play_median', 0) or 0
            flat_record['视频带货区间(低)'] = video.get('video_sale_low', 0) or 0
            flat_record['视频带货区间(高)'] = video.get('video_sale_high', 0) or 0

            # === 带货销售数据 (author_sale) ===
            sale = author.get('author_sale', {}) or {}
            flat_record['30天销售额(低)'] = sale.get('sale_d30_low', 0) or 0
            flat_record['30天销售额(高)'] = sale.get('sale_d30_high', 0) or 0
            flat_record['主营带货方式'] = sale.get('main_sale_type', '')

            # === 分数 (author_score) ===
            # 评分数据已移除（表达评分、商品评分、物流评分、服务评分）

            flattened_data.append(flat_record)

        df = pd.DataFrame(flattened_data)
        df.to_excel(output_path, index=False, sheet_name='达人列表')

        print(f'[INFO] 数据已成功导出到：{output_path}')
        print(f'[INFO] 共导出 {len(flattened_data)} 个达人')
        return True

    def capture_data(self, recommended_count=None):
        """捕获达人数据（通过滚动分页 + XHR 拦截器收集）
        
        方案：
        1. 从 XHR 拦截器获取筛选操作触发的第一页数据
        2. 如果数量不足，通过滚动 #portal 容器触发无限滚动加载后续页
        3. 每次滚动后等待并从拦截器收集新数据
        4. 全程不刷新页面，不影响已应用的筛选条件
        """
        self.all_authors = []
        self._author_id_set = set()
        
        # 调试：检查拦截器状态
        ready = self.driver.execute_script('return window.__darenInterceptorReady;')
        reqs = self.driver.execute_script('return (window.__seekAuthorReqs || []).length;')
        resps = self.driver.execute_script('return (window.__seekAuthorResps || []).length;')
        print(f'[DEBUG] 拦截器状态: ready={ready}, reqs={reqs}, resps={resps}')
        
        print(f'[INFO] 开始获取达人数据...' + (f'（目标: {recommended_count} 个）' if recommended_count else ''))
        
        # ====== 第一页：从拦截器获取筛选触发的数据 ======
        print('[INFO] 等待第一页数据...')
        first_page_data = None
        for wait_i in range(10):
            time.sleep(1)
            # 每次都重新获取所有响应
            all_resps = self._get_intercepted_responses()
            if all_resps:
                # 取最后一个响应
                try:
                    first_page_data = json.loads(all_resps[-1]['body'])
                    break
                except:
                    continue
        
        if first_page_data:
            authors = self._parse_authors(first_page_data)
            new_count = self._add_authors(authors)
            total_count = self._get_total_count(first_page_data)
            print(f'[INFO] 第一页: 新增 {new_count} 个达人, 总数: {total_count}')
        else:
            print('[WARN] 拦截器未捕获到第一页数据，尝试从页面 DOM 中获取...')
            total_count = 0
        
        # ====== 后续页：通过滚动触发分页 ======
        if recommended_count and len(self.all_authors) < recommended_count:
            remaining = recommended_count - len(self.all_authors)
            max_scroll_attempts = 40
            no_new_data_count = 0  # 连续无新数据计数
            max_no_new_data = 3    # 连续无新数据达到此次数才停止
            
            print(f'[INFO] 已获取 {len(self.all_authors)} 个，还需要 {remaining} 个，开始滚动分页...')
            
            # 调试：检查 portal 状态
            portal_info = self.driver.execute_script("""
                var portal = document.getElementById('portal');
                if (!portal) return {error: 'no portal'};
                return {
                    scrollH: portal.scrollHeight,
                    clientH: portal.clientHeight,
                    scrollTop: portal.scrollTop
                };
            """)
            print(f'[DEBUG] Portal: {portal_info}')
            
            resps_before = len(self._get_intercepted_responses())
            
            for attempt in range(max_scroll_attempts):
                if len(self.all_authors) >= recommended_count:
                    break
                
                # 滚动
                scrolled = self._scroll_portal_to_load_more()
                
                if not scrolled:
                    # 已经滚到底了，等待一会儿看看是否有新内容加载
                    print('[INFO] 已滚到底部，等待新内容加载...')
                    time.sleep(5)
                    # 检查 scrollHeight 是否变化（新内容加载会导致 scrollHeight 增大）
                    still_at_bottom = self.driver.execute_script("""
                        var portal = document.getElementById('portal');
                        if (!portal) return true;
                        var maxScroll = portal.scrollHeight - portal.clientHeight;
                        return portal.scrollTop >= maxScroll - 10;
                    """)
                    if still_at_bottom:
                        print('[INFO] 确认已到底部且无更多数据，停止分页')
                        break
                    # scrollHeight 变了，说明有新内容，继续滚动
                    print('[INFO] 检测到新内容，继续滚动...')
                    continue
                
                # 等待数据加载
                time.sleep(2)
                
                # 检查新响应
                all_resps = self._get_intercepted_responses()
                new_resps = all_resps[resps_before:]
                
                if new_resps:
                    no_new_data_count = 0  # 重置计数
                    for resp in new_resps:
                        try:
                            data = json.loads(resp['body'])
                            authors = self._parse_authors(data)
                            new_count = self._add_authors(authors)
                            total_count = self._get_total_count(data) or total_count
                            if new_count > 0:
                                print(f'[INFO] 滚动加载: 新增 {new_count} 个达人，'
                                      f'累计 {len(self.all_authors)} 个（总数: {total_count}）')
                            else:
                                # 调试：打印响应结构
                                try:
                                    top_keys = list(data.keys()) if isinstance(data, dict) else 'not dict'
                                    inner = data.get('data', {}) if isinstance(data, dict) else {}
                                    inner_keys = list(inner.keys()) if isinstance(inner, dict) else str(type(inner))
                                    print(f'[DEBUG] 响应结构: top={top_keys}, data.keys={inner_keys}')
                                except:
                                    pass
                        except Exception as e:
                            print(f'[WARN] 解析响应失败: {e}')
                    resps_before = len(all_resps)
                else:
                    no_new_data_count += 1
                    if no_new_data_count >= max_no_new_data:
                        print(f'[INFO] 连续 {max_no_new_data} 次滚动无新数据，停止分页')
                        break
                    print(f'[INFO] 滚动后暂无新数据（{no_new_data_count}/{max_no_new_data}），'
                          f'继续尝试...')
                    # 等待更长时间让页面加载
                    time.sleep(2)
        
        print(f'[INFO] 数据获取完成，共收集 {len(self.all_authors)} 个达人')
        return self.all_authors

    def _scroll_portal_to_load_more(self, step=None):
        """滚动 #portal 容器触发无限滚动加载下一页
        
        参数:
            step: 每次滚动的像素数。如果为 None，则自动计算为 clientHeight 的 80%，
                  确保触发懒加载但不会一次性跳过中间内容。
        
        返回: bool - 是否成功滚动（如果已经到底返回 False）
        """
        try:
            result = self.driver.execute_script("""
                var portal = document.getElementById('portal');
                if (!portal) {
                    console.log('[SCROLL] No #portal found');
                    return false;
                }
                
                var beforeScroll = portal.scrollTop;
                var maxScroll = portal.scrollHeight - portal.clientHeight;
                
                console.log('[SCROLL] before=' + beforeScroll + ' max=' + maxScroll + ' clientH=' + portal.clientHeight + ' scrollH=' + portal.scrollHeight);
                
                if (beforeScroll >= maxScroll - 10) {
                    console.log('[SCROLL] Already at bottom');
                    return false;
                }
                
                // 计算滚动步长：clientHeight 的 80%，确保不会跳过懒加载区域
                var scrollStep = arguments[0] || Math.floor(portal.clientHeight * 0.8);
                var targetScroll = Math.min(beforeScroll + scrollStep, maxScroll);
                
                portal.scrollTop = targetScroll;
                
                console.log('[SCROLL] Scrolled to ' + portal.scrollTop + ' (step=' + scrollStep + ')');
                return true;
            """, step)
            return bool(result)
        except Exception as e:
            print(f'[WARN] 滚动 portal 失败: {e}')
            return False

    def _add_authors(self, authors_list):
        """将达人添加到汇总列表中（自动去重）
        
        返回: 本次新增的数量
        """
        new_count = 0
        for author in authors_list:
            # 支持两种数据结构：
            # 1. 嵌套结构: author.author_base.uid
            # 2. 扁平结构: author.authorId
            base = author.get('author_base', {}) or {}
            author_id = str(base.get('uid', '')) or str(author.get('authorId', '')) or str(author.get('id', ''))
            if author_id and author_id not in self._author_id_set:
                self._author_id_set.add(author_id)
                self.all_authors.append(author)
                new_count += 1
            elif not author_id:
                self.all_authors.append(author)
                new_count += 1
        return new_count

    def _get_total_count(self, data):
        """从 API 响应中提取达人总数"""
        try:
            if isinstance(data, dict):
                inner = data.get('data', data)
                if isinstance(inner, dict):
                    return inner.get('totalCount', 0) or inner.get('total', 0) or 0
        except Exception:
            pass
        return 0

    def _get_page_num(self, data):
        """从 API 响应中提取当前页码"""
        try:
            if isinstance(data, dict):
                inner = data.get('data', data)
                if isinstance(inner, dict):
                    return inner.get('pageNum', 0) or inner.get('page', 0) or 0
        except Exception:
            pass
        return 0

    def close(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            print('[INFO] 浏览器已关闭')
            # 清理 Chrome 留下的 SingletonLock 等文件，避免下次启动冲突
            self._cleanup_chrome_locks()

    def _cleanup_chrome_locks(self):
        """清理 Chrome 用户数据目录中的锁文件，防止下次启动报端口/锁冲突"""
        lock_files = ['SingletonLock', 'SingletonSocket', 'SingletonCookie']
        for lock_file in lock_files:
            lock_path = os.path.join(self.USER_DATA_DIR, lock_file)
            try:
                if os.path.exists(lock_path):
                    os.remove(lock_path)
                    print(f'[INFO] 已清理锁文件: {lock_file}')
            except Exception:
                pass


def get_desktop_path():
    """获取桌面路径，若没有权限则使用临时目录"""
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    # 检查是否有写入权限
    try:
        test_file = os.path.join(desktop, 'test_write_permission.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return desktop
    except Exception:
        # 没有权限，返回临时目录
        import tempfile
        return tempfile.gettempdir()


class TagCheckboxSelector:
    """标签类复选框选择器
    
    用于处理页面上的标签类筛选条件，如：
    - 结算率高
    - 回复率高
    - 有联系方式
    - 纯佣达人
    - 明星
    - 黑马达人
    """
    
    TAG_MAP = {
        'high_settlement_rate': {
            'label': '结算率高',
            'options': {'true': '结算率高'}
        },
        'high_reply_rate': {
            'label': '回复率高',
            'options': {'true': '回复率高'}
        },
        'has_contact': {
            'label': '有联系方式',
            'options': {'true': '有联系方式'}
        },
        'pure_commission': {
            'label': '纯佣达人',
            'options': {'true': '纯佣达人'}
        },
        'star': {
            'label': '明星',
            'options': {'true': '明星'}
        },
        'dark_horse': {
            'label': '黑马达人',
            'options': {'true': '黑马达人'}
        }
    }
    
    @classmethod
    def select_tag_checkbox(cls, driver, tag_key, value):
        """选择标签类复选框
        
        参数:
            driver: WebDriver 实例
            tag_key: 标签键名（如 'signed_agency', 'high_settlement_rate'）
            value: 要选择的值（如 True, False, '是', '否'）
        
        返回:
            bool: 是否成功选择
        """
        if tag_key not in cls.TAG_MAP:
            print(f'[WARN] 未知的标签键: {tag_key}')
            return False
        
        tag_info = cls.TAG_MAP[tag_key]
        label = tag_info['label']
        
        # 处理布尔值
        if isinstance(value, bool):
            value_str = 'true' if value else 'false'
        else:
            value_str = str(value)
        
        if value_str not in tag_info['options']:
            print(f'[WARN] {label} 不支持的值: {value}')
            return False
        
        target_text = tag_info['options'][value_str]
        print(f'[INFO] 正在选择标签: {label} -> {target_text}')
        
        try:
            success = driver.execute_script("""
                var targetText = arguments[0];
                var checkboxes = document.querySelectorAll('input[type="checkbox"]');
                
                for (var i = 0; i < checkboxes.length; i++) {
                    var cb = checkboxes[i];
                    var parent = cb.parentElement;
                    var grandParent = parent.parentElement;
                    
                    // 查找相邻的文字元素
                    var siblingText = '';
                    var siblings = parent.children;
                    for (var j = 0; j < siblings.length; j++) {
                        if (siblings[j].tagName !== 'INPUT') {
                            siblingText += siblings[j].textContent || '';
                        }
                    }
                    
                    // 如果父级没有，检查祖父级
                    if (!siblingText) {
                        siblings = grandParent.children;
                        for (var k = 0; k < siblings.length; k++) {
                            if (siblings[k] !== parent) {
                                siblingText += siblings[k].textContent || '';
                            }
                        }
                    }
                    
                    // 检查是否匹配目标文字
                    if (siblingText.includes(targetText)) {
                        // 如果未勾选则点击
                        if (!cb.checked) {
                            cb.click();
                            return true;
                        } else {
                            return true; // 已勾选
                        }
                    }
                }
                
                // 第二种策略：查找包含文字的标签元素
                var labels = document.querySelectorAll('label, span, div');
                for (var m = 0; m < labels.length; m++) {
                    var labelEl = labels[m];
                    if (labelEl.textContent && labelEl.textContent.trim() === targetText) {
                        // 查找关联的 checkbox
                        var associatedCb = labelEl.querySelector('input[type="checkbox"]');
                        if (!associatedCb) {
                            // 查找兄弟 checkbox
                            var prev = labelEl.previousElementSibling;
                            while (prev) {
                                if (prev.tagName === 'INPUT' && prev.type === 'checkbox') {
                                    associatedCb = prev;
                                    break;
                                }
                                prev = prev.previousElementSibling;
                            }
                        }
                        if (associatedCb && !associatedCb.checked) {
                            associatedCb.click();
                            return true;
                        } else if (associatedCb && associatedCb.checked) {
                            return true;
                        }
                    }
                }
                
                return false;
            """, target_text)
            
            if success:
                print(f'[INFO] 已选择标签: {label} -> {target_text}')
                return True
            else:
                print(f'[WARN] 未找到标签复选框: {label}')
                return False
                
        except Exception as e:
            print(f'[WARN] 选择标签失败 {label}: {e}')
            return False


def search_daren(filters, recommended_count=None):
    """
    主函数：根据筛选条件搜索达人并导出

    参数:
        filters: 筛选条件字典
            - category: 主推类目
            - live_viewers: 直播观看人数范围 [min, max]
            - followers: 粉丝量范围 [min, max]
            - level: 达人等级
            - gender: 达人性别
            - email: 登录邮箱（可选）
            - password: 登录密码（可选）
        recommended_count: 推荐达人数量（可选）
    """
    # 验证必要参数
    email = filters.get('email')
    password = filters.get('password')
    
    # 检查推荐达人数量，确保是有效数值
    recommended_count_valid = recommended_count and isinstance(recommended_count, int) and recommended_count > 0
    
    if not email or not password or not recommended_count_valid:
        if not email and not password and not recommended_count_valid:
            print('[ERROR] 缺少必要参数: 邮箱、密码和推荐达人数量')
            print('请提供邮箱、密码和推荐达人数量')
        elif not email or not password:
            print('[ERROR] 缺少必要参数: 邮箱或密码')
            print('请提供邮箱和密码')
        else:
            print('[ERROR] 缺少推荐达人数量或数量无效')
            print('请提供有效的推荐达人数量（正整数）')
        return
    
    print('=' * 60)
    print('精选联盟达人筛选工具 v2.0')
    print('=' * 60)
    print('筛选条件：')
    display_filters = {k: v for k, v in filters.items() if k not in ['email', 'password']}
    for key, value in display_filters.items():
        print(f'  {key}: {value}')
    if recommended_count:
        print(f'  推荐数量: {recommended_count} 个')
    print('=' * 60)

    # 提前提取登录凭据
    email = filters.pop('email', None)
    password = filters.pop('password', None)

    if email and password:
        print(f'[INFO] 已获取登录凭据: {email[:3]}***')

    searcher = DarenSearcher()

    try:
        # 1. 启动浏览器
        searcher.setup_driver()
        
        # 1.5 导航到空白页再注册拦截器，确保后续导航会触发新文档创建
        searcher.driver.get('about:blank')
        time.sleep(1)
        searcher._inject_early_interceptor()

        # 2. 导航到页面，检测是否需要登录
        logged_in = searcher.navigate_to_page()

        # 3. 如果未登录，执行登录流程
        if not logged_in:
            print('[INFO] 需要登录才能继续...')
            if email and password:
                print('[INFO] 使用提供的邮箱密码进行自动登录...')
                login_ok = searcher.auto_login(email, password)
                if not login_ok:
                    print('[ERROR] 自动登录失败，任务终止')
                    return
                # 登录成功后重新导航到达人广场
                print('[INFO] 登录成功，正在重新导航到达人广场...')
                time.sleep(2)
                logged_in = searcher.navigate_to_page()
                if not logged_in:
                    print('[ERROR] 登录后仍无法访问达人广场')
                    return
            else:
                print('[WARN] 未提供登录凭据，请手动登录...')
                print('[INFO] 请在弹出的浏览器中完成登录操作')
                if not searcher._wait_for_manual_action(180):
                    print('[ERROR] 等待手动登录超时')
                    return
                logged_in = searcher.navigate_to_page()
                if not logged_in:
                    print('[ERROR] 手动登录后仍无法访问达人广场')
                    return

        # 3.5. Session 有效性二次校验（cookie 存在但 session 过期的情况）
        print('[INFO] 正在校验 session 有效性...')
        session_ok = searcher._ensure_logged_in(email, password)
        if not session_ok:
            print('[ERROR] Session 校验失败，无法继续执行筛选任务')
            return

        # 4. 应用筛选条件
        searcher.apply_filters(filters)

        # 5. 捕获数据（支持分页获取，传入推荐数量）
        authors_data = searcher.capture_data(recommended_count=recommended_count)

        # 6. 导出到Excel
        if authors_data:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'达人推荐_{timestamp}.xlsx'
            output_path = os.path.join(get_desktop_path(), filename)

            searcher.export_to_excel(authors_data, output_path, recommended_count)
            print('\n' + '=' * 60)
            print(f'任务完成！文件已保存到桌面：{filename}')
            print(f'共推荐 {min(len(authors_data), recommended_count or len(authors_data))} 个达人')
            print('=' * 60)
        else:
            print('\n未找到符合条件的达人')

    except Exception as e:
        print(f'[ERROR] 执行过程中出错: {e}')
        import traceback
        traceback.print_exc()
        searcher._save_debug_screenshot('error')

    finally:
        searcher.close()

