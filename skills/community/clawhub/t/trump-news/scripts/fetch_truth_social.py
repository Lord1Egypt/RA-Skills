#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过 truthbrush 客户端拉取 Truth Social 上指定用户（默认 @realDonaldTrump）的近期帖子。
需安装 truthbrush 并配置 TRUTHSOCIAL_USERNAME / TRUTHSOCIAL_PASSWORD 或 TRUTHSOCIAL_TOKEN。
"""
import os
import re
import sys
from datetime import datetime, timezone, timedelta

# 默认拉取特朗普官方账号；可通过环境变量 TRUTHSOCIAL_HANDLE 覆盖
DEFAULT_HANDLE = "realDonaldTrump"
# 只保留最近 N 天内的帖子
DAYS_BACK = 1


def strip_html(text):
    if not text:
        return ""
    return re.sub(r"<[^>]+>", " ", text).strip()


def fetch_truth_social_posts(handle=None, days_back=DAYS_BACK, max_posts=25):
    """
    使用 truthbrush 拉取用户最近帖子。
    返回 [(content_plain, created_at, url), ...]，失败返回 []。
    """
    try:
        import truthbrush as tb
    except ImportError:
        return [], "truthbrush 未安装，请执行: pip install truthbrush"

    username = os.environ.get("TRUTHSOCIAL_USERNAME")
    password = os.environ.get("TRUTHSOCIAL_PASSWORD")
    token = os.environ.get("TRUTHSOCIAL_TOKEN")
    if not token and not (username and password):
        return [], "未配置 Truth Social：请设置 TRUTHSOCIAL_USERNAME / TRUTHSOCIAL_PASSWORD 或 TRUTHSOCIAL_TOKEN"

    handle = handle or os.environ.get("TRUTHSOCIAL_HANDLE") or DEFAULT_HANDLE
    created_after = datetime.now(timezone.utc) - timedelta(days=days_back)

    try:
        api = tb.Api(username=username, password=password, token=token)
    except Exception as e:
        return [], f"Truth Social 登录失败: {e}"

    try:
        posts = []
        for post in api.pull_statuses(handle, replies=False, created_after=created_after):
            if len(posts) >= max_posts:
                break
            content = post.get("content") or ""
            created_at = post.get("created_at") or ""
            pid = post.get("id") or ""
            # Truth Social 帖子链接格式
            url = f"https://truthsocial.com/@{handle}/posts/{pid}" if pid else ""
            plain = strip_html(content)
            if plain:
                posts.append((plain[:500], created_at, url))
        return posts, None
    except Exception as e:
        return [], str(e)


def main():
    handle = os.environ.get("TRUTHSOCIAL_HANDLE") or DEFAULT_HANDLE
    posts, err = fetch_truth_social_posts(handle=handle, days_back=DAYS_BACK, max_posts=20)
    if err:
        print(f"## Truth Social (@{handle})", file=sys.stderr)
        print(f"*{err}*", file=sys.stderr)
        print("", file=sys.stderr)
        # 不退出，便于主脚本合并时仅跳过 Truth Social 块
        sys.exit(0)

    lines = [
        f"## Truth Social (@{handle})",
        "*特朗普个人首发阵地，重大声明第一出口（via truthbrush）*",
        "",
    ]
    for content, created_at, url in posts:
        lines.append(f"- **{content[:200]}{'…' if len(content) > 200 else ''}**")
        if created_at:
            lines.append(f"  Date: {created_at}")
        if url:
            lines.append(f"  Link: {url}")
        lines.append("")
    if not posts:
        lines.append("(近 24 小时无新帖。)")
        lines.append("")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
