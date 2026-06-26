#!/usr/bin/env python3
"""
课程相关工具模块
提供解析课程/专题信息和自动学习功能
"""

import json
import os
import re
import sys
import time
import urllib.request
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

# 引入chrome_tools中的函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chrome_tools import dump_page, navi


def get_url_type(url):
    """判断URL类型"""
    if "wangda.chinamobile.com" not in url:
        return "other"
    if "study/subject/detail" in url:
        return "subject"
    elif "study/course/detail" in url:
        return "course"
    return "other"


def parse_course_doc(document_file, url=""):
    """从dump的document文件中解析课程信息"""
    with open(document_file, "r", encoding="utf-8") as f:
        doc = json.load(f)

    course_id = ""

    # 1. 递归提取整个DOM的文本内容，并顺便抓取 courseid
    def find_title(node):
        if node.get("nodeName", "").upper() == "TITLE":
            for c in node.get("children", []):
                if c.get("nodeName") == "#text":
                    return c.get("nodeValue", "").strip()
        for c in node.get("children", []):
            res = find_title(c)
            if res:
                return res
        return ""

    flat_texts = []

    def traverse(node):
        nonlocal course_id

        attrs = node.get("attributes", [])
        if attrs and isinstance(attrs, list):
            for i in range(len(attrs) - 1):
                if attrs[i] == "data-courseid" and not course_id:
                    course_id = attrs[i + 1]

        if node.get("nodeName") == "#text":
            val = node.get("nodeValue", "").strip()
            # 简单过滤掉CSS和JS脚本内容
            if val and "{" not in val and "function" not in val and ".vjs" not in val:
                flat_texts.append(val)

        for child in node.get("children", []):
            traverse(child)

    root = doc.get("result", {}).get("root", doc)
    course_name = find_title(root)
    traverse(root)

    # 2. 根据提示的 "第n节" 开始解析章节状态机
    chapters = []
    current_chapter = None
    idx = 1

    status_map = {"未开始": "not_start", "学习中": "in_progress", "已完成": "completed"}

    chapter_pattern = re.compile(r"^第[0-9一二三四五六七八九十百]+节")

    for text in flat_texts:
        if chapter_pattern.match(text):
            if current_chapter:
                chapters.append(current_chapter)
            current_chapter = {
                "idx": idx,
                "name": text,
                "type": "video",  # 默认值
                "status": "not_start",  # 默认状态
            }
            idx += 1
        elif current_chapter:
            # 在章节标题之后的紧挨着的文本里获取类型和进度
            if text in ("视频", "video"):
                current_chapter["type"] = "video"
            elif text in ("文档", "doc", "pdf"):
                current_chapter["type"] = "doc"
            elif text in status_map:
                current_chapter["status"] = status_map[text]

    if current_chapter:
        chapters.append(current_chapter)

    # 判断整门课是否完成（如果没有任何有效章节，也算未完成）
    all_completed = True if chapters else False
    for ch in chapters:
        if ch["status"] != "completed":
            all_completed = False
            break

    result = {
        "id": course_id,
        "type": "course",
        "name": course_name,
        "url": url,
        "completed": all_completed,
        "chapters": chapters,
    }

    return result


def parse_subject_doc(document_file, url=""):
    """从dump的document文件中解析专题信息"""
    with open(document_file, "r", encoding="utf-8") as f:
        doc = json.load(f)

    subject_id = ""

    # 1. 提取 title
    def find_title(node):
        if node.get("nodeName", "").upper() == "TITLE":
            for c in node.get("children", []):
                if c.get("nodeName") == "#text":
                    return c.get("nodeValue", "").strip()
        for c in node.get("children", []):
            res = find_title(c)
            if res:
                return res
        return ""

    flat_tokens = []

    # 2. 递归拍平所有文本和带有跳转资源特征的 DOM 节点
    def traverse(node):
        nonlocal subject_id

        attrs = node.get("attributes", [])
        if attrs and isinstance(attrs, list):
            # 获取根 subject_id
            for i in range(len(attrs) - 1):
                if (
                    attrs[i] == "data-clipboard-text"
                    and "study/subject/detail" in attrs[i + 1]
                    and not subject_id
                ):
                    parts = attrs[i + 1].split("/")
                    if parts:
                        subject_id = parts[-1]

            # 捕获课程和课件的挂载节点
            is_resource = False
            res_id = ""
            sec_type = ""
            for i in range(len(attrs) - 1):
                if attrs[i] == "data-resource-id":
                    res_id = attrs[i + 1]
                    is_resource = True
                elif attrs[i] == "data-section-type":
                    sec_type = attrs[i + 1]
            if is_resource:
                flat_tokens.append(("RESOURCE", res_id, sec_type))

        if node.get("nodeName") == "#text":
            val = node.get("nodeValue", "").strip()
            if val and "{" not in val and "function" not in val and ".vjs" not in val:
                flat_tokens.append(("TEXT", val, ""))

        for child in node.get("children", []):
            traverse(child)

    root = doc.get("result", {}).get("root", doc)
    subject_name = find_title(root)
    traverse(root)

    # 3. 状态机解析 (按序抽取信息，避开多变的嵌套结构)
    items_map = {}
    current_folder = ""
    skip_current_folder = False

    status_map = {"未开始": "not_start", "学习中": "in_progress", "已完成": "completed"}

    n = len(flat_tokens)
    for i in range(n):
        typ, val, sec_type = flat_tokens[i]

        if typ == "TEXT":
            # 识别文件夹:紧接着如果出现 "收起" 或 "展开"，则当前 TEXT 为 Folder 名
            if (
                i + 1 < n
                and flat_tokens[i + 1][0] == "TEXT"
                and flat_tokens[i + 1][1] in ("收起", "展开")
            ):
                current_folder = val
                # 如果包含"选修"或"考试"则跳过深层解析
                skip_current_folder = (
                    "选修" in current_folder or "考试" in current_folder
                )

        elif typ == "RESOURCE" and not skip_current_folder:
            res_id = val
            sec_type = sec_type if sec_type else "6"

            # 进度状态紧靠在资源节点前方
            status = None
            if (
                i > 0
                and flat_tokens[i - 1][0] == "TEXT"
                and flat_tokens[i - 1][1] in status_map
            ):
                status = status_map[flat_tokens[i - 1][1]]

            # 类型和标题紧靠在资源节点后方
            texts_after = []
            for j in range(i + 1, min(i + 5, n)):
                if flat_tokens[j][0] == "TEXT":
                    texts_after.append(flat_tokens[j][1])

            item_type = "course"  # 缺省默认课件
            item_name = None
            if len(texts_after) >= 2:
                if texts_after[0] in ("专题", "subject"):
                    item_type = "subject"

                # 排除 UI 杂音文本
                if texts_after[1] not in (
                    "开始学习",
                    "继续学习",
                    "未开始",
                    "学习中",
                    "已完成",
                    "视频",
                    "文档",
                    "课程",
                    "收起",
                    "展开",
                ):
                    item_name = texts_after[1]

            # 构建并合并到 items_map (因为同一个 resource_id 会在 DOM 出现两次: 一次是状态按钮, 一次是标题链接)
            if res_id not in items_map:
                r_subject = subject_id if subject_id else res_id

                if item_type == "subject":
                    item_url = f"https://wangda.chinamobile.com/#/study/subject/detail/{res_id}"
                else:
                    item_url = f"https://wangda.chinamobile.com/#/study/course/detail/subject-course/{res_id}/{sec_type}/{r_subject}"

                items_map[res_id] = {
                    "id": res_id,
                    "name": "Unknown",
                    "status": "not_start",
                    "item_type": item_type,
                    "url": item_url,
                }

            # 更新已有项: 只覆盖有效数据
            if status:
                items_map[res_id]["status"] = status
            if item_name:
                items_map[res_id]["name"] = item_name

    # 4. 执行递归解析！
    sub_subjects = []
    courses = []
    all_completed = True

    for res_id, item in items_map.items():
        print(f"\n--- 递归进入 [{item['item_type'].upper()}]: {item['name']} ---")

        # 爬虫递归：重新利用 parse 方法进入该资源的详情页！
        full_item = parse(item["url"])

        if not full_item:
            # 如果解析失败，采用浅层对象兜底
            full_item = {
                "id": item["id"],
                "name": item["name"],
                "completed": (item["status"] == "completed"),
            }
            if item["item_type"] == "course":
                full_item["chapters"] = []

        # 统计整体进度
        if not full_item.get("completed", False):
            all_completed = False

        if item["item_type"] == "subject":
            sub_subjects.append(full_item)
        else:
            courses.append(full_item)

    if not courses and not sub_subjects:
        all_completed = False

    subject_url = (
        url
        if url
        else f"https://wangda.chinamobile.com/#/study/subject/detail/{subject_id}"
    )

    result = {
        "id": subject_id,
        "type": "subject",
        "name": subject_name,
        "url": subject_url,
        "completed": all_completed,
        "subjects": sub_subjects,
        "courses": courses,
    }

    return result


def parse(url, should_navi=True):
    """
    通用解析函数，根据URL类型自动判断是课程还是专题

    Args:
        url: 课程或专题的URL

    Returns:
        解析结果字典
    """
    url_type = get_url_type(url)

    if url_type == "other":
        print(f"非课程或课件地址: {url}")
        return None
    if should_navi:
        print(f"正在跳转至: {url}")
        navi(url)
        print("等待页面资源加载和 Vue 渲染 (等待 3 秒)...")
        time.sleep(3)

    dump_file = dump_page()

    if url_type == "course":
        result = parse_course_doc(dump_file, url)
    elif url_type == "subject":
        result = parse_subject_doc(dump_file, url)
    else:
        return None

    return result


def parse_subject(subject_url):
    """
    根据用户提供的subject_url地址，解析出session.progress下所需要的subject相关信息

    Args:
        subject_url: 专题URL

    Returns:
        如果解析成功返回解析结果，如果失败返回失败原因
    """
    url_type = get_url_type(subject_url)

    if url_type == "other":
        print(f"解析失败: 不是有效的课程或专题URL: {subject_url}")
        sys.exit(1)

    result = parse(subject_url)

    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    else:
        print("解析失败: 无法从页面提取有效信息")
        sys.exit(1)


def skip_to_uncompleted_chapter(course_info):
    """
    找到course_info中第一个未完成的chapter，在浏览器中点击跳转到该章节

    使用chrome_tools中的send_cdp_message（原始socket），避免触发反调试检测

    Args:
        course_info: 课程信息字典，包含chapters列表（每个chapter有idx, name, type, status）

    Returns:
        被点击的chapter信息字典，如果所有章节已完成则返回None
    """
    from chrome_tools import send_cdp_message, get_ws_url, close_pop_window

    chapters = course_info.get("chapters", [])
    if not chapters:
        print("该课程没有章节信息")
        return None

    # 1. 找到第一个未完成的章节（status != "completed"）
    target_chapter = None
    for ch in chapters:
        if ch.get("status") != "completed":
            target_chapter = ch
            break

    if not target_chapter:
        print("所有章节均已完成")
        return None

    chapter_name = target_chapter.get("name", "")
    chapter_idx = target_chapter.get("idx", 0)
    print(f"目标章节: [{chapter_idx}] {chapter_name}")

    # 2. 导航到课程页面（如果提供了url）
    course_url = course_info.get("url")
    if course_url:
        navi(course_url)
        time.sleep(3)  # 等待页面加载

    # 3. 先关闭可能存在的弹窗
    close_pop_window()
    time.sleep(0.5)

    # 4. 通过CDP连接浏览器，点击目标章节
    port = os.environ.get("_WANGDA_DEBUG_PORT")
    if not port:
        raise Exception("未设置_WANGDA_DEBUG_PORT环境变量")

    ws_url = get_ws_url(port)
    if not ws_url:
        raise Exception("无法获取WebSocket连接URL")

    # 转义章节名中的特殊字符用于JS
    escaped_name = chapter_name.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')

    # 使用 Runtime.evaluate 查找章节元素坐标
    # 策略1: 精确匹配章节名
    # 策略2: 前缀匹配（第N节）
    # 策略3: 按序号索引兜底
    find_expr = f"""
    (() => {{
        // 策略1: 精确匹配完整章节名（叶子节点优先）
        let els = Array.from(document.body.querySelectorAll('*'));
        let el = els.find(e => e.offsetHeight > 0 && e.innerText && e.innerText.trim() === '{escaped_name}' && e.children.length === 0);
        if (!el) el = els.find(e => e.offsetHeight > 0 && e.innerText && e.innerText.includes('{escaped_name}') && e.children.length === 0);

        // 策略2: 匹配包含章节名的元素（子元素少的优先）
        if (!el) {{
            for (const e of els) {{
                const text = (e.textContent || '').trim();
                if (text.includes('{escaped_name}') && e.offsetHeight > 0 && e.children.length <= 2) {{
                    const r = e.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0) {{
                        el = e;
                        break;
                    }}
                }}
            }}
        }}

        // 策略3: 放宽条件
        if (!el) {{
            for (const e of els) {{
                const text = (e.textContent || '').trim();
                if (text.includes('{escaped_name}') && e.offsetHeight > 0) {{
                    const r = e.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0) {{
                        el = e;
                        break;
                    }}
                }}
            }}
        }}

        // 策略4: 按序号查找第N个章节元素
        if (!el) {{
            const items = Array.from(document.querySelectorAll('[class*="chapter"], [class*="section"], [class*="catalog"], [class*="list"] li, [class*="item"]'));
            const chapterItems = items.filter(e => {{
                const text = (e.textContent || '').trim();
                return text.includes('第') && text.includes('节') && e.offsetHeight > 0;
            }});
            if (chapterItems.length >= {chapter_idx}) {{
                el = chapterItems[{chapter_idx - 1}];
            }}
        }}

        if (el) {{
            // 先滚动到元素可见区域，确保不会因为在视口外而点击失败
            el.scrollIntoView({{behavior: 'instant', block: 'center'}});
            // 滚动后重新获取坐标
            const r = el.getBoundingClientRect();
            return {{x: r.x + r.width / 2, y: r.y + r.height / 2}};
        }}
        return null;
    }})()
    """

    result = send_cdp_message(
        ws_url, "Runtime.evaluate",
        {"expression": find_expr, "returnByValue": True},
        wait_for_response=True
    )

    coords = None
    if result and "result" in result:
        value = result["result"].get("result", {}).get("value")
        if value and isinstance(value, dict) and "x" in value and "y" in value:
            coords = (value["x"], value["y"])

    if coords:
        print(f"找到章节元素，坐标: ({coords[0]:.0f}, {coords[1]:.0f})，正在点击...")

        # 模拟鼠标点击（mousePressed + mouseReleased）
        send_cdp_message(
            ws_url, "Input.dispatchMouseEvent",
            {"type": "mousePressed", "x": coords[0], "y": coords[1], "button": "left", "clickCount": 1},
            wait_for_response=True
        )
        time.sleep(0.05)
        send_cdp_message(
            ws_url, "Input.dispatchMouseEvent",
            {"type": "mouseReleased", "x": coords[0], "y": coords[1], "button": "left", "clickCount": 1},
            wait_for_response=True
        )

        time.sleep(1)
        print(f"已跳转到章节: [{chapter_idx}] {chapter_name}")
        return target_chapter
    else:
        raise Exception(f"未能在页面中找到章节: {chapter_name}")


def start_auto_study():
    """
    开始自动学习，选择合适的未完成的课件开始学习，并添加对应的定时监控

    Returns:
        目前正在学习的课件(course)信息
    """
    # 引入session_tools
    from session_tools import get_next_course

    # 1. 获取下一个需要学习的课件
    course = get_next_course()

    if not course:
        print("没有需要学习的课件")
        sys.exit(1)

    # 2. 导航到课件页面
    course_url = course.get("url")
    if not course_url:
        print("课件URL不存在")
        sys.exit(1)

    print(f"开始学习课件: {course.get('name', 'Unknown')}")
    navi(course_url)

    # 3. 等待页面加载
    time.sleep(3)

    # 4. 输出当前学习的课件信息
    print(json.dumps(course, ensure_ascii=False, indent=2))

    # 5. TODO: 添加定时监控（CronCreate）
    # 这里需要根据实际学习时长设置定时任务
    # 暂时留空，由上层调用者处理

    return course


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="课程相关工具")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # parse-subject command
    parse_subject_cmd = subparsers.add_parser(
        "parse-subject",
        help="根据用户提供的subject_url地址，解析出session.progress下所需要的subject相关信息",
    )
    parse_subject_cmd.add_argument("subject_url", type=str, help="专题或课程的URL地址")

    # start-auto-study command
    subparsers.add_parser(
        "start-auto-study",
        help="开始自动学习,选择合适的未完成的课件开始学习，并添加对应的定时监控",
    )

    args = parser.parse_args()

    if args.command == "parse-subject":
        parse_subject(args.subject_url)
    elif args.command == "start-auto-study":
        start_auto_study()
    else:
        parser.print_help()
