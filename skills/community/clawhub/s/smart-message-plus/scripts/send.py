#!/usr/bin/env python3
"""smart-message-plus: unified CLI to send messages via DingTalk / Feishu.

Usage examples (see SKILL.md for full docs):
  send.py --provider dingtalk --to 13800000000 --msg "hello"
  send.py --provider feishu --to user@example.com --msg "hello"
  send.py --to 张三 --msg "hello"                      # contact alias
  send.py --chat-id 项目群 --msg "notice" --mention-all
  send.py --broadcast --department 技术部 --msg "notice" --dry-run
  send.py --recall <MSG_ID>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core import accounts as A
from core import config as C
from core import contacts as CT
from core import onboard as OB
from core import safety, sendlog, templates
from providers import org_lookup
from providers.base import NotSupported, Provider
from providers.dingtalk import DingTalkProvider
from providers.feishu import FeishuProvider
from providers.wecom import WeComProvider

PROVIDERS: dict[str, type[Provider]] = {
    "dingtalk": DingTalkProvider,
    "feishu": FeishuProvider,
    "wecom": WeComProvider,
}


def die(msg: str, code: int = 1):
    print(f"❌ {msg}")
    sys.exit(code)


def ok(msg: str):
    print(f"✅ {msg}")


# ---------------- account / contact management commands ----------------

def cmd_list_accounts():
    accs = A.list_accounts()
    if not accs:
        print("（无账号）用 --save-account 添加")
        return
    for a in accs:
        star = " ★默认" if a["is_default"] else ""
        print(f"  {a['slug']}  [{a['provider']}]  {a['name']}  key={a['key_masked']}{star}")


def cmd_save_account(args):
    creds = {
        "app_key": args.app_key or "",
        "app_secret": args.app_secret or "",
        "app_id": args.app_id or "",
        "robot_code": args.robot_code or "",
        "agent_id": args.agent_id or "",
    }
    # feishu uses app_id/app_secret; dingtalk uses app_key/app_secret
    if args.save_account[1] == "feishu":
        creds = {"app_id": creds["app_id"] or creds["app_key"], "app_secret": creds["app_secret"]}
    elif args.save_account[1] == "wecom":
        # webhook 模式：无必填凭证；--webhook-url 可作为默认群
        creds = {"webhook_url": args.webhook_url or ""}
    try:
        A.save_account(args.save_account[0], args.save_account[1], args.save_account[2], creds)
    except ValueError as e:
        die(str(e))
    ok(f"账号已保存: {args.save_account[0]} ({args.save_account[1]})")


def cmd_test_account(args):
    try:
        slug, acc = A.get(args.test_account)
    except ValueError as e:
        die(str(e))
    cls = PROVIDERS.get(acc.get("provider", ""))
    if not cls:
        die(f"账号 provider 不支持: {acc.get('provider')}")
    p = cls(slug, acc, C.load_config())
    good, msg = p.test()
    print(("✅ " if good else "❌ ") + msg)
    sys.exit(0 if good else 1)


def cmd_list_contacts():
    data = CT.list_all()
    print("联系人:")
    for alias, ent in data["contacts"].items():
        if ent.get("type") == "single":
            ids = ", ".join(f"{k}:{v}" for k, v in (ent.get("ids") or {}).items())
            print(f"  {alias} (single) {ids}")
        else:
            print(f"  {alias} (members) -> {', '.join(ent.get('members', []))}")
    print("群:")
    for alias, ent in data["groups"].items():
        print(f"  {alias} [{ent.get('provider')}] {ent.get('chat_id')}")


def cmd_list_log():
    entries = sendlog.recent(20)
    if not entries:
        print("（暂无发送记录）")
        return
    for e in entries:
        print(f"  [{e['ts']}] {e['provider']}/{e['send_mode']} -> {e['target']}  "
              f"id={e['msg_id'][:36]}  {e['preview'][:40]}")


# ---------------- provider resolution ----------------

def build_provider(args) -> Provider:
    cfg = C.load_config()
    provider_name = args.provider or cfg.get("default_provider", "")
    try:
        if args.account:
            slug, acc = A.get(args.account)
            provider_name = acc["provider"]
        elif provider_name:
            slug, acc = A.get(provider=provider_name)
        else:
            slug, acc = A.get()
            provider_name = acc["provider"]
    except ValueError as e:
        die(str(e))
    cls = PROVIDERS.get(provider_name)
    if not cls:
        die(f"不支持的 provider: {provider_name}（支持: {', '.join(PROVIDERS)}）")
    return cls(slug, acc, cfg)


def resolve_recipients(p: Provider, raw_targets: list[str]) -> tuple[list[str], list[str]]:
    """Returns (resolved_ids, display_names). Dies with actionable message on failure."""
    ids, names, errors = [], [], []
    for t in raw_targets:
        try:
            alias_ids = CT.resolve_contact(t, p.name)
        except ValueError as e:
            errors.append(str(e))
            continue
        if alias_ids is not None:
            ids.extend(alias_ids)
            names.append(t)
            continue
        try:
            ids.append(p.resolve_user(t))
            names.append(t)
        except ValueError as e:
            errors.append(str(e))
    if errors:
        die("收件人解析失败:\n  - " + "\n  - ".join(errors))
    return list(dict.fromkeys(ids)), names


# ---------------- send flows ----------------

def do_send(args):
    p = build_provider(args)
    caps = p.capabilities()

    # message content
    text = args.msg or ""
    if args.template:
        try:
            text = templates.render(args.template, args.vars or [])
        except ValueError as e:
            die(str(e))
    if not text and not args.image and not args.file:
        die("缺少消息内容: --msg / --template / --image / --file 至少其一")

    # broadcast --department
    if args.broadcast and args.department:
        cfg = C.load_config()
        try:
            dept = org_lookup.resolve_department(p, args.department, cfg)
        except (ValueError, RuntimeError, NotSupported) as e:
            die(str(e))
        targets = dept["member_ids"]
        target_desc = f"部门[{dept['dept_name']}] {len(targets)}人"
        return _send_p2p_flow(args, p, targets, target_desc, text, broadcast=True)

    # group send
    if args.chat_id:
        try:
            chat_id = CT.resolve_group(args.chat_id, p.name)
        except ValueError as e:
            die(str(e))
        if chat_id is None:
            die(f"未知群别名: {args.chat_id}。用 --save-group 保存，如: "
                f"--save-group {args.chat_id} {p.name} <chat_id>")
        mention_ids = []
        if args.mention:
            mention_ids, _ = resolve_recipients(p, args.mention)
        return _send_group_flow(args, p, chat_id, text, mention_ids)

    # p2p
    if not args.to:
        die("缺少目标: --to / --chat-id / --department")
    ids, names = resolve_recipients(p, args.to)
    if not ids:
        die("收件人列表为空")
    target_desc = ",".join(names[:5]) + (f" 等{len(ids)}人" if len(ids) > 5 else "")
    return _send_p2p_flow(args, p, ids, target_desc, text, broadcast=args.broadcast)


def _gate(args, p: Provider, recipients: list[str], text: str) -> str:
    cfg = C.load_config()
    try:
        tier = safety.check(recipients, text, cfg,
                            force_send=args.force_send, approve_code=args.approve_code or "")
    except safety.GateWarn as e:
        die(str(e), 3)
    except safety.GateReview as e:
        msg = str(e)
        code = ""
        if "__PENDING_CODE__:" in msg:
            msg, code = msg.rsplit("__PENDING_CODE__:", 1)
        _notify_admins(cfg, code.strip(), len(recipients), text)
        die(msg.strip(), 4)
    if tier in ("warned", "approved"):
        sendlog.broadcast_audit(
            sender=p.slug, provider=p.name, mode=tier,
            count=len(recipients), preview=text, targets_sample=recipients,
        )
    return tier


def _notify_admins(cfg: dict, code: str, count: int, text: str):
    """Send approval code to admins via configured provider DM. Never crash."""
    if not code:
        return
    gate = cfg.get("safety_gate", {})
    admins = gate.get("admins") or []
    if not admins:
        print("⚠️ 未配置管理员（safety_gate.admins），审核码无法送达。"
              "请配置后重试，或由管理员直接查看 approvals.json")
        return
    notified = 0
    for adm in admins:
        prov_name = adm.get("provider") or gate.get("notify_provider", "")
        uid = adm.get("user_id", "")
        if not prov_name or not uid:
            continue
        try:
            slug, acc = A.get(provider=prov_name)
            padm = PROVIDERS[prov_name](slug, acc, cfg)
            note = (f"🔐 [smart-message-plus 审核] 有人申请群发 {count} 人\n"
                    f"内容预览: {text[:100]}\n审核码: {code}（30分钟有效，请确认后转告申请人）")
            res = padm.send_p2p([uid], note)
            if res.ok:
                notified += 1
        except (ValueError, RuntimeError, KeyError, OSError) as e:
            print(f"⚠️ 管理员通知失败（{prov_name}:{uid}）: {e}")
    if notified:
        print(f"📨 已通知 {notified} 位管理员")
    else:
        print("⚠️ 所有管理员通知均失败，请人工处理（approvals.json 中有审核码）")


def _parse_buttons(args) -> list:
    """--button '文案|URL' (repeatable) -> [(label, url), ...]"""
    buttons = []
    for group in (args.button or []):
        for b in group:
            if "|" not in b:
                die(f"按钮格式错误: {b!r}。应为 '文案|URL'，如 --button '查看详情|https://example.com'")
            label, url = b.split("|", 1)
            label, url = label.strip(), url.strip()
            if not label or not url.startswith(("http://", "https://")):
                die(f"按钮格式错误: {b!r}。文案不能为空且 URL 须以 http(s):// 开头")
            buttons.append((label, url))
    return buttons


def _send_p2p_flow(args, p: Provider, ids: list[str], target_desc: str, text: str, broadcast=False):
    mode = "broadcast" if broadcast else "p2p"
    if args.dry_run:
        print(f"[dry-run] {p.name} {mode} -> {target_desc}")
        print(f"[dry-run] 收件人 {len(ids)} 人: {', '.join(ids[:10])}{' ...' if len(ids) > 10 else ''}")
        print(f"[dry-run] 内容: {text[:200] if text else '(图片/文件)'}")
        if args.card:
            print(f"[dry-run] 卡片: 标题[{args.card_title or '(无)'}] 按钮 {len(_parse_buttons(args))} 个")
        return
    _gate(args, p, ids, text or "(媒体消息)")

    results = []
    try:
        if args.image:
            for img in args.image:
                results.append(("图片 " + img, p.send_image_p2p(ids, img)))
        if args.file:
            results.append(("文件 " + args.file, p.send_file_p2p(ids, args.file)))
        if text:
            if args.card:
                buttons = _parse_buttons(args)
                results.append(("卡片", p.send_card_p2p(ids, args.card_title, text, buttons)))
            else:
                results.append(("消息", p.send_p2p(ids, text, markdown=args.markdown)))
    except (NotSupported, ValueError) as e:
        die(str(e))

    all_ok = True
    for label, res in results:
        if res.ok:
            sendlog.record(p.name, p.slug, res.msg_id, mode, target_desc,
                           text or label, extra={"count": len(ids)})
            ok(f"{label} 已发送 -> {target_desc}  (msg_id: {res.msg_id})")
            if res.detail:
                print(f"   ⚠️ {res.detail}")
        else:
            all_ok = False
            print(f"❌ {label} 发送失败: {res.detail}")
    sys.exit(0 if all_ok else 1)


def _send_group_flow(args, p: Provider, chat_id: str, text: str, mention_ids: list[str]):
    if args.dry_run:
        print(f"[dry-run] {p.name} group -> {chat_id}")
        print(f"[dry-run] 内容: {text[:200] if text else '(图片/文件)'}"
              + (f"  @{len(mention_ids)}人" if mention_ids else "")
              + ("  @所有人" if args.mention_all else ""))
        if args.card:
            print(f"[dry-run] 卡片: 标题[{args.card_title or '(无)'}] 按钮 {len(_parse_buttons(args))} 个")
        return
    results = []
    try:
        if args.image:
            for img in args.image:
                results.append(("图片 " + img, p.send_image_group(chat_id, img)))
        if args.file:
            results.append(("文件 " + args.file, p.send_file_group(chat_id, args.file)))
        if text:
            if args.card:
                buttons = _parse_buttons(args)
                results.append(("卡片", p.send_card_group(chat_id, args.card_title, text, buttons)))
            else:
                results.append(("消息", p.send_group(chat_id, text, markdown=args.markdown,
                                                mention_ids=mention_ids, mention_all=args.mention_all)))
    except (NotSupported, ValueError) as e:
        die(str(e))
    all_ok = True
    for label, res in results:
        if res.ok:
            sendlog.record(p.name, p.slug, res.msg_id, "group", args.chat_id,
                           text or label, chat_id=chat_id)
            ok(f"{label} 已发送 -> 群[{args.chat_id}]  (msg_id: {res.msg_id})")
        else:
            all_ok = False
            print(f"❌ {label} 发送失败: {res.detail}")
    sys.exit(0 if all_ok else 1)


def do_recall(args):
    entry = sendlog.find(args.recall)
    if not entry:
        die(f"发送日志中找不到消息: {args.recall}（--list-log 查看近期记录）")
    prov_name = entry.get("provider", "")
    try:
        slug, acc = A.get(entry.get("account", ""))
    except ValueError:
        try:
            slug, acc = A.get(provider=prov_name)
        except ValueError as e:
            die(f"找不到可用的 {prov_name} 账号: {e}")
    p = PROVIDERS[prov_name](slug, acc, C.load_config())
    good, msg = p.recall(entry)
    print(("✅ " if good else "❌ ") + msg)
    sys.exit(0 if good else 1)


def do_create_group(args):
    p = build_provider(args)
    if not p.capabilities().get("create_group"):
        die(f"{p.name} 暂不支持建群")
    name = args.create_group.strip()
    if not name:
        die("群名不能为空")
    owner_id = ""
    if args.owner:
        try:
            owner_id = p.resolve_user(args.owner) if args.owner.isascii() else \
                (CT.resolve_contact(args.owner, p.name) or [""])[0]
            if not owner_id:
                die(f"群主「{args.owner}」无法解析为 {p.name} 用户")
        except ValueError as e:
            die(f"群主解析失败: {e}")
    member_ids = []
    if args.members:
        member_ids, _ = resolve_recipients(p, args.members)
    if p.name == "dingtalk" and not owner_id and not member_ids:
        die("钉钉建群需要群主: --owner <别名/手机号/userId>")

    # DingTalk: no API can add a robot to an ordinary group (platform limit),
    # and the scene-template console page is broken outside the DingTalk
    # client (JSAPI 4040 notInDingTalk). Strategy: create ordinary group
    # directly, then remind the user to add the bot manually (see below).
    kwargs = {}
    if p.name == "dingtalk" and args.with_bot:
        # advanced path kept for users who somehow obtained a scene template id
        template_id = args.scene_template or C.load_config().get("dingtalk_scene_template", "")
        kwargs = {"with_bot": True, "template_id": template_id}

    if args.dry_run:
        bot_note = ""
        if p.name == "dingtalk":
            bot_note = "  [场景群模板]" if kwargs.get("with_bot") else "  [普通群，建群后提示补加机器人]"
        print(f"[dry-run] {p.name} 建群「{name}」 群主: {owner_id or '(默认)'} "
              f"成员 {len(member_ids)} 人: {', '.join(member_ids[:10])}{bot_note}")
        return
    res = p.create_group(name, owner_id, member_ids, **kwargs)
    if not res.ok:
        die(f"建群失败: {res.detail}")
    chat_id = res.extra.get("chat_id", res.msg_id)
    CT.save_group(name, p.name, chat_id, note="由 --create-group 创建")
    # remember working scene template for next time
    if p.name == "dingtalk" and kwargs.get("with_bot") and kwargs.get("template_id"):
        cfg = C.load_config()
        if cfg.get("dingtalk_scene_template") != kwargs["template_id"]:
            cfg["dingtalk_scene_template"] = kwargs["template_id"]
            C.save_config(cfg)
    ok(f"群「{name}」已创建 (chat_id: {chat_id})，已存为群别名，可直接: --chat-id {name}")
    if res.detail:
        print(f"   ℹ️ {res.detail}")
    if p.name == "dingtalk" and not kwargs.get("with_bot"):
        print(
            "\n💡 当前群未包含机器人，已可正常发消息（文本 / Markdown / 图片 / 文件）。\n"
            "   把机器人加进群可解锁额外能力：\n"
            "     • 按钮卡片消息（--card + --button，带跳转按钮的交互卡片）\n"
            "     • 消息撤回（--recall，发错秒撤）\n"
            "     • @提醒（--at 精确@群成员）\n"
            "     • 群里 @机器人 触发自动回复（配合 Stream 监听）\n"
            "   添加方法（约30秒）：手机/电脑钉钉打开该群 → 群设置 → 机器人（智能群助手）→\n"
            "   添加机器人 → 选择本应用机器人\n"
            f"   添加完成后执行以下命令切换到机器人全能力通道：\n"
            f"     --save-group {name} dingtalk <cid开头的openConversationId>\n"
            "   （cid 可通过在群里 @机器人 发条消息由 Stream 监听抓取，或联系管理员查询）")


def do_list_groups(args):
    p = build_provider(args)
    try:
        groups = p.list_groups()
    except (NotSupported, RuntimeError) as e:
        die(str(e))
    if not groups:
        print(f"{p.name} 机器人不在任何群中")
        return
    print(f"{p.name} 机器人所在群 ({len(groups)}):")
    for g in groups:
        print(f"  - {g['name']}  {g['chat_id']}")


# ---------------- main ----------------

def main():
    ap = argparse.ArgumentParser(
        description="smart-message-plus: send messages via DingTalk / Feishu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # targets
    ap.add_argument("--to", nargs="+", help="收件人: 别名/手机号/邮箱/原生ID，可多个")
    ap.add_argument("--chat-id", help="群: 群别名或原生群ID")
    ap.add_argument("--department", help="部门广播: 部门名")
    ap.add_argument("--broadcast", action="store_true", help="广播模式（配 --department 或 --to）")
    # content
    ap.add_argument("--msg", help="消息内容（必须由用户提供，AI 不得代拟）")
    ap.add_argument("--markdown", action="store_true", help="以 Markdown 发送")
    ap.add_argument("--card", action="store_true", help="以卡片发送（配合 --card-title/--button）")
    ap.add_argument("--card-title", default="", help="卡片标题")
    ap.add_argument("--button", nargs="+", action="append", metavar="'文案|URL'",
                    help="卡片按钮，可多次: --button '查看详情|https://...'（钉钉最多5个）")
    ap.add_argument("--image", nargs="+", help="发送图片（本地路径，可多张）")
    ap.add_argument("--file", help="发送文件（本地路径）")
    ap.add_argument("--template", help="使用消息模板名")
    ap.add_argument("--vars", nargs="+", help="模板变量 key=value")
    # mention
    ap.add_argument("--mention", nargs="+", help="@指定人（群聊）")
    ap.add_argument("--mention-all", action="store_true", help="@所有人（群聊）")
    # control
    ap.add_argument("--provider", choices=list(PROVIDERS), help="渠道: dingtalk/feishu/wecom")
    ap.add_argument("--account", help="指定账号 slug/名称")
    ap.add_argument("--dry-run", action="store_true", help="只预览不发送")
    ap.add_argument("--force-send", action="store_true", help="越过警告线发送")
    ap.add_argument("--approve-code", help="审核码（超审核线时需要）")
    # recall / logs
    ap.add_argument("--recall", metavar="MSG_ID", help="撤回消息")
    ap.add_argument("--list-log", action="store_true", help="查看发送日志")
    # account mgmt
    ap.add_argument("--list-accounts", action="store_true")
    ap.add_argument("--save-account", nargs=3, metavar=("SLUG", "PROVIDER", "NAME"))
    ap.add_argument("--app-key", help="钉钉 AppKey/ClientID")
    ap.add_argument("--app-secret", help="AppSecret/ClientSecret")
    ap.add_argument("--app-id", help="飞书 App ID")
    ap.add_argument("--robot-code", help="钉钉 robotCode（默认=app_key）")
    ap.add_argument("--agent-id", help="钉钉 AgentId（可选）")
    ap.add_argument("--webhook-url", help="企业微信群机器人 webhook（wecom 账号可选默认群）")
    ap.add_argument("--test-account", metavar="SLUG", help="验证账号凭证")
    ap.add_argument("--set-default-account", metavar="SLUG")
    ap.add_argument("--remove-account", metavar="SLUG")
    # onboard (v2.1)
    ap.add_argument("--onboard", action="store_true", help="交互式配置向导（渠道/凭证/验证/默认账号）")
    ap.add_argument("--onboard-status", action="store_true", help="查看配置完整度（渠道/凭证有效性/别名/门控）")
    ap.add_argument("--force", action="store_true", help="配合 --onboard：已配置渠道也重新配置")
    # contact mgmt
    ap.add_argument("--save-contact", nargs=3, metavar=("ALIAS", "TYPE", "VALUE"),
                    help='TYPE=single: "dingtalk:ID,feishu:ID"; TYPE=members: "别名1,别名2"')
    ap.add_argument("--save-group", nargs=3, metavar=("ALIAS", "PROVIDER", "CHAT_ID"))
    ap.add_argument("--list-contacts", action="store_true")
    ap.add_argument("--remove-contact", metavar="ALIAS")
    ap.add_argument("--note", default="", help="备注（配合 save-contact/save-group）")
    # group mgmt (v2.0)
    ap.add_argument("--create-group", metavar="NAME", help="建群（配 --owner/--members）")
    ap.add_argument("--owner", help="建群群主（别名/手机号/原生ID；钉钉必填，飞书可选）")
    ap.add_argument("--members", nargs="+", help="建群成员（别名/手机号/邮箱/原生ID，可多个）")
    ap.add_argument("--list-groups", action="store_true", help="列出机器人所在的群（飞书）")
    ap.add_argument("--with-bot", action="store_true",
                    help="钉钉：用场景群模板建群（机器人直接在群内，需已有可用模板ID；控制台配置常不可用，一般不需要）")
    ap.add_argument("--no-bot", action="store_true", help=argparse.SUPPRESS)  # 兼容保留，普通群已是默认
    ap.add_argument("--scene-template", metavar="ID", help="钉钉场景群模板ID（配合 --with-bot，首次传入后自动记住）")

    args = ap.parse_args()

    # management commands (no send)
    if args.onboard:
        def _save(slug, prov, creds):
            name = {"dingtalk": "钉钉Bot", "feishu": "飞书Bot", "wecom": "企微Bot"}.get(prov, prov)
            A.save_account(slug, prov, name, creds)
        return OB.run(args, _save)
    if args.onboard_status:
        OB.print_status()
        return
    if args.list_accounts:
        return cmd_list_accounts()
    if args.save_account:
        return cmd_save_account(args)
    if args.test_account:
        return cmd_test_account(args)
    if args.set_default_account:
        try:
            slug = A.set_default(args.set_default_account)
        except ValueError as e:
            die(str(e))
        return ok(f"默认账号: {slug}")
    if args.remove_account:
        return ok("账号已删除") if A.remove_account(args.remove_account) else die("账号不存在")
    if args.save_contact:
        try:
            CT.save_contact(args.save_contact[0], args.save_contact[1], args.save_contact[2], args.note)
        except ValueError as e:
            die(str(e))
        return ok(f"联系人已保存: {args.save_contact[0]}")
    if args.save_group:
        CT.save_group(args.save_group[0], args.save_group[1], args.save_group[2], args.note)
        return ok(f"群已保存: {args.save_group[0]}")
    if args.list_contacts:
        return cmd_list_contacts()
    if args.remove_contact:
        return ok("已删除") if CT.remove(args.remove_contact) else die("别名不存在")
    if args.list_log:
        return cmd_list_log()
    if args.recall:
        return do_recall(args)
    if args.create_group:
        return do_create_group(args)
    if args.list_groups:
        return do_list_groups(args)

    # send
    do_send(args)


if __name__ == "__main__":
    main()
