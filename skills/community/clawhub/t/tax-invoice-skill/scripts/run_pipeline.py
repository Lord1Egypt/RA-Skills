#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发票归集自动台账 - 编排入口。

用法:
    python scripts/run_pipeline.py "<票据文件夹>" [--out "<输出xlsx路径>"] [--limit N]

流程:
    遍历目录 -> 本地OCR取字 + 规则定位(必要时本地VLM辅助) -> 校验 -> 按月分组 -> 生成台账Excel
"""
import argparse
import os
import sys

# 确保 scripts 目录在 sys.path，便于互 import
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import config
import field_extractor
import validate
import ledger_builder


def check_dependencies():
    """运行时环境检测：OCR / VLM 缺失则打印明确的安装命令提示并退出。

    坚持全本地离线原则：只检测、只提示，绝不静默联网安装或拉取模型。
    """
    problems = []

    # 1) 本地 OCR 引擎（PaddleOCR）
    try:
        import paddleocr  # noqa: F401
    except Exception:
        problems.append(
            "缺少本地 OCR 引擎 PaddleOCR（发票数字来源基准）。\n"
            "  安装命令: pip install -r " + os.path.join(config.SCRIPTS_DIR, "requirements.txt") + "\n"
            "  （含 paddleocr / paddlepaddle / opencv-python / pymupdf / openpyxl）"
        )

    # 2) 本地多模态模型（Ollama，仅作字段定位兜底）
    try:
        import requests  # noqa: F401
    except Exception:
        problems.append(
            "缺少依赖 requests（用于调用本地 Ollama）。\n"
            "  安装命令: pip install requests"
        )
    else:
        base = config.OLLAMA_API.rsplit("/api/", 1)[0]
        try:
            r = requests.get(base + "/api/tags", timeout=5)
            r.raise_for_status()
            models = [m.get("name", "") for m in r.json().get("models", [])]
            if config.VLM_MODEL not in models:
                problems.append(
                    "本地 Ollama 已运行，但未拉取所需模型 " + config.VLM_MODEL + "。\n"
                    "  拉取命令: ollama pull " + config.VLM_MODEL
                )
        except requests.exceptions.RequestException:
            problems.append(
                "未检测到本地 Ollama 服务（VLM 缺失）。\n"
                "  1) 安装 Ollama: https://ollama.com\n"
                "  2) 启动服务: ollama serve\n"
                "  3) 拉取模型: ollama pull " + config.VLM_MODEL
            )

    if problems:
        print("[环境检测未通过] 无法离线运行，请先完成以下准备：\n", file=sys.stderr)
        for p in problems:
            print("  - " + p + "\n", file=sys.stderr)
        print("说明：本工具坚持全本地离线，不会自动联网安装/拉取，请按上方命令手动准备。", file=sys.stderr)
        sys.exit(1)


def iter_invoice_files(folder):
    """仅读取用户指定目录，返回按文件名排序的发票文件绝对路径列表。"""
    files = []
    for name in sorted(os.listdir(folder)):
        ext = os.path.splitext(name)[1].lower()
        path = os.path.join(folder, name)
        if os.path.isfile(path) and ext in config.INVOICE_EXTS:
            files.append(path)
    return files


def process_file(path):
    """对单张发票执行抽取+校验，返回台账记录字典。"""
    fields, method = field_extractor.extract(path)
    status, remarks, itype = validate.validate(fields)
    month = validate.month_of(fields)
    return {
        "_src": os.path.basename(path),
        "开票日期": fields.get("开票日期", ""),
        "发票类型": itype,
        "销售方名称": fields.get("销售方名称", ""),
        "不含税金额": fields.get("不含税金额", ""),
        "税额": fields.get("税额", ""),
        "价税合计": fields.get("价税合计", ""),
        "发票号码": fields.get("发票号码", ""),
        "票据状态": status,
        "所属月份": month,
        "风险备注": "; ".join(remarks),
        "_method": method,
    }


def main():
    ap = argparse.ArgumentParser(description="发票归集自动台账 - 本地离线生成月度台账")
    ap.add_argument("folder", nargs="?", default=None, help="票据文件夹路径（仅读取此目录）")
    ap.add_argument("--out", default=None, help="输出 xlsx 路径（默认在文件夹内生成 月度财税台账.xlsx）")
    ap.add_argument("--limit", type=int, default=config.FILE_LIMIT, help="单批处理上限")
    args = ap.parse_args()

    folder = args.folder
    if not folder:
        print("[退出] 未提供票据文件夹路径，直接退出。", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(folder):
        print(f"[错误] 文件夹不存在: {folder}", file=sys.stderr)
        sys.exit(2)

    # 运行时环境检测：OCR / VLM 缺失则打印安装提示并退出（不自动联网安装）
    check_dependencies()

    out_path = args.out or os.path.join(folder, "月度财税台账.xlsx")
    files = iter_invoice_files(folder)
    if not files:
        print(f"[提示] 未在 {folder} 找到支持的发票文件（{', '.join(sorted(config.INVOICE_EXTS))}）")
        return

    if len(files) > args.limit:
        print(f"[提示] 共 {len(files)} 个文件，已超上限 {args.limit}，仅处理前 {args.limit} 个（可调大 file_limit 或分批）。")
        files = files[: args.limit]

    records = []
    for i, path in enumerate(files, 1):
        try:
            rec = process_file(path)
        except Exception as e:  # 单张失败不中断整体
            rec = {
                "_src": os.path.basename(path),
                "开票日期": "", "发票类型": "待确认", "销售方名称": "",
                "不含税金额": "", "税额": "", "价税合计": "", "发票号码": "",
                "票据状态": "异常", "所属月份": "未知月份",
                "风险备注": f"处理失败:{e}", "_method": "error",
            }
        records.append(rec)
        print(f"[{i}/{len(files)}] {rec['_src']} -> {rec['票据状态']} ({rec['_method']})")

    ledger_builder.build(records, out_path)

    normal = [r for r in records if r["票据状态"] not in ("异常", "待确认")]
    print(f"\n完成：共 {len(records)} 张，正常 {len(normal)}，异常/待确认 {len(records) - len(normal)}")
    print(f"台账已生成: {out_path}")


if __name__ == "__main__":
    main()
