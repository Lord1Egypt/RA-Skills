import logging
import os
import sys
from datetime import datetime, timedelta
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

class ChannelsPublisher(BasePublisher):
    """视频号发布器 - 实现微信视频号创作者后台发布流程"""
    
    PUBLISH_URL = "https://channels.weixin.qq.com/platform/post/create"
    LOGIN_URL_KEYWORDS = ["login.html", "/login", "weixin.qq.com/cgi-bin/loginpage"]
    
    def __init__(self, page, browser_config):
        super().__init__(page, browser_config)
        self.submit_model = 'publish'
    
    def _ensure_on_publish_page(self, publish_url):
        """确保当前在发布页面（视频号专用，处理登录重定向）
        
        视频号登录页面有多次重定向，需要特殊处理：
        1. 如果当前已在发布页面，直接返回
        2. 如果在登录页面，等待用户完成扫码登录
        3. 登录成功后等待页面跳转到发布页面
        """
        try:
            max_retries = 5
            retry_count = 0
            
            while retry_count < max_retries:
                current_url = self.page.url
                self.logger.info(f"当前页面URL: {current_url}")
                
                # 检查是否已在发布页面
                if publish_url in current_url or "/platform/post/create" in current_url:
                    self.logger.info(f"当前已在发布页面: {current_url}")
                    return True
                
                # 检查是否在登录页面
                is_login_page = any(keyword in current_url.lower() for keyword in self.LOGIN_URL_KEYWORDS)
                if is_login_page:
                    self.logger.info("检测到登录页面，等待用户完成登录...")
                    # 等待登录完成（最多120秒）
                    login_timeout = 120
                    check_interval = 3
                    elapsed = 0
                    
                    while elapsed < login_timeout:
                        try:
                            # 检查是否跳转到了发布页面
                            if publish_url in self.page.url or "/platform/post/create" in self.page.url:
                                self.logger.info(f"登录成功，已跳转到发布页面: {self.page.url}")
                                return True
                            
                            # 检查是否有扫码登录元素（表示仍在登录页面）
                            login_qrcode = self.page.locator('img[src*="qrcode"], .qrcode-img, .login-qrcode')
                            if login_qrcode.count() > 0:
                                self.logger.info(f"等待登录中... ({elapsed}/{login_timeout}秒)")
                            else:
                                # 可能正在跳转，等待一下
                                self.page.wait_for_timeout(1000)
                            
                            elapsed += check_interval
                            self.page.wait_for_timeout(check_interval * 1000)
                            
                        except Exception as e:
                            self.logger.warning(f"等待登录时出错: {e}")
                            break
                    
                    self.logger.warning("登录等待超时，尝试重新导航")
                    retry_count += 1
                    continue
                
                # 如果不在发布页面也不在登录页面，尝试导航
                self.logger.info(f"当前页面: {current_url}，导航到发布页面: {publish_url}")
                success = self._navigate(publish_url)
                if success:
                    # 等待页面加载并检查是否跳转成功
                    self.page.wait_for_timeout(3000)
                    # 检查是否跳转到了登录页面
                    if any(keyword in self.page.url.lower() for keyword in self.LOGIN_URL_KEYWORDS):
                        self.logger.info("导航后跳转到了登录页面")
                        continue
                    # 检查是否在发布页面
                    if publish_url in self.page.url or "/platform/post/create" in self.page.url:
                        return True
                    # 页面可能还在加载，等待一下
                    self._wait_for_page_load()
                    if publish_url in self.page.url or "/platform/post/create" in self.page.url:
                        return True
                
                retry_count += 1
                self.page.wait_for_timeout(2000)
            
            self.logger.warning(f"导航到发布页面失败，重试次数: {max_retries}")
            return False
            
        except Exception as e:
            self.logger.error(f"确保在发布页面失败: {str(e)}")
            return False
    
    def publish(self, media_info, content, publish_strategy):
        """发布视频到视频号（参照快手执行顺序）"""
        self.logger.info(f"开始发布视频号：{media_info.get('name', '')}")
        
        try:
            self.submit_model = publish_strategy.get('submit_model', 'publish')
            self.logger.info(f"发布模式: {self.submit_model}")
            
            if not self._ensure_on_publish_page(self.PUBLISH_URL):
                return False, "导航失败"
            
            video_already_uploaded = self._handle_continue_edit_prompt()
            need_wait_video = False
            if not video_already_uploaded:
                if not self._upload_video(media_info['video_path']):
                    return False, "视频上传失败"
                need_wait_video = True

            self._fill_title(content['title'])
            self._fill_description(content['description'])
            
            collection_name = self._get_collection_name(media_info)
            if collection_name:
                self._select_collection(collection_name)

            self._handle_original_declaration()

            if publish_strategy.get('time'):
                self._set_schedule_time(publish_strategy['time'])

            if need_wait_video:
                self._wait_for_video_upload()

            self._upload_cover(media_info)

            if not self._submit_publish():
                return False, "提交发布失败"

            return True, "发布成功"
            
        except Exception as e:
            self.logger.error(f"视频号发布异常: {str(e)}")
            self._take_screenshot("channels_error")
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
        """上传视频文件"""
        try:
            video_input = self.page.locator('.ant-upload input[type="file"]')
            video_input.wait_for(state="attached", timeout=10000)
            if video_input.count() > 0:
                video_input.first.set_input_files(video_path)
                self.logger.info(f"视频上传触发成功: {video_path}")
                return True
            self.logger.warning("未找到视频上传input")
            return False
        except Exception as e:
            self.logger.error(f"上传视频失败: {str(e)}")
            return False
    
    def _check_video_already_uploaded(self):
        """检查视频是否已经上传完成"""
        try:
            video_preview = self.page.locator('.post-media-wrap video')
            if video_preview.count() > 0:
                return True, "检测到视频预览元素"
            
            media_info = self.page.locator('.post-media-wrap')
            if media_info.count() > 0:
                return True, "检测到视频媒体区域"
            
            return False, "未检测到视频已上传"
        except Exception as e:
            self.logger.warning(f"检查视频上传状态失败: {str(e)}")
            return False, str(e)

    def _wait_for_video_upload(self):
        """等待视频上传完成"""
        try:
            self._wait_for_selector('.post-media-wrap', state="visible", timeout=120000)
            self.logger.info("视频上传完成")
            return True
        except Exception as e:
            self.logger.error(f"等待视频上传失败: {str(e)}")
            return False
    
    def _fill_title(self, title):
        """填写短标题（优先判断长度）"""
        try:
            if not title:
                return True
            
            max_len = 16
            self.logger.info(f"原始标题: {title}, 长度: {len(title)}, 最大长度: {max_len}")
            
            if len(title) <= max_len:
                trim_title = title
                self.logger.info(f"标题长度符合要求，无需截取")
            else:
                trim_title = self.trim_title(title, max_len)
                self.logger.info(f"标题截取后: {trim_title}, 长度: {len(trim_title)}")
            
            title_input = self.page.locator('input[placeholder="填写短标题有机会获得更多流量"]')
            if title_input.count() == 0:
                title_input = self.page.locator('.post-short-title-wrap input')
            if title_input.count() == 0:
                title_input = self.page.locator('[class*="short-title"] input')
            
            self.logger.info(f"短标题输入框数量: {title_input.count()}")
            if title_input.count() > 0:
                title_input.first.wait_for(state="visible", timeout=10000)
                title_input.first.fill(trim_title)
                self.logger.info(f"短标题填写成功: {trim_title}")
                return True
            self.logger.warning("未找到短标题输入框")
            return False
        except Exception as e:
            self.logger.error(f"填写短标题失败: {str(e)}")
            return False
    
    def _fill_description(self, description):
        """填写视频描述"""
        try:
            if not description:
                return True
            
            desc_editor = self.page.locator('.input-editor')
            if desc_editor.count() == 0:
                desc_editor = self.page.locator('[class*="editor"]')
            if desc_editor.count() == 0:
                desc_editor = self.page.locator('textarea')
            
            self.logger.info(f"描述编辑器数量: {desc_editor.count()}")
            if desc_editor.count() > 0:
                desc_editor.first.wait_for(state="visible", timeout=10000)
                desc_editor.first.click()
                self.page.wait_for_timeout(500)
                desc_editor.first.fill(description)
                self.logger.info(f"描述填写成功: {description[:50]}...")
                return True
            self.logger.warning("未找到描述编辑器")
            return False
        except Exception as e:
            self.logger.error(f"填写描述失败: {str(e)}")
            return False
    
    def _select_collection(self, collection_name):
        """选择合集"""
        try:
            album_select = self.page.locator('.post-album-display-wrap:has-text("选择合集")')
            if album_select.count() > 0:
                album_select.first.click()
                self.logger.info(f"已点击选择合集按钮，等待选项加载")
                
                album_option = self.page.locator(f'.option-item:has-text("{collection_name}")')
                album_option.first.wait_for(state="visible", timeout=10000)
                
                if album_option.count() > 0:
                    album_option.first.click()
                    self.logger.info(f"合集选择成功（{collection_name}）")
                    return True
                self.logger.warning(f"未找到合集选项: {collection_name}")
                return False
            self.logger.warning("未找到合集选择区域")
            return False
        except Exception as e:
            self.logger.error(f"选择合集失败: {str(e)}")
            return False
    
    def _handle_original_declaration(self):
        """处理原创声明"""
        try:
            original_checkbox = self.page.locator('.declare-original-checkbox .ant-checkbox-input')
            if original_checkbox.count() == 0:
                original_checkbox = self.page.locator('[class*="declare-original"] .ant-checkbox-input')
            
            if original_checkbox.count() > 0:
                original_checkbox.first.wait_for(state="visible", timeout=10000)
                original_checkbox.first.click()
                self.logger.info("已点击原创声明复选框")
                
                dialog_wrp = self.page.locator('.declare-original-dialog .weui-desktop-dialog__wrp')
                if dialog_wrp.count() == 0:
                    dialog_wrp = self.page.locator('.weui-desktop-dialog__wrp')
                
                dialog_wrp.first.wait_for(state="visible", timeout=5000)
                self.logger.info("原创声明弹窗已出现")
                
                agree_checkbox = self.page.locator('.declare-original-dialog .original-proto-wrapper .ant-checkbox-input')
                if agree_checkbox.count() == 0:
                    agree_checkbox = self.page.locator('.declare-original-dialog .ant-checkbox-input')
                if agree_checkbox.count() == 0:
                    agree_checkbox = self.page.locator('.weui-desktop-dialog__wrp .ant-checkbox-input')
                
                if agree_checkbox.count() > 0:
                    agree_checkbox.first.wait_for(state="visible", timeout=5000)
                    agree_checkbox.first.click()
                    self.logger.info("已勾选同意协议")
                else:
                    self.logger.warning("未找到同意协议复选框")
                
                confirm_btn = self.page.locator('.declare-original-dialog .weui-desktop-dialog__ft .weui-desktop-btn_primary:not(.weui-desktop-btn_disabled)')
                if confirm_btn.count() == 0:
                    confirm_btn = self.page.locator('.weui-desktop-dialog__ft .weui-desktop-btn_primary:not(.weui-desktop-btn_disabled)')
                if confirm_btn.count() == 0:
                    confirm_btn = self.page.locator('.weui-desktop-dialog__ft button:has-text("确认")')
                
                if confirm_btn.count() > 0:
                    confirm_btn.first.wait_for(state="visible", timeout=5000)
                    confirm_btn.first.click()
                    self.logger.info("原创声明处理成功")
                    
                    dialog_wrp.first.wait_for(state="hidden", timeout=15000)
                    self.logger.info("原创声明弹窗已关闭")
            else:
                self.logger.warning("未找到原创声明复选框")
            return True
        except Exception as e:
            self.logger.error(f"处理原创声明失败: {str(e)}")
            return False
    
    def _set_schedule_time(self, schedule_time):
        """设置定时发布时间"""
        try:
            target_date = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M")
            
            schedule_label = self.page.locator('.post-time-wrap .weui-desktop-form__check-label').nth(1)
            if schedule_label.count() > 0:
                schedule_label.wait_for(state="visible", timeout=10000)
                schedule_label.click()
                self.logger.info("已选择定时发布")
                
                self.page.wait_for_selector('.weui-desktop-picker__date', state="visible", timeout=5000)
                
                date_picker = self.page.locator('.weui-desktop-picker__date')
                if date_picker.count() > 0:
                    date_picker.click()
                    self.page.wait_for_selector('.weui-desktop-picker__panel_day', state="visible", timeout=5000)
                    self.logger.info("日期选择器弹窗已打开")
                    
                    target_day = target_date.day
                    target_month = f"{target_date.month:02d}月"
                    target_year = f"{target_date.year}年"
                    
                    max_attempts = 12
                    attempt = 0
                    while attempt < max_attempts:
                        current_month = self.page.locator('.weui-desktop-picker__panel__label').nth(1).text_content()
                        current_year = self.page.locator('.weui-desktop-picker__panel__label').nth(0).text_content()
                        if target_month in str(current_month) and target_year in str(current_year):
                            break
                        right_arrow = self.page.locator('.weui-desktop-btn__icon__right')
                        if right_arrow.count() > 0:
                            right_arrow.click()
                            self.page.wait_for_timeout(300)
                        attempt += 1
                    
                    day_str = str(target_day)
                    date_item = self.page.locator(f'.weui-desktop-picker__table a:not(.weui-desktop-picker__disabled):not(.weui-desktop-picker__faded):text-is("{day_str}")')
                    if date_item.count() > 0:
                        date_item.first.click()
                        self.logger.info(f"日期选择成功: {target_date.strftime('%Y-%m-%d')}")
                        self.page.wait_for_timeout(500)
                    else:
                        date_item_fallback = self.page.locator(f'.weui-desktop-picker__table a:text-is("{day_str}")')
                        if date_item_fallback.count() > 0:
                            date_item_fallback.nth(1).click()
                            self.logger.info(f"日期选择成功（fallback）: {target_date.strftime('%Y-%m-%d')}")
                            self.page.wait_for_timeout(500)
                    
                    time_picker = self.page.locator('.weui-desktop-picker__time')
                    if time_picker.count() > 0:
                        time_picker.click()
                        self.page.wait_for_selector('.weui-desktop-picker__dd__time', state="visible", timeout=5000)
                        self.logger.info("时间选择器面板已打开")
                        
                        hour_str = str(target_date.hour).zfill(2)
                        minute_str = str(target_date.minute).zfill(2)
                        
                        hour_item = self.page.locator(f'.weui-desktop-picker__time__hour li:text-is("{hour_str}")')
                        if hour_item.count() > 0:
                            hour_item.first.scroll_into_view_if_needed()
                            self.page.wait_for_timeout(300)
                            hour_item.first.click()
                            self.logger.info(f"小时选择成功: {hour_str}")
                            self.page.wait_for_timeout(300)
                        
                        minute_item = self.page.locator(f'.weui-desktop-picker__time__minute li:text-is("{minute_str}")')
                        if minute_item.count() > 0:
                            minute_item.first.scroll_into_view_if_needed()
                            self.page.wait_for_timeout(300)
                            minute_item.first.click()
                            self.logger.info(f"分钟选择成功: {minute_str}")
                            self.page.wait_for_timeout(300)
                        
                        self.page.click("html")
                        self.logger.info("点击空白区域关闭时间选择弹窗")
                        self.page.wait_for_timeout(300)
                
                self.logger.info(f"定时发布时间设置成功: {target_date.strftime('%Y-%m-%d %H:%M')}")
                return True
            self.logger.warning("未找到定时发布选项")
            return False
        except Exception as e:
            self.logger.error(f"设置定时发布失败: {str(e)}")
            return False
    
    def _upload_cover(self, media_info):
        """上传封面图片（完整流程）"""
        try:
            cover_path = self.get_cover_path(media_info)
            if not cover_path or not os.path.exists(cover_path):
                self.logger.info("封面文件不存在，跳过封面上传")
                return True
            
            self.logger.info(f"开始上传封面: {cover_path}")
            
            cover_wrap = self.page.locator('.cover-preview-wrap .vertical-cover-wrap.img-popover-wrap')
            self.logger.info(f"封面区域元素数量: {cover_wrap.count()}")
            
            if cover_wrap.count() > 0:
                cover_wrap.first.wait_for(state="visible", timeout=10000)
                cover_wrap.first.click()
                self.logger.info("【步骤1】已点击封面区域触发编辑弹窗")
                
                dialog_wrp = self.page.locator('.edit-cover-dialog .weui-desktop-dialog__wrp')
                if dialog_wrp.count() > 0:
                    dialog_wrp.first.wait_for(state="visible", timeout=10000)
                    self.logger.info("【步骤2】封面编辑弹窗已出现")
                    
                    cover_input = self.page.locator('.edit-cover-dialog .single-cover-uploader-wrap input[type="file"]')
                    self.logger.info(f"【步骤2】找到{cover_input.count()}个file input")
                    
                    if cover_input.count() > 0:
                        cover_input.first.set_input_files(cover_path)
                        self.logger.info(f"【步骤2】封面文件上传: {cover_path}")
                    else:
                        upload_btn = self.page.locator('.edit-cover-dialog .single-cover-uploader-wrap .text-wrap')
                        if upload_btn.count() > 0:
                            upload_btn.first.click()
                            self.logger.info("【步骤2】已点击上传封面按钮")
                    
                    finish_wrap = self.page.locator('.edit-cover-dialog .single-cover-uploader-wrap .finish-wrap')
                    finish_wrap.first.wait_for(state="visible", timeout=30000)
                    self.logger.info("【步骤3】封面上传完成（finish-wrap已出现）")
                    
                    confirm_btn = self.page.locator('.edit-cover-dialog .weui-desktop-dialog__ft .weui-desktop-btn_wrp:not(.cancel) button:has-text("确认")')
                    if confirm_btn.count() > 0:
                        confirm_btn.first.wait_for(state="visible", timeout=5000)
                        confirm_btn.first.click()
                        self.logger.info("【步骤4】已点击确认按钮")
                        
                        dialog_wrp.first.wait_for(state="hidden", timeout=15000)
                        self.logger.info("【步骤4】封面弹窗已关闭，应用封面完成")
                    
                    horizon_cover = self.page.locator('.cover-preview-wrap .horizon-cover-wrap')
                    if horizon_cover.count() > 0:
                        self.logger.info("【步骤5】检测到4:3封面区域，需要设置")
                        
                        horizon_edit = self.page.locator('.cover-preview-wrap .horizon-cover-wrap.img-popover-wrap')
                        if horizon_edit.count() > 0:
                            horizon_edit.first.wait_for(state="visible", timeout=10000)
                            horizon_edit.first.click()
                            self.logger.info("【步骤6】已点击4:3封面的编辑按钮")
                            
                            use_material_btn = self.page.locator('.ant-popover .img-recommend-wrap .btn-wrap button:has-text("使用素材")')
                            if use_material_btn.count() > 0:
                                use_material_btn.first.wait_for(state="visible", timeout=5000)
                                use_material_btn.first.click()
                                self.logger.info("【步骤6】已点击使用素材按钮")
                                
                                dialog_wrp = self.page.locator('.edit-cover-dialog .weui-desktop-dialog__wrp')
                                dialog_wrp.first.wait_for(state="visible", timeout=10000)
                                self.logger.info("【步骤6】封面上传弹窗再次出现")
                                
                                horizon_confirm_btn = self.page.locator('.edit-cover-dialog .weui-desktop-dialog__ft .weui-desktop-btn_wrp:not(.cancel) button:has-text("确认")')
                                if horizon_confirm_btn.count() > 0:
                                    horizon_confirm_btn.first.wait_for(state="visible", timeout=5000)
                                    horizon_confirm_btn.first.click()
                                    self.logger.info("【步骤6】已点击确认按钮")
                                    
                                    dialog_wrp.first.wait_for(state="hidden", timeout=15000)
                                    self.logger.info("【步骤6】4:3封面设置完成")
                            else:
                                self.logger.warning("【步骤6】未找到使用素材按钮")
                        else:
                            self.logger.warning("【步骤6】未找到4:3封面的编辑按钮")
                    else:
                        self.logger.info("【步骤5】未检测到4:3封面区域，跳过")
                else:
                    self.logger.warning("【步骤2】封面编辑弹窗未出现")
            else:
                self.logger.warning("【步骤1】未找到封面区域元素")
                return False
            
            self.logger.info("封面上传完成！")
            return True
            
        except Exception as e:
            self.logger.warning(f"封面上传异常: {str(e)}")
            return False
    
    def _submit_publish(self):
        """提交发布"""
        try:
            original_url = self.page.url
            # 表单底部的按钮：保存草稿，手机预览，发表
            form_btns = self.page.locator('.form-btns .weui-desktop-btn')
            if form_btns.count() == 0:
                self.logger.warning("未找到表单按钮区域")
                return False
            
            # 滚到到表单按钮位置
            form_btns.first.scroll_into_view_if_needed()
            form_btns.first.wait_for(state="visible", timeout=2000)
            self.logger.info(f"表单按钮数量：{form_btns.count()}")

            if self.submit_model =='draft':
                draft_btn = form_btns.filter(has_text="保存草稿")
                if draft_btn.count() > 0:
                    draft_btn.first.click()
                    self.logger.info("已点击保存草稿")
                else:
                    self.logger.warning("未找到保存草稿按钮")
                    return False
            else:
                publish_btn = form_btns.filter(has_text="发表")
                if publish_btn.count() > 0:
                    publish_btn.first.click()
                    self.logger.info("已点击发表")
                else:
                    self.logger.warning("未找到发表按钮")
                    return False
   
            try:
                self.page.wait_for_event("framenavigated", timeout=15000)
                self.logger.info("检测到页面跳转，视频号发布成功")
            except:
                if self.page.url != original_url:
                    self.logger.info("页面URL已变化，视频号发布成功")
                else:
                    self.logger.info("等待发布提交完成...")
                    self.page.wait_for_timeout(3000)
                    
                    if self.page.locator('.weui-desktop-toast').count() > 0:
                        self.logger.info("检测到成功提示，视频号发布成功")
                    elif self.page.locator('.post-media-wrap').count() == 0:
                        self.logger.info("视频区域已清空，视频号发布成功")
                    else:
                        self.logger.warning("页面未跳转，但发布按钮已点击")
            
            return True
        except Exception as e:
            self.logger.error(f"提交发布失败: {str(e)}")
            return False
    
    def _get_collection_name(self, media_info):
        return self.get_collection_name(media_info)
    
    def _wait_for_publish_success(self):
        """等待视频号发布成功
        
        视频号发布成功后：
        1. 页面跳转（framenavigated事件）
        2. URL变化
        3. 显示成功提示（.weui-desktop-toast）
        4. 视频区域清空（.post-media-wrap数量为0）
        """
        try:
            self.logger.info("等待视频号发布成功...")
            
            try:
                self.page.wait_for_event("framenavigated", timeout=15000)
                self.logger.info("检测到页面跳转，视频号发布成功")
                return True, "视频号发布成功"
            except:
                if self.page.url != self.page.url:
                    self.logger.info("页面URL已变化，视频号发布成功")
                    return True, "视频号发布成功"
                else:
                    self.logger.info("等待发布提交完成...")
                    self.page.wait_for_timeout(3000)
                    
                    if self.page.locator('.weui-desktop-toast').count() > 0:
                        self.logger.info("检测到成功提示，视频号发布成功")
                        return True, "视频号发布成功"
                    elif self.page.locator('.post-media-wrap').count() == 0:
                        self.logger.info("视频区域已清空，视频号发布成功")
                        return True, "视频号发布成功"
                    else:
                        self.logger.warning("页面未跳转，但发布按钮已点击")
                        return True, "视频号发布成功（未检测到跳转）"
        except Exception as e:
            self.logger.error(f"等待视频号发布成功失败: {str(e)}")
            return True, "视频号发布成功（异常）"

    def _fill_all_content(self, media_info, content, publish_strategy):
        """填写所有内容（标题、描述、合集、AI声明、视频标注、定时发布）"""
        try:
            self.submit_model = publish_strategy.get('submit_model', 'publish')
            
            self._fill_title(content['title'])
            self._fill_description(content['description'])
            
            collection_name = self._get_collection_name(media_info)
            if collection_name:
                self._select_collection(collection_name)

            self._handle_original_declaration()
            
            self._select_video_mark_tag(media_info)

            if publish_strategy.get('time'):
                self._set_schedule_time(publish_strategy['time'])
            
            self.logger.info("内容填写完成")
            return True
        except Exception as e:
            self.logger.error(f"填写内容失败: {str(e)}")
            return False
    
    def _select_video_mark_tag(self, media_info):
        """选择视频标注（含AI生成内容）"""
        if not self.should_add_ai_label(media_info):
            self.logger.info("AI标注开关关闭，跳过AI视频标注")
            return
        try:
            select_display = self.page.locator('.mark-tag-select .select-display')
            if select_display.count() == 0:
                self.logger.info("未找到视频标注选择器，跳过")
                return True
            
            select_display.first.click()
            self.logger.info("已点击视频标注下拉框")
            
            self.page.wait_for_selector('.mark-tag-options', state="visible", timeout=5000)
            
            ai_option = self.page.locator('.mark-tag-option:has-text("含AI生成内容")')
            if ai_option.count() > 0:
                ai_option.first.click()
                self.logger.info("已选择视频标注：含AI生成内容")
            else:
                self.logger.warning("未找到含AI生成内容选项")
            
            return True
        except Exception as e:
            self.logger.warning(f"选择视频标注失败: {str(e)}")
            return True

def create_publisher(page, browser_config):
    return ChannelsPublisher(page, browser_config)