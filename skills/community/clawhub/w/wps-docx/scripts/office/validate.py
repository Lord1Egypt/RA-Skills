from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from docx import Document
from lxml import etree

REQUIRED_PARTS = {
    "[Content_Types].xml",
    "_rels/.rels",
    "word/document.xml",
}


def validate_docx(path: str | Path) -> dict:
    docx_path = Path(path).expanduser().resolve()
    result = {
        "ok": True,
        "path": str(docx_path),
        "parts": 0,
        "errors": [],
        "warnings": [],
    }

    if not docx_path.exists():
        result["ok"] = False
        result["errors"].append(f"文件不存在: {docx_path}")
        return result

    try:
        with zipfile.ZipFile(docx_path, "r") as archive:
            names = set(archive.namelist())
            result["parts"] = len(names)
            missing = sorted(REQUIRED_PARTS - names)
            if missing:
                result["ok"] = False
                result["errors"].append(f"缺少必要部件: {', '.join(missing)}")

            for name in sorted(n for n in names if n.endswith(".xml")):
                try:
                    etree.fromstring(archive.read(name))
                except etree.XMLSyntaxError as exc:
                    result["ok"] = False
                    result["errors"].append(f"XML 解析失败 {name}: {exc}")

        if result["ok"]:
            Document(str(docx_path))
    except zipfile.BadZipFile as exc:
        result["ok"] = False
        result["errors"].append(f"不是有效的 DOCX/ZIP 文件: {exc}")
    except Exception as exc:
        result["ok"] = False
        result["errors"].append(f"python-docx 打开失败: {exc}")

    if result["ok"]:
        try:
            with zipfile.ZipFile(docx_path, "r") as archive:
                if "word/styles.xml" not in archive.namelist():
                    result["warnings"].append("缺少 word/styles.xml，Word 可能使用默认样式。")
        except Exception:
            pass

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a DOCX file.")
    parser.add_argument("path")
    args = parser.parse_args()

    result = validate_docx(args.path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
