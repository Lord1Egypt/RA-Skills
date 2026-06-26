#!/usr/bin/env python3
"""
一键全跑：依次执行一致性检查、大纲偏差、节奏分析、张力预测
输出汇总报告。
"""

import argparse
import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_script(script_name, args_list, label):
    """运行一个脚本，返回 (success, duration)"""
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, script_name)] + args_list
    print(f"\n{'='*60}")
    print(f"▶ {label}")
    print(f"  命令: {' '.join(cmd)}")
    print(f"{'='*60}")
    start = time.time()
    result = subprocess.run(cmd, capture_output=False)
    duration = time.time() - start
    success = result.returncode == 0
    status = "✅ 通过" if success else "❌ 失败"
    print(f"\n{status} [{label}] 耗时 {duration:.1f}s")
    return success, duration


def main():
    parser = argparse.ArgumentParser(description="一键全跑所有检查脚本")
    parser.add_argument("--novel-dir", required=True, help="小说正文目录")
    parser.add_argument("--outline", help="大纲文件路径")
    parser.add_argument("--character-states", help="角色状态目录")
    parser.add_argument("--dict", help="设定词典文件")
    parser.add_argument("--chapter-list", help="章节列表文件")
    parser.add_argument("--emotion-track", action="store_true", help="启用情感追踪（节奏分析）")
    args = parser.parse_args()

    novel_dir = os.path.abspath(args.novel_dir)
    results = []

    # 1. 一致性检查
    cc_args = [novel_dir]
    if args.dict:
        cc_args.extend(["--dict", args.dict])
    if args.character_states:
        cc_args.extend(["--character-states", args.character_states])
    if args.chapter_list:
        cc_args.extend(["--chapter-list", args.chapter_list])
    if args.outline:
        cc_args.extend(["--outline", args.outline])
    success, dur = run_script("consistency_check.py", cc_args, "一致性检查")
    results.append(("一致性检查", success, dur))

    # 2. 大纲偏差
    if args.outline:
        od_args = [novel_dir, "--outline", args.outline]
        if args.chapter_list:
            od_args.extend(["--chapter-list", args.chapter_list])
        success, dur = run_script("outline_drift.py", od_args, "大纲偏差检测")
        results.append(("大纲偏差检测", success, dur))
    else:
        results.append(("大纲偏差检测", None, 0))

    # 3. 节奏分析
    rc_args = [novel_dir]
    if args.emotion_track:
        rc_args.append("--emotion-track")
    success, dur = run_script("rhythm_check.py", rc_args, "节奏分析")
    results.append(("节奏分析", success, dur))

    # 4. 张力预测
    tf_args = [novel_dir]
    success, dur = run_script("tension_forecast.py", tf_args, "张力预测")
    results.append(("张力预测", success, dur))

    # 汇总
    print(f"\n{'='*60}")
    print("📋 汇总报告")
    print(f"{'='*60}")
    for label, success, dur in results:
        if success is None:
            status = "⏭️ 跳过"
        elif success:
            status = "✅ 通过"
        else:
            status = "❌ 失败"
        print(f"  {status} {label} ({dur:.1f}s)")

    total_time = sum(d for _, _, d in results)
    passed = sum(1 for _, s, _ in results if s is True)
    total = sum(1 for _, s, _ in results if s is not None)
    print(f"\n  总耗时 {total_time:.1f}s | 通过 {passed}/{total}")

    # 有失败则返回非0
    if any(s is False for _, s, _ in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
