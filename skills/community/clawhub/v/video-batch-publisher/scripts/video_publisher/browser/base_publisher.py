import os
import logging
import time
import re
from datetime import datetime
from abc import ABC, abstractmethod
from urllib.parse import urlparse
from playwright.sync_api import Page


class BasePublisher(ABC):
    """所有平台发布器的基类，封装通用逻辑"""

    def __init__(self, page: Page, browser_config):
        self.page = page
        self.browser_config = browser_config
        self.timeout = browser_config.get("timeout", 60000)
        self.debug = browser_config.get("debug", False)
        # 调试模式：True=浏览器常驻不关闭，False=正常关闭（默认关闭，与 BrowserSingleton 一致）
        self.debug_keep_browser = False

        # 获取日志记录器（优先使用传入的logger，否则使用默认logger）
        self.logger = browser_config.get("logger", logging.getLogger(__name__))

        # 确保日志输出到终端（添加StreamHandler）
        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            console_handler.setLevel(logging.INFO)
            self.logger.addHandler(console_handler)

        # 确保日志级别至少为INFO
        if self.logger.level > logging.INFO:
            self.logger.setLevel(logging.INFO)

    @abstractmethod
    def publish(self, media_info, content, publish_strategy):
        """发布视频的核心方法，子类必须实现"""
        pass

    def start_video_upload(self, video_path):
        """启动视频上传（只触发上传，不等待完成）
        
        返回：是否成功触发上传
        """
        try:
            if not self._ensure_on_publish_page(self.PUBLISH_URL):
                self.logger.warning("无法导航到发布页面，跳过视频上传")
                return False
            
            self._handle_continue_edit_prompt()
            
            if self._upload_video(video_path):
                self.logger.info(f"视频上传已启动: {video_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"启动视频上传失败: {str(e)}")
            return False

    def fill_content_only(self, media_info, content, publish_strategy):
        """只填写内容（标题、描述、合集、AI声明、定时发布），不上传视频和封面
        
        返回：是否成功填写内容
        """
        try:
            return self._fill_all_content(media_info, content, publish_strategy)
        except Exception as e:
            self.logger.error(f"填写内容失败: {str(e)}")
            return False

    def complete_publish(self, media_info, content, publish_strategy):
        """完成发布（等待视频上传完成、上传封面、提交发布）
        
        注意：调用此方法前，页面应该已经在发布页面且内容已填写完成
        返回：(是否成功, 消息)
        """
        try:
            already_uploaded, msg = self._check_video_already_uploaded()
            if already_uploaded:
                self.logger.info(f"视频已上传完成: {msg}")
            else:
                self._wait_for_video_upload()
            
            self._upload_cover(media_info)
            
            if not self._submit_publish():
                return False, "提交发布失败"
            
            success, msg = self._wait_for_publish_success()
            if not success:
                return False, msg
            
            # 调用 _handle_success_page 确保页面跳转完成（判断发布成功的关键）
            # continue_publish=False 表示不需要返回发布页面（单个视频发布时）
            self._handle_success_page(continue_publish=False)
            
            return True, "发布成功"
        except Exception as e:
            self.logger.error(f"完成发布失败: {str(e)}")
            return False, str(e)
    
    def _wait_for_publish_success(self):
        """等待发布成功（默认实现：等待页面跳转或成功提示）
        
        每个平台应该重写此方法，实现自己的发布成功验证逻辑
        返回：(是否成功, 消息)
        """
        try:
            self.logger.info("等待发布成功...")
            self.page.wait_for_timeout(3000)
            return True, "发布成功（默认等待3秒）"
        except Exception as e:
            self.logger.warning(f"等待发布成功失败: {str(e)}")
            return True, "发布成功（超时）"

    def _fill_all_content(self, media_info, content, publish_strategy):
        """填写所有内容（标题、描述、合集、AI声明、定时发布）- 子类可重写"""
        return True

    def _handle_success_page(self, continue_publish=False):
        """处理发布成功页面（默认不做任何操作，子类可重写）
        
        Args:
            continue_publish: 是否需要继续发布下一个视频
                              True: 需要返回发布页面
                              False: 不需要返回发布页面（单个视频发布时）
        """
        pass

    def _check_video_already_uploaded(self):
        """检查视频是否已经上传完成（用于并行上传模式）
        
        返回：(是否已上传, 消息)
        """
        return False, "未检测到视频已上传"

    def _wait_for_selector(self, selector, state="visible", timeout=None):
        """等待元素，封装超时处理"""
        if timeout is None:
            timeout = self.timeout

        try:
            self.page.wait_for_selector(selector, state=state, timeout=timeout)
            self.logger.debug(f"等待元素成功: {selector}")
            return True
        except Exception as e:
            self.logger.error(f"等待元素超时: {selector}, 错误: {str(e)}")
            return False

    def _wait_for_condition(
        self, condition_func, timeout=30, interval=1, name="condition"
    ):
        """通用等待条件满足方法（替代固定wait_for_timeout）

        Args:
            condition_func: 返回布尔值的函数，用于判断条件是否满足
            timeout: 最大等待时间（秒）
            interval: 检查间隔（秒）
            name: 条件名称（用于日志）

        Returns:
            True: 条件满足
            False: 超时
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                if condition_func():
                    self.logger.debug(f"✓ 条件 [{name}] 满足")
                    return True
            except Exception as e:
                self.logger.debug(f"检查条件 [{name}] 异常: {str(e)}")

            self.page.wait_for_timeout(interval * 1000)

        self.logger.warning(f"✗ 条件 [{name}] 超时 ({timeout}秒)")
        return False

    # ========== 基于 _wait_for_condition 的封装方法 ==========

    def _wait_for_element_present(self, selector, timeout=10, interval=0.5):
        """等待元素出现（存在于DOM中）- 使用Playwright原生方法"""
        try:
            self.page.wait_for_selector(
                selector, state="attached", timeout=timeout * 1000
            )
            self.logger.debug(f"✓ 元素出现: {selector}")
            return True
        except Exception as e:
            self.logger.warning(f"✗ 元素出现超时: {selector} ({timeout}秒)")
            return False

    def _wait_for_element_visible(self, selector, timeout=10, interval=0.5):
        """等待元素可见 - 使用Playwright原生方法"""
        try:
            self.page.wait_for_selector(
                selector, state="visible", timeout=timeout * 1000
            )
            self.logger.debug(f"✓ 元素可见: {selector}")
            return True
        except Exception as e:
            self.logger.warning(f"✗ 元素可见超时: {selector} ({timeout}秒)")
            return False

    def _wait_for_element_hidden(self, selector, timeout=10, interval=0.5):
        """等待元素隐藏/消失 - 使用Playwright原生方法"""
        try:
            self.page.wait_for_selector(
                selector, state="hidden", timeout=timeout * 1000
            )
            self.logger.debug(f"✓ 元素隐藏: {selector}")
            return True
        except Exception as e:
            self.logger.warning(f"✗ 元素隐藏超时: {selector} ({timeout}秒)")
            return False

    def _wait_for_text_present(self, text, timeout=10, interval=0.5):
        """等待页面出现指定文本 - 使用Playwright原生方法"""
        try:
            self.page.locator(f'text="{text}"').wait_for(
                state="visible", timeout=timeout * 1000
            )
            self.logger.debug(f"✓ 文本出现: {text}")
            return True
        except Exception as e:
            self.logger.warning(f"✗ 文本出现超时: {text} ({timeout}秒)")
            return False

    def _wait_for_url_contains(self, substring, timeout=10, interval=0.5):
        """等待URL包含指定字符串 - 使用Playwright原生方法"""
        try:
            self.page.wait_for_url(f"*{substring}*", timeout=timeout * 1000)
            self.logger.debug(f"✓ URL包含: {substring}")
            return True
        except Exception as e:
            self.logger.warning(f"✗ URL包含超时: {substring} ({timeout}秒)")
            return False

    def _wait_for_network_idle(self, timeout=30, interval=1):
        """等待网络空闲 - 使用Playwright原生方法"""
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout * 1000)
            self.logger.debug(f"✓ 网络空闲")
            return True
        except Exception as e:
            self.logger.warning(f"✗ 网络空闲超时 ({timeout}秒)")
            return False

    def _click(self, selector, timeout=None):
        """点击元素，封装异常处理和等待"""
        if timeout is None:
            timeout = self.timeout

        try:
            # 先等待元素可见
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            # 短延时适配弱网环境
            self.page.wait_for_timeout(300)
            self.page.click(selector, timeout=timeout)
            self.logger.debug(f"点击元素成功: {selector}")
            return True
        except Exception as e:
            self.logger.error(f"点击元素失败: {selector}, 错误: {str(e)}")
            return False

    def _fill(self, selector, value, timeout=None):
        """填写输入框，封装异常处理和等待"""
        if timeout is None:
            timeout = self.timeout

        try:
            # 先等待元素可见
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            # 短延时适配弱网环境
            self.page.wait_for_timeout(300)
            self.page.fill(selector, value, timeout=timeout)
            self.logger.debug(f"填写输入框成功: {selector} = {value[:20]}...")
            return True
        except Exception as e:
            self.logger.error(f"填写输入框失败: {selector}, 错误: {str(e)}")
            return False

    def _upload_file(self, selector, file_path, timeout=None):
        """上传文件，封装异常处理"""
        if timeout is None:
            timeout = self.timeout

        try:
            # 确保文件路径是绝对路径
            file_path = os.path.abspath(file_path)

            if not os.path.exists(file_path):
                self.logger.error(f"上传文件不存在: {file_path}")
                return False

            # 选择文件
            self.page.set_input_files(selector, file_path)
            self.logger.debug(f"上传文件成功: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"上传文件失败: {file_path}, 错误: {str(e)}")
            return False

    def _handle_original_declaration(
        self, checkbox_selector, confirm_button_selector=None
    ):
        """处理原创声明弹窗二次确认"""
        try:
            # 勾选原创复选框
            if not self._click(checkbox_selector):
                self.logger.warning("未能勾选原创声明复选框")
                return True  # 可能已经勾选或不存在

            # 等待弹窗出现
            time.sleep(1)

            # 检查是否有弹窗出现
            modal_selectors = [
                ".modal-content",
                ".ant-modal",
                ".el-dialog",
                '//div[@role="dialog"]',
                '//div[contains(@class, "modal")]',
            ]

            modal_found = False
            for modal_selector in modal_selectors:
                try:
                    self.page.wait_for_selector(modal_selector, timeout=5000)
                    modal_found = True
                    break
                except:
                    continue

            if modal_found:
                self.logger.info("检测到原创声明弹窗，进行二次确认")

                # 尝试勾选"已阅读并同意"复选框
                agree_checkbox_selectors = [
                    '//input[@type="checkbox"]',
                    '//label[contains(text(),"已阅读")]/input',
                    '//label[contains(text(),"同意")]/input',
                    ".agree-checkbox",
                    ".checkbox-agree",
                ]

                for checkbox_sel in agree_checkbox_selectors:
                    try:
                        self.page.click(checkbox_sel, timeout=3000)
                        self.logger.debug("勾选已阅读并同意")
                        break
                    except:
                        continue

                # 点击确认按钮
                if confirm_button_selector:
                    self._click(confirm_button_selector)
                else:
                    confirm_button_selectors = [
                        '//button[text()="确认"]',
                        '//button[text()="确定"]',
                        '//button[text()="申明原创"]',
                        ".btn-confirm",
                        ".confirm-btn",
                    ]

                    for btn_sel in confirm_button_selectors:
                        try:
                            self.page.click(btn_sel, timeout=3000)
                            self.logger.debug("点击确认按钮")
                            break
                        except:
                            continue

            self.logger.info("原创声明处理完成")
            return True

        except Exception as e:
            self.logger.error(f"处理原创声明失败: {str(e)}")
            return False

    def _set_schedule_time(self, schedule_time, datetime_selector):
        """设置定时发布时间"""
        try:
            if not schedule_time:
                self.logger.info("无需设置定时发布")
                return True

            # 解析时间
            dt = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M")

            # 填写日期时间
            self._fill(datetime_selector, schedule_time)
            self.logger.debug(f"设置定时发布时间: {schedule_time}")
            return True

        except Exception as e:
            self.logger.error(f"设置定时发布时间失败: {str(e)}")
            return False

    def _wait_for_upload_complete(self, progress_selector, timeout=120000):
        """等待上传完成"""
        try:
            # 等待进度条消失或显示完成
            self.page.wait_for_selector(
                progress_selector, state="hidden", timeout=timeout
            )
            self.logger.debug("上传完成")
            return True
        except Exception as e:
            self.logger.warning(f"等待上传完成超时: {str(e)}")
            return True  # 继续执行，可能上传已完成但进度条检测有问题

    def _take_screenshot(self, name="screenshot"):
        """截取当前页面截图"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"./screenshots/{name}_{timestamp}.png"

            # 确保目录存在
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            self.page.screenshot(path=screenshot_path, full_page=True)
            self.logger.info(f"截图已保存: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"截图失败: {str(e)}")
            return None

    def _is_on_publish_url(self, current_url, publish_url):
        """判断当前 URL 是否指向发布页面（忽略查询参数差异）

        部分平台（如 B站）发布成功后 URL 不变，且通过站内"投稿/再投一个"
        返回发布页时会丢掉 ?page_from=... 等查询参数，导致字符串包含判断失效、
        重复导航、上传区处于过渡态。这里只比较 scheme+netloc+path。
        """
        try:
            a = urlparse(current_url)
            b = urlparse(publish_url)
            return (a.scheme, a.netloc, a.path) == (b.scheme, b.netloc, b.path)
        except Exception:
            return publish_url in (current_url or "")

    def _navigate(self, url):
        """导航到指定URL（优化版）

        使用 domcontentloaded 而非 networkidle，大幅减少等待时间
        """
        try:
            # 使用更短的超时时间，只等待DOM加载完成
            self.page.goto(url, timeout=10000, wait_until="domcontentloaded")
            self.logger.info(f"导航到: {url}")

            # 等待页面基本渲染完成（仅500ms）
            self.page.wait_for_timeout(500)
            self.logger.debug("页面导航完成")
            return True
        except Exception as e:
            self.logger.error(f"导航失败: {url}, 错误: {str(e)}")
            return False

    def _ensure_on_publish_page(self, publish_url):
        """确保当前在发布页面，如果不是则导航过去

        用于批量发布时，每次发布新视频前检测页面状态

        Args:
            publish_url: 发布页面的URL

        Returns:
            bool: 是否成功导航到发布页面
        """
        try:
            # 检查页面是否已关闭
            try:
                current_url = self.page.url
            except Exception as page_e:
                self.logger.warning(f"页面已关闭或不可用: {str(page_e)}，重新获取页面")
                return self._reconnect_page_and_navigate(publish_url)

            # 检查当前页面是否已经是发布页面（模糊匹配）
            if self._is_on_publish_url(current_url, publish_url):
                self.logger.debug(f"检测到URL匹配发布页面: {current_url}")
                
                # 关键：对于某些平台（如B站），发布成功后URL不变但页面内容变了
                # 需要调用_handle_success_page来检测是否是成功页面并处理
                # 使用continue_publish=True，因为如果是成功页面就需要返回发布页面
                try:
                    self._handle_success_page(continue_publish=True)
                except:
                    pass
                
                # 再次检查URL，因为_handle_success_page可能已经处理了成功页面
                try:
                    current_url = self.page.url
                except:
                    pass
                
                if self._is_on_publish_url(current_url, publish_url):
                    self.logger.debug(f"当前已在发布页面: {current_url}")
                    self._wait_for_page_load()
                    self.page.wait_for_timeout(1000)
                    
                    # 验证页面内容是否真正是发布页面（检查是否有标题输入框或上传区域）
                    # 对于B站等平台，URL不变但页面内容可能仍然是成功页面
                    try:
                        title_input = self.page.locator('input.video-title-input')
                        upload_area = self.page.locator('.video-upload-area')
                        if title_input.count() > 0 or upload_area.count() > 0:
                            self.logger.debug("页面内容验证通过，确实是发布页面")
                            return True
                        else:
                            self.logger.warning("URL匹配但页面内容不是发布页面，需要重新导航")
                    except:
                        pass

            self.logger.info(f"当前页面: {current_url}，导航到发布页面: {publish_url}")
            
            # 处理发布成功页面（批量发布时，上一次发布完可能停留在成功页面）
            # continue_publish=True 表示需要返回发布页面继续发布下一个视频
            self._handle_success_page(continue_publish=True)

            # 再次检查是否已在发布页面（处理成功页面后可能自动跳转）
            try:
                current_url = self.page.url
            except Exception as page_e:
                self.logger.warning(f"页面在处理成功页面后关闭: {str(page_e)}，重新获取页面")
                return self._reconnect_page_and_navigate(publish_url)
                
            if self._is_on_publish_url(current_url, publish_url):
                self.logger.debug(f"处理成功页面后已在发布页面: {current_url}")
                # 关键：等待页面完全加载，避免页面刚跳转就开始操作
                self._wait_for_page_load()
                self.page.wait_for_timeout(1000)
                return True

            # 导航到发布页面
            success = self._navigate(publish_url)
            if success:
                self._wait_for_page_load()
                return True
            return False

        except Exception as e:
            self.logger.warning(f"检测页面状态失败: {str(e)}，尝试重新获取页面")
            # 出错时尝试重新获取页面
            return self._reconnect_page_and_navigate(publish_url)
    
    def _reconnect_page_and_navigate(self, publish_url):
        """页面关闭时重新获取页面并导航"""
        try:
            from browser.browser_singleton import get_platform_page
            platform_name = self.__class__.__name__.replace('Publisher', '')
            platform_name_map = {
                'Douyin': '抖音',
                'Bilibili': 'B站',
                'Kuaishou': '快手',
                'Weixin': '视频号',
                'Xiaohongshu': '小红书'
            }
            platform = platform_name_map.get(platform_name, platform_name)
            
            self.page = get_platform_page(platform)
            self.logger.info(f"重新获取页面成功，导航到发布页面: {publish_url}")
            
            success = self._navigate(publish_url)
            if success:
                self._wait_for_page_load()
                return True
            return False
        except Exception as e:
            self.logger.error(f"重新获取页面失败: {str(e)}")
            return False
    
    def close_current_page(self):
        """关闭当前页面（用于批量发布时清理页面状态）"""
        try:
            self.page.close()
            self.logger.info("当前页面已关闭")
        except Exception as e:
            self.logger.warning(f"关闭页面失败: {str(e)}")

    def _wait_for_page_load(self, timeout=None):
        """等待页面加载完成（优化版）

        注意：由于 _navigate 已等待 domcontentloaded，此方法不再重复等待，
        仅做页面就绪状态检查
        """
        if timeout is None:
            timeout = self.timeout

        try:
            # 检查页面是否基本就绪（不再重复等待domcontentloaded）
            # 通过检查document.readyState判断
            ready = self.page.evaluate(
                """() => {
                return document.readyState === 'complete' || document.readyState === 'interactive';
            }"""
            )

            if ready:
                self.logger.debug("页面已就绪")
                return True

            # 如果未就绪，等待一小段时间
            self.page.wait_for_timeout(500)
            self.logger.debug("页面加载完成")
            return True

        except Exception as e:
            self.logger.debug(f"等待页面加载: {str(e)}")
            return True

    def _scroll_to_element(self, selector):
        """滚动到指定元素"""
        try:
            element = self.page.query_selector(selector)
            if element:
                element.scroll_into_view_if_needed()
                self.logger.debug(f"滚动到元素: {selector}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"滚动到元素失败: {selector}, 错误: {str(e)}")
            return False

    def _check_login_status(self):
        """
        检查登录状态（基类默认实现）
        子类可根据平台元素重写
        """
        try:
            return True
        except Exception as e:
            self.logger.warning(f"检查登录状态失败: {str(e)}")
            return True

    def _select_ant_option(self, selector, keywords):
        """通用 ant-select 下拉框选项选择方法

        根据ant-select组件的标准结构：
        - 点击外层容器展开下拉框
        - 下拉选项可能在不同结构中：
          - div[role="listbox"] 内的 div[role="option"]
          - div.ant-select-dropdown-menu 内的选项
          - rc-virtual-list 虚拟滚动列表

        Args:
            selector: 下拉框选择器
            keywords: 用于匹配选项的关键词列表（字符串或列表）

        Returns:
            bool: 是否选择成功
        """
        try:
            if isinstance(keywords, str):
                keywords = [keywords]

            # 获取下拉框元素
            select_el = self.page.query_selector(selector)
            if not select_el:
                self.logger.warning(f"未找到下拉框元素: {selector}")
                return False

            # 点击下拉框展开选项（使用JS点击确保触发正确事件）
            self.page.evaluate("(el) => el.click()", select_el)
            self.logger.debug(f"点击下拉框: {selector}")

            # 使用循环判断等待下拉框展开
            dropdown_found = self._wait_for_condition(
                lambda: self.page.evaluate(
                    """() => {
                    const selectors = [
                        'div.ant-select-dropdown:not([style*="display: none"])',
                        '[role="listbox"]',
                        'div[class*="dropdown"]:not([style*="display: none"])'
                    ];
                    for (const sel of selectors) {
                        if (document.querySelector(sel)) return true;
                    }
                    return false;
                }"""
                ),
                timeout=10,
                interval=0.5,
                name="下拉框展开",
            )

            if not dropdown_found:
                self.logger.warning("下拉框列表未展开")
                return False

            # 查找并点击匹配的选项
            result = self.page.evaluate(
                """(keywords) => {
                const optionSelectors = [
                    'div.ant-select-item.ant-select-item-option',
                    'div.ant-select-dropdown-menu-item',
                    '[role="option"]',
                    'div.rc-virtual-list-item'
                ];
                
                let options = [];
                for (const sel of optionSelectors) {
                    const opts = document.querySelectorAll(sel);
                    const visibleOpts = Array.from(opts).filter(opt => {
                        const rect = opt.getBoundingClientRect();
                        return rect.width > 0 && rect.height > 0;
                    });
                    if (visibleOpts.length > 0) {
                        options = visibleOpts;
                        break;
                    }
                }
                
                if (options.length === 0) {
                    return {success: false, message: '未找到选项'};
                }
                
                for (const option of options) {
                    const contentEl = option.querySelector('.ant-select-item-option-content');
                    let text = contentEl ? contentEl.textContent.trim() : option.textContent.trim();
                    
                    if (!text) {
                        const spanEl = option.querySelector('span');
                        if (spanEl) text = spanEl.textContent.trim();
                    }
                    
                    for (const keyword of keywords) {
                        if (text.includes(keyword)) {
                            option.click();
                            return {success: true, text: text};
                        }
                    }
                }
                
                return {success: false, message: '未找到匹配的选项'};
            }""",
                keywords,
            )

            if result.get("success"):
                self.logger.info(f"选择选项: {result.get('text')}")
                return True
            else:
                self.logger.warning(f"选择下拉框选项失败: {result.get('message')}")
                return False

        except Exception as e:
            self.logger.error(f"选择ant-select选项失败: {str(e)}")
            return False

    def _handle_captcha(self):
        """
        处理验证码（基类默认实现）
        出现验证码时暂停，等待用户手动处理

        优化：使用 JS 一次性检查所有选择器，避免逐个等待超时
        """
        try:
            captcha_selectors = [
                "[class*='captcha']",
                "[class*='verify']",
                "#captcha",
                ".verification-code",
                "[class*='code']",
            ]

            # 使用 JS 一次性检查所有选择器，立即返回结果
            has_captcha = self.page.evaluate(
                """(selectors) => {
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el && el.offsetWidth > 0 && el.offsetHeight > 0) {
                        return true;
                    }
                }
                return false;
            }""",
                captcha_selectors,
            )

            if has_captcha:
                self.logger.warning("检测到验证码，请在浏览器中手动完成验证...")
                # 使用较短的超时检查验证码是否消失
                try:
                    # 先等5秒看看是否自动消失
                    for i in range(10):
                        self.page.wait_for_timeout(500)
                        has_captcha = self.page.evaluate(
                            """(selectors) => {
                            for (const sel of selectors) {
                                const el = document.querySelector(sel);
                                if (el && el.offsetWidth > 0 && el.offsetHeight > 0) {
                                    return true;
                                }
                            }
                            return false;
                        }""",
                            captcha_selectors,
                        )
                        if not has_captcha:
                            self.logger.info("验证码已自动消失")
                            break

                    if has_captcha:
                        # 继续等待用户处理（最多60秒）
                        self.logger.info("等待用户手动处理验证码...")
                        self.page.wait_for_timeout(60000)
                        self.logger.info("验证码处理完成")
                except Exception:
                    pass
            return True
        except Exception as e:
            self.logger.debug(f"处理验证码时出现异常: {str(e)}")
            return True

    # ========== 通用下拉框选择方法（支持包含文本匹配） ==========
    def select_dropdown_option(self, selector, target_text, match_type="contains"):
        """
        通用下拉框选择方法

        :param selector: 下拉框选择器
        :param target_text: 目标文本
        :param match_type: contains=包含匹配 / exact=精确匹配
        """
        try:
            # 等待下拉框可见
            self.page.wait_for_selector(selector, state="visible", timeout=5000)
            # 点击下拉框展开
            self.page.click(selector)
            # 等待选项列表出现（适配弱网环境）
            self.page.wait_for_timeout(500)
            self.page.wait_for_selector(
                f"{selector} option, .dropdown-menu li, .semi-select-option",
                timeout=5000,
            )

            if match_type == "contains":
                self.page.click(
                    f"{selector} option:has-text('{target_text}'), .dropdown-menu li:has-text('{target_text}'), .semi-select-option:has-text('{target_text}')"
                )
            elif match_type == "exact":
                self.page.click(f"{selector} option:text='{target_text}'")

            self.logger.debug(f"下拉框选择成功: {target_text}")
            return True
        except Exception as e:
            self.logger.warning(f"下拉框选择失败: {str(e)}")
            return False

    # ========== 通用标题精简方法（各平台标题截断统一调用） ==========
    def trim_title(
        self, title_text, max_len, 
        remove_fixed_words=None, 
        remove_patterns=None
    ):
        """
        通用标题精简方法（按顺序移除：固定词语 → 成对符号 → 单个符号）

        :param title_text: 原始标题文本
        :param max_len: 最大长度
        :param remove_fixed_words: 要移除的固定词语列表（如"成语故事"、"第XX集"）
        :param remove_patterns: 要移除的正则表达式列表（单个符号，如[r'[，。！？]']）
        :return: 精简后的标题
        """
        if not title_text:
            return ""
        
        # 优先判断长度，长度符合则直接返回
        if len(title_text) <= max_len:
            return title_text
        
        self.logger.info(f"标题长度 {len(title_text)} 超出最大长度 {max_len}，开始精简")
        
        # 默认固定词语
        default_fixed_words = ["岁", "3+", "必背","一听就会！","每天","阅读","一个","成语故事","一首","古诗","第","集", " "]
        
        # 默认成对符号（成对移除）
        default_pair_symbols = [
            ('《', '》'), ('“', '”'), ('"', '"'), ("'", "'"),
            ('（', '）'), ('【', '】'), ('「', '」'), ('『', '』'),
        ]
        
        # 默认单个符号模式
        default_patterns = [r'[，。！？、;:,!?+|]']
        
        # 使用默认值，外部传入的值动态添加到后面
        fixed_words = default_fixed_words.copy()
        if remove_fixed_words:
            fixed_words.extend(list(remove_fixed_words))
        
        pair_symbols = default_pair_symbols.copy()
        
        patterns = default_patterns.copy()
        if remove_patterns:
            patterns.extend(list(remove_patterns))

        # 第一步：逐个移除固定词语，每移除一个就检查长度
        for word in fixed_words:
            if len(title_text) <= max_len:
                break
            original_len = len(title_text)
            title_text = title_text.replace(word, "")
            removed_count = original_len - len(title_text)
            self.logger.info(f"移除固定词语 '{word}'，移除 {removed_count} 个字符，当前长度: {len(title_text)}")
        
        # 第二步：逐个移除成对符号，每移除一对就检查长度
        for start_sym, end_sym in pair_symbols:
            if len(title_text) <= max_len:
                break
            original_len = len(title_text)
            title_text = title_text.replace(start_sym, "").replace(end_sym, "")
            removed_count = original_len - len(title_text)
            self.logger.info(f"移除成对符号 '{start_sym}{end_sym}'，移除 {removed_count} 个字符，当前长度: {len(title_text)}")
        
        # 第三步：逐个移除单个符号，每移除一个就检查长度
        for pat in patterns:
            if len(title_text) <= max_len:
                break
            original_len = len(title_text)
            title_text = re.sub(pat, "", title_text)
            removed_count = original_len - len(title_text)
            self.logger.info(f"移除符号模式 '{pat}'，移除 {removed_count} 个字符，当前长度: {len(title_text)}")
        
        # 再次判断长度，移除后可能已符合要求
        if len(title_text) <= max_len:
            self.logger.info(f"标题精简完成，无需截断: {title_text}")
            return title_text
        
        # 最终截断到最大长度
        trimmed = title_text[:max_len]
        self.logger.info(f"标题精简完成，截断到 {max_len} 字符: {trimmed}")
        return trimmed

    # ========== 通用封面路径获取（按内容类型自动匹配封面文件） ==========
    def get_cover_path(self, media_info):
        """
        通用封面路径获取

        :param media_info: 媒体信息字典，包含 content_type 和 video_path
        :return: 封面文件路径
        """
        content_type = media_info.get("content_type", "")
        video_path = media_info.get("video_path", "")
        if not video_path:
            return ""
        base_path = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        cover_dir = os.path.join(base_path, video_name)

        if content_type == "idiom":
            return os.path.join(cover_dir, "0_cover_350.png")
        elif content_type == "poem":
            return os.path.join(cover_dir, "0_cover.png")
        else:
            # 其他类型默认使用成语封面规则
            return os.path.join(cover_dir, "0_cover_350.png")

    # ========== 通用定时时间解析（统一解析发布日期、补默认时间/补秒） ==========
    def parse_schedule_time(self, publish_date_str, default_time="20:00"):
        """
        通用定时时间解析

        :param publish_date_str: 发布日期字符串
        :param default_time: 默认时间（为空时使用）
        :return: (date_part, hhmm, hhmmss) 元组
        """
        if not publish_date_str:
            date_part = datetime.now().strftime("%Y-%m-%d")
            time_part = default_time
        else:
            parts = publish_date_str.strip().split()
            if len(parts) == 1:
                date_part = parts[0]
                time_part = default_time
            else:
                date_part, time_part = parts[0], parts[1]
                if not time_part:
                    time_part = default_time

        # 解析时分秒
        time_parts = time_part.split(":")
        hhmm = (
            f"{time_parts[0]}:{time_parts[1]}" if len(time_parts) >= 2 else default_time
        )
        hhmmss = (
            f"{time_parts[0]}:{time_parts[1]}:00"
            if len(time_parts) >= 2
            else f"{default_time}:00"
        )

        return date_part, hhmm, hhmmss

    # ========== 通用合集名称获取方法 ==========
    def get_collection_name(self, media_info):
        """
        根据内容类型获取合集名称（通用方法）
        优先级：Excel 行级 collection 列 > 配置类型级 collection > 中性兜底（空=不指定合集）

        :param media_info: 媒体信息字典，包含 content_type
        :return: 合集名称（空字符串表示不指定合集）
        """
        content_type = media_info.get("content_type", "")
        # 1) Excel 行级 collection 列优先（单行可覆盖类型默认合集）
        row_collection = media_info.get("collection")
        if row_collection:
            return row_collection
        # 2) 配置类型级 collection（config.yaml 的 content_types[].collection）
        try:
            from core.config_manager import config_manager
            cfg_collection = config_manager.get_collection_for_type(content_type)
            if cfg_collection:
                return cfg_collection
        except Exception:
            pass
        # 3) 兜底：空字符串（不指定合集），不再写死具体名称
        return ""

    # ========== 通用 AI 标注开关 ==========
    def should_add_ai_label(self, media_info):
        """
        根据配置判断该内容类型发布时是否勾选「AI生成内容」声明。
        读取 content_types[].ai_label（默认 False）。media_info 需携带 content_type。
        """
        content_type = (media_info or {}).get("content_type", "")
        if not content_type:
            return False
        try:
            from core.config_manager import config_manager
            return bool(config_manager.get_ai_label_for_type(content_type))
        except Exception:
            return False

    # ========== 通用提交发布方法 ==========
    def submit_publish(
        self,
        draft_selector='button:has-text("存草稿"), .draft-btn',
        publish_selector='button:has-text("发布"), .submit-btn, .publish-btn',
    ):
        """
        通用提交发布方法

        :param draft_selector: 草稿按钮选择器
        :param publish_selector: 发布按钮选择器
        :return: True 表示成功，False 表示失败
        """
        try:
            if self.submit_mode == "draft":
                self._click(draft_selector)
                self.logger.info("提交方式：存草稿")
            else:
                self._click(publish_selector)
                self.logger.info("提交方式：发布")

            return True
        except Exception as e:
            self.logger.error(f"提交发布失败: {str(e)}")
            return False

    # ========== 通用发布成功验证方法 ==========
    def verify_publish_success(
        self, success_selector='.success-tip, :text("发布成功")'
    ):
        """
        通用发布成功验证方法

        :param success_selector: 成功提示元素选择器
        :return: True 表示成功，False 表示失败
        """
        try:
            self._wait_for_selector(success_selector, timeout=30000)
            return True
        except Exception as e:
            self.logger.error(f"验证发布失败: {str(e)}")
            return False
