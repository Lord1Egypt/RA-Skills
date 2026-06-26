#!/usr/bin/env python3
"""
Reading Tracker CLI - 个人阅读管理系统核心工具
"""

import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# 数据目录
WORKSPACE = Path.home() / ".qclaw" / "workspace" / "reading"
BOOKS_DIR = WORKSPACE / "books"
REVIEWS_DIR = WORKSPACE / "reviews"
LIBRARY_FILE = WORKSPACE / "library.json"
SCHEDULE_FILE = WORKSPACE / "schedule.json"

# 艾宾浩斯复习间隔（天）
REVIEW_INTERVALS = [1, 3, 7, 30]


def init_workspace():
    """初始化数据目录"""
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    if not LIBRARY_FILE.exists():
        LIBRARY_FILE.write_text(json.dumps({"books": []}, ensure_ascii=False, indent=2))
    if not SCHEDULE_FILE.exists():
        SCHEDULE_FILE.write_text(json.dumps({"reviews": []}, ensure_ascii=False, indent=2))


def load_library():
    init_workspace()
    return json.loads(LIBRARY_FILE.read_text())


def save_library(data):
    LIBRARY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def load_schedule():
    init_workspace()
    return json.loads(SCHEDULE_FILE.read_text())


def save_schedule(data):
    SCHEDULE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def start_book(title, author=""):
    """开始阅读一本书"""
    library = load_library()
    # 检查是否已存在
    for book in library["books"]:
        if book["title"] == title and book["status"] == "reading":
            return f"📖 《{title}》已在阅读中（进度 {book['progress']}%）"

    book_id = str(uuid.uuid4())[:8]
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")
    file_name = f"{title}-{month}.md"
    file_path = BOOKS_DIR / file_name

    # 创建笔记文件
    content = f"""# 《{title}》

## 元信息
- 作者：{author or "（待填写）"}
- 开始时间：{today}
- 完成时间：
- 总进度：0%
- 评分：

## 核心输出（读完后填写）
- 一句话总结：
- 认知改变：
- 行动计划：

## 书摘与思考

## 复习记录
"""
    file_path.write_text(content, encoding="utf-8")

    # 更新书库
    library["books"].append({
        "id": book_id,
        "title": title,
        "author": author,
        "status": "reading",
        "progress": 0,
        "startDate": today,
        "finishDate": None,
        "rating": None,
        "filePath": str(file_path),
        "quotes": [],
        "readingDates": [today]
    })
    save_library(library)

    return f"""📖 开始阅读《{title}》
   作者：{author or "（未填写）"}
   开始时间：{today}

   已创建笔记文件，随时记录你的书摘和思考 ✨"""


def add_quote(title, quote, thought="", chapter="", progress=None):
    """记录书摘"""
    library = load_library()
    today = datetime.now().strftime("%Y-%m-%d")

    # 找到对应书籍
    book = None
    for b in library["books"]:
        if b["title"] == title and b["status"] == "reading":
            book = b
            break

    if not book:
        return f"❌ 未找到正在阅读的《{title}》，请先用「开始读《{title}》」记录"

    # 更新进度
    if progress is not None:
        book["progress"] = progress

    # 记录阅读日期
    if today not in book.get("readingDates", []):
        book.setdefault("readingDates", []).append(today)

    # 追加到笔记文件
    file_path = Path(book["filePath"])
    if file_path.exists():
        content = file_path.read_text(encoding="utf-8")
        chapter_str = f"第{chapter}章" if chapter else ""
        progress_str = f"（{progress}%）" if progress else ""
        entry = f"""
### {today} {chapter_str}{progress_str}
> "{quote}"

**我的想法**：{thought or "（待补充）"}

"""
        # 插入到"书摘与思考"章节后
        content = content.replace("## 书摘与思考\n", f"## 书摘与思考\n{entry}")
        file_path.write_text(content, encoding="utf-8")

    # 设置复习提醒
    schedule = load_schedule()
    for days in REVIEW_INTERVALS[:2]:  # 先设置1天和3天的提醒
        review_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        schedule["reviews"].append({
            "bookId": book["id"],
            "bookTitle": title,
            "type": "chapter",
            "content": quote[:50] + ("..." if len(quote) > 50 else ""),
            "thought": thought,
            "scheduledDate": review_date,
            "createdDate": today,
            "done": False
        })
    save_schedule(schedule)
    save_library(library)

    progress_info = f"进度：{progress}%" if progress else ""
    return f"""✓ 已记录《{title}》{chapter_str if chapter else ""}的书摘
  {progress_info}
  下次复习提醒：{(datetime.now() + timedelta(days=1)).strftime('%m-%d')}、{(datetime.now() + timedelta(days=3)).strftime('%m-%d')}"""


def finish_book(title, rating=None):
    """完成一本书，返回三问"""
    library = load_library()
    for book in library["books"]:
        if book["title"] == title and book["status"] == "reading":
            return {
                "status": "need_answers",
                "book": book,
                "message": f"""🎉 恭喜读完《{title}》！

为了真正记住这本书，请回答三个问题：

1️⃣  一句话总结这本书的核心观点：

2️⃣  它改变了你什么认知？

3️⃣  你会采取什么具体行动？"""
            }
    return {"status": "error", "message": f"❌ 未找到正在阅读的《{title}》"}


def save_finish_answers(title, summary, insight, action, rating=None):
    """保存完成三问答案"""
    library = load_library()
    today = datetime.now().strftime("%Y-%m-%d")

    for book in library["books"]:
        if book["title"] == title and book["status"] == "reading":
            book["status"] = "finished"
            book["finishDate"] = today
            book["progress"] = 100
            if rating:
                book["rating"] = rating

            # 更新笔记文件
            file_path = Path(book["filePath"])
            if file_path.exists():
                content = file_path.read_text(encoding="utf-8")
                content = content.replace("- 一句话总结：", f"- 一句话总结：{summary}")
                content = content.replace("- 认知改变：", f"- 认知改变：{insight}")
                content = content.replace("- 行动计划：", f"- 行动计划：{action}")
                content = content.replace("- 完成时间：\n", f"- 完成时间：{today}\n")
                content = content.replace("- 总进度：0%", "- 总进度：100%")
                if rating:
                    stars = "⭐" * rating
                    content = content.replace("- 评分：\n", f"- 评分：{stars}\n")
                file_path.write_text(content, encoding="utf-8")

            # 设置长期复习提醒
            schedule = load_schedule()
            for days in REVIEW_INTERVALS[2:]:  # 7天和30天
                review_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                schedule["reviews"].append({
                    "bookId": book["id"],
                    "bookTitle": title,
                    "type": "full",
                    "content": summary,
                    "scheduledDate": review_date,
                    "createdDate": today,
                    "done": False
                })
            save_schedule(schedule)
            save_library(library)

            # 统计
            start = datetime.strptime(book["startDate"], "%Y-%m-%d")
            days_spent = (datetime.now() - start).days + 1
            quotes_count = len(book.get("quotes", []))

            return f"""✓ 核心输出已保存

📊 阅读统计：
   用时：{days_spent} 天
   开始：{book['startDate']} → 完成：{today}

🔄 已设置复习计划：
   7天后回顾核心观点（{(datetime.now() + timedelta(days=7)).strftime('%m-%d')}）
   30天后检查行动进展（{(datetime.now() + timedelta(days=30)).strftime('%m-%d')}）"""

    return "❌ 未找到对应书籍"


def get_today_reviews():
    """获取今日复习任务"""
    schedule = load_schedule()
    today = datetime.now().strftime("%Y-%m-%d")

    due = [r for r in schedule["reviews"]
           if r["scheduledDate"] <= today and not r.get("done", False)]

    if not due:
        return "✅ 今日没有复习任务，继续保持阅读！"

    result = f"📚 今日复习（{len(due)} 项）\n\n"
    for i, r in enumerate(due, 1):
        days_ago = (datetime.now() - datetime.strptime(r["createdDate"], "%Y-%m-%d")).days
        review_type = "全书回顾" if r["type"] == "full" else "章节回顾"
        result += f"""{i}. 《{r['bookTitle']}》- {review_type}
   {days_ago}天前记录："{r['content']}"
"""
        if r.get("thought"):
            result += f"   当时的想法：{r['thought']}\n"
        result += "   现在有什么新的感悟？\n\n"

    return result.strip()


def generate_monthly_report(year=None, month=None):
    """生成月度报告"""
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    month_str = f"{year}-{month:02d}"

    library = load_library()

    # 统计本月数据
    finished = []
    reading = []
    all_reading_dates = set()

    for book in library["books"]:
        # 本月读完的书
        if (book.get("finishDate") or "").startswith(month_str):
            finished.append(book)
        # 本月在读的书
        if book["status"] == "reading":
            reading.append(book)
        # 收集所有阅读日期
        for d in book.get("readingDates", []):
            if d.startswith(month_str):
                all_reading_dates.add(d)

    # 生成日历
    calendar_str = _generate_calendar(year, month, all_reading_dates)

    # 计算连续天数
    streak_info = _calc_streak(sorted(all_reading_dates))

    # 今天是本月第几天
    today = now.day if now.year == year and now.month == month else _days_in_month(year, month)

    # 组装报告
    report = f"""📊 {year}年{month}月阅读报告

┌─────────────────────────────────────┐
│  本月读完：{len(finished)} 本{"                        " [:24-len(str(len(finished)))-3]}│
│  在读：{len(reading)} 本{"                           " [:27-len(str(len(reading)))-3]}│
│  有记录天数：{len(all_reading_dates)} 天{"                      " [:22-len(str(len(all_reading_dates)))-3]}│
└─────────────────────────────────────┘

{calendar_str}

📈 关键数字
✅ 本月有记录：{len(all_reading_dates)} 天 / {today} 天（截至今日）
⚡ 最长连续：{streak_info['max_streak']} 天{f"（{streak_info['max_streak_range']}）" if streak_info['max_streak_range'] else ""}
😅 最长断档：{streak_info['max_gap']} 天{f"（{streak_info['max_gap_range']}）" if streak_info['max_gap_range'] else ""}
"""

    if finished:
        report += "\n📖 本月读完：\n"
        for book in finished:
            stars = "⭐" * (book.get("rating") or 0)
            summary = ""
            # 尝试读取核心输出
            fp = Path(book.get("filePath", ""))
            if fp.exists():
                content = fp.read_text(encoding="utf-8")
                for line in content.split("\n"):
                    if "一句话总结：" in line and len(line) > 10:
                        summary = line.split("一句话总结：")[-1].strip()
                        break
            report += f"   《{book['title']}》{stars}\n"
            if summary:
                report += f"   核心收获：{summary}\n"
            report += "\n"

    if reading:
        report += "📌 进行中：\n"
        for book in reading:
            report += f"   《{book['title']}》{book['progress']}%\n"

    return report.strip()


def _generate_calendar(year, month, reading_dates):
    """生成月历"""
    import calendar
    cal = calendar.monthcalendar(year, month)
    header = "Mo  Tu  We  Th  Fr  Sa  Su"
    lines = [f"📅 {year}年{month}月阅读日历\n", header]

    for week in cal:
        row = ""
        for day in week:
            if day == 0:
                row += "    "
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                if date_str in reading_dates:
                    row += "📖  "
                else:
                    row += f"{day:2d}  "
        lines.append(row.rstrip())

    lines.append("\n📖 = 有阅读记录   数字 = 无记录")
    return "\n".join(lines)


def _calc_streak(dates):
    """计算最长连续和最长断档"""
    if not dates:
        return {"max_streak": 0, "max_streak_range": "", "max_gap": 0, "max_gap_range": ""}

    date_objs = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

    max_streak = 1
    max_streak_range = f"{dates[0][5:]} - {dates[0][5:]}"
    cur_streak = 1
    cur_start = dates[0]

    max_gap = 0
    max_gap_range = ""

    for i in range(1, len(date_objs)):
        diff = (date_objs[i] - date_objs[i-1]).days
        if diff == 1:
            cur_streak += 1
            if cur_streak > max_streak:
                max_streak = cur_streak
                max_streak_range = f"{cur_start[5:]} - {dates[i][5:]}"
        else:
            cur_streak = 1
            cur_start = dates[i]
            gap = diff - 1
            if gap > max_gap:
                max_gap = gap
                gap_start = (date_objs[i-1] + timedelta(days=1)).strftime("%m-%d")
                gap_end = (date_objs[i] - timedelta(days=1)).strftime("%m-%d")
                max_gap_range = f"{gap_start} - {gap_end}"

    return {
        "max_streak": max_streak,
        "max_streak_range": max_streak_range,
        "max_gap": max_gap,
        "max_gap_range": max_gap_range
    }


def _days_in_month(year, month):
    import calendar
    return calendar.monthrange(year, month)[1]


def list_books(status=None):
    """列出书籍"""
    library = load_library()
    books = library["books"]
    if status:
        books = [b for b in books if b["status"] == status]

    if not books:
        return "📚 暂无书籍记录"

    status_map = {"reading": "📖 在读", "finished": "✅ 已读", "paused": "⏸ 暂停"}
    result = "📚 书库\n\n"
    for book in books:
        s = status_map.get(book["status"], book["status"])
        result += f"{s} 《{book['title']}》"
        if book["author"]:
            result += f" - {book['author']}"
        if book["status"] == "reading":
            result += f" ({book['progress']}%)"
        result += "\n"
    return result.strip()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "start":
        title = sys.argv[2] if len(sys.argv) > 2 else ""
        author = sys.argv[3] if len(sys.argv) > 3 else ""
        print(start_book(title, author))

    elif cmd == "quote":
        title = sys.argv[2] if len(sys.argv) > 2 else ""
        quote = sys.argv[3] if len(sys.argv) > 3 else ""
        thought = sys.argv[4] if len(sys.argv) > 4 else ""
        chapter = sys.argv[5] if len(sys.argv) > 5 else ""
        print(add_quote(title, quote, thought, chapter))

    elif cmd == "finish":
        title = sys.argv[2] if len(sys.argv) > 2 else ""
        result = finish_book(title)
        print(result["message"])

    elif cmd == "review":
        print(get_today_reviews())

    elif cmd == "report":
        print(generate_monthly_report())

    elif cmd == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        print(list_books(status))

    else:
        print("""Reading Tracker CLI

用法：
  python reading_cli.py start <书名> [作者]     开始阅读
  python reading_cli.py quote <书名> <书摘> [思考] [章节]  记录书摘
  python reading_cli.py finish <书名>           完成阅读
  python reading_cli.py review                  今日复习
  python reading_cli.py report                  月度报告
  python reading_cli.py list [reading|finished] 书库列表
""")
