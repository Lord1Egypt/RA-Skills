#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本质控点 skill 的文本入口；逻辑见同目录 `emr_qc_impl.py`（可单独打包）。"""

import argparse
import sys

from emr_qc_impl import (
    DEFAULT_LLM_BASE,
    DEFAULT_LLM_MODEL,
    read_record,
    run_qc,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="门诊病历内涵质控：未记录肿瘤名称（missing-tumor-name）。",
    )
    parser.add_argument("--input", required=True, help="门诊病历文本文件路径（UTF-8）。")
    parser.add_argument(
        "--appkey", required=True,
        help="调用内部医疗大模型的鉴权 key，由平台分配。",
    )
    parser.add_argument(
        "--base", default=DEFAULT_LLM_BASE,
        help=f"大模型 base URL（默认：{DEFAULT_LLM_BASE}）。",
    )
    parser.add_argument(
        "--model", default=DEFAULT_LLM_MODEL,
        help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）。",
    )
    parser.add_argument("--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）。")
    parser.add_argument("--output", default="", help="输出文件路径（默认：../runs/med-emr-qc/missing-tumor-name.txt）。")
    args = parser.parse_args()

    try:
        record = read_record(args.input)
        run_qc(
            record=record,
            appkey=args.appkey,
            base=args.base,
            model=args.model,
            timeout=args.timeout,
            output_path=args.output or None,
        )
        return 0
    except (ValueError, FileNotFoundError) as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
