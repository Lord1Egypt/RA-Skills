#!/usr/bin/env python3
"""
ops.py — 文件操作统一入口
功能：下载、上传、移入工作区、清理垃圾。
所有文件格式通用，不上传/下载路径硬编码。
"""
import sys, os, json, shutil, fnmatch
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import get_download_dir_abs, get_upload_dir, get_semester, \
    get_student_id, get_student_name, get_username, get_submissions_log
from learn_api import LearnAPI, LEARN_BASE

DOWNLOAD_DIR = get_download_dir_abs()
UPLOAD_DIR = get_upload_dir()


def _fmt_size(n):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def ensure_api():
    """获取已验证的 LearnAPI 实例。失败时退出。"""
    api = LearnAPI()
    if not api.reload_session():
        print("Session 无效，请先运行 login_manager.py", file=sys.stderr)
        raise SystemExit(1)
    return api


# ── 下载 ──────────────────────────────────────

def list_course_files(wlkcid, pattern=None):
    """列出课程文件，可选通配符过滤。返回文件信息列表。"""
    api = ensure_api()
    files = api.get_files(wlkcid)
    if pattern:
        files = [f for f in files if fnmatch.fnmatch(f.get('bt', '').lower(), pattern.lower())]
    return [{
        "wjid": f.get("wjid", ""),
        "name": f"{f.get('bt','?')}.{f.get('wjlx','?')}",
        "type": f.get("wjlx", ""),
        "is_new": str(f.get("isNew", "")) == "1",
        "time": f.get("fssjStr", f.get("cjsjStr", "")),
    } for f in files]


def download_file(wlkcid, wjid, filename=None, save_dir=None):
    """下载单个文件。返回保存路径或 None。"""
    api = ensure_api()
    path = api.download_file(wlkcid, wjid, filename=filename, save_dir=save_dir or DOWNLOAD_DIR)
    if path:
        size = os.path.getsize(path)
        print(json.dumps({"status": "ok", "path": path, "size": size, "size_str": _fmt_size(size)}))
    else:
        print(json.dumps({"status": "error", "message": "下载失败"}), file=sys.stderr)
    return path


def download_batch(wlkcid, wjid_list, save_dir=None):
    """批量下载文件。wjid_list 为 wjid 列表。返回路径列表。"""
    api = ensure_api()
    results = []
    for wjid in wjid_list:
        path = api.download_file(wlkcid, wjid, save_dir=save_dir or DOWNLOAD_DIR)
        if path:
            results.append(path)
    print(json.dumps({"status": "ok", "downloaded": len(results), "failed": len(wjid_list) - len(results), "paths": results}))
    return results


def download_all(wlkcid, pattern=None, save_dir=None):
    """下载课程所有（或匹配 pattern 的）文件。先 list 再批量下载。"""
    files = list_course_files(wlkcid, pattern)
    if not files:
        print(json.dumps({"status": "ok", "downloaded": 0, "message": "无匹配文件", "files": []}))
        return []
    wjids = [f["wjid"] for f in files]
    return download_batch(wlkcid, wjids, save_dir)


# ── 上传 ──────────────────────────────────────

def upload_homework(wlkcid, xszyid, file_path):
    """提交作业。自动重命名为 '学号_姓名.扩展名'。返回 bool。"""
    api = ensure_api()
    sid = get_username()
    sname = get_student_name()
    ext = os.path.splitext(file_path)[1]
    renamed = os.path.join(os.path.dirname(file_path), f"{sid}_{sname}{ext}")
    if file_path != renamed:
        shutil.copy2(file_path, renamed)
        upload_path = renamed
    else:
        upload_path = file_path

    ok = api.submit_homework(wlkcid, xszyid, upload_path, content="")
    if upload_path != file_path and os.path.exists(upload_path):
        os.remove(upload_path)
    print(json.dumps({"status": "ok" if ok else "error", "message": "提交成功" if ok else "提交失败"}))
    return ok


# ── 提交记录 ──────────────────────────────────

SUBMISSIONS_LOG = get_submissions_log()


def _read_log():
    """读取提交记录日志。返回 dict（key=xszyid）。"""
    if not os.path.exists(SUBMISSIONS_LOG):
        return {}
    with open(SUBMISSIONS_LOG, encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}


def _write_log(data):
    with open(SUBMISSIONS_LOG, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def sync_submissions_log(api):
    """
    在查看待办时调用：扫描所有已交未批改作业，追加到日志（已存在则跳过）。
    返回新增数量。
    """
    log = _read_log()
    courses = api.get_courses()
    new_count = 0
    for c in courses:
        wlkcid = c["wlkcid"]
        data = {"aoData": [{"name": "wlkcid", "value": wlkcid}]}
        d = api._post("/b/wlxt/kczy/zy/student/zyListYjwg", data, use_ajax=True)
        items = d.get("object", {}).get("aaData", [])
        for h in items:
            xszyid = h.get("xszyid", "")
            if not xszyid or xszyid in log:
                continue
            log[xszyid] = {
                "wlkcid": wlkcid,
                "course": c.get("kcm", ""),
                "xszyid": xszyid,
                "zyid": h.get("zyid", ""),
                "title": h.get("bt", ""),
            }
            new_count += 1
    if new_count:
        _write_log(log)
    return new_count


def check_graded_submissions(api):
    """
    遍历日志，检查是否有作业已被批改。
    已批改的：获取评语/分数，从日志中移除，返回报告列表。
    """
    log = _read_log()
    graded = []
    to_remove = []
    for xszyid, entry in log.items():
        try:
            hws = api.get_homeworks(entry["wlkcid"])
            for h in hws:
                if h.get("xszyid") == xszyid and h.get("zt") == "\u5df2\u6279\u6539":
                    detail = api.get_homework_full_detail(entry["wlkcid"], h.get("zyid", ""), xszyid)
                    graded.append({
                        "course": entry.get("course", ""),
                        "title": entry.get("title", ""),
                        "score": detail.get("score", ""),
                        "comment": (detail.get("comment", "") or "")[:200],
                    })
                    to_remove.append(xszyid)
                    break
        except Exception:
            continue
    for xszyid in to_remove:
        del log[xszyid]
    if to_remove:
        _write_log(log)
    return graded


# ── PDF 合并 ──────────────────────────────────

def pdf_merge(input_dir, output=None):
    """合并目录中的图片为 PDF，按文件名排序。返回 {status, path, pages}。"""
    from pdf_merge import merge
    return merge(input_dir, output)


# ── 移入工作区 ──────────────────────────────

def move_to_workspace(source_path):
    """将外部文件移入 uploads/ 目录。返回目标路径。"""
    if not os.path.exists(source_path):
        print(json.dumps({"status": "error", "message": f"源文件不存在: {source_path}"}), file=sys.stderr)
        return None
    target = os.path.join(UPLOAD_DIR, os.path.basename(source_path))
    shutil.move(source_path, target)
    print(json.dumps({"status": "ok", "path": target, "size": os.path.getsize(target), "size_str": _fmt_size(os.path.getsize(target))}))
    return target


# ── 清理 ──────────────────────────────────────

def _get_garbage():
    """扫描垃圾文件。返回列表。"""
    garbage = []
    garbage_dirs = [
        DOWNLOAD_DIR,
        UPLOAD_DIR,
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sessions"),
    ]
    for d in garbage_dirs:
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            fpath = os.path.join(d, name)
            if os.path.isfile(fpath) and (name.endswith('.html') or name.endswith('.tmp') or name.endswith('.json')):
                if name == 'learn_session.json':
                    continue  # 保留 session 文件
                garbage.append({"path": fpath, "size": os.path.getsize(fpath), "name": name})
    # __pycache__
    pycache = os.path.join(os.path.dirname(os.path.abspath(__file__)), "__pycache__")
    if os.path.isdir(pycache):
        total = sum(os.path.getsize(os.path.join(pycache, f)) for f in os.listdir(pycache) if os.path.isfile(os.path.join(pycache, f)))
        garbage.append({"path": pycache, "size": total, "name": "__pycache__"})
    return garbage


def cleanup(dry_run=True):
    """清理工作区垃圾文件。
    dry_run=True: 只列出不删除。
    dry_run=False: 列出并删除。
    返回操作结果 dict。
    """
    garbage = _get_garbage()
    total_size = sum(g["size"] for g in garbage)
    result = {
        "status": "preview" if dry_run else "done",
        "total_files": len(garbage),
        "total_size": total_size,
        "total_size_str": _fmt_size(total_size),
        "items": [{"name": g["name"], "size_str": _fmt_size(g["size"]), "path": g["path"]} for g in garbage],
    }

    if not dry_run:
        for g in garbage:
            if os.path.isfile(g["path"]):
                os.remove(g["path"])
            elif os.path.isdir(g["path"]):
                shutil.rmtree(g["path"], ignore_errors=True)
        result["status"] = "done"
    elif garbage:
        result["suggestion"] = "运行 cleanup (不带 --dry-run) 执行清理"

    print(json.dumps(result, ensure_ascii=False))
    return result


# ====== CLI ======
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="文件操作工具")
    parser.add_argument('--action', required=True,
                        choices=['download', 'download-all', 'list-files',
                                 'upload', 'move-in', 'cleanup', 'pdf-merge'])
    parser.add_argument('--course', default=None, help='wlkcid')
    parser.add_argument('--wjid', default=None, help='文件 ID')
    parser.add_argument('--wjid-list', default=None, help='文件 ID 列表（逗号分隔）')
    parser.add_argument('--pattern', default=None, help='通配符过滤（如 "*.pdf"）')
    parser.add_argument('--file', default=None, help='文件路径')
    parser.add_argument('--xszyid', default=None, help='学生作业 ID')
    parser.add_argument('--save-dir', default=None, help='保存目录')
    parser.add_argument('--input-dir', default=None, help='PDF 合并输入目录')
    parser.add_argument('--output', default=None, help='输出路径')
    parser.add_argument('--dry-run', action='store_true', help='清理预览模式')
    parser.add_argument('--confirm', action='store_true', help='上传作业确认（必需）')
    args = parser.parse_args()

    if args.action == 'list-files':
        if not args.course:
            print("需要 --course", file=sys.stderr); sys.exit(1)
        files = list_course_files(args.course, args.pattern)
        result = {"count": len(files), "files": files}
        if files:
            result["suggestion"] = "使用 download 或 download-all 下载文件"
        print(json.dumps(result, ensure_ascii=False))

    elif args.action == 'download':
        if not args.course or not args.wjid:
            print("需要 --course 和 --wjid", file=sys.stderr); sys.exit(1)
        download_file(args.course, args.wjid, save_dir=args.save_dir)

    elif args.action == 'download-all':
        if not args.course:
            print("需要 --course", file=sys.stderr); sys.exit(1)
        download_all(args.course, args.pattern, args.save_dir)

    elif args.action == 'upload':
        if not args.course or not args.xszyid or not args.file:
            print("需要 --course --xszyid --file", file=sys.stderr); sys.exit(1)
        if not args.confirm:
            print(json.dumps({
                "status": "pending",
                "requiring": "confirmation",
                "details": {
                    "course": args.course,
                    "xszyid": args.xszyid,
                    "file": args.file,
                },
                "message": "请确认提交以上文件到指定作业。AI 必须获得用户明确同意后，添加 --confirm 重新执行"
            }, ensure_ascii=False))
            sys.exit(2)
        upload_homework(args.course, args.xszyid, args.file)

    elif args.action == 'move-in':
        if not args.file:
            print("需要 --file", file=sys.stderr); sys.exit(1)
        move_to_workspace(args.file)

    elif args.action == 'cleanup':
        cleanup(dry_run=args.dry_run)

    elif args.action == 'pdf-merge':
        if not args.input_dir:
            print("需要 --input-dir", file=sys.stderr); sys.exit(1)
        result = pdf_merge(args.input_dir, args.output)
        print(json.dumps(result, ensure_ascii=False))
