#!/usr/bin/env python3
"""
多幕合并：把各场景的白板动画 MP4 按顺序硬切拼接成一条完整视频。

优先用系统 ffmpeg 无损拼接（-c copy，不重编码）；各片尺寸/编码不一致或无
ffmpeg 时，回退到 PyAV 逐帧重编码并缩放补边到第一段尺寸。单片仍保留。

用法：
  <ENV_PY> merge_scenes.py --inputs a.mp4 b.mp4 c.mp4 --output final.mp4
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path


def _ffmpeg_concat_copy(inputs: list[Path], output: Path) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        return False
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for p in inputs:
            f.write(f"file '{p.resolve().as_posix()}'\n")
        list_path = Path(f.name)
    try:
        res = subprocess.run(
            [ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(list_path), "-c", "copy", str(output)],
            capture_output=True, text=True,
        )
        if res.returncode == 0:
            print(f"  ffmpeg 无损拼接完成: {output}")
            return True
        print(f"  [warn] ffmpeg -c copy 失败，尝试重编码: {res.stderr.strip()[:200]}")
        res = subprocess.run(
            [ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(list_path), "-c:v", "libx264", "-crf", "20",
             "-pix_fmt", "yuv420p", "-vf", "scale='trunc(iw/2)*2':'trunc(ih/2)*2'", str(output)],
            capture_output=True, text=True,
        )
        if res.returncode == 0:
            print(f"  ffmpeg 重编码拼接完成: {output}")
            return True
        print(f"  [warn] ffmpeg 重编码也失败: {res.stderr.strip()[:200]}")
        return False
    finally:
        list_path.unlink(missing_ok=True)


def _fs_path(path: Path) -> str:
    """
    PyAV 底层 libav 期望「文件系统编码」的字节路径；直接传含中文的
    Python str 在 Windows 上会报 ArgumentError（errno 22）。
    这里优先返回 os.fsdecode 后的字符串，无法解码时退回原字符串。
    """
    try:
        raw = os.fsencode(str(path))
        return os.fsdecode(raw)
    except (UnicodeError, ValueError):
        return str(path)


def _pyav_concat(inputs: list[Path], output: Path) -> bool:
    """
    用 PyAV 逐帧重编码并拼接。

    关键点：每段 MP4 的时间戳都从 0 重新开始，若直接连续 encode，输出流的 DTS
    会非单调，libav 会以 ArgumentError(errno 22) 拒绝 mux。因此这里为每帧
    重写 PTS：让第 n 段接在第 n-1 段之后，保持全局单调递增。
    """
    try:
        import av
    except ImportError:
        return False
    first = av.open(_fs_path(inputs[0]))
    vs = first.streams.video[0]
    w, h = vs.codec_context.width, vs.codec_context.height
    rate = vs.average_rate
    first.close()

    out = av.open(_fs_path(output), mode="w")
    ostream = out.add_stream("h264", rate=rate)
    ostream.width, ostream.height = w, h
    ostream.pix_fmt = "yuv420p"
    ostream.options = {"crf": "24", "preset": "medium"}

    # 输出帧的时基：与编码帧率一致，保证 PTS 单调递增。
    # 注意 ostream.time_base 在首次 encode 前为 None，不能直接使用。
    tb = Fraction(1, int(round(float(rate)))) if float(rate) > 0 else Fraction(1, 60)

    offset = 0  # 已写入的累计帧数，作为下一段的 PTS 起点
    for p in inputs:
        cont = av.open(_fs_path(p))
        idx = 0
        for frame in cont.decode(video=0):
            if frame.width != w or frame.height != h:
                frame = frame.reformat(width=w, height=h)
            frame.pts = offset + idx
            frame.time_base = tb
            idx += 1
            for pkt in ostream.encode(frame):
                out.mux(pkt)
        offset += idx
        cont.close()
    for pkt in ostream.encode(None):
        out.mux(pkt)
    out.close()
    print(f"  PyAV 拼接完成: {output}")
    return True


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="按顺序合并多幕白板动画 MP4")
    p.add_argument("--inputs", nargs="+", required=True, help="按播放顺序的 MP4 列表")
    p.add_argument("--output", required=True, help="合并输出路径")
    args = p.parse_args(argv)

    inputs = [Path(x) for x in args.inputs]
    missing = [str(x) for x in inputs if not x.exists()]
    if missing:
        print(f"[err] 缺少输入文件: {', '.join(missing)}", file=sys.stderr)
        return 1
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    if _ffmpeg_concat_copy(inputs, output) or _pyav_concat(inputs, output):
        print(f"OUTPUT={output.resolve()}")
        return 0
    print("[err] 合并失败：系统无 ffmpeg 且 PyAV 不可用", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
