from __future__ import annotations

import argparse
from pathlib import Path

from lxml import etree

from ._shared import (
    XML_FILES_TO_PRETTY_PRINT,
    iter_word_xml_files,
    qn,
    read_xml,
    unzip_docx,
    write_xml,
)

TEXT_TAGS = {
    qn("w", "t"),
    qn("w", "instrText"),
    qn("w", "delText"),
    qn("w", "delInstrText"),
}


def _is_mergeable_run(run) -> bool:
    return all(child.tag == qn("w", "rPr") or child.tag in TEXT_TAGS for child in run)


def _same_run_properties(left, right) -> bool:
    left_rpr = left.find(qn("w", "rPr"))
    right_rpr = right.find(qn("w", "rPr"))
    if left_rpr is None and right_rpr is None:
        return True
    if left_rpr is None or right_rpr is None:
        return False
    return etree.tostring(left_rpr) == etree.tostring(right_rpr)


def _merge_runs(root) -> bool:
    changed = False
    for paragraph in root.findall(f".//{qn('w', 'p')}"):
        children = list(paragraph)
        index = 0
        while index < len(children) - 1:
            current = children[index]
            following = children[index + 1]
            if (
                current.tag == qn("w", "r")
                and following.tag == qn("w", "r")
                and _is_mergeable_run(current)
                and _is_mergeable_run(following)
                and _same_run_properties(current, following)
            ):
                insert_after = len(current)
                for child in list(following):
                    if child.tag == qn("w", "rPr"):
                        continue
                    following.remove(child)
                    current.insert(insert_after, child)
                    insert_after += 1
                paragraph.remove(following)
                children.pop(index + 1)
                changed = True
                continue
            index += 1
    return changed


def unpack_docx(input_docx: str | Path, output_dir: str | Path, merge_runs: bool = True) -> Path:
    input_path = Path(input_docx).expanduser().resolve()
    output_path = Path(output_dir).expanduser().resolve()
    unzip_docx(input_path, output_path)

    xml_files = [output_path / "[Content_Types].xml"]
    xml_files.extend(iter_word_xml_files(output_path))

    for xml_path in xml_files:
        if not xml_path.exists():
            continue
        root = read_xml(xml_path)
        relative_name = xml_path.relative_to(output_path).as_posix()
        if merge_runs and relative_name.startswith("word/") and relative_name.endswith(".xml"):
            _merge_runs(root)
        pretty = (
            relative_name in XML_FILES_TO_PRETTY_PRINT
            or relative_name.startswith("word/header")
            or relative_name.startswith("word/footer")
        )
        write_xml(xml_path, root, pretty=pretty)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Unpack a DOCX file into XML parts.")
    parser.add_argument("input_docx")
    parser.add_argument("output_dir")
    parser.add_argument("--merge-runs", choices=["true", "false"], default="true")
    args = parser.parse_args()

    unpacked = unpack_docx(args.input_docx, args.output_dir, merge_runs=args.merge_runs == "true")
    print(unpacked)


if __name__ == "__main__":
    main()
