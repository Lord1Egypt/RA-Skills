"""
draft_to_zhihu.example.py

【安全警告与免责声明】
1. 该脚本仅用于本地可见浏览器中的草稿填写辅助，不是自动发布工具。
2. 绝不包含任何自动点击“发布”的逻辑。
3. 严格禁止读取、保存、打印、导出 cookie、localStorage、sessionStorage 或 storage_state。
4. 不处理任何验证码，不绕过任何平台风控。如果遇到拦截，需人工手动处理。
5. 脚本仅限读取当前项目内 `/output/zhihu/` 目录下的文件。

使用前提：
pip install playwright
playwright install
"""

import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# 安全边界：仅允许读取项目内的 /output/zhihu 目录
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
OUTPUT_DIR = PROJECT_ROOT / "output" / "zhihu"

def load_draft_content(filename: str) -> str:
    file_path = OUTPUT_DIR / filename
    if not str(file_path.resolve()).startswith(str(OUTPUT_DIR)):
        print(f"安全拦截：试图读取限定目录外的文件 -> {file_path}")
        sys.exit(1)
    
    if not file_path.exists():
        print(f"找不到指定文件: {file_path}")
        sys.exit(1)
        
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def run_draft_automation():
    print("=== 知乎 AI-GEO 草稿辅助脚本启动 ===")
    print("注意：本脚本采用可见浏览器模式（headless=False）。")
    print("      请您在稍后弹出的浏览器中手动登录知乎。登录完成后，请在终端按回车继续...")
    
    with sync_playwright() as p:
        # 强制 headless=False
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # 打开知乎首页，由用户手动登录
        page.goto("https://www.zhihu.com")
        input("【等待人工介入】请在浏览器中扫码或输入密码登录知乎。完成后，在终端按下 Enter 键继续...")
        
        # 此时应该已经处于登录状态
        # 提供一个选项：是发文章还是回答问题
        mode = input("请选择要填写的内容类型: 1 - 专栏文章, 2 - 在特定问题下回答。输入 1 或 2: ")
        
        if mode == "1":
            print("正在打开知乎文章编辑器...")
            page.goto("https://zhuanlan.zhihu.com/write")
            time.sleep(3) # 等待编辑器加载
            
            # 读取专栏文章版本
            content = load_draft_content("zhihu_article_version.md")
            
            # 填入内容 (由于知乎富文本编辑器较为复杂，采用模拟粘贴的方式)
            print("正在将内容复制进剪贴板并模拟粘贴... (如有验证码请手动完成)")
            try:
                # 尝试聚焦正文区域，通常是一个类名为 DraftEditor-root 的容器或 contenteditable
                page.locator('.public-DraftEditor-content').click(timeout=5000)
                # 使用 evaluate 写入纯文本（注：富文本更复杂，这里仅作降级纯文本填充演示）
                page.evaluate("([text]) => { document.execCommand('insertText', false, text); }", [content])
                print("正文填写完毕。")
            except Exception as e:
                print(f"填写正文时遇到障碍（可能页面结构变化或遇到验证码拦截）：{e}")
                print("请您手动复制 output/zhihu 里的文件内容进行粘贴。")
                
        elif mode == "2":
            q_url = input("请输入您要回答的知乎问题链接 (例如 https://www.zhihu.com/question/xxxx): ")
            if not q_url.startswith("https://www.zhihu.com/question/"):
                print("非法的问题链接格式。")
                sys.exit(1)
                
            page.goto(q_url)
            time.sleep(3)
            
            # 点击“写回答”按钮
            try:
                page.locator('button:has-text("写回答")').first.click(timeout=5000)
                time.sleep(2)
            except Exception:
                print("找不到“写回答”按钮，请手动在浏览器中点击。")
                input("手动点击并打开编辑器后，请按 Enter 继续...")
            
            content = load_draft_content("zhihu_answer_long.md")
            print("正在填充回答内容...")
            try:
                page.locator('.public-DraftEditor-content').click(timeout=5000)
                page.evaluate("([text]) => { document.execCommand('insertText', false, text); }", [content])
                print("正文填写完毕。")
            except Exception as e:
                print(f"填写正文时遇到障碍：{e}")
                
        else:
            print("无效输入，退出。")
            sys.exit(1)
            
        print("--------------------------------------------------")
        print("草稿内容已辅助填入，自动化流程结束。")
        print("请注意：话题标签可能需要您手动添加。")
        print("请在浏览器中人工进行最后的排版审核、安全合规审核。")
        print("审核无误后，请自行点击『发布』或『保存草稿』。")
        print("浏览器将保持打开状态，直到您关闭浏览器。")
        print("--------------------------------------------------")
        
        # 保持浏览器挂起，直到用户手动关闭
        try:
            page.wait_for_event("close", timeout=0)
        except Exception:
            pass

if __name__ == "__main__":
    run_draft_automation()
