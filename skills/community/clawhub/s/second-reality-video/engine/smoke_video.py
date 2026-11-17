"""端到端 smoke：extract → render 跑两遍，逐帧哈希必须逐字节一致。

这是「确定性渲染流水线」的最小可执行证明：
不依赖外部产物，只依赖 pygame / pyyaml / cryptography / ffmpeg(PATH)。

用法：python smoke_video.py
退出码：0 = PASS，1 = FAIL。
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable


def run_cli(args):
    r = subprocess.run(
        [PY, "-m", "video.cli", *args],
        cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        raise SystemExit(f"FAILED: python -m video.cli {' '.join(args)}")
    return r.stdout


def pipeline(work: Path, tag: str) -> str:
    """跑一遍 extract → render，返回 hashes.txt 全文。"""
    out = work / tag
    out.mkdir(parents=True, exist_ok=True)
    run_cli([
        "extract", "--world-id", "smoke", "--world", str(out / "world"),
        "--seed", "42", "--agents", "4", "--ticks", "0-10",
        "--out", str(out / "states.jsonl"),
    ])
    run_cli([
        "render", "--state", str(out / "states.jsonl"),
        "--shot", str(ROOT / "video" / "shots" / "demo.yaml"),
        "--tier", "R1", "--samples", "0",
        "--out", str(out / "world.mp4"),
    ])
    return (out / "hashes.txt").read_text(encoding="utf-8")


def main():
    work = Path(tempfile.mkdtemp(prefix="sr-video-smoke-"))
    try:
        h1 = pipeline(work, "run1")
        h2 = pipeline(work, "run2")
        n = len([x for x in h1.splitlines() if x.strip()])
        if h1 != h2:
            first = next(
                (i for i, (a, b) in enumerate(zip(h1.splitlines(), h2.splitlines())) if a != b),
                None,
            )
            print(f"SMOKE FAIL: {n} 帧中首个分歧在第 {first} 帧，两次运行哈希序列不一致")
            raise SystemExit(1)
        print(f"SMOKE PASS: {n} 帧，两次独立运行逐帧哈希逐字节一致")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
