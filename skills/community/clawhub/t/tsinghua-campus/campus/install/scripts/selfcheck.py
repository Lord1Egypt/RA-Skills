"""selfcheck.py — 技能包环境自检

检查: Python 版本 / playwright / chromium / runtime 目录 / 凭据配置状态
输出 JSON，AI 据结果决定下一步（缺什么装什么）。

CLI:
  selfcheck.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "base-cas", "scripts"))
import common
import browser


def main():
    report = {}
    # Python
    v = sys.version_info
    report["python"] = {"ok": (v.major, v.minor) >= (3, 10), "version": f"{v.major}.{v.minor}.{v.micro}"}
    # playwright / chromium
    r = browser.ensure_ready()
    report["playwright"] = {"ok": r.get("ok", False)}
    report["chromium"] = {"ok": r.get("ok", False), "path": r.get("chromium")}
    if r.get("missing"):
        report["missing"] = r["missing"]
    # runtime 目录
    report["runtime"] = {
        "ok": True,
        "dirs": {
            "profiles": os.path.isdir(str(common.runtime_dir("profiles"))),
            "sessions": os.path.isdir(str(common.runtime_dir("sessions"))),
        },
    }
    # 凭据配置状态
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "creds", "scripts"))
        import creds
        saved = creds._load_creds()
        configured = [k for k, v in saved.items() if v]
        report["creds"] = {"configured": configured, "all_configured": False}
    except Exception as e:
        report["creds"] = {"ok": False, "error": str(e)[:100]}

    all_ok = report["python"]["ok"] and report["chromium"]["ok"]
    report["status"] = "ok" if all_ok else "error"
    common.output_json(report)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
