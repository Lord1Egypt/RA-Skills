#!/usr/bin/env python3
"""
腾讯企业邮箱 - 收信、读取、搜索、附件下载脚本
使用 IMAP over SSL，服务器：imap.exmail.qq.com:993
"""

import os
import sys
import argparse
import imaplib
import email
import email.header
import email.utils
import json
import re
from pathlib import Path
from datetime import datetime

# ── 服务器配置 ────────────────────────────────────────────
IMAP_HOST = "imap.exmail.qq.com"
IMAP_PORT = 993  # SSL

# 海外用户备用（取消注释）
# IMAP_HOST = "hwimap.exmail.qq.com"


def get_credentials():
    address = os.environ.get("EXMAIL_ADDRESS")
    password = os.environ.get("EXMAIL_PASSWORD")
    if not address or not password:
        print("❌ 错误：请设置环境变量 EXMAIL_ADDRESS 和 EXMAIL_PASSWORD")
        sys.exit(1)
    return address, password


def connect_imap():
    """建立 IMAP SSL 连接并登录"""
    address, password = get_credentials()
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        mail.login(address, password)
        return mail
    except imaplib.IMAP4.error as e:
        print(f"❌ 连接/登录失败：{e}")
        print("   请检查邮箱地址和密码（绑定微信账号需使用客户端专用密码）")
        sys.exit(1)
    except ConnectionRefusedError:
        print(f"❌ 连接被拒绝：请检查网络，确认端口 {IMAP_PORT} 已开放")
        sys.exit(1)


def decode_header_value(value: str) -> str:
    """解码邮件头部（处理 Base64/QP 编码）"""
    if not value:
        return ""
    decoded_parts = email.header.decode_header(value)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            charset = charset or "utf-8"
            try:
                result.append(part.decode(charset, errors="replace"))
            except (LookupError, UnicodeDecodeError):
                result.append(part.decode("utf-8", errors="replace"))
        else:
            result.append(str(part))
    return "".join(result)


def get_email_body(msg) -> tuple[str, str]:
    """提取邮件正文，返回 (text, html)"""
    text_body = ""
    html_body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in content_disposition:
                continue
            charset = part.get_content_charset() or "utf-8"
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            try:
                decoded = payload.decode(charset, errors="replace")
            except (LookupError, UnicodeDecodeError):
                decoded = payload.decode("utf-8", errors="replace")

            if content_type == "text/plain" and not text_body:
                text_body = decoded
            elif content_type == "text/html" and not html_body:
                html_body = decoded
    else:
        charset = msg.get_content_charset() or "utf-8"
        payload = msg.get_payload(decode=True)
        if payload:
            try:
                body = payload.decode(charset, errors="replace")
            except (LookupError, UnicodeDecodeError):
                body = payload.decode("utf-8", errors="replace")
            if msg.get_content_type() == "text/html":
                html_body = body
            else:
                text_body = body

    return text_body, html_body


def list_attachments(msg) -> list[dict]:
    """列出邮件中的附件"""
    attachments = []
    for part in msg.walk():
        content_disposition = str(part.get("Content-Disposition", ""))
        if "attachment" in content_disposition or part.get_filename():
            filename = decode_header_value(part.get_filename() or "unnamed")
            attachments.append({
                "filename": filename,
                "content_type": part.get_content_type(),
                "size": len(part.get_payload(decode=True) or b""),
            })
    return attachments


def format_email_summary(uid: str, msg) -> dict:
    """格式化邮件摘要信息"""
    subject = decode_header_value(msg.get("Subject", "(无主题)"))
    from_ = decode_header_value(msg.get("From", ""))
    to_ = decode_header_value(msg.get("To", ""))
    date_str = msg.get("Date", "")
    flags = msg.get("X-Keywords", "")

    # 解析日期
    try:
        date_tuple = email.utils.parsedate(date_str)
        if date_tuple:
            dt = datetime(*date_tuple[:6])
            date_display = dt.strftime("%Y-%m-%d %H:%M")
        else:
            date_display = date_str
    except Exception:
        date_display = date_str

    attachments = list_attachments(msg)

    return {
        "uid": uid,
        "subject": subject,
        "from": from_,
        "to": to_,
        "date": date_display,
        "has_attachments": len(attachments) > 0,
        "attachment_count": len(attachments),
    }


# ── 操作函数 ─────────────────────────────────────────────

def action_list_folders():
    """列出所有文件夹"""
    mail = connect_imap()
    _, folders = mail.list()
    mail.logout()

    print("📁 邮箱文件夹列表：")
    for folder in folders:
        if isinstance(folder, bytes):
            folder = folder.decode("utf-8", errors="replace")
        # 提取文件夹名
        match = re.search(r'"([^"]+)"$|(\S+)$', folder)
        if match:
            name = match.group(1) or match.group(2)
            print(f"   {name}")


def action_list(folder: str, limit: int, unread_only: bool):
    """列出收件箱邮件"""
    mail = connect_imap()

    # 选择文件夹
    status, _ = mail.select(f'"{folder}"')
    if status != "OK":
        status, _ = mail.select(folder)
        if status != "OK":
            print(f"❌ 无法打开文件夹：{folder}")
            mail.logout()
            sys.exit(1)

    # 搜索
    search_criteria = "UNSEEN" if unread_only else "ALL"
    _, data = mail.search(None, search_criteria)
    uid_list = data[0].split() if data[0] else []

    if not uid_list:
        label = "未读邮件" if unread_only else "邮件"
        print(f"📭 {folder} 中没有{label}")
        mail.logout()
        return

    # 取最新的 N 封
    recent_uids = uid_list[-limit:][::-1]  # 最新在前

    total = len(uid_list)
    label = "未读邮件" if unread_only else "邮件"
    print(f"📬 {folder} 共 {total} 封{label}，显示最新 {len(recent_uids)} 封：")
    print("─" * 70)

    for uid in recent_uids:
        _, msg_data = mail.fetch(uid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        summary = format_email_summary(uid.decode(), msg)

        attach_icon = "📎" if summary["has_attachments"] else "  "
        print(f"[{summary['uid']:>6}] {attach_icon} {summary['date']}  {summary['from'][:30]:<30}  {summary['subject'][:40]}")

    print("─" * 70)
    print(f"💡 使用 --action read --uid <UID> 读取邮件详情")
    mail.logout()


def action_read(uid: str, folder: str):
    """读取邮件详情"""
    mail = connect_imap()
    mail.select(f'"{folder}"' if " " in folder else folder)

    _, msg_data = mail.fetch(uid.encode(), "(RFC822)")
    if not msg_data or msg_data[0] is None:
        print(f"❌ 找不到 UID={uid} 的邮件")
        mail.logout()
        sys.exit(1)

    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject = decode_header_value(msg.get("Subject", "(无主题)"))
    from_ = decode_header_value(msg.get("From", ""))
    to_ = decode_header_value(msg.get("To", ""))
    cc_ = decode_header_value(msg.get("Cc", ""))
    date_ = msg.get("Date", "")
    text_body, html_body = get_email_body(msg)
    attachments = list_attachments(msg)

    print("=" * 70)
    print(f"主题：{subject}")
    print(f"发件人：{from_}")
    print(f"收件人：{to_}")
    if cc_:
        print(f"抄送：{cc_}")
    print(f"日期：{date_}")
    if attachments:
        print(f"附件（{len(attachments)} 个）：")
        for att in attachments:
            size_kb = att['size'] / 1024
            print(f"  📎 {att['filename']} ({size_kb:.1f} KB)")
    print("─" * 70)

    body = text_body or (re.sub(r"<[^>]+>", "", html_body) if html_body else "(无正文)")
    print(body.strip())
    print("=" * 70)

    if attachments:
        print(f"\n💡 使用 --action download-attachment --uid {uid} 下载附件")

    # 标记为已读
    mail.store(uid.encode(), "+FLAGS", "\\Seen")
    mail.logout()


def action_search(query: str, folder: str, limit: int):
    """搜索邮件"""
    mail = connect_imap()
    mail.select(f'"{folder}"' if " " in folder else folder)

    try:
        # 支持中文搜索（UTF-8 编码）
        _, data = mail.search("UTF-8", query.encode("utf-8"))
    except Exception:
        try:
            _, data = mail.search(None, query)
        except Exception as e:
            print(f"❌ 搜索失败：{e}")
            mail.logout()
            sys.exit(1)

    uid_list = data[0].split() if data[0] else []

    if not uid_list:
        print(f"🔍 未找到匹配的邮件：{query}")
        mail.logout()
        return

    recent_uids = uid_list[-limit:][::-1]
    print(f"🔍 搜索「{query}」：共找到 {len(uid_list)} 封，显示最新 {len(recent_uids)} 封：")
    print("─" * 70)

    for uid in recent_uids:
        _, msg_data = mail.fetch(uid, "(RFC822.HEADER)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        summary = format_email_summary(uid.decode(), msg)

        attach_icon = "📎" if summary["has_attachments"] else "  "
        print(f"[{summary['uid']:>6}] {attach_icon} {summary['date']}  {summary['from'][:30]:<30}  {summary['subject'][:40]}")

    print("─" * 70)
    mail.logout()


def action_download_attachment(uid: str, folder: str, save_dir: str):
    """下载邮件附件"""
    mail = connect_imap()
    mail.select(f'"{folder}"' if " " in folder else folder)

    _, msg_data = mail.fetch(uid.encode(), "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    save_path = Path(save_dir).expanduser()
    save_path.mkdir(parents=True, exist_ok=True)

    saved = 0
    for part in msg.walk():
        content_disposition = str(part.get("Content-Disposition", ""))
        filename = part.get_filename()
        if not filename and "attachment" not in content_disposition:
            continue

        filename = decode_header_value(filename or "attachment")
        # 清理文件名
        filename = re.sub(r'[\\/*?:"<>|]', "_", filename)

        data = part.get_payload(decode=True)
        if data:
            file_path = save_path / filename
            with open(file_path, "wb") as f:
                f.write(data)
            size_kb = len(data) / 1024
            print(f"✅ 已保存：{file_path} ({size_kb:.1f} KB)")
            saved += 1

    if saved == 0:
        print("📭 该邮件没有附件")
    else:
        print(f"\n共下载 {saved} 个附件到：{save_path}")

    mail.logout()


def action_mark(uid: str, folder: str, flag: str, add: bool):
    """标记邮件状态"""
    mail = connect_imap()
    mail.select(f'"{folder}"' if " " in folder else folder)

    op = "+FLAGS" if add else "-FLAGS"
    mail.store(uid.encode(), op, flag)

    action = "已标记" if add else "已取消标记"
    flag_name = {"\\Seen": "已读", "\\Flagged": "星标", "\\Deleted": "删除"}.get(flag, flag)
    print(f"✅ UID {uid} {action}为「{flag_name}」")
    mail.logout()


def action_move(uid: str, folder: str, target_folder: str):
    """移动邮件到其他文件夹"""
    mail = connect_imap()
    mail.select(f'"{folder}"' if " " in folder else folder)

    # COPY + DELETE
    target = f'"{target_folder}"' if " " in target_folder else target_folder
    result, _ = mail.copy(uid.encode(), target)
    if result == "OK":
        mail.store(uid.encode(), "+FLAGS", "\\Deleted")
        mail.expunge()
        print(f"✅ 邮件已移动到：{target_folder}")
    else:
        print(f"❌ 移动失败：{result}")
    mail.logout()


# ── 主入口 ───────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="腾讯企业邮箱收信工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
操作示例：
  # 查看收件箱（最新 20 封）
  python3 read_email.py --action list

  # 只看未读邮件
  python3 read_email.py --action list --unread-only

  # 读取邮件详情
  python3 read_email.py --action read --uid 1234

  # 搜索邮件
  python3 read_email.py --action search --query 'FROM "boss@company.com"'
  python3 read_email.py --action search --query 'SUBJECT "合同" UNSEEN'

  # 下载附件
  python3 read_email.py --action download-attachment --uid 1234 --save-dir ~/Downloads

  # 列出文件夹
  python3 read_email.py --action list-folders

  # 标记已读/未读
  python3 read_email.py --action mark-read --uid 1234
  python3 read_email.py --action mark-unread --uid 1234

  # 移动邮件
  python3 read_email.py --action move --uid 1234 --target-folder "Archived"
        """,
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["list", "read", "search", "download-attachment", "list-folders", "mark-read", "mark-unread", "move"],
        help="操作类型",
    )
    parser.add_argument("--folder", default="INBOX", help="邮箱文件夹（默认：INBOX）")
    parser.add_argument("--uid", help="邮件 UID")
    parser.add_argument("--limit", type=int, default=20, help="最大显示数量（默认：20）")
    parser.add_argument("--unread-only", action="store_true", help="只显示未读邮件")
    parser.add_argument("--query", help="搜索条件（IMAP 搜索语法）")
    parser.add_argument("--save-dir", default="~/Downloads", help="附件保存目录")
    parser.add_argument("--target-folder", help="目标文件夹（用于移动操作）")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.action == "list-folders":
        action_list_folders()

    elif args.action == "list":
        action_list(args.folder, args.limit, args.unread_only)

    elif args.action == "read":
        if not args.uid:
            print("❌ 请提供 --uid 参数")
            sys.exit(1)
        action_read(args.uid, args.folder)

    elif args.action == "search":
        if not args.query:
            print("❌ 请提供 --query 搜索条件")
            sys.exit(1)
        action_search(args.query, args.folder, args.limit)

    elif args.action == "download-attachment":
        if not args.uid:
            print("❌ 请提供 --uid 参数")
            sys.exit(1)
        action_download_attachment(args.uid, args.folder, args.save_dir)

    elif args.action == "mark-read":
        if not args.uid:
            print("❌ 请提供 --uid 参数")
            sys.exit(1)
        action_mark(args.uid, args.folder, "\\Seen", add=True)

    elif args.action == "mark-unread":
        if not args.uid:
            print("❌ 请提供 --uid 参数")
            sys.exit(1)
        action_mark(args.uid, args.folder, "\\Seen", add=False)

    elif args.action == "move":
        if not args.uid or not args.target_folder:
            print("❌ 请提供 --uid 和 --target-folder 参数")
            sys.exit(1)
        action_move(args.uid, args.folder, args.target_folder)
