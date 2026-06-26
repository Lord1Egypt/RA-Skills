#!/usr/bin/env python3
"""SJTU Canvas API 核心模块 - 课程/文件/作业/成绩/讨论区"""

import os
import sys
import json
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path

TZ_SHANGHAI = timezone(timedelta(hours=8))

# Search for config.json: script dir → skill dir → workspace skill dir
def _find_config():
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"),
        os.path.expanduser("~/.openclaw/workspace/skills/sjtu-canvas/config.json"),
    ]
    for p in candidates:
        p = os.path.normpath(p)
        if os.path.exists(p):
            return p
    return None

def load_config():
    path = _find_config()
    if path:
        with open(path) as f:
            return json.load(f)
    return {}

def get_token():
    config = load_config()
    token = config.get("canvas_token", "")
    if not token:
        print("ERROR: Canvas token not configured. Set it in config.json")
        sys.exit(1)
    return token

def get_base_url():
    config = load_config()
    return config.get("base_url", "https://oc.sjtu.edu.cn")

def headers():
    return {"Authorization": f"Bearer {get_token()}"}

def api_get(path, params=None):
    url = f"{get_base_url()}{path}"
    items = []
    while url:
        r = requests.get(url, headers=headers(), params=params)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list):
            items.extend(data)
        else:
            return data
        # 分页
        links = r.headers.get("Link", "")
        url = None
        for link in links.split(","):
            if 'rel="next"' in link:
                url = link.split("<")[1].split(">")[0]
        params = None  # 后续页面 URL 已包含参数
    return items

# ===== 用户 =====
def get_me():
    return api_get("/api/v1/users/self")

# ===== 课程 =====
def list_courses():
    return api_get("/api/v1/courses", {"enrollment_state": "active", "per_page": 50})

# ===== 文件 =====
def list_course_files(course_id, search_term=None):
    params = {"per_page": 100}
    if search_term:
        params["search_term"] = search_term
    return api_get(f"/api/v1/courses/{course_id}/files", params)

def list_course_folders(course_id):
    return api_get(f"/api/v1/courses/{course_id}/folders", {"per_page": 100})

def download_file(file_url, save_path):
    r = requests.get(file_url, headers=headers(), stream=True)
    r.raise_for_status()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return save_path

def download_course_files(course_id, course_name, save_dir, extensions=None):
    """批量下载课程文件，可按扩展名过滤"""
    files = list_course_files(course_id)
    downloaded = []
    for f in files:
        name = f.get("display_name", "")
        if extensions:
            ext = os.path.splitext(name)[1].lower()
            if ext not in extensions:
                continue
        save_path = os.path.join(save_dir, course_name, name)
        if os.path.exists(save_path):
            downloaded.append(save_path)
            continue
        try:
            download_file(f["url"], save_path)
            downloaded.append(save_path)
            print(f"  ✅ {name}")
        except Exception as e:
            print(f"  ❌ {name}: {e}")
    return downloaded

# ===== 作业 =====
def list_assignments(course_id):
    return api_get(f"/api/v1/courses/{course_id}/assignments", {"per_page": 50, "order_by": "due_at"})

def get_assignment(course_id, assignment_id):
    return api_get(f"/api/v1/courses/{course_id}/assignments/{assignment_id}")

def get_my_submission(course_id, assignment_id):
    return api_get(f"/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/self")

def submit_assignment(course_id, assignment_id, file_paths):
    """上传文件并提交作业"""
    token = get_token()
    h = headers()
    uploaded_ids = []
    for fp in file_paths:
        fname = os.path.basename(fp)
        fsize = os.path.getsize(fp)
        # Step 1: 请求上传
        r = requests.post(
            f"{get_base_url()/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/self/files",
            headers=h,
            data={"name": fname, "size": fsize}
        )
        r.raise_for_status()
        upload_info = r.json()
        # Step 2: 上传文件
        with open(fp, "rb") as f:
            r2 = requests.post(
                upload_info["upload_url"],
                data=upload_info.get("upload_params", {}),
                files={"file": (fname, f)}
            )
            r2.raise_for_status()
            uploaded_ids.append(r2.json()["id"])
    # Step 3: 提交
    r3 = requests.post(
        f"{get_base_url()/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions",
        headers=h,
        data={
            "submission[submission_type]": "online_upload",
            **{f"submission[file_ids][{i}]": fid for i, fid in enumerate(uploaded_ids)}
        }
    )
    r3.raise_for_status()
    return r3.json()

# ===== 成绩 =====
def get_course_grades(course_id):
    assignments = list_assignments(course_id)
    results = []
    for a in assignments:
        sub = a.get("submission", {})
        results.append({
            "name": a["name"],
            "points_possible": a.get("points_possible"),
            "score": sub.get("score") if sub else None,
            "grade": sub.get("grade") if sub else None,
            "workflow_state": sub.get("workflow_state", "") if sub else "",
            "due_at": a.get("due_at"),
        })
    return results

# ===== 讨论区 =====
def list_discussions(course_id):
    return api_get(f"/api/v1/courses/{course_id}/discussion_topics", {"per_page": 50})

def get_full_discussion(course_id, topic_id):
    return api_get(f"/api/v1/courses/{course_id}/discussion_topics/{topic_id}/view")

# ===== DDL 汇总 =====
def get_all_upcoming_ddls():
    """获取所有课程的未来DDL"""
    now = datetime.now(TZ_SHANGHAI)
    courses = list_courses()
    ddls = []
    for c in courses:
        try:
            assignments = list_assignments(c["id"])
        except:
            continue
        for a in assignments:
            due = a.get("due_at")
            if not due:
                continue
            due_dt = datetime.fromisoformat(due.replace("Z", "+00:00")).astimezone(TZ_SHANGHAI)
            if due_dt > now:
                sub = a.get("submission", {})
                workflow = sub.get("workflow_state", "") if sub else ""
                ddls.append({
                    "course": c.get("name", ""),
                    "course_id": c["id"],
                    "assignment": a["name"],
                    "assignment_id": a["id"],
                    "due_at": due,
                    "due_local": due_dt.strftime("%Y-%m-%d %H:%M"),
                    "submitted": workflow in ["submitted", "graded"],
                    "points": a.get("points_possible"),
                })
    ddls.sort(key=lambda x: x["due_at"])
    return ddls

# ===== 日历事件 =====
def list_calendar_events(course_ids, start_date, end_date):
    context_codes = [f"course_{cid}" for cid in course_ids]
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "per_page": 100,
    }
    for i, cc in enumerate(context_codes):
        params[f"context_codes[{i}]"] = cc
    return api_get("/api/v1/calendar_events", params)

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "courses"
    
    if cmd == "courses":
        for c in list_courses():
            print(f"[{c['id']}] {c['name']}")
    elif cmd == "ddls":
        for d in get_all_upcoming_ddls():
            status = "✅" if d["submitted"] else "❌"
            print(f"{status} [{d['course']}] {d['assignment']} → {d['due_local']}")
    elif cmd == "grades":
        for c in list_courses():
            grades = get_course_grades(c["id"])
            scored = [g for g in grades if g["score"] is not None]
            if scored:
                print(f"\n📚 {c['name']}:")
                for g in scored:
                    print(f"  {g['name']}: {g['score']}/{g['points_possible']}")
    elif cmd == "me":
        me = get_me()
        print(f"用户: {me['name']} (ID: {me['id']})")
