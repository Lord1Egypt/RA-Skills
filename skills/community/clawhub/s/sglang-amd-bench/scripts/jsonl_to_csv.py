#!/usr/bin/env python3
"""Extract sglang benchmark JSONL metrics into InferenceX-compatible CSV."""

import argparse
import csv
import json
import os
import sys
from datetime import date
from glob import glob
from pathlib import Path


COLUMNS = [
    "Model", "ISL", "OSL", "Hardware", "Hardware Key", "Framework", "Precision",
    "TP", "Concurrency", "Date",
    "Throughput/GPU (tok/s)", "Output Throughput/GPU (tok/s)", "Input Throughput/GPU (tok/s)",
    "Mean TTFT (ms)", "Median TTFT (ms)", "P99 TTFT (ms)", "Std TTFT (ms)",
    "Mean TPOT (ms)", "Median TPOT (ms)", "P99 TPOT (ms)", "Std TPOT (ms)",
    "Mean Interactivity (tok/s/user)", "Median Interactivity (tok/s/user)",
    "P99 Interactivity (tok/s/user)", "Std Interactivity (tok/s/user)",
    "Mean ITL (ms)", "Median ITL (ms)", "P99 ITL (ms)", "Std ITL (ms)",
    "Mean E2E Latency (ms)", "Median E2E Latency (ms)", "P99 E2E Latency (ms)", "Std E2E Latency (ms)",
    "Disaggregated", "Num Prefill GPUs", "Num Decode GPUs", "Spec Decoding",
    "EP", "DP Attention", "Is Multinode",
]

HEADER_COMMENT = (
    "# Licensed under Apache License 2.0 — https://www.apache.org/licenses/LICENSE-2.0\n"
)


def ms_to_sec(v):
    if v is None:
        return ""
    return v / 1000.0


def interactivity_from_tpot_ms(tpot_ms):
    if tpot_ms is None or tpot_ms == 0:
        return ""
    return 1000.0 / tpot_ms


def guess_model_name(model_path):
    name = Path(model_path).name
    for suffix in ["-FP8", "-FP4", "-MXFP4", "-BF16", "-INT8", "-INT4"]:
        name = name.replace(suffix, "")
    return name


def detect_spec_decoding(server_info):
    steps = server_info.get("speculative_num_steps", 0)
    if steps and steps > 0:
        return f"mtp{steps}"
    return "none"


def process_jsonl(filepath, args):
    with open(filepath) as f:
        data = json.load(f)

    si = data.get("server_info", {})
    tp = si.get("tp_size", 1)
    num_gpus = tp

    model_name = args.model or guess_model_name(si.get("model_path", "unknown"))

    total_tp = data.get("total_throughput", 0)
    out_tp = data.get("output_throughput", 0)
    in_tp = data.get("input_throughput", 0)

    mean_tpot = data.get("mean_tpot_ms")
    median_tpot = data.get("median_tpot_ms")
    p99_tpot = data.get("p99_tpot_ms")
    std_tpot = data.get("std_tpot_ms")

    disagg_mode = si.get("disaggregation_mode", "null")
    is_disagg = disagg_mode not in ("null", None, "None", "")

    row = {
        "Model": model_name,
        "ISL": data.get("random_input_len", ""),
        "OSL": data.get("random_output_len", ""),
        "Hardware": args.hardware,
        "Hardware Key": f"{args.hardware}_{args.framework}",
        "Framework": args.framework,
        "Precision": args.precision,
        "TP": tp,
        "Concurrency": data.get("max_concurrency", ""),
        "Date": args.date,
        "Throughput/GPU (tok/s)": total_tp / num_gpus if num_gpus else "",
        "Output Throughput/GPU (tok/s)": out_tp / num_gpus if num_gpus else "",
        "Input Throughput/GPU (tok/s)": in_tp / num_gpus if num_gpus else "",
        "Mean TTFT (ms)": ms_to_sec(data.get("mean_ttft_ms")),
        "Median TTFT (ms)": ms_to_sec(data.get("median_ttft_ms")),
        "P99 TTFT (ms)": ms_to_sec(data.get("p99_ttft_ms")),
        "Std TTFT (ms)": ms_to_sec(data.get("std_ttft_ms")),
        "Mean TPOT (ms)": ms_to_sec(mean_tpot),
        "Median TPOT (ms)": ms_to_sec(median_tpot),
        "P99 TPOT (ms)": ms_to_sec(p99_tpot),
        "Std TPOT (ms)": ms_to_sec(std_tpot),
        "Mean Interactivity (tok/s/user)": interactivity_from_tpot_ms(mean_tpot),
        "Median Interactivity (tok/s/user)": interactivity_from_tpot_ms(median_tpot),
        "P99 Interactivity (tok/s/user)": interactivity_from_tpot_ms(p99_tpot),
        "Std Interactivity (tok/s/user)": interactivity_from_tpot_ms(std_tpot),
        "Mean ITL (ms)": ms_to_sec(data.get("mean_itl_ms")),
        "Median ITL (ms)": ms_to_sec(data.get("median_itl_ms")),
        "P99 ITL (ms)": ms_to_sec(data.get("p99_itl_ms")),
        "Std ITL (ms)": ms_to_sec(data.get("std_itl_ms")),
        "Mean E2E Latency (ms)": ms_to_sec(data.get("mean_e2e_latency_ms")),
        "Median E2E Latency (ms)": ms_to_sec(data.get("median_e2e_latency_ms")),
        "P99 E2E Latency (ms)": ms_to_sec(data.get("p99_e2e_latency_ms")),
        "Std E2E Latency (ms)": ms_to_sec(data.get("std_e2e_latency_ms")),
        "Disaggregated": str(is_disagg).lower(),
        "Num Prefill GPUs": "",
        "Num Decode GPUs": "",
        "Spec Decoding": detect_spec_decoding(si),
        "EP": si.get("ep_size", 1),
        "DP Attention": str(si.get("enable_dp_attention", False)).lower(),
        "Is Multinode": str(si.get("nnodes", 1) > 1).lower(),
    }
    return row


def main():
    parser = argparse.ArgumentParser(description="Convert sglang bench JSONL to InferenceX CSV")
    parser.add_argument("--jsonl-dir", required=True, help="Directory containing JSONL files")
    parser.add_argument("--hardware", required=True, help="Hardware name (e.g. mi355x, b200)")
    parser.add_argument("--precision", required=True, help="Precision (e.g. fp4, fp8, bf16)")
    parser.add_argument("--model", default=None, help="Model name override")
    parser.add_argument("--date", default=str(date.today()), help="Benchmark date (YYYY-MM-DD)")
    parser.add_argument("--framework", default="sglang", help="Framework name")
    parser.add_argument("--output", default=None, help="Output CSV path (default: auto-named in jsonl-dir parent)")
    args = parser.parse_args()

    jsonl_files = sorted(glob(os.path.join(args.jsonl_dir, "*.jsonl")))
    if not jsonl_files:
        print(f"Error: No JSONL files found in {args.jsonl_dir}", file=sys.stderr)
        sys.exit(1)

    rows = []
    for f in jsonl_files:
        try:
            rows.append(process_jsonl(f, args))
        except Exception as e:
            print(f"Warning: Failed to process {f}: {e}", file=sys.stderr)

    rows.sort(key=lambda r: (r.get("TP", 0), r.get("Concurrency", 0)))

    if args.output:
        out_path = args.output
    else:
        parent = Path(args.jsonl_dir).parent
        model_name = rows[0]["Model"] if rows else "benchmark"
        out_path = str(parent / f"{model_name}_{args.hardware}_{args.precision}.csv")

    with open(out_path, "w", newline="") as f:
        f.write(HEADER_COMMENT)
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Written {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
