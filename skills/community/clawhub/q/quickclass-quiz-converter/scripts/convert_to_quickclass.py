#!/usr/bin/env python3
"""
QuickClass 作业 JSON 生成器

将 LLM 提取的题目数据转换为 QuickClass 兼容的 JSON 格式。
支持题型：SINGLE_CHOICE / MULTIPLE_CHOICE / TRUE_FALSE

用法:
  python convert_to_quickclass.py --teacher "张老师" --grade "三年级下学期" \
    --subject "数学" --task-title "圆的认识" --quiz-title "练习题" \
    --input questions.json --output result.json

输入 questions.json 格式（由 LLM 从文档提取后生成的中间格式）:
[
  {
    "type": "SINGLE_CHOICE",
    "content": "题目内容",
    "options": {"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
    "answer": "B",
    "difficulty": "BASIC",
    "score": 5,
    "explanation": "解析内容"
  },
  ...
]

输出: QuickClass 兼容的 JSON 文件
"""

import argparse
import json
import sys
import time
import random
import string


def generate_cuid2():
    """生成类 CUID2 格式的 ID（兼容 QuickClass 的 ID 规范）"""
    # QuickClass 使用类似 cm + base36 时间戳 + 随机字符串的格式
    # 示例: cmshqbzmd00076t7iq26nt33a
    timestamp = int(time.time() * 1000)
    base36_ts = base36_encode(timestamp)
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"cm{base36_ts}{random_part}"[:25]


def base36_encode(num):
    """将数字编码为 base36 字符串"""
    chars = string.ascii_lowercase + string.digits
    if num == 0:
        return '0'
    result = []
    while num > 0:
        result.append(chars[num % 36])
        num //= 36
    return ''.join(reversed(result))


# 题型映射
TYPE_MAP = {
    "单选": "SINGLE_CHOICE",
    "单选题": "SINGLE_CHOICE",
    "SINGLE_CHOICE": "SINGLE_CHOICE",
    "多选": "MULTIPLE_CHOICE",
    "多选题": "MULTIPLE_CHOICE",
    "MULTIPLE_CHOICE": "MULTIPLE_CHOICE",
    "判断": "TRUE_FALSE",
    "判断题": "TRUE_FALSE",
    "TRUE_FALSE": "TRUE_FALSE",
}

# 难度映射
DIFFICULTY_MAP = {
    "基础": "BASIC",
    "基本": "BASIC",
    "简单": "BASIC",
    "BASIC": "BASIC",
    "中等": "INTERMEDIATE",
    "进阶": "INTERMEDIATE",
    "INTERMEDIATE": "INTERMEDIATE",
    "较难": "ADVANCED",
    "困难": "ADVANCED",
    "高级": "ADVANCED",
    "ADVANCED": "ADVANCED",
    "拓展": "EXPANDED",
    "扩展": "EXPANDED",
    "EXPANDED": "EXPANDED",
}

# 选项字母列表
OPTION_LETTERS = ["A", "B", "C", "D", "E", "F"]


def normalize_question_type(q_type: str) -> str:
    """规范化题型为 QuickClass 格式"""
    t = q_type.strip()
    if t in TYPE_MAP:
        return TYPE_MAP[t]
    raise ValueError(f"未知题型: '{q_type}'，支持的题型: 单选/多选/判断")


def normalize_difficulty(diff: str) -> str:
    """规范化难度为 QuickClass 格式"""
    if not diff:
        return "BASIC"
    d = diff.strip()
    if d in DIFFICULTY_MAP:
        return DIFFICULTY_MAP[d]
    raise ValueError(f"未知难度: '{diff}'，支持的难度: 基础/中等/较难/拓展")


def normalize_options(options: dict, q_type: str) -> str:
    """将选项 dict 转为 QuickClass 要求的 JSON 字符串格式"""
    if q_type == "TRUE_FALSE":
        return "{}"
    if isinstance(options, str):
        # 已经是 JSON 字符串，验证格式
        try:
            parsed = json.loads(options)
            return json.dumps(parsed, ensure_ascii=False, separators=(',', ':'))
        except json.JSONDecodeError:
            raise ValueError(f"选项 JSON 格式无效: {options}")
    if isinstance(options, dict):
        # 确保 key 是大写字母
        normalized = {}
        for i, (k, v) in enumerate(options.items()):
            if k.upper() in OPTION_LETTERS:
                normalized[k.upper()] = str(v)
            else:
                # 自动分配字母
                letter = OPTION_LETTERS[i] if i < len(OPTION_LETTERS) else str(k)
                normalized[letter] = str(v)
        return json.dumps(normalized, ensure_ascii=False, separators=(',', ':'))
    raise ValueError(f"选项格式无效: {type(options)}")


def normalize_answer(answer: str, q_type: str) -> str:
    """规范化答案格式"""
    answer = answer.strip().upper()

    if q_type == "TRUE_FALSE":
        # 判断题: T/F 或 对/错 或 正确/错误
        if answer in ("T", "对", "正确", "TRUE", "YES", "√"):
            return "T"
        if answer in ("F", "错", "错误", "FALSE", "NO", "×"):
            return "F"
        raise ValueError(f"判断题答案无效: '{answer}'，应为 T 或 F")

    if q_type == "MULTIPLE_CHOICE":
        # 多选题: 标准化为 "A,B,C" 格式
        answer = answer.replace("，", ",").replace(" ", "").replace(";", ",")
        parts = sorted([p.strip() for p in answer.split(",") if p.strip()])
        for p in parts:
            if p not in OPTION_LETTERS:
                raise ValueError(f"多选题答案选项无效: '{p}'")
        return ",".join(parts)

    if q_type == "SINGLE_CHOICE":
        # 单选题: 标准化为单个字母
        answer = answer.replace("，", ",").strip()
        if "," in answer:
            raise ValueError(f"单选题答案不应包含多个选项: '{answer}'")
        if answer not in OPTION_LETTERS:
            raise ValueError(f"单选题答案无效: '{answer}'")
        return answer

    raise ValueError(f"未知题型: {q_type}")


def convert_questions(questions: list, teacher: str, grade: str, subject: str,
                      task_title: str, quiz_title: str, description: str = "") -> dict:
    """将题目列表转换为 QuickClass JSON 格式"""
    converted_questions = []

    for idx, q in enumerate(questions):
        # 题型
        q_type = normalize_question_type(q.get("type", "SINGLE_CHOICE"))

        # 选项
        options = normalize_options(q.get("options", {}), q_type)

        # 答案
        answer = normalize_answer(q.get("answer", ""), q_type)

        # 难度
        difficulty = normalize_difficulty(q.get("difficulty", "BASIC"))

        # 分值
        score = q.get("score", 0)
        if isinstance(score, str):
            score = int(score) if score.isdigit() else 0

        # 解析
        explanation = q.get("explanation") or None
        if explanation == "":
            explanation = None

        question_obj = {
            "id": generate_cuid2(),
            "type": q_type,
            "content": q.get("content", "").strip(),
            "options": options,
            "answer": answer,
            "difficulty": difficulty,
            "score": score,
            "explanation": explanation,
            "order": idx,
        }
        converted_questions.append(question_obj)

    result = {
        "teacher": teacher,
        "grade": grade,
        "subject": subject,
        "taskTitle": task_title,
        "quizTitle": quiz_title,
        "description": description,
        "questions": converted_questions,
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="将题目数据转换为 QuickClass JSON 格式")
    parser.add_argument("--teacher", required=True, help="教师姓名")
    parser.add_argument("--grade", required=True, help="年级学期，如'三年级下学期'")
    parser.add_argument("--subject", required=True, help="学科，如'数学'")
    parser.add_argument("--task-title", required=True, help="任务标题，如'圆的认识'")
    parser.add_argument("--quiz-title", required=True, help="测验标题，如'练习题'")
    parser.add_argument("--description", default="", help="描述")
    parser.add_argument("--input", required=True, help="输入题目 JSON 文件路径")
    parser.add_argument("--output", required=True, help="输出 QuickClass JSON 文件路径")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        questions = json.load(f)

    if not isinstance(questions, list):
        print("错误: 输入 JSON 应为题目数组", file=sys.stderr)
        sys.exit(1)

    result = convert_questions(
        questions=questions,
        teacher=args.teacher,
        grade=args.grade,
        subject=args.subject,
        task_title=args.task_title,
        quiz_title=args.quiz_title,
        description=args.description,
    )

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"转换完成！共 {len(result['questions'])} 道题目，输出文件: {args.output}")


if __name__ == "__main__":
    main()
