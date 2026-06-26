#!/usr/bin/env python3
"""
微信公众号评论自动回复脚本

功能：
- 扫描已发布文章的新评论
- 用 AI 生成风格化的回复
- 自动发送回复
- 记录已回复的评论，避免重复

用法：
  python3 comment_reply.py                # 扫描并回复
  python3 comment_reply.py --dry-run      # 只看不发
  python3 comment_reply.py --articles 5   # 扫描最近 5 篇（默认 10）
"""

import argparse
import json
import os
import re
import time
import requests
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR.parent / "config.json"
STATE_PATH = SCRIPT_DIR.parent / "comment_state.json"
LOG_PATH = SCRIPT_DIR.parent / "comment_reply.log"

# AI 回复的系统提示（请修改为你自己的公众号名称和风格）
SYSTEM_PROMPT = """你是微信公众号作者，负责回复读者评论。

要求：
- 先判断评论是否与文章内容相关；相关时简短准确回答，避免编造。
- 闲聊、感谢、反馈类评论保持自然、简洁、友好。
- 技术求助只给安全的排查方向；不索要密钥、隐私或账号信息。
- 不攻击具体个人或组织，不发布未经证实的判断。
- 不处理政治、医疗、法律、金融等高风险建议；必要时提示谨慎核实。
- 每条回复适合公开展示，通常 5-40 个中文字符。
- 避免连续重复同一句话。
"""


def log(msg):
    """写日志"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_state():
    if STATE_PATH.exists():
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"replied": {}}  # {mid_commentid: timestamp}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_access_token(wechat_config):
    resp = requests.get("https://api.weixin.qq.com/cgi-bin/token", params={
        "grant_type": "client_credential",
        "appid": wechat_config["app_id"],
        "secret": wechat_config["app_secret"]
    }).json()
    if "access_token" not in resp:
        raise Exception(f"Token 获取失败: {resp}")
    return resp["access_token"]


def get_published_articles(token, count=10):
    """获取已发布文章列表"""
    resp = requests.post(
        f"https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token={token}",
        json={"offset": 0, "count": count}
    ).json()

    articles = []
    for item in resp.get("item", []):
        for idx, news in enumerate(item.get("content", {}).get("news_item", [])):
            url = news.get("url", "")
            mid_match = re.search(r"mid=(\d+)", url)
            if mid_match and news.get("need_open_comment", 0) == 1:
                # 提取文章摘要，供 AI 回复文章相关问题
                digest = news.get("digest", "")
                # 如果有完整内容，提取纯文本摘要（前500字）
                content_html = news.get("content", "")
                if content_html:
                    import re as _re
                    text = _re.sub(r"<[^>]+>", "", content_html)
                    text = _re.sub(r"\s+", " ", text).strip()
                    digest = text[:500]
                articles.append({
                    "mid": int(mid_match.group(1)),
                    "index": idx,
                    "title": news.get("title", "无标题"),
                    "digest": digest,
                })
    return articles


def get_comments(token, mid, index=0):
    """获取文章评论"""
    resp = requests.post(
        f"https://api.weixin.qq.com/cgi-bin/comment/list?access_token={token}",
        data=json.dumps({
            "msg_data_id": mid,
            "index": index,
            "begin": 0,
            "count": 50,
            "type": 0
        })
    ).json()

    if resp.get("errcode", 0) != 0:
        return []
    return resp.get("comment", [])


def find_unreplied(comments, mid, state):
    """找出未回复的精选评论"""
    unreplied = []
    for c in comments:
        cid = c.get("user_comment_id", "")
        state_key = f"{mid}_{cid}"

        # 跳过已回复的（微信已回复 或 我们已处理过的）
        if c.get("reply", {}).get("content"):
            continue
        if state_key in state.get("replied", {}):
            continue
        # 只回复精选评论（comment_type == 1 表示精选）
        # 实测发现精选评论的 comment_type 不一定可靠，
        # 用 is_elected 字段或直接回复所有未回复的

        unreplied.append({
            "comment_id": cid,
            "content": c.get("content", ""),
            "state_key": state_key,
        })
    return unreplied


def generate_reply(comment_content, article_title, ai_config, article_digest=""):
    """用 AI 生成回复"""
    try:
        user_msg = f"文章标题：{article_title}\n"
        if article_digest:
            user_msg += f"文章内容摘要：{article_digest}\n"
        user_msg += f"\n读者评论：{comment_content}\n\n请生成回复："

        resp = requests.post(
            f"{ai_config['url']}/chat/completions",
            headers={
                "Authorization": f"Bearer {ai_config['key']}",
                "Content-Type": "application/json",
            },
            json={
                "model": ai_config.get("model", "google/gemini-2.5-flash"),
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg}
                ],
                "max_tokens": 150,
                "temperature": 0.7,
            },
            timeout=30,
        ).json()

        reply = resp.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        # 清理可能的引号包裹
        if reply.startswith('"') and reply.endswith('"'):
            reply = reply[1:-1]
        if reply.startswith("'") and reply.endswith("'"):
            reply = reply[1:-1]
        return reply
    except Exception as e:
        log(f"  AI 生成失败: {e}")
        return None


def send_reply(token, mid, index, comment_id, reply_content):
    """发送评论回复"""
    resp = requests.post(
        f"https://api.weixin.qq.com/cgi-bin/comment/reply/add?access_token={token}",
        data=json.dumps({
            "msg_data_id": mid,
            "index": index,
            "user_comment_id": comment_id,
            "content": reply_content,
        }, ensure_ascii=False).encode("utf-8")
    ).json()
    return resp.get("errcode", -1) == 0, resp


def main():
    parser = argparse.ArgumentParser(description="微信公众号评论自动回复")
    parser.add_argument("--dry-run", action="store_true", help="只生成回复，不发送")
    parser.add_argument("--articles", type=int, default=10, help="扫描最近几篇文章（默认 10）")
    args = parser.parse_args()

    log("=" * 40)
    log("评论自动回复启动")

    config = load_config()
    state = load_state()

    # AI 配置（从本技能 config.json 的 ai 字段读取，或环境变量 OPENROUTER_API_KEY）
    ai_section = config.get("ai", {})
    ai_config = {
        "url": ai_section.get("url", os.environ.get("OPENROUTER_URL", "https://openrouter.ai/api/v1")),
        "key": ai_section.get("api_key", os.environ.get("OPENROUTER_API_KEY", "")),
        "model": ai_section.get("model", "anthropic/claude-sonnet-4"),
    }

    # 获取 token
    try:
        token = get_access_token(config["wechat"])
        log("Token OK")
    except Exception as e:
        log(f"Token 失败: {e}")
        return

    # 获取文章
    articles = get_published_articles(token, count=args.articles)
    log(f"扫描 {len(articles)} 篇文章")

    total_replied = 0
    total_skipped = 0

    for article in articles:
        mid = article["mid"]
        title = article["title"]

        comments = get_comments(token, mid, article["index"])
        unreplied = find_unreplied(comments, mid, state)

        if not unreplied:
            continue

        log(f"\n📝 {title} ({len(unreplied)} 条待回复)")

        for item in unreplied:
            content = item["content"][:100]
            log(f"  💬 [{item['comment_id']}] {content}")

            # 生成回复
            reply = generate_reply(item["content"], title, ai_config, article_digest=article.get("digest", ""))
            if not reply:
                log(f"  ⚠️ 跳过（AI 生成失败）")
                total_skipped += 1
                continue

            log(f"  ↳ 回复: {reply}")

            if args.dry_run:
                log(f"  [dry-run] 未发送")
                continue

            # 发送回复
            ok, resp = send_reply(token, mid, article["index"], item["comment_id"], reply)
            if ok:
                log(f"  ✅ 发送成功")
                state["replied"][item["state_key"]] = datetime.now().isoformat()
                save_state(state)
                total_replied += 1
            else:
                log(f"  ❌ 发送失败: {resp}")
                total_skipped += 1

            # 避免请求太快
            time.sleep(1)

    log(f"\n完成：回复 {total_replied} 条，跳过 {total_skipped} 条")
    log("=" * 40)


if __name__ == "__main__":
    main()
