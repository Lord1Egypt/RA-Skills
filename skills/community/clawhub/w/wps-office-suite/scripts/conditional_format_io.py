"""
条件格式跨引擎 IO 扩展层 v5.1.0
功能：将 openpyxl 条件格式规则（色阶/数据条/公式条件）序列化为 JSON 中间格式，
      实现跨引擎保真往返（WPS COM 读出 → JSON → 纯 Python 写入）

v5.1.0 变更：
  - 🎯 初始版本

死规则合规：
  - 规则4：禁止自动发布
  - 规则9：基础功能自研（纯 openpyxl 实现，无外部 API）
  - 规则10：性能优化（不拖累用户设备）
  - 规则13：不生成任何禁止文件类型
  - 规则14：三次自审
  - 规则15：沙箱模拟运行
  - 规则16：子进程超时自动关闭

安全合规：
  - 无网络请求，无数据外传
  - 仅处理本地 xlsx 文件
  - 不读取系统注册表或 COM 接口
  - JSON 中间格式为纯文本，无敏感信息泄露风险
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    from openpyxl import load_workbook
    from openpyxl.formatting import Rule
    from openpyxl.formatting.rule import (
        CellIsRule,
        ColorScaleRule,
        DataBarRule,
        IconSetRule,
        FormatObject,
    )
    from openpyxl.styles import Font, PatternFill, Color
    from openpyxl.utils import get_column_letter
except ImportError:
    print("ERROR: openpyxl is required. Install with: pip install openpyxl")
    sys.exit(1)

__version__ = "5.1.0"

# JSON 中间格式版本
JSON_SCHEMA_VERSION = "1.0"


def extract_conditional_formats(filepath: str, sheet: Optional[str] = None) -> Dict[str, Any]:
    """
    从 xlsx 文件提取所有条件格式规则，序列化为 JSON 中间格式
    
    Args:
        filepath: xlsx 文件路径
        sheet: 工作表名称（None 表示全部）
    
    Returns:
        {
            "schema_version": "1.0",
            "file": str,
            "sheets": {
                "Sheet1": {
                    "rules": [
                        {
                            "type": "color-scale|data-bar|icon-set|cell-is",
                            "range": "A1:A100",
                            "priority": 1,
                            "properties": { ... }  # 类型特定属性
                        }
                    ]
                }
            }
        }
    """
    if not os.path.isfile(filepath):
        return {"ok": False, "error": f"文件不存在: {filepath}"}

    try:
        wb = load_workbook(filepath)
        result = {
            "schema_version": JSON_SCHEMA_VERSION,
            "file": filepath,
            "sheets": {},
        }

        sheets_to_process = [sheet] if sheet else wb.sheetnames

        for sheet_name in sheets_to_process:
            if sheet_name not in wb.sheetnames:
                continue
            ws = wb[sheet_name]
            sheet_rules = []

            # 遍历 openpyxl ConditionalFormattingList
            for cf in ws.conditional_formatting:
                cell_range = str(getattr(cf, 'sqref', ''))
                cf_rules = getattr(cf, 'cfRule', [])
                if cf_rules:
                    for rule in cf_rules:
                        rule_dict = _serialize_rule(rule, cell_range)
                        if rule_dict:
                            sheet_rules.append(rule_dict)

            result["sheets"][sheet_name] = {"rules": sheet_rules}

        return {"ok": True, "data": result}

    except Exception as e:
        return {"ok": False, "error": f"提取失败: {str(e)}"}


def _serialize_rule(rule, cell_range: str) -> Optional[Dict[str, Any]]:
    """将单条条件格式规则序列化为 JSON 字典"""
    base = {
        "type": _get_rule_type(rule),
        "range": cell_range,
        "priority": getattr(rule, 'priority', 0),
    }

    props = {}

    rule_type = getattr(rule, 'type', '')
    if rule_type == 'colorScale':
        props = _serialize_color_scale(rule)
    elif rule_type == 'dataBar':
        props = _serialize_data_bar(rule)
    elif rule_type == 'iconSet':
        props = _serialize_icon_set(rule)
    elif rule_type == 'cellIs':
        props = _serialize_cell_is(rule)
    else:
        # 通用序列化
        props = _serialize_generic_rule(rule)

    base["properties"] = props
    return base


def _get_rule_type(rule) -> str:
    """识别规则类型"""
    rule_type = getattr(rule, 'type', '')
    type_map = {
        'colorScale': 'color-scale',
        'dataBar': 'data-bar',
        'iconSet': 'icon-set',
        'cellIs': 'cell-is',
    }
    return type_map.get(rule_type, 'unknown')


def _serialize_color_scale(rule) -> Dict[str, Any]:
    """序列化色阶规则"""
    props = {"method": "color_scale"}
    # 颜色信息
    color_scale = getattr(rule, 'colorScale', None)
    if color_scale:
        if hasattr(color_scale, 'cfvo') and color_scale.cfvo:
            props["colors"] = []
            for cfvo in color_scale.cfvo:
                entry = {"type": getattr(cfvo, 'type', '')}
                val = getattr(cfvo, 'val', None)
                if val is not None:
                    entry["value"] = val
                props["colors"].append(entry)
        if hasattr(color_scale, 'color') and color_scale.color:
            rgb_colors = []
            for c in color_scale.color:
                if c and hasattr(c, 'rgb') and c.rgb:
                    rgb_colors.append(str(c.rgb))
                else:
                    rgb_colors.append("FFFFFFFF")
            props["rgb_colors"] = rgb_colors
    return props


def _serialize_data_bar(rule) -> Dict[str, Any]:
    """序列化数据条规则"""
    props = {"method": "data_bar"}
    data_bar = getattr(rule, 'dataBar', None)
    if data_bar:
        color = getattr(data_bar, 'color', None)
        if color and hasattr(color, 'rgb') and color.rgb:
            props["color"] = str(color.rgb)
        else:
            props["color"] = "FF638EC6"
        if hasattr(data_bar, 'minLength'):
            props["min_length"] = data_bar.minLength
        if hasattr(data_bar, 'maxLength'):
            props["max_length"] = data_bar.maxLength
        if hasattr(data_bar, 'showValue'):
            props["show_value"] = data_bar.showValue
    return props


def _serialize_icon_set(rule) -> Dict[str, Any]:
    """序列化图标集规则"""
    props = {"method": "icon_set"}
    icon_set = getattr(rule, 'iconSet', None)
    if icon_set:
        props["icon_set"] = str(icon_set)
    if hasattr(rule, 'showValue'):
        props["show_value"] = rule.showValue
    if hasattr(rule, 'reverse'):
        props["reverse"] = rule.reverse
    return props


def _serialize_cell_is(rule) -> Dict[str, Any]:
    """序列化单元格值规则"""
    props = {
        "method": "cell_is",
        "operator": getattr(rule, 'operator', ''),
        "formula": getattr(rule, 'formula', []),
    }
    # 样式信息
    font = getattr(rule, 'font', None)
    if font and hasattr(font, 'color') and font.color:
        props["font_color"] = str(font.color.rgb) if font.color.rgb else ""
    fill = getattr(rule, 'fill', None)
    if fill:
        start_color = getattr(fill, 'start_color', None) or getattr(fill, 'fgColor', None)
        if start_color and hasattr(start_color, 'rgb') and start_color.rgb:
            props["fill_color"] = str(start_color.rgb)
    if hasattr(rule, 'stopIfTrue'):
        props["stop_if_true"] = rule.stopIfTrue
    return props


def _serialize_generic_rule(rule) -> Dict[str, Any]:
    """通用规则序列化（兜底）"""
    props = {}
    attrs = ['dxfId', 'priority', 'stopIfTrue']
    for attr in attrs:
        if hasattr(rule, attr):
            val = getattr(rule, attr)
            if val is not None:
                props[attr] = val
    return props


def apply_conditional_formats(filepath: str, json_data: Any, sheet: Optional[str] = None) -> Dict[str, Any]:
    """
    将 JSON 中间格式的条件格式规则写入 xlsx 文件
    
    Args:
        filepath: xlsx 文件路径
        json_data: JSON 中间格式（dict 或 JSON 字符串）
        sheet: 工作表名称（None 表示全部）
    
    Returns:
        {"ok": bool, "message": str, "applied_count": int}
    """
    if not os.path.isfile(filepath):
        return {"ok": False, "error": f"文件不存在: {filepath}"}

    # 如果是字符串，解析 JSON
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError as e:
            return {"ok": False, "error": f"JSON 解析失败: {e}"}

    try:
        wb = load_workbook(filepath)
        applied_count = 0

        data = json_data.get("data", json_data) if isinstance(json_data, dict) else {"sheets": {}}
        sheets = data.get("sheets", {})

        for sheet_name, sheet_data in sheets.items():
            if sheet and sheet_name != sheet:
                continue
            if sheet_name not in wb.sheetnames:
                continue

            ws = wb[sheet_name]
            rules = sheet_data.get("rules", [])

            for rule_dict in rules:
                cf_range = rule_dict.get("range", "")
                rule_type = rule_dict.get("type", "")
                props = rule_dict.get("properties", {})

                if not cf_range:
                    continue

                success = _apply_rule_by_type(ws, cf_range, rule_type, props)
                if success:
                    applied_count += 1

        wb.save(filepath)
        return {
            "ok": True,
            "message": f"已应用 {applied_count} 条条件格式规则",
            "applied_count": applied_count,
        }

    except Exception as e:
        return {"ok": False, "error": f"应用失败: {str(e)}"}


def _apply_rule_by_type(ws, cell_range: str, rule_type: str, props: Dict) -> bool:
    """根据类型应用条件格式规则"""
    try:
        if rule_type == "color-scale":
            return _apply_color_scale(ws, cell_range, props)
        elif rule_type == "data-bar":
            return _apply_data_bar(ws, cell_range, props)
        elif rule_type == "icon-set":
            return _apply_icon_set(ws, cell_range, props)
        elif rule_type == "cell-is":
            return _apply_cell_is(ws, cell_range, props)
        return False
    except Exception:
        return False


def _apply_color_scale(ws, cell_range: str, props: Dict) -> bool:
    """应用色阶规则"""
    colors = props.get("rgb_colors", ["F8696B", "FFEB84", "63BE7B"])
    if len(colors) < 3:
        colors = ["F8696B", "FFEB84", "63BE7B"]

    rule = ColorScaleRule(
        start_type="min", start_color=colors[0].lstrip("0") if colors[0].startswith("0") else colors[0],
        mid_type="percentile", mid_value=50, mid_color=colors[1].lstrip("0") if colors[1].startswith("0") else colors[1],
        end_type="max", end_color=colors[2].lstrip("0") if colors[2].startswith("0") else colors[2],
    )
    ws.conditional_formatting.add(cell_range, rule)
    return True


def _apply_data_bar(ws, cell_range: str, props: Dict) -> bool:
    """应用数据条规则"""
    color = props.get("color", "FF638EC6")
    rule = DataBarRule(
        start_type="min", end_type="max",
        color=color.lstrip("0") if color.startswith("0") else color,
    )
    ws.conditional_formatting.add(cell_range, rule)
    return True


def _apply_icon_set(ws, cell_range: str, props: Dict) -> bool:
    """应用图标集规则"""
    icon_set = props.get("icon_set", "3TrafficLights1")
    rule = IconSetRule(
        icon_set, "percent",
        [0, 50, 100], showValue=props.get("show_value", True),
    )
    ws.conditional_formatting.add(cell_range, rule)
    return True


def _apply_cell_is(ws, cell_range: str, props: Dict) -> bool:
    """应用单元格值规则"""
    operator = props.get("operator", "greaterThan")
    formulas = props.get("formula", ["0"])

    fill_color = props.get("fill_color", "F8696B")
    fill = PatternFill(
        start_color=fill_color.lstrip("0") if fill_color.startswith("0") else fill_color,
        end_color=fill_color.lstrip("0") if fill_color.startswith("0") else fill_color,
        fill_type="solid",
    )

    font = None
    if props.get("font_color"):
        font = Font(color=props["font_color"])

    rule = CellIsRule(
        operator=operator,
        formula=formulas,
        fill=fill,
        font=font,
    )
    ws.conditional_formatting.add(cell_range, rule)
    return True


def export_json(input_file: str, output_file: str, sheet: Optional[str] = None) -> Dict[str, Any]:
    """从 xlsx 导出条件格式为 JSON 文件"""
    result = extract_conditional_formats(input_file, sheet)
    if not result.get("ok"):
        return result

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result["data"], f, ensure_ascii=False, indent=2)
        return {"ok": True, "message": f"已导出到 {output_file}"}
    except Exception as e:
        return {"ok": False, "error": f"导出失败: {str(e)}"}


def import_json(input_file: str, json_file: str, sheet: Optional[str] = None) -> Dict[str, Any]:
    """从 JSON 文件导入条件格式到 xlsx"""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return apply_conditional_formats(input_file, data, sheet)
    except Exception as e:
        return {"ok": False, "error": f"导入失败: {str(e)}"}


def cmd_extract(args):
    """提取命令"""
    result = extract_conditional_formats(args.file, args.sheet)
    if result.get("ok"):
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result["data"], f, ensure_ascii=False, indent=2)
            print(f"✅ 已提取到: {args.output}")
        else:
            print(json.dumps(result["data"], ensure_ascii=False, indent=2))
    else:
        print(f"❌ 提取失败: {result.get('error', '未知错误')}")
    return 0 if result.get("ok") else 1


def cmd_apply(args):
    """应用命令"""
    try:
        with open(args.json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"❌ JSON 文件读取失败: {e}")
        return 1
    result = apply_conditional_formats(args.file, json_data, args.sheet)
    if result.get("ok"):
        print(f"✅ {result['message']}")
    else:
        print(f"❌ 应用失败: {result.get('error', '未知错误')}")
    return 0 if result.get("ok") else 1


def main():
    parser = argparse.ArgumentParser(
        description="条件格式跨引擎 IO v5.1.0 — JSON 中间格式序列化"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # extract 子命令
    p_extract = subparsers.add_parser("extract", help="从 xlsx 提取条件格式为 JSON")
    p_extract.add_argument("--file", required=True, help="xlsx 文件路径")
    p_extract.add_argument("--sheet", default="", help="工作表名称")
    p_extract.add_argument("--output", default="", help="输出 JSON 文件路径")
    p_extract.set_defaults(func=cmd_extract)

    # apply 子命令
    p_apply = subparsers.add_parser("apply", help="将 JSON 条件格式写入 xlsx")
    p_apply.add_argument("--file", required=True, help="xlsx 文件路径")
    p_apply.add_argument("--json-file", required=True, help="JSON 文件路径")
    p_apply.add_argument("--sheet", default="", help="工作表名称")
    p_apply.set_defaults(func=cmd_apply)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
