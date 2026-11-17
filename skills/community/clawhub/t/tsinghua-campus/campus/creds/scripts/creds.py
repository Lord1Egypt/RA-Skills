"""creds.py — 技能包统一凭据管理

单一加密保险箱（skill/campus/runtime/credentials.enc），所有子 SKILL 共用。
凭据整体加密，解密只需一个主密钥（环境变量 CAMPUS_MASTER_KEY / OS keyring / 密钥文件）。

每条凭据有元数据（用途/获取方式/影响范围/是否已配），支持查询与责任告知。

CLI:
  creds.py status                  → 全部凭据配置状态（已配/未配/影响哪些功能）
  creds.py guide [key]             → 责任告知：凭据去哪申请、用来干嘛、存哪、怎么删
  creds.py add <key> --value-stdin → 添加/更新凭据（stdin 传入，不进命令行）
  creds.py remove <key> --confirm  → 删除凭据（需 --confirm）
  creds.py verify <key>            → 校验某凭据是否已配
  creds.py key show|set|source     → 主密钥管理（跨机同步用）

约定:
- 密码/密钥一律走 --value-stdin，禁止出现在命令行参数（防进程列表泄露）
- 输出脱敏：展示时密钥只显示前 4 位
"""
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common
import vault

# ============ 凭据 schema（元数据 = 责任告知） ============
# 每个子 SKILL 需要哪些凭据写在这里；value 只存密文，不进本文件
# system 字段 = 凭据归属的系统域（cas/文献/邮件/llm），用于分组展示与独立配置
SYSTEMS_META = {
    "cas": {"label": "清华统一认证（CAS）", "desc": "learn/info/timetable/library 共用，登录 id.tsinghua.edu.cn"},
    "literature": {"label": "文献检索（Scopus/Elsevier）", "desc": "literature 子技能，查论文/摘要/引用"},
    "mail": {"label": "邮箱（IMAP）", "desc": "mail 子技能，收发邮件"},
    "llm": {"label": "AI 大模型（DeepSeek）", "desc": "learn 预批改 / 文献摘要"},
}

CRED_SCHEMA = {
    "cas_username": {
        "system": "cas",
        "label": "清华统一认证账号（CAS）",
        "used_by": ["learn 网络学堂", "timetable 课表考试", "library 图书馆", "info 信息查询"],
        "how_to_get": "即学号（学号/工号），用于登录 id.tsinghua.edu.cn 统一身份认证。所有需要 CAS 的子技能共用，配一次即可。",
        "security": "仅发送至 id.tsinghua.edu.cn（CAS）及目标校内系统。本地使用操作系统安全存储 API 加密，安全性很高，凭据不出设备。",
    },
    "cas_password": {
        "system": "cas",
        "label": "清华统一认证密码（CAS）",
        "used_by": ["learn 网络学堂", "timetable 课表考试", "library 图书馆", "info 信息查询"],
        "how_to_get": "与登录信息门户的密码相同。若开启过二次验证，首次登录时需完成一次人工 2FA（会引导你操作）。",
        "security": "仅发送至 id.tsinghua.edu.cn（CAS）。本地使用操作系统安全存储 API 加密，安全性很高，不出设备。",
    },
    "student_id": {
        "system": "cas",
        "label": "学号",
        "used_by": ["learn 网络学堂（提交作业命名）"],
        "how_to_get": "你的学生证号。若不配，自动使用 CAS 账号（cas_username）。",
        "security": "仅用于作业文件命名（学号_姓名.pdf）。本地加密存储。",
    },
    "student_name": {
        "system": "cas",
        "label": "姓名",
        "used_by": ["learn 网络学堂（提交作业命名）"],
        "how_to_get": "你的真实姓名，用于作业文件命名（学号_姓名.pdf）。",
        "security": "仅用于作业文件命名。本地加密存储。",
    },
    "scopus_api_key": {
        "system": "literature",
        "label": "Scopus API Key",
        "used_by": ["literature 文献检索"],
        "how_to_get": "登录 https://dev.elsevier.com 注册申请（可走清华 CARSI 机构登录）。免费层每日配额，见 agent/literature/scopus_api_policy.md。",
        "security": "仅用于 api.elsevier.com 请求。",
    },
    "scopus_inst_token": {
        "system": "literature",
        "label": "Scopus 机构 Token（可选）",
        "used_by": ["literature 文献检索"],
        "how_to_get": "清华订阅的 Institutional Token，提升配额与数据权限。可向图书馆申请。",
        "security": "仅用于 api.elsevier.com 请求。",
    },
    "deepseek_api_key": {
        "system": "llm",
        "label": "DeepSeek API Key（可选）",
        "used_by": ["learn AI 预批改", "literature 摘要"],
        "how_to_get": "https://platform.deepseek.com 注册并创建 API Key。OpenAI 兼容。",
        "security": "仅用于 api.deepseek.com。",
    },
    "email_imap": {
        "system": "mail",
        "label": "邮箱授权码/凭据",
        "used_by": ["mail 邮箱"],
        "how_to_get": "各邮箱的 IMAP 授权码：QQ/清华/腾讯企业等在邮箱设置里开启 IMAP 并生成授权码。详见 email-accounts skill。",
        "security": "仅用于 imap/smtp 服务器。",
    },
}


def _load_creds():
    """读凭据保险箱（无箱返回 {}；解不开抛 vault.VaultLocked）。"""
    return vault.vault_read()


def _save_creds(data):
    vault.vault_write(data)


def _mask(v):
    if not v:
        return ""
    return v[:4] + "****"


def cmd_status():
    locked = None
    try:
        stored = _load_creds()
    except vault.VaultLocked as e:
        stored = {}
        locked = str(e)
    # 按系统域分组展示
    systems = {}
    for key, meta in CRED_SCHEMA.items():
        sys_name = meta.get("system", "other")
        s = systems.setdefault(sys_name, {"label": SYSTEMS_META.get(sys_name, {}).get("label", sys_name),
                                          "desc": SYSTEMS_META.get(sys_name, {}).get("desc", ""),
                                          "creds": []})
        raw = stored.get(key, "")
        s["creds"].append({
            "key": key,
            "label": meta["label"],
            "configured": bool(raw),
            "used_by": meta["used_by"],
        })
    rows = [{"key": k, "label": m["label"], "configured": bool(stored.get(k, ""))} for k, m in CRED_SCHEMA.items()]
    configured = sum(1 for r in rows if r["configured"])
    common.output_json({
        "status": "ok",
        "configured": configured,
        "total": len(rows),
        "all_configured": configured == len(rows),
        "systems": systems,
        "creds": rows,
        "vault_file": vault.VAULT_FILE,
        "vault_locked": locked,
        "master_key_source": vault.master_key_source(),
        "master_key_env": vault.MASTER_KEY_ENV,
        "guide": "creds.py guide [system] 查看各系统凭据说明",
    })


def cmd_guide(keys):
    # 支持按系统域过滤：creds.py guide <system> 或 <key>
    target = list(keys) if keys else list(CRED_SCHEMA.keys())
    out = []
    stored = _load_creds()
    for item in target:
        if item in SYSTEMS_META:  # 按系统域展开
            for key, meta in CRED_SCHEMA.items():
                if meta.get("system") == item:
                    out.append(_guide_entry(key, meta, stored))
            continue
        if item not in CRED_SCHEMA:
            common.output_json({"status": "error", "message": f"未知凭据或系统: {item}",
                                "known_keys": list(CRED_SCHEMA.keys()),
                                "known_systems": list(SYSTEMS_META.keys())})
            sys.exit(1)
        out.append(_guide_entry(item, CRED_SCHEMA[item], stored))
    common.output_json({"status": "ok", "guide": out})


def _guide_entry(key, meta, stored):
    return {
        "key": key,
        "system": meta.get("system"),
        "label": meta["label"],
        "how_to_get": meta["how_to_get"],
        "used_by": meta["used_by"],
        "security": meta["security"],
        "configured": bool(stored.get(key, "")),
        "stored_as": "操作系统安全存储 API 加密（安全性很高）",
    }


def cmd_add(key, value):
    if key not in CRED_SCHEMA:
        common.output_json({"status": "error", "message": f"未知凭据: {key}", "known": list(CRED_SCHEMA.keys())})
        sys.exit(1)
    if not value:
        common.output_json({"status": "error", "message": "value 为空（用 --value-stdin 传值）"})
        sys.exit(1)
    try:
        stored = _load_creds()
    except vault.VaultLocked as e:
        common.output_json({"status": "error", "locked": True, "message": str(e)})
        sys.exit(1)
    stored[key] = value
    _save_creds(stored)
    common.output_json({"status": "ok", "key": key, "masked": _mask(value),
                        "master_key_source": vault.master_key_source(),
                        "message": "已加密保存"})


def cmd_remove(key):
    if key not in CRED_SCHEMA:
        common.output_json({"status": "error", "message": f"未知凭据: {key}"})
        sys.exit(1)
    stored = _load_creds()
    if key not in stored:
        common.output_json({"status": "error", "message": f"{key} 未配置，无需删除"})
        sys.exit(1)
    del stored[key]
    _save_creds(stored)
    common.output_json({"status": "ok", "key": key, "message": "已删除"})


def cmd_verify(keys):
    try:
        stored = _load_creds()
    except vault.VaultLocked as e:
        common.output_json({"status": "error", "locked": True, "message": str(e)})
        sys.exit(1)
    result = {}
    for key in keys:
        dec = stored.get(key, "")
        ok = bool(dec)
        result[key] = {"configured": ok, "masked": _mask(dec) if ok else ""}
    common.output_json({"status": "ok", "verify": result})


def cmd_key(action, value=None):
    """主密钥管理（跨机同步用）。

    show   → 显示当前主密钥（敏感：用于把同一密钥带到其他设备）
    set    → 显式设置主密钥（写 keyring 或密钥文件）
    source → 显示主密钥来源与保险箱路径
    """
    if action == "show":
        mk, src = vault.get_master_key(create=False)
        if not mk:
            common.output_json({"status": "error", "message": "尚无主密钥（先配置一次凭据）"})
            sys.exit(1)
        common.output_json({
            "status": "ok", "source": src, "master_key": mk,
            "env": vault.MASTER_KEY_ENV,
            "hint": f"在其他设备设环境变量 {vault.MASTER_KEY_ENV}=<此值>，即可解密同步过来的保险箱",
        })
    elif action == "set":
        if not value:
            common.output_json({"status": "error", "message": "需 --value-stdin 传主密钥"})
            sys.exit(1)
        where = vault.set_master_key(value)
        common.output_json({
            "status": "ok", "stored_at": where,
            "hint": f"跨机同步请在每台设备设环境变量 {vault.MASTER_KEY_ENV}=<同一值>",
        })
    else:
        common.output_json({
            "status": "ok",
            "source": vault.master_key_source(),
            "env": vault.MASTER_KEY_ENV,
            "vault_file": vault.VAULT_FILE,
        })


def cmd_reset_system(system):
    """按系统域重置凭据（cas/literature/mail/llm）。只清该系统，不统一清空。"""
    if system not in SYSTEMS_META:
        common.output_json({"status": "error", "message": f"未知系统: {system}",
                            "known_systems": list(SYSTEMS_META.keys())})
        sys.exit(1)
    keys = [k for k, m in CRED_SCHEMA.items() if m.get("system") == system]
    try:
        stored = _load_creds()
    except vault.VaultLocked as e:
        common.output_json({"status": "error", "locked": True, "message": str(e)})
        sys.exit(1)
    removed = []
    for k in keys:
        if k in stored:
            del stored[k]
            removed.append(k)
    if removed:
        _save_creds(stored)
    # 顺带清掉旧版 per-credential keyring 冗余条目（值已不在 keyring）
    vault.purge_legacy_keyring(keys)
    common.output_json({
        "status": "ok",
        "system": system,
        "label": SYSTEMS_META[system]["label"],
        "removed": removed,
        "message": f"已重置 {SYSTEMS_META[system]['label']} 的凭据（{len(removed)} 个），其他系统不受影响",
    })


def main():
    ap = argparse.ArgumentParser(description="技能包统一凭据管理")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("status")
    g = sub.add_parser("guide")
    g.add_argument("keys", nargs="*")
    a = sub.add_parser("add")
    a.add_argument("key")
    a.add_argument("--value-stdin", action="store_true", help="从 stdin 读值（推荐，不进命令行）")
    r = sub.add_parser("remove")
    r.add_argument("key")
    r.add_argument("--confirm", action="store_true")
    rs = sub.add_parser("reset")
    rs.add_argument("system", help="系统域: cas/literature/mail/llm")
    rs.add_argument("--confirm", action="store_true")
    v = sub.add_parser("verify")
    v.add_argument("keys", nargs="+")
    k = sub.add_parser("key", help="主密钥管理（跨机同步用）")
    k.add_argument("action", choices=["show", "set", "source"])
    k.add_argument("--value-stdin", action="store_true")
    args = ap.parse_args()

    if not args.cmd:
        cmd_status()
        return
    if args.cmd == "status":
        cmd_status()
    elif args.cmd == "guide":
        cmd_guide(args.keys)
    elif args.cmd == "add":
        value = sys.stdin.read() if args.value_stdin else None
        if not value:
            common.output_json({"status": "error", "message": "需要 --value-stdin 且 stdin 非空"})
            sys.exit(1)
        value = value.rstrip("\r\n")
        while value.startswith("\ufeff"):
            value = value[1:]
        cmd_add(args.key, value)
    elif args.cmd == "remove":
        if not args.confirm:
            common.output_json({"status": "error", "message": "删除需 --confirm"})
            sys.exit(1)
        cmd_remove(args.key)
    elif args.cmd == "reset":
        if not args.confirm:
            common.output_json({"status": "error", "message": f"重置需 --confirm（将清空 {args.system} 系统的全部凭据）"})
            sys.exit(1)
        cmd_reset_system(args.system)
    elif args.cmd == "verify":
        cmd_verify(args.keys)
    elif args.cmd == "key":
        value = None
        if args.action == "set":
            value = sys.stdin.read() if args.value_stdin else None
            if value:
                value = value.rstrip("\r\n")
                while value.startswith("\ufeff"):
                    value = value[1:]
        cmd_key(args.action, value)


if __name__ == "__main__":
    main()
