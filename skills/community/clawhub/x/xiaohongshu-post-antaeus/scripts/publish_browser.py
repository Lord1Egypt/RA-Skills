#!/usr/bin/env python3
"""
Create Xiaohongshu (小红书/RED) note via browser automation.
适用于个人账号（无 API 权限）或需要浏览器发文的场景。

每次打开或跳转页面后：等待 → 获取页面代码 → 由模型分析当前状态及下一步操作。
无硬编码，模型根据页面内容动态决策。

Usage:
  pip install playwright openai && playwright install chromium
  export DASHSCOPE_API_KEY=...   # 百炼，与 OpenClaw 主模型一致
  python3 publish_browser.py --title "标题" --content "正文" --images img1.jpg,img2.jpg
"""
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Callable, Optional

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "Error: playwright not installed. Run: pip install playwright && playwright install chromium",
        file=sys.stderr,
    )
    sys.exit(1)

from page_analyzer import analyze_page

XHS_BASE = "https://creator.xiaohongshu.com"
PUBLISH_URL = "https://creator.xiaohongshu.com/publish"

PAGE_WAIT_MS = 3000  # 每次打开/跳转后等待时间


def default_user_data_dir() -> Path:
    base = Path.home() / ".openclaw" / "xhs-browser"
    base.mkdir(parents=True, exist_ok=True)
    return base


def step_screenshot_and_confirm(page, step_name: str, step_num: int, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"step-{step_num:02d}-{step_name}.png"
    try:
        page.screenshot(path=str(path))
        print(f"[步骤 {step_num}] 截图已保存：{path}", file=sys.stderr)
    except Exception as e:
        print(f"截图失败：{e}", file=sys.stderr)
    print("  → 2 秒后自动继续...", file=sys.stderr)
    page.wait_for_timeout(2000)


def md_to_html(text: str) -> str:
    """将 Markdown 转换为小红书编辑器可用的 HTML。
    
    关键：用 <p> 标签包裹每段，因为小红书会过滤 <br> 但保留 <p> 的换行效果。
    """
    # 按空行分割成段落
    paragraphs = text.split('\n\n')
    
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        
        # 处理标题（# 号）
        if p.startswith('### '):
            html_paragraphs.append(f'<h3>{p[4:]}</h3>')
            continue
        if p.startswith('## '):
            html_paragraphs.append(f'<h2>{p[3:]}</h2>')
            continue
        if p.startswith('# '):
            html_paragraphs.append(f'<h1>{p[2:]}</h1>')
            continue
        
        # 处理段落内的换行（单行换行用<br>）
        lines = p.split('\n')
        processed_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 处理粗体和斜体
            line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"__(.+?)__", r"<b>\1</b>", line)
            line = re.sub(r"\*(.+?)\*", r"<i>\1</i>", line)
            line = re.sub(r"_(.+?)_", r"<i>\1</i>", line)
            
            # 处理列表项
            if line.startswith('- ') or line.startswith('• '):
                line = f'<div>• {line[2:]}</div>'
            
            processed_lines.append(line)
        
        # 用<br>连接行，然后用<p>包裹整个段落
        paragraph_html = '<br>'.join(processed_lines)
        html_paragraphs.append(f'<p>{paragraph_html}</p>')
    
    # 用空行（双<br>）连接段落
    return '<br><br>'.join(html_paragraphs)


def wait_for_login(page, timeout_ms: int = 120_000) -> bool:
    """等待登录完成。"""
    try:
        page.wait_for_url(
            lambda url: "creator.xiaohongshu.com" in url and "login" not in url.lower(),
            timeout=timeout_ms,
        )
        page.wait_for_timeout(5000)
        for _ in range(6):
            if "login" in page.url.lower():
                page.wait_for_timeout(5000)
                continue
            if page.locator("text=登录").count() > 0 or page.locator("text=扫码").count() > 0:
                page.wait_for_timeout(5000)
                continue
            break
        return "login" not in page.url.lower()
    except Exception:
        return False


def check_account_status(page) -> dict:
    """检查账户状态：实名认证、发布权限等。"""
    result = {
        "authenticated": True,
        "can_publish": True,
        "warnings": []
    }
    
    html = page.content()
    
    # 检查实名认证提示
    if "实名认证" in html or "去认证" in html:
        result["authenticated"] = False
        result["warnings"].append("账户未实名认证")
    
    # 检查发布权限
    if "无发布权限" in html or "权限不足" in html:
        result["can_publish"] = False
        result["warnings"].append("账户无发布权限")
    
    # 检查违规提示
    if "违规" in html or "被限制" in html:
        result["warnings"].append("账户可能存在违规记录")
    
    return result


def fill_note(
    page,
    *,
    title: str,
    content: str,
    tags: str = "",
    image_paths: list[Path] = None,
    step_cb: Optional[Callable] = None,
) -> bool:
    """
    填入笔记内容：标题、正文、标签、图片。
    模型驱动：每一步都获取页面 → 分析 → 执行
    """
    
    # 循环直到完成所有步骤
    max_rounds = 20
    for round_idx in range(max_rounds):
        # 每一步都分析当前页面
        result = analyze_page(page, context=f"目标：创建图文笔记《{title}》，需要上传图片、填标题正文、发布")
        print(f"[分析] state={result['state']} next_action={result['next_action']} reason={result['reason']}", file=sys.stderr)
        
        action = result['next_action']
        
        # 需要切换到图文模式
        if action == "goto_publish" or (action == "click_new_note" and "图文" in result.get('reason', '')):
            selector = result.get('selector')
            if selector:
                try:
                    page.locator(selector).first.click(timeout=3000)
                    print(f"已点击：{selector}", file=sys.stderr)
                    page.wait_for_timeout(3000)
                    continue
                except:
                    pass
            
            # 尝试常见选择器
            for sel in ["text=上传图文", "text=图文", "text=图文笔记"]:
                try:
                    if page.locator(sel).first.count() > 0:
                        page.locator(sel).first.click(timeout=3000)
                        print(f"已切换到图文模式", file=sys.stderr)
                        page.wait_for_timeout(3000)
                        break
                except:
                    continue
            continue
        
        # 上传图片
        if action == "upload_images" and image_paths:
            for img_path in image_paths[:9]:
                if not img_path.exists():
                    continue
                
                uploaded = False
                
                # 方法 1: 直接设置 file input
                try:
                    file_input = page.locator("input[type='file']").first
                    if file_input.count() > 0:
                        file_input.set_input_files(str(img_path), timeout=15000)
                        print(f"✅ 图片已上传（file input）: {img_path.name}", file=sys.stderr)
                        uploaded = True
                        
                        # 等待文件处理
                        page.wait_for_timeout(1000)
                        
                        # 使用 pyautogui 模拟按下 Esc 键关闭 macOS 文件对话框
                        try:
                            import pyautogui
                            pyautogui.press('esc')
                            print("⌨️  [pyautogui] 已发送 Esc 键关闭文件对话框", file=sys.stderr)
                            page.wait_for_timeout(500)
                            # 再按一次确保关闭
                            pyautogui.press('esc')
                            print("⌨️  [pyautogui] 再次发送 Esc 键", file=sys.stderr)
                        except Exception as e:
                            print(f"pyautogui 失败：{e}", file=sys.stderr)
                        
                        # 等待一下
                        page.wait_for_timeout(1000)
                        
                        # 点击页面确保焦点回来
                        try:
                            viewport = page.viewport_size
                            if viewport:
                                page.mouse.click(viewport['width'] // 2, 100)
                        except:
                            pass
                except Exception as e:
                    print(f"方法 1 失败：{e}", file=sys.stderr)
                
                if uploaded:
                    # 等待图片上传完成并显示预览（最多等待 30 秒）
                    print("⏳ 等待图片处理完成...", file=sys.stderr)
                    for i in range(30):
                        page.wait_for_timeout(1000)
                        # 检查是否有图片预览显示
                        preview = page.locator("[class*='image-preview'], [class*='uploadedImage'], img[src*='xiaohongshu']").first
                        if preview.count() > 0:
                            print(f"✅ 图片预览已显示（等待 {i+1}秒）", file=sys.stderr)
                            break
                        if i == 29:
                            print("⚠️  图片预览未显示，但继续执行", file=sys.stderr)
                    page.wait_for_timeout(3000)
                    continue
                
                # 方法 2: 点击上传按钮后设置 file input
                try:
                    upload_btn = page.locator("text=上传图片").first
                    if upload_btn.count() > 0:
                        upload_btn.click(timeout=3000)
                        page.wait_for_timeout(2000)
                        file_input = page.locator("input[type='file']").first
                        if file_input.count() > 0:
                            file_input.set_input_files(str(img_path), timeout=15000)
                            print(f"✅ 图片已上传（点击按钮）: {img_path.name}", file=sys.stderr)
                            uploaded = True
                except Exception as e:
                    print(f"方法 2 失败：{e}", file=sys.stderr)
                
                if uploaded:
                    page.wait_for_timeout(8000)
                    continue
                
                # 方法 3: 尝试拖拽上传（模拟 dragover + drop）
                try:
                    upload_zone = page.locator("[class*='upload'], [class*='drop'], div:has-text('上传图片')").first
                    if upload_zone.count() > 0:
                        # 触发文件对话框
                        upload_zone.click(timeout=3000)
                        page.wait_for_timeout(2000)
                        file_input = page.locator("input[type='file']").first
                        if file_input.count() > 0:
                            file_input.set_input_files(str(img_path), timeout=15000)
                            print(f"✅ 图片已上传（拖拽区域）: {img_path.name}", file=sys.stderr)
                            uploaded = True
                except Exception as e:
                    print(f"方法 3 失败：{e}", file=sys.stderr)
                
                if uploaded:
                    page.wait_for_timeout(8000)
                    continue
                
                # 所有方法都失败
                print(f"⚠️  无法上传图片：{img_path.name}", file=sys.stderr)
            
            continue
        
        # 填标题和正文
        if action == "fill_note":
            # 填标题（确保完整，最多 20 字）
            # 注意：emoji 占用多个字符，需要计算实际长度
            full_title = title
            while len(full_title.encode('utf-8')) > 60:  # 20 个中文字符约 60 字节
                full_title = full_title[:-1]
            
            for sel in ["input[placeholder*='标题']", "#title", "[name='title']"]:
                try:
                    inp = page.locator(sel).first
                    if inp.count() > 0:
                        # 先清空再填入
                        inp.clear(timeout=2000)
                        inp.fill(full_title, timeout=2000)
                        page.wait_for_timeout(1000)
                        # 验证填入的值
                        value = inp.input_value(timeout=2000)
                        print(f"✅ 标题已填入：{value}", file=sys.stderr)
                        break
                except Exception as e:
                    print(f"填标题失败：{e}", file=sys.stderr)
                    continue
            
            # 填正文
            raw = content[:900]
            if tags:
                raw = f"{raw}\n\n{tags}"
            content_html = f"<div>{raw}</div>"
            
            try:
                ok = page.evaluate(
                    """(html) => {
                        const editor = document.querySelector('[contenteditable="true"]');
                        if (editor) {
                            editor.innerHTML = html;
                            editor.dispatchEvent(new Event('input', { bubbles: true }));
                            return true;
                        }
                        return false;
                    }""",
                    content_html
                )
                if ok:
                    print("✅ 正文已写入", file=sys.stderr)
                else:
                    print("⚠️  未找到编辑器", file=sys.stderr)
            except Exception as e:
                print(f"正文写入失败：{e}", file=sys.stderr)
            
            if step_cb:
                step_cb(page, "填入内容后")
            
            # 填完后继续分析，检查是否需要发布
            page.wait_for_timeout(3000)
            continue
        
        # 发布
        if action == "done":
            print("流程完成", file=sys.stderr)
            break
        
        # 需要用户操作
        if action == "user_action_required":
            print(f"需用户操作：{result['reason']}", file=sys.stderr)
            # 尝试填内容
            if result['state'] == 'note_editor':
                # 填标题
                for sel in ["input[placeholder*='标题']"]:
                    try:
                        inp = page.locator(sel).first
                        if inp.count() > 0:
                            inp.fill(title[:20], timeout=2000)
                            break
                    except:
                        pass
                # 填正文
                try:
                    editable = page.locator("[contenteditable='true']").first
                    if editable.count() > 0:
                        editable.evaluate("(el, html) => { el.innerHTML = html; }", f"<div>{content[:900]}</div>")
                except:
                    pass
            break
        
        # 未知状态，等待后重试
        page.wait_for_timeout(3000)
    
    return True
    title_selectors = [
        "input[placeholder*='标题']",
        "input[placeholder*='title']",
        "#title",
        "[name='title']",
    ]
    for sel in title_selectors:
        try:
            inp = page.locator(sel).first
            if inp.count() > 0:
                inp.fill(title[:20], timeout=2000)
                print(f"标题已填入：{title[:20]}", file=sys.stderr)
                break
        except Exception:
            continue
    if step_cb:
        step_cb(page, "填入标题后")
    
    # 第四步：填入正文
    print("填入正文...", file=sys.stderr)
    raw = content[:900]
    if tags:
        raw = f"{raw}\n\n{tags}"
    content_html = f"<div>{raw}</div>" if not raw.strip().startswith("<") else raw
    
    for attempt in range(5):
        try:
            ok = page.evaluate(
                """(html) => {
                return new Promise((resolve) => {
                    const editor = document.querySelector('[contenteditable="true"]') || 
                                   document.querySelector('.editor') ||
                                   document.querySelector('[class*="editor"]');
                    if (!editor) { resolve(false); return; }
                    editor.innerHTML = html;
                    editor.dispatchEvent(new Event('input', { bubbles: true }));
                    resolve(true);
                });
            }""",
                content_html,
            )
            if ok:
                print("正文已写入", file=sys.stderr)
                break
        except Exception:
            pass
        page.wait_for_timeout(2000)
    else:
        try:
            editable = page.locator("[contenteditable='true']").first
            if editable.count() > 0:
                editable.click()
                editable.evaluate("(el, html) => { el.innerHTML = html; }", content_html)
                editable.evaluate("(el) => { el.dispatchEvent(new Event('input', { bubbles: true })); }")
                print("正文已通过 contenteditable 注入", file=sys.stderr)
        except Exception as e:
            print(f"正文写入失败：{e}", file=sys.stderr)

    if step_cb:
        step_cb(page, "填入正文后")
    
    # 第五步：上传图片（最后一步）
    if image_paths:
        print("上传图片...", file=sys.stderr)
        
        for img_path in image_paths[:9]:
            if not img_path.exists():
                print(f"Warning: image not found: {img_path}", file=sys.stderr)
                continue
            try:
                # 直接使用文件输入上传
                file_input = page.locator("input[type='file']").first
                if file_input.count() > 0:
                    file_input.set_input_files(str(img_path), timeout=15000)
                    print(f"✅ 图片已上传：{img_path.name}", file=sys.stderr)
                    
                    # 关键：等待上传完成后，检查是否跳转到视频模式
                    page.wait_for_timeout(5000)
                    
                    # 检查 URL 是否变成视频模式
                    current_url = page.url
                    if "target=video" in current_url:
                        print("⚠️  检测到跳转到视频模式，立即切换回图文...", file=sys.stderr)
                        page.locator("text=上传图文").first.click(timeout=5000)
                        page.wait_for_timeout(5000)
                    
                    # 检查是否有发布按钮（图文模式编辑页）
                    try:
                        publish_btn = page.locator("text=发布").first
                        if publish_btn.count() > 0:
                            print("✅ 确认在图文编辑页", file=sys.stderr)
                    except:
                        # 如果不在编辑页，强制导航
                        print("⚠️  不在编辑页，强制导航...", file=sys.stderr)
                        page.goto("https://creator.xiaohongshu.com/publish/publish?from=menu", wait_until="networkidle", timeout=20000)
                        page.wait_for_timeout(3000)
                        page.locator("text=上传图文").first.click(timeout=3000)
                        page.wait_for_timeout(5000)
                        
                else:
                    print("⚠️  未找到文件输入框", file=sys.stderr)
                    
            except Exception as e:
                print(f"⚠️  图片上传失败：{e}", file=sys.stderr)

    if step_cb:
        step_cb(page, "上传图片后")

    return True
    title_selectors = [
        "input[placeholder*='标题']",
        "input[placeholder*='title']",
        "#title",
        "[name='title']",
    ]
    for sel in title_selectors:
        try:
            inp = page.locator(sel).first
            if inp.count() > 0:
                inp.fill(title[:20], timeout=2000)
                print(f"标题已填入：{title[:20]}", file=sys.stderr)
                break
        except Exception:
            continue
    if step_cb:
        step_cb(page, "填入标题后")

    # 填入正文
    raw = content[:900]
    if tags:
        raw = f"{raw}\n\n{tags}"
    content_html = f"<div>{raw}</div>" if not raw.strip().startswith("<") else raw
    
    for attempt in range(5):
        try:
            ok = page.evaluate(
                """(html) => {
                return new Promise((resolve) => {
                    const editor = document.querySelector('[contenteditable="true"]') || 
                                   document.querySelector('.editor') ||
                                   document.querySelector('[class*="editor"]');
                    if (!editor) { resolve(false); return; }
                    editor.innerHTML = html;
                    editor.dispatchEvent(new Event('input', { bubbles: true }));
                    resolve(true);
                });
            }""",
                content_html,
            )
            if ok:
                print("正文已写入", file=sys.stderr)
                break
        except Exception:
            pass
        page.wait_for_timeout(2000)
    else:
        try:
            editable = page.locator("[contenteditable='true']").first
            if editable.count() > 0:
                editable.click()
                editable.evaluate("(el, html) => { el.innerHTML = html; }", content_html)
                editable.evaluate("(el) => { el.dispatchEvent(new Event('input', { bubbles: true })); }")
                print("正文已通过 contenteditable 注入", file=sys.stderr)
        except Exception as e:
            print(f"正文写入失败：{e}", file=sys.stderr)

    if step_cb:
        step_cb(page, "填入正文后")

    # 上传图片
    if image_paths:
        for img_path in image_paths[:9]:
            if not img_path.exists():
                print(f"Warning: image not found: {img_path}", file=sys.stderr)
                continue
            try:
                file_input = page.locator("input[type='file']").first
                if file_input.count() > 0:
                    file_input.set_input_files(str(img_path), timeout=10000)
                    print(f"图片已上传：{img_path.name}", file=sys.stderr)
                    page.wait_for_timeout(2000)
                else:
                    upload_area = page.locator(
                        "[class*='upload'], [class*='cover'], text=上传，text=添加图片"
                    ).first
                    if upload_area.count() > 0:
                        upload_area.click()
                        page.wait_for_timeout(1000)
                        fi = page.locator("input[type='file']").first
                        if fi.count() > 0:
                            fi.set_input_files(str(img_path), timeout=10000)
                            print(f"图片已上传：{img_path.name}", file=sys.stderr)
                            page.wait_for_timeout(2000)
            except Exception as e:
                print(f"Warning: image upload may have failed: {e}", file=sys.stderr)

    if step_cb:
        step_cb(page, "上传图片后")

    return True


def click_publish(page) -> bool:
    """
    点击「发布」按钮并等待发布完成。
    流程：获取页面代码 → 分析 → 找到发布按钮 → 点击 → 处理确认弹窗 → 等待结果
    """
    # 第一步：获取页面代码并分析
    print("分析当前页面，查找发布按钮...", file=sys.stderr)
    html = page.content()
    current_url = page.url
    
    # 检查是否在编辑页
    if "/publish/publish" not in current_url:
        print(f"⚠️  当前不在编辑页：{current_url}", file=sys.stderr)
        return False
    
    # 第二步：找到发布按钮（使用精确选择器）
    selectors = [
        # 精确匹配用户提供的 HTML
        "button.d-button.bg-red:has-text('发布')",
        "button.--color-bg-fill:has-text('发布')",
        # 通用选择器
        "text=发布",
        "text=发布笔记", 
        "button:has-text('发布')",
        "[class*='publish-btn']",
        "[class*='submit']",
    ]
    
    publish_btn = None
    used_selector = None
    
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if el.count() > 0:
                # 检查按钮是否可见且在视口内
                if el.is_visible(timeout=2000):
                    el.scroll_into_view_if_needed(timeout=3000)
                    page.wait_for_timeout(1000)
                    publish_btn = el
                    used_selector = sel
                    print(f"✅ 找到发布按钮：{sel}", file=sys.stderr)
                    break
        except Exception as e:
            continue
    
    if not publish_btn:
        print("⚠️  未找到发布按钮，尝试用模型分析...", file=sys.stderr)
        # 用模型分析页面找发布按钮
        result = analyze_page(page, context="找到发布按钮并点击")
        if result.get('next_action') == 'done':
            print("模型认为流程已完成", file=sys.stderr)
            return True
        # 尝试点击模型返回的选择器
        if result.get('selector'):
            try:
                page.locator(result['selector']).first.click(timeout=3000)
                print(f"已点击模型选择器：{result['selector']}", file=sys.stderr)
                page.wait_for_timeout(2000)
            except:
                pass
    
    # 第三步：点击发布按钮
    if publish_btn:
        try:
            # 先确保按钮在视口内
            publish_btn.scroll_into_view_if_needed(timeout=3000)
            page.wait_for_timeout(500)
            
            # 点击按钮
            publish_btn.click(timeout=5000)
            print("✅ 已点击发布按钮", file=sys.stderr)
            
            # 截图确认
            try:
                page.screenshot(path="/tmp/xhs-after-click.png")
                print("📸 已保存点击后截图", file=sys.stderr)
            except:
                pass
        except Exception as e:
            print(f"点击失败：{e}", file=sys.stderr)
            # 尝试用 JavaScript 点击
            try:
                publish_btn.evaluate("el => el.click()")
                print("✅ 已用 JS 点击", file=sys.stderr)
            except Exception as e2:
                print(f"JS 点击也失败：{e2}", file=sys.stderr)
                return False
    else:
        print("❌ 未找到发布按钮", file=sys.stderr)
        return False
    
    # 第四步：等待 3 秒，检查确认弹窗
    page.wait_for_timeout(3000)
    
    # 检查是否有确认弹窗（多种可能）
    confirm_texts = ["确认发布", "确定", "确认", "知道了", "好的"]
    confirm_clicked = False
    
    for text in confirm_texts:
        try:
            confirm_btn = page.locator(f"text={text}").first
            if confirm_btn.count() > 0 and confirm_btn.is_visible(timeout=2000):
                confirm_btn.scroll_into_view_if_needed(timeout=2000)
                page.wait_for_timeout(500)
                confirm_btn.click(timeout=3000)
                print(f"✅ 已点击确认：{text}", file=sys.stderr)
                confirm_clicked = True
                page.wait_for_timeout(2000)
                break
        except:
            continue
    
    # 第五步：等待发布完成（最多 45 秒）
    print("等待发布完成...", file=sys.stderr)
    for i in range(22):
        page.wait_for_timeout(2000)
        current_url = page.url
        html = page.content()
        
        # 检查发布成功
        success_indicators = [
            "发布成功", "已发布", "发布完成",
            "success", "已成功"
        ]
        for indicator in success_indicators:
            if indicator in html or indicator in page.title():
                print(f"✅ 发布成功！（{indicator}）", file=sys.stderr)
                return True
        
        # 检查是否跳转到笔记列表
        if "/publish/note" in current_url and "draft" not in current_url and "publish" not in current_url:
            print("✅ 已跳转到笔记列表，发布成功！", file=sys.stderr)
            return True
        
        # 检查错误
        error_indicators = ["失败", "错误", "审核不通过", "违规", "拒绝"]
        for indicator in error_indicators:
            if indicator in html:
                print(f"⚠️  发布失败：{indicator}", file=sys.stderr)
                return False
        
        # 每 5 秒检查一次是否有新的确认弹窗
        if i % 5 == 0 and i > 0:
            for text in confirm_texts:
                try:
                    confirm_btn = page.locator(f"text={text}").first
                    if confirm_btn.count() > 0 and confirm_btn.is_visible(timeout=2000):
                        confirm_btn.click(timeout=3000)
                        print(f"✅ 再次点击确认：{text}", file=sys.stderr)
                        page.wait_for_timeout(2000)
                        break
                except:
                    continue
        
        print(f"  等待中... ({i+1}/22)", file=sys.stderr)
    
    print("⚠️  发布超时，请手动检查", file=sys.stderr)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create Xiaohongshu note via browser (model-driven)"
    )
    parser.add_argument("--title", help="Note title (≤20 chars)")
    parser.add_argument("--content", help="Note body (Markdown or HTML)")
    parser.add_argument("--content-file", help="Read content from file")
    parser.add_argument("--images", help="Image paths, comma-separated")
    parser.add_argument("--tags", default="", help="Hashtags, comma-separated")
    parser.add_argument("--headed", action="store_true", default=True)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--user-data-dir", help="Browser profile dir")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--step", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--model", help="LLM model (default: qwen3.5-plus)")
    args = parser.parse_args()

    if args.model:
        os.environ["XHS_ANALYZER_MODEL"] = args.model

    content = args.content
    if args.content_file:
        p = Path(args.content_file)
        if not p.exists():
            print(f"Error: file not found: {p}", file=sys.stderr)
            return 1
        content = p.read_text(encoding="utf-8")
    if not args.check_only:
        if not args.title:
            print("Error: --title required (unless --check-only)", file=sys.stderr)
            return 1
        if not content:
            print("Error: --content or --content-file required", file=sys.stderr)
            return 1

    if content and not content.strip().startswith("<"):
        content = md_to_html(content)

    image_paths = []
    if args.images:
        for img in args.images.split(","):
            img_path = Path(img.strip())
            if not img_path.exists():
                print(f"Error: image not found: {img_path}", file=sys.stderr)
                return 1
            image_paths.append(img_path)

    user_data = Path(args.user_data_dir) if args.user_data_dir else default_user_data_dir()
    step_dir = Path.home() / ".openclaw" / "xhs-steps"
    step_num = [0]

    def step_cb(pg, name: str) -> None:
        if args.step:
            step_num[0] += 1
            step_screenshot_and_confirm(pg, name, step_num[0], step_dir)

    headless = args.headless and not args.headed
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data),
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
            permissions=["clipboard-read", "clipboard-write"],
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        page.goto(XHS_BASE, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(PAGE_WAIT_MS)
        if args.step:
            step_num[0] += 1
            step_screenshot_and_confirm(page, "01-打开首页", step_num[0], step_dir)

        if args.check_only:
            result = analyze_page(page)
            print(
                f"state: {result['state']}\nnext_action: {result['next_action']}\nreason: {result['reason']}",
                file=sys.stderr,
            )
            if args.debug:
                (Path.home() / ".openclaw").mkdir(parents=True, exist_ok=True)
                (Path.home() / ".openclaw" / "xhs-page-check.html").write_text(
                    page.content(), encoding="utf-8"
                )
            browser.close()
            return 0 if result["state"] != "login_required" else 1

        # 模型驱动主循环
        max_rounds = 30
        for round_idx in range(max_rounds):
            # 检查账户状态
            if round_idx == 0:
                account_status = check_account_status(page)
                if account_status["warnings"]:
                    print(f"\n⚠️  账户状态警告:", file=sys.stderr)
                    for w in account_status["warnings"]:
                        print(f"   - {w}", file=sys.stderr)
                    if not account_status["authenticated"]:
                        print("\n❌ 账户未实名认证，无法发布", file=sys.stderr)
                        print("请前往：https://creator.xiaohongshu.com 进行实名认证", file=sys.stderr)
                        browser.close()
                        return 1
            
            result = analyze_page(page, context=f"目标：创建小红书笔记，标题《{args.title}》，需要上传图片、填标题正文、点击发布")
            print(
                f"[分析] state={result['state']} next_action={result['next_action']} reason={result['reason']}",
                file=sys.stderr,
            )

            action = result["next_action"]

            if action == "wait_for_scan":
                print("\n" + "=" * 50, file=sys.stderr)
                print("请使用小红书 App 扫描屏幕上的二维码登录", file=sys.stderr)
                print("=" * 50 + "\n", file=sys.stderr)
                if not wait_for_login(page, timeout_ms=args.timeout * 1000):
                    print("登录超时", file=sys.stderr)
                    browser.close()
                    return 1
                page.wait_for_timeout(PAGE_WAIT_MS)
                continue

            if action == "goto_publish":
                # 强制使用图文发布 URL（不是视频）
                url = "https://creator.xiaohongshu.com/publish/publish?from=menu"
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                page.wait_for_load_state("networkidle", timeout=10000)
                page.wait_for_timeout(PAGE_WAIT_MS)
                if args.step:
                    step_num[0] += 1
                    step_screenshot_and_confirm(page, "跳转发布页", step_num[0], step_dir)
                continue

            if action == "click_new_note":
                clicked = False
                # 优先点击「发布图文笔记」（不是视频）
                for sel in ["text=发布图文笔记", "text=图文笔记", "text=发布图文"]:
                    try:
                        if page.locator(sel).first.count() > 0:
                            page.locator(sel).first.click(timeout=3000)
                            clicked = True
                            print(f"已点击：{sel}", file=sys.stderr)
                            break
                    except Exception:
                        continue
                # 回退到通用选择器
                if not clicked:
                    for sel in ["text=发布笔记", "text=创作", "text=新建"]:
                        try:
                            if page.locator(sel).first.count() > 0:
                                page.locator(sel).first.click(timeout=3000)
                                clicked = True
                                break
                        except Exception:
                            continue
                page.wait_for_timeout(PAGE_WAIT_MS)
                if len(browser.pages) > 1:
                    page = browser.pages[-1]
                    page.bring_to_front()
                    page.wait_for_load_state("domcontentloaded", timeout=15000)
                    page.wait_for_timeout(PAGE_WAIT_MS)
                if args.step:
                    step_num[0] += 1
                    step_screenshot_and_confirm(page, "新建笔记", step_num[0], step_dir)
                continue

            if action == "fill_note" or action == "upload_images":
                # 检查当前是否在图文模式
                if "target=video" in page.url:
                    print("⚠️  检测到视频模式，切换到图文...", file=sys.stderr)
                    page.goto("https://creator.xiaohongshu.com/publish/publish?from=menu", wait_until="networkidle", timeout=20000)
                    page.wait_for_timeout(3000)
                    try:
                        page.locator("text=上传图文").first.click(timeout=5000)
                        page.wait_for_timeout(5000)
                        print("✅ 已切换到图文模式", file=sys.stderr)
                    except:
                        pass
                
                if args.debug:
                    try:
                        page.screenshot(path=str(Path.home() / ".openclaw" / "xhs-debug.png"))
                        (Path.home() / ".openclaw").mkdir(parents=True, exist_ok=True)
                        (Path.home() / ".openclaw" / "xhs-debug.html").write_text(
                            page.content(), encoding="utf-8"
                        )
                    except Exception:
                        pass
                fill_note(
                    page,
                    title=args.title,
                    content=content,
                    tags=args.tags,
                    image_paths=image_paths,
                    step_cb=step_cb if args.step else None,
                )
                if click_publish(page):
                    print("已点击发布，请等待上传完成。")
                else:
                    print("请手动点击「发布」。")
                break

            if action == "done":
                print("流程完成", file=sys.stderr)
                break

            if action == "user_action_required":
                print(f"需用户操作：{result['reason']}", file=sys.stderr)
                if result["state"] == "note_editor":
                    fill_note(
                        page,
                        title=args.title,
                        content=content,
                        tags=args.tags,
                        image_paths=image_paths,
                        step_cb=step_cb if args.step else None,
                    )
                    if click_publish(page):
                        print("已点击发布，请等待上传完成。")
                    else:
                        print("请手动点击「发布」。")
                break

            page.wait_for_timeout(PAGE_WAIT_MS)
        else:
            print("达到最大轮次，未完成流程", file=sys.stderr)

        if args.headed:
            try:
                input("按 Enter 关闭浏览器...")
            except EOFError:
                page.wait_for_timeout(600_000)
        else:
            page.wait_for_timeout(5000)

        browser.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
