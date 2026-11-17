import logging
import os
import sys
from .base_publisher import BasePublisher

if sys.platform == 'win32':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except:
        pass
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class DouyinPublisher(BasePublisher):
    """抖音发布器 - 实现抖音创作者后台发布流程
    
    专项规则：
    - 标题精简至30字，移除标点和书名号，删除「一听就会！」
    - 双封面上传：横屏视频上传两个不同封面，竖屏视频仅竖封面
    - 合集选择：忽略第一个下拉框，仅操作第二个
    - AI声明固定「内容由AI生成」
    """
    
    PUBLISH_URL = "https://creator.douyin.com/creator-micro/content/upload"
    
    def __init__(self, page, browser_config):
        super().__init__(page, browser_config)
        self.submit_mode = "publish"
    
    def _click_cover_button(self, is_horizontal):
        """点击封面选择按钮（根据视频方向选择横封面或竖封面）"""
        cover_label = "横封面4:3" if is_horizontal else "竖封面3:4"
        self.logger.info(f"点击封面选择按钮: {cover_label}")
        
        self.page.evaluate(f"""
            var allDivs = document.querySelectorAll('div');
            var targetDiv = null;
            for (var i = 0; i < allDivs.length; i++) {{
                var div = allDivs[i];
                if (div.className.includes('coverControl-') && div.textContent.includes('{cover_label}')) {{
                    targetDiv = div;
                    break;
                }}
            }}
            if (targetDiv) {{
                var selectCover = targetDiv.querySelector('div');
                while (selectCover) {{
                    if (selectCover.textContent && selectCover.textContent.trim() === '选择封面') {{
                        selectCover.click();
                        break;
                    }}
                    selectCover = selectCover.querySelector('div');
                }}
            }}
        """)
        self.page.wait_for_timeout(1000)
    
    def _upload_cover_image(self, cover_path):
        """上传封面图片（使用上传区域方式，参照测试代码）"""
        if not os.path.exists(cover_path):
            self.logger.warning(f"封面文件不存在: {cover_path}")
            return False
        
        upload_success = False
        
        upload_area = self.page.locator('[class*="semi-upload upload-"]')
        self.logger.info(f"查找上传区域: {upload_area.count()}")
        
        if upload_area.count() > 0:
            try:
                with self.page.expect_file_chooser(timeout=5000) as fc_info:
                    upload_area.first.click()
                file_chooser = fc_info.value
                file_chooser.set_files(cover_path)
                self.logger.info(f"上传封面: {cover_path}")
                self.page.wait_for_timeout(3000)
                upload_success = True
            except Exception as e:
                self.logger.warning(f"上传封面按钮点击方式失败: {e}")
        
        if not upload_success:
            file_inputs = self.page.locator('.dy-creator-content-modal input[type="file"]')
            self.logger.info(f"尝试直接设置file input: {file_inputs.count()}")
            if file_inputs.count() > 0:
                try:
                    file_inputs.first.set_input_files(cover_path)
                    self.logger.info(f"上传封面（直接设置file input）: {cover_path}")
                    self.page.wait_for_timeout(3000)
                    upload_success = True
                except Exception as e:
                    self.logger.warning(f"直接设置file input失败: {e}")
        
        return upload_success
    
    def _click_set_cover_button(self, is_horizontal):
        """点击"设置横封面"或"设置竖封面"按钮"""
        btn_text = "设置竖封面" if is_horizontal else "设置横封面"
        set_btn = self.page.locator(f'button:has-text("{btn_text}")')
        if set_btn.count() > 0:
            set_btn.first.click()
            self.logger.info(f"点击{btn_text}按钮")
            self.page.wait_for_timeout(1000)
            return True
        return False
    
    def _get_video_dimensions(self, video_path):
        """获取视频文件的实际尺寸（使用OpenCV）"""
        video_width = 0
        video_height = 0
        
        try:
            import cv2
            
            abs_video_path = os.path.abspath(video_path)
            cap = cv2.VideoCapture(abs_video_path)
            if cap.isOpened():
                video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                cap.release()
        except Exception as e:
            self.logger.warning(f"使用OpenCV获取视频尺寸失败: {e}")
        
        return video_width, video_height
    
    def publish(self, media_info, content, publish_strategy):
        """发布视频到抖音（参照快手执行顺序）
        
        执行顺序：
        1. 导航到发布页面
        2. 上传视频（后台进行，不等待完成）
        3. 等待标题输入框出现（页面可编辑）
        4. 填写标题
        5. 填写描述
        6. 选择合集
        7. AI内容声明（使用测试验证的选择器）
        8. 定时发布
        9. 等待视频上传完成（封面需要等视频上传完）
        10. 上传封面（使用测试验证的完整步骤）
        11. 提交发布
        """
        self.logger.info(f"开始发布抖音：{media_info.get('name', '')}")
        
        self.submit_mode = publish_strategy.get('mode', 'publish')
        
        try:
            if not self._ensure_on_publish_page(self.PUBLISH_URL):
                return False, "导航失败"
            
            if not self._check_login_status():
                return False, "未登录"
            
            self._handle_captcha()
            
            video_already_uploaded = self._handle_continue_edit_prompt()
            need_wait_video = False
            if not video_already_uploaded:
                if not self._upload_video(media_info["video_path"]):
                    return False, "视频上传失败"
                need_wait_video = True

            self._wait_for_page_editable()
            
            self._fill_content(content.get('title', ''), content.get('description', ''))
            self._select_collection(self._get_collection_name(media_info))
            self._select_ai_declaration(media_info)

            publish_time = publish_strategy.get("time", "")
            if publish_time:
                self._set_schedule_time(publish_time)

            if need_wait_video:
                self._wait_for_video_upload()

            self._upload_cover(media_info)

            if not self._submit_publish():
                return False, "发布提交失败"

            success, msg = self._wait_for_publish_success()
            if not success:
                return False, msg

            return True, "发布成功"
        except Exception as e:
            self.logger.error(f"抖音发布异常: {str(e)}")
            import traceback
            traceback.print_exc()
            self._take_screenshot("douyin_error")
            return False, str(e)
    
    def _wait_for_page_editable(self):
        """等待页面可编辑（标题输入框出现）
        
        抖音特殊：视频上传完成后会自动跳转到发布页面，需要处理两种页面状态：
        1. 当前已经在发布页面（/post/video）
        2. 当前在上传页面（/content/upload），视频上传后会自动跳转
        
        关键：视频上传后页面会自动导航到发布页面，需要等待导航完成
        """
        try:
            current_url = self.page.url
            
            # 如果已经在发布页面，直接等待标题输入框
            if '/post/video' in current_url:
                self.logger.info("当前已在发布页面")
                self.page.wait_for_selector('input.semi-input[placeholder*="填写作品标题"]', state="visible", timeout=30000)
                self.logger.info("页面可编辑")
                return True
            
            # 如果在上传页面，视频上传后会自动跳转到发布页面
            # 需要等待页面导航完成
            if '/content/upload' in current_url:
                self.logger.info("当前在上传页面，等待视频上传后页面自动跳转到发布页面...")
                try:
                    # 等待页面导航到发布页面
                    self.page.wait_for_url("**/post/video**", timeout=60000)
                    self.logger.info("页面已跳转到发布页面")
                except:
                    self.logger.info("未检测到页面跳转，检查当前URL")
                
                # 等待标题输入框出现
                self.page.wait_for_selector('input.semi-input[placeholder*="填写作品标题"]', state="visible", timeout=30000)
                self.logger.info("页面可编辑")
                return True
            
            # 其他情况，直接等待标题输入框
            self.page.wait_for_selector('input.semi-input[placeholder*="填写作品标题"]', state="visible", timeout=30000)
            self.logger.info("页面可编辑")
            return True
        except Exception as e:
            self.logger.warning(f"等待页面可编辑超时: {e}")
            return False
    
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
        """上传视频文件（参照测试代码：使用state="attached"处理隐藏input）"""
        try:
            self.logger.info(f"开始上传视频: {video_path}")
            file_input = self.page.locator('input[type="file"][accept*="video"]')
            file_input.wait_for(state="attached", timeout=30000)
            file_input.first.set_input_files(video_path)
            self.logger.info("视频上传触发成功")
            return True
        except Exception as e:
            self.logger.warning(f"视频上传失败: {str(e)}")
            return False
    
    def _check_video_already_uploaded(self):
        """检查视频是否已经上传完成"""
        try:
            current_url = self.page.url
            if '/post/video' in current_url:
                return True, "页面已跳转到发布页面，视频上传完成"
            
            video_element = self.page.locator('video')
            if video_element.count() > 0:
                return True, "检测到视频元素"
            
            progress_inner = self.page.locator('.upload-progress-inner')
            if progress_inner.count() == 0:
                return True, "未检测到上传进度条"
            
            return False, "未检测到视频已上传"
        except Exception as e:
            self.logger.warning(f"检查视频上传状态失败: {str(e)}")
            return False, str(e)

    def _wait_for_video_upload(self):
        """等待视频上传完成（参照测试代码）"""
        try:
            self.logger.info("开始等待视频上传完成")
            
            self.page.wait_for_selector('.upload-progress-inner', state="hidden", timeout=180000)
            self.page.wait_for_selector('video', state="attached", timeout=60000)
            
            self.logger.info("视频上传完成")
            return True
        except Exception as e:
            self.logger.warning(f"等待视频上传完成超时: {e}")
            return True
    
    def _fill_content(self, title, description):
        """填写标题和描述（参照测试代码）"""
        try:
            if title:
                trim_title = self.trim_title(title, 30)
                
                title_input = self.page.locator('input.semi-input[placeholder*="填写作品标题"]')
                title_input.wait_for(state="visible", timeout=10000)
                title_input.fill(trim_title)
                
                self.logger.info(f"填写标题（精简后）：{trim_title}")
            
            if description:
                desc_placeholder = self.page.locator('div[data-placeholder="添加作品简介"]')
                self.logger.info(f"查找简介placeholder: {desc_placeholder.count()}")
                if desc_placeholder.count() > 0:
                    desc_placeholder.first.click()
                    self.page.wait_for_timeout(500)
                    self.page.keyboard.type(description, delay=20)
                    self.logger.info(f"填写描述（完整）：{description[:50]}...")
                else:
                    desc_editor = self.page.locator('div.editor-comp-publish[contenteditable="true"]')
                    self.logger.info(f"查找editor-comp-publish: {desc_editor.count()}")
                    if desc_editor.count() > 0:
                        desc_editor.first.click()
                        self.page.wait_for_timeout(500)
                        self.page.keyboard.type(description, delay=20)
                        self.logger.info(f"填写描述（完整）：{description[:50]}...（备选方案）")
                    else:
                        textarea = self.page.locator('textarea[placeholder*="描述"], textarea[placeholder*="简介"]')
                        if textarea.count() > 0:
                            textarea.first.wait_for(state="visible", timeout=10000)
                            textarea.first.fill(description)
                            self.logger.info(f"填写描述（完整）：{description[:50]}...（textarea方案）")
            
            return True
        except Exception as e:
            self.logger.warning(f"填写内容失败: {str(e)}")
            return False
    
    def _set_schedule_time(self, schedule_time):
        """设置定时发布时间（参照测试代码）"""
        try:
            self.logger.info(f"开始设置定时发布时间: {schedule_time}")
            
            schedule_radio = self.page.locator('label:has-text("定时发布")')
            if schedule_radio.count() > 0:
                schedule_radio.wait_for(state="visible", timeout=10000)
                schedule_radio.click()
                self.page.wait_for_timeout(1000)
                self.logger.info("点击定时发布选项")
                
                self.page.wait_for_selector('.semi-datepicker', state="visible", timeout=5000)
                
                time_input = self.page.locator('.semi-datepicker-input input.semi-input')
                if time_input.count() > 0:
                    time_input.fill(schedule_time)
                    time_input.dispatch_event('blur')
                    self.logger.info(f"定时发布时间设置成功: {schedule_time}")
            
            return True
        except Exception as e:
            self.logger.warning(f"设置定时发布失败: {str(e)}")
            return False
    
    def _select_collection(self, collection_name):
        """选择合集（参照测试代码）"""
        if not collection_name:
            return True
            
        try:
            self.logger.info(f"开始选择合集: {collection_name}")
            
            collection_select = self.page.locator('.semi-select:has-text("请选择合集")')
            if collection_select.count() > 0:
                collection_select.wait_for(state="visible", timeout=10000)
                collection_select.click()
                self.page.wait_for_timeout(1000)
                
                self.page.wait_for_selector('.semi-popover', state="visible", timeout=5000)
                
                collection_options = self.page.locator('.collection-option')
                if collection_options.count() > 0:
                    for i in range(collection_options.count()):
                        option = collection_options.nth(i)
                        text = option.text_content()
                        if collection_name in text:
                            option.click()
                            self.logger.info(f"选择合集成功: {collection_name}")
                            return True
            
            self.logger.warning(f"未找到合集: {collection_name}")
            return False
        except Exception as e:
            self.logger.warning(f"选择合集失败: {str(e)}")
            return False
    
    def _select_ai_declaration(self, media_info):
        """选择AI内容声明（参照测试代码，使用测试验证的选择器）"""
        if not self.should_add_ai_label(media_info):
            self.logger.info("AI标注开关关闭，跳过AI内容声明")
            return
        try:
            self.logger.info("开始选择AI内容声明")
            
            declaration_select = self.page.locator('.selectBox-buZRzi:has(.selectText-XSrMFZ)')
            
            if declaration_select.count() == 0:
                declaration_select = self.page.locator('section:has-text("自主声明") div:has-text("请选择自主声明")')
            
            if declaration_select.count() > 0:
                declaration_select.wait_for(state="visible", timeout=10000)
                declaration_select.click()
                self.logger.info("点击自主声明下拉")
                
                self.page.wait_for_selector('.semi-modal-wrap', state="visible", timeout=5000)
                
                ai_option = self.page.locator('label.semi-radio:has-text("内容由AI生成")')
                if ai_option.count() > 0:
                    ai_option.click()
                    self.logger.info("已选择AI声明：内容由AI生成")
                    
                    confirm_btn = self.page.locator('.semi-modal-body button.semi-button-primary:has-text("确定")')
                    if confirm_btn.count() > 0:
                        confirm_btn.wait_for(state="visible", timeout=5000)
                        confirm_btn.click()
                        self.logger.info("点击确定按钮")
                        return True
            
            self.logger.warning("未找到自主声明选择器或AI声明选项")
            return False
        except Exception as e:
            self.logger.warning(f"自主声明处理失败: {str(e)}")
            return False
    
    def _upload_cover(self, media_info):
        """上传封面（双封面：横屏+竖屏，参照测试代码完整步骤）"""
        if not media_info:
            return True
        
        try:
            video_path = media_info.get('video_path', '')
            
            if not video_path:
                return True
            
            video_width, video_height = self._get_video_dimensions(video_path)
            is_horizontal = video_width > video_height if (video_width and video_height) else False
            self.logger.info(f"视频尺寸: {video_width}x{video_height}, 是否横屏: {is_horizontal}")
            
            cover_dir = media_info.get('cover_dir', os.path.dirname(video_path))
            
            if is_horizontal:
                horizontal_cover = media_info.get('cover_horizontal', os.path.join(cover_dir, "0_cover_350.png"))
                vertical_cover = media_info.get('cover_vertical', os.path.join(cover_dir, "0_cover_300.png"))
            else:
                horizontal_cover = None
                vertical_cover = media_info.get('cover_vertical', os.path.join(cover_dir, "0_cover.png"))
            
            cover_uploaded = False
            
            try:
                if is_horizontal:
                    # ======== 横屏视频处理逻辑 ========
                    # 1.点击横封面选择按钮
                    self._click_cover_button(is_horizontal)
                    self.logger.info("点击横封面选择按钮")
                    
                    # 等待弹窗出现
                    self.page.wait_for_selector('.dy-creator-content-modal', state="visible", timeout=15000)
                    self.logger.info("封面弹窗已出现")
                    
                    # 2.上传横封面
                    upload_success = self._upload_cover_image(horizontal_cover)
                    
                    if upload_success:
                        # 3.点击"设置竖封面"按钮（切换到竖封面选项卡）
                        if self._click_set_cover_button(is_horizontal):
                            # 4.等待选项卡切换，然后上传竖封面
                            self.page.wait_for_timeout(1000)
                            self._upload_cover_image(vertical_cover)
                    else:
                        self.logger.warning(f"横封面上传失败: 文件存在={os.path.exists(horizontal_cover)}")
                else:
                    # ======== 竖屏视频处理逻辑 ========
                    # 1.点击竖封面选择按钮
                    self._click_cover_button(is_horizontal)
                    self.logger.info("点击竖封面选择按钮")
                    
                    # 等待弹窗出现
                    self.page.wait_for_selector('.dy-creator-content-modal', state="visible", timeout=15000)
                    self.logger.info("封面弹窗已出现")
                    
                    # 2.上传竖封面
                    upload_success = self._upload_cover_image(vertical_cover)
                    
                    if upload_success:
                        # 3.点击"设置横封面"按钮（不用上传图片，直接使用竖封面裁剪）
                        self._click_set_cover_button(is_horizontal)
                    else:
                        self.logger.warning(f"竖封面上传失败: 文件存在={os.path.exists(vertical_cover)}")
                
                # ======== 通用步骤：点击完成 ========
                done_btn = self.page.locator('.dy-creator-content-modal button:has-text("完成")')
                if done_btn.count() > 0:
                    done_btn.first.click()
                    self.logger.info("点击完成按钮")
                    
                    # 等待弹窗消失（使用first定位，避免多个弹窗问题）
                    modal = self.page.locator('.dy-creator-content-modal').first
                    modal.wait_for(state="hidden", timeout=10000)
                    self.logger.info("封面上传完成")
                    cover_uploaded = True
                else:
                    self.logger.warning("未找到完成按钮")
                    
            except Exception as e:
                self.logger.warning(f"封面上传异常: {e}")
            
            if not cover_uploaded:
                self.logger.info("封面上传未成功，尝试使用AI智能推荐封面")
                try:
                    close_btn = self.page.locator('.dy-creator-content-modal [class*="close-"]')
                    if close_btn.count() > 0:
                        close_btn.first.click()
                        # 等待弹窗消失（使用first定位，避免多个弹窗问题）
                        modal = self.page.locator('.dy-creator-content-modal').first
                        modal.wait_for(state="hidden", timeout=5000)
                    
                    ai_covers = self.page.locator('[class*="recommendCoverContainer-"] [class*="recommendCover-"]')
                    self.logger.info(f"找到AI推荐封面数量: {ai_covers.count()}")
                    
                    if ai_covers.count() > 0:
                        ai_covers.first.click()
                        
                        selected = self.page.locator('[class*="recommendCoverContainer-"] [class*="recommendCover-"][class*="selected-"]')
                        selected.wait_for(state="visible", timeout=5000)
                        cover_uploaded = True
                        self.logger.info("AI推荐封面选择成功")
                    else:
                        ai_cover_imgs = self.page.locator('[class*="recommendCoverContainer-"] img')
                        if ai_cover_imgs.count() > 0:
                            ai_cover_imgs.first.click()
                            
                            selected = self.page.locator('[class*="recommendCoverContainer-"] [class*="selected-"]')
                            selected.wait_for(state="visible", timeout=5000)
                            cover_uploaded = True
                            self.logger.info("AI推荐封面选择成功（img方式）")
                except Exception as ai_e:
                    self.logger.warning(f"AI推荐封面选择失败: {ai_e}")
            
            return True
            
        except Exception as e:
            self.logger.warning(f"封面上传异常: {str(e)}")
            return True
    
    def _submit_publish(self):
        """提交发布（使用#popover-tip-container定位）"""
        try:
            # 根据HTML结构，发布按钮在#popover-tip-container下
            publish_button = self.page.locator('#popover-tip-container button:has-text("发布")')
            self.logger.info(f"查找发布按钮(#popover-tip-container): {publish_button.count()}")
            
            if publish_button.count() == 0:
                # 备选：使用类名定位
                publish_button = self.page.locator('button:has-text("发布")')
                self.logger.info(f"查找发布按钮(类名): {publish_button.count()}")            
            
            if publish_button.count() > 0:
                publish_button.first.click()
                self.logger.info("点击发布按钮")
            else:
                self.logger.warning("未找到发布按钮")
                return False
            
            return True
        except Exception as e:
            self.logger.warning(f"提交发布失败: {str(e)}")
            return False
    
    def _get_collection_name(self, media_info):
        return self.get_collection_name(media_info)
    
    def _wait_for_publish_success(self):
        """等待抖音发布成功
        
        抖音发布成功后：
        1. 页面跳转（framenavigated事件）
        2. URL变化（跳转到作品管理页面）
        3. 显示成功提示
        
        判断发布成功的关键：检查URL是否跳转到 /content/manage（最可靠的判断方式）
        
        注意：使用 load 状态而非 networkidle，因为抖音页面有轮询请求会导致 networkidle 永远不会到来
        """
        try:
            self.logger.info("等待抖音发布成功...")
            
            original_url = self.page.url
            
            try:
                self.page.wait_for_event("framenavigated", timeout=30000)
                self.logger.info("检测到页面跳转")
            except:
                self.logger.info("未检测到framenavigated事件，检查URL变化")
            
            # 等待URL变化（跳转到作品管理页面）
            try:
                self.page.wait_for_url("**/content/manage**", timeout=15000)
                self.logger.info("检测到页面跳转到作品管理页面")
            except:
                current_url = self.page.url
                if '/content/manage' in current_url:
                    self.logger.info(f"当前已在作品管理页面: {current_url}")
                else:
                    self.logger.warning(f"页面未跳转到作品管理页面，当前URL: {current_url}")
            
            # 关键：等待页面基本加载完成（使用 load 状态，比 networkidle 更可靠）
            # 抖音页面有轮询请求会导致 networkidle 永远不会到来
            self.logger.info("等待页面基本加载完成...")
            try:
                self.page.wait_for_load_state("load", timeout=10000)
            except:
                self.logger.info("页面加载状态等待超时，继续执行")
            
            # 等待页面稳定
            self.page.wait_for_timeout(2000)
            
            # 检查页面是否稳定（页面没有继续跳转）
            final_url = self.page.url
            if final_url != original_url:
                self.logger.info(f"确认页面已跳转，发布成功（{original_url} -> {final_url}）")
                return True, "抖音发布成功"
            else:
                self.logger.warning("页面URL未变化，等待额外时间确保数据提交...")
                self.page.wait_for_timeout(3000)
                return True, "抖音发布成功（URL未变化）"
        except Exception as e:
            self.logger.error(f"等待抖音发布成功失败: {str(e)}")
            # 即使出错，也等待一段时间确保数据提交
            self.page.wait_for_timeout(3000)
            return True, "抖音发布成功（异常）"

    def _handle_success_page(self, continue_publish=False):
        """处理发布成功页面
        
        判断发布成功的关键：检查页面是否跳转到 /content/manage（最可靠的判断方式）
        
        Args:
            continue_publish: 是否需要继续发布下一个视频
                              True: 需要返回发布页面（批量发布时）
                              False: 不需要返回发布页面（单个视频发布时，只等待页面跳转完成）
        
        按钮HTML结构：
        <button class="douyin-creator-master-button-primary">
            <span class="header-button-text-Ww8aQU">高清发布</span>
        </button>
        """
        try:
            current_url = self.page.url
            self.logger.info(f"当前页面URL: {current_url}")
            
            # 检查是否在作品管理页面（最可靠的判断方式）
            if '/content/manage' in current_url:
                self.logger.info("检测到发布成功页面（URL包含 /content/manage）")
                
                # 等待页面基本加载完成（使用 load 状态，比 networkidle 更可靠）
                try:
                    self.page.wait_for_load_state("load", timeout=10000)
                except:
                    self.logger.info("页面加载状态等待超时，继续执行")
                
                # 等待页面稳定
                self.page.wait_for_timeout(1500)
                
                # 如果需要继续发布，才执行跳转到发布页面的操作
                if continue_publish:
                    self.logger.info("需要继续发布，准备返回发布页面")
                    
                    # 方案1：使用按钮文本"高清发布"定位
                    publish_btn = self.page.locator('text="高清发布"')
                    self.logger.info(f"查找高清发布按钮(文本): {publish_btn.count()} 个")
                    
                    if publish_btn.count() > 0:
                        publish_btn.first.click()
                        self.logger.info("点击高清发布按钮")
                        # 等待页面跳转到发布页面
                        try:
                            self.page.wait_for_url("**/content/upload**", timeout=10000)
                            self.logger.info("已成功跳转到发布页面")
                        except:
                            try:
                                self.page.wait_for_load_state("load", timeout=10000)
                            except:
                                pass
                            self.page.wait_for_timeout(2000)
                            self.logger.info("等待页面加载完成")
                        return True
                    
                    # 方案2：使用按钮class定位
                    class_btn = self.page.locator('.douyin-creator-master-button-primary')
                    self.logger.info(f"查找高清发布按钮(类名): {class_btn.count()} 个")
                    
                    if class_btn.count() > 0:
                        class_btn.first.click()
                        self.logger.info("点击高清发布按钮(类名)")
                        try:
                            self.page.wait_for_load_state("load", timeout=10000)
                        except:
                            pass
                        self.page.wait_for_timeout(2000)
                        return True
                    
                    # 方案3：使用按钮id定位
                    id_btn = self.page.locator('#douyin-creator-master-side-upload')
                    self.logger.info(f"查找高清发布按钮(id): {id_btn.count()} 个")
                    
                    if id_btn.count() > 0:
                        id_btn.first.click()
                        self.logger.info("点击高清发布按钮(id)")
                        try:
                            self.page.wait_for_load_state("load", timeout=10000)
                        except:
                            pass
                        self.page.wait_for_timeout(2000)
                        return True
                    
                    # 方案4：使用父容器定位
                    wrap_btn = self.page.locator('#douyin-creator-master-side-upload-wrap button')
                    self.logger.info(f"查找高清发布按钮(父容器): {wrap_btn.count()} 个")
                    
                    if wrap_btn.count() > 0:
                        wrap_btn.first.click()
                        self.logger.info("点击高清发布按钮(父容器)")
                        try:
                            self.page.wait_for_load_state("load", timeout=10000)
                        except:
                            pass
                        self.page.wait_for_timeout(2000)
                        return True
                    
                    # 方案5：关闭当前页面并重新创建（兜底方案，最可靠）
                    self.logger.warning("未找到高清发布按钮，关闭当前页面并重新创建")
                    try:
                        from browser.browser_singleton import get_platform_page
                        self.page = get_platform_page("抖音", force_new=True)
                        self._navigate(self.PUBLISH_URL)
                        self.page.wait_for_timeout(3000)
                        return True
                    except Exception as e:
                        self.logger.error(f"重新创建页面失败: {str(e)}")
                        return False
                else:
                    self.logger.info("不需要继续发布，等待页面稳定后结束")
                    # 单个视频发布时，只等待页面跳转完成，不执行跳转操作
                    self.page.wait_for_timeout(2000)
                    return True
            
            self.logger.info("当前不在发布成功页面，无需处理")
            return True
        except Exception as e:
            self.logger.warning(f"处理成功页面失败: {str(e)}")
            # 如果需要继续发布，关闭当前页面并重新创建（兜底方案）
            if continue_publish:
                try:
                    from browser.browser_singleton import get_platform_page
                    self.page = get_platform_page("抖音", force_new=True)
                    self._navigate(self.PUBLISH_URL)
                except:
                    pass
            return True

    def _fill_all_content(self, media_info, content, publish_strategy):
        """填写所有内容（标题、描述、合集、AI声明、定时发布）"""
        try:
            self.submit_mode = publish_strategy.get('mode', 'publish')
            
            self._wait_for_page_editable()
            
            self._fill_content(content.get('title', ''), content.get('description', ''))
            self._select_collection(self._get_collection_name(media_info))
            self._select_ai_declaration(media_info)

            publish_time = publish_strategy.get("time", "")
            if publish_time:
                self._set_schedule_time(publish_time)
            
            self.logger.info("内容填写完成")
            return True
        except Exception as e:
            self.logger.error(f"填写内容失败: {str(e)}")
            return False

def create_publisher(page, browser_config):
    return DouyinPublisher(page, browser_config)