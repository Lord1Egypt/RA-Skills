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

class BilibiliPublisher(BasePublisher):
    """B站发布器 - 实现B站投稿平台发布流程
    
    专项规则：
    - 标题截取前80字符
    - AI创作声明固定「含AI生成内容」
    - 分区固定「亲子」
    - 标签：基础标签 + 内容类型补充标签，英文逗号拼接
    - 封面：成语故事用0_cover_350.png，古诗词用0_cover.png
    """
    
    PUBLISH_URL = "https://member.bilibili.com/platform/upload/video/frame?page_from=creative_home_top_upload"
    
    def __init__(self, page, browser_config):
        super().__init__(page, browser_config)
        self.submit_mode = "publish"
    
    def publish(self, media_info, content, publish_strategy):
        """发布视频到B站（参照快手执行顺序）
        
        执行顺序：
        1. 导航到发布页面
        2. 上传视频（后台进行，不等待完成）
        3. 填写标题
        4. 填写简介
        5. 选择分区
        6. 添加标签
        7. AI创作声明
        8. 定时发布
        9. 等待视频上传完成（封面需要等视频上传完）
        10. 上传封面（参照测试代码完整步骤）
        11. 提交发布
        """
        self.logger.info(f"开始发布B站：{media_info.get('name', '')}")
        
        self.submit_mode = publish_strategy.get('mode', 'publish')
        
        try:
            if not self._ensure_on_publish_page(self.PUBLISH_URL):
                return False, "导航失败"
            
            if not self._check_login_status():
                return False, "未登录"
            
            # 检查是否在发布成功页面，如果是则点击"再投一个"按钮
            self._handle_success_page()
            
            video_already_uploaded = self._handle_continue_edit_prompt()
            need_wait_video = False
            if not video_already_uploaded:
                if not self._upload_video(media_info["video_path"]):
                    return False, "视频上传失败"
                need_wait_video = True

            self._fill_title(content.get('title', ''))
            description = content.get('description', '')
            self._fill_description(description)
            self._select_category()
            self._add_tags(media_info.get('content_type', ''), description)
            self._select_ai_declaration(media_info)

            publish_time = publish_strategy.get("time", "")
            
            self.logger.info(f"publish_strategy: {publish_strategy}")
            self.logger.info(f"publish_time: {publish_time}")
            if publish_time:
                self._set_schedule_time(publish_time)

            if need_wait_video:
                self._wait_for_video_upload()

            self._upload_cover(media_info)

            if not self._submit_publish():
                return False, "发布提交失败"

            return True, "发布成功"
        except Exception as e:
            self.logger.error(f"B站发布异常: {str(e)}")
            import traceback
            traceback.print_exc()
            self._take_screenshot("bilibili_error")
            return False, str(e)
    
    def _ensure_on_publish_page(self, publish_url):
        """B站专用：多视频批量发布时确保拿到「干净」的发布页

        问题背景：
        - B站发布成功后 URL 不变（页面内容变为成功提示），且通过站内"投稿/再投一个"
          返回发布页时会丢掉 ?page_from=... 查询参数；
        - 若直接沿用上一视频成功页的过渡态，下一个视频的 set_input_files 会出现
          "触发了但上传没真正接管" → 后续 _wait_for_video_upload 干等 120s 超时、
          连环导致后续视频"无法导航到发布页面"。
        策略：只要不是「上传区存在 + 无成功提示 + 无残留上传项」的干净态，就硬导航到
        完整 PUBLISH_URL 并等待上传区就绪，强制拿到干净上传页。
        """
        try:
            try:
                current_url = self.page.url
            except Exception:
                return self._reconnect_page_and_navigate(publish_url)

            upload_area = self.page.locator('.upload-area')
            success_text = self.page.locator('text=稿件投递成功')
            stale_item = self.page.locator('.file-item-content')

            clean = (
                self._is_on_publish_url(current_url, publish_url)
                and upload_area.count() > 0
                and success_text.count() == 0
                and stale_item.count() == 0
            )
            if clean:
                self._wait_for_page_load()
                self.page.wait_for_timeout(1000)
                return True

            # 任意非干净态：硬导航到发布页，强制干净状态
            self.logger.info("B站：硬导航到发布页面以确保上传区干净（批量发布防卡死）")
            if not self._navigate(publish_url):
                return self._reconnect_page_and_navigate(publish_url)

            try:
                self.page.wait_for_selector('.upload-area', state='attached', timeout=30000)
            except Exception:
                self.logger.warning("B站：导航后未检测到上传区，仍继续")
            self._wait_for_page_load()
            self.page.wait_for_timeout(1500)
            return True
        except Exception as e:
            self.logger.warning(f"B站检测页面状态失败: {e}")
            return self._reconnect_page_and_navigate(publish_url)

    def _wait_upload_item_appear(self, timeout=15000):
        """上传后等待上传项元素出现，确认上传真正被前端接收

        避免"set_input_files 调用了但 B站 上传器没接管"导致的假触发，
        从而把失败提前暴露（快速失败），而不是干等 120s 后连环崩。
        """
        try:
            self.page.wait_for_selector('.file-item-content', state='attached', timeout=timeout)
            self.logger.info("检测到上传项，上传已真正触发")
            return True
        except Exception:
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
    
    def _wait_for_publish_success(self):
        """等待B站发布成功
        
        B站发布成功后：
        1. 页面显示"稿件投递成功"文字
        2. 出现"再投一个"按钮
        """
        try:
            self.logger.info("等待B站发布成功...")
            
            try:
                self.page.wait_for_selector(
                    'text=稿件投递成功',
                    state="visible",
                    timeout=30000,
                )
                self.logger.info("检测到B站发布成功提示：稿件投递成功")
                return True, "B站发布成功"
            except Exception as e:
                self.logger.warning(f"等待发布成功超时: {e}")
                return True, "B站发布成功（超时）"
        except Exception as e:
            self.logger.error(f"等待B站发布成功失败: {str(e)}")
            return True, "B站发布成功（异常）"
    
    def _handle_success_page(self, continue_publish=False):
        """处理发布成功页面
        
        判断发布成功的关键：检测页面是否显示"稿件投递成功"提示
        
        B站特殊：发布成功后URL不变，页面内容变为成功提示页面
        
        Args:
            continue_publish: 是否需要继续发布下一个视频
                              True: 需要返回发布页面（批量发布时）
                              False: 不需要返回发布页面（单个视频发布时，只等待页面跳转完成）
        
        注意：使用 load 状态而非 networkidle，因为页面有轮询请求会导致 networkidle 永远不会到来
        
        可用的返回发布页面方式（按优先级）：
        1. 页面上的"再投一个"按钮
        2. 导航栏的"投稿"按钮（id="nav_upload_btn"）
        3. 直接导航到发布页面URL
        """
        try:
            # B站发布成功后页面不会自动跳转，需要检测成功提示
            success_text = self.page.locator('text=稿件投递成功')
            if success_text.count() > 0:
                self.logger.info("检测到发布成功页面（稿件投递成功）")
                
                # 等待页面基本加载完成（使用 load 状态，比 networkidle 更可靠）
                try:
                    self.page.wait_for_load_state("load", timeout=10000)
                except:
                    self.logger.info("页面加载状态等待超时，继续执行")
                
                self.page.wait_for_timeout(1000)
                
                # 如果需要继续发布，才执行跳转操作
                if continue_publish:
                    self.logger.info("需要继续发布，准备返回发布页面")
                    
                    # 方案1：导航栏的"投稿"按钮（优先使用，ID选择器最稳定）
                    # <div class="nav-upload-btn newApp"><a href="/platform/upload?page_from=creative_home_top_upload" class="active" id="nav_upload_btn"><i class="bcc-iconfont bcc-icon-ic_contribute"></i>投稿</a></div>
                    # 注意：id="nav_upload_btn" 在 <a> 标签上，不是在 <div> 上，所以使用 a#nav_upload_btn
                    nav_upload_btn = self.page.locator('#nav_upload_btn')
                    self.logger.info(f"查找导航栏投稿按钮(#nav_upload_btn): {nav_upload_btn.count()}")
                    
                    if nav_upload_btn.count() == 0:
                        nav_upload_btn = self.page.locator('.nav-upload-btn a')
                        self.logger.info(f"查找导航栏投稿按钮(.nav-upload-btn a): {nav_upload_btn.count()}")
                    
                    if nav_upload_btn.count() == 0:
                        nav_upload_btn = self.page.locator('a:has-text("投稿")')
                        self.logger.info(f"查找导航栏投稿按钮(a:has-text): {nav_upload_btn.count()}")
                    
                    if nav_upload_btn.count() > 0:
                        nav_upload_btn.first.click()
                        self.logger.info("已点击导航栏投稿按钮")
                        try:
                            self.page.wait_for_load_state("load", timeout=10000)
                        except:
                            pass
                        self.page.wait_for_timeout(3000)
                        
                        # 验证页面是否真正跳转到了发布页面
                        # 检查是否有标题输入框，如果没有说明跳转失败
                        title_input = self.page.locator('input.video-title-input')
                        if title_input.count() == 0:
                            self.logger.warning("点击导航栏按钮后页面未真正跳转，尝试兜底方案")
                        else:
                            self.logger.info("点击导航栏按钮成功跳转到发布页面")
                            return True
                    
                    # 方案2：页面上的"再投一个"按钮（备选方案，文本选择器可能会变）
                    retry_btn = self.page.locator('button.bcc-button.group-2-btn:has-text("再投一个")')
                    self.logger.info(f"查找再投一个按钮(精确): {retry_btn.count()}")
                    
                    if retry_btn.count() == 0:
                        retry_btn = self.page.locator('button:has-text("再投一个")')
                        self.logger.info(f"查找再投一个按钮(button): {retry_btn.count()}")
                    
                    if retry_btn.count() == 0:
                        retry_btn = self.page.locator('div:has-text("再投一个")')
                        self.logger.info(f"查找再投一个按钮(div): {retry_btn.count()}")
                    
                    if retry_btn.count() > 0:
                        retry_btn.first.click()
                        self.logger.info("已点击再投一个按钮")
                        try:
                            self.page.wait_for_load_state("load", timeout=10000)
                        except:
                            pass
                        self.page.wait_for_timeout(2000)
                        return True
                    
                    # 方案3：关闭当前页面并重新创建（兜底方案，最可靠）
                    self.logger.warning("未找到投稿按钮，关闭当前页面并重新创建")
                    try:
                        from browser.browser_singleton import get_platform_page
                        self.page = get_platform_page("B站", force_new=True)
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
            self.logger.warning(f"处理成功页面失败: {e}")
            # 如果需要继续发布，尝试直接导航
            if continue_publish:
                try:
                    self._navigate(self.PUBLISH_URL)
                except:
                    pass
            return True
    
    def _upload_video(self, video_path):
        """上传视频文件（参照测试代码精确选择器）
        
        注意：上传区域可能是hidden状态，但input元素仍然可以操作，所以使用attached而非visible
        """
        try:
            self.logger.info(f"开始上传视频: {video_path}")
            
            self.page.bring_to_front()
            # 使用attached而非visible，因为上传区域可能是hidden状态
            self.page.wait_for_selector(".upload-area", state="attached", timeout=30000)
            self.logger.info("页面加载完成")
            
            file_input = self.page.locator('.bcc-upload.upload input[accept*=".mp4"][multiple="multiple"]')
            self.logger.info(f"视频上传input数量:{file_input.count()}")
            
            if file_input.count() > 0:
                file_input.wait_for(state="attached", timeout=10000)
                file_input.first.set_input_files(video_path)
                self.logger.info("视频上传触发成功")
                if self._wait_upload_item_appear():
                    return True
                self.logger.warning("上传项未出现，上传可能未真正触发")
                return False
            
            file_input = self.page.locator('input[type="file"][accept*="video"]')
            if file_input.count() > 0:
                file_input.first.set_input_files(video_path)
                self.logger.info("视频上传触发成功（备选选择器）")
                if self._wait_upload_item_appear():
                    return True
                self.logger.warning("上传项未出现，上传可能未真正触发（备选选择器）")
                return False
            
            self.logger.warning("未找到视频上传input元素")
            return False
        except Exception as e:
            self.logger.warning(f"视频上传失败: {str(e)}")
            return False
    
    def _check_video_already_uploaded(self):
        """检查视频是否已经上传完成
        
        B站特殊：视频上传完成后会显示标题输入框
        """
        try:
            title_input = self.page.locator('input#video-title-input')
            if title_input.count() > 0:
                return True, "检测到标题输入框，视频已上传完成"
            
            success_text = self.page.locator(".file-item-content-status-text:has(.success)")
            if success_text.count() > 0:
                return True, "检测到上传成功状态"
            
            video_title = self.page.locator('.file-item-content-title')
            if video_title.count() > 0:
                return True, "检测到视频标题"
            
            return False, "未检测到视频已上传"
        except Exception as e:
            self.logger.warning(f"检查视频上传状态失败: {str(e)}")
            return False, str(e)

    def _wait_for_video_upload(self):
        """等待视频上传完成"""
        try:
            self.page.bring_to_front()
            self.logger.info("开始等待视频上传完成")
            
            self.page.wait_for_selector(
                ".file-item-content-status-text:has(.success)",
                state="visible",
                timeout=120000,
            )
            self.logger.info("视频上传完成")
            return True
        except Exception as e:
            self.logger.warning(f"等待视频上传超时: {e}")
            return True
    
    def _fill_title(self, title):
        """填写标题（优先判断长度）"""
        try:
            if not title:
                return True
            
            # B站标题限制为80个字符
            max_len = 80
            if len(title) <= max_len:
                trim_title = title
            else:
                trim_title = self.trim_title(title, max_len)
            
            title_input = self.page.locator('input[placeholder="请输入稿件标题"]')
            self.logger.info(f"title_input数量:{title_input.count()}")
            if title_input.count() > 0:
                title_input.wait_for(state="visible", timeout=10000)
                title_input.fill(trim_title)
                self.logger.info(f"标题填写成功: {trim_title}")
                return True
            
            self.logger.warning("未找到标题输入框")
            return False
        except Exception as e:
            self.logger.warning(f"填写标题失败: {str(e)}")
            return False
    
    def _fill_description(self, description):
        """填写简介"""
        try:
            if not description:
                return True
            
            desc_editor = self.page.locator(".desc-text-wrp .ql-editor")
            self.logger.info(f"desc_editor数量:{desc_editor.count()}")
            if desc_editor.count() > 0:
                desc_editor.first.wait_for(state="visible", timeout=10000)
                desc_editor.first.click()
                desc_editor.first.type(description)
                self.logger.info(f"简介填写成功: {description[:50]}...")
            return True
        except Exception as e:
            self.logger.warning(f"填写简介失败: {str(e)}")
            return False
    
    def _select_category(self):
        """选择分区 - 固定选择「亲子」"""
        try:
            section_button = self.page.locator(".select-controller")
            self.logger.info(f"section_button数量:{section_button.count()}")
            if section_button.count() > 0:
                section_button.wait_for(state="visible", timeout=10000)
                section_button.click()

                self.page.wait_for_selector(
                    ".drop-list-v2-container", state="visible", timeout=5000
                )

                section_item = self.page.locator('.drop-list-v2-item:has-text("亲子")')
                if section_item.count() > 0:
                    section_item.click()
                    self.logger.info("分区选择成功（亲子）")
                    return True
            return False
        except Exception as e:
            self.logger.warning(f"选择分区失败: {str(e)}")
            return False
    
    def _add_tags(self, content_type, description=''):
        """添加标签（包含视频类型标签和描述中的#标签）"""
        try:
            existing_tags = []
            tag_items = self.page.locator(".tag-pre-wrp .label-item-v2-container")
            for i in range(tag_items.count()):
                tag_text = (
                    tag_items.nth(i).locator(".label-item-v2-content").text_content()
                )
                if tag_text:
                    existing_tags.append(tag_text.strip())
            self.logger.info(f"现有标签: {existing_tags}")

            tag_input = self.page.locator('input[placeholder="按回车键Enter创建标签"]')
            if tag_input.count() > 0:
                tag_input.first.wait_for(state="visible", timeout=10000)
                tag_input.first.click()
                self.page.wait_for_timeout(300)
                
                if content_type == 'poem':
                    tags_to_add = ['古诗词', '诗词']
                    tags_to_remove = ['成语故事', '成语']
                elif content_type == 'idiom':
                    tags_to_add = ['成语故事', '成语']
                    tags_to_remove = ['古诗词', '诗词']
                else:
                    tags_to_add = ['成语']
                    tags_to_remove = []
                
                # 删除不适合当前内容类型的标签
                for tag_to_remove in tags_to_remove:
                    if tag_to_remove in existing_tags:
                        self.logger.info(f"尝试删除标签: {tag_to_remove}")
                        try:
                            remove_tag_item = tag_items.filter(has_text=tag_to_remove)
                            self.logger.info(f"filter方式查找标签 {tag_to_remove}: {remove_tag_item.count()} 个")
                            
                            if remove_tag_item.count() > 0:
                                close_btn = remove_tag_item.locator(".label-item-v2-close")
                                self.logger.info(f"关闭按钮数量: {close_btn.count()}")
                                if close_btn.count() > 0:
                                    close_btn.first.click()
                                    self.page.wait_for_timeout(300)
                                    self.logger.info(f"标签删除成功: {tag_to_remove}")
                                else:
                                    self.logger.warning(f"未找到关闭按钮，尝试点击标签文字区域")
                                    remove_tag_item.first.click()
                                    self.page.wait_for_timeout(300)
                            else:
                                self.logger.info(f"filter方式未找到标签，尝试重新定位")
                                all_tag_items = self.page.locator(".tag-pre-wrp .label-item-v2-container")
                                for i in range(all_tag_items.count()):
                                    item_text = all_tag_items.nth(i).locator(".label-item-v2-content").text_content()
                                    if item_text and tag_to_remove in item_text:
                                        close_btn = all_tag_items.nth(i).locator(".label-item-v2-close")
                                        if close_btn.count() > 0:
                                            close_btn.click()
                                            self.page.wait_for_timeout(300)
                                            self.logger.info(f"标签删除成功(逐个查找): {tag_to_remove}")
                                            break
                                        else:
                                            self.logger.warning(f"找到标签但未找到关闭按钮")
                        except Exception as e:
                            self.logger.warning(f"删除标签 {tag_to_remove} 失败: {str(e)}")
                
                # 从描述中提取#标签
                if description:
                    import re
                    hash_tags = re.findall(r'#(\S+)', description)
                    if hash_tags:
                        self.logger.info(f"从描述中提取的标签: {hash_tags}")
                        tags_to_add.extend(hash_tags)
                
                # 去重
                tags_to_add = list(dict.fromkeys(tags_to_add))
                
                for tag in tags_to_add:
                    if tag not in existing_tags:
                        tag_input.first.fill(tag)
                        self.page.wait_for_timeout(200)
                        self.page.keyboard.press("Enter")
                        self.page.wait_for_timeout(500)
                        self.logger.info(f"标签添加成功: {tag}")
                    else:
                        self.logger.info(f"标签已存在，跳过: {tag}")
            
            return True
        except Exception as e:
            self.logger.warning(f"添加标签失败: {str(e)}")
            return False
    
    def _select_ai_declaration(self, media_info):
        """选择创作声明"""
        if not self.should_add_ai_label(media_info):
            self.logger.info("AI标注开关关闭，跳过AI内容声明")
            return
        try:
            ai_select = self.page.locator(".creation-statement-container .bcc-select")
            self.logger.info(f"ai_select数量:{ai_select.count()}")
            if ai_select.count() > 0:
                ai_select.wait_for(state="visible", timeout=10000)
                ai_select.click()

                self.page.wait_for_selector(
                    ".bcc-select-list-wrap", state="visible", timeout=5000
                )

                ai_option = self.page.locator(
                    '.bcc-select-option-list li.bcc-option:has-text("含AI生成内容")'
                )
                if ai_option.count() > 0:
                    ai_option.click()
                    self.logger.info("创作声明选择成功（含AI生成内容）")
                    return True
            return False
        except Exception as e:
            self.logger.warning(f"选择创作声明失败: {str(e)}")
            return False
    
    def _set_schedule_time(self, schedule_time):
        """设置定时发布时间"""
        try:
            self.logger.info(f"开始设置定时发布时间: {schedule_time}")
            
            target_date = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M")
            self.logger.info(f"格式化后的时间: {target_date}")
            
            schedule_switch = self.page.locator(".time-container .switch-container")
            self.logger.info(f"schedule_switch数量:{schedule_switch.count()}")
            if schedule_switch.count() > 0:
                schedule_switch.first.wait_for(state="visible", timeout=10000)

                is_active = schedule_switch.first.get_attribute("class")
                self.logger.info(f"定时发布开关class: {is_active}")
                
                if not is_active or "switch-container-active" not in is_active:
                    schedule_switch.first.click()
                    self.logger.info("定时发布开关已开启")

                self.page.wait_for_selector(".time-picker", state="visible", timeout=5000)

                date_picker = self.page.locator(".date-picker-date-wrp > .date-picker-date")
                if date_picker.count() > 0:
                    date_picker.first.click()
                    self.logger.info("已点击日期选择器")

                    date_container = self.page.locator(".date-picker-container")
                    date_container.first.wait_for(state="visible", timeout=5000)
                    self.logger.info("日期选择器弹窗已出现")

                    target_month = target_date.month
                    target_year = target_date.year
                    max_attempts = 12
                    attempt = 0
                    
                    while attempt < max_attempts:
                        nav_title = self.page.locator(
                            ".date-picker-nav-title"
                        ).text_content()
                        self.logger.info(f"当前导航标题: {nav_title}")

                        if (
                            str(target_year) in nav_title
                            and str(target_month) in nav_title
                        ):
                            break

                        next_month_btn = self.page.locator(".next-btn-month")
                        if next_month_btn.count() > 0:
                            next_month_btn.first.click()
                            self.page.wait_for_timeout(300)
                        attempt += 1

                    if attempt >= max_attempts:
                        self.logger.warning("切换月份失败")

                    day_str = str(target_date.day)
                    date_item = self.page.locator(
                        f'.date-picker-body-wrp .date-picker-body-item:text-is("{day_str}")'
                    )
                    if date_item.count() > 0:
                        date_item.first.click()
                        self.logger.info(
                            f"日期选择成功: {target_date.strftime('%Y-%m-%d')}"
                        )

                    date_show = self.page.locator(
                        ".date-picker-date > p.date-show"
                    ).text_content()
                    self.logger.info(f"日期显示: {date_show}")

                time_picker = self.page.locator(".date-picker-date-wrp > .date-picker-timer")
                if time_picker.count() > 0:
                    time_picker.first.click()
                    self.logger.info("已点击时间选择器")

                    time_container = self.page.locator(".time-picker-container")
                    time_container.first.wait_for(state="visible", timeout=5000)
                    self.logger.info("时间选择器弹窗已出现")

                    hour_str = str(target_date.hour).zfill(2)
                    minute_str = str(target_date.minute).zfill(2)
                    self.logger.info(f"预设的时间:{hour_str}:{minute_str}")
                    
                    time_item = self.page.locator(".time-picker-body-wrp > .time-picker-panel-select-wrp")
                    self.logger.info(f"选择列表数量:{time_item.count()}")
                    
                    if time_item.count() == 2:
                        hour_item = time_item.first.locator(f'.time-picker-panel-select-item:text-is("{hour_str}")')
                        hour_item.click()
                        self.logger.info(f"选择小时成功: {hour_str}")
                        
                        minute_item = time_item.last.locator(f'.time-picker-panel-select-item:text-is("{minute_str}")')
                        minute_item.click()
                        self.logger.info(f"选择分钟成功: {minute_str}")
                        
                        self.page.click('.time-container', position={'x': 0, 'y': 0})
                        self.page.wait_for_timeout(500)
                        self.logger.info("已点击空白处关闭时间选择器")

                    time_show = self.page.locator(
                        ".date-picker-timer > p.date-show"
                    ).text_content()
                    self.logger.info(f"时间显示: {time_show}")

            self.logger.info(
                f"定时发布时间设置成功: {target_date.strftime('%Y-%m-%d %H:%M')}"
            )
            return True
        except Exception as e:
            self.logger.warning(f"设置定时发布失败: {str(e)}")
            return False
    
    def _upload_cover(self, media_info):
        """上传封面（参照测试代码完整步骤）"""
        try:
            cover_path = self.get_cover_path(media_info)
            
            if not cover_path or not os.path.exists(cover_path):
                self.logger.info("封面文件不存在，跳过封面上传")
                return True
            
            self.logger.info(f"开始上传封面: {cover_path}")
            
            cover_btn = self.page.locator(".cover-img .edit-text")
            self.logger.info(f"封面设置按钮数量:{cover_btn.count()}")
            if cover_btn.count() > 0:
                cover_btn.first.wait_for(state="visible", timeout=10000)
                cover_btn.first.click()
                self.logger.info("已点击封面设置按钮")
                
                self.page.wait_for_selector(".cover-upload", state="visible", timeout=10000)
                self.logger.info("封面上传区域已出现")

            cover_input = self.page.locator('input[accept="image/png, image/jpeg"]')
            self.logger.info(f"封面上传input数量:{cover_input.count()}")

            if cover_input.count() > 0:
                cover_input.first.set_input_files(cover_path)
                self.logger.info(f"封面文件上传: {cover_path}")
            else:
                upload_btn = self.page.locator(".cover-upload .upload-text")
                if upload_btn.count() > 0:
                    with self.page.expect_file_chooser() as fc_info:
                        upload_btn.first.click()
                        file_chooser = fc_info.value
                        file_chooser.set_files(cover_path)
                    self.logger.info(
                        f"封面文件上传（文件选择器方式）: {cover_path}"
                    )

            self.page.wait_for_selector(
                ".cover-upload .upload-area.has-image",
                state="visible",
                timeout=30000,
            )
            self.logger.info("封面上传完成（has-image类已出现）")

            sync_checkbox = self.page.locator(
                '.sync.ratio_4_3 .bcc-checkbox-checkbox input[type="checkbox"]'
            )
            if sync_checkbox.count() > 0:
                is_checked = sync_checkbox.first.is_checked()
                if not is_checked:
                    sync_checkbox.first.click()
                    self.logger.info("已勾选双比例同步改动")
                else:
                    self.logger.info("双比例同步改动已勾选")

            finish_btn = self.page.locator(
                '.cover-editor-button .button.submit:has-text("完成")'
            )
            self.logger.info(f"完成按钮数量:{finish_btn.count()}")
            
            if finish_btn.count() == 0:
                # 备选：查找"下一步"按钮
                finish_btn = self.page.locator('.cover-editor-button .button.submit:has-text("下一步")')
                self.logger.info(f"下一步按钮数量:{finish_btn.count()}")
            
            if finish_btn.count() == 0:
                # 备选：使用更宽泛的选择器
                finish_btn = self.page.locator('.cover-editor-button .button.submit')
                self.logger.info(f"submit按钮数量:{finish_btn.count()}")
            
            if finish_btn.count() > 0:
                finish_btn.first.wait_for(state="visible", timeout=5000)
                finish_btn.first.click()
                self.logger.info("已点击完成/下一步按钮，封面上传完成")
            else:
                self.logger.warning("未找到完成或下一步按钮")
            
            return True
        except Exception as e:
            self.logger.warning(f"上传封面失败: {str(e)}")
            return True
    
    def _submit_publish(self):
        """提交发布（只负责点击发布按钮，不处理成功后的跳转）"""
        try:
            publish_button = self.page.locator(".submit-add")
            if publish_button.count() > 0:
                publish_button.first.scroll_into_view_if_needed()
                publish_button.first.wait_for(state="visible", timeout=5000)
                
                if self.submit_mode == 'draft':
                    draft_btn = self.page.locator('.submit-container .submit-draft')
                    if draft_btn.count() > 0:
                        draft_btn.first.click()
                        self.logger.info("已点击存草稿")
                        return True
                else:
                    publish_button.first.click()
                    self.logger.info("已点击立即投稿")
                    return True
            
            self.logger.warning("未找到发布按钮")
            return False
        except Exception as e:
            self.logger.warning(f"提交发布失败: {str(e)}")
            return False

    def _fill_all_content(self, media_info, content, publish_strategy):
        """填写所有内容（标题、描述、分区、标签、AI声明、定时发布）
        
        B站流程：上传视频后立即填写内容（不等待上传完成），
        封面需要等视频上传完，在阶段3处理。
        """
        try:
            self.submit_mode = publish_strategy.get('mode', 'publish')
            
            self.page.bring_to_front()
            self.logger.info("开始填写内容（不等待视频上传完成）...")
            
            self._fill_title(content.get('title', ''))
            description = content.get('description', '')
            self._fill_description(description)
            self._select_category()
            self._add_tags(media_info.get('content_type', ''), description)
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
    return BilibiliPublisher(page, browser_config)