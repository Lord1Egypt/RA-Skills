from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path

from office._shared import XML_FILES_TO_PRETTY_PRINT, qn, read_xml, write_xml
from office.pack import pack_docx
from office.unpack import unpack_docx
from office.validate import validate_docx

TEXT_TAGS = {
    qn("w", "t"),
    qn("w", "instrText"),
    qn("w", "delText"),
    qn("w", "delInstrText"),
}
DEFAULT_PART_PATTERNS = [
    "word/document.xml",
    "word/header*.xml",
    "word/footer*.xml",
]


def _normalize_replacements(replacements: list[dict]) -> list[dict]:
    normalized = []
    for item in replacements:
        if not isinstance(item, dict):
            raise TypeError("replacements 中的每一项都必须是字典。")
        old = item.get("from")
        new = item.get("to")
        if not isinstance(old, str) or not isinstance(new, str):
            raise TypeError("replacements 中的 from/to 必须是字符串。")
        if not old:
            raise ValueError("replacements 中的 from 不能为空字符串。")
        normalized.append({"from": old, "to": new})
    if not normalized:
        raise ValueError("replacements 不能为空。")
    return normalized


def _expand_parts(unpacked_dir: Path, parts: list[str] | None) -> list[Path]:
    patterns = parts or DEFAULT_PART_PATTERNS
    resolved: list[Path] = []
    seen: set[Path] = set()

    for pattern in patterns:
        matched = False
        for candidate in sorted(unpacked_dir.glob(pattern)):
            if candidate.is_file() and candidate not in seen:
                resolved.append(candidate)
                seen.add(candidate)
                matched = True
        if not matched and not any(ch in pattern for ch in "*?[]"):
            candidate = unpacked_dir / pattern
            if candidate.is_file() and candidate not in seen:
                resolved.append(candidate)
                seen.add(candidate)

    return resolved


def _apply_single_replacement(text: str, replacement: dict, match_mode: str, ignore_case: bool) -> tuple[str, int]:
    old = replacement["from"]
    new = replacement["to"]

    if match_mode == "literal":
        flags = re.IGNORECASE if ignore_case else 0
        return re.subn(re.escape(old), new, text, flags=flags)
    if match_mode == "regex":
        flags = re.IGNORECASE if ignore_case else 0
        return re.subn(old, new, text, flags=flags)
    raise ValueError(f"不支持的 match_mode: {match_mode}")


def _replace_in_part(xml_path: Path, base_dir: Path, replacements: list[dict], match_mode: str, ignore_case: bool) -> tuple[bool, list[dict]]:
    root = read_xml(xml_path)
    stats = [{"from": item["from"], "to": item["to"], "count": 0} for item in replacements]
    changed = False

    for node in root.iter():
        if node.tag not in TEXT_TAGS:
            continue
        original = node.text or ""
        if not original:
            continue

        updated = original
        node_changed = False
        for idx, item in enumerate(replacements):
            updated, count = _apply_single_replacement(updated, item, match_mode, ignore_case)
            stats[idx]["count"] += count
            node_changed = node_changed or count > 0

        if node_changed:
            node.text = updated
            changed = True

    if changed:
        relative_name = xml_path.relative_to(base_dir).as_posix()
        pretty = (
            relative_name in XML_FILES_TO_PRETTY_PRINT
            or relative_name.startswith("word/header")
            or relative_name.startswith("word/footer")
        )
        write_xml(xml_path, root, pretty=pretty)

    return changed, stats


def edit_docx(
    input_docx: str,
    output_docx: str,
    replacements: list[dict],
    parts: list[str] | None = None,
    match_mode: str = "literal",
    ignore_case: bool = False,
) -> dict:
    source = Path(input_docx).expanduser().resolve()
    target = Path(output_docx).expanduser().resolve()
    normalized = _normalize_replacements(replacements)

    if not source.exists():
        raise FileNotFoundError(f"文件不存在: {source}")

    with tempfile.TemporaryDirectory(prefix="edit_docx_") as tmp_dir:
        unpacked_dir = Path(tmp_dir) / "unpacked"
        unpack_docx(source, unpacked_dir, merge_runs=True)

        part_paths = _expand_parts(unpacked_dir, parts)
        if not part_paths:
            raise FileNotFoundError("未找到可编辑的 XML 部件。")

        aggregate = [{"from": item["from"], "to": item["to"], "count": 0} for item in normalized]
        modified_files: list[str] = []

        for xml_path in part_paths:
            changed, stats = _replace_in_part(
                xml_path=xml_path,
                base_dir=unpacked_dir,
                replacements=normalized,
                match_mode=match_mode,
                ignore_case=ignore_case,
            )
            for idx, stat in enumerate(stats):
                aggregate[idx]["count"] += stat["count"]
            if changed:
                modified_files.append(xml_path.relative_to(unpacked_dir).as_posix())

        pack_docx(unpacked_dir, target, validate=True)
        validation = validate_docx(target)

    return {
        "ok": validation["ok"],
        "input_path": str(source),
        "output_path": str(target),
        "match_mode": match_mode,
        "ignore_case": ignore_case,
        "files_modified": modified_files,
        "replacements_applied": aggregate,
        "validation": validation,
    }


def _load_replacements(raw: str) -> list[dict]:
    if raw.startswith("@"):
        return json.loads(Path(raw[1:]).read_text(encoding="utf-8"))
    return json.loads(raw)


def main() -> None:
    parser = argparse.ArgumentParser(description="Edit a DOCX file through unpack/replace/pack/validate.")
    parser.add_argument("input_docx")
    parser.add_argument("output_docx")
    parser.add_argument("--replacements", required=True, help="JSON 字符串，或以 @ 开头的 JSON 文件路径。")
    parser.add_argument("--parts", nargs="*")
    parser.add_argument("--match-mode", choices=["literal", "regex"], default="literal")
    parser.add_argument("--ignore-case", action="store_true")
    args = parser.parse_args()

    result = edit_docx(
        input_docx=args.input_docx,
        output_docx=args.output_docx,
        replacements=_load_replacements(args.replacements),
        parts=args.parts,
        match_mode=args.match_mode,
        ignore_case=args.ignore_case,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
