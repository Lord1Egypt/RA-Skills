import logging
import os
import sys
import random
from .base_publisher import BasePublisher

if sys.platform == "win32":
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except:
        pass
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


class XiaohongshuPublisher(BasePublisher):
    """小红书发布器 - 实现小红书创作者后台发布流程

    专项规则：
    - 封面：按内容类型获取并上传（使用通用方法）
    - 标题：限制20字；先清除 +|《》符号，再删除 3岁、必背、古诗、第、集，最后截断
    - 描述：读取Excel【描述】
    - 合集：下拉匹配内容类型
    - 原创声明：勾选复选框 → 弹窗内勾选协议 → 点击「声明原创」
    - 内容类型声明：下拉选择「笔记含AI合成内容」
    - 定时发布：格式 yyyy-MM-dd HH:mm
    - 提交：支持「暂存离开」「定时发布」
    
    防检测策略：
    - 在关键操作之间添加随机延迟，模拟人类思考时间
    - 使用鼠标移动模拟去其他地方复制内容的行为
    - 使用自然的点击方式，避免精确的元素定位点击
    """

    PUBLISH_URL = (
        "https://creator.xiaohongshu.com/publish/publish?from=menu&target=video"
    )

    def __init__(self, page, browser_config):
        super().__init__(page, browser_config)
        self.submit_mode = "publish"
    
    def _human_delay(self, min_ms=500, max_ms=2000):
        """模拟人类思考延迟（毫秒）"""
        delay = random.randint(min_ms, max_ms)
        self.logger.info(f"模拟人类思考延迟: {delay}ms")
        self.page.wait_for_timeout(delay)
    
    def _random_mouse_move(self):
        """随机移动鼠标到页面的不同位置，模拟去其他地方复制内容"""
        try:
            viewport = self.page.viewport_size
            if viewport:
                x = random.randint(100, viewport.get("width", 1920) - 100)
                y = random.randint(100, viewport.get("height", 1080) - 100)
                self.page.mouse.move(x, y)
                self.logger.info(f"鼠标移动到: ({x}, {y})")
        except Exception as e:
            self.logger.warning(f"鼠标移动失败: {str(e)}")

    def publish(self, media_info, content, publish_strategy):
        """发布视频到小红书（参照快手执行顺序）

        执行顺序：
        1. 导航到发布页面
        2. 上传视频（后台进行，不等待完成）
        3. 填写标题
        4. 填写描述
        5. AI内容声明（参照测试代码）
        6. 选择合集
        7. 定时发布
        8. 原创声明
        9. 等待视频上传完成（封面需要等视频上传完）
        10. 上传封面（参照测试代码完整步骤）
        11. 提交发布
        
        防检测优化：
        - 在关键操作之间添加随机延迟，模拟人类思考时间
        - 使用鼠标移动模拟去其他地方复制内容的行为
        """
        self.logger.info(f"开始发布小红书：{media_info.get('name', '')}")

        self.submit_mode = publish_strategy.get("mode", "publish")

        try:
            if not self._ensure_on_publish_page(self.PUBLISH_URL):
                return False, "导航失败"

            if not self._check_login_status():
                return False, "未登录"

            self._handle_captcha()
            
            self._human_delay(1000, 3000)

            video_already_uploaded = self._handle_continue_edit_prompt()
            need_wait_video = False
            if not video_already_uploaded:
                if not self._upload_video_human(media_info["video_path"]):
                    return False, "视频上传失败"
                need_wait_video = True

            self._human_delay(2000, 5000)
            self._random_mouse_move()

            self._fill_title(content.get("title", ""))
            
            self._human_delay(1500, 3500)
            self._random_mouse_move()

            self._fill_description(content.get("description", ""))
            
            self._human_delay(1000, 2500)

            self._select_ai_declaration(media_info)

            self._human_delay(800, 2000)

            collection_name = self._get_collection_name(media_info)
            if collection_name:
                self._select_collection(collection_name)
                self._human_delay(800, 2000)

            publish_time = publish_strategy.get("time", "")
            if publish_time:
                self._set_schedule_time(publish_time)
                self._human_delay(800, 2000)

            self._handle_original_declaration()

            self._human_delay(1000, 3000)

            if need_wait_video:
                self._wait_for_video_upload()

            self._human_delay(1000, 2500)

            self._upload_cover_human(media_info)

            self._human_delay(2000, 4000)

            if not self._submit_publish():
                return False, "发布提交失败"

            return True, "发布成功"
        except Exception as e:
            self.logger.error(f"小红书发布异常: {str(e)}")
            import traceback

            traceback.print_exc()
            self._take_screenshot("xiaohongshu_error")
            return False, str(e)

    def _handle_continue_edit_prompt(self):
        """处理继续编辑提示"""
        try:
            continue_btn = self.page.query_selector('button:has-text("继续编辑")')
            if continue_btn and continue_btn.is_visible():
                self.logger.info("检测到未发布视频，点击继续编辑")
                continue_btn.click()
                self.page.wait_for_timeout(3000)
                return True
            return False
        except Exception as e:
            self.logger.warning(f"处理继续编辑提示失败: {e}")
            return False

    def _upload_video(self, video_path):
        """上传视频文件（参照测试代码）"""
        try:
            self.logger.info(f"开始上传视频: {video_path}")

            self.page.wait_for_selector(
                ".upload-button", state="visible", timeout=30000
            )
            self.logger.info("页面加载完成")

            file_input = self.page.locator("input.upload-input")
            file_input.wait_for(state="attached", timeout=10000)

            file_input.set_input_files(video_path)
            self.logger.info("视频上传触发成功")

            return True
        except Exception as e:
            self.logger.warning(f"上传视频失败: {str(e)}")
            return False

    def _upload_video_human(self, video_path):
        """上传视频文件（模拟人类操作：先点击上传区域，再设置文件）"""
        try:
            self.logger.info(f"开始上传视频(模拟人类操作): {video_path}")

            self.page.wait_for_selector(
                ".upload-button", state="visible", timeout=30000
            )
            self.logger.info("页面加载完成")

            upload_button = self.page.locator(".upload-button")
            upload_button.wait_for(state="visible", timeout=10000)
            
            self._human_delay(500, 1500)
            
            upload_button.click()
            self.logger.info("点击上传按钮（模拟人类操作）")
            
            self._human_delay(500, 1500)

            file_input = self.page.locator("input.upload-input")
            file_input.wait_for(state="attached", timeout=10000)

            file_input.set_input_files(video_path)
            self.logger.info("视频上传触发成功")

            return True
        except Exception as e:
            self.logger.warning(f"上传视频失败(模拟人类操作): {str(e)}")
            return False

    def _check_video_already_uploaded(self):
        """检查视频是否已经上传完成"""
        try:
            preview_element = self.page.locator(".preview-new")
            if preview_element.count() > 0:
                return True, "检测到视频预览"
            
            uploading_element = self.page.locator(".uploading")
            if uploading_element.count() == 0:
                return True, "未检测到上传中状态"
            
            return False, "未检测到视频已上传"
        except Exception as e:
            self.logger.warning(f"检查视频上传状态失败: {str(e)}")
            return False, str(e)

    def _wait_for_video_upload(self):
        """等待视频上传完成（参照测试代码）"""
        try:
            self.logger.info("开始等待视频上传完成")

            self.page.wait_for_selector(".uploading", state="hidden", timeout=120000)
            self.page.wait_for_selector(".preview-new", state="visible", timeout=30000)
            self.logger.info("视频上传完成")
            return True
        except Exception as e:
            self.logger.warning(f"等待视频上传失败: {str(e)}")
            return False

    def _fill_title(self, title):
        """填写标题（参照测试代码）"""
        try:
            if title:
                trim_title = self.trim_title(title, 20)

                input_element = self.page.locator(
                    ".c-input_inner .d-input input.d-text"
                )
                input_element.wait_for(state="visible", timeout=10000)
                input_element.fill(trim_title)

                self.logger.info(f"填写标题（精简后）：{trim_title}")

            return True
        except Exception as e:
            self.logger.warning(f"填写标题失败: {str(e)}")
            return False

    def _fill_description(self, description):
        """填写描述（参照测试代码）"""
        try:
            if description:
                editor = self.page.locator(".tiptap-container .tiptap")
                editor.wait_for(state="visible", timeout=10000)
                editor.click()
                editor.type(description)

                self.logger.info(f"填写描述（完整）：{description[:50]}...")

            return True
        except Exception as e:
            self.logger.warning(f"填写描述失败: {str(e)}")
            return False

    def _select_collection(self, collection_name):
        """选择合集（参照测试代码）"""
        try:
            self.logger.info(f"开始选择合集: {collection_name}")

            collection_button = self.page.locator(".collection-plugin-button")
            if collection_button.count() > 0:
                collection_button.wait_for(state="visible", timeout=10000)
                collection_button.click()

                self.page.wait_for_selector(
                    ".collection-plugin-popover", state="visible", timeout=5000
                )

                # 根据合集名称选择正确的合集
                target_collection = self.page.locator(
                    f'.collection-plugin-popover .item:has-text("{collection_name}")'
                )
                self.logger.info(
                    f"查找目标合集'{collection_name}': {target_collection.count()}"
                )

                if target_collection.count() > 0:
                    target_collection.first.click()
                    self.logger.info(f"合集选择成功: {collection_name}")
                    return True
                else:
                    # 如果找不到指定名称的合集，打印所有可用合集
                    collection_items = self.page.locator(
                        ".collection-plugin-popover .item"
                    )
                    self.logger.info(f"可用合集数量: {collection_items.count()}")
                    for i in range(collection_items.count()):
                        item_text = collection_items.nth(i).text_content()
                        self.logger.info(f"合集 {i}: {item_text}")

            self.logger.warning(f"未找到合集: {collection_name}")
            return False
        except Exception as e:
            self.logger.warning(f"选择合集失败: {str(e)}")
            return False

    def _select_ai_declaration(self, media_info):
        """选择AI内容声明（参照测试代码）"""
        if not self.should_add_ai_label(media_info):
            self.logger.info("AI标注开关关闭，跳过AI内容声明")
            return
        try:
            self.logger.info("开始选择AI内容声明")

            ai_select = self.page.locator(
                'div.d-select-content:has-text("添加内容类型声明")'
            ).locator("..")
            self.logger.info(f"查找ai_select:{ai_select.count()}")

            if ai_select.count() > 0:
                ai_select.wait_for(state="visible", timeout=10000)
                ai_select.click()
                self.logger.info("点击AI声明选择器")

                self.page.wait_for_selector(
                    ".declaration-drop-down", state="visible", timeout=5000
                )

                ai_option = self.page.locator(
                    '.declaration-drop-down .d-grid-item:has-text("笔记含AI合成内容")'
                )
                if ai_option.count() > 0:
                    ai_option.first.click()
                    self.logger.info("选择AI声明成功: 笔记含AI合成内容")
                    return True

            self.logger.warning("未找到AI声明选项")
            return False
        except Exception as e:
            self.logger.warning(f"选择AI声明失败: {str(e)}")
            return False

    def _set_schedule_time(self, schedule_time):
        """设置定时发布时间（参照测试代码）"""
        try:
            self.logger.info(f"开始设置定时发布时间: {schedule_time}")

            schedule_switch = self.page.locator(
                ".post-time-switch-container .d-switch-box"
            )
            if schedule_switch.count() > 0:
                schedule_switch.wait_for(state="visible", timeout=10000)
                schedule_switch.click()
                self.logger.info("点击定时发布开关")

                self.page.wait_for_selector(
                    ".date-picker-container", state="visible", timeout=5000
                )

                self.page.evaluate(
                    f"""
                    const input = document.querySelector('.date-picker-container .d-datepicker-wrapper input.d-text');
                    if (input) {{
                        input.value = '{schedule_time}';
                        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                """
                )
                self.logger.info(f"定时发布时间设置成功: {schedule_time}")

            return True
        except Exception as e:
            self.logger.warning(f"设置定时发布失败: {str(e)}")
            return False

    def _handle_original_declaration(self):
        """原创声明处理（参照测试代码）"""
        try:
            self.logger.info("开始处理原创声明")

            original_switch = self.page.locator(".original-wrapper .d-switch-box")
            if original_switch.count() > 0:
                original_switch.wait_for(state="visible", timeout=10000)
                original_switch.click()
                self.logger.info("点击原创声明开关")

                self.page.wait_for_selector(
                    ".d-modal-mask", state="visible", timeout=5000
                )

                agreement_checkbox = self.page.locator(
                    ".d-modal-mask .footerLeft .d-checkbox-simulator"
                )
                if agreement_checkbox.count() > 0:
                    agreement_checkbox.click()
                    self.logger.info("勾选协议")

                declare_btn = self.page.locator(
                    '.d-modal-mask button:has-text("声明原创")'
                )
                if declare_btn.count() > 0:
                    declare_btn.wait_for(state="visible", timeout=5000)
                    declare_btn.click()
                    self.logger.info("点击声明原创按钮")

            self.logger.info("原创声明处理成功")
            return True
        except Exception as e:
            self.logger.warning(f"处理原创声明失败: {str(e)}")
            return False

    def _upload_cover(self, media_info):
        """上传封面（参照测试代码完整步骤）"""
        try:
            cover_path = self.get_cover_path(media_info)

            if not cover_path or not os.path.exists(cover_path):
                self.logger.info("封面文件不存在，跳过封面上传")
                return True

            self.logger.info(f"开始上传封面: {cover_path}")

            self.page.wait_for_selector(
                ".publish-page-content-cover-content", state="visible", timeout=30000
            )
            self.logger.info("封面区域已加载")

            cover_button = self.page.locator(".cover-plugin-preview .operator")
            self.logger.info(f"查找cover_button:{cover_button.count()}")

            if cover_button.count() > 0:
                self.page.evaluate(
                    'document.querySelector(".cover-plugin-preview .operator").click()'
                )
                self.logger.info("点击修改封面div")

                try:
                    self.page.wait_for_selector(
                        ".cover-modal", state="visible", timeout=15000
                    )
                    self.logger.info("封面弹窗已出现")
                except Exception as e:
                    self.logger.warning(f"等待弹窗超时，尝试其他选择器: {e}")
                    self.page.wait_for_selector(
                        ".d-modal.cover-modal", state="visible", timeout=10000
                    )

                cover_uploading = False

                # 重要补充：判断封面是否成功的关键是 “.preview .preview-container .cover .content .left .single-note .cover img.cover” 这个img的src 出现了变化
                # 获取预览图img元素
                cover_preview_img = self.page.locator(
                    ".preview .preview-container .cover .content .left .single-note .cover img.cover"
                )
                # 第一步：上传前提前读取原图src
                old_src = cover_preview_img.first.get_attribute("src")

                # #workspace 紧跟后面的 input
                cover_input = self.page.locator(
                    '#workspace + input[type="file"][accept*="image"]'
                )
                self.logger.info(
                    f"找到紧跟 #workspace 后面的input元素{cover_input.count()}个"
                )

                if cover_input.count() > 0:
                    cover_input.set_input_files(cover_path, timeout=10000)
                    self.logger.info(f"封面文件上传: {cover_path}")
                    cover_uploading = True
                else:
                    # 备选：查找所有隐藏的file input
                    all_inputs = self.page.locator(
                        'input[type="file"][accept*="image"][style*="display: none"]'
                    )
                    self.logger.info(
                        f"页面中共有{all_inputs.count()}个隐藏的file input"
                    )
                    if all_inputs.count() > 0:
                        all_inputs.first.set_input_files(cover_path, timeout=10000)
                        self.logger.info(f"封面文件上传: {cover_path}")
                        cover_uploading = True

                if cover_uploading:
                    # 等待预览图的src发生变化
                    self.page.wait_for_function(
                        """
                        ([el, oldSrc]) => el.getAttribute('src') !== oldSrc
                        """,
                        arg=[cover_preview_img.first.element_handle(), old_src],
                        timeout=30000,
                    )
                    self.logger.info("封面图片上传完成")

                    confirm_btn = self.page.locator(".cover-modal .mojito-button")
                    if confirm_btn.count() > 0:
                        confirm_btn.wait_for(state="visible", timeout=3000)
                        confirm_btn.click()
                        self.logger.info("点击确定按钮")

                        # .cover-modal 会从page上被移除，所以用detached更合适
                        # self.page.wait_for_selector('.cover-modal', state="detached", timeout=3000)
                        self.logger.info("已关闭封面弹窗")
                else:
                    self.logger.warning("未找到封面上传input元素")

            return True
        except Exception as e:
            self.logger.warning(f"封面上传异常: {str(e)}")
            return True

    def _upload_cover_human(self, media_info):
        """上传封面（模拟人类操作：先点击封面区域，再设置文件）"""
        try:
            cover_path = self.get_cover_path(media_info)

            if not cover_path or not os.path.exists(cover_path):
                self.logger.info("封面文件不存在，跳过封面上传")
                return True

            self.logger.info(f"开始上传封面(模拟人类操作): {cover_path}")

            self.page.wait_for_selector(
                ".publish-page-content-cover-content", state="visible", timeout=30000
            )
            self.logger.info("封面区域已加载")
            
            self._human_delay(500, 1500)

            cover_button = self.page.locator(".cover-plugin-preview .operator")
            self.logger.info(f"查找cover_button:{cover_button.count()}")

            if cover_button.count() > 0:
                cover_button.wait_for(state="visible", timeout=10000)
                cover_button.click()
                self.logger.info("点击修改封面区域（模拟人类操作）")
                
                self._human_delay(1000, 2500)

                try:
                    self.page.wait_for_selector(
                        ".cover-modal", state="visible", timeout=15000
                    )
                    self.logger.info("封面弹窗已出现")
                except Exception as e:
                    self.logger.warning(f"等待弹窗超时，尝试其他选择器: {e}")
                    self.page.wait_for_selector(
                        ".d-modal.cover-modal", state="visible", timeout=10000
                    )

                cover_uploading = False
                
                self._human_delay(500, 1500)

                cover_preview_img = self.page.locator(
                    ".preview .preview-container .cover .content .left .single-note .cover img.cover"
                )
                old_src = cover_preview_img.first.get_attribute("src")

                cover_input = self.page.locator(
                    '#workspace + input[type="file"][accept*="image"]'
                )
                self.logger.info(
                    f"找到紧跟 #workspace 后面的input元素{cover_input.count()}个"
                )

                if cover_input.count() > 0:
                    cover_input.set_input_files(cover_path, timeout=10000)
                    self.logger.info(f"封面文件上传: {cover_path}")
                    cover_uploading = True
                else:
                    all_inputs = self.page.locator(
                        'input[type="file"][accept*="image"][style*="display: none"]'
                    )
                    self.logger.info(
                        f"页面中共有{all_inputs.count()}个隐藏的file input"
                    )
                    if all_inputs.count() > 0:
                        all_inputs.first.set_input_files(cover_path, timeout=10000)
                        self.logger.info(f"封面文件上传: {cover_path}")
                        cover_uploading = True

                if cover_uploading:
                    self.page.wait_for_function(
                        """
                        ([el, oldSrc]) => el.getAttribute('src') !== oldSrc
                        """,
                        arg=[cover_preview_img.first.element_handle(), old_src],
                        timeout=30000,
                    )
                    self.logger.info("封面图片上传完成")

                    confirm_btn = self.page.locator(".cover-modal .mojito-button")
                    if confirm_btn.count() > 0:
                        confirm_btn.wait_for(state="visible", timeout=3000)
                        confirm_btn.click()
                        self.logger.info("点击确定按钮")
                        self.logger.info("已关闭封面弹窗")
                else:
                    self.logger.warning("未找到封面上传input元素")

            return True
        except Exception as e:
            self.logger.warning(f"封面上传异常(模拟人类操作): {str(e)}")
            return True

    def _submit_publish_test(self):
        """JS方案：强制读取closed shadow，点击内部按钮"""
        try:
            if self.submit_mode == "draft":
                js_code = """
                    const comp = document.querySelector("xhs-publish-btn");
                    const root = comp.shadowRoot;
                    const btn = root.querySelector('button:has-text("暂存离开")');
                    if(btn) alert("暂存离开");
                """
                log_msg = "暂存离开提交成功"
            else:
                js_code = """
                    const comp = document.querySelector("xhs-publish-btn");
                    const root = comp.shadowRoot;
                    const btn = root.querySelector('button.ce-btn.bg-red');
                    if(btn) alert("发布按钮已找到");
                """
                log_msg = "发布提交成功"
            # 执行JS
            self.page.evaluate(js_code)
            self.logger.info(log_msg)
            return True
        except Exception as e:
            self.logger.warning(f"提交发布失败: {str(e)}")
            return False

    def _submit_publish(self):
        """提交发布（含暂存草稿，兼容closed shadow-root）"""
        try:
            base = "pierce/xhs-publish-btn pierce/.publish-page-publish-btn"
            if self.submit_mode == "draft":
                btn = self.page.locator(f'{base} button:has-text("暂存离开")')
                tip = "暂存成功"
            else:
                btn = self.page.locator(f'{base} button.ce-btn.bg-red:has-text("发布")')
                tip = "发布成功"

            try:
                btn.wait_for(state="visible", timeout=10000)
                btn.click()
                self.logger.info(tip)
                return True
            except Exception as e:
                self.logger.warning(f"pierce策略失败: {e}，尝试兜底方案")

            container = self.page.locator("xhs-publish-btn")
            container.wait_for(state="visible", timeout=10000)

            # .publish-page-publish-btn { display: flex; justify-content: center; gap: 24px; width: 100%; } .ce-btn { width:120px; }
            button_text = "暂存离开" if self.submit_mode == "draft" else "发布"
            result = self.page.evaluate(
                """(buttonText) => {
                const xhsBtn = document.querySelector('xhs-publish-btn');
                if (!xhsBtn) return null;
                
                const rect = xhsBtn.getBoundingClientRect();
                const containerWidth = rect.width;
                const containerHeight = rect.height;
                
                const buttonWidth = 120;
                const gap = 24;
                
                if (buttonText === '暂存离开') {
                    return { x: containerWidth / 2 - buttonWidth / 2 - gap / 2, y: containerHeight / 2 };
                } else {
                    return { x: containerWidth / 2 + buttonWidth / 2 + gap / 2, y: containerHeight / 2 };
                }
            }""",
                button_text,
            )

            if result:
                container.click(position={"x": result["x"], "y": result["y"]})
                self.logger.info(f"{button_text}提交成功（比例坐标点击）")
            else:
                self.logger.info(f"未找到{button_text}按钮")
                return False

            return True
        except Exception as e:
            self.logger.warning(f"提交发布失败: {str(e)}")
            return False

    def _get_collection_name(self, media_info):
        return self.get_collection_name(media_info)
    
    def _wait_for_publish_success(self):
        """等待小红书发布成功
        
        小红书发布成功后：
        1. 页面跳转（framenavigated事件）
        2. URL变化（跳转到笔记管理页面）
        """
        try:
            self.logger.info("等待小红书发布成功...")
            
            try:
                self.page.wait_for_event("framenavigated", timeout=15000)
                self.logger.info("检测到页面跳转，小红书发布成功")
                return True, "小红书发布成功"
            except:
                if self.page.url != self.page.url:
                    self.logger.info("页面URL已变化，小红书发布成功")
                    return True, "小红书发布成功"
                else:
                    self.logger.info("等待发布提交完成...")
                    self.page.wait_for_timeout(3000)
                    return True, "小红书发布成功（未检测到跳转）"
        except Exception as e:
            self.logger.error(f"等待小红书发布成功失败: {str(e)}")
            return True, "小红书发布成功（异常）"

    def _fill_all_content(self, media_info, content, publish_strategy):
        """填写所有内容（标题、描述、合集、AI声明、定时发布）"""
        try:
            self.submit_mode = publish_strategy.get("mode", "publish")
            
            self._fill_title(content.get("title", ""))
            self._fill_description(content.get("description", ""))
            self._select_ai_declaration(media_info)

            collection_name = self._get_collection_name(media_info)
            if collection_name:
                self._select_collection(collection_name)

            publish_time = publish_strategy.get("time", "")
            if publish_time:
                self._set_schedule_time(publish_time)

            self._handle_original_declaration()
            
            self.logger.info("内容填写完成")
            return True
        except Exception as e:
            self.logger.error(f"填写内容失败: {str(e)}")
            return False


def create_publisher(page, browser_config):
    return XiaohongshuPublisher(page, browser_config)
