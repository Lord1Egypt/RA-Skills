#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
曲阜师范大学 学分绩点计算器（qfnu-campus-life）

依据《曲阜师范大学学生管理规定》第十七、十八条（曲师大校字〔2017〕55 号）：
    课程绩点（百分制）   = 课程成绩 ÷ 10 - 5        （成绩 < 60 分时课程绩点为 0）
    五级记分制课程绩点    = 优秀4.5 / 良好3.5 / 中等2.5 / 及格1.5 / 不及格0
    课程学分绩点         = 课程绩点 × 课程学分
    平均学分绩点(GPA)    = Σ课程学分绩点 ÷ Σ课程学分

用法：
    # 命令行直接传成绩，格式：课程名:成绩:学分
    python gpa.py --grades "高等数学A:92:5,大学英语:78:4,体育:良好:1"

    # 从 CSV 读取，列顺序：课程名,成绩,学分（首行可为表头）
    python gpa.py --csv courses.csv

    # 学位门槛自检：专业平均 GPA 与个人 GPA
    python gpa.py --major-gpa 2.80 --my-gpa 2.10

    # 推免资格自检：给出专业排名百分比
    python gpa.py --推免 --综测排名 40 --绩点排名 18

注意：
    教务系统实际计入 GPA 的课程范围由教务处规定。推免计算时，师范类计入
    「教师教育理论课 + 政治外语类通识必修 + 专业核心课 + 专业拓展课」，
    非师范类计入「政治外语类通识必修 + 专业核心课 + 专业拓展课」，
    且体育类通识必修课须及格。本脚本“给什么算什么”，
    请在输入时自行剔除不应计入的课程。
"""

import argparse
import csv
import sys

GRADE_MAP = {
    "优秀": 4.5, "优": 4.5,
    "良好": 3.5, "良": 3.5,
    "中等": 2.5, "中": 2.5,
    "及格": 1.5, "及": 1.5, "合格": 1.5,
    "不及格": 0.0, "不合格": 0.0,
}


def to_gp(score):
    """把成绩换算成课程绩点。"""
    s = str(score).strip()
    if s in GRADE_MAP:
        return GRADE_MAP[s]
    try:
        v = float(s)
    except ValueError:
        raise ValueError(
            "无法识别的成绩：%r（应为 0-100 的数字，或 优秀/良好/中等/及格/不及格）" % score
        )
    if not (0.0 <= v <= 100.0):
        raise ValueError("成绩超出 0-100 范围：%s" % v)
    return 0.0 if v < 60 else v / 10.0 - 5.0


def read_grades_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.reader(f)):
            if not row or len(row) < 3:
                continue
            name, score, credit = row[0], row[1], row[2]
            try:
                float(credit)
            except ValueError:
                if i == 0:  # 表头行，跳过
                    continue
                raise ValueError("学分不是数字：%r（第 %d 行）" % (credit, i + 1))
            rows.append((str(name).strip(), score, float(credit)))
    return rows


def parse_grades_text(text):
    rows = []
    for item in text.split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split(":")
        if len(parts) != 3:
            raise ValueError("成绩项格式应为 课程名:成绩:学分，收到：%r" % item)
        rows.append((parts[0].strip(), parts[1].strip(), float(parts[2])))
    return rows


def compute(rows):
    total_credit = 0.0
    total_point = 0.0
    detail = []
    for name, score, credit in rows:
        gp = to_gp(score)
        point = gp * credit
        total_credit += credit
        total_point += point
        detail.append((name, score, credit, gp, point))
    gpa = total_point / total_credit if total_credit else 0.0
    return detail, total_credit, total_point, gpa


def degree_check(major_gpa, my_gpa):
    """学士学位绩点门槛自检。

    细则原文（《曲阜师范大学全日制本科毕业生学士学位授予工作细则（修订）》第八条）：
      个人平均学分绩点不低于本专业平均学分绩点的 65%；
      若本专业平均学分绩点的 65% 高于 1.8 时，以 1.8 为该专业授予学位的最低平均学分绩点。
    文字表述有歧义，这里同时给出两种口径供对照，实际以学院当年公示为准。
    """
    ratio_line = 0.65 * major_gpa
    print("\n【学位绩点门槛自检】")
    print("  专业平均学分绩点        : %.4f" % major_gpa)
    print("  你的平均学分绩点        : %.4f" % my_gpa)
    print("  口径A（按原文65%%）      : 门槛 %.4f → %s"
          % (ratio_line, "达标" if my_gpa >= ratio_line else "未达标"))
    floor = 1.8
    print("  口径B（不低于1.8底线）   : 门槛 %.4f → %s"
          % (floor, "达标" if my_gpa >= floor else "未达标"))
    print("  ⚠ 细则原文表述存在歧义，且专业平均绩点每年变动；")
    print("    最终口径请以学院/教务处当年公示的学位审核名单口径为准。")


def tuimian_check(zhc_rank, gpa_rank, plan="普通推免"):
    """推免基本条件自检（依据学校当年推免工作办法）。"""
    limits = {
        "普通推免": 20.0,
        "研究生支教团": 50.0,
        "农村学校教育硕士师资培养": 30.0,
    }
    limit = limits.get(plan, 20.0)
    print("\n【推免资格自检 · %s】" % plan)
    print("  前6学期综合素质测评排名 : 前 %.1f%% → %s（要求前50%%）"
          % (zhc_rank, "符合" if zhc_rank <= 50 else "不符合"))
    print("  平均学分绩点排名        : 前 %.1f%% → %s（要求前%.0f%%）"
          % (gpa_rank, "符合" if gpa_rank <= limit else "不符合", limit))
    ok = zhc_rank <= 50 and gpa_rank <= limit
    print("  综合结论                : %s"
          % ("满足学校基本门槛（还要看学院细则与名额）" if ok else "未满足学校基本门槛"))
    print("  综合成绩 = 平均学分绩点×90% + 发展性综合评价×10%（各学院权重不同，以学院细则为准）")


def main():
    ap = argparse.ArgumentParser(description="曲阜师范大学学分绩点计算器")
    ap.add_argument("--grades", help='成绩列表，形如 "高数:92:5,英语:78:4,体育:良好:1"')
    ap.add_argument("--csv", help="CSV 文件路径，列：课程名,成绩,学分")
    ap.add_argument("--major-gpa", type=float, help="本专业平均学分绩点（用于学位门槛自检）")
    ap.add_argument("--my-gpa", type=float, help="你的平均学分绩点（用于学位门槛自检）")
    ap.add_argument("--推免", action="store_true", help="进行推免资格自检")
    ap.add_argument("--综测排名", type=float, help="前6学期综测排名百分比，如 40 表示前40%%")
    ap.add_argument("--绩点排名", type=float, help="平均学分绩点排名百分比，如 18 表示前18%%")
    ap.add_argument("--计划", default="普通推免",
                    choices=["普通推免", "研究生支教团", "农村学校教育硕士师资培养"],
                    help="推免计划类型，默认普通推免")
    args = ap.parse_args()

    did = False

    if args.grades or args.csv:
        if args.grades:
            rows = parse_grades_text(args.grades)
        else:
            rows = read_grades_csv(args.csv)
        detail, tc, tp, gpa = compute(rows)
        print("=" * 58)
        print("%-20s %8s %8s %10s %10s" % ("课程", "成绩", "学分", "课程绩点", "学分绩点"))
        print("-" * 58)
        for name, score, credit, gp, point in detail:
            print("%-20s %8s %8.2f %10.4f %10.4f" % (name, score, credit, gp, point))
        print("-" * 58)
        print("%-20s %8s %8.2f %10s %10.4f" % ("合计", "", tc, "", tp))
        print("=" * 58)
        print("平均学分绩点 GPA = %.4f  （即 %.2f）" % (gpa, round(gpa, 2)))
        did = True

    if args.major_gpa is not None and args.my_gpa is not None:
        degree_check(args.major_gpa, args.my_gpa)
        did = True

    if args.推免:
        if args.综测排名 is None or args.绩点排名 is None:
            ap.error("使用 --推免 时请同时提供 --综测排名 与 --绩点排名")
        tuimian_check(args.综测排名, args.绩点排名, args.计划)
        did = True

    if not did:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
