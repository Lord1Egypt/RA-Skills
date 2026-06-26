from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from ._shared import iter_word_xml_files, qn, read_xml, write_xml, zip_dir
from .validate import validate_docx

XML_SPACE = qn("xml", "space")
TEXT_TAGS = {
    qn("w", "t"),
    qn("w", "instrText"),
    qn("w", "delText"),
    qn("w", "delInstrText"),
}
MAX_DURABLE_ID = 0x7FFFFFFE


def _repair_text_nodes(root) -> bool:
    changed = False
    for node in root.iter():
        if node.tag not in TEXT_TAGS:
            continue
        text = node.text or ""
        if text[:1].isspace() or text[-1:].isspace():
            if node.get(XML_SPACE) != "preserve":
                node.set(XML_SPACE, "preserve")
                changed = True
        elif node.get(XML_SPACE) == "preserve":
            node.attrib.pop(XML_SPACE, None)
            changed = True
    return changed


def _repair_durable_ids(root) -> bool:
    changed = False
    for node in root.iter():
        for attr_name in list(node.attrib.keys()):
            if attr_name.split("}", 1)[-1] != "durableId":
                continue
            value = node.attrib.get(attr_name, "")
            base = 16 if value.lower().startswith("0x") else 10
            try:
                numeric = int(value, base)
            except ValueError:
                numeric = MAX_DURABLE_ID + 1
            if numeric > MAX_DURABLE_ID:
                node.attrib[attr_name] = str(random.randint(1, MAX_DURABLE_ID))
                changed = True
    return changed


def _repair_unpack_dir(unpacked_dir: Path) -> None:
    xml_files = [unpacked_dir / "[Content_Types].xml"]
    xml_files.extend(iter_word_xml_files(unpacked_dir))

    for xml_path in xml_files:
        if not xml_path.exists():
            continue
        root = read_xml(xml_path)
        changed = _repair_text_nodes(root)
        changed = _repair_durable_ids(root) or changed
        if changed:
            write_xml(xml_path, root, pretty=False)


def pack_docx(
    input_dir: str | Path,
    output_docx: str | Path,
    original: str | Path | None = None,
    validate: bool = True,
) -> Path:
    unpacked_dir = Path(input_dir).expanduser().resolve()
    output_path = Path(output_docx).expanduser().resolve()
    if not unpacked_dir.exists():
        raise FileNotFoundError(f"目录不存在: {unpacked_dir}")

    _repair_unpack_dir(unpacked_dir)
    zip_dir(unpacked_dir, output_path)

    if validate:
        result = validate_docx(output_path)
        if not result["ok"]:
            errors = "\n".join(result["errors"])
            raise ValueError(f"DOCX 验证失败:\n{errors}")

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Pack an unpacked DOCX directory.")
    parser.add_argument("input_dir")
    parser.add_argument("output_docx")
    parser.add_argument("--original")
    parser.add_argument("--validate", choices=["true", "false"], default="true")
    args = parser.parse_args()

    output = pack_docx(
        args.input_dir,
        args.output_docx,
        original=args.original,
        validate=args.validate == "true",
    )
    result = validate_docx(output) if args.validate == "true" else {"ok": True, "path": str(output)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
