"""DWG -> DXF 转换：探测本机可用的转换器（ODA File Converter 或 GNU LibreDWG dwg2dxf），
按 --converter auto|oda|libredwg 调用，记录工具名、版本（能取就取）与生成 DXF 的 sha256。

两个转换器的可执行文件路径**只**通过环境变量或自动探测取得，不写死具体机器上的安装路径：
  - ODA_FILE_CONVERTER 环境变量 -> C:\\Program Files\\ODA\\*\\ODAFileConverter.exe（及 x86 目录）
  - LIBREDWG_DWG2DXF 环境变量 -> ~/.uking/tools/libredwg-*/dwg2dxf.exe -> PATH 上的 dwg2dxf

ODA File Converter 只接受目录做输入/输出，所以每次转换都把源文件拷进一个临时输入目录再调用；
它转换失败时也可能返回退出码 0，因此一律以「目标 DXF 文件是否真的生成」为准，而不是退出码。
"""
from __future__ import annotations

import glob
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


class ConversionError(RuntimeError):
    pass


@dataclass
class ConverterInfo:
    tool: str  # "oda" | "libredwg"
    path: str
    version: Optional[str]


def _glob_first(patterns: list[str]) -> Optional[Path]:
    for pattern in patterns:
        matches = sorted(Path(p) for p in glob.glob(pattern))
        if matches:
            return matches[0]
    return None


def _oda_version(path: Path) -> Optional[str]:
    # ODAFileConverter.exe 本身没有 --version 出口；安装目录名通常带版本号，能取就取，取不到留 None。
    m = re.search(r"(\d+\.\d+(?:\.\d+)?)", str(path.parent))
    return m.group(1) if m else None


def find_oda() -> Optional[ConverterInfo]:
    env = os.environ.get("ODA_FILE_CONVERTER")
    if env and Path(env).is_file():
        p = Path(env)
        return ConverterInfo("oda", str(p), _oda_version(p))
    found = _glob_first([
        r"C:\Program Files\ODA\*\ODAFileConverter.exe",
        r"C:\Program Files (x86)\ODA\*\ODAFileConverter.exe",
    ])
    if found:
        return ConverterInfo("oda", str(found), _oda_version(found))
    return None


def _libredwg_version(path: Path) -> Optional[str]:
    try:
        out = subprocess.run([str(path), "--version"], capture_output=True, text=True, timeout=15)
        text = (out.stdout or "") + (out.stderr or "")
        m = re.search(r"(\d+\.\d+(?:\.\d+)?)", text)
        return m.group(0) if m else None
    except Exception:
        return None


def find_libredwg() -> Optional[ConverterInfo]:
    env = os.environ.get("LIBREDWG_DWG2DXF")
    if env and Path(env).is_file():
        p = Path(env)
        return ConverterInfo("libredwg", str(p), _libredwg_version(p))
    home = Path(os.path.expanduser("~"))
    found = _glob_first([str(home / ".uking" / "tools" / "libredwg-*" / "dwg2dxf.exe")])
    if found:
        return ConverterInfo("libredwg", str(found), _libredwg_version(found))
    on_path = shutil.which("dwg2dxf")
    if on_path:
        return ConverterInfo("libredwg", on_path, _libredwg_version(Path(on_path)))
    return None


def detect_converters() -> dict[str, Optional[ConverterInfo]]:
    return {"oda": find_oda(), "libredwg": find_libredwg()}


def convert_with_oda(info: ConverterInfo, dwg_path: Path, out_dir: Path, timeout: int = 180) -> Path:
    with tempfile.TemporaryDirectory(prefix="rebar-audit-oda-in-") as tmp_in:
        tmp_in_path = Path(tmp_in)
        shutil.copy2(dwg_path, tmp_in_path / dwg_path.name)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [info.path, str(tmp_in_path), str(out_dir), "ACAD2018", "DXF", "0", "1", dwg_path.name]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise ConversionError(f"ODAFileConverter 超时（>{timeout}s），可能弹出了 GUI 或卡死：{exc}") from exc
        expected = out_dir / (dwg_path.stem + ".dxf")
        if not expected.is_file():
            raise ConversionError(
                f"ODAFileConverter 退出码 {proc.returncode}，但未生成 {expected.name}"
                f"（该工具失败时也可能返回退出码 0，需要靠产物是否存在判断）。"
                f"stdout={proc.stdout[-500:]!r} stderr={proc.stderr[-500:]!r}"
            )
        return expected


def convert_with_libredwg(info: ConverterInfo, dwg_path: Path, out_dir: Path, timeout: int = 180) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    expected = out_dir / (dwg_path.stem + ".dxf")
    cmd = [info.path, "-y", "-o", str(expected), str(dwg_path)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise ConversionError(f"dwg2dxf 超时（>{timeout}s）：{exc}") from exc
    if not expected.is_file():
        raise ConversionError(
            f"dwg2dxf 退出码 {proc.returncode}，未生成 {expected.name}。"
            f"stdout={proc.stdout[-500:]!r} stderr={proc.stderr[-500:]!r}"
        )
    return expected


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def convert_dwg_to_dxf(dwg_path: Path, out_dir: Path, preference: str = "auto") -> tuple[Path, dict]:
    """按 preference 探测并调用转换器，返回 (dxf_path, conversion_info)。

    conversion_info: {tool, tool_path, tool_version, dxf_sha256}
    """
    converters = detect_converters()
    order_map = {"auto": ["oda", "libredwg"], "oda": ["oda"], "libredwg": ["libredwg"]}
    order = order_map.get(preference)
    if order is None:
        raise ConversionError(f"未知的 --converter 取值：{preference!r}（可选 auto|oda|libredwg）")

    errors = []
    for name in order:
        info = converters.get(name)
        if info is None:
            errors.append(f"{name}: 未探测到可用程序")
            continue
        try:
            if name == "oda":
                dxf_path = convert_with_oda(info, dwg_path, out_dir)
            else:
                dxf_path = convert_with_libredwg(info, dwg_path, out_dir)
        except ConversionError as exc:
            errors.append(f"{name}: {exc}")
            continue
        return dxf_path, {
            "tool": info.tool,
            "tool_path": info.path,
            "tool_version": info.version,
            "dxf_sha256": sha256_of(dxf_path),
        }
    raise ConversionError("所有可用转换器都失败或未找到：\n" + "\n".join(errors))
