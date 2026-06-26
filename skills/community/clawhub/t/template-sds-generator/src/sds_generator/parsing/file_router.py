from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sds_generator.config_loader import load_defaults
from sds_generator.exceptions import InvalidInputCountError, UnsupportedFileTypeError
from sds_generator.models.source import ParsedSourceDocument

from .docx_parser import parse_docx
from .pdf_parser import parse_pdf
from .txt_parser import parse_txt


def _validate_input_count(inputs: list[Path]) -> None:
    parsing_defaults = load_defaults().get("parsing", {})
    min_inputs = int(parsing_defaults.get("min_source_inputs", parsing_defaults.get("min_inputs", 1)))
    max_inputs = int(parsing_defaults.get("max_source_inputs", parsing_defaults.get("max_inputs", 3)))
    if not (min_inputs <= len(inputs) <= max_inputs):
        raise InvalidInputCountError(f"Expected {min_inputs}-{max_inputs} source inputs, got {len(inputs)}.")


def parse_inputs(
    inputs: Iterable[str | Path],
    *,
    enable_ocr: bool = False,
    logger=None,
) -> list[ParsedSourceDocument]:
    paths = [Path(item) for item in inputs]
    _validate_input_count(paths)

    documents: list[ParsedSourceDocument] = []
    for path in paths:
        suffix = path.suffix.lower()
        if logger is not None:
            logger.info("Parsing %s", path.name)

        if suffix == ".pdf":
            documents.append(parse_pdf(path, enable_ocr=enable_ocr))
        elif suffix == ".docx":
            documents.append(parse_docx(path))
        elif suffix == ".txt":
            documents.append(parse_txt(path))
        else:
            raise UnsupportedFileTypeError(f"Unsupported input type: {path.name}")

    return documents
