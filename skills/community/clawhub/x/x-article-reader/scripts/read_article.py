#!/usr/bin/env python3
"""
read_article.py — 朗读 X (Twitter) Articles
============================================
用法:
  python3 read_article.py <url>
  python3 read_article.py <url> --voice Tingting
  python3 read_article.py <url> --output ~/Desktop/article.aiff
  python3 read_article.py <url> --show-browser

首次使用前运行一次认证：
  python3 auth_setup.py
"""

import argparse
import subprocess
import sys
import time
import re
from pathlib import Path

# ============================================================================
# 路径 — 本技能完全独立，不依赖任何其他技能
# ============================================================================
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data" / "browser_state"
BROWSER_PROFILE_DIR = DATA_DIR / "browser_profile"


# ============================================================================
# 语言检测
# ============================================================================
def detect_language(text: str) -> str:
    """中文字符占比 >15% → zh，否则 → en"""
    if not text:
        return "en"
    chinese = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))
    return "zh" if chinese / len(text) > 0.15 else "en"


def get_voice(lang: str, override: str = None) -> str:
    if override:
        return override
    return {"zh": "Tingting", "en": "Samantha"}.get(lang, "Samantha")


# ============================================================================
# 文章抓取
# ============================================================================
def fetch_article(url: str, headless: bool = True) -> dict:
    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        print("❌ patchright 未安装，请运行：")
        print("   pip install patchright")
        print("   python3 -m patchright install chromium")
        sys.exit(1)

    if not BROWSER_PROFILE_DIR.exists():
        print("❌ 未找到认证数据，请先运行：")
        print(f"   cd {SKILL_DIR}/scripts")
        print("   python3 auth_setup.py")
        sys.exit(1)

    print(f"🌐 正在加载文章...")
    print(f"   {url}")

    playwright = sync_playwright().start()
    context = None
    try:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_PROFILE_DIR),
            headless=headless,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        )

        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)

        # 等待内容出现
        try:
            page.wait_for_selector("article, main, [role='article']", timeout=8000)
        except Exception:
            pass

        # 提取标题
        title = page.evaluate("""() => {
            const sel = ['[data-testid="articleTitle"]','article h1','h1','.article-title'];
            for (const s of sel) {
                const el = document.querySelector(s);
                if (el && el.innerText.trim()) return el.innerText.trim();
            }
            let t = document.title || '无标题';
            t = t.replace(/^\\(\\d+\\)\\s*/, '').replace(/\\s*\\/\\s*X$/, '');
            const m = t.match(/on X: "(.+)"/);
            return m ? m[1] : t;
        }""")

        # 提取正文
        text = page.evaluate("""() => {
            const body = document.body.cloneNode(true);
            ['nav','header','footer','script','style','button',
             '[role="navigation"]','[aria-hidden="true"]'].forEach(s => {
                body.querySelectorAll(s).forEach(el => el.remove());
            });
            const main = body.querySelector('article') ||
                         body.querySelector('[role="article"]') ||
                         body.querySelector('main') || body;
            return (main.innerText || '').trim();
        }""")

        # 清理空行
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        text = '\n'.join(lines)
        if text.startswith(title):
            text = text[len(title):].strip()

        lang = detect_language(text or title)

        print(f"✅ 文章加载成功")
        print(f"   标题：{title}")
        print(f"   字数：{len(text)} 字符")
        print(f"   语言：{'中文 🇨🇳' if lang == 'zh' else '英文 🇺🇸'}")

        return {"title": title, "text": text, "lang": lang}

    except Exception as e:
        print(f"❌ 加载失败：{e}")
        sys.exit(1)
    finally:
        if context:
            try:
                context.close()
            except Exception:
                pass
        try:
            playwright.stop()
        except Exception:
            pass


# ============================================================================
# TTS 朗读
# ============================================================================
def speak(title: str, text: str, voice: str, output_file: str = None):
    content = f"{title}。\n\n{text}"

    print(f"\n🔊 开始朗读...")
    print(f"   语音：{voice}")
    if output_file:
        print(f"   输出：{output_file}")
    print("   （按 Ctrl+C 停止）\n")

    cmd = ["say", "-v", voice]
    if output_file:
        cmd += ["-o", str(Path(output_file).expanduser())]
    cmd.append(content)

    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ {'音频已保存：' + output_file if output_file else '朗读完毕'}")
    except KeyboardInterrupt:
        print("\n⏹️  已停止")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 朗读失败：{e}")
        print(f"   检查语音是否存在：say -v '?'")
        sys.exit(1)


# ============================================================================
# 主程序
# ============================================================================
def main():
    parser = argparse.ArgumentParser(description="朗读 X Article")
    parser.add_argument("url", help="X Article URL")
    parser.add_argument("--voice", "-v", default=None,
                        help="指定语音（默认自动检测：中文=Tingting，英文=Samantha）")
    parser.add_argument("--output", "-o", default=None,
                        help="保存为音频文件（如 ~/Desktop/article.aiff）")
    parser.add_argument("--show-browser", action="store_true",
                        help="显示浏览器窗口（调试用）")
    args = parser.parse_args()

    article = fetch_article(url=args.url, headless=not args.show_browser)
    voice = get_voice(article["lang"], args.voice)
    speak(title=article["title"], text=article["text"],
          voice=voice, output_file=args.output)


if __name__ == "__main__":
    main()
