# -*- coding: utf-8 -*-
"""
dt_import_ue.py - UE Editor Python 脚本：将修改后的 JSON 导入回 DataTable 并保存
在 UE Editor 内部执行，不可在外部 Python 环境运行

用法（在 UE Editor Output Log 中）：
  py "<skill_path>/scripts/dt_import_ue.py" --json <json_path> --part 1
  py "<skill_path>/scripts/dt_import_ue.py" --json <json_path> --part 0
  py "<skill_path>/scripts/dt_import_ue.py" --json <json_path> --part all
"""

import unreal
import json
import os
import sys


# ========== 配置 ==========

# DataTable 资产路径映射 — 默认值，可通过 --asset-base 参数覆盖
DEFAULT_ASSET_BASE = "/Game/SMG/Configs/DataTables/AISkills"

def get_dt_asset_paths(asset_base=None):
    """生成 DataTable 资产路径映射"""
    base = asset_base or DEFAULT_ASSET_BASE
    return {
        0: f"{base}/DT_AI_Skills_Part0",
        1: f"{base}/DT_AI_Skills_Part1",
        2: f"{base}/DT_AI_Skills_Part2",
        "rogue": f"{base}/DT_AI_Skills_Rogue",
        "main": f"{base}/DT_AI_Skills",
    }

# ID 范围映射
PART_RANGES = {
    0: (200000, 230000),
    1: (230000, 240000),
    2: (240000, 250000),
}


def _auto_find_json(project_root):
    """在项目 Content 目录下自动查找 DataTable JSON 文件"""
    content_dir = os.path.join(project_root, "Content")
    if not os.path.isdir(content_dir):
        return ""
    for dirpath, dirnames, filenames in os.walk(content_dir):
        for f in filenames:
            if f.endswith('.json'):
                full_path = os.path.join(dirpath, f)
                try:
                    with open(full_path, "rb") as fh:
                        raw = fh.read(512)
                    # 快速判断是否为 DataTable 格式
                    for enc in ['utf-8', 'utf-16-le']:
                        try:
                            text = raw.decode(enc)
                            if '"Name"' in text and '[' in text:
                                return full_path
                        except (UnicodeDecodeError, UnicodeError):
                            continue
                except (IOError, OSError):
                    continue
    return ""


def detect_and_read_json(json_path):
    """自动检测编码并读取 JSON"""
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


def filter_skills_by_part(all_skills, part_number):
    """按 Part 范围筛选技能"""
    if part_number not in PART_RANGES:
        unreal.log_error(f"[DT_Import] 不支持的 Part 编号: {part_number}")
        return []
    low, high = PART_RANGES[part_number]
    return [s for s in all_skills if low <= int(s.get("Name", "0")) < high]


def import_part(all_skills, part_number, asset_base=None):
    """导入指定 Part 的技能数据到 DataTable"""
    dt_paths = get_dt_asset_paths(asset_base)
    dt_path = dt_paths.get(part_number)
    if not dt_path:
        unreal.log_error(f"[DT_Import] 未找到 Part{part_number} 的 DataTable 路径")
        return False

    part_skills = filter_skills_by_part(all_skills, part_number)
    if not part_skills:
        unreal.log_warning(f"[DT_Import] Part{part_number} 范围内无技能数据")
        return False

    unreal.log(f"[DT_Import] Part{part_number}: {len(part_skills)} 个技能")

    # 加载 DataTable
    dt = unreal.EditorAssetLibrary.load_asset(dt_path)
    if dt is None:
        unreal.log_error(f"[DT_Import] 无法加载 DataTable: {dt_path}")
        return False

    # 构建 JSON 并导入
    json_string = json.dumps(part_skills, ensure_ascii=False, indent=2)
    result = unreal.DataTableFunctionLibrary.fill_data_table_from_json_string(dt, json_string)

    if not result:
        unreal.log_error(f"[DT_Import] Part{part_number} 导入失败！")
        return False

    unreal.log(f"[DT_Import] Part{part_number} 导入成功")

    # 保存
    save_result = unreal.EditorAssetLibrary.save_asset(dt_path, only_if_is_dirty=False)
    if save_result:
        unreal.log(f"[DT_Import] Part{part_number} 已保存: {dt_path}")
    else:
        unreal.log_warning(f"[DT_Import] Part{part_number} 保存失败，请手动保存")

    return True


def main():
    """主函数 - 解析命令行参数"""
    # 简单的参数解析（UE Python 环境中 argparse 可能有问题）
    args = sys.argv[1:] if len(sys.argv) > 1 else []

    json_path = ""
    part = None
    asset_base = None

    i = 0
    while i < len(args):
        if args[i] == "--json" and i + 1 < len(args):
            json_path = args[i + 1]
            i += 2
        elif args[i] == "--part" and i + 1 < len(args):
            part = args[i + 1]
            i += 2
        elif args[i] == "--asset-base" and i + 1 < len(args):
            asset_base = args[i + 1]
            i += 2
        else:
            i += 1

    # 默认路径回退 — 尝试从环境变量获取项目路径
    if not json_path:
        project_root = os.environ.get("ProjectDir", "")
        if not project_root:
            unreal.log_error("[DT_Import] 未指定 --json 路径，且 ProjectDir 环境变量未设置。")
            unreal.log_error("[DT_Import] 请使用: py \"<script>\" --json \"<json_path>\" --part <n>")
            return
        # 尝试在项目 Content 目录下查找 JSON 文件
        json_path = _auto_find_json(project_root)

    if not os.path.exists(json_path):
        unreal.log_error(f"[DT_Import] JSON 文件不存在: {json_path}")
        return

    unreal.log("=" * 60)
    unreal.log("[DT_Import] 开始导入 AI 技能数据")
    unreal.log(f"[DT_Import] JSON: {json_path}")

    all_skills = detect_and_read_json(json_path)
    unreal.log(f"[DT_Import] 总技能数: {len(all_skills)}")

    # 确定要导入的 Part
    if part == "all":
        parts_to_import = [0, 1, 2]
    elif part is not None:
        parts_to_import = [int(part)]
    else:
        # 默认导入所有
        parts_to_import = [0, 1, 2]

    success_count = 0
    for p in parts_to_import:
        if import_part(all_skills, p, asset_base=asset_base):
            success_count += 1

    unreal.log(f"[DT_Import] 完成！成功导入 {success_count}/{len(parts_to_import)} 个 DataTable")
    unreal.log("=" * 60)


# 执行
main()
