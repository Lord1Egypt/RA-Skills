"""rebar-audit 命令行入口。stdout 只放结果（人读摘要或 --json 的 JSON），日志一律走 stderr。

退出码：0 无 error 级疑点；2 有 error 级疑点；3 未找到任何数量表；1 运行失败。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import ezdxf
import openpyxl

from . import convert, extract, report, rules, tables as tables_mod
from .symbols import load_symbol_table


def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


def cmd_doctor(args: argparse.Namespace) -> int:
    converters = convert.detect_converters()

    def conv_info(info):
        if info is None:
            return None
        return {"path": info.path, "version": info.version}

    payload = {
        "python_version": sys.version.split()[0],
        "ezdxf_version": ezdxf.__version__,
        "openpyxl_version": openpyxl.__version__,
        "converters": {"oda": conv_info(converters["oda"]), "libredwg": conv_info(converters["libredwg"])},
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(f"Python: {payload['python_version']}")
        print(f"ezdxf: {payload['ezdxf_version']}")
        print(f"openpyxl: {payload['openpyxl_version']}")
        for name, info in payload["converters"].items():
            if info:
                print(f"{name}: {info['path']} (version={info['version']})")
            else:
                print(f"{name}: 未找到")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    input_path = Path(args.input).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.is_file():
        _log(f"输入文件不存在：{input_path}")
        return 1

    conversion_info = None
    if input_path.suffix.lower() == ".dwg":
        _log(f"正在用 --converter {args.converter} 转换 {input_path.name} -> DXF …")
        try:
            dxf_path, conversion_info = convert.convert_dwg_to_dxf(input_path, out_dir, preference=args.converter)
        except convert.ConversionError as exc:
            _log(f"DWG 转换失败：{exc}")
            return 1
        _log(f"转换完成：{dxf_path}（工具={conversion_info['tool']} 版本={conversion_info['tool_version']}）")
    elif input_path.suffix.lower() == ".dxf":
        dxf_path = input_path
    else:
        _log(f"不支持的输入类型：{input_path.suffix}（只接受 .dwg / .dxf）")
        return 1

    try:
        doc, recover_errors = report.read_dxf(dxf_path)
    except Exception as exc:
        _log(f"DXF 读取失败：{exc}")
        return 1
    if recover_errors is not None:
        _log(f"正常读取失败，已用 ezdxf.recover 兜底，auditor 报告 {recover_errors} 处结构错误")

    extraction = extract.extract_all(doc)
    for dxftype, reason in extraction.skipped:
        _log(f"跳过图元 {dxftype}：{reason}")
    _log(f"抽取到文字 {len(extraction.texts)} 条，线段 {len(extraction.segments)} 条")

    symbol_path = Path(args.symbols).resolve() if args.symbols else None
    symbol_table = load_symbol_table(extra_path=symbol_path)

    found_tables = tables_mod.find_tables(extraction.texts, extraction.segments, symbol_table)
    _log(f"识别到数量表 {len(found_tables)} 张")

    findings, gaps = rules.run_all_rules(found_tables)
    symbol_mappings_used = symbol_table.usage_report()

    evidence = report.build_evidence(
        source_path=input_path,
        dxf_path=dxf_path,
        doc=doc,
        recover_error_count=recover_errors,
        conversion_info=conversion_info,
        tables=found_tables,
        findings=findings,
        gaps=gaps,
        symbol_mappings_used=symbol_mappings_used,
    )
    evidence, sanitized_count = report.sanitize_evidence(evidence)
    if sanitized_count:
        _log(f"警告：{sanitized_count} 处文字（多在 raw 字段）仍含无法编码为 utf-8 的孤立代理项，已转成 \\udcXX 转义形式才能写出证据文件，未替换成 '?'")

    evidence_path = out_dir / "evidence.json"
    xlsx_path = out_dir / "钢筋数量表.xlsx"
    report_path = out_dir / "report.md"
    report.write_evidence_json(evidence, evidence_path)
    report.write_xlsx(evidence, xlsx_path)
    report.write_report_md(evidence, report_path)
    _log(f"已写出 {evidence_path}, {xlsx_path}, {report_path}")

    error_count = sum(1 for f in findings if f["severity"] == "error")
    warning_count = sum(1 for f in findings if f["severity"] == "warning")
    # tables_parsed：真正还原出至少一行数据的表数（找到标题但网格不合格/网格异常的表
    # 只产出空表 + R005 gap，不算"还原出了数量表"）。
    tables_parsed = sum(1 for t in found_tables if len(t["rows"]) > 0)
    complete = len(gaps) == 0

    if tables_parsed == 0:
        exit_code = 3  # 未找到或未能还原任何数量表
    elif error_count > 0:
        exit_code = 2
    else:
        exit_code = 0

    summary = {
        "tables": len(found_tables),
        "tables_parsed": tables_parsed,
        "complete": complete,
        "findings": {"error": error_count, "warning": warning_count},
        "gaps": len(gaps),
        "exit_code": exit_code,
        "outputs": {"evidence_json": str(evidence_path), "xlsx": str(xlsx_path), "report_md": str(report_path)},
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
    else:
        print(f"表数：{summary['tables']}（还原出数据行：{tables_parsed}）；error：{error_count}；warning：{warning_count}；证据缺口：{len(gaps)}；complete：{complete}")
        print(f"输出：{evidence_path}\n     {xlsx_path}\n     {report_path}")
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rebar-audit", description="钢筋/材料工程数量表抽取与算术核对")
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="从 DWG/DXF 抽取数量表并核对")
    p_run.add_argument("input", help="输入 .dwg 或 .dxf 文件路径")
    p_run.add_argument("--out", required=True, help="输出目录")
    p_run.add_argument("--symbols", default=None, help="自定义符号映射 JSON（覆盖/追加默认映射）")
    p_run.add_argument("--converter", choices=["auto", "oda", "libredwg"], default="auto", help="DWG 转换器选择")
    p_run.add_argument("--json", action="store_true", help="stdout 只输出 JSON 摘要")
    p_run.set_defaults(func=cmd_run)

    p_doctor = sub.add_parser("doctor", help="报告运行环境状态")
    p_doctor.add_argument("--json", action="store_true")
    p_doctor.set_defaults(func=cmd_doctor)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
