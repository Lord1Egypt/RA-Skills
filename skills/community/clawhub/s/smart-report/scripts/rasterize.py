"""SVG → PNG 静态光栅化（供 docx/pptx 嵌入图表）。

依赖：resvg-py（pip wheel，无需系统 cairo）。若缺失抛 RasterizerError，
调用方按 5006 EXPORT_ERROR 报结构化错误并给安装建议。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable


class RasterizerError(Exception):
    """所有光栅化失败的统一异常；code=5006 对应 EXPORT_ERROR。"""
    def __init__(self, message: str, suggestion: str = ""):
        super().__init__(message)
        self.message = message
        self.suggestion = suggestion or (
            "pip install resvg-py 启用 PNG 光栅化（pip wheel，无系统依赖）"
        )


def _load_resvg():
    try:
        import resvg_py
        return resvg_py
    except ImportError as e:
        raise RasterizerError(
            f"resvg-py 不可用，无法生成 PNG: {e}",
            suggestion="pip install resvg-py",
        ) from e


def _font_dirs() -> list[str]:
    """查找系统字体目录（供 resvg 渲染 CJK 文本）。"""
    candidates = []
    if os.name == 'posix':
        candidates += ['/System/Library/Fonts', '/Library/Fonts',
                       '/usr/share/fonts', '/usr/share/fonts/truetype']
    elif os.name == 'nt':
        win_fonts = os.environ.get('WINDIR', r'C:\Windows')
        candidates += [os.path.join(win_fonts, 'Fonts')]
    # 仅保留存在的
    return [d for d in candidates if os.path.isdir(d)]


def svg_to_png_bytes(svg_text: str, width: int = 1200, background: str | None = None) -> bytes:
    resvg = _load_resvg()
    kwargs = {'width': width, 'font_dirs': _font_dirs()}
    if background:
        kwargs['background'] = background
    try:
        out = resvg.svg_to_bytes(svg_text, **kwargs)
    except Exception as e:
        raise RasterizerError(f"resvg 渲染失败: {e}") from e
    if not out:
        raise RasterizerError("resvg 返回空字节")
    return out


def rasterize_files(svg_paths: Iterable[Path], png_paths: Iterable[Path],
                    width: int = 1200) -> list[Path]:
    """把每个 SVG 文件转为 PNG，写入对应路径；返回成功的 png_paths 列表。"""
    written: list[Path] = []
    for svg_path, png_path in zip(svg_paths, png_paths):
        svg_text = Path(svg_path).read_text(encoding='utf-8')
        png_bytes = svg_to_png_bytes(svg_text, width=width)
        png_path = Path(png_path)
        png_path.parent.mkdir(parents=True, exist_ok=True)
        png_path.write_bytes(png_bytes)
        written.append(png_path)
    return written