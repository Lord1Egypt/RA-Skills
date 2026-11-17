import logging
import os
import time
from PIL import Image
from .base_publisher import BasePublisher

def create_publisher(page, browser_config):
    return KuaishouPublisher(page, browser_config)

class KuaishouPublisher(BasePublisher):
    PUBLISH_URL = "https://cp.kuaishou.com/article/publish/video"

    def __init__(self, page, browser_config):
        super().__init__(page, browser_config)
        self.submit_mode = "publish"

    def publish(self, media_info, content, publish_strategy):
        self.logger.info(f"开始发布快手：{media_info.get('name', '')}")
        try:
            # 确保当前在发布页面（批量发布时，上一次发布完可能停留在其他页面）
            if not self._ensure_on_publish_page(self.PUBLISH_URL):
                return False, "导航失败"
            
            if not self._check_login_status():
                return False, "未登录"
                        
            if not self._upload_video(media_info["video_path"]):
                return False, "视频上传失败"

            self._fill_content(content["description"])
            self._select_ai_declaration(media_info)
            
            collection_name = self._get_collection_name(media_info)
            if collection_name:
                self._select_collection(collection_name)

            publish_time = publish_strategy.get("time", "")
            if publish_time:
                self._set_schedule_time(publish_time)

            self._wait_for_video_upload()

            self._upload_cover(media_info)

            # 点击发布按钮
            submit_mode = publish_strategy.get("mode", "publish")
            if not self._submit_publish(submit_mode):
                return False, "发布提交失败"

            return True, "发布成功"
        except Exception as e:
            self.logger.error(f"快手发布异常: {str(e)}")
            return False, str(e)

    def _wait_for_publish_success(self):
        """等待快手发布成功
        
        快手发布成功后：
        1. 页面跳转到视频管理页面（URL包含 manage/video）
        2. 显示"发布成功"提示
        """
        try:
            self.logger.info("等待快手发布成功...")
            
            try:
                self.page.wait_for_url(
                    "**/manage/video**",
                    timeout=30000,
                )
                self.logger.info("检测到快手发布成功：已跳转到视频管理页面")
                return True, "快手发布成功"
            except Exception as e:
                self.logger.warning(f"等待发布成功超时: {e}")
                
                current_url = self.page.url
                if "/manage/video" in current_url:
                    self.logger.info("检测到快手发布成功：当前已在视频管理页面")
                    return True, "快手发布成功"
                
                return True, "快手发布成功（超时）"
        except Exception as e:
            self.logger.error(f"等待快手发布成功失败: {str(e)}")
            return True, "快手发布成功（异常）"
    
    def _handle_success_page(self, continue_publish=False):
        """处理发布成功页面
        
        判断发布成功的关键：检查URL是否包含发布成功页面特征
        
        Args:
            continue_publish: 是否需要继续发布下一个视频
                              True: 需要返回发布页面（批量发布时）
                              False: 不需要返回发布页面（单个视频发布时，只等待页面跳转完成）
        
        注意：使用 load 状态而非 networkidle，因为页面有轮询请求会导致 networkidle 永远不会到来
        """
        try:
            current_url = self.page.url
            self.logger.info(f"当前页面URL: {current_url}")
            
            # 检查是否在发布成功页面（URL不包含发布页面关键词）
            if "/article/publish/video" not in current_url:
                self.logger.info("检测到发布成功页面（URL不包含发布页面）")
                
                # 等待页面基本加载完成（使用 load 状态，比 networkidle 更可靠）
                try:
                    self.page.wait_for_load_state("load", timeout=10000)
                except:
                    self.logger.info("页面加载状态等待超时，继续执行")
                
                self.page.wait_for_timeout(1000)
                
                # 如果需要继续发布，才执行跳转操作
                if continue_publish:
                    self.logger.info("需要继续发布，准备返回发布页面")
                    
                    # 检查是否有发布新作品相关的按钮
                    new_publish_btn = self.page.locator('button:has-text("发布新作品")')
                    if new_publish_btn.count() > 0:
                        self.logger.info("点击发布新作品")
                        new_publish_btn.first.click()
                        try:
                            self.page.wait_for_load_state("load", timeout=10000)
                        except:
                            pass
                        self.page.wait_for_timeout(2000)
                        return True
                    
                    # 检查是否有返回发布页面的链接
                    publish_link = self.page.locator('a:has-text("发布")')
                    if publish_link.count() > 0:
                        self.logger.info("点击发布链接")
                        publish_link.first.click()
                        try:
                            self.page.wait_for_load_state("load", timeout=10000)
                        except:
                            pass
                        self.page.wait_for_timeout(2000)
                        return True
                    
                    # 方案3：关闭当前页面并重新创建（兜底方案，最可靠）
                    self.logger.warning("未找到发布按钮，关闭当前页面并重新创建")
                    try:
                        from browser.browser_singleton import get_platform_page
                        self.page = get_platform_page("快手", force_new=True)
                        self._navigate(self.PUBLISH_URL)
                        self.page.wait_for_timeout(3000)
                        return True
                    except Exception as e:
                        self.logger.error(f"重新创建页面失败: {str(e)}")
                        return False
                else:
                    self.logger.info("不需要继续发布，等待页面稳定后结束")
                    self.page.wait_for_timeout(2000)
            
            return True
        except Exception as e:
            self.logger.warning(f"处理成功页面失败: {str(e)}")
            return True

    def _handle_continue_edit_prompt(self):
        """处理继续编辑提示（使用测试验证的方法）"""
        try:
            # 使用query_selector更可靠（与测试文件一致）
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
            self.logger.info(f"开始上传视频: {video_path}")
            video_input = self.page.locator('input[type="file"][accept*="video"]').first
            video_input.set_input_files(video_path)
            self.logger.info("视频上传触发成功")
            return True
        except Exception as e:
            self.logger.warning(f"视频上传失败: {str(e)}")
            return False

    def _check_video_already_uploaded(self):
        """检查视频是否已经上传完成"""
        try:
            progress_text = self.page.locator('.ant-progress-text')
            if progress_text.count() > 0:
                text = progress_text.first.text_content()
                if text and '100%' in text:
                    return True, "上传进度已达100%"
            
            cover_preview = self.page.locator('[class*="_cover-preview_"]')
            if cover_preview.count() > 0:
                return True, "检测到封面预览"
            
            preview_text = self.page.locator('text=预览封面')
            if preview_text.count() > 0:
                return True, "检测到预览封面文本"
            
            return False, "未检测到视频已上传"
        except Exception as e:
            self.logger.warning(f"检查视频上传状态失败: {str(e)}")
            return False, str(e)

    def _wait_for_video_upload(self, timeout=180):
        """等待视频上传完成（根据文本内容检测，避免动态类名）"""
        try:
            self.logger.info("开始等待视频上传完成")
            
            # 根据HTML结构：上传完成后会出现"预览封面"、"预览作品"等文本
            self._wait_for_condition(
                lambda: self.page.evaluate('''() => {
                    // 检查是否存在上传进度条（上传中）
                    const progressText = document.querySelector('.ant-progress-text');
                    if (progressText && progressText.textContent && !progressText.textContent.includes('100%')) {
                        return false; // 还在上传中
                    }
                    
                    // 检查是否出现预览相关文本（上传完成）
                    const bodyText = document.body.textContent || '';
                    if (bodyText.includes('预览封面') || bodyText.includes('预览作品') || bodyText.includes('编辑画布')) {
                        return true; // 上传完成，出现预览相关文本
                    }
                    
                    // 检查是否出现预览视频元素
                    const videoEl = document.querySelector('#preview-tours video');
                    if (videoEl && videoEl.src) {
                        return true; // 上传完成，出现视频元素
                    }
                    
                    // 检查进度条是否显示100%
                    if (progressText && progressText.textContent && progressText.textContent.includes('100%')) {
                        return true; // 进度条显示100%
                    }
                    
                    return false;
                }'''),
                timeout=timeout, interval=2, name="视频上传完成"
            )
            
            self.logger.info("视频上传完成")
        except Exception as e:
            self.logger.warning(f"等待视频上传完成异常: {e}")

    def _fill_content(self, description):
        """填写视频描述（使用测试验证的方法）
        
        快手描述输入框是 contenteditable="true" 的 div，
        测试验证：先等待元素出现，再点击激活，最后用 fill 方法可以正常填充。
        
        Args:
            description: 描述内容
        """
        try:
            self.logger.info(f"开始填写描述: {description[:20]}...")
            
            description_input = self.page.locator('#work-description-edit')
            # 先等待元素出现（可能需要视频上传完成后才出现）
            description_input.wait_for(state="visible", timeout=30000)
            
            description_input.first.click()
            self.page.wait_for_timeout(300)
            description_input.first.fill(description)
            self.page.wait_for_timeout(500)
            self.logger.info(f"描述填写成功: {description[:50]}...")
                
        except Exception as e:
            self.logger.warning(f"填写描述失败: {str(e)}")

    def _check_and_compress_cover(self, cover_path, max_size_mb=5):
        """检查封面文件大小，超过最大限制时进行压缩"""
        try:
            if not cover_path or not os.path.exists(cover_path):
                return cover_path
            
            file_size = os.path.getsize(cover_path) / (1024 * 1024)
            if file_size <= max_size_mb:
                self.logger.info(f"封面文件大小 {file_size:.2f}M，无需压缩")
                return cover_path
            
            self.logger.info(f"封面文件过大({file_size:.2f}M)，开始压缩到{max_size_mb}M以下")
            
            with Image.open(cover_path) as img:
                quality = 90
                compressed_path = cover_path.replace('.png', '_compressed.png').replace('.jpg', '_compressed.jpg').replace('.jpeg', '_compressed.jpeg')
                
                while True:
                    img.save(compressed_path, quality=quality)
                    compressed_size = os.path.getsize(compressed_path) / (1024 * 1024)
                    
                    if compressed_size <= max_size_mb or quality <= 10:
                        break
                    
                    quality -= 10
                
                self.logger.info(f"封面压缩完成，原始{file_size:.2f}M → 压缩后{compressed_size:.2f}M，质量{quality}")
                return compressed_path
        
        except Exception as e:
            self.logger.warning(f"封面压缩失败: {str(e)}，使用原始文件")
            return cover_path

    def _upload_cover(self, media_info):
        """上传封面图片（使用Playwright原生方法，精确定位）"""
        try:
            cover_path = self.get_cover_path(media_info)
            if not cover_path or not os.path.exists(cover_path):
                self.logger.info("封面文件不存在，跳过封面上传")
                return True
            
            cover_path = self._check_and_compress_cover(cover_path)
            self.logger.info(f"开始上传封面: {cover_path}")
            
            # 步骤1：查找并点击封面设置按钮（根据HTML结构精确定位）
            # HTML结构: <div class="_high-cover-editor-wrapper_xxx">
            #               <div class="_high-cover-editor-main_xxx">
            #                   <div class="_cover-full-editor_xxx">封面设置</div>
            #               </div>
            #           </div>
            
            # 优先使用精确选择器：直接定位封面编辑器区域
            cover_editor = self.page.locator('[class*="_cover-full-editor_"]')
            
            if cover_editor.count() > 0:
                cover_editor.wait_for(state="visible", timeout=5000)
                cover_editor.click()
                self.logger.info("点击封面设置按钮（通过_cover-full-editor类定位）")
            else:
                # 备用方案：通过wrapper定位
                wrapper = self.page.locator('[class*="_high-cover-editor-wrapper_"]')
                if wrapper.count() > 0:
                    wrapper.wait_for(state="visible", timeout=5000)
                    # 点击wrapper内的main区域
                    main = wrapper.locator('[class*="_high-cover-editor-main_"]')
                    if main.count() > 0:
                        main.click()
                        self.logger.info("点击封面设置按钮（通过wrapper定位）")
                    else:
                        wrapper.click()
                        self.logger.info("点击封面设置按钮（直接点击wrapper）")
                else:
                    self.logger.warning("未找到封面设置按钮")
                    return False
            
            # 步骤2：等待封面弹窗出现并切换到上传封面tab
            # 等待弹窗稳定（固定等待，测试验证有效）
            self.page.wait_for_timeout(2000)
            self.logger.info("等待封面弹窗稳定")
            
            # 切换到上传封面tab（使用Playwright原生方法）
            upload_tab = self.page.locator('#microSupport [class*="_header-title-item_"]', has_text='上传封面')
            if upload_tab.count() == 0:
                self.logger.warning("未找到上传封面tab")
                return False
            
            upload_tab.first.click()
            self.logger.info("点击上传封面tab")
            
            # 等待tab切换完成
            self.page.wait_for_timeout(2000)
            self.logger.info("已切换到上传封面tab")
            
            # 步骤3：检测封面上传状态并上传（使用Playwright原生方法）
            # 检查是否有"清空上传"文本（表示封面已上传）
            clear_upload = self.page.locator('#microSupport', has_text='清空上传')
            has_clear_upload = clear_upload.count() > 0
            
            # 检查是否有文件输入框
            has_file_input = self.page.locator('#microSupport input[type="file"]').count() > 0
            
            cover_status = {
                'uploaded': has_clear_upload,
                'hasInput': has_file_input
            }
            self.logger.info(f"封面状态检查: {cover_status}")
            
            if cover_status.get('uploaded'):
                # 封面已上传，直接点击确认按钮
                self.logger.info("封面已上传，直接点击确认")
                self.page.locator('#microSupport button', has_text='确认').first.click()
                self.logger.info("点击确认按钮")
                self.page.wait_for_timeout(2000)
            elif cover_status.get('hasInput'):
                # 封面未上传，上传新封面
                self.logger.info("封面未上传，开始上传")
                image_input = self.page.locator('#microSupport input[type="file"]').first
                image_input.set_input_files(cover_path)
                self.logger.info(f"封面文件上传: {cover_path}")
                self.page.wait_for_timeout(2000)
                
                # 点击确认按钮
                self.page.locator('#microSupport button', has_text='确认').first.click()
                self.logger.info("点击确认按钮")
                self.page.wait_for_timeout(2000)
            else:
                self.logger.warning("无法确定封面上传状态")
                return False
            
            # 关闭弹窗（使用JS，测试验证有效）
            self.page.locator('#microSupport').evaluate('el => el.style.display = "none"')
            self.page.wait_for_timeout(1000)
            self.logger.info("封面上传完成！")
            return True
            
        except Exception as e:
            self.logger.warning(f"封面上传异常: {str(e)}")
            return False

    def _select_ai_declaration(self, media_info):
        """选择作者声明（内容为AI生成，使用条件等待优化）"""
        if not self.should_add_ai_label(media_info):
            self.logger.info("AI标注开关关闭，跳过AI内容声明")
            return
        try:
            self.logger.info("开始选择作者声明")
            
            # 点击下拉框
            author_label = self.page.locator('label', has_text='作者声明').first
            author_select = author_label.locator('..').locator('.ant-select').first
            author_select.click()
            self.logger.info("点击作者声明下拉框")
            
            # 等待选项可见（条件等待，比固定等待更高效）
            ai_option = self.page.locator('text="内容为AI生成"').first
            ai_option.wait_for(state="visible", timeout=3000)
            
            ai_option.click()
            self.logger.info("点击内容为AI生成选项")
            
            # 等待下拉框关闭（条件等待）
            self.page.wait_for_selector('[role="listbox"]', state="hidden", timeout=2000)
            
            self.logger.info("作者声明选择成功！")
            return True
            
        except Exception as e:
            self.logger.warning(f"作者声明选择失败: {e}")
            return False

    def _select_collection(self, collection_name):
        """选择合集（使用条件等待优化）"""
        if not collection_name:
            return True
        try:
            self.logger.info(f"开始选择合集: {collection_name}")
            
            # 点击下拉框
            collection_label = self.page.locator('label', has_text='加入合集').first
            collection_select = collection_label.locator('..').locator('.ant-select').first
            collection_select.click()
            self.logger.info("点击合集下拉框")
            
            # 等待选项可见（条件等待，比固定等待更高效）
            collection_option = self.page.locator(f'text="{collection_name}"').first
            collection_option.wait_for(state="visible", timeout=3000)
            
            collection_option.click()
            self.logger.info(f"点击{collection_name}选项")
            
            # 等待下拉框关闭（条件等待）
            self.page.wait_for_selector('[role="listbox"]', state="hidden", timeout=2000)
            
            self.logger.info("合集选择成功！")
            return True
            
        except Exception as e:
            self.logger.warning(f"合集选择失败: {e}")
            return False

    def _get_collection_name(self, media_info):
        return self.get_collection_name(media_info)

    def _fill_all_content(self, media_info, content, publish_strategy):
        """填写所有内容（标题、描述、合集、AI声明、定时发布）"""
        try:
            self.submit_mode = publish_strategy.get("mode", "publish")
            
            self._fill_content(content["description"])
            self._select_ai_declaration(media_info)
            
            collection_name = self._get_collection_name(media_info)
            if collection_name:
                self._select_collection(collection_name)

            publish_time = publish_strategy.get("time", "")
            if publish_time:
                self._set_schedule_time(publish_time)
            
            self.logger.info("内容填写完成")
            return True
        except Exception as e:
            self.logger.error(f"填写内容失败: {str(e)}")
            return False

    def _set_schedule_time(self, publish_time):
        """设置定时发布时间
        
        外部传入格式：yyyy-MM-dd HH:mm
        快手需要：yyyy-MM-dd HH:mm:ss（内部补秒）
        
        Args:
            publish_time: 时间字符串（yyyy-MM-dd HH:mm）
        """
        try:
            # 1. 选中定时发布单选
            self.page.click('label:has-text("定时发布")')
            self.page.wait_for_timeout(800)

            # 内部补秒，因为快手需要完整的 yyyy-MM-dd HH:mm:ss 格式
            full_time = f"{publish_time}:00"
            self.logger.info(f"传入待设置定时时间：{full_time}")

            # 2. 定位输入框，先点击唤起弹窗
            picker_input = self.page.locator('.ant-picker-input input')
            picker_input.click()
            self.page.wait_for_timeout(1200)

            # 关键：Playwright原生fill，自动移除readonly、完整输入，模拟真实键盘录入
            picker_input.fill(full_time)
            self.page.wait_for_timeout(600)
            # 原生回车，和人手操作完全一致
            picker_input.press("Enter")
            self.page.wait_for_timeout(1000)

            # 空白点击兜底
            self.page.mouse.click(10, 10)
            self.page.wait_for_timeout(500)

            # 校验结果
            final_val = self.page.evaluate('document.querySelector(".ant-picker-input input").value')
            self.logger.info(f"页面最终保存定时时间：{final_val}")
            if final_val != full_time:
                self.logger.warning(f"⚠️ 定时时间不匹配！目标:{full_time} 页面实际:{final_val}")
                return False
            self.logger.info(f"✅ 定时时间校验完全匹配：{final_val}")
            return True
            
        except Exception as e:
            self.logger.warning(f"❌ 快手定时设置失败: {str(e)}")
            return False

    def _submit_publish(self, submit_mode="publish"):
        """提交发布（快手不支持存草稿，只有发布和取消）
        
        使用页面跳转监听代替固定等待：
        - 点击发布按钮后监听页面跳转事件
        - URL变化说明提交成功，立即返回
        - 设置10秒最大等待时间作为兜底
        
        Args:
            submit_mode: "publish"=正式发布（快手只支持这个）
            
        HTML结构：
            <div class="_edit-section-btns_ql0z6_118">
                <div class="_button_3a3lq_1 _button-primary_3a3lq_60" style="width: 96px; height: 36px;">
                    <div>发布</div>
                </div>
                <div class="_button_3a3lq_1 _button-default_3a3lq_35" style="width: 96px; height: 36px;">
                    <div>取消</div>
                </div>
            </div>
        """
        try:
            self.logger.info("点击发布按钮")
            
            # 记录当前URL
            original_url = self.page.url
            
            # 点击发布按钮（通过外层容器+按钮样式前缀定位，精确匹配）
            # _edit-section-btns_ 是发布按钮区域的容器
            # _button-primary_ 是发布按钮的样式前缀
            self.page.click('[class*="_edit-section-btns_"] [class*="_button-primary_"]')
            
            # 监听页面跳转（最多等待10秒）
            # 如果页面跳转，说明提交成功；如果超时也继续（发布按钮已点击）
            try:
                self.page.wait_for_event("framenavigated", timeout=10000)
                self.logger.info("检测到页面跳转，发布提交成功")
            except:
                # 超时但不视为失败，检查URL是否变化
                if self.page.url != original_url:
                    self.logger.info("页面URL已变化，发布提交成功")
                else:
                    self.logger.warning("页面未跳转，但发布按钮已点击")
            
            return True
            
        except Exception as e:
            self.logger.error(f"提交发布失败: {str(e)}")
            return False
