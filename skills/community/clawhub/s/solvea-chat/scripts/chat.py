"""
Solvea Chat CLI

用法:
    python chat.py --peer-id <用户标识> --message <用户消息>
    python chat.py --peer-id <用户标识> --reset
    python chat.py --mark-reset
    python chat.py --version

输出:
    成功: AI 回复内容打印到 stdout
    失败: 错误信息打印到 stderr，exit code 非 0
"""

__version__ = "0.5.3"
import argparse
import json
import logging
import sys
from pathlib import Path

from solvea_client import SolveaClient

_WORKSPACE_ROOT = Path(__file__).parents[3]
SESSIONS_FILE = _WORKSPACE_ROOT / "memory" / "solvea-sessions.json"
RESET_MARKER  = _WORKSPACE_ROOT / "memory" / "solvea-reset-pending"
LOG_FILE      = _WORKSPACE_ROOT / "memory" / "solvea-chat.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


def load_sessions() -> dict:
    if SESSIONS_FILE.is_file():
        return json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
    return {}


def save_sessions(sessions: dict) -> None:
    SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SESSIONS_FILE.write_text(
        json.dumps(sessions, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def do_mark_reset() -> None:
    """记录"下次 chat 时先清除 session"的标记，供 /reset 后的首条消息使用。"""
    RESET_MARKER.parent.mkdir(parents=True, exist_ok=True)
    RESET_MARKER.write_text("", encoding="utf-8")


def do_reset(peer_id: str) -> None:
    """清除指定用户的 Solvea session，下次对话将开启新会话。"""
    sessions = load_sessions()
    if peer_id in sessions:
        del sessions[peer_id]
        save_sessions(sessions)


def do_chat(peer_id: str, message: str) -> None:
    """发送消息并输出 AI 回复，自动处理 session 创建和失效重试。"""
    # 若存在 reset 标记，先清除该用户的 session，再正常 chat
    if RESET_MARKER.is_file():
        do_reset(peer_id)
        RESET_MARKER.unlink(missing_ok=True)

    client = SolveaClient()
    sessions = load_sessions()
    chat_id = sessions.get(peer_id)

    logging.info("chat peer_id=%s chat_id=%s message=%r", peer_id, chat_id, message)

    def _call(cid):
        try:
            result = client.chat(message=message, chat_id=cid)
            logging.debug("api result: %s", json.dumps(result, ensure_ascii=False))
            return result
        except Exception as e:
            logging.error("api error: %s", e)
            print(f"Error: failed to call Solvea API: {e}", file=sys.stderr)
            sys.exit(1)

    result = _call(chat_id)

    # session 失效：服务端返回无内容且我们传了 chat_id → 清掉重试
    if not result.get("content") and not result.get("handoff") and chat_id:
        logging.warning("session invalid, retrying without chat_id")
        sessions.pop(peer_id, None)
        save_sessions(sessions)
        result = _call(None)

    # 持久化服务端返回的 chat_id
    returned_chat_id = result.get("chatId")
    if returned_chat_id and returned_chat_id != sessions.get(peer_id):
        sessions[peer_id] = returned_chat_id
        save_sessions(sessions)

    action_type = result.get("type", "")
    content = result.get("content", "")

    if action_type == "MESSAGE" and content:
        print(content)
    elif result.get("handoff"):
        print("您的问题需要人工客服处理，正在为您转接...")
    elif action_type == "CONFUSED":
        print("抱歉，我暂时无法回答您的问题，请稍后再试或联系人工客服。")
    else:
        logging.error("unexpected result: %s", json.dumps(result, ensure_ascii=False))
        print("客服系统暂时无法响应，请稍后再试。", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solvea Chat CLI")
    subgroup = parser.add_mutually_exclusive_group(required=True)
    subgroup.add_argument("--version", action="store_true", help="显示版本号")
    subgroup.add_argument("--mark-reset", action="store_true",
                          help="记录 reset 标记，下次 chat 时自动清除 session")
    subgroup.add_argument("--peer-id", help="用户唯一标识，如 feishu:<open_id>")
    group = parser.add_argument_group("与 --peer-id 配合使用")
    mode = group.add_mutually_exclusive_group()
    mode.add_argument("--message", help="用户消息内容")
    mode.add_argument("--reset", action="store_true", help="清除该用户的 Solvea session")
    args = parser.parse_args()

    if args.version:
        print(f"solvea-chat {__version__}")
    elif args.mark_reset:
        do_mark_reset()
    elif args.peer_id:
        if args.reset:
            do_reset(args.peer_id)
        elif args.message:
            do_chat(peer_id=args.peer_id, message=args.message)
        else:
            parser.error("--peer-id 需要搭配 --message 或 --reset")
    else:
        parser.error("需要 --mark-reset 或 --peer-id")


if __name__ == "__main__":
    main()
