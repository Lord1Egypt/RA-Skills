#!/usr/bin/env python3
"""
WotoHub 收件箱查询 & 邮件操作

支持功能:
- 查询收件箱列表 (selInboxClaw)
- 查看邮件详情 (inboxDetailClaw/{id})
- 查看对话详情 (inboxDialogueClaw by chatId)
- 发送邮件 (writeMultipleEmailClaw)
- 定时发送邮件 (writeMultipleEmailClaw type=2)
- 保存草稿 (writeMultipleEmailClaw type=99)

API 路径: /email/*
"""
import argparse
import json
import sys
from datetime import datetime

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from config import (
    BASE_URL, INBOX_LIST_PATH, EMAIL_DETAIL_PATH, INBOX_DIALOGUE_PATH,
    SEND_EMAIL_PATH,
    email_detail_path, inbox_dialogue_path,
    send_email_path,
)
from common import get_token, request_json, print_json


def load_batch_payload(path: str) -> dict:
    raw = open(path, encoding="utf-8").read()
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("batch payload must be a JSON object")
    emails = data.get("emails")
    blogger_infos = data.get("bloggerInfos")
    if not isinstance(emails, list) or not isinstance(blogger_infos, list):
        raise ValueError("batch payload must contain emails[] and bloggerInfos[]")
    return data


# ── 收件箱列表 ────────────────────────────────────────────────────────────────

def list_inbox(token: str, current_page: int = 1, page_size: int = 20,
               blogger_name: str = "", subject: str = "", task_name: str = "",
               popularize_plan_name: str = "", is_read: int = 0, is_star: int = 0,
               is_reply: int = 0, tag_names: list[str] = None,
               time_range: int = 1, start_date: str = "", sent_mail: int = 0,
               email_addr: str = "", ai_email_scope: int = 0) -> dict:
    """
    分页查看收件箱列表

    timeRange: 1-近三月; 2-近六月; 3-全部
    isRead:    1-正常(未读); 2-已读
    isStar:    0-未标记; 1-已标记
    isReply:   0-未回复; 1-已回复
    sentMail:  0-系统邮箱; 1-企业邮箱
    aiEmailScope: 0-全部; 1-AI邮件; 2-非AI邮件
    """
    path = INBOX_LIST_PATH
    body = {
        "currentPage": current_page,
        "pageSize": page_size,
        "timeRange": time_range,
        "sentMail": sent_mail,
        "aiEmailScope": ai_email_scope,
    }
    if blogger_name:
        body["bloggerName"] = blogger_name
    if subject:
        body["subject"] = subject
    if task_name:
        body["taskName"] = task_name
    if popularize_plan_name:
        body["popularizePlanName"] = popularize_plan_name
    if is_read:
        body["isRead"] = is_read
    if is_star:
        body["isStar"] = is_star
    if is_reply:
        body["isReply"] = is_reply
    if tag_names:
        body["tagName"] = tag_names
    if start_date:
        body["startDate"] = start_date
    if email_addr:
        body["email"] = email_addr

    return request_json("POST", path, token=token, payload=body)


def inbox_list_cli(args):
    token = get_token(feature="inbox_list")
    sent_mail = 1 if args.sent_mail else 0
    result = list_inbox(
        token,
        current_page=args.page,
        page_size=args.page_size,
        blogger_name=args.blogger_name or "",
        subject=args.subject or "",
        is_read=args.is_read or 0,
        is_star=args.is_star or 0,
        is_reply=args.is_reply or 0,
        time_range=args.time_range or 1,
        sent_mail=sent_mail,
        ai_email_scope=args.ai_scope or 0,
    )
    print_json(result)
    return result


# ── 邮件详情 ─────────────────────────────────────────────────────────────────

def get_email_detail(token: str, email_id: int) -> dict:
    """查看收件箱详情"""
    path = email_detail_path().replace("{id}", str(email_id))
    return request_json("GET", path, token=token)


def email_detail_cli(args):
    token = get_token(feature="inbox_detail")
    result = get_email_detail(token, args.email_id)
    print_json(result)
    return result


# ── 对话详情 ─────────────────────────────────────────────────────────────────

def get_dialogue(token: str, chat_id: str) -> dict:
    """查看收件箱对话详情 (by chatId)"""
    path = INBOX_DIALOGUE_PATH
    body = {
        "chatId": chat_id,
    }
    return request_json("POST", path, token=token, payload=body)


def dialogue_cli(args):
    token = get_token(feature="inbox_dialogue")
    result = get_dialogue(token, args.chat_id)
    print_json(result)
    return result


# ── 发送邮件 ─────────────────────────────────────────────────────────────────

def send_email(token: str,
               emails: list[dict], blogger_infos: list[dict],
               mail_type: int = 1, timing: str = "",
               reply_id: int = 0, is_reply_all: bool = False,
               cc: str = "",
               task_id: int = 0, nick_name: str = "") -> dict:
    """
    发送或定时发送邮件

    mailType: 1-普通邮件; 2-定时邮件; 3-Gmail代发; 99-草稿
    timing:   定时发送时间，格式 yyyy-MM-dd HH:mm:ss（mailType=2 时必填）

    emails 数组元素:
        frontId:       前端预先生成的邮件id
        templateId:     模版id
        id:            写信ID
        subject:       主题
        content:       正文
        attachments:   附件列表 [{link, size, name, uuid}]
        bloggerIds:    该邮件对应的博主ID列表

    bloggerInfos 数组元素:
        bloggerId:         博主id
        chooseSource:       添加来源，默认0
        popularizePlanId:   推广计划id，无推广计划默认-1
        popularizePlanName: 推广计划名称
        isFiltered:         是否过滤，默认false
    """
    path = SEND_EMAIL_PATH
    body = {
        "emails": emails,
        "bloggerInfos": blogger_infos,
        "type": mail_type,
        "taskId": task_id,
    }
    if timing:
        body["timing"] = timing
    if reply_id:
        body["replyId"] = reply_id
    if is_reply_all:
        body["isReplyAll"] = is_reply_all
    if cc:
        body["cc"] = cc
    if nick_name:
        body["nickName"] = nick_name

    return request_json("POST", path, token=token, payload=body)


def send_email_cli(args):
    token = get_token(feature="send_email")

    if args.emails_file:
        payload = load_batch_payload(args.emails_file)
        result = send_email(
            token,
            emails=payload.get("emails", []),
            blogger_infos=payload.get("bloggerInfos", []),
            mail_type=2 if args.timing else 1,
            timing=args.timing or payload.get("timing", ""),
            reply_id=args.reply_id or payload.get("replyId", 0),
            task_id=args.task_id if args.task_id is not None else payload.get("taskId", 0),
            is_reply_all=bool(payload.get("isReplyAll", False)),
            cc=payload.get("cc", ""),
            nick_name=payload.get("nickName", ""),
        )
        print_json(result)
        return result

    emails = []
    blogger_infos = []

    blogger_ids = args.blogger_ids or []
    if isinstance(blogger_ids, str):
        blogger_ids = [b.strip() for b in blogger_ids.split(",") if b.strip()]

    # bloggerId 应取搜索结果中的 besId（完整博主ID），例如 "6937155518503257094ttfe56"
    # 调用方需传入 besId 而非昵称/用户名
    for bid in blogger_ids:
        emails.append({
            "subject": args.subject or "Partnership Opportunity",
            "content": args.content or "",
            "bloggerIds": [bid],
        })
        blogger_infos.append({
            "bloggerId": bid,   # besId from search results
            "chooseSource": 0,
            "popularizePlanId": -1,
        })

    result = send_email(
        token,
        emails=emails,
        blogger_infos=blogger_infos,
        mail_type=2 if args.timing else 1,
        timing=args.timing or "",
        reply_id=args.reply_id or 0,
        task_id=args.task_id or 0,
    )
    print_json(result)
    return result


# ── 回复邮件 ─────────────────────────────────────────────────────────────────

def reply_email_cli(args):
    """回复某封邮件（通过 inbox dialogue 查到的邮件ID）"""
    token = get_token(feature="reply_email")

    emails = []
    blogger_infos = []

    blogger_ids = args.blogger_ids or []
    if isinstance(blogger_ids, str):
        blogger_ids = [b.strip() for b in blogger_ids.split(",") if b.strip()]
    if len(blogger_ids) != 1:
        raise ValueError("reply requires exactly one bloggerId for a single replyId")

    for bid in blogger_ids:
        emails.append({
            "subject": args.subject or "",
            "content": args.content or "",
        })
        blogger_infos.append({
            "bloggerId": bid,
            "chooseSource": 0,
            "popularizePlanId": -1,
        })

    result = send_email(
        token,
        emails=emails,
        blogger_infos=blogger_infos,
        mail_type=1,
        reply_id=args.reply_id,
        is_reply_all=args.reply_all,
    )
    print_json(result)
    return result


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="WotoHub 收件箱 & 邮件操作")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # list
    p = sub.add_parser("list", help="收件箱列表")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int, default=20)
    p.add_argument("--blogger-name", default="")
    p.add_argument("--subject", default="")
    p.add_argument("--is-read", type=int, default=0, choices=[0, 1, 2])
    p.add_argument("--is-star", type=int, default=0, choices=[0, 1])
    p.add_argument("--is-reply", type=int, default=0, choices=[0, 1])
    p.add_argument("--time-range", type=int, default=1, choices=[1, 2, 3])
    p.add_argument("--sent-mail", action="store_true", help="查询发件箱（默认查收件箱）")
    p.add_argument("--ai-scope", type=int, default=0, choices=[0, 1, 2])
    p.set_defaults(func=inbox_list_cli)

    # detail
    p = sub.add_parser("detail", help="邮件详情")
    p.add_argument("email_id", type=int)
    p.set_defaults(func=email_detail_cli)

    # dialogue
    p = sub.add_parser("dialogue", help="对话详情")
    p.add_argument("chat_id", type=str)
    p.set_defaults(func=dialogue_cli)

    # send
    p = sub.add_parser("send", help="发送邮件")
    p.add_argument("--blogger-ids",
                   help="博主 besId（搜索结果中的完整ID），多个用逗号分隔，不可传昵称或用户名")
    p.add_argument("--subject")
    p.add_argument("--content")
    p.add_argument("--emails-file", help="批量发送 payload JSON 文件，需包含 emails[] 与 bloggerInfos[]")
    p.add_argument("--timing", default="", help="定时发送时间，格式 yyyy-MM-dd HH:mm:ss")
    p.add_argument("--task-id", type=int, default=0)
    p.add_argument("--reply-id", type=int, default=0)
    p.set_defaults(func=send_email_cli)

    # reply
    p = sub.add_parser("reply", help="回复邮件")
    p.add_argument("--blogger-ids", required=True,
                   help="博主 besId（搜索结果中的完整ID），多个用逗号分隔，不可传昵称或用户名")
    p.add_argument("--reply-id", required=True, type=int, help="原邮件ID（回复哪封就填哪封的ID）")
    p.add_argument("--subject", required=True)
    p.add_argument("--content", required=True)
    p.add_argument("--reply-all", action="store_true", help="回复所有人（含抄送人）")
    p.set_defaults(func=reply_email_cli)

    args = parser.parse_args()
    if args.cmd == "send":
        if not args.emails_file:
            if not args.blogger_ids or not args.subject or not args.content:
                parser.error("send 需要 --emails-file，或同时提供 --blogger-ids --subject --content")
    if args.cmd == "reply":
        blogger_ids = [b.strip() for b in str(args.blogger_ids or "").split(",") if b.strip()]
        if len(blogger_ids) != 1:
            parser.error("reply 仅支持单个 --blogger-ids，单个 replyId 只能对应一个 bloggerId")
        args.blogger_ids = blogger_ids
    args.func(args)


if __name__ == "__main__":
    main()
