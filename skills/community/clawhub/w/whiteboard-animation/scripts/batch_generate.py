#!/usr/bin/env python3
"""
白板手绘动画 - 批量生成脚本
直接通过命令行参数传入图片路径数组和时长数组，串行调用 generate_whiteboard.py 逐个生成视频。

用法：
  <PYTHON_PATH> batch_generate.py --images img1.png img2.png img3.png --durations 10 15 8 [--output-dir ./output]
"""
import argparse
import subprocess
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
GENERATE_SCRIPT = SCRIPT_DIR / "generate_whiteboard.py"


def main():
    parser = argparse.ArgumentParser(
        description="批量白板手绘动画生成器 - 串行生成多个视频"
    )
    parser.add_argument(
        "--images",
        nargs="+",
        required=True,
        help="图片路径列表（多张图片用空格分隔）"
    )
    parser.add_argument(
        "--durations",
        nargs="+",
        type=int,
        required=True,
        help="时长列表（与图片一一对应，单位毫秒）"
    )
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="输出目录 (默认: ./output)"
    )
    parser.add_argument(
        "--no-hand",
        action="store_true",
        help="禁用手部覆盖效果（对所有任务生效）"
    )
    args = parser.parse_args()

    images = args.images
    durations = args.durations

    # 校验长度一致
    if len(images) != len(durations):
        print(
            f"错误: 图片数量 ({len(images)}) 与时长数量 ({len(durations)}) 不一致"
        )
        sys.exit(1)

    # 校验图片存在
    for i, image_path in enumerate(images):
        if not os.path.exists(image_path):
            print(f"错误: 第 {i + 1} 张图片不存在: {image_path}")
            sys.exit(1)

    total = len(images)
    results = []

    print("=" * 60)
    print(f"批量白板手绘动画生成器 - 共 {total} 个任务")
    print("=" * 60)

    for i, (image, duration) in enumerate(zip(images, durations)):
        print(f"\n{'=' * 60}")
        print(f"[{i + 1}/{total}] 处理: {os.path.basename(image)} (时长: {duration}ms / {duration / 1000:.3f}s)")
        print(f"{'=' * 60}")

        cmd = [
            sys.executable,
            str(GENERATE_SCRIPT),
            image,
            "--output-dir", args.output_dir,
            "--duration", str(duration),
        ]
        if args.no_hand:
            cmd.append("--no-hand")

        result = subprocess.run(cmd)
        success = result.returncode == 0
        results.append({
            "image": image,
            "duration": duration,
            "success": success,
        })

        if not success:
            print(f"\n警告: 第 {i + 1} 个任务失败: {image}")
        else:
            print(f"\n完成: 第 {i + 1}/{total} 个任务")

    # 汇总
    print(f"\n{'=' * 60}")
    print("批量生成完成 - 汇总")
    print(f"{'=' * 60}")
    succeeded = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])
    print(f"  成功: {succeeded}/{total}")
    if failed > 0:
        print(f"  失败: {failed}/{total}")
        for r in results:
            if not r["success"]:
                print(f"    - {r['image']}")
    print(f"\n输出目录: {os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    main()
