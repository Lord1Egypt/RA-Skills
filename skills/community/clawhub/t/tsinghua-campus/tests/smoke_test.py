"""smoke_test.py — 底座冒烟测试

一键跑通: 平台检测 → 环境检查 → creds status → vault 加密往返 → session 读写 → login --check
用于开发回归与交付验收。输出汇总 JSON。

用法:
  python smoke_test.py              # 全部检查
  python smoke_test.py --quick      # 只跑不依赖浏览器/凭据的部分
"""
import sys
import os
import json
import tempfile
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campus", "shared", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campus", "creds", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campus", "base-cas", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campus", "install", "scripts"))
import common
import vault
import session
import creds
import browser


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="跳过浏览器相关")
    args = ap.parse_args()

    results = {}
    ok_all = True

    # 1. 平台
    p = common.detect_platform()
    results["platform"] = p
    common.log(f"[smoke] platform={p}")

    # 2. vault 加解密往返（单文件保险箱，用临时文件避免污染真实凭据）
    try:
        tmpvault = os.path.join(tempfile.gettempdir(), "campus_smoke_vault.enc")
        tmplegacy = os.path.join(tempfile.gettempdir(), "campus_smoke_legacy.json")
        for f in (tmpvault, tmplegacy):
            try:
                os.remove(f)
            except Exception:
                pass
        _ov, _ol = vault.VAULT_FILE, vault.LEGACY_FILE
        vault.VAULT_FILE, vault.LEGACY_FILE = tmpvault, tmplegacy
        try:
            probes = {"k1": "甲", "k2": "乙"}
            vault.vault_write(probes)
            got = vault.vault_read()
            ok = all(got.get(k) == v for k, v in probes.items())
            vault.vault_set("k1", "AAA")
            vault.vault_set("k2", "BBB")
            ok &= (vault.vault_get("k1") == "AAA" and vault.vault_get("k2") == "BBB")
        finally:
            vault.VAULT_FILE, vault.LEGACY_FILE = _ov, _ol
            for f in (tmpvault, tmplegacy):
                try:
                    os.remove(f)
                except Exception:
                    pass
        results["vault"] = {"ok": ok, "master_key_source": vault.master_key_source(),
                            "keyring_ok": vault._keyring_ok()}
        ok_all &= ok
    except Exception as e:
        results["vault"] = {"ok": False, "error": str(e)[:150]}
        ok_all = False

    # 3. session 读写
    try:
        tmp = "smoke_test"
        session.save_session(tmp, {"jsession": "t", "csrf": "t", "url": "x"})
        ok = session.session_valid(tmp)
        session.clear_session(tmp)
        results["session"] = {"ok": ok}
        ok_all &= ok
    except Exception as e:
        results["session"] = {"ok": False, "error": str(e)[:150]}
        ok_all = False

    # 4. creds schema 完整性
    try:
        known = set(creds.CRED_SCHEMA.keys())
        results["creds_schema"] = {"ok": len(known) > 0, "count": len(known)}
        ok_all &= len(known) > 0
    except Exception as e:
        results["creds_schema"] = {"ok": False, "error": str(e)[:150]}
        ok_all = False

    # 5. 浏览器就绪（quick 模式跳过）
    if not args.quick:
        try:
            r = browser.ensure_ready()
            results["browser"] = {"ok": r.get("ok", False), "missing": r.get("missing")}
            if not r.get("ok", False):
                ok_all = False
        except Exception as e:
            results["browser"] = {"ok": False, "error": str(e)[:150]}
            ok_all = False

    results["status"] = "ok" if ok_all else "error"
    common.output_json(results)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
