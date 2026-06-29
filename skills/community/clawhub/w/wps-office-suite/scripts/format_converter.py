# 格式转换脚本 v2.0 - 三引擎支持
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from wps_common import get_wps, release_wps, safe_path, detect_engine


def convert_format(input_path: str, output_format: str) -> dict:
    """单文件格式转换（自动选择引擎）"""
    try:
        filepath = safe_path(input_path).resolve()
        if not filepath.exists():
            return {"success": False, "error": f"文件不存在: {filepath}"}

        engine = detect_engine()
        ext = filepath.suffix.lower()
        output_path = filepath.with_suffix(f".{output_format}")

        # Word 转换
        if ext == ".docx":
            if engine in ("WPS", "MSOFFICE"):
                wps = get_wps()
                doc = wps.Documents.Open(str(filepath))
                fmt_map = {"pdf": 17, "txt": 7, "html": 8}
                fmt = fmt_map.get(output_format)
                if fmt is None:
                    doc.Close()
                    release_wps()
                    return {
                        "success": False,
                        "error": f"Word 不支持转 {output_format}，支持: {list(fmt_map.keys())}",
                    }
                doc.SaveAs(str(output_path), fmt)
                doc.Close()
                release_wps()
            else:
                return {
                    "success": False,
                    "error": "纯 Python 模式不支持 Word 格式转换，请安装 WPS 或 MS Office",
                }

        # Excel 转换
        elif ext == ".xlsx":
            if engine in ("WPS", "MSOFFICE"):
                wps = get_wps()
                wb = wps.Workbooks.Open(str(filepath))
                if output_format == "csv":
                    wb.SaveAs(str(output_path), 6)
                elif output_format == "pdf":
                    wb.SaveAs(str(output_path), 0)
                elif output_format == "xlsx":
                    wb.SaveAs(str(output_path), 51)
                else:
                    wb.Close()
                    release_wps()
                    return {
                        "success": False,
                        "error": f"Excel 不支持转 {output_format}，支持: csv/pdf/xlsx",
                    }
                wb.Close()
                release_wps()
            else:
                return {
                    "success": False,
                    "error": "纯 Python 模式不支持 Excel 格式转换，请安装 WPS 或 MS Office",
                }

        # PPT 转换
        elif ext == ".pptx":
            if engine in ("WPS", "MSOFFICE"):
                wps = get_wps()
                ppt = wps.Presentations.Open(str(filepath))
                if output_format == "pdf":
                    ppt.SaveAs(str(output_path), 32)
                elif output_format in ("png", "jpg"):
                    ppt.SaveAs(str(output_path), 17)
                else:
                    ppt.Close()
                    release_wps()
                    return {
                        "success": False,
                        "error": f"PPT 不支持转 {output_format}，支持: pdf/png/jpg",
                    }
                ppt.Close()
                release_wps()
            else:
                return {
                    "success": False,
                    "error": "纯 Python 模式不支持 PPT 格式转换，请安装 WPS 或 MS Office",
                }

        else:
            return {"success": False, "error": f"不支持的文件类型: {ext}"}

        return {"success": True, "path": str(output_path), "engine": engine}

    except Exception as e:
        return {"success": False, "error": str(e)}


def batch_convert(input_dir: str, input_format: str, output_format: str) -> dict:
    """批量转换（带逐文件进度）"""
    try:
        input_dir = Path(input_dir).resolve()
        if not input_dir.exists() or not input_dir.is_dir():
            return {"success": False, "error": f"目录不存在: {input_dir}"}

        files = list(input_dir.glob(f"*.{input_format}"))
        files = [f for f in files if not f.name.startswith("~$")]

        if not files:
            return {"success": True, "message": f"目录内没有 .{input_format} 文件", "results": []}

        engine = detect_engine()
        results = []
        success_count = 0

        for idx, f in enumerate(files, start=1):
            result = convert_format(str(f), output_format)
            result["index"] = f"{idx}/{len(files)}"
            result["file"] = f.name
            if result.get("success"):
                success_count += 1
            results.append(result)

        return {
            "success": True,
            "engine": engine,
            "total": len(files),
            "success_count": success_count,
            "fail_count": len(files) - success_count,
            "message": f"转换完成：{success_count}/{len(files)} 个文件成功",
            "results": results,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="格式转换 v2.0")
    sub = parser.add_subparsers(dest="command", required=True)

    p_convert = sub.add_parser("convert", help="单文件转换")
    p_convert.add_argument("--input", required=True, help="输入文件路径")
    p_convert.add_argument("--output-format", required=True, help="目标格式")

    p_batch = sub.add_parser("batch", help="批量转换")
    p_batch.add_argument("--input-dir", required=True, help="输入目录")
    p_batch.add_argument("--input-format", required=True, help="源格式")
    p_batch.add_argument("--output-format", required=True, help="目标格式")

    args = parser.parse_args()

    try:
        if args.command == "convert":
            result = convert_format(args.input, args.output_format)
        elif args.command == "batch":
            result = batch_convert(args.input_dir, args.input_format, args.output_format)
        else:
            result = {"error": f"未知命令: {args.command}"}

        print(json.dumps(result, ensure_ascii=False, default=str))
    finally:
        release_wps()


if __name__ == "__main__":
    main()
