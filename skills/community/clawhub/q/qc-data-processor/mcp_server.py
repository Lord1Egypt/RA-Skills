#!/usr/bin/env python3
"""QC Data Processor - MCP Server + CLI
Usage:
  # MCP mode (default)
  python mcp_server.py

  # CLI mode
  python mcp_server.py parse <file>                    # Parse data file
  python mcp_server.py spc <file> [--column COL] [--chart TYPE] [--subgroup N]  # SPC analysis
  python mcp_server.py reliability <file> --time COL --censor COL [--dist DIST]  # Reliability analysis
  python mcp_server.py report <file> [--template TPL] [--product NAME] [--date DATE]  # Generate report
"""

import argparse
import json
import sys

from mcp.server.fastmcp import FastMCP
from tools.parse_data import qc_parse_data
from tools.spc_analyze import qc_spc_analyze
from tools.reliability_analyze import qc_reliability_analyze
from tools.report_generate import qc_report_generate

mcp = FastMCP("QC Tool")


@mcp.tool()
def qc_parse_data_tool(file_path: str, mode: str = "auto") -> dict:
    """Parse quality control data from Excel/CSV file. Auto-detects column types, pipeline (SPC/reliability), and suggests control charts."""
    return qc_parse_data(file_path, mode)


@mcp.tool()
def qc_spc_analyze_tool(data_schema: dict, column: str, subgroup_size: int = None, chart_type: str = "auto") -> dict:
    """Perform SPC analysis: control charts (Xbar-R, I-MR), capability indices (Cp, Cpk, Pp, Ppk), and 8 Western Electric alarm rules."""
    return qc_spc_analyze(data_schema, column, subgroup_size, chart_type)


@mcp.tool()
def qc_reliability_analyze_tool(data_schema: dict, time_column: str, censor_column: str, distribution: str = "auto") -> dict:
    """Perform reliability analysis: Weibull/Lognormal/Exponential fitting, AICc selection, B10/B50/MTTF computation."""
    return qc_reliability_analyze(data_schema, time_column, censor_column, distribution)


@mcp.tool()
def qc_report_generate_tool(analysis_result: dict, template: str, metadata: dict = None) -> str:
    """Generate QC report (daily/weekly/8d/reliability) in Markdown format with ASCII charts."""
    return qc_report_generate(analysis_result, template, metadata)


def _parse_and_bind(file_path: str) -> dict:
    """Parse file and inject _file_path for downstream tools."""
    schema = qc_parse_data(file_path)
    schema["_file_path"] = file_path
    return schema


def cmd_parse(args):
    result = qc_parse_data(args.file)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_spc(args):
    schema = _parse_and_bind(args.file)
    column = args.column
    if not column:
        # auto-select first measurement column
        meas_cols = [c["name"] for c in schema["columns"] if c["type"] == "measurement"]
        column = meas_cols[0] if meas_cols else schema["columns"][0]["name"]
    result = qc_spc_analyze(schema, column, args.subgroup, args.chart)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_reliability(args):
    schema = _parse_and_bind(args.file)
    result = qc_reliability_analyze(schema, args.time, args.censor, args.dist)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_report(args):
    schema = _parse_and_bind(args.file)
    pipeline = schema["pipeline"]

    if pipeline == "spc":
        meas_cols = [c["name"] for c in schema["columns"] if c["type"] == "measurement"]
        column = meas_cols[0] if meas_cols else schema["columns"][0]["name"]
        analysis = qc_spc_analyze(schema, column)
    elif pipeline == "reliability":
        time_cols = [c["name"] for c in schema["columns"] if c["type"] == "time"]
        censor_cols = [c["name"] for c in schema["columns"] if c["type"] == "censor"]
        analysis = qc_reliability_analyze(schema, time_cols[0], censor_cols[0])
    else:
        print(f"Error: unknown pipeline '{pipeline}'", file=sys.stderr)
        sys.exit(1)

    metadata = {}
    if args.product:
        metadata["product"] = args.product
    if args.date:
        metadata["date"] = args.date
    if args.week:
        metadata["week"] = args.week
    if args.customer:
        metadata["customer"] = args.customer

    report = qc_report_generate(analysis, args.template, metadata if metadata else None)
    print(report)


def main():
    parser = argparse.ArgumentParser(
        description="QC Data Processor - MCP Server & CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mcp_server.py parse data/spc_sample.csv
  python mcp_server.py spc data/spc_sample.csv --column measurement
  python mcp_server.py reliability data/reliability_sample.csv --time time --censor censor
  python mcp_server.py report data/spc_sample.csv --template daily --product "Widget" --date 2024-01-01
  python mcp_server.py report data/spc_sample.csv -t weekly --product "Widget" --week W01
  python mcp_server.py report data/reliability_sample.csv -t reliability --product "Widget"
        """
    )
    sub = parser.add_subparsers(dest="command")

    # parse
    p_parse = sub.add_parser("parse", help="Parse QC data file")
    p_parse.add_argument("file", help="Path to CSV/Excel file")

    # spc
    p_spc = sub.add_parser("spc", help="SPC analysis")
    p_spc.add_argument("file", help="Path to CSV/Excel file")
    p_spc.add_argument("--column", "-c", help="Measurement column name (auto-detect if omitted)")
    p_spc.add_argument("--chart", "-C", default="auto", choices=["auto", "Xbar-R", "I-MR"], help="Control chart type")
    p_spc.add_argument("--subgroup", "-n", type=int, help="Subgroup size")

    # reliability
    p_rel = sub.add_parser("reliability", help="Reliability/Weibull analysis")
    p_rel.add_argument("file", help="Path to CSV/Excel file")
    p_rel.add_argument("--time", "-t", required=True, help="Time-to-failure column name")
    p_rel.add_argument("--censor", "-s", required=True, help="Censor indicator column name (1=failure, 0=censored)")
    p_rel.add_argument("--dist", "-d", default="auto", choices=["auto", "Weibull", "Lognormal", "Exponential"], help="Distribution to fit")

    # report
    p_rpt = sub.add_parser("report", help="Generate QC report")
    p_rpt.add_argument("file", help="Path to CSV/Excel file")
    p_rpt.add_argument("--template", "-t", default="daily", choices=["daily", "weekly", "8d", "reliability"], help="Report template")
    p_rpt.add_argument("--product", "-p", help="Product name")
    p_rpt.add_argument("--date", "-d", help="Date (for daily/8d templates)")
    p_rpt.add_argument("--week", "-w", help="Week (for weekly template)")
    p_rpt.add_argument("--customer", help="Customer name (for 8D template)")

    args = parser.parse_args()

    if not args.command:
        # Default: MCP mode
        mcp.run()
        return

    cmds = {
        "parse": cmd_parse,
        "spc": cmd_spc,
        "reliability": cmd_reliability,
        "report": cmd_report,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
