#!/usr/bin/env python3
"""smart-message-plus: interactive onboarding wizard (--onboard / --onboard-status).

设计要点：
- 交互式（TTY）：逐步引导选渠道→录凭证→验证→设默认→（可选）别名/门控
- 非交互（管道/Agent 调用）：不卡死等输入，打印当前状态 + 每一步对应的单条命令
- 增量补缺：已配置且验证通过的渠道默认跳过，--force 才全部重走
- 权限清单内嵌：按选中的渠道只显示相关部分（详版见 references/console-setup.md）
"""
from __future__ import annotations

import sys

from . import accounts as A
from . import config as C
from . import contacts as CT

# ---------------- channel metadata (内嵌引导 + 权限清单) ----------------

CHANNELS = {
    "dingtalk": {
        "label": "钉钉（企业内部应用）",
        "cred_fields": [
            ("app_key", "AppKey / Client ID", True),
            ("app_secret", "AppSecret / Client Secret", True),
            ("robot_code", "robotCode（回车默认=AppKey）", False),
        ],
        "guide": [
            "后台: https://open-dev.dingtalk.com → 应用开发 → 企业内部应用 → 创建",
            "应用能力 → 机器人 → 开启（改完必须点「发布」）",
            "权限（按需）:",
            "  - 机器人消息（随机器人能力，单聊/群聊/撤回）",
            "  - qyapi_get_member_by_mobile  手机号查人（--to 手机号）",
            "  - qyapi_get_department_list + qyapi_get_member  部门广播",
            "  - qyapi_chat_manage  建群（开通即生效）",
            "版本管理与发布 → 发布（开发版仅开发者可见！）",
        ],
    },
    "feishu": {
        "label": "飞书（自建应用）",
        "cred_fields": [
            ("app_id", "App ID", True),
            ("app_secret", "App Secret", True),
        ],
        "guide": [
            "后台: https://open.feishu.cn → 创建企业自建应用",
            "权限（注意选「应用身份」，不是用户身份）:",
            "  - im:message  发消息（必须）",
            "  - im:resource  图片/文件",
            "  - contact:user.id:readonly  邮箱/手机号查人",
            "  - im:chat  群列表/建群",
            "⚠️ 权限每次变更后必须: 版本管理 → 创建版本 → 发布",
            "⚠️ 「可用范围」必须包含目标用户，否则单聊失败",
        ],
    },
    "wecom": {
        "label": "企业微信（群机器人 webhook）",
        "cred_fields": [
            ("webhook_url", "默认群 webhook 地址（可回车跳过，之后用 --save-group 按群保存）", False),
        ],
        "guide": [
            "无需管理后台！任意纯内部群（PC 端最稳）:",
            "  群右上角「···」→ 添加群机器人 → 新建 → 复制 Webhook 地址",
            "能力: 仅群聊（文本/MD/图片≤2MB/文件≤20MB/news卡片/@人）",
            "  无单聊/通讯录/建群/撤回（需 wecom-app 模式=企业可信IP，托管环境不可用）",
            "一个 webhook = 一个群；发多个群保存多个群别名",
            "⚠️ webhook 泄漏者可向群发任意消息，按密钥对待",
        ],
    },
}


# ---------------- status ----------------

def channel_status() -> dict:
    """Returns {provider: {"configured": bool, "slugs": [...], "ok": bool|None, "msg": str}}"""
    cfg = A.load()
    out = {}
    for prov in A.PROVIDERS:
        slugs = [s for s, a in cfg.get("accounts", {}).items() if a.get("provider") == prov]
        out[prov] = {"configured": bool(slugs), "slugs": slugs, "ok": None, "msg": ""}
    return out


def verify_channel(prov: str, slug: str) -> tuple[bool, str]:
    """Live credential check via provider.test(). Imports deferred to avoid cycles
    (send.py already puts scripts/ on sys.path)."""
    from providers.dingtalk import DingTalkProvider
    from providers.feishu import FeishuProvider
    from providers.wecom import WeComProvider
    classes = {"dingtalk": DingTalkProvider, "feishu": FeishuProvider, "wecom": WeComProvider}
    try:
        _, acc = A.get(slug)
        p = classes[prov](slug, acc, C.load_config())
        return p.test()
    except (ValueError, RuntimeError, KeyError, OSError) as e:
        return False, str(e)


def print_status() -> dict:
    """--onboard-status: configuration completeness overview."""
    st = channel_status()
    cfg = A.load()
    data = CT.list_all()
    gate = C.load_config().get("safety_gate", {})

    print("📋 smart-message-plus 配置状态\n")
    print("渠道:")
    for prov, info in st.items():
        label = CHANNELS[prov]["label"]
        if not info["configured"]:
            print(f"  ⬜ {prov:9s} {label} — 未配置")
            continue
        marks = []
        for slug in info["slugs"]:
            good, msg = verify_channel(prov, slug)
            info["ok"] = good
            marks.append(f"{slug}{'✅' if good else '❌ ' + msg[:60]}")
        print(f"  ✅ {prov:9s} {label} — {'; '.join(marks)}")
    dft = cfg.get("default", "")
    print(f"\n默认账号: {dft or '（未设置）'}")
    print(f"联系人别名: {len(data['contacts'])} 个；群别名: {len(data['groups'])} 个")
    admins = gate.get("admins") or []
    print(f"安全门控: {'开启' if gate.get('enabled', True) else '关闭'}"
          f"（警告线 {gate.get('warn_threshold', 50)} / 审核线 {gate.get('review_threshold', 100)} / "
          f"管理员 {len(admins)} 人{'' if admins else ' ⚠️ 未配置，>审核线的群发将无法送码'}）")
    missing = [p for p, i in st.items() if not i["configured"]]
    if missing:
        print(f"\n💡 未配置渠道: {', '.join(missing)}。运行 --onboard 补齐")
    return st


# ---------------- wizard ----------------

def _ask(prompt: str, default: str = "") -> str:
    """input() with EOF safety (non-TTY → default). Ctrl+C exits as promised."""
    try:
        v = input(prompt).strip()
        return v or default
    except KeyboardInterrupt:
        print("\n👋 已退出向导（已保存的配置不丢，重跑 --onboard 可继续）")
        sys.exit(130)
    except EOFError:
        print("\n（输入结束，跳过）")
        return default


def _ask_yn(prompt: str, default: bool = True) -> bool:
    v = _ask(f"{prompt} [{'Y/n' if default else 'y/N'}] ").lower()
    if not v:
        return default
    return v in ("y", "yes", "是")


def _print_guide(prov: str):
    print(f"\n📖 {CHANNELS[prov]['label']} 配置指引:")
    for line in CHANNELS[prov]["guide"]:
        print(f"   {line}")


def _noninteractive_help():
    """Non-TTY fallback: print status + per-step commands instead of blocking."""
    print("（非交互环境，onboard 向导改为输出操作手册）\n")
    print_status()
    print("""
━━━ 分步命令（复制执行） ━━━
# 1. 保存账号
--save-account my-dingtalk dingtalk "钉钉Bot" --app-key <KEY> --app-secret <SECRET>
--save-account my-feishu feishu "飞书Bot" --app-id <ID> --app-secret <SECRET>
--save-account my-wecom wecom "企微Bot"            # webhook 模式无需凭证
# 2. 验证
--test-account <slug>
# 3. 默认账号
--set-default-account <slug>
# 4. 别名（可选）
--save-contact 张三 single "dingtalk:0144xxx,feishu:ou_xxx"
--save-group 告警群 wecom "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
# 5. 查看状态
--onboard-status
权限清单详版: references/console-setup.md""")


def run(args, save_account_fn) -> None:
    """--onboard main flow. save_account_fn(slug, provider, creds) -> None."""
    force = bool(getattr(args, "force", False))
    if not sys.stdin.isatty():
        _noninteractive_help()
        return

    print("👋 smart-message-plus 配置向导（Ctrl+C 随时退出，已保存的不丢）\n")
    st = channel_status()

    # Step 1: 渠道逐个走
    for prov, meta in CHANNELS.items():
        info = st[prov]
        if info["configured"] and not force:
            good, msg = verify_channel(prov, info["slugs"][0])
            if good:
                print(f"⏭️  {meta['label']}: 已配置且凭证有效（{info['slugs'][0]}），跳过（--force 可重配）")
                continue
            print(f"⚠️  {meta['label']}: 已配置但验证失败——{msg[:80]}，重新配置")
        if not _ask_yn(f"配置 {meta['label']}？", default=not info["configured"]):
            continue
        _print_guide(prov)
        creds = {}
        aborted = False
        for field, label, required in meta["cred_fields"]:
            v = _ask(f"  {label}: ")
            if required and not v:
                print(f"  ⏭️ 未填写必填项 {field}，跳过 {prov}")
                aborted = True
                break
            if v:
                creds[field] = v
        if aborted:
            continue
        slug = _ask(f"  账号名 slug（回车默认 my-{prov}）: ", f"my-{prov}")
        try:
            save_account_fn(slug, prov, creds)
        except ValueError as e:
            print(f"  ❌ 保存失败: {e}")
            continue
        good, msg = verify_channel(prov, slug)
        print(f"  {'✅' if good else '❌'} 验证: {msg[:120]}")
        if not good and prov != "wecom":
            print("  💡 常见原因: Secret 抄错 / 应用未发布 / 权限未开。详见 references/console-setup.md")

    # Step 2: 默认账号
    cfg = A.load()
    accounts = cfg.get("accounts", {})
    if accounts and (not cfg.get("default") or force):
        slugs = list(accounts)
        if len(slugs) == 1:
            A.set_default(slugs[0])
            print(f"\n默认账号: {slugs[0]}（唯一账号自动设置）")
        else:
            v = _ask(f"\n设置默认账号（{'/'.join(slugs)}，回车跳过）: ")
            if v in slugs:
                A.set_default(v)
                print(f"默认账号: {v}")

    # Step 3: 可选项引导（不强塞流程，给命令）
    data = CT.list_all()
    if not data["contacts"] and not data["groups"]:
        print("\n💡 下一步（可选）:")
        print('   联系人: --save-contact 张三 single "dingtalk:0144xxx,feishu:ou_xxx"')
        print('   群:     --save-group 告警群 wecom "<webhook地址>"')
    gate = C.load_config().get("safety_gate", {})
    if not (gate.get("admins") or []):
        print("   门控管理员（>100人群发送审核码用）: 编辑数据目录 config.json 的 safety_gate.admins")

    print("\n🎉 onboard 完成。--onboard-status 随时查看配置状态；发送示例:")
    print('   --to 张三 --msg "内容"   |   --provider wecom --chat-id 告警群 --msg "内容"')
