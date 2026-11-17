# -*- coding: utf-8 -*-
"""
batch_generate_reports.py
批量报告生成脚本（v4.23 积分优化）
用法：python batch_generate_reports.py <configs_dir>

作用：一次性运行 configs_dir 目录下所有 config_*.json，批量生成 HTML 报告。
避免每个视频都单独调用一次 gen_report_template.py，减少 Bash 工具调用次数。
"""
import sys
import os
import glob
import subprocess

PYTHON = r"C:\Users\Admin\.workbuddy\binaries\python\versions\3.13.12\python.exe"
TEMPLATE = r"C:\Users\Admin\WorkBuddy\2026-06-22-16-41-15\gen_report_template.py"

def main(configs_dir):
    if not os.path.isdir(configs_dir):
        print(f"Error: directory not found: {configs_dir}")
        sys.exit(1)

    config_files = sorted(glob.glob(os.path.join(configs_dir, "config_*.json")))
    if not config_files:
        print(f"No config_*.json found in {configs_dir}")
        sys.exit(0)

    print(f"Found {len(config_files)} config files in {configs_dir}")
    success = 0
    failed = []

    for cfg_path in config_files:
        print(f"\n[Processing] {os.path.basename(cfg_path)}")
        r = subprocess.run([PYTHON, TEMPLATE, cfg_path], capture_output=True, text=True)
        if r.stdout:
            print(r.stdout)
        if r.stderr:
            print(r.stderr, file=sys.stderr)
        if r.returncode == 0:
            success += 1
        else:
            failed.append(cfg_path)
            print(f"[FAILED] {cfg_path}")

    print(f"\n{'='*50}")
    print(f"Total: {len(config_files)} | Success: {success} | Failed: {len(failed)}")
    if failed:
        for f in failed:
            print(f"  Failed: {f}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_generate_reports.py <configs_dir>")
        print("Example: python batch_generate_reports.py C:/Users/Admin/WorkBuddy/2026-06-22-16-41-15/.workbuddy/temp_video_analysis")
        sys.exit(1)
    main(sys.argv[1])
