"""session.py — 多系统 session 隔离

每个校内系统（learn/info/seat/…）有自己的 session（JSESSIONID + CSRF 等），
按系统名分文件存 runtime/sessions/<system>.json，互不串扰。

接口:
  load_session(system) -> dict | None
  save_session(system, data)
  clear_session(system)
  session_valid(system) -> bool   # 存在且含必需字段
"""
import sys
import os
import json
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common


def _path(system):
    d = common.session_dir()
    d.mkdir(parents=True, exist_ok=True)
    return os.path.join(str(d), f"{system}.json")


def load_session(system):
    p = _path(system)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def save_session(system, data):
    data = dict(data)
    data["_updated"] = time.time()
    with open(_path(system), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clear_session(system):
    p = _path(system)
    if os.path.exists(p):
        os.remove(p)


def session_valid(system, required_fields=None):
    """存在且含必需字段才有效。字段按系统区分：
    - direct（learn）: jsession + csrf
    - webvpn（info/seat）: ticket（wengine_vpn_ticket）
    """
    if required_fields is None:
        required_fields = ("jsession", "csrf") if system != "info" else ("ticket",)
    s = load_session(system)
    if not s:
        return False
    return all(s.get(k) for k in required_fields)


def load_cookies(system):
    """取 session 里保存的完整 cookie 快照（login.py _extract_session 写入）。

    浏览器即用即退后，跨进程的信任态靠这些 cookie + profile 指纹恢复。
    返回 playwright 可直接 add_cookies 的列表，无则返回 []。
    """
    s = load_session(system)
    if not s:
        return []
    ck = s.get("_cookies") or []
    return [c for c in ck if c.get("name") and c.get("value")]


def inject_cookies(context, system):
    """把已保存的系统 cookie 注入 playwright context（供 CDP 复用前恢复会话）。"""
    ck = load_cookies(system)
    if not ck:
        return 0
    try:
        context.add_cookies(ck)
        return len(ck)
    except Exception:
        return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="列出所有已存 session")
    args = ap.parse_args()
    if args.list:
        sessions = {}
        sd = common.session_dir()
        if os.path.isdir(sd):
            for f in os.listdir(sd):
                if f.endswith(".json") and f != "pending":
                    try:
                        s = json.load(open(os.path.join(sd, f), encoding="utf-8"))
                        sessions[f[:-5]] = {
                            "exists": True,
                            "age_h": round((time.time() - s.get("_updated", 0)) / 3600, 1),
                        }
                    except Exception:
                        sessions[f[:-5]] = {"exists": True, "corrupt": True}
        common.output_json({"status": "ok", "sessions": sessions})
