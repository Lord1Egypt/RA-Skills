#!/usr/bin/env python3
"""Parse, download, and read SmartBI conversation artifacts.

The module is intentionally independent from the conversation runner so it can
also be used with an already captured ``stream.ndjson`` file.  It never treats
an SSE ``file.uri`` as a local file until the file has been downloaded and
verified.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator


class ArtifactError(RuntimeError):
    """Raised when an artifact cannot be parsed, downloaded, or read."""


@dataclass(frozen=True)
class ArtifactFile:
    """A file advertised by an ``artifact-update`` SSE event."""

    uri: str
    name: str | None = None
    artifact_id: str | None = None
    task_id: str | None = None

    @property
    def source_path(self) -> str:
        """Return the server-side path used by the download operation."""

        return self.uri


def _json_event(value: str) -> dict[str, Any] | None:
    """Decode one SSE data payload, ignoring keep-alives and non-JSON data."""

    value = value.strip()
    if not value or value == "[DONE]":
        return None
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def iter_sse_events(source: Iterable[str]) -> Iterator[dict[str, Any]]:
    """Yield JSON event objects from SSE or CLI ``--stream`` output.

    The CLI normally writes one ``data:...`` record per line, while a generic
    SSE client may write a multi-line event block.  Both forms are supported.
    Comment lines and non-data fields are ignored.
    """

    data_lines: list[str] = []

    def flush() -> Iterator[dict[str, Any]]:
        if not data_lines:
            return
        payload = _json_event("\n".join(data_lines))
        data_lines.clear()
        if payload is not None:
            yield payload

    def decoded_lines() -> Iterator[str]:
        # CLI envelopes carry transport chunks, not necessarily complete events.
        pending = ""
        for raw in source:
            wrapper = _json_event(raw) if raw.lstrip().startswith("{") else None
            chunk = wrapper.get("event") if wrapper else None
            if isinstance(chunk, str):
                pending += chunk
                while "\n" in pending:
                    line, pending = pending.split("\n", 1)
                    yield line + "\n"
            elif wrapper is None:
                yield raw
        if pending:
            yield pending

    for raw_line in decoded_lines():
        line = raw_line.rstrip("\r\n")
        # ``smartbi call --stream`` wraps each SSE block in a JSON envelope:
        # {"schemaVersion":"smartbi.cli.call.stream.v1", "event":"data:..."}.
        # Unwrap it before feeding the inner event back through the SSE parser.
        if line and not line.startswith((":", "data:")):
            wrapper = _json_event(line)
            wrapped_event = wrapper.get("event") if wrapper else None
            if isinstance(wrapped_event, str):
                yield from iter_sse_events(wrapped_event.splitlines(keepends=True))
            continue
        if line == "":
            yield from flush()
            continue
        if line.startswith(":"):
            continue
        if line.startswith("data:"):
            data_lines.append(line[5:].lstrip())

    yield from flush()


def iter_stream_events(stream_path: str | os.PathLike[str]) -> Iterator[dict[str, Any]]:
    """Open a captured UTF-8 SSE/NDJSON stream and yield decoded events."""

    path = Path(stream_path)
    if not path.is_file():
        raise ArtifactError(f"stream file does not exist: {path}")
    with path.open("r", encoding="utf-8") as stream:
        yield from iter_sse_events(stream)


def iter_artifacts(events: Iterable[dict[str, Any]]) -> Iterator[ArtifactFile]:
    """Extract unique file parts from ``artifact-update`` events."""

    seen: set[tuple[str, str | None]] = set()
    for event in events:
        result = event.get("result")
        if not isinstance(result, dict) or result.get("kind") != "artifact-update":
            continue
        artifact = result.get("artifact")
        if not isinstance(artifact, dict):
            continue
        artifact_id = artifact.get("artifactId")
        task_id = result.get("taskId")
        parts = artifact.get("parts")
        if not isinstance(parts, list):
            continue
        for part in parts:
            if not isinstance(part, dict) or part.get("kind") != "file":
                continue
            file_info = part.get("file")
            if not isinstance(file_info, dict):
                continue
            uri = file_info.get("uri")
            if not isinstance(uri, str) or not uri.strip():
                continue
            name = file_info.get("name")
            name = name if isinstance(name, str) and name else None
            key = (uri, name)
            if key in seen:
                continue
            seen.add(key)
            yield ArtifactFile(uri=uri, name=name, artifact_id=artifact_id, task_id=task_id)


def find_artifacts(stream_path: str | os.PathLike[str]) -> list[ArtifactFile]:
    """Return all unique file artifacts in a captured stream."""

    return list(iter_artifacts(iter_stream_events(stream_path)))


def _safe_output_path(output_dir: Path, artifact: ArtifactFile, index: int) -> Path:
    """Build a non-traversing destination path from a server artifact name."""

    candidate = Path(artifact.name or Path(artifact.uri).name or f"artifact-{index}").name
    if candidate in {"", ".", ".."}:
        candidate = f"artifact-{index}"
    return output_dir / candidate


def download_artifact(
    profile: str,
    artifact: ArtifactFile,
    output_path: str | os.PathLike[str],
    *,
    operation: str = "aichat.downloadQueryResult",
    request_field: str = "filePath",
    smartbi_command: str = "smartbi.cmd" if os.name == "nt" else "smartbi",
    overwrite: bool = False,
) -> Path:
    """Download one server artifact through the SmartBI CLI.

    ``operation`` defaults to the current conversation-result download API.
    Callers handling a server exposing a different binary endpoint can provide
    another operation key without changing artifact parsing.
    """

    destination = Path(output_path)
    if destination.exists() and not overwrite:
        raise ArtifactError(f"refusing to overwrite existing file: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)

    # The CLI accepts @file request bodies.  A temporary file avoids shell
    # quoting issues and keeps the artifact URI out of command-line history.
    with tempfile.TemporaryDirectory(prefix="smartbi-artifact-") as temp_name:
        request_path = Path(temp_name) / "download.json"
        request_path.write_text(
            json.dumps({request_field: artifact.source_path}, ensure_ascii=False),
            encoding="utf-8",
        )
        command = [
            smartbi_command,
            "call",
            operation,
            "--profile",
            profile,
            "-d",
            f"@{request_path}",
            "-o",
            str(destination),
            "--agent",
        ]
        result = subprocess.run(command, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ArtifactError(f"download failed for {artifact.uri}: {detail}")
    if not destination.is_file():
        raise ArtifactError(f"download reported success but file is missing: {destination}")
    if destination.stat().st_size <= 0:
        raise ArtifactError(f"downloaded file is empty: {destination}")
    return destination


def download_artifacts(
    profile: str,
    artifacts: Iterable[ArtifactFile],
    output_dir: str | os.PathLike[str],
    *,
    operation: str = "aichat.downloadQueryResult",
    request_field: str = "filePath",
    smartbi_command: str = "smartbi.cmd" if os.name == "nt" else "smartbi",
    overwrite: bool = False,
) -> list[Path]:
    """Download all artifacts into ``output_dir`` and return local paths."""

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    for index, artifact in enumerate(artifacts, start=1):
        destination = _safe_output_path(directory, artifact, index)
        if destination.exists() and not overwrite:
            suffix = destination.suffix
            destination = destination.with_name(f"{destination.stem}-{index}{suffix}")
        downloaded.append(
            download_artifact(
                profile,
                artifact,
                destination,
                operation=operation,
                request_field=request_field,
                smartbi_command=smartbi_command,
                overwrite=overwrite,
            )
        )
    return downloaded


def detect_artifact_format(path: str | os.PathLike[str]) -> str:
    """Recognize supported binary formats before trusting a filename suffix."""
    file_path = Path(path)
    if not file_path.is_file():
        raise ArtifactError(f"artifact file does not exist: {file_path}")
    with file_path.open("rb") as stream:
        head = stream.read(8)
        if head[:4] == b"PAR1" and file_path.stat().st_size >= 8:
            stream.seek(-4, os.SEEK_END)
            if stream.read(4) == b"PAR1":
                return "parquet"
    if head[:2] == b"PK":
        try:
            with zipfile.ZipFile(file_path) as archive:
                if "xl/workbook.xml" in archive.namelist():
                    return "xlsx"
        except zipfile.BadZipFile as exc:
            raise ArtifactError(f"invalid ZIP artifact: {file_path}") from exc
        raise ArtifactError(f"ZIP artifact is not an Excel workbook: {file_path}")
    if head == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        return "xls"
    # CSV has no magic signature; retain its explicit extension and let the
    # parser validate contents. Do not reinterpret unknown binary files as CSV.
    if file_path.suffix.lower() == ".csv" and b"\x00" not in head:
        return "csv"
    raise ArtifactError(f"unrecognized artifact format: {file_path}")


def read_artifact(path: str | os.PathLike[str], *, sheet_name: str | int | None = 0) -> Any:
    """Read a downloaded tabular artifact with pandas.

    Excel workbooks return one DataFrame by default (the first sheet), or a
    ``dict[str, DataFrame]`` when ``sheet_name=None`` is explicitly requested.
    CSV retains textual values because it has no type schema; Excel preserves
    stored cell types. Neither reader treats literal NA/NULL as missing data.
    Convert measures using model metadata after reading, not inferred dtypes.
    Parquet retains its schema. Imports are lazy so parsing an SSE stream does
    not require pandas.
    """

    file_path = Path(path)
    if not file_path.is_file():
        raise ArtifactError(f"artifact file does not exist: {file_path}")
    detected_format = detect_artifact_format(file_path)
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover - depends on caller env
        raise ArtifactError("pandas is required to read downloaded artifacts") from exc

    try:
        if detected_format in {"xlsx", "xls"}:
            # The default is convenient for a single-sheet result.  Passing
            # None deliberately requests every sheet, matching pandas' API.
            return pd.read_excel(file_path, sheet_name=sheet_name, dtype=object, keep_default_na=False)
        if detected_format == "csv":
            return pd.read_csv(file_path, dtype=str, keep_default_na=False)
        if detected_format == "parquet":
            return pd.read_parquet(file_path)
    except Exception as exc:
        raise ArtifactError(f"failed to read {file_path}: {exc}") from exc
    raise ArtifactError(f"unsupported artifact format: {file_path.suffix or '<none>'}")


def artifact_summary(path: str | os.PathLike[str], *, sheet_name: str | int | None = 0) -> dict[str, Any]:
    """Return safe, JSON-serializable metadata and a small table preview."""

    data = read_artifact(path, sheet_name=sheet_name)
    if isinstance(data, dict):
        sheets = {
            str(name): {"rows": int(frame.shape[0]), "columns": [str(c) for c in frame.columns]}
            for name, frame in data.items()
        }
        return {"path": str(Path(path)), "format": detect_artifact_format(path), "sheets": sheets}
    return {
        "path": str(Path(path)),
        "format": detect_artifact_format(path),
        "rows": int(data.shape[0]),
        "columns": [str(column) for column in data.columns],
        "preview": data.head(5).where(data.notna(), None).to_dict(orient="records"),
    }


def _command_inspect(args: argparse.Namespace) -> int:
    artifacts = find_artifacts(args.stream)
    print(json.dumps([asdict(item) for item in artifacts], ensure_ascii=False, indent=2))
    return 0


def _command_download(args: argparse.Namespace) -> int:
    artifacts = find_artifacts(args.stream)
    if args.index < 1 or args.index > len(artifacts):
        raise ArtifactError(f"artifact index {args.index} is outside 1..{len(artifacts)}")
    path = download_artifact(
        args.profile,
        artifacts[args.index - 1],
        args.output,
        operation=args.operation,
        request_field=args.request_field,
        smartbi_command=args.smartbi,
        overwrite=args.overwrite,
    )
    print(json.dumps({"path": str(path), "bytes": path.stat().st_size}, ensure_ascii=False, indent=2))
    return 0


def _command_read(args: argparse.Namespace) -> int:
    sheet = None if args.all_sheets else (args.sheet if args.sheet is not None else 0)
    print(json.dumps(artifact_summary(args.file, sheet_name=sheet), ensure_ascii=False, indent=2, default=str))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect = subparsers.add_parser("inspect", help="list file artifacts in an SSE/NDJSON stream")
    inspect.add_argument("stream", type=Path)
    inspect.set_defaults(func=_command_inspect)

    download = subparsers.add_parser("download", help="download one file artifact from a stream")
    download.add_argument("stream", type=Path)
    download.add_argument("--profile", required=True)
    download.add_argument("--index", type=int, default=1, help="1-based artifact index")
    download.add_argument("--output", type=Path, required=True)
    download.add_argument("--operation", default="aichat.downloadQueryResult")
    download.add_argument(
        "--request-field",
        default="filePath",
        help="download request field (use s3Uri for the S3 CGI endpoint)",
    )
    download.add_argument("--smartbi", default=("smartbi.cmd" if os.name == "nt" else "smartbi"))
    download.add_argument("--overwrite", action="store_true")
    download.set_defaults(func=_command_download)

    read = subparsers.add_parser("read", help="read a downloaded CSV/Excel/Parquet artifact")
    read.add_argument("file", type=Path)
    read.add_argument("--sheet", help="Excel sheet name or zero-based index")
    read.add_argument("--all-sheets", action="store_true", help="read every Excel sheet")
    read.set_defaults(func=_command_read)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        if getattr(args, "command", None) == "read" and args.sheet is not None:
            try:
                args.sheet = int(args.sheet)
            except ValueError:
                pass
        return int(args.func(args))
    except (ArtifactError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
