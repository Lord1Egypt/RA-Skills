#!/usr/bin/env python3
"""
社交媒体一键发布脚本
支持：掘金、知乎、微博
用法：
  python3 social_publisher.py --platform juejin --file article.md
  python3 social_publisher.py --all --file article.md
  python3 social_publisher.py --schedule "2026-03-21 10:00" --file article.md
"""

import json
import time
import argparse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Optional

W = Path(__file__).parent.parent
CONFIG_FILE = W / "config/social-publisher.json"
LOG_FILE = W / "memory/social-publish-log.jsonl"

# 平台配置
PLATFORMS = {
    "juejin": {
        "name": "掘金",
        "api": "https://api.juejin.cn",
        "max_length": 20000,
        "cookie_key": "juejin"
    },
    "zhihu": {
        "name": "知乎",
        "api": "https://www.zhihu.com/api",
        "max_length": 100000,
        "cookie_key": "zhihu"
    },
    "weibo": {
        "name": "微博",
        "api": "https://api.weibo.cn",
        "max_length": 2000,
        "cookie_key": "weibo"
    }
}


def load_config() -> dict:
    """加载配置"""
    if not CONFIG_FILE.exists():
        return {}
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def get_cookie(platform: str) -> Optional[str]:
    """获取平台 Cookie"""
    config = load_config()
    return config.get(platform, {}).get("cookie")


def read_article(file_path: Path) -> tuple[str, str]:
    """读取文章内容"""
    if file_path.suffix == ".json":
        data = json.loads(file_path.read_text(encoding="utf-8"))
        title = data.get("title", file_path.stem)
        content = data.get("content_markdown", "") or data.get("markdown_content", "")
    else:
        text = file_path.read_text(encoding="utf-8").strip()
        lines = text.splitlines()
        title = lines[0].lstrip("#").strip() if lines else file_path.stem
        content = text
    return title, content


def adapt_content(content: str, platform: str) -> str:
    """适配内容到平台"""
    max_len = PLATFORMS[platform]["max_length"]
    if len(content) > max_len:
        return content[:max_len-50] + "\n\n...（内容过长，已截断）"
    return content


def publish_to_juejin(title: str, content: str, cookie: str) -> dict:
    """发布到掘金"""
    url = f"{PLATFORMS['juejin']['api']}/content_api/v1/article_draft/create"
    payload = {
        "title": title,
        "content": content,
        "category_id": "6809637773935378440",  # AI
        "tag_ids": ["6809640408797167623"],
        "brief_content": content[:200]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"err_no": -1, "err_msg": str(e)}


def publish_to_zhihu(title: str, content: str, cookie: str) -> dict:
    """发布到知乎（创建草稿）"""
    url = "https://www.zhihu.com/api/v4/articles"
    payload = {
        "title": title,
        "content": content,
        "draft": True,
        "can_reward": False
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0",
            "x-requested-with": "fetch"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read().decode("utf-8"))
            return {"err_no": 0, "data": resp} if "id" in resp else {"err_no": -1, "err_msg": resp.get("error", {}).get("message", "未知错误")}
    except Exception as e:
        return {"err_no": -1, "err_msg": str(e)}


def publish_to_weibo(content: str, cookie: str) -> dict:
    """发布到微博"""
    url = "https://api.weibo.cn/2/statuses/share.json"
    # 微博只支持短文本 + 图片
    text = content[:2000] if len(content) > 2000 else content
    
    req = urllib.request.Request(
        url,
        data=f"content={text}".encode("utf-8"),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read().decode("utf-8"))
            return {"err_no": 0, "data": resp} if "id" in resp else {"err_no": -1, "err_msg": resp.get("error", "未知错误")}
    except Exception as e:
        return {"err_no": -1, "err_msg": str(e)}


def log_publish(platform: str, title: str, result: dict):
    """记录发布日志"""
    log_entry = {
        "time": datetime.now().isoformat(),
        "platform": platform,
        "title": title,
        "result": result
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="社交媒体一键发布")
    parser.add_argument("--platform", choices=["juejin", "zhihu", "weibo"])
    parser.add_argument("--all", action="store_true", help="发布到所有平台")
    parser.add_argument("--file", required=True, help="文章文件路径")
    parser.add_argument("--schedule", help="定时发布时间")
    args = parser.parse_args()
    
    # 读取文章
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return
    
    title, content = read_article(file_path)
    
    # 定时发布
    if args.schedule:
        schedule_time = datetime.fromisoformat(args.schedule)
        wait_seconds = (schedule_time - datetime.now()).total_seconds()
        if wait_seconds > 0:
            print(f"⏰ 定时发布：{args.schedule}，等待 {wait_seconds:.0f} 秒")
            time.sleep(wait_seconds)
    
    # 确定发布平台
    platforms = ["juejin", "zhihu", "weibo"] if args.all else [args.platform]
    
    for platform in platforms:
        cookie = get_cookie(platform)
        if not cookie:
            print(f"⚠️ {PLATFORMS[platform]['name']} Cookie 未配置，跳过")
            continue
        
        adapted_content = adapt_content(content, platform)
        
        print(f"📤 发布到 {PLATFORMS[platform]['name']}...")
        
        if platform == "juejin":
            result = publish_to_juejin(title, adapted_content, cookie)
        elif platform == "zhihu":
            result = publish_to_zhihu(title, adapted_content, cookie)
        elif platform == "weibo":
            result = publish_to_weibo(adapted_content, cookie)
        
        if result.get("err_no") == 0:
            print(f"✅ {PLATFORMS[platform]['name']} 发布成功")
        else:
            print(f"❌ {PLATFORMS[platform]['name']} 发布失败: {result.get('err_msg')}")
        
        log_publish(platform, title, result)
        time.sleep(1)  # 避免频率限制


if __name__ == "__main__":
    main()