#!/usr/bin/env python3
"""
团队工作计划汇总脚本
用法:
  python3 summary.py [周度/月度] [周数/月数] [年] [--data <文件路径>]
  python3 summary.py 周度 --data /tmp/workplan_paste.tsv   # 粘贴模式，自动检测周期
  python3 summary.py 周度 13 2026                          # MCP模式，指定第13周
"""

import json
import subprocess
import sys
import re
import csv
import io
from collections import defaultdict
from datetime import datetime, timedelta

# 智能表格配置
DOCID = "dcrZNwuyF7QzK5GW4oQ9B3Y3i6Vdc_RzIxAc1zWMMVr9K4EWCEEza2Ea1XGGuQumBW2IKp9XR6au-lDtMi--j27A"
SHEET_ID = "q979lj"

# 管理层角色
ROLE_MAP = {
    "张鹏乐": ("总经理", 0),
    "王紫龙": ("项目总监", 1),
    "付岩": ("技术总监", 2),
}

# 列名别名映射
COLUMN_ALIASES = {
    "日期": ["日期", "date", "时间", "提交日期"],
    "姓名": ["姓名", "成员", "提交人", "name", "人员"],
    "岗位": ["岗位", "职位", "position", "角色", "role"],
    "计划": ["今日计划", "工作内容", "计划内容", "工作计划", "今日工作", "本日计划", "任务"],
}


def call_smartsheet_get_records():
    """调用 wecom_mcp 获取智能表格记录"""
    cmd = [
        "wecom_mcp", "call", "doc", "smartsheet_get_records",
        json.dumps({"docid": DOCID, "sheet_id": SHEET_ID})
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"MCP调用失败: {result.stderr}")

    try:
        data = json.loads(result.stdout)
        if data.get("errcode") != 0:
            raise Exception(f"API错误: {data.get('errmsg')}")
        return data.get("data", {}).get("records", [])
    except json.JSONDecodeError:
        raise Exception(f"返回数据解析失败: {result.stdout}")


def detect_separator(text):
    """检测分隔符，优先 tab，其次逗号"""
    first_line = text.split('\n')[0] if '\n' in text else text
    if '\t' in first_line:
        return '\t'
    return ','


def match_column(header, field_key):
    """模糊匹配列名到字段键"""
    header_lower = header.strip().lower()
    for alias in COLUMN_ALIASES.get(field_key, []):
        if header_lower == alias.lower():
            return True
    return False


def parse_data_file(filepath):
    """解析 TSV/CSV 文件，返回与 MCP 格式相同的 records 列表"""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    sep = detect_separator(content)
    reader = csv.reader(io.StringIO(content), delimiter=sep)
    rows = list(reader)

    if not rows:
        raise Exception("数据文件为空")

    # 识别表头行（找第一个非空行）
    header_row = None
    data_start = 0
    for i, row in enumerate(rows):
        if any(cell.strip() for cell in row):
            header_row = row
            data_start = i + 1
            break

    if header_row is None:
        raise Exception("未找到表头行")

    # 建立列名到索引的映射
    col_map = {}
    for field_key in COLUMN_ALIASES:
        for j, header in enumerate(header_row):
            if match_column(header, field_key):
                col_map[field_key] = j
                break

    if "日期" not in col_map:
        raise Exception(f"未找到日期列，当前表头：{header_row}")
    if "姓名" not in col_map:
        raise Exception(f"未找到姓名列，当前表头：{header_row}")
    if "计划" not in col_map:
        raise Exception(f"未找到计划列，当前表头：{header_row}")

    date_col = col_map["日期"]
    name_col = col_map["姓名"]
    plan_col = col_map["计划"]
    pos_col = col_map.get("岗位")

    # 转换为内部 records 格式
    # 多行计划处理：编号列表出现在最后一行（含姓名/日期）之前
    # 策略：缓存无姓名/日期的孤立行，遇到有效命名行时将缓存合并为该记录的前置计划内容
    max_col = max(col_map.values())
    records = []
    pending_lines = []  # 缓存等待归属的孤立行

    for row in rows[data_start:]:
        if not any(cell.strip() for cell in row):
            continue

        # 补齐短行
        while len(row) <= max_col:
            row.append("")

        name = row[name_col].strip()
        date_str = row[date_col].strip()
        plan = row[plan_col].strip()

        # 判断是否是有效记录行（有姓名且有日期）
        has_name = bool(name)
        has_date = bool(date_str) and parse_date(date_str) is not None

        if has_name and has_date:
            # 将缓存的孤立行 + 当前行的计划合并
            all_parts = [p for p in pending_lines if p] + ([plan] if plan else [])
            combined_plan = "\n".join(all_parts)
            pending_lines = []

            fields = {
                "日期": date_str,
                "姓名": name,
                "今日计划": combined_plan,
            }
            if pos_col is not None:
                fields["岗位"] = row[pos_col].strip()
            records.append({"fields": fields, "record_id": name})
        elif not has_name and not has_date and plan:
            # 纯文本续行（无姓名也无日期）：缓存，等待归属到下一个有名字的记录
            pending_lines.append(plan)
        # 有日期但无姓名的行（如机器人/匿名条目）直接跳过

    return records


def get_week_range(week_num, year):
    """获取指定周数的日期范围（周一到周五）"""
    jan_1 = datetime(year, 1, 1)
    first_monday = jan_1 + timedelta(days=(7 - jan_1.weekday()) % 7)
    target_monday = first_monday + timedelta(weeks=week_num - 1)

    dates = []
    for i in range(5):
        d = target_monday + timedelta(days=i)
        dates.append(d)

    return dates


def get_month_range(year, month):
    """获取指定月份的日期范围（仅工作日）"""
    from calendar import monthrange
    start = datetime(year, month, 1)
    _, last_day = monthrange(year, month)
    end = datetime(year, month, last_day)

    dates = []
    d = start
    while d <= end:
        if d.weekday() < 5:
            dates.append(d)
        d += timedelta(days=1)

    return dates


def get_week_num(date, year):
    """计算某个日期是该年第几周（与 get_week_range 对应）"""
    jan_1 = datetime(year, 1, 1)
    first_monday = jan_1 + timedelta(days=(7 - jan_1.weekday()) % 7)
    delta = date - first_monday
    if delta.days < 0:
        return 1
    return delta.days // 7 + 1


def parse_date(date_str):
    """解析日期字符串"""
    formats = [
        "%Y年%m月%d日",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def detect_time_range(records, mode="周度"):
    """从记录中自动检测时间范围：找数据量最多的周/月"""
    date_counts = defaultdict(int)

    for record in records:
        fields = record.get("fields", {})
        date_val = fields.get("日期", "")
        if isinstance(date_val, list):
            date_val = date_val[0].get("text", "") if date_val else ""
        elif isinstance(date_val, dict):
            date_val = date_val.get("text", "")

        parsed = parse_date(str(date_val))
        if not parsed:
            continue

        if mode == "周度":
            # 以"年-周数"为键
            year = parsed.year
            wn = get_week_num(parsed, year)
            date_counts[(year, wn)] += 1
        else:
            date_counts[(parsed.year, parsed.month)] += 1

    if not date_counts:
        raise Exception("数据中未找到有效日期，无法自动检测时间范围")

    # 取数据最多的，若相同则取最近的
    best = max(date_counts.keys(), key=lambda k: (date_counts[k], k[0], k[1]))

    if mode == "周度":
        year, week_num = best
        return get_week_range(week_num, year), week_num, year
    else:
        year, month = best
        return get_month_range(year, month), month, year


def filter_by_range(records, date_range, date_field="日期"):
    """按日期范围筛选记录，按人员聚合，保留每条记录的日期"""
    date_set = set(d.date() for d in date_range)
    # 结构: {name: {'岗位': str, '计划': [(date_str, plan_str), ...]}}
    filtered = defaultdict(lambda: {'岗位': '', '计划': []})

    for record in records:
        fields = record.get("fields", {})

        date_val = fields.get(date_field, "")
        if isinstance(date_val, list):
            date_val = date_val[0].get("text", "") if date_val else ""
        elif isinstance(date_val, dict):
            date_val = date_val.get("text", "")

        parsed_date = parse_date(str(date_val))
        if not parsed_date:
            continue

        if parsed_date.date() not in date_set:
            continue

        date_label = parsed_date.strftime("%m/%d")

        name = record.get("record_id", "未知")
        name_field = fields.get("姓名") or fields.get("成员") or fields.get("提交人")

        if name_field:
            if isinstance(name_field, list):
                name = name_field[0].get("text", name) if name_field else name
            elif isinstance(name_field, dict):
                name = name_field.get("text", name)
            else:
                name = str(name_field)

        # 过滤无效记录：空姓名、智能助手等机器人条目
        position_raw = fields.get("岗位", "")
        if isinstance(position_raw, list):
            position_raw = position_raw[0].get("text", "") if position_raw else ""
        elif isinstance(position_raw, dict):
            position_raw = position_raw.get("text", "")
        if not name or name == "未知" or str(position_raw) == "智能助手":
            continue

        plan_field = fields.get("今日计划", "")
        if isinstance(plan_field, list):
            plan = plan_field[0].get("text", "") if plan_field else ""
        elif isinstance(plan_field, dict):
            plan = plan_field.get("text", "")
        else:
            plan = str(plan_field)

        # 无论是否有计划都记录该人（便于识别未提交）
        filtered[name]['计划'].append((date_label, plan.strip()))

        position_field = fields.get("岗位") or fields.get("职位")
        if position_field and not filtered[name]['岗位']:
            if isinstance(position_field, list):
                filtered[name]['岗位'] = position_field[0].get("text", "") if position_field else ""
            elif isinstance(position_field, dict):
                filtered[name]['岗位'] = position_field.get("text", "")
            else:
                filtered[name]['岗位'] = str(position_field)

    return filtered


def format_raw(people, date_range, mode="周度", week_num=None):
    """输出结构化原始数据供 Claude 生成自然语言报告"""
    def sort_key(item):
        name = item[0]
        if name in ROLE_MAP:
            return (ROLE_MAP[name][1], name)
        return (99, name)

    if mode == "周度":
        if week_num is None:
            week_num = get_week_num(date_range[0], date_range[0].year)
        start_str = date_range[0].strftime("%m/%d")
        end_str = date_range[-1].strftime("%m/%d")
        header = f"第{week_num}周（{start_str}-{end_str}）"
        period_label = "本周"
    else:
        month = date_range[0].month
        year = date_range[0].year
        header = f"{year}年{month}月"
        period_label = "本月"

    lines = [f"=== {header}原始工作数据 ===", ""]

    no_plan = []
    for name, info in sorted(people.items(), key=sort_key):
        role = ROLE_MAP[name][0] if name in ROLE_MAP else info['岗位']
        plans = [(d, p) for d, p in info['计划'] if p]

        if not plans:
            no_plan.append(f"{name}（{role}）")
            continue

        lines.append(f"【{name} · {role}】")
        for date_label, plan in plans:
            plan_clean = plan.replace('\n', ' / ').strip()
            lines.append(f"  {date_label}: {plan_clean}")
        lines.append("")

    if no_plan:
        lines.append(f"【{period_label}未提交计划】")
        for p in no_plan:
            lines.append(f"  {p}")
    else:
        lines.append(f"【{period_label}未提交计划】")
        lines.append("  无，全员均有记录")

    lines.append("")
    lines.append("=== END ===")
    return "\n".join(lines)


def main():
    mode = "周度"
    week_num = None
    month = None
    year = None
    data_file = None
    auto_detect = True

    # 解析参数
    args = sys.argv[1:]
    i = 0
    positional = []
    while i < len(args):
        if args[i] == "--data" and i + 1 < len(args):
            data_file = args[i + 1]
            i += 2
        else:
            positional.append(args[i])
            i += 1

    if positional and positional[0] in ["周度", "月度"]:
        mode = positional[0]
        positional = positional[1:]

    if positional:
        if mode == "周度":
            week_num = int(positional[0])
        else:
            month = int(positional[0])
        auto_detect = False

    if len(positional) >= 2:
        year = int(positional[1])

    now = datetime.now()
    if year is None:
        year = now.year

    try:
        # 读取数据
        if data_file:
            records = parse_data_file(data_file)
            print(f"已从文件读取 {len(records)} 条记录")
        else:
            print("正在读取智能表格数据…")
            records = call_smartsheet_get_records()
            print(f"共获取 {len(records)} 条记录")

        # 计算日期范围
        if auto_detect:
            date_range, time_param, detected_year = detect_time_range(records, mode)
            if mode == "周度":
                week_num = time_param
                year = detected_year
                print(f"自动检测到：{year}年第{week_num}周")
            else:
                month = time_param
                year = detected_year
                print(f"自动检测到：{year}年{month}月")
        else:
            if mode == "周度":
                if week_num is None:
                    week_num = get_week_num(datetime(year, now.month, now.day), year)
                date_range = get_week_range(week_num, year)
            else:
                if month is None:
                    month = now.month
                date_range = get_month_range(year, month)

        if not date_range:
            print("错误：无效的日期范围")
            return

        # 筛选数据
        people = filter_by_range(records, date_range)
        print(f"筛选后 {len(people)} 人有记录\n")

        # 输出结构化原始数据
        output = format_raw(people, date_range, mode, week_num)
        print(output)

    except Exception as e:
        print(f"错误：{e}")
        if not data_file:
            print("请确认：\n1. MCP 工具已正确配置\n2. docid 和 sheet_id 正确")


if __name__ == "__main__":
    main()
