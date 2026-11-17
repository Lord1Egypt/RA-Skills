"""get-new-messages 命令 — 增量消息查询，状态持久化到磁盘"""

import json
import os
import sqlite3
from contextlib import closing
from datetime import datetime

import click

from ..core.config import STATE_DIR
from ..core.contacts import get_contact_names
from ..core.db_cache import DBCache
from ..core.mask import mask_text
from ..core.messages import decompress_content, format_msg_type
from ..output.formatter import output

STATE_FILE = os.path.join(STATE_DIR, "last_check.json")


def _load_last_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_last_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, 'w', encoding="utf-8") as f:
        json.dump(state, f)


@click.command("new-messages")
@click.option("--format", "fmt", default="json", type=click.Choice(["json", "text"]), help="输出格式")
@click.option("--mask", is_flag=True, help="脱敏手机号/身份证/银行卡/邮箱后再输出")
@click.option("--clean", is_flag=True, help="输出后删除解密缓存（明文数据库），避免隐私残留")
@click.pass_context
def new_messages(ctx, fmt, mask, clean):
    """获取自上次调用以来的新消息

    \b
    示例:
      wechat-cli new-messages               # 首次: 返回未读消息并记录状态
      wechat-cli new-messages               # 再次: 仅返回新增消息
      wechat-cli new-messages --format text  # 纯文本输出
      wechat-cli new-messages --mask --clean  # 脱敏并退出即清缓存（自动化推荐）
    \b
    状态文件: ~/.wechat-cli/last_check.json (删除此文件可重置)
    """
    app = ctx.obj

    path = app.cache.get(os.path.join("session", "session.db"))
    if not path:
        click.echo("错误: 无法解密 session.db", err=True)
        ctx.exit(3)

    names = get_contact_names(app.cache, app.decrypted_dir)
    with closing(sqlite3.connect(path)) as conn:
        rows = conn.execute("""
            SELECT username, unread_count, summary, last_timestamp,
                   last_msg_type, last_msg_sender, last_sender_display_name
            FROM SessionTable
            WHERE last_timestamp > 0
            ORDER BY last_timestamp DESC
        """).fetchall()

    curr_state = {}
    for r in rows:
        username, unread, summary, ts, msg_type, sender, sender_name = r
        curr_state[username] = {
            'unread': unread, 'summary': summary, 'timestamp': ts,
            'msg_type': msg_type, 'sender': sender or '', 'sender_name': sender_name or '',
        }

    last_state = _load_last_state()

    if not last_state:
        # 首次调用：保存状态，返回未读
        _save_last_state({u: s['timestamp'] for u, s in curr_state.items()})

        unread_msgs = []
        for username, s in curr_state.items():
            if s['unread'] and s['unread'] > 0:
                display = names.get(username, username)
                is_group = '@chatroom' in username
                summary = s['summary']
                if isinstance(summary, bytes):
                    summary = decompress_content(summary, 4) or '(压缩内容)'
                if isinstance(summary, str) and ':\n' in summary:
                    summary = summary.split(':\n', 1)[1]
                if mask and isinstance(summary, str):
                    summary = mask_text(summary)
                time_str = datetime.fromtimestamp(s['timestamp']).strftime('%H:%M')
                unread_msgs.append({
                    'chat': display,
                    'username': username,
                    'is_group': is_group,
                    'unread': s['unread'],
                    'last_message': str(summary or ''),
                    'msg_type': format_msg_type(s['msg_type']),
                    'time': time_str,
                    'timestamp': s['timestamp'],
                })

        if fmt == 'json':
            output({'first_call': True, 'unread_count': len(unread_msgs), 'messages': unread_msgs}, 'json')
        else:
            if unread_msgs:
                lines = []
                for m in unread_msgs:
                    tag = " [群]" if m['is_group'] else ""
                    lines.append(f"[{m['time']}] {m['chat']}{tag} ({m['unread']}条未读): {m['last_message']}")
                output(f"当前 {len(unread_msgs)} 个未读会话:\n\n" + "\n".join(lines), 'text')
            else:
                output("当前无未读消息（已记录状态，下次调用将返回新消息）", 'text')
        if clean:
            DBCache.clear_cache()
        return

    # 后续调用：对比差异
    new_msgs = []
    for username, s in curr_state.items():
        prev_ts = last_state.get(username, 0)
        if s['timestamp'] > prev_ts:
            display = names.get(username, username)
            is_group = '@chatroom' in username
            summary = s['summary']
            if isinstance(summary, bytes):
                summary = decompress_content(summary, 4) or '(压缩内容)'
            if isinstance(summary, str) and ':\n' in summary:
                summary = summary.split(':\n', 1)[1]
            if mask and isinstance(summary, str):
                summary = mask_text(summary)

            sender_display = ''
            if is_group and s['sender']:
                sender_display = names.get(s['sender'], s['sender_name'] or s['sender'])

            new_msgs.append({
                'chat': display,
                'username': username,
                'is_group': is_group,
                'last_message': str(summary or ''),
                'msg_type': format_msg_type(s['msg_type']),
                'sender': sender_display,
                'time': datetime.fromtimestamp(s['timestamp']).strftime('%H:%M:%S'),
                'timestamp': s['timestamp'],
            })

    _save_last_state({u: s['timestamp'] for u, s in curr_state.items()})

    new_msgs.sort(key=lambda m: m['timestamp'])

    if fmt == 'json':
        output({'first_call': False, 'new_count': len(new_msgs), 'messages': new_msgs}, 'json')
    else:
        if not new_msgs:
            output("无新消息", 'text')
        else:
            lines = []
            for m in new_msgs:
                entry = f"[{m['time']}] {m['chat']}"
                if m['is_group']:
                    entry += " [群]"
                entry += f": {m['msg_type']}"
                if m['sender']:
                    entry += f" ({m['sender']})"
                entry += f" - {m['last_message']}"
                lines.append(entry)
            output(f"{len(new_msgs)} 条新消息:\n\n" + "\n".join(lines), 'text')

    if clean:
        DBCache.clear_cache()
