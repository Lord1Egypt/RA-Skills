"""learn.py — 网络学堂子 SKILL 统一入口

AI 与主 SKILL 只调这一个脚本。JSON 输出 + session 自动保障。

Session 保障（两阶段）:
  本脚本会先尝试从 base-cas 读 learn session；无效时自动调
  base-cas login.py --system learn --ensure 登录。
   若返回 needs=2fa_code → 输出该状态，AI 引导用户输码后 submit-code。

CLI:
  learn.py courses                                   → 课程列表
  learn.py homeworks [--course <部分匹配>]           → 作业列表
  learn.py announcements [--course <部分匹配>]       → 公告
  learn.py files [--course <部分匹配>]               → 课件
  learn.py todos                                     → 待办汇总（复用 todos_api）
  learn.py download --course <名> [--pattern <glob>] → 下载课件
  learn.py homework-full --course <名> [--id <zyid>] → 作业详情
  learn.py mark-read                                 → 标已读
  learn.py aggregated                                → 各课汇总
"""
import sys
import os
import json
import argparse
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common
import learn_api
import ops

BASE_CAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "base-cas", "scripts", "login.py")


def _ensure_session():
    """确保 learn session 有效；失败时自动登录。返回 (api, ok)。"""
    api = learn_api.LearnAPI()
    if api.reload_session():
        return api, True
    # session 无效 → 自动登录（两阶段）
    common.log("[learn] session 无效，尝试自动登录")
    r = subprocess.run([sys.executable, BASE_CAS, "--system", "learn", "--ensure"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    try:
        out = json.loads(r.stdout or "{}")
    except Exception:
        out = {"status": "error", "raw": r.stdout[:200]}
    if out.get("status") == "pending" and out.get("needs") == "2fa_code":
        return None, out  # 需要 AI 引导用户输码
    if out.get("session_valid"):
        if api.reload_session():
            return api, True
        # login 声称成功但 reload 仍失败 → session 实际无效
        common.log("[learn] login 返回 ok 但 session 校验失败")
        return None, {"status": "error", "error": "session_invalid",
                      "message": "learn 登录态已过期且重登后仍无效，请重新执行 base-cas login.py --system learn --ensure（可能需重新 2FA）。"}
    return None, out


def _require_course(api, keyword):
    courses = api.get_courses()
    if keyword:
        courses = [c for c in courses if keyword in c.get("kcm", "")]
    if not courses:
        common.output_json({"status": "error", "message": "未找到课程" + (f"（含 '{keyword}'）" if keyword else "")})
        sys.exit(1)
    return courses


def cmd_courses(api, keyword):
    courses = _require_course(api, keyword)
    common.output_json({
        "status": "ok",
        "courses": [{
            "wlkcid": c.get("wlkcid"),
            "name": c.get("kcm"),
            "teacher": c.get("jsm"),
            "type": c.get("jslx"),
        } for c in courses],
    })


def cmd_todos():
    import todos_api
    summary = todos_api.build_summary()
    summary["status"] = summary.get("status", "ok")
    common.output_json(summary)


def cmd_homeworks(api, keyword):
    courses = _require_course(api, keyword)
    all_hw = []
    for c in courses:
        for h in api.get_homeworks(c["wlkcid"]):
            all_hw.append({
                "course": c.get("kcm"),
                "wlkcid": c.get("wlkcid"),
                "title": h.get("bt"),
                "status": h.get("zt"),
                "deadline": h.get("scsjStr"),
                "zyid": h.get("zyid"),
            })
    common.output_json({"status": "ok", "homeworks": all_hw})


def cmd_announcements(api, keyword):
    courses = _require_course(api, keyword)
    items = []
    for c in courses:
        for a in api.get_announcements(c["wlkcid"]):
            items.append({
                "course": c.get("kcm"),
                "title": a.get("bt"),
                "time": a.get("fbsjStr"),
                "unread": a.get("sfyd") == "否",
                "id": a.get("id", a.get("ggid", "")),
            })
    common.output_json({"status": "ok", "announcements": items})


def cmd_files(api, keyword):
    courses = _require_course(api, keyword)
    items = []
    for c in courses:
        for f in api.get_files(c["wlkcid"]):
            items.append({
                "course": c.get("kcm"),
                "name": f"{f.get('bt','?')}.{f.get('wjlx','?')}",
                "is_new": str(f.get("isNew", "")) == "1",
                "wjid": f.get("wjid"),
                "time": f.get("fssjStr", ""),
            })
    common.output_json({"status": "ok", "files": items})


def cmd_download(api, keyword, pattern):
    courses = _require_course(api, keyword)
    results = []
    for c in courses:
        files = api.get_files(c["wlkcid"])
        if pattern:
            import fnmatch
            files = [f for f in files if fnmatch.fnmatch(str(f.get("bt", "")).lower(), pattern.lower())]
        for f in files:
            path = api.download_file(c["wlkcid"], f["wjid"])
            results.append({"course": c.get("kcm"), "name": f"{f.get('bt','?')}.{f.get('wjlx','?')}", "path": path})
    common.output_json({"status": "ok", "downloaded": results})


def cmd_homework_full(api, keyword, zyid):
    courses = _require_course(api, keyword)
    out = []
    for c in courses:
        for h in api.get_homeworks(c["wlkcid"]):
            if zyid and zyid != h.get("zyid"):
                continue
            detail = api.get_homework_full_detail(c["wlkcid"], h["zyid"], h.get("xszyid", ""))
            detail.pop("raw_html_len", None)
            out.append({"course": c.get("kcm"), "title": h.get("bt"), "detail": detail})
    common.output_json({"status": "ok", "homework_full": out})


def cmd_mark_read(api, keyword):
    courses = _require_course(api, keyword)
    a_marked = a_total = 0
    f_marked = f_total = 0
    for c in courses:
        m, t = api.mark_all_announcements_read(c["wlkcid"])
        a_marked += m; a_total += t
        m, t = api.mark_all_files_read(c["wlkcid"])
        f_marked += m; f_total += t
    common.output_json({"status": "ok", "announcements_marked": f"{a_marked}/{a_total}", "files_marked": f"{f_marked}/{f_total}"})


def cmd_aggregated(api, keyword):
    courses = _require_course(api, keyword)
    out = []
    for c in courses:
        detail = api.get_course_detail(c["wlkcid"])
        out.append({"course": c.get("kcm"), "counts": {k: len(v) for k, v in detail.items()}})
    common.output_json({"status": "ok", "aggregated": out})


def main():
    ap = argparse.ArgumentParser(description="网络学堂统一入口")
    ap.add_argument("cmd", choices=["courses", "todos", "homeworks", "announcements",
                                    "files", "download", "homework-full", "mark-read", "aggregated"])
    ap.add_argument("--course", default=None, help="课程名部分匹配")
    ap.add_argument("--pattern", default=None, help="下载文件通配符（如 *.pdf）")
    ap.add_argument("--id", default=None, help="条目 ID（zyid 等）")
    args = ap.parse_args()

    if args.cmd == "todos":
        cmd_todos()
        return

    api, ok = _ensure_session()
    if isinstance(ok, dict) and ok.get("status") == "pending" and ok.get("needs") == "2fa_code":
        common.output_json({
            "status": "pending",
            "needs": "2fa_code",
            "pending": ok.get("pending"),
            "message": "需要二次验证。请让用户提供短信验证码，然后调用 base-cas login.py --submit-code <token> <code>，完成后重试本命令。",
        })
        sys.exit(2)
    if not ok or api is None:
        # 透传 login.py 的具体错误（如 trust_limit / cas_credential / code_invalid / 凭据未配置）
        if isinstance(ok, dict):
            err = ok.get("error")
            msg = ok.get("message") or ("登录失败" if err else "learn session 无法建立")
            out = {
                "status": "error",
                "error": err or "session_unavailable",
                "message": msg,
            }
            if ok.get("needs"):
                out["needs"] = ok["needs"]
                if ok.get("run"):
                    out["run"] = ok["run"]
            if err:
                out["detail"] = ok
            common.output_json(out)
        else:
            common.output_json({"status": "error", "message": "learn session 无法建立", "detail": str(ok)})
        sys.exit(1)

    if args.cmd == "courses":
        cmd_courses(api, args.course)
    elif args.cmd == "homeworks":
        cmd_homeworks(api, args.course)
    elif args.cmd == "announcements":
        cmd_announcements(api, args.course)
    elif args.cmd == "files":
        cmd_files(api, args.course)
    elif args.cmd == "download":
        cmd_download(api, args.course, args.pattern)
    elif args.cmd == "homework-full":
        cmd_homework_full(api, args.course, args.id)
    elif args.cmd == "mark-read":
        cmd_mark_read(api, args.course)
    elif args.cmd == "aggregated":
        cmd_aggregated(api, args.course)


if __name__ == "__main__":
    main()
