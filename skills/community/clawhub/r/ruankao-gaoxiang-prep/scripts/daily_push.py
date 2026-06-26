#!/usr/bin/env python3
"""
软考高项每日推送脚本
根据日期生成每日复习内容（章节重点 + 英语单词）
"""

import sys
import json
import os
from datetime import datetime, date

# 章节映射（教材第四版，共24章）
CHAPTERS = {
    1: {"file": "chapter01-info-system.md", "name": "信息系统基础"},
    2: {"file": "chapter02-it-development.md", "name": "信息系统项目管理"},
    3: {"file": "chapter03-governance.md", "name": "项目立项管理"},
    4: {"file": "chapter04-is-management.md", "name": "项目整体管理"},
    5: {"file": "chapter05-is-engineering.md", "name": "信息系统工程"},
    6: {"file": "chapter06-pm-overview.md", "name": "项目整体管理"},
    7: {"file": "chapter07-initiation.md", "name": "立项管理"},
    8: {"file": "chapter08-integration.md", "name": "项目整合管理"},
    9: {"file": "chapter09-scope.md", "name": "项目范围管理"},
    10: {"file": "chapter10-schedule.md", "name": "进度管理"},
    11: {"file": "chapter11-cost.md", "name": "成本管理"},
    12: {"file": "chapter12-quality.md", "name": "质量管理"},
    13: {"file": "chapter13-resource.md", "name": "资源管理"},
    14: {"file": "chapter14-communication.md", "name": "沟通管理"},
    15: {"file": "chapter15-risk.md", "name": "风险管理"},
    16: {"file": "chapter16-procurement.md", "name": "采购管理"},
    17: {"file": "chapter17-stakeholder.md", "name": "干系人管理"},
    18: {"file": "chapter18-performance.md", "name": "项目绩效域"},
    19: {"file": "chapter19-config-change.md", "name": "配置与变更管理"},
    20: {"file": "chapter20-advanced.md", "name": "高级项目管理"},
    21: {"file": "chapter21-calculation.md", "name": "运筹学计算"},
    22: {"file": "chapter22-governance.md", "name": "组织通用治理"},
    23: {"file": "chapter23-management.md", "name": "组织通用管理"},
    24: {"file": "chapter24-legal.md", "name": "法律法规与标准规范"},
}

def get_skill_dir():
    """获取技能目录"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)

def get_today_chapter():
    """根据日期确定今天的章节（24章轮询）"""
    today = date.today()
    day_of_year = today.timetuple().tm_yday
    chapter_num = (day_of_year % 24) + 1  # 1-24
    return chapter_num

def read_chapter_points(chapter_num):
    """读取章节重点"""
    skill_dir = get_skill_dir()
    chapter_file = CHAPTERS[chapter_num]["file"]
    file_path = os.path.join(skill_dir, "references", chapter_file)

    if not os.path.exists(file_path):
        return None, f"章节文件不存在：{file_path}"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取重点内容
    lines = content.split('\n')
    points = []
    in_points_section = False

    for line in lines:
        line = line.strip()
        if line.startswith("## 背诵重点"):
            in_points_section = True
            continue
        elif line.startswith("##") and in_points_section:
            break
        elif in_points_section and line and not line.startswith("#"):
            # 移除开头的数字编号
            if line[0].isdigit():
                # 找到第一个非数字字符
                i = 0
                while i < len(line) and line[i].isdigit():
                    i += 1
                # 跳过点号和空格
                while i < len(line) and (line[i] == '.' or line[i] == '、' or line[i] == ' '):
                    i += 1
                line = line[i:] if i < len(line) else line
            points.append(line)

    return points, None

def read_english_words():
    """读取英语单词"""
    skill_dir = get_skill_dir()
    file_path = os.path.join(skill_dir, "references", "english-words.md")

    if not os.path.exists(file_path):
        return None, "英语单词文件不存在"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取单词
    lines = content.split('\n')
    words = []

    for line in lines:
        line = line.strip()
        if line and line[0].isdigit() and line[1] == '.':
            words.append(line)

    return words, None

def read_exam_questions():
    """读取考试题目"""
    skill_dir = get_skill_dir()
    file_path = os.path.join(skill_dir, "references", "exam-questions.md")

    if not os.path.exists(file_path):
        return None, "考试题目文件不存在"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取所有题目（每题包含年份标注）
    questions = []
    lines = content.split('\n')
    current_question = []

    for line in lines:
        line_stripped = line.strip()
        
        # 题目开始（数字. [年份] 内容）
        if line_stripped and line_stripped[0].isdigit() and '[' in line_stripped and '年]' in line_stripped:
            if current_question:
                questions.append("\n".join(current_question))
            # 保留完整的题目行（包含年份标注）
            current_question = [line_stripped]
        # 选项行（stripped后以A./B./C./D.开头）
        elif (line_stripped.startswith("A.") or line_stripped.startswith("B.") or 
              line_stripped.startswith("C.") or line_stripped.startswith("D.")):
            current_question.append(line_stripped)
        # 答案行
        elif line_stripped.startswith("**答案："):
            current_question.append(line_stripped)
        # 跳过空行和分隔线

    # 添加最后一题
    if current_question:
        questions.append("\n".join(current_question))

    return questions, None

def format_exam_questions(all_questions, group_num, limit=10):
    """格式化考试题目"""
    if not all_questions:
        return "暂无考试题目"

    # 根据日期轮询选择题目（从所有题目中选择10题）
    today = date.today()
    start_index = today.timetuple().tm_yday % len(all_questions)
    
    # 选择10道题（循环选择）
    selected_questions = []
    for i in range(limit):
        index = (start_index + i) % len(all_questions)
        # 去掉题号，保留年份标注
        question_text = all_questions[index]
        # 将 "35. [2023年] xxx" 改为 "[2023年] xxx"
        import re
        question_text = re.sub(r'^\d+\.\s+', '', question_text)
        
        # 将选项合并到一行
        # 分割成行
        lines = question_text.split('\n')
        if len(lines) >= 2:
            # 第一行是题目
            formatted_question = lines[0]
            # 后面是选项，合并到一行
            options = []
            answer = None
            for line in lines[1:]:
                if line.startswith('A.'):
                    options.append(line)
                elif line.startswith('B.'):
                    options.append(line)
                elif line.startswith('C.'):
                    options.append(line)
                elif line.startswith('D.'):
                    options.append(line)
                elif line.startswith('**答案：'):
                    answer = line
            
            # 将选项合并为一行
            if options:
                formatted_question += '\n' + ' '.join(options)
            # 答案单独一行
            if answer:
                formatted_question += '\n' + answer
            
            selected_questions.append(formatted_question)
        else:
            selected_questions.append(question_text)

    # 添加题号（1-10）
    numbered_questions = []
    for i, q in enumerate(selected_questions, 1):
        numbered_questions.append(f"{i}. {q}")

    # 格式化输出
    result = "🎯 历年真题精选（10题）\n\n" + "\n\n".join(numbered_questions)
    return result

def format_chapter_points(points, limit=10):
    """格式化章节重点"""
    if not points:
        return "暂无重点内容"

    result = []
    for i, point in enumerate(points[:limit], 1):
        result.append(f"{i}. {point}")
    return "\n".join(result)

def format_english_words(words, limit=10):
    """格式化英语单词"""
    if not words:
        return "暂无单词"

    # 取前limit个单词
    selected_words = words[:limit]
    return "\n".join(selected_words)

def main():
    # 获取今天的章节
    chapter_num = get_today_chapter()
    chapter_info = CHAPTERS.get(chapter_num)
    chapter_name = chapter_info["name"] if chapter_info else "未知章节"

    # 读取章节重点
    points, error = read_chapter_points(chapter_num)
    if error:
        points_text = f"⚠️ {error}"
    else:
        points_text = format_chapter_points(points, 10)

    # 读取英语单词
    words, error = read_english_words()
    if error:
        words_text = f"⚠️ {error}"
    else:
        words_text = format_english_words(words, 10)

    # 读取考试题目
    all_questions, error = read_exam_questions()
    if error:
        questions_text = f"⚠️ {error}"
    else:
        questions_text = format_exam_questions(all_questions, 0, 10)

    # 获取日期
    today = date.today()
    date_str = today.strftime("%Y年%m月%d日")
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = weekdays[today.weekday()]

    # 生成完整消息
    message = f"""📚 软考高项每日复习 {date_str} {weekday_str}

📖 今日重点（第{chapter_num}章 {chapter_name}）：

{points_text}

📝 今日英语单词：

{words_text}

{questions_text}

💪 加油，坚持就是胜利！"""

    # 输出结果
    result = {
        "date": date_str,
        "weekday": weekday_str,
        "chapter": chapter_num,
        "chapter_name": chapter_name,
        "points": points[:10] if points else [],
        "words": words[:10] if words else [],
        "questions_count": 10,  # 每次固定10题
        "message": message
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
