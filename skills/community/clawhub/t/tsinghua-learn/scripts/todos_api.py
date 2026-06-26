#!/usr/bin/env python3
"""
todos_api.py — 日常管理脚本
网络学堂代办总览 + 可选标记已读 + 可选清理工作区。

用法：
  python todos_api.py                                    # 纯代办汇总
  python todos_api.py --mark-read                        # 汇总 + 标记可读项已读
  python todos_api.py --cleanup-preview                  # 汇总 + 清理预览
  python todos_api.py --cleanup                          # 汇总 + 执行清理
  python todos_api.py --mark-read --cleanup              # 汇总 + 标已读 + 清理
"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from learn_api import LearnAPI
from ops import _fmt_size, _get_garbage, cleanup, sync_submissions_log, check_graded_submissions
from _config import get_semester, auto_mark_read


def build_summary():
    """构建完整代办汇总。返回 dict。"""
    api = LearnAPI()
    if not api.reload_session():
        return {"status": "error", "message": "Session 无效，请先运行 login_manager.py"}

    courses = api.get_courses()
    summary = {"semester": get_semester(), "courses": [], "total_unread": 0}

    # 同步已交未批改作业到日志，检查是否有新批改
    try:
        new_subs = sync_submissions_log(api)
        graded_hws = check_graded_submissions(api)
        if new_subs:
            summary["new_submissions_logged"] = new_subs
        if graded_hws:
            summary["graded_homeworks"] = graded_hws
        # 当前日志中的已提交未批改总数
        from ops import _read_log
        log = _read_log()
        if log:
            summary["submissions_tracked"] = len(log)
    except Exception:
        pass

    for c in courses:
        wlkcid = c["wlkcid"]
        kcm = c.get("kcm", "?")
        try:
            detail = api.get_course_detail(wlkcid)
        except Exception:
            continue

        unread_gg = [a for a in detail.get("announcements", []) if a.get("unread")]
        new_kj = [f for f in detail.get("files", []) if f.get("is_new")]
        unsubmitted_zy = [h for h in detail.get("homeworks", []) if h.get("status") == "未交"]
        active_tl = [t for t in detail.get("discussions", []) if int(t.get("replies", 0)) > 0]
        unanswered_wj = detail.get("questionnaires", [])

        course_data = {
            "name": kcm,
            "wlkcid": wlkcid,
            "unread_announcements": {
                "count": len(unread_gg),
                "items": [{"title": a["title"], "time": a["time"]} for a in unread_gg[:5]],
            },
            "new_files": {
                "count": len(new_kj),
                "items": [{"name": f["title"], "type": f["type"]} for f in new_kj[:5]],
            },
            "unsubmitted_homeworks": {
                "count": len(unsubmitted_zy),
                "items": [{"title": h["title"], "deadline": h["deadline"]} for h in unsubmitted_zy[:5]],
            },
            "active_discussions": {
                "count": len(active_tl),
                "items": [{"title": t["title"], "replies": t["replies"]} for t in active_tl[:5]],
            },
            "unanswered_questionnaires": {
                "count": len(unanswered_wj),
                "items": [{"title": q["title"], "deadline": q.get("deadline", "")} for q in unanswered_wj[:5]],
            },
        }
        total = len(unread_gg) + len(new_kj) + len(unsubmitted_zy) + len(active_tl) + len(unanswered_wj)
        course_data["total"] = total
        summary["total_unread"] += total
        summary["courses"].append(course_data)

    # 清理建议
    garbage = _get_garbage()
    if garbage:
        total_size = sum(g["size"] for g in garbage)
        summary["cleanup_suggestion"] = {
            "total_files": len(garbage),
            "total_size": total_size,
            "total_size_str": _fmt_size(total_size),
            "items": [{"name": g["name"], "size_str": _fmt_size(g["size"])} for g in garbage],
        }
    else:
        summary["cleanup_suggestion"] = None

    # 建议操作（给 AI 参考）
    suggestions = []
    if summary.get("cleanup_suggestion"):
        suggestions.append("运行 --cleanup-preview 查看可清理的文件")
    if suggestions:
        summary["suggestions"] = suggestions

    return summary


def do_mark_read(api, courses):
    """标记所有课程的可读项（公告+课件）为已读。返回汇总。"""
    results = {"announcements_marked": 0, "announcements_total": 0, "files_marked": 0, "files_total": 0}
    for c in courses:
        marked_gg, total_gg = api.mark_all_announcements_read(c["wlkcid"])
        results["announcements_marked"] += marked_gg
        results["announcements_total"] += total_gg
        marked_kj, total_kj = api.mark_all_files_read(c["wlkcid"])
        results["files_marked"] += marked_kj
        results["files_total"] += total_kj
    return results


# ====== CLI ======
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="网络学堂日常管理")
    parser.add_argument('--mark-read', action='store_true', help="标记可读项已读（需配合 --confirm）")
    parser.add_argument('--confirm', action='store_true', help="确认执行标记已读")
    parser.add_argument('--cleanup-preview', action='store_true', help="清理预览")
    parser.add_argument('--cleanup', action='store_true', help="执行清理")
    args = parser.parse_args()

    # auto_mark_read 为 true 时，先自动标记已读，再构建 summary
    mark_result = None
    if auto_mark_read() and not args.mark_read:
        api = LearnAPI()
        if api.reload_session():
            courses = api.get_courses()
            mark_result = do_mark_read(api, courses)

    # 先构建 summary
    summary = build_summary()
    if summary.get("status") == "error":
        print(json.dumps(summary, ensure_ascii=False))
        sys.exit(1)

    if mark_result:
        summary["mark_read_result"] = mark_result

    # 标记已读：--mark-read 时按 auto_mark_read 决定是否需确认
    if args.mark_read:
        api = LearnAPI()
        if not api.reload_session():
            print(json.dumps({"status": "error", "message": "Session 无效"}, ensure_ascii=False))
            sys.exit(1)
        courses = api.get_courses()
        if not args.confirm and not auto_mark_read():
            unread_count = sum(
                len([a for a in api.get_course_detail(c["wlkcid"]).get("announcements",[]) if a.get("unread")]) +
                len([f for f in api.get_course_detail(c["wlkcid"]).get("files",[]) if f.get("is_new")])
                for c in courses
            )
            print(json.dumps({
                "status": "pending",
                "requiring": "confirmation",
                "unread_items": unread_count,
                "message": "请确认标记以上未读项为已读。AI 必须获得用户明确同意后，添加 --confirm 重新执行"
            }, ensure_ascii=False))
            sys.exit(2)
        mark_result = do_mark_read(api, courses)
        summary["mark_read_result"] = mark_result

    # 未开启 auto_mark_read 时给出普通建议
    if not auto_mark_read() and summary["total_unread"] > 0:
        if "suggestions" not in summary:
            summary["suggestions"] = []
        summary["suggestions"].append("运行 --mark-read --confirm 标记公告和课件为已读")

    # 处理清理预览
    if args.cleanup_preview:
        summary["cleanup_preview"] = cleanup(dry_run=True)

    # 处理执行清理
    if args.cleanup:
        summary["cleanup_result"] = cleanup(dry_run=False)

    print(json.dumps(summary, ensure_ascii=False))
