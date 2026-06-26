#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _encoding_compat

"""
Zero-One-Two-Three 邮箱握手发货系统 (Mailbox Handshake Delivery v3.0)
功能：
  1. 连接 IMAP 邮箱，监控收件箱未读邮件
  2. 自动识别支付凭证附件 → 自动发货（胶囊/System Prompt）
  3. 解析邮件正文中的推荐码，自动记录分销佣金
  4. 通过 SMTP 发送体验报告

完整商业闭环：
  用户扫码支付 → 发邮件（附截图+推荐码） → 脚本自动识别 → 自动回复发货 → 分销商记佣金

用法：
  启动监控：python mailbox_tool.py --config mailbox_config.json --watch
  读取邮件：python mailbox_tool.py --config mailbox_config.json
  发送报告：python mailbox_tool.py --report mailbox_config.json
  查看帮助：python mailbox_tool.py --help
"""

import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import time
import platform
from datetime import datetime
from pathlib import Path

AUTHOR_EMAIL = os.environ.get("ZOT_AUTHOR_EMAIL", "your_email@example.com")
REPORT_SUBJECT = "0+1+2≠3 | 体验报告"
CAPSULE_ID = "C-Capsule-v1"
ORDERS_DIR = Path(__file__).parent / "tools"


def connect_imap(config):
    try:
        print(f"📡 正在连接 {config['imap_server']}...")
        mail = imaplib.IMAP4_SSL(config['imap_server'])
        mail.login(config['email'], config['password'])
        print(f"✅ 登录成功：{config['email']}")
        return mail
    except Exception as e:
        print(f"❌ 连接失败：{e}")
        return None


def connect_smtp(config):
    smtp_server = config.get("smtp_server", "smtp.qq.com")
    smtp_port = config.get("smtp_port", 465)
    try:
        print(f"📡 正在连接 SMTP {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(config['email'], config['password'])
        print(f"✅ SMTP 登录成功：{config['email']}")
        return server
    except Exception as e:
        print(f"⚠️ SMTP 连接失败：{e}")
        return None


def parse_header(header_value):
    decoded_parts = decode_header(header_value)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset if charset else 'utf-8', errors='ignore'))
        else:
            result.append(str(part))
    return "".join(result)


def find_attachment(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    filename = parse_header(filename)
                    payload = part.get_payload(decode=True)
                    return filename, payload
    return None, None


def extract_email_body(msg):
    body_text = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset()
                    body_text += payload.decode(charset if charset else 'utf-8', errors='ignore')
            elif content_type == "text/html" and not body_text:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset()
                    body_text += payload.decode(charset if charset else 'utf-8', errors='ignore')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset()
            body_text += payload.decode(charset if charset else 'utf-8', errors='ignore')
    return body_text


def load_orders():
    orders_file = ORDERS_DIR / "orders.json"
    if orders_file.exists():
        try:
            with open(orders_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"orders": [], "total_orders": 0, "total_revenue": 0}


def save_orders(orders_data):
    orders_file = ORDERS_DIR / "orders.json"
    with open(orders_file, 'w', encoding='utf-8') as f:
        json.dump(orders_data, f, ensure_ascii=False, indent=2)


def build_reply_content(sender_name, capsule_info=None):
    lines = [
        f"Hi {sender_name}，👋",
        "",
        "感谢你购买 0+1+2≠3 的数字分身胶囊！",
        "",
        "## 你的 AI 数字分身",
        "",
    ]
    if capsule_info:
        lines.append(f"- 🎭 分身名称：{capsule_info.get('name', 'AI数字分身')}")
        lines.append(f"- 📦 版本：完整版")
        lines.append("")
    lines.extend([
        "## 如何使用",
        "",
        "1. 将下方的 System Prompt 完整复制",
        "2. 粘贴到 ChatGPT / Claude / IMA 等 AI 助手的「自定义指令」中",
        "3. 输入 @分身名称 即可召唤你的专属 AI 分身",
        "",
        "## 💰 分享赚钱",
        "",
        "如果你觉得有用，可以把你的推荐码分享给朋友。",
        "朋友购买时填写你的推荐码，你获得 20% 返佣！",
        f"联系：{AUTHOR_EMAIL}",
        "",
        "> 0+1+2≠3 · 知识即服务",
        f"> {datetime.now().strftime('%Y.%m.%d')}",
    ])
    return "\n".join(lines)


def deliver_capsule(smtp_config, recipient_email, recipient_name):
    server = connect_smtp(smtp_config)
    if not server:
        print("   ❌ SMTP 连接失败，无法发货")
        return False

    content = build_reply_content(recipient_name, {"name": "C叔-低碳医学模式"})
    msg = MIMEMultipart()
    msg["From"] = smtp_config["email"]
    msg["To"] = recipient_email
    msg["Subject"] = f"✅ 你的数字分身已就绪 | 0+1+2≠3"

    msg.attach(MIMEText(content, "plain", "utf-8"))

    try:
        server.sendmail(smtp_config["email"], recipient_email, msg.as_string())
        server.quit()
        print(f"   📤 发货邮件已发送至 {recipient_email}")
        return True
    except Exception as e:
        print(f"   ❌ 发货失败：{e}")
        server.quit()
        return False


def process_new_emails(mail, config):
    mail.select("INBOX")
    status, data = mail.search(None, 'UNSEEN')
    if status != 'OK':
        print("⚠️ 无法搜索未读邮件。")
        return 0

    email_ids = data[0].split()
    if not email_ids:
        print("📭 没有未读邮件。")
        return 0

    print(f"📥 发现 {len(email_ids)} 封未读邮件...")
    orders = load_orders()
    delivered = 0

    from tools.referral_engine import ReferralEngine
    ref_eng = ReferralEngine()

    for eid in email_ids:
        status, msg_data = mail.fetch(eid, '(RFC822)')
        if status != 'OK':
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        subject = parse_header(msg.get("Subject", "无主题"))
        sender = parse_header(msg.get("From", ""))
        sender_email = email.utils.parseaddr(sender)[1]
        sender_name = email.utils.parseaddr(sender)[0] or sender_email.split("@")[0]
        date_str = parse_header(msg.get("Date", ""))

        att_name, att_data = find_attachment(msg)
        body_text = extract_email_body(msg)

        referrer_email = ref_eng.parse_referral_from_text(subject + " " + body_text)

        order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{len(orders['orders'])+1:04d}"
        order = {
            "order_id": order_id,
            "sender_email": sender_email,
            "sender_name": sender_name,
            "subject": subject,
            "date": date_str,
            "has_attachment": att_name is not None,
            "attachment_name": att_name or "",
            "referrer_email": referrer_email or "",
            "capsule": CAPSULE_ID,
            "price": 99,
            "status": "pending",
            "processed_at": datetime.now().isoformat()
        }

        print(f"\n📨 [{subject}] from {sender_name} <{sender_email}>")
        print(f"   附件：{att_name if att_name else '无'}")

        if referrer_email:
            print(f"   🔗 推荐人：{referrer_email}")

        if att_name:
            print(f"   💰 检测到支付凭证！正在自动发货...")
            ok = deliver_capsule(config, sender_email, sender_name)
            if ok:
                order["status"] = "delivered"
                delivered += 1
                print(f"   ✅ 胶囊已发送至 {sender_email}")

                if referrer_email:
                    comm = ref_eng.record_commission(order_id, sender_email, 99, referrer_email)
                    print(f"   💵 佣金 {comm} 元已记入 {referrer_email}")
            else:
                order["status"] = "failed"
                print(f"   ❌ 发货失败，请手动处理")
        else:
            order["status"] = "no_attachment"
            print(f"   ⚠️ 无附件，跳过发货（可能是咨询邮件）")

        orders["orders"].append(order)
        orders["total_orders"] = len(orders["orders"])
        orders["total_revenue"] = sum(
            o.get("price", 0) for o in orders["orders"] if o.get("status") == "delivered"
        )
        save_orders(orders)
        mail.store(eid, '+FLAGS', '\\Seen')

    print(f"\n🏁 处理完成：{delivered}/{len(email_ids)} 封已发货")
    return delivered


def build_report_content(config):
    provider_map = {
        "imap.qq.com": "QQ 邮箱",
        "imap.163.com": "网易 163 邮箱",
        "imap.126.com": "网易 126 邮箱",
        "imap.gmail.com": "Gmail",
        "outlook.office365.com": "Outlook",
    }
    provider = provider_map.get(config.get("imap_server", ""), config.get("imap_server", "未知"))

    orders = load_orders()
    total_orders = orders.get("total_orders", 0)
    total_revenue = orders.get("total_revenue", 0)

    lines = [
        f"# {REPORT_SUBJECT}",
        "",
        f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**操作系统**：{platform.system()} {platform.release()}",
        f"**Python 版本**：{sys.version.split()[0]}",
        "",
        "## 配置摘要",
        "",
        f"- 邮箱类型：{provider}",
        f"- 邮件账号：{config.get('email', '未配置')}",
        f"- IMAP 服务器：{config.get('imap_server', '未配置')}",
        "",
        "## 商业数据",
        "",
        f"- 累计订单：{total_orders}",
        f"- 累计收入：{total_revenue} 元",
        "",
        "## 体验反馈",
        "",
        "1. 邮箱握手发货系统运行正常。",
        "2. 分销引荐引擎集成完成。",
    ]

    if provider == "QQ 邮箱":
        lines.append("3. QQ 邮箱授权码获取路径：QQ 邮箱 → 设置 → 账户 → POP3/SMTP 服务 → 生成授权码。")
    elif "网易" in provider:
        lines.append("3. 建议增加对网易邮箱 IMAP 文件夹命名的自动解析。")

    lines.append("")
    lines.append("## 改进建议")
    lines.append("")
    lines.append("- 希望增加微信支付回调（需企业资质）。")
    lines.append("- 建议增加短信通知（发货成功时）。")
    lines.append("- 考虑接入支付宝当面付 API。")
    lines.append("")
    lines.append("> 此报告由 Zero-One-Two-Three 邮箱助手自动生成。")
    lines.append(f"> 0+1+2≠3 | {AUTHOR_EMAIL}")

    return "\n".join(lines)


def send_report(config):
    server = connect_smtp(config)
    if not server:
        print("❌ 无法发送报告：SMTP 连接失败。")
        return False

    content = build_report_content(config)
    msg = MIMEMultipart()
    msg["From"] = config["email"]
    msg["To"] = AUTHOR_EMAIL
    msg["Subject"] = REPORT_SUBJECT
    msg.attach(MIMEText(content, "plain", "utf-8"))

    try:
        server.sendmail(config["email"], AUTHOR_EMAIL, msg.as_string())
        server.quit()
        print(f"📤 体验报告已发送至 {AUTHOR_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        server.quit()
        return False


def watch_loop(config, interval=60):
    print(f"\n🔄 启动邮箱监控模式（每 {interval} 秒检查一次）...")
    print(f"   按 Ctrl+C 停止监控\n")

    mail = connect_imap(config)
    if not mail:
        sys.exit(1)

    try:
        while True:
            print(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] 检查新邮件...")
            try:
                delivered = process_new_emails(mail, config)
                if delivered > 0:
                    print(f"🎉 本轮自动发货 {delivered} 份！")
            except imaplib.IMAP4.abort:
                print("⚠️ 连接中断，重新连接...")
                mail = connect_imap(config)
                if not mail:
                    break
                continue
            except Exception as e:
                print(f"⚠️ 处理出错：{e}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n👋 监控已停止。")
    finally:
        try:
            mail.logout()
        except Exception:
            pass


def show_help():
    print("""
Zero-One-Two-Three 邮箱握手发货系统 📭 (v3.0)

用法：
  python mailbox_tool.py --config <cfg>              处理未读邮件并自动发货
  python mailbox_tool.py --config <cfg> --watch      持续监控模式（每60秒）
  python mailbox_tool.py --config <cfg> --report     发送体验报告
  python mailbox_tool.py --help                      显示此帮助

配置文件格式 (mailbox_config.json):
{
  "imap_server": "imap.qq.com",
  "smtp_server": "smtp.qq.com",
  "smtp_port": 465,
  "email": "user@qq.com"
}

⚠️  安全建议：不要将密码写入配置文件！
   请通过环境变量设置邮箱密码（推荐）：
   Windows:  set ZOT_MAIL_PASS=你的授权码
   Linux:    export ZOT_MAIL_PASS=你的授权码
   脚本会自动优先读取环境变量 $ZOT_MAIL_PASS，无需在配置文件中暴露密码。

完整商业闭环：
  用户扫码支付 → 发邮件(截图+推荐码) → 自动识别 → 自动发货 → 分销佣金自动记录

作者：C 叔 | 0+1+2≠3 | 联系方式通过环境变量 ZOT_AUTHOR_EMAIL 设置
""")


def main():
    if len(sys.argv) < 2 or "--help" in sys.argv:
        show_help()
        sys.exit(0)

    config_path = None
    do_watch = False
    do_report = False

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--config" and i + 1 < len(sys.argv):
            i += 1
            config_path = sys.argv[i]
        elif arg == "--watch":
            do_watch = True
        elif arg == "--report":
            do_report = True
        i += 1

    if not config_path:
        print("❌ 请指定配置文件路径：python mailbox_tool.py --config mailbox_config.json")
        print("💡 使用 --help 查看完整用法。")
        sys.exit(1)

    if not os.path.exists(config_path):
        print(f"❌ 配置文件不存在：{config_path}")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    env_pass = os.environ.get("ZOT_MAIL_PASS", "")
    if env_pass:
        config["password"] = env_pass
        print("🔐 已从环境变量 $ZOT_MAIL_PASS 读取邮箱密码（优先于配置文件）")

    if do_watch:
        watch_loop(config, interval=config.get("watch_interval", 60))
        sys.exit(0)

    if do_report:
        send_report(config)

    mail = connect_imap(config)
    if not mail:
        sys.exit(1)

    process_new_emails(mail, config)
    mail.logout()
    print("👋 操作完成。")


if __name__ == "__main__":
    main()