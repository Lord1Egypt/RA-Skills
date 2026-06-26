"""
视频自动发布脚本
支持平台：抖音、快手、B站、小红书
使用 Playwright 实现浏览器自动化
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# 设置标准输出编码为 UTF-8，避免 Windows 控制台编码错误
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 配置
BASE_DIR = Path(__file__).parent
COOKIES_DIR = BASE_DIR / "cookies"
COOKIES_DIR.mkdir(exist_ok=True)

# 平台配置
PLATFORMS = {
    "douyin": {
        "name": "抖音",
        "url": "https://creator.douyin.com/creator-micro/content/upload?enter_from=dou_web",
        "cookies_file": COOKIES_DIR / "douyin_cookies.json"
    },
    "kuaishou": {
        "name": "快手",
        "url": "https://cp.kuaishou.com/article/publish/video?origin=www.kuaishou.com&source=NewReco",
        "cookies_file": COOKIES_DIR / "kuaishou_cookies.json"
    },
    "bilibili": {
        "name": "B站",
        "url": "https://member.bilibili.com/platform/upload/video/frame",
        "cookies_file": COOKIES_DIR / "bilibili_cookies.json"
    },
    "xiaohongshu": {
        "name": "小红书",
        "url": "https://creator.xiaohongshu.com/publish/publish?source=official",
        "cookies_file": COOKIES_DIR / "xiaohongshu_cookies.json"
    }
}


class VideoPublisher:
    def __init__(self, platform, headless=False):
        self.platform = platform
        self.config = PLATFORMS[platform]
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()

        # 加载 cookies
        if self.config["cookies_file"].exists():
            with open(self.config["cookies_file"], 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                self.context.add_cookies(cookies)
                print(f"已加载 {self.config['name']} 的 cookies")

        self.page = self.context.new_page()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def save_cookies(self):
        """保存当前 cookies"""
        cookies = self.context.cookies()
        with open(self.config["cookies_file"], 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print(f"已保存 {self.config['name']} 的 cookies")

    def login_manual(self):
        """手动登录并保存 cookies"""
        print(f"\n请在浏览器中登录 {self.config['name']}")
        print(f"URL: {self.config['url']}")
        self.page.goto(self.config['url'])

        print("\n等待登录完成...")
        print("登录完成后，请在终端按 Enter 键继续...")
        input()

        self.save_cookies()
        print("登录成功！")

    def publish_douyin(self, video_path, title, description, tags):
        """发布到抖音"""
        print(f"\n开始发布到抖音: {video_path}")

        try:
            self.page.goto(self.config['url'], timeout=30000)
            time.sleep(3)

            # 检查是否需要登录
            if "login" in self.page.url.lower() or self.page.locator("text=登录").count() > 0:
                print("❌ 需要登录，请先运行登录流程保存 cookies")
                return False

            # 上传视频
            print("正在上传视频...")
            upload_input = self.page.locator('input[type="file"]').first
            upload_input.set_input_files(str(video_path))

            # 等待上传完成 - 检查上传进度
            print("等待视频上传...")
            max_wait = 120  # 最多等待2分钟
            for i in range(max_wait):
                time.sleep(1)
                # 检查是否有上传完成的标志
                if self.page.locator('text=上传成功').count() > 0 or \
                   self.page.locator('text=处理完成').count() > 0:
                    print("✓ 视频上传完成")
                    break
                if i % 10 == 0:
                    print(f"  上传中... {i}秒")

            time.sleep(2)

            # 填写标题
            print("填写标题...")
            title_input = self.page.locator('input[placeholder*="标题"], input[placeholder*="作品标题"]').first
            title_input.fill(title)
            time.sleep(1)

            # 填写描述
            print("填写描述...")
            desc_input = self.page.locator('textarea, div[contenteditable="true"]').first
            desc_input.fill(description)
            time.sleep(1)

            # 添加话题标签
            if tags:
                print("添加标签...")
                for tag in tags[:3]:  # 限制标签数量
                    desc_input.type(f" #{tag}")
                    time.sleep(0.5)

            # 自动点击发布按钮
            print("正在点击发布按钮...")

            # 查找所有包含"发布"的按钮，但排除"高清发布"等入口按钮
            clicked = False
            all_publish_buttons = self.page.locator('button:has-text("发布")')
            button_count = all_publish_buttons.count()

            print(f"找到 {button_count} 个包含'发布'的按钮")

            # 遍历所有按钮，找到纯"发布"按钮（排除"高清发布"、"定时发布"等）
            for i in range(button_count):
                try:
                    btn = all_publish_buttons.nth(i)
                    btn_text = btn.inner_text(timeout=1000).strip()

                    print(f"  检查按钮 {i+1}: '{btn_text}'")

                    # 排除不是真正发布的按钮
                    if btn_text in ['高清发布', '定时发布', '草稿发布']:
                        print(f"    ❌ 跳过（入口按钮）")
                        continue

                    # 只点击纯"发布"或"立即发布"
                    if btn_text in ['发布', '立即发布', '确认发布']:
                        if btn.is_visible() and btn.is_enabled():
                            btn.click(timeout=5000)
                            print(f"    ✓ 已点击发布按钮: '{btn_text}'")
                            clicked = True
                            break
                        else:
                            print(f"    ⚠️  按钮不可点击")
                except Exception as e:
                    print(f"    ❌ 检查失败: {e}")
                    continue

            if not clicked:
                print("❌ 未找到可点击的发布按钮")
                self.page.screenshot(path=str(BASE_DIR / "douyin_publish_error.png"))
                return False

            # 等待可能的弹窗或二次确认
            print("等待页面响应...")
            time.sleep(3)

            # 处理可能的二次确认弹窗
            print("检查是否有二次确认弹窗...")
            confirm_selectors = [
                'button:has-text("确认")',
                'button:has-text("确定")',
                'button:has-text("确认发布")',
                'button:has-text("继续发布")',
                '.modal button:has-text("发布")',
                '[class*="modal"] button:has-text("确认")'
            ]

            for selector in confirm_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        button = self.page.locator(selector).first
                        if button.is_visible():
                            button.click(timeout=3000)
                            print(f"✓ 已点击二次确认按钮 (选择器: {selector})")
                            time.sleep(2)
                            break
                except Exception as e:
                    continue

            # 处理"是否继续编辑"弹窗 - 选择"不编辑/放弃"
            print("检查是否有草稿提示...")
            abandon_selectors = [
                'button:has-text("放弃")',
                'button:has-text("不编辑")',
                'button:has-text("取消")',
                'button:has-text("关闭")'
            ]

            # 先检查是否有"继续编辑"的提示
            if self.page.locator('text=继续编辑').count() > 0 or \
               self.page.locator('text=未发布').count() > 0:
                print("⚠️  检测到草稿提示，说明视频未真正发布")
                self.page.screenshot(path=str(BASE_DIR / "douyin_draft_warning.png"))

                # 尝试找到真正的发布按钮
                print("尝试重新查找发布按钮...")
                retry_selectors = [
                    'button:has-text("发布")',
                    'button:has-text("确认发布")',
                    'button:has-text("立即发布")'
                ]

                for selector in retry_selectors:
                    try:
                        buttons = self.page.locator(selector)
                        for i in range(buttons.count()):
                            btn = buttons.nth(i)
                            if btn.is_visible() and btn.is_enabled():
                                btn.click(timeout=3000)
                                print(f"✓ 已重新点击发布按钮")
                                time.sleep(3)
                                break
                    except:
                        continue

            # 等待发布完成
            print("等待发布完成...")
            time.sleep(5)

            # 检查发布结果
            success_indicators = ['发布成功', '发布中', '审核中', '等待审核']
            found_success = False
            for indicator in success_indicators:
                if self.page.locator(f'text={indicator}').count() > 0:
                    print(f"✅ 检测到: {indicator}")
                    found_success = True
                    break

            # 如果已经检测到成功标志，直接返回成功
            if found_success:
                return True

            # 检查是否还在编辑页面（说明没发布成功）
            if self.page.locator('text=继续编辑').count() > 0 or \
               self.page.locator('text=未发布').count() > 0 or \
               self.page.locator('input[placeholder*="标题"]').count() > 0:
                print("❌ 视频未成功发布，仍在编辑页面")
                self.page.screenshot(path=str(BASE_DIR / "douyin_still_editing.png"))
                return False

            # 如果没有明确的成功标志，也没有编辑页面标志，保存截图供检查
            print("⚠️  未检测到明确的成功或失败标志")
            self.page.screenshot(path=str(BASE_DIR / "douyin_uncertain.png"))
            return False

        except Exception as e:
            print(f"❌ 发布失败: {e}")
            self.page.screenshot(path=str(BASE_DIR / "douyin_error.png"))
            return False

    def publish_kuaishou(self, video_path, title, description, tags):
        """发布到快手"""
        print(f"\n开始发布到快手: {video_path}")

        try:
            self.page.goto(self.config['url'], timeout=30000)
            time.sleep(3)

            # 检查是否需要登录（通过检测上传控件）
            upload_check = self.page.locator('input[type="file"]').count()
            if upload_check == 0:
                # 等待页面加载
                time.sleep(2)
                upload_check = self.page.locator('input[type="file"]').count()

            if upload_check == 0:
                print("❌ 需要登录，请先运行登录流程保存 cookies")
                return False

            # 上传视频
            print("正在上传视频...")
            upload_input = self.page.locator('input[type="file"]').first
            upload_input.set_input_files(str(video_path))

            # 等待上传完成
            print("等待视频上传...")
            max_wait = 120
            for i in range(max_wait):
                time.sleep(1)
                if self.page.locator('text=上传成功').count() > 0 or \
                   self.page.locator('text=处理完成').count() > 0:
                    print("✓ 视频上传完成")
                    break
                if i % 10 == 0:
                    print(f"  上传中... {i}秒")

            time.sleep(2)

            # 处理新手引导弹窗（上传后立即出现）
            print("检查并关闭新手引导弹窗...")
            time.sleep(3)  # 增加等待时间

            # 方法1：尝试点击 X 关闭按钮（最快）
            close_selectors = [
                'svg[class*="close"]',
                'button[class*="close"]',
                '[class*="close-btn"]',
                '[aria-label*="关闭"]',
                '[aria-label*="close"]'
            ]

            closed = False
            for selector in close_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        elem = self.page.locator(selector).first
                        if elem.is_visible():
                            elem.click(timeout=3000)
                            print(f"✓ 已点击关闭按钮")
                            closed = True
                            time.sleep(2)
                            break
                except:
                    continue

            # 方法2：如果没有 X，点击"下一步"和"立即体验"
            if not closed:
                print("尝试通过引导流程...")
                # 点击3次"下一步"
                for i in range(3):
                    try:
                        next_btn = self.page.locator('button:has-text("下一步")')
                        if next_btn.count() > 0 and next_btn.first.is_visible():
                            next_btn.first.click(timeout=3000)
                            print(f"✓ 已点击第 {i+1} 次下一步")
                            time.sleep(2)  # 增加等待时间
                        else:
                            break
                    except:
                        break

                # 点击"立即体验"
                try:
                    experience_btn = self.page.locator('button:has-text("立即体验")')
                    if experience_btn.count() > 0 and experience_btn.first.is_visible():
                        experience_btn.first.click(timeout=3000)
                        print(f"✓ 已点击立即体验")
                        time.sleep(2)
                except:
                    pass

            # 等待弹窗完全关闭
            print("等待页面加载...")
            time.sleep(3)

            # 填写标题
            print("填写标题...")
            title_input = self.page.locator('input[placeholder*="标题"]').first
            title_input.fill(title)
            time.sleep(1)

            # 填写描述
            print("填写描述...")
            desc_input = self.page.locator('textarea').first
            desc_input.fill(description)
            time.sleep(1)

            # 自动点击发布按钮
            print("正在点击发布按钮...")
            publish_selectors = [
                'button:has-text("发布")',
                'button:has-text("立即发布")',
                'button.submit-btn',
                '[class*="publish"][class*="btn"]'
            ]

            clicked = False
            for selector in publish_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        button = self.page.locator(selector).first
                        if button.is_visible() and button.is_enabled():
                            button.click(timeout=5000)
                            print(f"✓ 已点击发布按钮 (选择器: {selector})")
                            clicked = True
                            break
                except Exception as e:
                    continue

            if not clicked:
                print("❌ 未找到可点击的发布按钮")
                self.page.screenshot(path=str(BASE_DIR / "kuaishou_publish_error.png"))
                return False

            # 等待可能的弹窗
            print("等待页面响应...")
            time.sleep(3)

            # 处理快手的二次弹窗（需要关闭）
            print("检查是否有二次弹窗...")

            # 先尝试关闭弹窗
            close_selectors = [
                'button:has-text("关闭")',
                'button:has-text("取消")',
                'button:has-text("知道了")',
                'button:has-text("我知道了")',
                '.modal .close',
                '[class*="modal"] [class*="close"]',
                '[class*="dialog"] [class*="close"]',
                'svg[class*="close"]'
            ]

            for selector in close_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        button = self.page.locator(selector).first
                        if button.is_visible():
                            button.click(timeout=3000)
                            print(f"✓ 已关闭弹窗 (选择器: {selector})")
                            time.sleep(2)
                            break
                except:
                    continue

            # 再检查是否有确认按钮
            confirm_selectors = [
                'button:has-text("确认")',
                'button:has-text("确定")',
                'button:has-text("确认发布")',
                '.modal button:has-text("发布")'
            ]

            for selector in confirm_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        button = self.page.locator(selector).first
                        if button.is_visible():
                            button.click(timeout=3000)
                            print(f"✓ 已点击确认按钮")
                            time.sleep(2)
                            break
                except:
                    continue

            # 等待发布完成
            print("等待发布完成...")
            time.sleep(5)

            # 检查发布结果
            success_indicators = ['发布成功', '发布中', '审核中', '等待审核']
            found_success = False
            for indicator in success_indicators:
                if self.page.locator(f'text={indicator}').count() > 0:
                    print(f"✅ 检测到: {indicator}")
                    found_success = True
                    break

            # 检查是否还在编辑页面
            if self.page.locator('input[placeholder*="标题"]').count() > 0:
                print("❌ 视频未成功发布，仍在编辑页面")
                self.page.screenshot(path=str(BASE_DIR / "kuaishou_still_editing.png"))
                return False

            if found_success:
                return True

            print("⚠️  未检测到明确的成功标志")
            self.page.screenshot(path=str(BASE_DIR / "kuaishou_uncertain.png"))
            return False

        except Exception as e:
            print(f"❌ 发布失败: {e}")
            self.page.screenshot(path=str(BASE_DIR / "kuaishou_error.png"))
            return False

    def publish_bilibili(self, video_path, title, description, tags):
        """发布到B站"""
        print(f"\n开始发布到B站: {video_path}")

        try:
            # B站投稿页面
            upload_url = "https://member.bilibili.com/platform/upload/video/frame"
            self.page.goto(upload_url, timeout=30000)
            time.sleep(3)

            # 检查是否需要登录（通过检测上传控件）
            upload_check = self.page.locator('input[type="file"]').count()
            if upload_check == 0:
                # 等待页面加载
                time.sleep(2)
                upload_check = self.page.locator('input[type="file"]').count()

            if upload_check == 0:
                print("❌ 需要登录，请先运行登录流程保存 cookies")
                return False

            # 上传视频
            print("正在上传视频...")
            upload_input = self.page.locator('input[type="file"]').first
            upload_input.set_input_files(str(video_path))

            # 等待上传完成
            print("等待视频上传...")
            max_wait = 180  # B站视频处理较慢，等待3分钟
            for i in range(max_wait):
                time.sleep(1)
                if self.page.locator('text=上传完成').count() > 0 or \
                   self.page.locator('text=转码完成').count() > 0:
                    print("✓ 视频上传完成")
                    break
                if i % 15 == 0:
                    print(f"  上传中... {i}秒")

            time.sleep(3)

            # 填写标题
            print("填写标题...")
            title_input = self.page.locator('input.input-val').first
            title_input.fill(title)
            time.sleep(1)

            # 填写简介（B站使用富文本编辑器，不是 textarea）
            print("填写简介...")
            desc_selectors = [
                '.ql-editor',  # Quill 编辑器
                '[contenteditable="true"]',  # 可编辑 div
                'textarea'  # 备用
            ]

            desc_filled = False
            for selector in desc_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        desc_elem = self.page.locator(selector).first
                        if desc_elem.is_visible():
                            desc_elem.click()  # 先点击激活编辑器
                            time.sleep(0.5)
                            desc_elem.fill(description)
                            print(f"  ✓ 简介已填写 (使用选择器: {selector})")
                            desc_filled = True
                            break
                except:
                    continue

            if not desc_filled:
                print("  ⚠️  未找到简介输入框，跳过")

            time.sleep(1)

            # 添加标签
            if tags:
                print("添加标签...")
                tag_input = self.page.locator('input[placeholder*="标签"]').first
                for tag in tags[:3]:  # B站最多3个标签
                    tag_input.fill(tag)
                    tag_input.press("Enter")
                    time.sleep(1)

            # 检查并选择分区（如果需要）
            print("检查分区设置...")
            if self.page.locator('text=请选择分区').count() > 0:
                print("  需要选择分区，尝试自动选择...")
                try:
                    # 点击分区选择器
                    self.page.locator('text=请选择分区').first.click()
                    time.sleep(1)
                    # 选择"生活"分区
                    if self.page.locator('text=生活').count() > 0:
                        self.page.locator('text=生活').first.click()
                        time.sleep(1)
                        # 选择"日常"子分区
                        if self.page.locator('text=日常').count() > 0:
                            self.page.locator('text=日常').first.click()
                            print("  ✓ 已选择分区：生活 > 日常")
                            time.sleep(1)
                except Exception as e:
                    print(f"  ⚠️  自动选择分区失败: {e}")
            else:
                print("  ✓ 分区已设置")

            # 等待封面自动生成（在滚动之前）
            print("等待封面自动生成...")
            time.sleep(8)  # 给封面生成足够的时间

            # 滚动到页面底部（"立即投稿"按钮在底部）
            print("滚动到页面底部...")
            # 多次滚动确保到达底部
            for _ in range(3):
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)

            # 滚动后等待页面重新渲染
            time.sleep(3)

            # 使用准确的选择器查找并点击提交按钮
            print("使用准确选择器查找并点击'立即投稿'按钮...")
            clicked = False

            # B站的"立即投稿"按钮在 micro-app 中，使用多种策略
            selectors = [
                'span.submit-add',  # class 选择器
                'span[data-reporter-id="82"]',  # 属性选择器
                '//span[@class="submit-add"]',  # XPath
                '//span[contains(@class, "submit-add")]',  # XPath 模糊匹配
                '//span[text()="立即投稿"]',  # XPath 文本匹配
            ]

            for attempt in range(3):  # 尝试点击 2-3 次
                time.sleep(2)  # 间隔 2 秒

                for selector in selectors:
                    try:
                        # 尝试使用 Playwright 的选择器
                        if self.page.locator(selector).count() > 0:
                            btn = self.page.locator(selector).first
                            if btn.is_visible() and btn.is_enabled():
                                btn.click(timeout=5000)
                                print(f"✓ 第 {attempt + 1} 次点击成功 (选择器: {selector})")
                                clicked = True
                                time.sleep(2)
                                break
                    except Exception as e:
                        continue

                if clicked:
                    # 检查按钮是否还在
                    time.sleep(1)
                    still_there = self.page.locator('span.submit-add').count() > 0
                    if not still_there:
                        print("✓ 按钮已消失，发布可能成功")
                        break
                else:
                    print(f"  第 {attempt + 1} 次未找到可点击按钮")

            # 如果 Playwright 选择器失败，尝试 JavaScript
            if not clicked:
                print("尝试使用 JavaScript 点击...")
                result = self.page.evaluate("""
                    () => {
                        // 查找 submit-add 类的 span
                        const btn = document.querySelector('span.submit-add');
                        if (btn) {
                            btn.click();
                            return {success: true, text: btn.textContent.trim()};
                        }

                        // 备用：查找所有 span，匹配文本
                        const spans = Array.from(document.querySelectorAll('span'));
                        const submitBtn = spans.find(s => s.textContent.trim() === '立即投稿');
                        if (submitBtn) {
                            submitBtn.click();
                            return {success: true, text: submitBtn.textContent.trim()};
                        }

                        return {success: false};
                    }
                """)

                if result['success']:
                    print(f"✓ JavaScript 点击成功: '{result['text']}'")
                    clicked = True
                    time.sleep(2)

            # 检查是否有二次确认弹窗
            time.sleep(2)
            print("检查是否有确认弹窗...")
            if self.page.locator('button:has-text("确定")').count() > 0:
                confirm_btn = self.page.locator('button:has-text("确定")').first
                if confirm_btn.is_visible():
                    confirm_btn.click()
                    print("✓ 已点击确认按钮")
                    time.sleep(2)
                    clicked = True

            if not clicked:
                print("\n" + "=" * 60)
                print("⚠️  自动点击失败（可能是 B站 反自动化检测）")
                print("请在浏览器中手动点击【立即投稿】按钮")
                print("点击后脚本将自动继续...")
                print("=" * 60)

                # 等待用户手动点击，检测页面是否离开编辑状态
                print("\n等待手动点击...")
                for i in range(120):  # 等待最多 2 分钟
                    time.sleep(1)

                    # 检查是否还在编辑页面
                    has_upload = self.page.locator('input[type="file"]').count() > 0
                    has_title = self.page.locator('input.input-val').count() > 0

                    if not has_upload and not has_title:
                        print(f"\n✓ 检测到页面已跳转（等待 {i+1} 秒）")
                        clicked = True
                        break

                    if i % 10 == 0 and i > 0:
                        print(f"  等待中... {i}秒")

                if not clicked:
                    print("\n❌ 等待超时，未检测到页面跳转")
                    return False

            # 等待页面响应（点击后可能有弹窗或跳转）
            print("等待页面响应...")
            time.sleep(3)

            # 检查是否有错误提示
            print("检查是否有错误提示...")
            error_keywords = ['错误', '失败', '请填写', '必填', '不能为空', '请选择', '请上传']
            found_errors = []

            for keyword in error_keywords:
                if self.page.locator(f'text={keyword}').count() > 0:
                    print(f"  ⚠️  检测到错误提示: {keyword}")
                    found_errors.append(keyword)

            if found_errors:
                self.page.screenshot(path=str(BASE_DIR / "bilibili_errors.png"))
                print(f"  已保存错误截图: bilibili_errors.png")
                print(f"  错误信息: {', '.join(found_errors)}")

            # 处理可能的二次确认弹窗
            print("检查是否有二次确认弹窗...")
            time.sleep(2)
            confirm_selectors = [
                'button:has-text("确认")',
                'button:has-text("确定")',
                'button:has-text("确认投稿")',
                '.modal button:has-text("投稿")'
            ]

            for selector in confirm_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        button = self.page.locator(selector).first
                        if button.is_visible():
                            button.click(timeout=3000)
                            print(f"✓ 已点击二次确认按钮")
                            time.sleep(2)
                            break
                except:
                    continue

            # 等待发布完成
            print("等待发布完成...")
            time.sleep(5)

            # 检查发布结果
            # 1. 首先检查是否还在上传/编辑页面（有上传控件或标题输入框）
            has_upload_control = self.page.locator('input[type="file"]').count() > 0
            has_title_input = self.page.locator('input.input-val').count() > 0

            current_url = self.page.url
            print(f"当前 URL: {current_url}")
            print(f"是否有上传控件: {has_upload_control}")
            print(f"是否有标题输入框: {has_title_input}")

            # 2. 如果还在编辑页面，说明没有提交成功
            if has_upload_control or has_title_input:
                print("❌ 视频未成功发布，仍在上传/编辑页面")
                self.page.screenshot(path=str(BASE_DIR / "bilibili_still_editing.png"))
                return False

            # 3. 如果已经离开编辑页面，检查成功标志
            success_indicators = ['投稿成功', '提交成功', '审核中', '等待审核', '稿件列表', '我的稿件']
            found_success = False
            for indicator in success_indicators:
                if self.page.locator(f'text={indicator}').count() > 0:
                    print(f"✅ 检测到: {indicator}")
                    found_success = True
                    break

            # 4. 如果没有编辑控件，且 URL 还是在 bilibili.com，认为可能成功
            if not has_upload_control and not has_title_input and 'bilibili.com' in current_url:
                print("✅ 已离开编辑页面，发布可能成功")
                found_success = True

            if found_success:
                print("✅ B站发布成功")
                return True

            print("❌ 未检测到明确的成功标志")
            self.page.screenshot(path=str(BASE_DIR / "bilibili_uncertain.png"))
            return False

        except Exception as e:
            print(f"❌ 发布失败: {e}")
            self.page.screenshot(path=str(BASE_DIR / "bilibili_error.png"))
            return False

    def publish_xiaohongshu(self, video_path, title, description, tags):
        """发布到小红书"""
        print(f"\n开始发布到小红书: {video_path}")

        try:
            self.page.goto(self.config['url'], timeout=30000)
            time.sleep(3)

            # 检查是否需要登录（通过检测上传控件）
            upload_check = self.page.locator('input[type="file"]').count()
            if upload_check == 0:
                # 等待页面加载
                time.sleep(2)
                upload_check = self.page.locator('input[type="file"]').count()

            if upload_check == 0:
                print("❌ 需要登录，请先运行登录流程保存 cookies")
                return False

            # 上传视频
            print("正在上传视频...")
            upload_input = self.page.locator('input[type="file"]').first
            upload_input.set_input_files(str(video_path))

            # 等待上传完成并自动进入编辑页面
            print("等待视频上传并进入编辑页面...")
            time.sleep(15)  # 等待上传和自动跳转

            # 检查是否已进入编辑页面（通过查找标题输入框）
            title_check = self.page.locator('input[placeholder*="标题"]').count()
            if title_check > 0:
                print("✓ 已自动进入编辑页面")
            else:
                print("等待进入编辑页面...")
                time.sleep(5)

            # 填写标题
            print("填写标题...")
            title_input = self.page.locator('input[placeholder*="标题"]').first
            title_input.fill(title)
            time.sleep(1)

            # 填写描述（把话题放在开头，避免下拉菜单挡住发布按钮）
            print("填写描述...")
            desc_input = self.page.locator('textarea, div[contenteditable="true"]').first

            # 先添加话题标签
            if tags:
                print("添加话题...")
                tags_text = ' '.join([f'#{tag}' for tag in tags[:5]])
                desc_input.fill(tags_text + '\n\n' + description)
            else:
                desc_input.fill(description)

            time.sleep(1)

            # 关闭话题选择框（只按 Escape 键，不点击其他地方）
            print("关闭话题选择框...")
            try:
                self.page.keyboard.press('Escape')
                time.sleep(1)
            except:
                pass

            # 自动点击发布按钮
            print("正在点击发布按钮...")

            # 等待页面完全加载
            print("等待页面完全加载...")
            time.sleep(3)

            # 滚动到页面顶部（发布按钮在右上角）
            try:
                self.page.evaluate("window.scrollTo(0, 0)")
                time.sleep(1)
            except:
                pass

            # 查找纯"发布"按钮
            all_publish_buttons = self.page.locator('button:has-text("发布")')
            button_count = all_publish_buttons.count()

            print(f"找到 {button_count} 个包含'发布'的按钮")

            # 如果没找到，列出所有按钮用于调试
            if button_count == 0:
                print("调试：列出所有按钮...")
                all_btns = self.page.locator('button')
                total = all_btns.count()
                print(f"  页面共有 {total} 个按钮")
                for i in range(min(total, 10)):
                    try:
                        btn = all_btns.nth(i)
                        if btn.is_visible():
                            text = btn.inner_text(timeout=1000).strip()
                            if text:
                                print(f"    按钮 {i+1}: '{text}'")
                    except:
                        pass

            # 查找纯"发布"按钮（排除"发布笔记"等）
            clicked = False
            for i in range(button_count):
                try:
                    btn = all_publish_buttons.nth(i)
                    btn_text = btn.inner_text(timeout=1000).strip()

                    # 只点击纯"发布"按钮
                    if btn_text == '发布' and btn.is_visible() and btn.is_enabled():
                        print(f"找到纯'发布'按钮，点击...")
                        btn.click(timeout=5000)
                        print("✓ 发布按钮已点击")
                        clicked = True
                        break
                except Exception as e:
                    continue

            if not clicked:
                print("❌ 未找到可点击的'发布'按钮")
                return False

            time.sleep(3)

            # 等待发布完成
            print("等待发布完成...")
            time.sleep(5)

            # 检查是否已离开编辑页面（成功发布的标志）
            title_input_count = self.page.locator('input[placeholder*="标题"]').count()

            if title_input_count == 0:
                # 已离开编辑页面，说明发布成功
                print("✅ 已离开编辑页面，发布成功")
                return True

            # 如果还在编辑页面，检查是否有成功提示
            success_indicators = ['发布成功', '发布中', '审核中', '等待审核']
            found_success = False
            for indicator in success_indicators:
                if self.page.locator(f'text={indicator}').count() > 0:
                    print(f"✅ 检测到: {indicator}")
                    found_success = True
                    break

            if found_success:
                return True

            # 仍在编辑页面且没有成功提示
            print("❌ 视频未成功发布，仍在编辑页面")
            self.page.screenshot(path=str(BASE_DIR / "xiaohongshu_still_editing.png"))
            return False

        except Exception as e:
            print(f"❌ 发布失败: {e}")
            self.page.screenshot(path=str(BASE_DIR / "xiaohongshu_error.png"))
            return False

    def publish(self, video_path, title, description, tags=None):
        """发布视频到指定平台"""
        if tags is None:
            tags = []

        if self.platform == "douyin":
            return self.publish_douyin(video_path, title, description, tags)
        elif self.platform == "kuaishou":
            return self.publish_kuaishou(video_path, title, description, tags)
        elif self.platform == "bilibili":
            return self.publish_bilibili(video_path, title, description, tags)
        elif self.platform == "xiaohongshu":
            return self.publish_xiaohongshu(video_path, title, description, tags)
        else:
            print(f"不支持的平台: {self.platform}")
            return False


def get_latest_video():
    """获取最新的视频文件"""
    video_files = list(BASE_DIR.glob("output_*/iran_news_*.mp4"))
    if not video_files:
        return None

    # 按修改时间排序，返回最新的
    latest = max(video_files, key=lambda p: p.stat().st_mtime)
    return latest


def generate_content(video_path):
    """生成视频标题、描述和标签"""
    now = datetime.now()

    title = f"伊朗战争最新消息 {now.strftime('%m月%d日')} | 中东局势快讯"

    description = f"""📰 伊朗战争最新资讯播报
🕐 更新时间：{now.strftime('%Y年%m月%d日 %H:%M')}

本期内容涵盖：
✅ 伊朗最新军事动态
✅ 中东地区局势分析
✅ 国际关系最新进展

#伊朗战争 #中东局势 #国际新闻 #时事热点"""

    tags = ["伊朗战争", "中东局势", "国际新闻", "时事热点", "军事资讯"]

    return title, description, tags


def main():
    print("=" * 60)
    print("视频自动发布工具")
    print("=" * 60)

    # 获取最新视频
    video_path = get_latest_video()
    if not video_path:
        print("错误: 未找到视频文件")
        return

    print(f"\n找到视频: {video_path}")
    print(f"文件大小: {video_path.stat().st_size / 1024 / 1024:.2f} MB")

    # 生成内容
    title, description, tags = generate_content(video_path)

    print(f"\n标题: {title}")
    print(f"描述: {description[:100]}...")
    print(f"标签: {', '.join(tags)}")

    # 选择平台
    print("\n请选择发布平台:")
    print("1. 抖音")
    #print("2. 快手")
    print("3. B站")
    print("4. 小红书")
    print("5. 全部平台")

    choice = input("\n请输入选项 (1-5): ").strip()

    platforms_to_publish = []
    if choice == "1":
        platforms_to_publish = ["douyin"]
    elif choice == "2":
        platforms_to_publish = ["kuaishou"]
    elif choice == "3":
        platforms_to_publish = ["bilibili"]
    elif choice == "4":
        platforms_to_publish = ["xiaohongshu"]
    elif choice == "5":
        platforms_to_publish = ["douyin", "kuaishou", "bilibili", "xiaohongshu"]
    else:
        print("无效选项")
        return

    # 发布到各平台
    results = {}
    for platform in platforms_to_publish:
        print(f"\n{'=' * 60}")
        print(f"发布到 {PLATFORMS[platform]['name']}")
        print(f"{'=' * 60}")

        with VideoPublisher(platform, headless=False) as publisher:
            success = publisher.publish(video_path, title, description, tags)
            results[platform] = success

    # 显示结果
    print("\n" + "=" * 60)
    print("发布结果汇总")
    print("=" * 60)
    for platform, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{PLATFORMS[platform]['name']}: {status}")


if __name__ == "__main__":
    main()
