#!/usr/bin/env python3
"""
content-engine 发布管理模块

支持将内容发布到 Twitter、LinkedIn、微信公众号、博客、Medium 等平台。
大部分发布功能为付费版功能。
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode

from utils import (
    check_subscription,
    format_platform_name,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    validate_platform,
    validate_status,
    write_json_file,
    PLATFORMS,
)


# ============================================================
# 数据文件路径
# ============================================================

CONTENTS_FILE = "contents.json"
ADAPTED_FILE = "adapted_contents.json"
PUBLISH_HISTORY_FILE = "publish_history.json"
SCHEDULE_FILE = "schedule.json"


def _get_contents() -> List[Dict[str, Any]]:
    """读取所有内容数据。"""
    return read_json_file(get_data_file(CONTENTS_FILE))


def _save_contents(contents: List[Dict[str, Any]]) -> None:
    """保存内容数据到文件。"""
    write_json_file(get_data_file(CONTENTS_FILE), contents)


def _find_content(contents: List[Dict], content_id: str) -> Optional[Dict]:
    """根据 ID 查找内容。"""
    for c in contents:
        if c.get("id") == content_id:
            return c
    return None


def _get_adapted() -> List[Dict[str, Any]]:
    """读取所有已适配内容。"""
    return read_json_file(get_data_file(ADAPTED_FILE))


def _get_publish_history() -> List[Dict[str, Any]]:
    """读取发布历史。"""
    return read_json_file(get_data_file(PUBLISH_HISTORY_FILE))


def _save_publish_history(history: List[Dict[str, Any]]) -> None:
    """保存发布历史。"""
    write_json_file(get_data_file(PUBLISH_HISTORY_FILE), history)


def _get_schedules() -> List[Dict[str, Any]]:
    """读取排期列表。"""
    return read_json_file(get_data_file(SCHEDULE_FILE))


def _save_schedules(schedules: List[Dict[str, Any]]) -> None:
    """保存排期列表。"""
    write_json_file(get_data_file(SCHEDULE_FILE), schedules)


# ============================================================
# 平台发布实现
# ============================================================

def _api_request(url: str, data: Any = None, headers: Optional[Dict] = None, method: str = "POST") -> Dict[str, Any]:
    """发送 HTTP API 请求。

    Args:
        url: 请求 URL。
        data: 请求数据（将转为 JSON）。
        headers: 请求头。
        method: HTTP 方法。

    Returns:
        响应数据字典。

    Raises:
        Exception: 请求失败时抛出。
    """
    if headers is None:
        headers = {}

    headers.setdefault("Content-Type", "application/json")

    body = None
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")

    req = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(req, timeout=30) as resp:
            resp_data = resp.read().decode("utf-8")
            return json.loads(resp_data) if resp_data else {}
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise Exception(f"HTTP {e.code}: {error_body}")
    except URLError as e:
        raise Exception(f"网络请求失败: {e.reason}")


def _publish_twitter(adapted: Dict[str, Any]) -> Dict[str, Any]:
    """发布到 Twitter (X)。

    使用 Twitter API v2，通过 Bearer Token 认证。

    Args:
        adapted: 已适配的 Twitter 内容。

    Returns:
        发布结果字典。
    """
    bearer_token = os.environ.get("CE_TWITTER_BEARER_TOKEN", "")
    if not bearer_token:
        return {
            "success": False,
            "error": "未配置 CE_TWITTER_BEARER_TOKEN 环境变量",
        }

    tweets = adapted.get("tweets", [])
    if not tweets:
        return {"success": False, "error": "无推文内容"}

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    tweet_ids = []
    reply_to_id = None

    for i, tweet_text in enumerate(tweets):
        payload = {"text": tweet_text}

        # Thread 模式: 后续推文作为回复
        if reply_to_id:
            payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}

        try:
            result = _api_request(
                "https://api.twitter.com/2/tweets",
                data=payload,
                headers=headers,
            )
            tweet_id = result.get("data", {}).get("id", "")
            tweet_ids.append(tweet_id)
            reply_to_id = tweet_id
        except Exception as e:
            return {
                "success": False,
                "error": f"第 {i + 1} 条推文发布失败: {str(e)}",
                "published_tweets": tweet_ids,
            }

    return {
        "success": True,
        "tweet_ids": tweet_ids,
        "tweet_count": len(tweet_ids),
        "url": f"https://twitter.com/i/status/{tweet_ids[0]}" if tweet_ids else "",
    }


def _publish_linkedin(adapted: Dict[str, Any]) -> Dict[str, Any]:
    """发布到 LinkedIn。

    使用 LinkedIn API，通过 Access Token 认证。

    Args:
        adapted: 已适配的 LinkedIn 内容。

    Returns:
        发布结果字典。
    """
    access_token = os.environ.get("CE_LINKEDIN_ACCESS_TOKEN", "")
    if not access_token:
        return {
            "success": False,
            "error": "未配置 CE_LINKEDIN_ACCESS_TOKEN 环境变量",
        }

    text = adapted.get("text", "")
    if not text:
        return {"success": False, "error": "无帖子内容"}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    # 获取用户 profile URN
    try:
        profile = _api_request(
            "https://api.linkedin.com/v2/me",
            headers={"Authorization": f"Bearer {access_token}"},
            method="GET",
        )
        person_urn = f"urn:li:person:{profile.get('id', '')}"
    except Exception as e:
        return {"success": False, "error": f"获取 LinkedIn 用户信息失败: {str(e)}"}

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }

    try:
        result = _api_request(
            "https://api.linkedin.com/v2/ugcPosts",
            data=payload,
            headers=headers,
        )
        post_id = result.get("id", "")
        return {
            "success": True,
            "post_id": post_id,
            "url": f"https://www.linkedin.com/feed/update/{post_id}" if post_id else "",
        }
    except Exception as e:
        return {"success": False, "error": f"LinkedIn 发布失败: {str(e)}"}


def _publish_wechat(adapted: Dict[str, Any]) -> Dict[str, Any]:
    """发布到微信公众号。

    使用微信公众号 API:
    1. 通过 appid + secret 获取 access_token
    2. 上传图文素材
    3. 发布文章

    Args:
        adapted: 已适配的微信公众号内容。

    Returns:
        发布结果字典。
    """
    appid = os.environ.get("CE_WECHAT_APPID", "")
    secret = os.environ.get("CE_WECHAT_SECRET", "")

    if not appid or not secret:
        return {
            "success": False,
            "error": "未配置 CE_WECHAT_APPID 和 CE_WECHAT_SECRET 环境变量",
        }

    # 第一步: 获取 access_token
    try:
        token_url = (
            f"https://api.weixin.qq.com/cgi-bin/token?"
            f"grant_type=client_credential&appid={appid}&secret={secret}"
        )
        req = Request(token_url, method="GET")
        with urlopen(req, timeout=30) as resp:
            token_data = json.loads(resp.read().decode("utf-8"))

        if "access_token" not in token_data:
            errcode = token_data.get("errcode", "unknown")
            errmsg = token_data.get("errmsg", "未知错误")
            return {"success": False, "error": f"获取 access_token 失败: {errcode} - {errmsg}"}

        access_token = token_data["access_token"]
    except Exception as e:
        return {"success": False, "error": f"获取微信 access_token 失败: {str(e)}"}

    # 第二步: 添加草稿（新版接口）
    title = adapted.get("title", "")
    html = adapted.get("html", "")
    digest = adapted.get("digest", "")
    author = adapted.get("author", "")

    article = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": html,
                "content_source_url": "",
                "thumb_media_id": "",
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }

    try:
        draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
        result = _api_request(draft_url, data=article)

        if "media_id" not in result:
            errcode = result.get("errcode", "unknown")
            errmsg = result.get("errmsg", "未知错误")
            return {"success": False, "error": f"创建草稿失败: {errcode} - {errmsg}"}

        media_id = result["media_id"]
    except Exception as e:
        return {"success": False, "error": f"创建微信草稿失败: {str(e)}"}

    # 第三步: 发布
    try:
        publish_url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
        pub_result = _api_request(publish_url, data={"media_id": media_id})

        publish_id = pub_result.get("publish_id", "")
        if pub_result.get("errcode", 0) != 0:
            errmsg = pub_result.get("errmsg", "未知错误")
            return {"success": False, "error": f"发布失败: {errmsg}", "media_id": media_id}

        return {
            "success": True,
            "media_id": media_id,
            "publish_id": publish_id,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"微信发布失败: {str(e)}",
            "media_id": media_id,
        }


def _publish_medium(adapted: Dict[str, Any]) -> Dict[str, Any]:
    """发布到 Medium。

    使用 Medium API，通过 Integration Token 认证。

    Args:
        adapted: 已适配的 Medium 内容。

    Returns:
        发布结果字典。
    """
    token = os.environ.get("CE_MEDIUM_TOKEN", "")
    if not token:
        return {
            "success": False,
            "error": "未配置 CE_MEDIUM_TOKEN 环境变量",
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # 获取用户 ID
    try:
        user_data = _api_request(
            "https://api.medium.com/v1/me",
            headers={"Authorization": f"Bearer {token}"},
            method="GET",
        )
        user_id = user_data.get("data", {}).get("id", "")
        if not user_id:
            return {"success": False, "error": "无法获取 Medium 用户信息"}
    except Exception as e:
        return {"success": False, "error": f"获取 Medium 用户信息失败: {str(e)}"}

    title = adapted.get("title", "")
    markdown = adapted.get("markdown", "")
    tags = adapted.get("tags", [])

    payload = {
        "title": title,
        "contentFormat": "markdown",
        "content": markdown,
        "tags": tags[:5],
        "publishStatus": "public",
    }

    try:
        result = _api_request(
            f"https://api.medium.com/v1/users/{user_id}/posts",
            data=payload,
            headers=headers,
        )
        post = result.get("data", {})
        return {
            "success": True,
            "post_id": post.get("id", ""),
            "url": post.get("url", ""),
        }
    except Exception as e:
        return {"success": False, "error": f"Medium 发布失败: {str(e)}"}


def _publish_blog(adapted: Dict[str, Any]) -> Dict[str, Any]:
    """发布到博客（写入本地文件系统）。

    根据 CE_BLOG_TYPE 和 CE_BLOG_PATH 写入 Markdown 文件。

    Args:
        adapted: 已适配的博客内容。

    Returns:
        发布结果字典。
    """
    blog_path = os.environ.get("CE_BLOG_PATH", "")
    if not blog_path:
        return {
            "success": False,
            "error": "未配置 CE_BLOG_PATH 环境变量（博客内容目录路径）",
        }

    blog_type = adapted.get("blog_type", "hugo")
    markdown = adapted.get("markdown", "")
    filename = adapted.get("suggested_filename", "untitled.md")

    # 确定写入目录
    if blog_type == "hugo":
        target_dir = os.path.join(blog_path, "content", "posts")
    elif blog_type == "jekyll":
        target_dir = os.path.join(blog_path, "_posts")
    elif blog_type == "hexo":
        target_dir = os.path.join(blog_path, "source", "_posts")
    else:
        target_dir = blog_path

    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        return {
            "success": True,
            "file_path": file_path,
            "blog_type": blog_type,
        }
    except IOError as e:
        return {"success": False, "error": f"写入博客文件失败: {str(e)}"}


# 平台发布器注册表
_PUBLISHERS = {
    "twitter": _publish_twitter,
    "linkedin": _publish_linkedin,
    "wechat": _publish_wechat,
    "medium": _publish_medium,
    "blog": _publish_blog,
}


# ============================================================
# 发布操作
# ============================================================

def publish_content(data: Dict[str, Any]) -> None:
    """发布内容到指定平台。

    必填字段: id, platform

    Args:
        data: 包含内容 ID 和目标平台的字典。
    """
    if not require_paid_feature("auto_publish", "自动发布"):
        return

    content_id = data.get("id")
    platform = data.get("platform", "")

    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    if not platform:
        output_error("目标平台（platform）为必填字段", code="VALIDATION_ERROR")
        return

    try:
        platform = validate_platform(platform)
    except ValueError as e:
        output_error(str(e), code="VALIDATION_ERROR")
        return

    # 查找已适配的内容
    adapted_list = _get_adapted()
    adapted = None
    for a in adapted_list:
        if a.get("content_id") == content_id and a.get("platform") == platform:
            adapted = a
            break

    if not adapted:
        output_error(
            f"未找到内容 {content_id} 在 {format_platform_name(platform)} 的适配版本，"
            "请先执行 adapt 操作",
            code="NOT_FOUND",
        )
        return

    # 执行发布
    publisher = _PUBLISHERS.get(platform)
    if not publisher:
        output_error(f"暂不支持发布到: {platform}", code="UNSUPPORTED_PLATFORM")
        return

    result = publisher(adapted)

    # 记录发布历史
    history = _get_publish_history()
    record = {
        "id": generate_id("PH"),
        "content_id": content_id,
        "platform": platform,
        "platform_name": format_platform_name(platform),
        "result": result,
        "published_at": now_iso(),
    }
    history.append(record)
    _save_publish_history(history)

    # 更新内容状态和发布结果
    contents = _get_contents()
    content = _find_content(contents, content_id)
    if content and result.get("success"):
        content["status"] = "已发布"
        content["published_at"] = now_iso()
        if "publish_results" not in content:
            content["publish_results"] = {}
        content["publish_results"][platform] = result
        content["updated_at"] = now_iso()
        _save_contents(contents)

    if result.get("success"):
        output_success({
            "message": f"已成功发布到 {format_platform_name(platform)}",
            "publish_record": record,
        })
    else:
        output_error(
            f"发布到 {format_platform_name(platform)} 失败: {result.get('error', '未知错误')}",
            code="PUBLISH_FAILED",
        )


def schedule_content(data: Dict[str, Any]) -> None:
    """排期发布内容。

    必填字段: id, platform, scheduled_at（ISO 格式日期时间）

    Args:
        data: 包含内容 ID、平台和排期时间的字典。
    """
    if not require_paid_feature("schedule", "定时发布"):
        return

    content_id = data.get("id")
    platform = data.get("platform", "")
    scheduled_at = data.get("scheduled_at", "")

    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    if not platform:
        output_error("目标平台（platform）为必填字段", code="VALIDATION_ERROR")
        return

    if not scheduled_at:
        output_error("排期时间（scheduled_at）为必填字段", code="VALIDATION_ERROR")
        return

    try:
        platform = validate_platform(platform)
    except ValueError as e:
        output_error(str(e), code="VALIDATION_ERROR")
        return

    # 校验时间格式和合法性
    try:
        scheduled_dt = datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
        scheduled_dt = scheduled_dt.replace(tzinfo=None)
        if scheduled_dt <= datetime.now():
            output_error("排期时间必须是未来时间", code="VALIDATION_ERROR")
            return
    except ValueError:
        output_error("排期时间格式无效，请使用 ISO 格式（如 2026-03-20T10:00:00）", code="VALIDATION_ERROR")
        return

    # 检查内容是否存在
    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    # 创建排期记录
    schedules = _get_schedules()
    schedule = {
        "id": generate_id("SC"),
        "content_id": content_id,
        "platform": platform,
        "platform_name": format_platform_name(platform),
        "scheduled_at": scheduled_at,
        "status": "pending",
        "created_at": now_iso(),
    }
    schedules.append(schedule)
    _save_schedules(schedules)

    # 更新内容状态为"已排期"
    if content["status"] in ("草稿", "待审核"):
        content["status"] = "已排期"
        content["scheduled_at"] = scheduled_at
        content["updated_at"] = now_iso()
        _save_contents(contents)

    output_success({
        "message": f"已排期在 {scheduled_at} 发布到 {format_platform_name(platform)}",
        "schedule": schedule,
    })


def list_published(data: Optional[Dict[str, Any]] = None) -> None:
    """列出发布历史。

    可选过滤: platform, content_id, date_from, date_to

    Args:
        data: 可选的过滤条件字典。
    """
    history = _get_publish_history()

    if data:
        # 按平台过滤
        platform_filter = data.get("platform")
        if platform_filter:
            history = [h for h in history if h.get("platform") == platform_filter.lower()]

        # 按内容 ID 过滤
        content_id = data.get("content_id")
        if content_id:
            history = [h for h in history if h.get("content_id") == content_id]

        # 按日期范围过滤
        date_from = data.get("date_from", "")
        date_to = data.get("date_to", "")
        if date_from:
            history = [h for h in history if h.get("published_at", "") >= date_from]
        if date_to:
            history = [h for h in history if h.get("published_at", "") <= date_to + "T23:59:59"]

    # 按发布时间倒序
    history.sort(key=lambda h: h.get("published_at", ""), reverse=True)

    # 统计
    success_count = sum(1 for h in history if h.get("result", {}).get("success"))
    fail_count = len(history) - success_count

    platform_stats = {}
    for p in PLATFORMS:
        count = sum(1 for h in history if h.get("platform") == p)
        if count > 0:
            platform_stats[format_platform_name(p)] = count

    output_success({
        "total": len(history),
        "success_count": success_count,
        "fail_count": fail_count,
        "platform_stats": platform_stats,
        "history": history,
    })


def unpublish_content(data: Dict[str, Any]) -> None:
    """撤回已发布的内容（标记为已归档）。

    必填字段: id

    注意: 此操作仅更新本地状态，不会从平台上删除已发布的内容。

    Args:
        data: 包含内容 ID 的字典。
    """
    content_id = data.get("id")
    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    if content["status"] != "已发布":
        output_error(
            f"只能撤回已发布的内容，当前状态为「{content['status']}」",
            code="INVALID_STATUS",
        )
        return

    content["status"] = "已归档"
    content["updated_at"] = now_iso()
    _save_contents(contents)

    output_success({
        "message": f"内容已标记为归档（注意：已发布到平台的内容需手动删除）",
        "content_id": content_id,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("content-engine 发布管理")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "publish": lambda: publish_content(data or {}),
        "schedule": lambda: schedule_content(data or {}),
        "list-published": lambda: list_published(data),
        "unpublish": lambda: unpublish_content(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
