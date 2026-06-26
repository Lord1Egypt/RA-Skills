#!/usr/bin/env python3
"""
腾讯企业邮箱 - 实时邮件监听脚本
使用 IMAP IDLE 协议，服务器推送新邮件通知，无需轮询。

依赖：pip3 install imapclient
"""

import os
import sys
import argparse
import time
import signal
import json
import email
import email.header
import email.utils
import threading
from datetime import datetime
from pathlib import Path

# ── 检查依赖 ─────────────────────────────────────────────
try:
    from imapclient import IMAPClient
    from imapclient.exceptions import IMAPClientError
except ImportError:
    print("❌ 缺少依赖库：imapclient")
    print("   请运行：pip3 install imapclient")
    sys.exit(1)

# ── 服务器配置 ────────────────────────────────────────────
IMAP_HOST = "imap.exmail.qq.com"
IMAP_PORT = 993

# 海外用户改用：
# IMAP_HOST = "hwimap.exmail.qq.com"

IDLE_TIMEOUT = 29 * 60   # 29 分钟重连一次（服务器通常 30 分钟超时）
RECONNECT_DELAY = 5       # 断线重连等待秒数


def get_credentials():
    address = os.environ.get("EXMAIL_ADDRESS")
    password = os.environ.get("EXMAIL_PASSWORD")
    if not address or not password:
        print("❌ 错误：请设置环境变量 EXMAIL_ADDRESS 和 EXMAIL_PASSWORD")
        sys.exit(1)
    return address, password


def decode_header_value(value: str) -> str:
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


def fetch_new_email(client: IMAPClient, uid: int) -> dict | None:
    """拉取新邮件的摘要信息"""
    try:
        messages = client.fetch([uid], ["ENVELOPE", "FLAGS", "RFC822.SIZE"])
        if uid not in messages:
            return None

        msg_data = messages[uid]
        envelope = msg_data.get(b"ENVELOPE")
        size = msg_data.get(b"RFC822.SIZE", 0)
        flags = msg_data.get(b"FLAGS", [])

        if envelope:
            subject = decode_header_value(
                envelope.subject.decode("utf-8", errors="replace") if isinstance(envelope.subject, bytes) else str(envelope.subject or "")
            )
            from_addr = ""
            if envelope.from_:
                addr = envelope.from_[0]
                name = decode_header_value(
                    addr.name.decode("utf-8", errors="replace") if isinstance(addr.name, bytes) else str(addr.name or "")
                )
                mailbox = addr.mailbox.decode() if isinstance(addr.mailbox, bytes) else str(addr.mailbox or "")
                host = addr.host.decode() if isinstance(addr.host, bytes) else str(addr.host or "")
                from_addr = f"{name} <{mailbox}@{host}>" if name else f"{mailbox}@{host}"

            date_str = str(envelope.date) if envelope.date else ""

            return {
                "uid": uid,
                "subject": subject,
                "from": from_addr,
                "date": date_str,
                "size_kb": round(size / 1024, 1),
                "is_unread": b"\\Seen" not in flags,
            }
    except Exception as e:
        print(f"⚠️  获取邮件信息失败 UID={uid}：{e}")
    return None


def format_notification(info: dict, folder: str) -> str:
    """格式化通知输出"""
    now = datetime.now().strftime("%H:%M:%S")
    lines = [
        f"\n{'='*60}",
        f"📬 [{now}] 新邮件到达！（文件夹：{folder}）",
        f"   主题：{info['subject']}",
        f"   发件人：{info['from']}",
        f"   时间：{info['date']}",
        f"   大小：{info['size_kb']} KB",
        f"   UID：{info['uid']}",
        f"{'='*60}",
        f"💡 使用以下命令读取：",
        f"   python3 read_email.py --action read --uid {info['uid']}",
    ]
    return "\n".join(lines)


def write_hook(info: dict, folder: str, hook_file: str):
    """将新邮件信息写入 JSON 文件（供其他程序消费）"""
    record = {
        "timestamp": datetime.now().isoformat(),
        "folder": folder,
        **info,
    }
    path = Path(hook_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    # 追加模式：保留历史
    records = []
    if path.exists():
        try:
            with open(path) as f:
                records = json.load(f)
        except Exception:
            records = []

    records.append(record)
    # 只保留最近 100 条
    records = records[-100:]

    with open(path, "w") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


class EmailWatcher:
    """IMAP IDLE 邮件监听器"""

    def __init__(self, folder: str, hook_file: str | None, quiet: bool):
        self.folder = folder
        self.hook_file = hook_file
        self.quiet = quiet
        self.running = True
        self.client: IMAPClient | None = None

    def connect(self) -> IMAPClient:
        address, password = get_credentials()
        client = IMAPClient(IMAP_HOST, port=IMAP_PORT, ssl=True)
        client.login(address, password)
        client.select_folder(self.folder)
        return client

    def handle_new_messages(self, uids: list[int]):
        """处理新到达的邮件"""
        for uid in uids:
            info = fetch_new_email(self.client, uid)
            if not info:
                continue

            if not self.quiet:
                print(format_notification(info, self.folder))

            if self.hook_file:
                write_hook(info, self.folder, self.hook_file)

    def run(self):
        """主循环：连接 → IDLE → 处理通知 → 循环"""
        address, _ = get_credentials()
        print(f"📡 腾讯企业邮箱实时监听启动")
        print(f"   账号：{address}")
        print(f"   文件夹：{self.folder}")
        print(f"   服务器：{IMAP_HOST}:{IMAP_PORT} (SSL)")
        if self.hook_file:
            print(f"   事件文件：{self.hook_file}")
        print(f"   按 Ctrl+C 停止\n")

        while self.running:
            try:
                print(f"🔌 正在连接...")
                self.client = self.connect()

                # 记录连接前的最大 UID
                msgs = self.client.search(["ALL"])
                last_uid = max(msgs) if msgs else 0
                print(f"✅ 连接成功，当前邮件数：{len(msgs)}，等待新邮件...\n")

                idle_start = time.time()

                while self.running:
                    # 进入 IDLE 模式
                    self.client.idle()

                    # 等待服务器推送，最长 IDLE_TIMEOUT 秒
                    responses = self.client.idle_check(timeout=IDLE_TIMEOUT)

                    # 退出 IDLE 模式
                    self.client.idle_done()

                    if not self.running:
                        break

                    # 检查是否有 EXISTS 或 RECENT 通知（新邮件）
                    has_new = any(
                        flag in (b"EXISTS", b"RECENT") or
                        (isinstance(flag, tuple) and len(flag) >= 2 and flag[1] in (b"EXISTS", b"RECENT"))
                        for item in responses
                        for flag in ([item] if not isinstance(item, (list, tuple)) else item)
                    )

                    # 简化检测：只要有响应就查询新 UID
                    if responses:
                        current_msgs = self.client.search(["ALL"])
                        new_uids = [uid for uid in current_msgs if uid > last_uid]

                        if new_uids:
                            self.handle_new_messages(new_uids)
                            last_uid = max(current_msgs) if current_msgs else last_uid

                    # 超时重连（防止服务器端超时断开）
                    if time.time() - idle_start > IDLE_TIMEOUT:
                        print(f"🔄 定期重连（每 {IDLE_TIMEOUT // 60} 分钟）")
                        break

            except KeyboardInterrupt:
                self.stop()
                break

            except (IMAPClientError, OSError, ConnectionError) as e:
                if self.running:
                    print(f"⚠️  连接断开：{e}")
                    print(f"   {RECONNECT_DELAY} 秒后重连...\n")
                    time.sleep(RECONNECT_DELAY)

            except Exception as e:
                if self.running:
                    print(f"❌ 未知错误：{e}")
                    print(f"   {RECONNECT_DELAY} 秒后重连...\n")
                    time.sleep(RECONNECT_DELAY)

            finally:
                if self.client:
                    try:
                        self.client.logout()
                    except Exception:
                        pass
                    self.client = None

        print("\n👋 监听已停止")

    def stop(self):
        self.running = False
        print("\n⏹  正在停止...")
        if self.client:
            try:
                self.client.idle_done()
            except Exception:
                pass


def parse_args():
    parser = argparse.ArgumentParser(
        description="腾讯企业邮箱实时监听（IMAP IDLE）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 监听收件箱，有新邮件时打印通知
  python3 watch_email.py

  # 监听指定文件夹
  python3 watch_email.py --folder "Starred"

  # 将新邮件信息写入 JSON 文件（供外部程序读取）
  python3 watch_email.py --hook-file ~/.openclaw/workspace/new_emails.json

  # 静默模式（只写文件，不打印）
  python3 watch_email.py --hook-file ~/new_emails.json --quiet
        """,
    )
    parser.add_argument("--folder", default="INBOX", help="监听的文件夹（默认：INBOX）")
    parser.add_argument(
        "--hook-file",
        help="新邮件到达时写入此 JSON 文件路径（供其他程序消费）",
        metavar="PATH",
    )
    parser.add_argument("--quiet", action="store_true", help="静默模式，不打印通知到终端")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    watcher = EmailWatcher(
        folder=args.folder,
        hook_file=args.hook_file,
        quiet=args.quiet,
    )

    # 注册信号处理
    def handle_signal(signum, frame):
        watcher.stop()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    watcher.run()
