#!/usr/bin/env python3
"""
srt_to_txt.py — SRT 字幕转 TXT 工具（带时间轴）
用法：python scripts/srt_to_txt.py <input.srt> [output.txt]
      若不指定输出路径，默认在同目录下生成同名 .txt 文件
"""

import re
import sys
from pathlib import Path


CANDIDATE_ENCODINGS = ['utf-8-sig', 'utf-8', 'gbk', 'gb18030', 'big5', 'latin-1']


def detect_encoding(path: Path) -> tuple[str, str]:
    """
    依次尝试候选编码，返回第一个能成功解码的 (encoding, content)。
    优先使用 chardet（若已安装），否则回退到逐一尝试。
    """
    # 优先用 chardet
    try:
        import chardet
        raw = path.read_bytes()
        result = chardet.detect(raw)
        detected = result.get('encoding')
        confidence = result.get('confidence', 0)
        # GB2312 是 GBK 的子集，统一用 GBK 解码避免兼容性问题
        if detected and detected.upper() in ('GB2312', 'GB-2312'):
            detected = 'gbk'
        if detected and confidence >= 0.85:
            try:
                content = raw.decode(detected).replace('\r\n', '\n').replace('\r', '\n')
                # 验证解码结果是否包含 SRT 结构（至少有一个 --> 时间轴）
                if '-->' in content:
                    print(f'[编码检测] chardet: {detected}（置信度 {confidence:.0%}）')
                    return detected, content
            except (UnicodeDecodeError, LookupError):
                pass
    except ImportError:
        pass

    # 回退：逐一尝试候选编码
    raw = path.read_bytes()
    for enc in CANDIDATE_ENCODINGS:
        try:
            content = raw.decode(enc).replace('\r\n', '\n').replace('\r', '\n')
            print(f'[编码检测] 回退探测: {enc}')
            return enc, content
        except (UnicodeDecodeError, LookupError):
            continue

    raise ValueError(f'无法识别文件编码，已尝试：{CANDIDATE_ENCODINGS}')


def srt_to_txt(srt_path: str, txt_path: str | None = None) -> Path:
    """
    将 SRT 文件转换为带时间轴的 TXT 文件。
    返回输出文件的 Path 对象。
    """
    src = Path(srt_path)
    if not src.exists():
        raise FileNotFoundError(f'找不到文件：{srt_path}')

    dst = Path(txt_path) if txt_path else src.with_suffix('.txt')

    # 编码检测
    encoding, content = detect_encoding(src)

    # 解析字幕块
    blocks = re.split(r'\n\n+', content.strip())
    lines = []

    for block in blocks:
        parts = block.strip().split('\n')
        if len(parts) < 2:
            continue

        # 跳过序号行（纯数字）
        start = 1 if re.match(r'^\d+$', parts[0].strip()) else 0
        if start >= len(parts):
            continue

        # 提取时间轴
        time_line = parts[start].strip()
        if '-->' not in time_line:
            continue

        # 合并多行文本为一行
        text = ' '.join(p.strip() for p in parts[start + 1:] if p.strip())
        if text:
            lines.append(f'[{time_line}] {text}')

    # 写出，统一使用 UTF-8
    dst.write_text('\n\n'.join(lines), encoding='utf-8')

    print(f'[完成] {len(lines)} 条字幕 → {dst}')
    print(f'[时长] {_last_timestamp(lines)}')
    return dst


def _last_timestamp(lines: list[str]) -> str:
    """从最后一条字幕提取结束时间戳，用于估算视频时长。"""
    if not lines:
        return '未知'
    last = lines[-1]
    m = re.search(r'--> (\d{2}:\d{2}:\d{2})', last)
    return m.group(1) if m else '未知'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        srt_to_txt(input_path, output_path)
    except (FileNotFoundError, ValueError) as e:
        print(f'[错误] {e}', file=sys.stderr)
        sys.exit(1)
