#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""creds.py — 通用凭据保险箱 CLI（各 skill 原样复制到 <skill>/creds/creds.py）

用法（供 AI/脚本调用，stdout 输出 JSON）:
  python creds.py init                     初始化（无主密钥则生成并打印）
  python creds.py get <key>                取明文（供脚本使用；不含 key 时报错）
  python creds.py set <key> --value-stdin  从 stdin 读入并写入（避免命令行泄露）
  python creds.py set <key> --value <v>    直接写入
  python creds.py del <key>                删除一条
  python creds.py keys                     列出所有 key 名
  python creds.py status                   状态（主密钥来源，值脱敏）
  python creds.py hooks                    查看/自检自动钩子（hooks.json）
  python creds.py test                     自测加解密往返

主密钥来自环境变量 OPENCODE_SKILL_MASTER_KEY（跨机同步各设备填同一值）。

自动钩子（hooks.json）
----------------------
本目录下可选 `hooks.json`，形如 {"after_set": {"<key 通配>": [["argv","..."], ...]}}。
`set` 成功后自动按 key 匹配执行（cwd = skill 根目录，`{python}` 替换为当前解释器），
结果附在 set 输出的 `hooks` 字段里。设了钩子却不想跑时加 `--no-hook`。
用途示例：tencentcloud-ops 用它把旋转后的密钥同步到 VPS 的 cosfs 挂载（见 scripts/sync_cosfs.py），
避免"改了保险箱、VPS 还是旧钥匙"导致的静默失效。
"""
import argparse
import fnmatch
import json
import os
import shlex
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault  # noqa: E402

HOOKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hooks.json")
HOOK_TIMEOUT = 300


def out(obj, code=0):
    text = json.dumps(obj, ensure_ascii=False)
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    sys.exit(code)


def mask(v):
    if not v:
        return ""
    return v[:4] + "***" + v[-2:] if len(v) > 8 else "***"


def load_hooks():
    """读 hooks.json；返回 {pattern: [argv, ...]}。文件不存在/损坏时返回 ({}, 错误说明)。"""
    if not os.path.exists(HOOKS_FILE):
        return {}, None
    try:
        with open(HOOKS_FILE, encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception as e:
        return {}, "hooks.json 解析失败: %s" % e
    rules = cfg.get("after_set") or {}
    norm = {}
    for pattern, val in rules.items():
        if isinstance(val, str):
            norm[pattern] = [shlex.split(val)]
            continue
        if not isinstance(val, list):
            continue
        if all(isinstance(x, str) for x in val):          # 单个 argv
            norm[pattern] = [val]
        else:                                              # argv 列表的列表
            norm[pattern] = [c for c in val if isinstance(c, list) and all(isinstance(x, str) for x in c)]
    return norm, None


def run_hooks(key):
    """按 key 匹配 after_set 钩子并逐个执行（非阻塞、有超时）。返回结果列表。"""
    rules, err = load_hooks()
    if err:
        return [{"pattern": None, "status": "error", "message": err}]
    results = []
    for pattern, cmds in rules.items():
        if not fnmatch.fnmatch(key, pattern):
            continue
        for cmd in cmds:
            argv = [c.replace("{python}", sys.executable) for c in cmd]
            t0 = time.time()
            rec = {"pattern": pattern, "cmd": argv}
            try:
                p = subprocess.run(argv, cwd=vault.SKILL_ROOT, capture_output=True, timeout=HOOK_TIMEOUT)
                rec.update({
                    "status": "ok" if p.returncode == 0 else "error",
                    "exit_code": p.returncode,
                    "seconds": round(time.time() - t0, 2),
                    "stdout": p.stdout.decode("utf-8", "replace").strip()[:2000],
                    "stderr": p.stderr.decode("utf-8", "replace").strip()[:800],
                })
            except subprocess.TimeoutExpired:
                rec.update({"status": "error", "seconds": round(time.time() - t0, 2),
                            "message": "钩子超时（%ss）" % HOOK_TIMEOUT})
            except Exception as e:
                rec.update({"status": "error", "message": "%s: %s" % (type(e).__name__, e)})
            results.append(rec)
    return results


def main():
    ap = argparse.ArgumentParser(description="通用凭据保险箱 CLI")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("init")
    p_get = sub.add_parser("get")
    p_get.add_argument("key")
    p_set = sub.add_parser("set")
    p_set.add_argument("key")
    p_set.add_argument("--value")
    p_set.add_argument("--value-stdin", action="store_true")
    p_set.add_argument("--no-hook", action="store_true", help="跳过 hooks.json 的 after_set 钩子")
    p_del = sub.add_parser("del")
    p_del.add_argument("key")
    sub.add_parser("keys")
    sub.add_parser("status")
    sub.add_parser("hooks")
    sub.add_parser("test")

    a = ap.parse_args()

    if a.cmd == "init":
        src = vault.master_key_source()
        created = False
        if not src:
            key, src = vault.get_master_key(create=True)
            created = True
            print(json.dumps({"status": "ok", "created": True,
                              "master_key": key, "stored": src,
                              "note": "请保存主密钥并设为环境变量 " + vault.MASTER_KEY_ENV},
                             ensure_ascii=False), flush=True)
            return
        out({"status": "ok", "created": False, "master_key_source": src,
             "vault_exists": os.path.exists(vault.VAULT_FILE)})

    elif a.cmd == "get":
        try:
            v = vault.vault_read().get(a.key)
        except vault.VaultLocked as e:
            out({"status": "error", "error": "vault_locked", "message": str(e)}, 1)
        if not a.key:
            out({"status": "error", "error": "key required"}, 2)
        out({"status": "ok", "key": a.key, "value": v or ""})

    elif a.cmd == "set":
        if a.value_stdin:
            val = sys.stdin.read().rstrip("\r\n")
        elif a.value is not None:
            val = a.value
        else:
            out({"status": "error", "error": "need --value or --value-stdin"}, 2)
        try:
            vault.vault_set(a.key, val)
        except vault.VaultLocked as e:
            out({"status": "error", "error": "vault_locked", "message": str(e)}, 1)
        hooks = [] if a.no_hook else run_hooks(a.key)
        res = {"status": "ok", "key": a.key, "stored": True}
        if hooks:
            res["hooks"] = hooks
            if any(h.get("status") != "ok" for h in hooks):
                res["hooks_warning"] = "有钩子未成功；请检查上面的 hooks[].stderr/stdout（保险箱已写入）"
        out(res)

    elif a.cmd == "hooks":
        rules, err = load_hooks()
        out({"status": "error", "message": err} if err else
            {"status": "ok", "hooks_file": HOOKS_FILE,
             "exists": os.path.exists(HOOKS_FILE), "after_set": rules})

    elif a.cmd == "del":
        ok = vault.vault_delete(a.key)
        out({"status": "ok", "key": a.key, "deleted": ok})

    elif a.cmd == "keys":
        out({"status": "ok", "keys": vault.vault_keys()})

    elif a.cmd == "status":
        try:
            data = vault.vault_read()
            keys = {k: mask(v) for k, v in data.items()}
        except vault.VaultLocked as e:
            out({"status": "locked", "master_key_source": vault.master_key_source(),
                 "vault_file": vault.VAULT_FILE, "message": str(e)})
        out({"status": "ok", "master_key_source": vault.master_key_source(),
             "vault_file": vault.VAULT_FILE, "keys": keys})

    elif a.cmd == "test":
        import tempfile
        import secrets
        tmp = os.path.join(tempfile.gettempdir(), "opencode_creds_test.enc")
        _ov = vault.VAULT_FILE
        vault.VAULT_FILE = tmp
        os.environ.setdefault(vault.MASTER_KEY_ENV, "selftest-" + secrets.token_hex(8))
        try:
            probe = {"甲": "值1", "b": "值2"}
            vault.vault_write(probe)
            ok = vault.vault_read() == probe
        finally:
            vault.VAULT_FILE = _ov
            try:
                os.remove(tmp)
            except Exception:
                pass
        out({"status": "ok" if ok else "error", "roundtrip_ok": ok})

    else:
        ap.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
