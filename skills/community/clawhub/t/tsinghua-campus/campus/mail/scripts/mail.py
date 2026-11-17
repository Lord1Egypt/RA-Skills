"""mail.py — 邮件子 SKILL 统一入口

抽象收发邮件，配置从 mail.env 读取（同学填自己的 IMAP/SMTP/授权码）。
复用 email-accounts skill 的精华（IMAP 连接/标已读/SMTP 发件/formataddr）。

CLI:
  mail.py accounts                        → 列出配置的账户
  mail.py list [--account <name>] [--days N]  → 收件列表（默认近1天）
  mail.py read --account <name> --uid <uid>   → 读单封邮件
  mail.py send --from <name> --to <addr> --subject <主题> --body <正文> [--cc]
  mail.py mark-read --account <name> [--uid <uid>]  → 标已读（缺省全部）

配置: mail.env（同目录，见 mail.env.example）
"""
import sys
import os
import json
import imaplib
import smtplib
import argparse
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, parseaddr

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")


def _load_accounts():
    """从统一 .env 读取邮箱账户配置（MAIL_ACCOUNTS）。"""
    if not os.path.exists(ENV_PATH):
        common.output_json({"status": "error", "message": f"统一配置 {ENV_PATH} 不存在。请复制 skill/campus/.env.example 为 .env 并填写。"})
        sys.exit(1)
    try:
        with open(ENV_PATH, encoding="utf-8") as f:
            env = f.read()
        # 提取 MAIL_ACCOUNTS=[...]（支持 JSON 数组）
        start = env.find("MAIL_ACCOUNTS=")
        if start < 0:
            raise ValueError("MAIL_ACCOUNTS 未找到")
        arr = env[env.find("[", start):]
        depth = 0
        end = 0
        for i, ch in enumerate(arr):
            if ch == "[": depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        accounts = json.loads(arr[:end])
        if not accounts:
            raise ValueError("MAIL_ACCOUNTS 为空")
        return accounts
    except Exception as e:
        common.output_json({"status": "error", "message": f"统一 .env 解析失败（MAIL_ACCOUNTS）: {str(e)[:100]}"})
        sys.exit(1)


def _find_account(accounts, name):
    for a in accounts:
        if a.get("name") == name or (name and name in a.get("label", "")):
            return a
    common.output_json({"status": "error", "message": f"未找到账户 {name}。可用: {[a.get('name') for a in accounts]}"})
    sys.exit(1)


def _decode(s):
    """解码邮件头（RFC2047）。"""
    if not s:
        return ""
    parts = decode_header(s)
    out = []
    for text, charset in parts:
        if isinstance(text, bytes):
            try:
                out.append(text.decode(charset or "utf-8", "replace"))
            except Exception:
                out.append(text.decode("utf-8", "replace"))
        else:
            out.append(text)
    return "".join(out)


def _connect_imap(acc):
    imap = imaplib.IMAP4_SSL(acc["imap_host"], int(acc.get("imap_port", 993)), timeout=15)
    imap.login(acc["user"], acc["password"])
    return imap


def cmd_accounts():
    accounts = _load_accounts()
    common.output_json({"status": "ok", "type": "accounts",
                        "accounts": [{"name": a.get("name"), "label": a.get("label"), "user": a.get("user"),
                                      "imap": f"{a.get('imap_host')}:{a.get('imap_port')}",
                                      "smtp": f"{a.get('smtp_host')}:{a.get('smtp_port')}"} for a in accounts]})


def cmd_list(account_name, days):
    accounts = _load_accounts()
    acc = _find_account(accounts, account_name or accounts[0]["name"])
    try:
        imap = _connect_imap(acc)
    except Exception as e:
        common.output_json({"status": "error", "message": f"IMAP 连接失败: {str(e)[:100]}"})
        sys.exit(1)
    try:
        imap.select("INBOX")
        # 日期搜索（近 N 天）
        import datetime
        since = (datetime.date.today() - datetime.timedelta(days=days)).strftime("%d-%b-%Y")
        typ, data = imap.search(None, f'(SINCE "{since}")')
        ids = data[0].split()
        mails = []
        # 倒序（最新在前）
        for uid in reversed(ids[-50:]):
            typ2, msg_data = imap.fetch(uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if typ2 != "OK" or not msg_data or msg_data[0] is None:
                continue
            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)
            mails.append({
                "uid": uid.decode(),
                "from": _decode(msg.get("From", "")),
                "subject": _decode(msg.get("Subject", "")),
                "date": msg.get("Date", ""),
            })
        common.output_json({"status": "ok", "type": "list", "account": acc["name"],
                            "days": days, "mails": mails})
    finally:
        imap.logout()


def cmd_read(account_name, uid):
    accounts = _load_accounts()
    acc = _find_account(accounts, account_name)
    try:
        imap = _connect_imap(acc)
    except Exception as e:
        common.output_json({"status": "error", "message": f"IMAP 连接失败: {str(e)[:100]}"})
        sys.exit(1)
    try:
        imap.select("INBOX")
        typ, data = imap.fetch(uid.encode(), "(BODY.PEEK[])")
        if typ != "OK" or not data or data[0] is None:
            common.output_json({"status": "error", "message": f"邮件 {uid} 获取失败"})
            sys.exit(1)
        msg = email.message_from_bytes(data[0][1])
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
                    break
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", "replace")
        common.output_json({"status": "ok", "type": "read", "account": acc["name"],
                            "from": _decode(msg.get("From", "")), "to": _decode(msg.get("To", "")),
                            "subject": _decode(msg.get("Subject", "")), "date": msg.get("Date", ""),
                            "body": body[:3000]})
    finally:
        imap.logout()


def cmd_send(from_name, to, subject, body, cc=""):
    accounts = _load_accounts()
    acc = _find_account(accounts, from_name)
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = formataddr([acc.get("from_name", acc["user"]), acc["user"]], charset="utf-8")
        msg["To"] = to
        if cc:
            msg["Cc"] = cc
        msg["Subject"] = Header(subject, "utf-8")
        to_list = [to] + ([cc] if cc else [])
        if acc.get("smtp_ssl", True):
            server = smtplib.SMTP_SSL(acc["smtp_host"], int(acc.get("smtp_port", 465)), timeout=15)
        else:
            server = smtplib.SMTP(acc["smtp_host"], int(acc.get("smtp_port", 587)), timeout=15)
            server.starttls()
        server.login(acc["user"], acc["password"])
        server.sendmail(acc["user"], to_list, msg.as_string())
        server.quit()
        common.output_json({"status": "ok", "type": "send", "from": acc["user"], "to": to,
                            "subject": subject, "message": "发送成功"})
    except Exception as e:
        common.output_json({"status": "error", "message": f"发送失败: {str(e)[:100]}"})
        sys.exit(1)


def cmd_mark_read(account_name, uid):
    accounts = _load_accounts()
    acc = _find_account(accounts, account_name)
    try:
        imap = _connect_imap(acc)
    except Exception as e:
        common.output_json({"status": "error", "message": f"IMAP 连接失败: {str(e)[:100]}"})
        sys.exit(1)
    try:
        imap.select("INBOX")
        if uid:
            imap.store(uid.encode(), "+FLAGS", "\\Seen")
        else:
            typ, data = imap.search(None, "UNSEEN")
            ids = data[0].split()
            if ids:
                imap.store(b",".join(ids), "+FLAGS", "\\Seen")
        common.output_json({"status": "ok", "type": "mark_read", "account": acc["name"],
                            "message": f"已标已读（uid={'所有未读' if not uid else uid}）"})
    finally:
        imap.logout()


def main():
    ap = argparse.ArgumentParser(description="邮件子 SKILL")
    ap.add_argument("cmd", choices=["accounts", "list", "read", "send", "mark-read"])
    ap.add_argument("--account", default="", help="账户名（accounts 里的 name）")
    ap.add_argument("--days", type=int, default=1, help="list: 近 N 天（默认 1）")
    ap.add_argument("--uid", default="", help="read/mark-read: 邮件 uid")
    ap.add_argument("--from", dest="from_name", default="", help="send: 发件账户名")
    ap.add_argument("--to", default="", help="send: 收件人")
    ap.add_argument("--subject", default="", help="send: 主题")
    ap.add_argument("--body", default="", help="send: 正文")
    ap.add_argument("--cc", default="", help="send: 抄送")
    args = ap.parse_args()
    if args.cmd == "accounts":
        cmd_accounts()
    elif args.cmd == "list":
        cmd_list(args.account, args.days)
    elif args.cmd == "read":
        cmd_read(args.account, args.uid)
    elif args.cmd == "send":
        if not args.to or not args.subject or not args.body:
            common.output_json({"status": "error", "message": "send 需要 --to --subject --body"})
            sys.exit(1)
        cmd_send(args.from_name, args.to, args.subject, args.body, args.cc)
    elif args.cmd == "mark-read":
        cmd_mark_read(args.account, args.uid)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        common.log(f"[mail] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected", "message": f"脚本异常: {str(e)[:200]}"})
        sys.exit(1)
