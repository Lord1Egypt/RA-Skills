import os
import time
from playwright.sync_api import sync_playwright

# ==============================================================================
# 安全声明：本脚本仅用于本地可见浏览器中的草稿填写辅助，绝对不是自动发布工具。
# ==============================================================================
# - 必须在 headless=False 模式下运行。
# - 绝不自动点击“发布”按钮。
# - 绝不保存账号密码、不读取或注入 Cookie。
# - 遇到验证码或登录框必须等待人工处理。
# - 绝不读取项目外部文件。
# ==============================================================================

def load_local_article(filepath):
    """仅允许读取当前项目 output 目录内的文件"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    expected_path = os.path.abspath(filepath)
    
    # 防止路径穿越安全检查
    if not expected_path.startswith(base_dir):
        raise SecurityError("禁止读取项目目录之外的文件！")
        
    if not os.path.exists(expected_path):
        return None, None
        
    with open(expected_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    if not lines:
        return "", ""
        
    title = ""
    body = ""
    if lines[0].startswith('# '):
        title = lines[0].replace('# ', '').strip()
        body = "".join(lines[1:]).strip()
    else:
        title = "未命名草稿标题"
        body = "".join(lines).strip()
        
    return title, body

def fill_toutiao_draft():
    article_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'output', 'toutiao', 'toutiao_article.md')
    title, body = load_local_article(article_path)
    
    if not title and not body:
        print("未找到文章文件，请先运行提示词生成文章内容。")
        return

    print("启动浏览器辅助进程 (Playwright Headless=False)...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("打开头条号创作者平台...")
        try:
            page.goto("https://mp.toutiao.com/profile_v4/graphic/publish", timeout=30000)
        except Exception as e:
            print(f"页面加载超时或出错，尝试继续: {e}")
        
        print("\n=========================================")
        print("请在浏览器中手动登录头条号。")
        print("遇到拼图或验证码，请手动处理。")
        print("脚本正在等待进入编辑器页面...")
        print("=========================================\n")

        # 监控页面元素，判断是否进入编辑器
        # 头条号编辑器可能会改版，这里给出通用逻辑
        editor_loaded = False
        try:
            # 这是一个示例选择器，实际中头条号标题输入框可能不同
            # 等待长达5分钟，给用户充足的登录时间
            page.wait_for_selector("input.input-title, textarea.title-input, div.ProseMirror", timeout=300000)
            editor_loaded = True
        except Exception as e:
            print("等待编辑器超时或界面改版，交出控制权。")
            
        if editor_loaded:
            print("检测到编辑器已加载，开始填入标题和正文...")
            
            try:
                # 尝试填入标题
                title_input = page.locator("textarea[placeholder*='标题']").first
                if title_input.is_visible():
                    title_input.fill(title)
                
                # 尝试填入正文 (ProseMirror编辑器通常处理复杂，用类型模拟或剪贴板)
                content_editor = page.locator(".ProseMirror").first
                if content_editor.is_visible():
                    content_editor.click()
                    # 简单地把Markdown文本填入，为了排版用户后续需人工调整
                    # 头条编辑器对 markdown 的直接粘贴支持可能有限，这仅为草稿导入
                    page.keyboard.insert_text(body)
                
                print("\n✅ 草稿已成功导入文本区域！")
            except Exception as e:
                print(f"填入过程遇到界面变化: {e}")
                print("请手动将文本复制进编辑器。")

        print("\n⚠️ 脚本已完成自动化工作，现在停止并交出控制权。")
        print("👉 请人工核查：内容排版、上传封面、摘要。")
        print("👉 确认无误后，请人工点击界面下方的保存草稿或发布按钮。")
        
        # 挂起脚本，不关闭浏览器，等待人工操作
        try:
            page.wait_for_timeout(3600000) # 保持开启1小时
        except KeyboardInterrupt:
            pass
        finally:
            print("浏览器已关闭。")
            browser.close()

class SecurityError(Exception):
    pass

if __name__ == "__main__":
    fill_toutiao_draft()
