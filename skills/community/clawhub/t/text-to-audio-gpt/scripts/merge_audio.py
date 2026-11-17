#!/usr/bin/env python3
"""Join compatible MP3 speech segments and validate the resulting audio."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(args: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)


def probe(path: Path) -> dict[str, object]:
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_name,sample_rate,channels:format=duration,size",
            "-of",
            "json",
            str(path),
        ]
    )
    if result.returncode:
        raise RuntimeError(f"Не удалось прочитать {path.name}: {result.stderr.strip()}")
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    if not streams:
        raise RuntimeError(f"В файле нет аудиодорожки: {path.name}")
    info = streams[0]
    fmt = data.get("format", {})
    try:
        duration = float(fmt["duration"])
        sample_rate = int(info["sample_rate"])
        channels = int(info["channels"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(f"Недостаточно метаданных в {path.name}") from exc
    if duration <= 0:
        raise RuntimeError(f"Нулевая длительность: {path.name}")
    return {
        "codec": info.get("codec_name"),
        "sample_rate": sample_rate,
        "channels": channels,
        "duration": duration,
        "size": int(fmt.get("size", path.stat().st_size)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Join compatible MP3 parts in the order supplied and decode-check the result."
    )
    parser.add_argument("output", type=Path, help="Output .mp3 path")
    parser.add_argument("parts", nargs="+", type=Path, help="Input MP3 files, in reading order")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    args = parser.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("Нужны установленные ffmpeg и ffprobe.", file=sys.stderr)
        return 2

    output = args.output.expanduser().resolve()
    inputs = [part.expanduser().resolve() for part in args.parts]
    if output.suffix.lower() != ".mp3":
        print("Укажите для результата расширение .mp3.", file=sys.stderr)
        return 2
    if len(set(inputs)) != len(inputs):
        print("В списке есть повторяющиеся входные файлы.", file=sys.stderr)
        return 2
    if output in inputs:
        print("Выходной файл не должен совпадать с входным.", file=sys.stderr)
        return 2
    if output.exists() and not args.force:
        print(f"Файл уже существует: {output}. Для замены добавьте --force.", file=sys.stderr)
        return 2
    for path in inputs:
        if not path.is_file() or path.stat().st_size == 0:
            print(f"Файл отсутствует или пуст: {path}", file=sys.stderr)
            return 2

    try:
        infos = [probe(path) for path in inputs]
        profiles = {
            (info["codec"], info["sample_rate"], info["channels"]) for info in infos
        }
        if len(profiles) != 1 or next(iter(profiles))[0] != "mp3":
            raise RuntimeError(
                "Фрагменты должны быть MP3 с одинаковыми частотой дискретизации и числом каналов. "
                "Сначала нормализуйте их в один формат, затем запустите сборку снова."
            )

        output.parent.mkdir(parents=True, exist_ok=True)
        expected_duration = sum(float(info["duration"]) for info in infos)
        with tempfile.TemporaryDirectory(prefix=".tta-merge-", dir=output.parent) as temp_name:
            temp_dir = Path(temp_name)
            list_file = temp_dir / "inputs.txt"
            links: list[str] = []
            for index, source in enumerate(inputs, 1):
                link_name = f"part-{index:04d}.mp3"
                os.symlink(source, temp_dir / link_name)
                links.append(link_name)
            list_file.write_text(
                "".join(f"file '{name}'\n" for name in links), encoding="utf-8"
            )
            temp_output = temp_dir / "merged.mp3"
            merged = run(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-y",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(list_file),
                    "-map",
                    "0:a:0",
                    "-c:a",
                    "copy",
                    str(temp_output),
                ],
                cwd=temp_dir,
            )
            if merged.returncode:
                raise RuntimeError(f"Сборка FFmpeg не удалась: {merged.stderr.strip()}")

            final_info = probe(temp_output)
            tolerance = max(2.0, expected_duration * 0.01)
            actual_duration = float(final_info["duration"])
            if abs(actual_duration - expected_duration) > tolerance:
                raise RuntimeError(
                    f"Длительность после сборки отличается: ожидалось около "
                    f"{expected_duration:.2f} с, получено {actual_duration:.2f} с."
                )
            decoded = run(
                ["ffmpeg", "-hide_banner", "-v", "error", "-i", str(temp_output), "-f", "null", "-"]
            )
            if decoded.returncode:
                raise RuntimeError(f"Проверка декодирования не пройдена: {decoded.stderr.strip()}")
            os.replace(temp_output, output)

        print(
            json.dumps(
                {
                    "output": str(output),
                    "parts": len(inputs),
                    "duration_seconds": round(actual_duration, 2),
                    "sample_rate": final_info["sample_rate"],
                    "channels": final_info["channels"],
                    "size_bytes": output.stat().st_size,
                    "decode_check": "passed",
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
