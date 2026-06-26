#!/usr/bin/env python3
"""
Session管理工具模块
提供session的读取、设置、重置、验证以及课程进度管理功能
"""

import json
import os
import sys
from datetime import datetime
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

SESSION_FILE = os.environ.get("_WANGDA_SESSION_FILE")


def get_session(key=None):
    """
    获取当前session

    Args:
        key: 可选，session的某个字段名，如果不填则返回整个session

    Returns:
        session文件中的内容，如果没有返回空对象{}
    """
    if not SESSION_FILE or not os.path.exists(SESSION_FILE):
        return {}

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session = json.load(f)

        if key:
            value = session.get(key)
            if value is None:
                return {}
            return value
        else:
            return session

    except (json.JSONDecodeError, IOError):
        return {}


def set_session(key, value):
    """
    设置session的某个字段

    Args:
        key: 字段名
        value: 字段值

    Returns:
        设置成功或失败
    """
    if not SESSION_FILE:
        print("Error: _WANGDA_SESSION_FILE环境变量未设置")
        sys.exit(1)

    # 读取现有session
    session = {}
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                session = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    # 当value为空时，删除key；否则解析JSON并设置
    if value == "":
        session.pop(key, None)
        action_msg = f"删除成功: {key}"
    else:
        # 尝试解析值为JSON
        try:
            parsed_value = json.loads(value)
        except json.JSONDecodeError:
            # JSON解析失败，检查是否是大小写不敏感的布尔值
            if value.lower() == "true":
                parsed_value = True
            elif value.lower() == "false":
                parsed_value = False
            else:
                parsed_value = value
        session[key] = parsed_value
        action_msg = f"设置成功: {key}"

    # 保存session
    try:
        os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
        print(action_msg)
        return True
    except IOError as e:
        print(f"保存失败: {e}")
        sys.exit(1)


def remove_session_file():
    if not SESSION_FILE or not os.path.exists(SESSION_FILE):
        return
    try:
        os.remove(SESSION_FILE)
    except Exception as e:
        print(f"删除session文件失败: {e}")


def reset_session():
    """
    重置session

    Returns:
        返回重置后的session内容
    """
    session = {
        "debugPort": int(os.environ.get("_WANGDA_DEBUG_PORT", "0")),
        "userDataDir": os.environ.get("_WANGDA_USER_DATA_DIR", ""),
        "createdTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    if SESSION_FILE:
        os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(session, f, ensure_ascii=False, indent=2)

    print(json.dumps(session, ensure_ascii=False, indent=2))
    return session


def add_progress(subject_progress):
    """
    添加课程进度

    Args:
        subject_progress: 课程进度信息（JSON格式字符串）

    Returns:
        添加成功或失败
    """
    if not SESSION_FILE:
        print("Error: _WANGDA_SESSION_FILE环境变量未设置")
        sys.exit(1)

    # 解析subject_progress
    try:
        item = json.loads(subject_progress)
    except json.JSONDecodeError as e:
        print(f"解析失败，无效的JSON格式: {e}")
        sys.exit(1)

    if not isinstance(item, dict) or "id" not in item or "name" not in item:
        print("Error: 无效的subject-progress格式，必须包含id和name字段")
        sys.exit(1)

    # 读取现有session
    session = {}
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                session = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    if "progress" not in session:
        session["progress"] = {"subjects": []}

    item_type = item.get("type")
    item_id = item.get("id")

    if item_type == "subject" or (not item_type and "courses" in item):
        # subject 直接加到 progress.subjects
        items = session["progress"].setdefault("subjects", [])
        item["type"] = "subject"

        for i, existing in enumerate(items):
            if existing.get("id") == item_id:
                items[i] = item
                print(f"更新subject成功: {item.get('name', item_id)}")
                break
        else:
            items.append(item)
            print(f"添加subject成功: {item.get('name', item_id)}")

    elif item_type == "course" or not item_type:
        # course 必须加到其父 subject 的 courses 下
        item["type"] = "course"
        subjects = session["progress"].setdefault("subjects", [])

        # 从 course URL 中提取父 subject ID
        # URL格式: .../subject-course/{course_id}/{type}/{subject_id}
        parent_subject_id = None
        course_url = item.get("url", "")
        if "subject-course" in course_url:
            parts = course_url.split("/")
            try:
                sc_idx = parts.index("subject-course")
                if sc_idx + 3 < len(parts):
                    parent_subject_id = parts[sc_idx + 3]
            except (ValueError, IndexError):
                pass

        # 也检查 _parentSubject 字段（get_next_course 可能附加的）
        parent_info = item.pop("_parentSubject", None)
        if not parent_subject_id and parent_info:
            parent_subject_id = parent_info.get("id")

        if parent_subject_id:
            # 找到父 subject 并将 course 加到其 courses 下
            parent_found = False
            for subject in subjects:
                if subject.get("id") == parent_subject_id:
                    courses = subject.setdefault("courses", [])
                    for i, existing in enumerate(courses):
                        if existing.get("id") == item_id:
                            courses[i] = item
                            print(f"更新course成功: {item.get('name', item_id)} (subject: {subject.get('name')})")
                            parent_found = True
                            break
                    else:
                        courses.append(item)
                        print(f"添加course成功: {item.get('name', item_id)} (subject: {subject.get('name')})")
                        parent_found = True
                    break
                # 递归检查子 subject
                for sub in subject.get("subjects", []):
                    if sub.get("id") == parent_subject_id:
                        courses = sub.setdefault("courses", [])
                        for i, existing in enumerate(courses):
                            if existing.get("id") == item_id:
                                courses[i] = item
                                parent_found = True
                                break
                        else:
                            courses.append(item)
                            parent_found = True
                        if parent_found:
                            print(f"更新course成功: {item.get('name', item_id)} (subject: {sub.get('name')})")
                            break

            if not parent_found:
                print(f"警告: 未找到父subject(id={parent_subject_id})，course未添加: {item.get('name')}")
        else:
            print(f"警告: 无法确定course的父subject，course未添加: {item.get('name')}")

    # 保存session
    try:
        os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"保存失败: {e}")
        sys.exit(1)


def get_next_course():
    """
    获取下一个需要学习的课件(course)

    Returns:
        课件信息，如果已经全部完成或其他原因没有待学习的课件，
        则返回没有对应的课件的原因
    """
    if not SESSION_FILE or not os.path.exists(SESSION_FILE):
        print("不存在有效session")
        raise Exception("不存在有效session")

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session = json.load(f)
    except (json.JSONDecodeError, IOError):
        print("不存在有效session")
        raise Exception("不存在有效session")

    if not isinstance(session, dict):
        print("不存在有效session")
        raise Exception("不存在有效session")

    progress = session.get("progress", {})
    subjects = progress.get("subjects", [])

    if not subjects:
        print("尚未加入任何待学习课程")
        return {}

    # 递归搜索所有 subject（包括子 subject）中的未完成 course
    def _find_uncompleted_course(subject_list):
        for subject in subject_list:
            if subject.get("completed", False):
                continue
            # 先检查该 subject 下的 courses
            for course in subject.get("courses", []):
                if not course.get("completed", False):
                    course_info = {
                        **course,
                        "_parentSubject": {
                            "id": subject.get("id"),
                            "name": subject.get("name"),
                        },
                    }
                    return course_info
            # 再检查子 subject
            result = _find_uncompleted_course(subject.get("subjects", []))
            if result:
                return result
        return None

    result = _find_uncompleted_course(subjects)
    if result:
        return result

    # 所有课程都已完成
    print("所有课程均已完成")

    # 更新completed状态
    session["completed"] = True
    for s in subjects:
        s["completed"] = True

    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
    except IOError:
        pass

    return {}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Session管理工具")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # get-session command
    get_session_cmd = subparsers.add_parser("get-session", help="获取当前session")
    get_session_cmd.add_argument(
        "key", nargs="?", type=str, help="session字段名（可选）"
    )

    # set-session command
    set_session_cmd = subparsers.add_parser("set-session", help="设置session的某个字段")
    set_session_cmd.add_argument("key", type=str, help="字段名")
    set_session_cmd.add_argument("value", type=str, help="字段值")

    # reset-session command
    subparsers.add_parser("reset-session", help="重置session")

    # add-progress command
    add_progress_cmd = subparsers.add_parser("add-progress", help="添加课程进度")
    add_progress_cmd.add_argument(
        "subject_progress", type=str, help="课程进度信息（JSON格式）"
    )

    # get-next-course command
    subparsers.add_parser("get-next-course", help="获取下一个需要学习的课件")

    args = parser.parse_args()

    if args.command == "get-session":
        print(json.dumps(get_session(args.key), ensure_ascii=False, indent=2))
    elif args.command == "set-session":
        set_session(args.key, args.value)
    elif args.command == "reset-session":
        reset_session()
    elif args.command == "add-progress":
        add_progress(args.subject_progress)
    elif args.command == "get-next-course":
        print(json.dumps(get_next_course(), ensure_ascii=False, indent=2))
    else:
        parser.print_help()
