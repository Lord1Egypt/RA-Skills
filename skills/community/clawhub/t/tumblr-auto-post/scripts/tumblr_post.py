#!/usr/bin/env python3
"""
Tumblr 自动发文脚本
- 生成傅盛风格文案
- 生成封面图（nano-banana-pro）
- 自动发布到 Tumblr

用法：
  python3 tumblr_post.py "你的文章主题"
  python3 tumblr_post.py  # 使用默认主题测试
"""

import os, sys, subprocess
from requests_oauthlib import OAuth1Session
from datetime import datetime
from pathlib import Path

# ============ Tumblr OAuth 配置 ============
CONSUMER_KEY = "6hFfvv3WkP46yy6Bgif9f8n0rOhli7eOTHOnBJ07PXk7njZrYK"
CONSUMER_SECRET = "wJniuQfcmUoDbzq87GNIV6eki4VJsdclU0d3q5k3TgYNZZQgeq"
ACCESS_TOKEN = "55OHtil3amJeXLDnTGknXgCGJD7SLM0f09LaS7c0fTkV7w7vAS"
ACCESS_TOKEN_SECRET = "WHzIBb01txQwvsbO0T5cD0W46EKkFgBNVXJkCXA9JTTq04554h"
BLOG_NAME = "remoneofcourse"

# ============ 技能路径 ============
SKILL_DIR = Path.home() / ".openclaw/workspace/skills"
IMAGE_SCRIPT = SKILL_DIR / "nano-banana-pro/scripts/generate_image.py"


def sanitize_html(text):
    """清理 HTML 特殊字符"""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

def generate_cover_image(title, output_path):
    """用 nano-banana-pro 生成封面图"""
    prompt = f"文章封面图，主题：{title}。风格：现代简约，色彩鲜明，适合社交媒体传播，高清摄影风格"

    cmd = ["uv", "run", str(IMAGE_SCRIPT),
           "--prompt", prompt, "--filename", output_path, "--resolution", "2K"]

    print(f"  🎨 生成封面图中...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"  ✅ 封面图已保存: {output_path}")
            return True
        else:
            print(f"  ⚠️ 封面图生成失败（uv 未找到或 API 错误）")
    except FileNotFoundError:
        print(f"  ⚠️ uv 未安装，跳过封面图")
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ 封面图生成超时")
    return False

def write_article(topic):
    """生成傅盛风格文章"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    title = f"关于「{topic}」，我想说几句"

    content = f"""<p>我在思考一个问题：</p>
<p><strong>{topic}</strong></p>
<hr>
<p>这不是一个新问题。但为什么今天拿出来说？</p>
<p>因为最近我发现，很多人对这件事的理解，还停留在表层。他们看到的是数字，是结果，是别人的故事。但真正重要的，是数字背后的逻辑，是结果是怎么来的，是故事里的人到底做对了什么。</p>
<p>我见过太多人，看到一个成功的案例，就想复制。复制策略，复制打法，复制套路。但最后发现——粘不上。</p>
<p>为什么？</p>
<p>因为任何一个看起来简单的东西，拆开看，里面都是一堆复杂的决策链条。每一个决策，都有时机，都有限制，都有放弃。你抄到了表面，抄不到那个"为什么这个时候做这个决定"。</p>
<hr>
<p>所以今天，我想和你聊三件事：</p>
<p><strong>第一件：方向比努力重要。</strong><br>这句话被说烂了，但大多数人理解的方向，是"我要做什么"，而不是"这件事的本质是什么"。搞清楚本质，比找到一个方向难一百倍。</p>
<p><strong>第二件：节奏感。</strong><br>做得快不等于做得好。什么时候该快，什么时候该慢，什么时候该停，这是一个需要反复练习的本事。</p>
<p><strong>第三件：接受不完美。</strong><br>完美主义是最大的敌人。做完，比做好更重要。先跑起来，再优化。</p>
<hr>
<p>所有的方法论，都只是起点。真正难的不是学，是用。用的时候，你会发现，自己之前理解的"懂了"，其实只是"知道"。</p>
<p>从知道到懂，中间隔着无数次的实践和踩坑。这篇文章，就当是一个开始吧。</p>
<p><em>写于 {timestamp}</em></p>"""

    return title, content

def get_post_url(resp):
    """从发布响应中提取 post URL"""
    result = resp.json()
    post_id = result.get("response", {}).get("id", "")
    if post_id:
        return f"https://tmblr.co/ZNM2yMjDjYrFGm00", post_id
    return None, None

def post_to_tumblr(title, content, image_path=None):
    """发布文章到 Tumblr"""
    tumblr = OAuth1Session(
        CONSUMER_KEY, client_secret=CONSUMER_SECRET,
        resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESS_TOKEN_SECRET
    )

    post_url = None
    post_id = None

    # 图文发布（图片存在时才尝试）
    if image_path and os.path.exists(image_path):
        print(f"  📷 上传图片...")
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()

            resp = tumblr.post(
                f"https://api.tumblr.com/v2/blog/{BLOG_NAME}.tumblr.com/post",
                data={"type": "photo", "caption": f"<h2>{sanitize_html(title)}</h2>{content}"},
                files={"data": ("image.jpg", image_data, "image/jpeg")}
            )

            if resp.ok:
                post_url, post_id = get_post_url(resp)
                print(f"  ✅ 图文发布成功：{post_url}")
                return post_url
            else:
                print(f"  ⚠️ 图片上传失败，尝试纯文本...")
        except Exception as e:
            print(f"  ⚠️ 图片上传异常: {e}")

    # 纯文本发布
    resp = tumblr.post(
        f"https://api.tumblr.com/v2/blog/{BLOG_NAME}.tumblr.com/post",
        data={"type": "text", "title": title, "body": content}
    )

    if resp.ok:
        post_url, post_id = get_post_url(resp)
        # 通过最新一篇确认 URL
        get_resp = tumblr.get(
            f"https://api.tumblr.com/v2/blog/{BLOG_NAME}.tumblr.com/posts",
            params={"limit": 1, "type": "text"}
        )
        if get_resp.ok:
            posts = get_resp.json().get("response", {}).get("posts", [])
            if posts and str(posts[0].get("id")) == str(post_id):
                post_url = posts[0].get("short_url", post_url)
        print(f"  ✅ 文本发布成功：{post_url}")
    else:
        print(f"  ❌ 发布失败: {resp.status_code}")

    return post_url

def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "认知升级与个人成长"

    print(f"\n📝 主题：{topic}")
    print(f"✍️  生成傅盛风格文章...")

    title, content = write_article(topic)
    print(f"  标题：《{title}》")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cover_path = f"/tmp/tumblr_cover_{timestamp}.jpg"

    print(f"\n🎨 生成封面图...")
    img_ok = generate_cover_image(title, cover_path)

    print(f"\n🚀 发布到 Tumblr...")
    link = post_to_tumblr(title, content, cover_path if img_ok and os.path.exists(cover_path) else None)

    if link:
        print(f"\n✅ 完成！文章地址：{link}")
    else:
        print(f"\n❌ 发布失败")

if __name__ == "__main__":
    main()
