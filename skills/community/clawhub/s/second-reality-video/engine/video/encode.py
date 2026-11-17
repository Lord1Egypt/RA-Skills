"""视频编码：raw RGB24 帧流 → mp4（ffmpeg rawvideo 管道）。

为什么走管道而不落盘 PNG
------------------------
1. 逐帧 PNG 让编码绑定在 `frame_%04d.png` 的名字序列上，帧号一旦跳号
   ffmpeg 的 image2 解复用器就会截断 —— 旧实现正是在这里产出过 0.37 秒的废片；
2. 管道直接喂 rawvideo，帧序即写入序，不存在"按文件名排序"这一层不确定性。

复现锚点
--------
逐帧 sha256 是本管线的**主复现锚点**；mp4 容器哈希只作旁证
（容器含封装层元数据，即使 `-fflags +bitexact` 也不保证跨 ffmpeg 版本一致）。
"""

import hashlib
import subprocess
from pathlib import Path
from typing import Iterable, List

# x264 多线程会改变码流切分（帧级并行导致熵编码边界漂移），
# 故强制单线程以保证同输入同码流。
DETERMINISTIC_ARGS = [
    "-threads", "1",
    "-fflags", "+bitexact",
    "-flags", "+bitexact",
    "-map_metadata", "-1",
    "-movflags", "+faststart",
]


def ffmpeg_available() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True,
                       check=True, timeout=10)
        return True
    except Exception:
        return False


def encode_raw_stream(frames: Iterable[bytes], output_path: str,
                      width: int, height: int, fps: int,
                      codec: str = "libx264", crf: int = 18,
                      preset: str = "medium") -> List[str]:
    """把 RGB24 帧流编码成 mp4，返回逐帧 sha256 列表。

    Args:
        frames: 可迭代的 RGB24 帧（每帧恰好 width*height*3 字节）
        output_path: 输出 mp4 路径
        width/height: 帧尺寸
        fps: 输出帧率

    Returns:
        逐帧 sha256（顺序与写入顺序一致）

    Raises:
        ValueError: 帧字节数与 width*height*3 不符
        RuntimeError: ffmpeg 退出码非 0
    """
    if not ffmpeg_available():
        raise RuntimeError(
            "ffmpeg not found. Windows: winget install ffmpeg / choco install ffmpeg"
        )

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    frame_size = width * height * 3

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}", "-r", str(fps),
        "-i", "-",
        "-an",
        "-c:v", codec, "-crf", str(crf), "-preset", preset,
        "-pix_fmt", "yuv420p",
        *DETERMINISTIC_ARGS,
        str(out),
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    hashes: List[str] = []
    try:
        for frame in frames:
            if len(frame) != frame_size:
                raise ValueError(
                    f"frame size mismatch: got {len(frame)}, expected {frame_size}"
                )
            hashes.append(hashlib.sha256(frame).hexdigest())
            proc.stdin.write(frame)
    except BrokenPipeError:
        pass  # ffmpeg 提前退出，错误在下方统一抛出
    finally:
        if proc.stdin is not None:
            try:
                proc.stdin.close()
            except BrokenPipeError:
                pass

    stderr = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
    code = proc.wait()
    if code != 0:
        raise RuntimeError(f"ffmpeg failed (exit {code}): {stderr[-900:]}")
    if not hashes:
        raise RuntimeError("no frames were written")

    return hashes


# ---- 逐帧哈希序列的读写（复现锚点的载体）----

def save_frame_hashes(hashes: List[str], path: str) -> str:
    """保存逐帧哈希序列，返回该序列自身的 sha256（可写进 manifest）。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        for h in hashes:
            f.write(h + '\n')
    return hashlib.sha256('\n'.join(hashes).encode('utf-8')).hexdigest()


def load_frame_hashes(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def hashes_digest(hashes: List[str]) -> str:
    """哈希序列的摘要 —— 长视频的单一复现锚（避免逐帧比对的开销）。"""
    return hashlib.sha256('\n'.join(hashes).encode('utf-8')).hexdigest() if hashes else ""


def diff_hash_sequences(a: List[str], b: List[str]) -> dict:
    """两个逐帧哈希序列的比对结果。"""
    n = min(len(a), len(b))
    first_mismatch = next((i for i in range(n) if a[i] != b[i]), None) \
        if len(a) == len(b) else None
    return {
        "frames_a": len(a),
        "frames_b": len(b),
        "length_equal": len(a) == len(b),
        "identical_count": sum(1 for i in range(n) if a[i] == b[i]),
        "different_count": n - sum(1 for i in range(n) if a[i] == b[i]),
        "first_mismatch_index": first_mismatch,
        "identical": len(a) == len(b) and first_mismatch is None,
    }
