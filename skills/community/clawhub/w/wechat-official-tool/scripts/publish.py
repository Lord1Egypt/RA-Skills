"""
publish.py - 微信公众号一键发布脚本

用法:
  python publish.py <文章.md路径> <封面图路径> [摘要]

功能:
  1. 读取 wechat_credentials.json 获取 AppID 和 AppSecret
  2. 获取 Access Token
  3. 上传封面图到永久素材
  4. 将 Markdown 转换为微信草稿 JSON
  5. 提交草稿到公众号

依赖: requests, Pillow
"""
import json
import os
import re
import sys
from pathlib import Path

# 尝试导入，缺少时给出友好提示
try:
    import requests
except ImportError:
    print("❌ 缺少 requests 库，请安装：pip install requests")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("❌ 缺少 Pillow 库，请安装：pip install Pillow")
    sys.exit(1)


# ============== 配置 ==============
API_BASE = "https://api.weixin.qq.com"
CREDENTIALS_FILE = "wechat_credentials.json"


# ============== 凭证读取 ==============
def load_credentials():
    """读取微信公众号凭证"""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(
            f"❌ 找不到凭证文件：{CREDENTIALS_FILE}\n"
            f"请在工作目录创建包含 appid 和 appsecret 的 JSON 文件"
        )

    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        creds = json.load(f)

    if "appid" not in creds or "appsecret" not in creds:
        raise ValueError("❌ 凭证文件必须包含 appid 和 appsecret 字段")

    return creds["appid"], creds["appsecret"]


# ============== API 请求 ==============
def get_access_token(appid, appsecret):
    """获取 Access Token"""
    url = f"{API_BASE}/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": appsecret
    }

    print("📡 获取 Access Token...")
    resp = requests.get(url, params=params, timeout=30)
    data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        error_msg = data.get("errmsg", "未知错误")
        if data["errcode"] == 40164:
            raise Exception(f"❌ 错误 40164：IP不在白名单\n请在 mp.weixin.qq.com 后台添加 IP：112.8.202.216")
        raise Exception(f"❌ 获取 Token 失败：{error_msg}")

    token = data["access_token"]
    print(f"✅ Token 获取成功")
    return token


def upload_permanent_material(token, file_path):
    """上传永久素材（封面图）"""
    url = f"{API_BASE}/cgi-bin/material/add_material"
    params = {"access_token": token, "type": "image"}

    # 检查文件大小
    file_size = os.path.getsize(file_path)
    max_size = 2 * 1024 * 1024  # 2MB

    if file_size > max_size:
        raise Exception(
            f"❌ 图片太大（{file_size / 1024 / 1024:.1f}MB），"
            f"永久素材限制 2MB\n"
            f"请使用 compress_img.py 压缩图片"
        )

    print(f"📤 上传封面图：{os.path.basename(file_path)} ({file_size / 1024:.0f}KB)...")

    with open(file_path, "rb") as f:
        files = {"media": (os.path.basename(file_path), f, "image/png")}
        resp = requests.post(url, params=params, files=files, timeout=60)

    data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        error_msg = data.get("errmsg", "未知错误")
        if data["errcode"] == 40006:
            raise Exception(f"❌ 图片太大，请压缩后再试")
        if data["errcode"] == 40007:
            raise Exception(f"❌ 无效的 media_id，请确认使用永久素材接口")
        raise Exception(f"❌ 上传失败：{error_msg}")

    media_id = data["media_id"]
    print(f"✅ 封面上传成功：media_id = {media_id}")
    return media_id


# ============== Markdown 转换 ==============
def md_to_wechat_html(md_text):
    """将 Markdown 转换为微信公众号 HTML"""
    html_parts = []
    lines = md_text.strip().split("\n")
    in_code_block = False

    for line in lines:
        line = line.strip()

        if line.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_parts.append(
                f'<p style="background:#f6f8fa;padding:10px;font-family:monospace;font-size:14px;">{escaped}</p>'
            )
            continue

        # 分割线
        if line == "---":
            html_parts.append('<hr style="border:none;border-top:1px solid #eee;margin:20px 0;"/>')
            continue

        # h2 标题
        if line.startswith("## "):
            title = escape_html(line[3:])
            html_parts.append(
                f'<h2 style="font-size:20px;font-weight:bold;margin:24px 0 10px 0;'
                f'border-left:4px solid #5766d9;padding-left:10px;">{title}</h2>'
            )
            continue

        # 主标题（# 开头的第一行，跳过）
        if line.startswith("# "):
            continue

        # 修改记录等辅助段落（以 ## 修改记录 开头则截断）
        if line.startswith("## 修改记录"):
            break

        # 空行
        if not line:
            continue

        # 列表项
        if line.startswith("- "):
            item = process_inline(line[2:])
            html_parts.append(
                f'<p style="margin:6px 0;padding-left:16px;color:#555;">&#8226; {item}</p>'
            )
            continue

        line = process_inline(line)
        html_parts.append(
            f'<p style="margin:12px 0;line-height:1.9;font-size:15px;">{line}</p>'
        )

    return "\n".join(html_parts)


def process_inline(text):
    """处理行内格式：粗体等"""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def escape_html(text):
    """转义 HTML 特殊字符"""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


# ============== 草稿提交 ==============
def create_draft_json(md_path, thumb_media_id, digest=None):
    """从 Markdown 文件创建草稿 JSON"""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取主标题
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "无标题"

    # 提取第一段作为摘要
    if digest is None:
        paragraphs = [l.strip() for l in content.split("\n")
                      if l.strip() and not l.strip().startswith("#")
                      and not l.strip().startswith("##") and l.strip() != "---"]
        digest = paragraphs[0][:54] + "..." if paragraphs else ""

    html_content = md_to_wechat_html(content)

    draft = {
        "articles": [
            {
                "title": title,
                "author": "",
                "digest": digest,
                "content": html_content,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
        ]
    }

    print(f"📝 标题：{title}")
    print(f"📝 摘要：{digest[:50]}...")

    return draft


def submit_draft(token, draft):
    """提交草稿到公众号"""
    url = f"{API_BASE}/cgi-bin/draft/add"
    params = {"access_token": token}

    print("📤 提交草稿...")
    resp = requests.post(url, params=params, json=draft, timeout=30)
    data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        error_msg = data.get("errmsg", "未知错误")
        raise Exception(f"❌ 提交草稿失败：{error_msg}")

    media_id = data.get("media_id", "未知")
    print(f"✅ 草稿提交成功！")
    print(f"   media_id = {media_id}")
    return media_id


# ============== 主流程 ==============
def main():
    # 检查参数
    if len(sys.argv) < 3:
        print("""
📤 微信公众号一键发布

用法:
  python publish.py <文章.md路径> <封面图路径> [摘要]

示例:
  python publish.py my_article.md cover.png
  python publish.py my_article.md cover.png "这是一篇关于xxx的文章"

注意:
  1. 工作目录需包含 wechat_credentials.json
  2. 封面图需为 1280×720 分辨率，< 2MB
  3. 服务器 IP 112.8.202.216 需加入白名单
""")
        sys.exit(1)

    md_path = sys.argv[1]
    cover_path = sys.argv[2]
    digest = sys.argv[3] if len(sys.argv) > 3 else None

    # 验证文件
    if not os.path.exists(md_path):
        print(f"❌ 找不到文章文件：{md_path}")
        sys.exit(1)

    if not os.path.exists(cover_path):
        print(f"❌ 找不到封面图：{cover_path}")
        sys.exit(1)

    try:
        # Step 1: 读取凭证
        print("\n" + "=" * 40)
        print("📋 Step 1: 读取凭证")
        print("=" * 40)
        appid, appsecret = load_credentials()

        # Step 2: 获取 Token
        print("\n" + "=" * 40)
        print("📋 Step 2: 获取 Access Token")
        print("=" * 40)
        token = get_access_token(appid, appsecret)

        # Step 3: 上传封面图
        print("\n" + "=" * 40)
        print("📋 Step 3: 上传封面图")
        print("=" * 40)
        media_id = upload_permanent_material(token, cover_path)

        # Step 4: 创建草稿
        print("\n" + "=" * 40)
        print("📋 Step 4: 创建草稿")
        print("=" * 40)
        draft = create_draft_json(md_path, media_id, digest)

        # Step 5: 提交草稿
        print("\n" + "=" * 40)
        print("📋 Step 5: 提交草稿")
        print("=" * 40)
        submit_draft(token, draft)

        # 完成
        print("\n" + "🎉" * 20)
        print("✅ 发布成功！")
        print("🎉" * 20)
        print("\n请前往微信公众号后台 - 内容与互动 - 草稿箱 查看和编辑")

    except Exception as e:
        print(f"\n{'❌' * 20}")
        print(f"发布失败：{e}")
        print(f"{'❌' * 20}")
        sys.exit(1)


if __name__ == "__main__":
    main()
