# -*- coding: utf-8 -*-
"""
dt_search.py - 在 AI Skills JSON 中检索技能数据
支持按 ID、名称、关键字等多种方式查询

用法：
  python dt_search.py --json <json_path> --id <skill_id>
  python dt_search.py --json <json_path> --name <keyword>
  python dt_search.py --json <json_path> --field <field_name> --value <value>
  python dt_search.py --json <json_path> --part <part_number>
  python dt_search.py --json <json_path> --list-fields
"""

import argparse
import json
import sys
import os


def detect_and_read_json(json_path):
    """自动检测编码并读取 JSON 文件（支持 UTF-16 LE/BE、UTF-8 BOM、UTF-8）"""
    with open(json_path, "rb") as f:
        raw = f.read()
    if raw[:2] == b'\xff\xfe':
        text = raw.decode("utf-16-le")
        if text and text[0] == '\ufeff':
            text = text[1:]
    elif raw[:2] == b'\xfe\xff':
        text = raw.decode("utf-16-be")
        if text and text[0] == '\ufeff':
            text = text[1:]
    elif raw[:3] == b'\xef\xbb\xbf':
        text = raw[3:].decode("utf-8")
    else:
        text = raw.decode("utf-8")
    return json.loads(text)


def get_part_range(part_number):
    """根据 Part 编号返回 ID 范围"""
    ranges = {
        0: (200000, 230000),
        1: (230000, 240000),
        2: (240000, 250000),
    }
    return ranges.get(part_number, None)


def search_by_id(skills, skill_id):
    """按 ID 精确搜索"""
    return [s for s in skills if s.get("Name") == str(skill_id)]


def search_by_name(skills, keyword):
    """按 DevName 或 LOC_Name 模糊搜索"""
    keyword_lower = keyword.lower()
    results = []
    for s in skills:
        dev_name = s.get("DevName", "").lower()
        loc_name = s.get("LOC_Name", "").lower()
        notice = s.get("Notice", "").lower()
        if keyword_lower in dev_name or keyword_lower in loc_name or keyword_lower in notice:
            results.append(s)
    return results


def search_by_field(skills, field_name, value):
    """按指定字段值搜索"""
    results = []
    for s in skills:
        field_val = s.get(field_name)
        if field_val is not None:
            if isinstance(field_val, str) and value.lower() in field_val.lower():
                results.append(s)
            elif str(field_val) == str(value):
                results.append(s)
    return results


def search_by_part(skills, part_number):
    """按 Part 范围筛选"""
    part_range = get_part_range(part_number)
    if not part_range:
        print(f"[Error] 未知的 Part 编号: {part_number}，支持 0/1/2")
        return []
    low, high = part_range
    return [s for s in skills if low <= int(s.get("Name", "0")) < high]


def print_skill_summary(skill):
    """简要打印技能信息"""
    print(f"  ID: {skill.get('Name')}")
    print(f"  DevName: {skill.get('DevName', 'N/A')}")
    print(f"  LOC_Name: {skill.get('LOC_Name', '')}")
    print(f"  LOC_Desc: {skill.get('LOC_Desc', '')}")
    print(f"  SkillClass: {skill.get('SkillClass', '')}")
    print(f"  Notice: {skill.get('Notice', '')}")
    print()


def print_skill_full(skill):
    """完整打印技能 JSON"""
    print(json.dumps(skill, ensure_ascii=False, indent=2))
    print()


def list_all_fields(skills):
    """列出所有字段名"""
    fields = set()
    for s in skills:
        fields.update(s.keys())
    print("可用字段列表:")
    for f in sorted(fields):
        print(f"  - {f}")


def main():
    parser = argparse.ArgumentParser(description="在 AI Skills JSON 中检索技能数据")
    parser.add_argument("--json", required=True, help="Json_AI_Skills.json 文件路径")
    parser.add_argument("--id", type=str, help="按技能 ID 精确搜索")
    parser.add_argument("--name", type=str, help="按名称关键字模糊搜索 (DevName/LOC_Name/Notice)")
    parser.add_argument("--field", type=str, help="按指定字段搜索 (配合 --value)")
    parser.add_argument("--value", type=str, help="字段值 (配合 --field)")
    parser.add_argument("--part", type=int, help="按 Part 编号筛选 (0/1/2)")
    parser.add_argument("--list-fields", action="store_true", help="列出所有可用字段")
    parser.add_argument("--full", action="store_true", help="显示完整 JSON 而非摘要")
    parser.add_argument("--limit", type=int, default=20, help="最大显示数量 (默认 20)")

    args = parser.parse_args()

    if not os.path.exists(args.json):
        print(f"[Error] JSON 文件不存在: {args.json}")
        sys.exit(1)

    skills = detect_and_read_json(args.json)
    print(f"[Info] 已加载 {len(skills)} 个技能\n")

    if args.list_fields:
        list_all_fields(skills)
        return

    results = None

    if args.id:
        results = search_by_id(skills, args.id)
        print(f"[搜索] ID = {args.id}")
    elif args.name:
        results = search_by_name(skills, args.name)
        print(f"[搜索] 名称包含 '{args.name}'")
    elif args.field and args.value:
        results = search_by_field(skills, args.field, args.value)
        print(f"[搜索] {args.field} 包含 '{args.value}'")
    elif args.part is not None:
        results = search_by_part(skills, args.part)
        print(f"[搜索] Part{args.part} 范围技能")
    else:
        print("[Error] 请指定搜索条件: --id, --name, --field+--value, --part, 或 --list-fields")
        sys.exit(1)

    if not results:
        print("未找到匹配结果。")
        return

    print(f"找到 {len(results)} 个结果" + (f" (显示前 {args.limit} 个)" if len(results) > args.limit else "") + ":\n")

    for skill in results[:args.limit]:
        if args.full:
            print_skill_full(skill)
        else:
            print_skill_summary(skill)


if __name__ == "__main__":
    main()
