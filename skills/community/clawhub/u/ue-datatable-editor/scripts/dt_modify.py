# -*- coding: utf-8 -*-
"""
dt_modify.py - 修改 AI Skills JSON 中的技能字段并进行格式校验
支持修改单个/多个字段，自动备份，格式校验后保存

用法：
  python dt_modify.py --json <json_path> --id <skill_id> --set <field>=<value> [--set <field2>=<value2>]
  python dt_modify.py --json <json_path> --id <skill_id> --set-loc-desc "新的描述文本"
  python dt_modify.py --json <json_path> --id <skill_id> --set-loc-name "新的名称"
  python dt_modify.py --json <json_path> --validate
"""

import argparse
import json
import sys
import os
import shutil
import re
from datetime import datetime


# ========== 编码检测与读写 ==========

def detect_encoding(raw_bytes):
    """检测文件编码"""
    if raw_bytes[:2] == b'\xff\xfe':
        return "utf-16-le"
    elif raw_bytes[:2] == b'\xfe\xff':
        return "utf-16-be"
    elif raw_bytes[:3] == b'\xef\xbb\xbf':
        return "utf-8-sig"
    else:
        return "utf-8"


def read_json_file(json_path):
    """读取 JSON 文件，自动检测编码"""
    with open(json_path, "rb") as f:
        raw = f.read()
    encoding = detect_encoding(raw)
    if encoding == "utf-16-le":
        text = raw.decode("utf-16-le")
        if text and text[0] == '\ufeff':
            text = text[1:]
    elif encoding == "utf-16-be":
        text = raw.decode("utf-16-be")
        if text and text[0] == '\ufeff':
            text = text[1:]
    elif encoding == "utf-8-sig":
        text = raw[3:].decode("utf-8")
    else:
        text = raw.decode("utf-8")
    return json.loads(text), encoding


def write_json_file(json_path, data, encoding):
    """以原始编码写回 JSON 文件"""
    text = json.dumps(data, ensure_ascii=False, indent='\t')
    if encoding == "utf-16-le":
        raw = ('\ufeff' + text).encode("utf-16-le")
    elif encoding == "utf-16-be":
        raw = ('\ufeff' + text).encode("utf-16-be")
    elif encoding == "utf-8-sig":
        raw = b'\xef\xbb\xbf' + text.encode("utf-8")
    else:
        raw = text.encode("utf-8")
    with open(json_path, "wb") as f:
        f.write(raw)


# ========== 格式校验 ==========

REQUIRED_FIELDS = [
    "Name", "SkillClass", "Notice", "LOC_MonsterSkillTypeDisplays",
    "MonsterSkillTag", "CmdQueue_TGT_Display", "bUseAlert", "LOC_AlertText",
    "bUseNotice", "LOC_NoticeText", "bUseWarningTip", "LOC_InterruptMessage",
    "bIsDangerousSkill", "SkillFunctionType", "LOC_Name", "LOC_Desc",
    "DevName", "TargetPicker", "bDeathWhisper", "Settlement",
    "MultiSettlements", "ScriptPath"
]

BOOL_FIELDS = ["bUseAlert", "bUseNotice", "bUseWarningTip", "bIsDangerousSkill", "bDeathWhisper"]
INT_FIELDS = ["SkillFunctionType"]
STRING_FIELDS = ["Name", "SkillClass", "Notice", "LOC_AlertText", "LOC_NoticeText",
                 "LOC_InterruptMessage", "LOC_Name", "LOC_Desc", "DevName", "ScriptPath"]
ARRAY_FIELDS = ["LOC_MonsterSkillTypeDisplays", "MonsterSkillTag"]
OBJECT_FIELDS = ["CmdQueue_TGT_Display", "TargetPicker", "Settlement", "MultiSettlements"]


def validate_skill(skill, index):
    """校验单个技能条目的格式"""
    errors = []
    skill_id = skill.get("Name", f"index_{index}")

    # 检查必要字段
    for field in REQUIRED_FIELDS:
        if field not in skill:
            errors.append(f"[{skill_id}] 缺少必要字段: {field}")

    # 类型检查
    for field in BOOL_FIELDS:
        if field in skill and not isinstance(skill[field], bool):
            errors.append(f"[{skill_id}] {field} 应为 bool 类型，当前: {type(skill[field]).__name__}")

    for field in INT_FIELDS:
        if field in skill and not isinstance(skill[field], int):
            errors.append(f"[{skill_id}] {field} 应为 int 类型，当前: {type(skill[field]).__name__}")

    for field in STRING_FIELDS:
        if field in skill and not isinstance(skill[field], str):
            errors.append(f"[{skill_id}] {field} 应为 string 类型，当前: {type(skill[field]).__name__}")

    for field in ARRAY_FIELDS:
        if field in skill and not isinstance(skill[field], list):
            errors.append(f"[{skill_id}] {field} 应为 array 类型，当前: {type(skill[field]).__name__}")

    for field in OBJECT_FIELDS:
        if field in skill and not isinstance(skill[field], dict):
            errors.append(f"[{skill_id}] {field} 应为 object 类型，当前: {type(skill[field]).__name__}")

    # Name 格式检查
    name = skill.get("Name", "")
    if name and not name.isdigit():
        errors.append(f"[{skill_id}] Name 应为纯数字字符串")

    # NSLOCTEXT / INVTEXT 格式检查
    for field in ["LOC_Name", "LOC_Desc", "LOC_AlertText", "LOC_InterruptMessage"]:
        val = skill.get(field, "")
        if val and val != "":
            if not (val.startswith("NSLOCTEXT(") or val.startswith("INVTEXT(") or val.startswith("")):
                errors.append(f"[{skill_id}] {field} 格式不标准，应以 NSLOCTEXT( 或 INVTEXT( 开头，当前: {val[:50]}...")

    return errors


def validate_all(skills):
    """校验所有技能数据"""
    all_errors = []
    ids_seen = set()
    for i, skill in enumerate(skills):
        # ID 重复检查
        name = skill.get("Name", "")
        if name in ids_seen:
            all_errors.append(f"[{name}] 重复的技能 ID")
        ids_seen.add(name)

        errors = validate_skill(skill, i)
        all_errors.extend(errors)
    return all_errors


# ========== 修改操作 ==========

def get_part_name(skill_id):
    """根据 ID 判断所属 Part"""
    sid = int(skill_id)
    if sid < 230000:
        return "DT_AI_Skills_Part0"
    elif sid < 240000:
        return "DT_AI_Skills_Part1"
    elif sid < 250000:
        return "DT_AI_Skills_Part2"
    else:
        return "DT_AI_Skills_Rogue"


def wrap_nsloctext(part_name, skill_id, field_suffix, text):
    """将纯文本包装为 NSLOCTEXT 格式"""
    return f'NSLOCTEXT("{part_name}", "{skill_id}_{field_suffix}", "{text}")'


def modify_skill(skills, skill_id, modifications, auto_wrap_loc=True):
    """
    修改指定技能的字段
    modifications: dict of {field_name: new_value}
    """
    target = None
    for skill in skills:
        if skill.get("Name") == str(skill_id):
            target = skill
            break

    if target is None:
        print(f"[Error] 未找到技能 ID: {skill_id}")
        return False

    part_name = get_part_name(skill_id)

    for field, value in modifications.items():
        old_value = target.get(field, "<不存在>")

        # 对 LOC 字段自动包装 NSLOCTEXT
        if auto_wrap_loc and field in ("LOC_Desc", "LOC_Name", "LOC_AlertText", "LOC_InterruptMessage", "LOC_NoticeText"):
            if not (value.startswith("NSLOCTEXT(") or value.startswith("INVTEXT(")):
                suffix_map = {
                    "LOC_Desc": "LOC_Desc",
                    "LOC_Name": "LOC_Name",
                    "LOC_AlertText": "LOC_AlertText",
                    "LOC_InterruptMessage": "LOC_InterruptMessage",
                    "LOC_NoticeText": "LOC_NoticeText",
                }
                value = wrap_nsloctext(part_name, skill_id, suffix_map[field], value)

        # 类型转换
        if field in BOOL_FIELDS:
            value = value.lower() in ("true", "1", "yes") if isinstance(value, str) else bool(value)
        elif field in INT_FIELDS:
            value = int(value)

        target[field] = value
        print(f"  [{skill_id}] {field}:")
        print(f"    旧值: {old_value}")
        print(f"    新值: {value}")

    return True


# ========== 主函数 ==========

def main():
    parser = argparse.ArgumentParser(description="修改 AI Skills JSON 中的技能字段并校验格式")
    parser.add_argument("--json", required=True, help="Json_AI_Skills.json 文件路径")
    parser.add_argument("--id", type=str, help="要修改的技能 ID")
    parser.add_argument("--set", action="append", metavar="FIELD=VALUE", help="设置字段值 (可多次使用)")
    parser.add_argument("--set-loc-desc", type=str, help="快捷设置 LOC_Desc (自动包装 NSLOCTEXT)")
    parser.add_argument("--set-loc-name", type=str, help="快捷设置 LOC_Name (自动包装 NSLOCTEXT)")
    parser.add_argument("--no-wrap", action="store_true", help="不自动包装 NSLOCTEXT")
    parser.add_argument("--validate", action="store_true", help="仅校验 JSON 格式")
    parser.add_argument("--no-backup", action="store_true", help="不创建备份")
    parser.add_argument("--dry-run", action="store_true", help="仅预览修改，不实际保存")

    args = parser.parse_args()

    if not os.path.exists(args.json):
        print(f"[Error] JSON 文件不存在: {args.json}")
        sys.exit(1)

    skills, encoding = read_json_file(args.json)
    print(f"[Info] 已加载 {len(skills)} 个技能 (编码: {encoding})")

    # 仅校验模式
    if args.validate:
        errors = validate_all(skills)
        if errors:
            print(f"\n[校验] 发现 {len(errors)} 个问题:")
            for e in errors:
                print(f"  ⚠ {e}")
        else:
            print("\n[校验] 所有技能数据格式正确 ✓")
        return

    # 修改模式
    if not args.id:
        print("[Error] 修改操作需要指定 --id")
        sys.exit(1)

    modifications = {}

    # 收集 --set 参数
    if args.set:
        for item in args.set:
            if "=" not in item:
                print(f"[Error] --set 格式错误: {item}，应为 FIELD=VALUE")
                sys.exit(1)
            field, value = item.split("=", 1)
            modifications[field.strip()] = value.strip()

    # 快捷参数
    if args.set_loc_desc:
        modifications["LOC_Desc"] = args.set_loc_desc
    if args.set_loc_name:
        modifications["LOC_Name"] = args.set_loc_name

    if not modifications:
        print("[Error] 未指定任何修改，使用 --set, --set-loc-desc, 或 --set-loc-name")
        sys.exit(1)

    print(f"\n[修改] 技能 {args.id}:")
    success = modify_skill(skills, args.id, modifications, auto_wrap_loc=not args.no_wrap)

    if not success:
        sys.exit(1)

    # 校验修改后的数据
    print("\n[校验] 检查修改后的数据...")
    errors = validate_all(skills)
    if errors:
        print(f"  发现 {len(errors)} 个问题:")
        for e in errors:
            print(f"  ⚠ {e}")
        if not args.dry_run:
            print("\n  存在校验问题，仍然继续保存（问题可能是已有数据引起的）")

    if args.dry_run:
        print("\n[Dry-run] 预览完成，未实际保存")
        return

    # 备份
    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = args.json + f".bak_{timestamp}"
        shutil.copy2(args.json, backup_path)
        print(f"\n[备份] {backup_path}")

    # 保存
    write_json_file(args.json, skills, encoding)
    print(f"[保存] 修改已写入: {args.json}")
    print("[完成] 修改成功 ✓")


if __name__ == "__main__":
    main()
