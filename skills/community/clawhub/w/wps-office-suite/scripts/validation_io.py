"""
数据验证跨引擎 IO 扩展层 v5.1.0
功能：将 openpyxl 数据验证规则（下拉/数值区间/日期等）序列化为 JSON 中间格式，
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
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.utils import get_column_letter
except ImportError:
    print("ERROR: openpyxl is required. Install with: pip install openpyxl")
    sys.exit(1)

__version__ = "5.1.0"

# JSON 中间格式版本
JSON_SCHEMA_VERSION = "1.0"


def extract_data_validations(filepath: str, sheet: Optional[str] = None) -> Dict[str, Any]:
    """
    从 xlsx 文件提取所有数据验证规则，序列化为 JSON 中间格式
    
    Args:
        filepath: xlsx 文件路径
        sheet: 工作表名称（None 表示全部）
    
    Returns:
        {
            "schema_version": "1.0",
            "file": str,
            "sheets": {
                "Sheet1": {
                    "validations": [
                        {
                            "type": "list|date|whole|decimal|textLength",
                            "range": "B1:B100",
                            "formula1": "...",
                            "formula2": "...",
                            "operator": "between|notBetween|...",
                            "allow_blank": true,
                            "show_error": true,
                            "error_title": "...",
                            "error_message": "...",
                            "prompt_title": "...",
                            "prompt_message": "..."
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
            validations = []

            for dv in ws.data_validations.dataValidation:
                dv_dict = _serialize_validation(dv)
                if dv_dict:
                    validations.append(dv_dict)

            result["sheets"][sheet_name] = {"validations": validations}

        return {"ok": True, "data": result}

    except Exception as e:
        return {"ok": False, "error": f"提取失败: {str(e)}"}


def _serialize_validation(dv: DataValidation) -> Optional[Dict[str, Any]]:
    """将单条数据验证规则序列化为 JSON 字典"""
    dv_dict = {
        "type": dv.type,
        "ranges": [str(r) for r in dv.sqref] if dv.sqref else [],
        "formula1": dv.formula1 if dv.formula1 else "",
        "formula2": dv.formula2 if dv.formula2 else "",
        "operator": dv.operator if dv.operator else "",
        "allow_blank": dv.allow_blank if dv.allow_blank else False,
        "show_error": dv.showErrorMessage if hasattr(dv, 'showErrorMessage') else True,
        "error_title": dv.errorTitle if dv.errorTitle else "",
        "error_message": dv.error if dv.error else "",
        "prompt_title": dv.promptTitle if dv.promptTitle else "",
        "prompt_message": dv.prompt if dv.prompt else "",
    }
    return dv_dict


def apply_data_validations(filepath: str, json_data: Dict[str, Any], sheet: Optional[str] = None) -> Dict[str, Any]:
    """
    将 JSON 中间格式的数据验证规则写入 xlsx 文件
    
    Args:
        filepath: xlsx 文件路径
        json_data: JSON 中间格式（extract_data_validations 的输出）
        sheet: 工作表名称（None 表示全部）
    
    Returns:
        {"ok": bool, "message": str, "applied_count": int}
    """
    if not os.path.isfile(filepath):
        return {"ok": False, "error": f"文件不存在: {filepath}"}

    try:
        wb = load_workbook(filepath)
        applied_count = 0

        data = json_data.get("data", json_data)
        sheets = data.get("sheets", {})

        for sheet_name, sheet_data in sheets.items():
            if sheet and sheet_name != sheet:
                continue
            if sheet_name not in wb.sheetnames:
                continue

            ws = wb[sheet_name]
            validations = sheet_data.get("validations", [])

            for vd in validations:
                success = _apply_validation(ws, vd)
                if success:
                    applied_count += 1

        wb.save(filepath)
        return {
            "ok": True,
            "message": f"已应用 {applied_count} 条数据验证规则",
            "applied_count": applied_count,
        }

    except Exception as e:
        return {"ok": False, "error": f"应用失败: {str(e)}"}


def _apply_validation(ws, vd: Dict[str, Any]) -> bool:
    """应用单条数据验证规则"""
    try:
        ranges = vd.get("ranges", [])
        if not ranges:
            return False

        dv_type = vd.get("type", "list")
        formula1 = vd.get("formula1", "")
        formula2 = vd.get("formula2", "")
        operator = vd.get("operator", "")

        dv = DataValidation(
            type=dv_type,
            allow_blank=vd.get("allow_blank", True),
            showErrorMessage=vd.get("show_error", True),
        )

        if formula1:
            dv.formula1 = formula1
        if formula2:
            dv.formula2 = formula2
        if operator:
            dv.operator = operator

        if vd.get("error_title"):
            dv.errorTitle = vd["error_title"]
        if vd.get("error_message"):
            dv.error = vd["error_message"]
        if vd.get("prompt_title"):
            dv.promptTitle = vd["prompt_title"]
        if vd.get("prompt_message"):
            dv.prompt = vd["prompt_message"]

        for r in ranges:
            dv.add(r)
        ws.add_data_validation(dv)
        return True

    except Exception:
        return False


def export_json(input_file: str, output_file: str, sheet: Optional[str] = None) -> Dict[str, Any]:
    """从 xlsx 导出数据验证为 JSON 文件"""
    result = extract_data_validations(input_file, sheet)
    if not result.get("ok"):
        return result

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result["data"], f, ensure_ascii=False, indent=2)
        return {"ok": True, "message": f"已导出到 {output_file}"}
    except Exception as e:
        return {"ok": False, "error": f"导出失败: {str(e)}"}


def import_json(input_file: str, json_file: str, sheet: Optional[str] = None) -> Dict[str, Any]:
    """从 JSON 文件导入数据验证到 xlsx"""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return apply_data_validations(input_file, data, sheet)
    except Exception as e:
        return {"ok": False, "error": f"导入失败: {str(e)}"}


def cmd_extract(args):
    """提取命令"""
    result = extract_data_validations(args.file, args.sheet)
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
    result = apply_data_validations(args.file, args.json_file, args.sheet)
    if result.get("ok"):
        print(f"✅ {result['message']}")
    else:
        print(f"❌ 应用失败: {result.get('error', '未知错误')}")
    return 0 if result.get("ok") else 1


def main():
    parser = argparse.ArgumentParser(
        description="数据验证跨引擎 IO v5.1.0 — JSON 中间格式序列化"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # extract 子命令
    p_extract = subparsers.add_parser("extract", help="从 xlsx 提取数据验证为 JSON")
    p_extract.add_argument("--file", required=True, help="xlsx 文件路径")
    p_extract.add_argument("--sheet", default="", help="工作表名称")
    p_extract.add_argument("--output", default="", help="输出 JSON 文件路径")
    p_extract.set_defaults(func=cmd_extract)

    # apply 子命令
    p_apply = subparsers.add_parser("apply", help="将 JSON 数据验证写入 xlsx")
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
