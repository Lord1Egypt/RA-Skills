#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wechat_push.py — 微信主动推送核心（v2）

不再裸调 ilink API（已被微信踢 / 网络层不通）。
走 OpenClaw 内部 message send CLI（用插件内部活跃长连接）。

用法（一般用户不直接调这个文件，由 bin/wechat-push 包一层）：
  python3 wechat_push.py "消息内容"
  python3 wechat_push.py --to <openid> "消息"
  python3 wechat_push.py --silent "消息"
  echo "消息" | python3 wechat_push.py --from-file

退出码：0=成功，1=失败

原理解释（v1 → v2 修复了什么）：
  v1 裸调 ilink sendmessage 用的是 5/31 老账号 token，session expired
  → 返 {"errcode":-14, "session timeout"} 或 {}
  → 只看 HTTP 200 = 假成功（消息根本没送达）

  v2 调 openclaw message send（OpenClaw 插件内部 CLI）
  → 走插件维护的 getupdates 长连接
  → ilink 接受（活跃 session）
  → 消息真送达用户手机微信
"""
import argparse
import os
import subprocess
import sys


# 通道配置（OpenClaw 内部）
CHANNEL = "openclaw-weixin"
DEFAULT_ACCOUNT = ""  # 公开版本不内置个人 bot；优先从配置/本机账号自动探测


def load_config():
    """从 ~/.config/wechat-push/config 读 openid/account（如果存在）"""
    config_paths = [
        os.path.expanduser("~/.config/wechat-push/config"),
        os.path.expanduser("~/.openclaw/skills/wechat-push-skill/config"),
    ]
    for p in config_paths:
        if os.path.exists(p):
            try:
                with open(p, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip('"').strip("'")
                            if k == "openid":
                                yield ("openid", v)
                            elif k == "account":
                                yield ("account", v)
            except Exception:
                pass


def get_default_target() -> str:
    """从配置文件读默认 openid。空值/占位符一律返 None（公开版本不内置个人 openid）。"""
    for k, v in load_config():
        if k == "openid":
            v = v.strip()
            if v and "<" not in v:  # 拒接占位符
                return v
    return None  # 不要再硬编码任何 openid


def detect_active_account(target_openid: str = None) -> str:
    """
    扫描 ~/.openclaw/openclaw-weixin/accounts/ 找"跟你有 context"的 bot。
    
    关键洞察：plugin 同时给多个用户轮询多个 bot，sync.json mtime 不区分
    "哪个 bot 跟你相关"。真正的活跃账号 = context_tokens 里有你 openid 那个。
    
    优先级：
      1. context_tokens 里有 target_openid 的 bot（你能发的）
      2. 多个 context match 时，取 sync.json mtime 最新的
      3. 都没 match → 返 DEFAULT_ACCOUNT（为空时要求用户先建立 context 或高级手动指定）
    
    返回格式：与 `openclaw message send --account` 期望一致（xxx-im-bot，带横线）。
    """
    import json as _json
    accounts_dir = os.path.expanduser("~/.openclaw/openclaw-weixin/accounts")
    if not os.path.isdir(accounts_dir):
        return DEFAULT_ACCOUNT

    # 1. 找 context_tokens 里有 target_openid 的 bot
    matches = []
    for f in os.listdir(accounts_dir):
        if not f.endswith("-im-bot.context-tokens.json"):
            continue
        bot_id = f.replace("-im-bot.context-tokens.json", "") + "-im-bot"
        path = os.path.join(accounts_dir, f)
        try:
            tokens = _json.load(open(path))
        except Exception:
            continue
        if target_openid and target_openid in tokens:
            sync_path = os.path.join(accounts_dir, bot_id + ".sync.json")
            sync_mtime = os.path.getmtime(sync_path) if os.path.exists(sync_path) else 0
            matches.append((sync_mtime, bot_id))
    
    if matches:
        matches.sort(reverse=True)
        return matches[0][1]  # 跟你有 context 且 sync 最新的 bot

    # 2. 降级：扫 sync.json mtime
    candidates = []
    for f in os.listdir(accounts_dir):
        if f.endswith("-im-bot.sync.json"):
            bot_id = f.replace(".sync.json", "")
            path = os.path.join(accounts_dir, f)
            mtime = os.path.getmtime(path)
            candidates.append((mtime, bot_id))
    if not candidates:
        # 3. 兜底：扫 token 文件
        for f in os.listdir(accounts_dir):
            if f.endswith("im-bot.json"):
                bot_id = f.replace("im-bot.json", "") + "-im-bot"
                path = os.path.join(accounts_dir, f)
                mtime = os.path.getmtime(path)
                candidates.append((mtime, bot_id))
        if not candidates:
            return DEFAULT_ACCOUNT
    candidates.sort(reverse=True)
    return candidates[0][1]


def get_default_account(target_openid: str = None) -> str:
    """从配置文件读默认 account，否则按 target_openid 探测活跃 bot。

    顺序：config > 按 target 探测（context_tokens 匹配）> 兜底（sync mtime）> DEFAULT_ACCOUNT
    """
    for k, v in load_config():
        if k == "account":
            v = v.strip()
            if v and "<" not in v:
                return v
    # 没有 config：按 target 自动探测
    detected = detect_active_account(target_openid)
    if detected:
        return detected
    return DEFAULT_ACCOUNT


def normalize_account(account: str) -> str:
    """把用户常见的短 id 归一化成 openclaw message send 需要的 xxx-im-bot。"""
    if not account:
        return account
    account = account.strip()
    if account.endswith("-im-bot"):
        return account
    return f"{account}-im-bot"


def send_via_openclaw(message: str, target: str, account: str, silent: bool = False) -> tuple:
    """
    调 openclaw message send 推消息
    返回 (success, detail)
    """
    if not message or not message.strip():
        return False, "empty message"

    if not target:
        return False, "no target openid (set in ~/.config/wechat-push/config)"
    if not account:
        return False, "no bot account found. Send a message to the bot first to establish context, then retry."

    account = normalize_account(account)

    cmd = [
        "openclaw", "message", "send",
        "--channel", CHANNEL,
        "--account", account,
        "--target", target,
        "-m", message,
    ]
    if silent:
        cmd.append("--silent")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return False, "openclaw message send timeout (20s)"
    except FileNotFoundError:
        return False, "openclaw CLI not found in PATH. Install OpenClaw first."

    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()

    # 成功判定：stdout 含 "Sent via" + 退出码 0
    if "Sent via" in stdout and result.returncode == 0:
        return True, stdout

    return False, f"exit={result.returncode} stdout={stdout[:200]} stderr={stderr[:200]}"


def main():
    parser = argparse.ArgumentParser(
        description="微信主动推送（v2：走 OpenClaw 内部 message send）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("text", nargs="?", help="消息内容")
    parser.add_argument("--text", dest="text_opt", help="消息内容（备选）")
    parser.add_argument("--to", default=None, help="目标 openid（默认从配置读）")
    parser.add_argument("--account", default=None, help="bot 账号（默认自动探测）")
    parser.add_argument("--silent", action="store_true", help="静默推送（不响通知）")
    parser.add_argument("--from-file", action="store_true", help="从 stdin 读消息")
    parser.add_argument("--dry-run", action="store_true", help="只打印将使用的配置，不发送")
    parser.add_argument("--detect-account", action="store_true",
                       help="只探测并打印活跃 bot 账号，不推送")

    args = parser.parse_args()

    if args.detect_account:
        # 如果传了 --to，用它做匹配；否则返 DEFAULT_ACCOUNT
        target_for_detect = args.to or get_default_target()
        print(detect_active_account(target_for_detect))
        sys.exit(0)

    target = args.to or get_default_target()
    account = normalize_account(args.account or get_default_account(target_openid=target))

    if args.from_file:
        text = sys.stdin.read().strip()
    elif args.text:
        text = args.text
    elif args.text_opt:
        text = args.text_opt
    else:
        parser.print_help()
        sys.exit(1)

    if not text:
        print("ERROR: message text cannot be empty", file=sys.stderr)
        sys.exit(1)

    if not target:
        print("ERROR: no target openid. Set 'openid=...' in ~/.config/wechat-push/config or use --to", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print("DRY RUN: no message sent")
        print(f"  channel: {CHANNEL}")
        print(f"  account: {account}")
        print(f"  target:  {target}")
        print(f"  silent:  {str(args.silent).lower()}")
        print(f"  text:    {text}")
        sys.exit(0)

    ok, detail = send_via_openclaw(text, target, account, silent=args.silent)
    if ok:
        print(f"SUCCESS: {detail}")
        sys.exit(0)
    else:
        print(f"ERROR: {detail}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
