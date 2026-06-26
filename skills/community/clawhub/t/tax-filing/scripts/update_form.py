#!/usr/bin/env python3
"""
Safe PDF form field updater for IRS fillable forms.

Encodes the three critical pypdf rules:
  1. Never write output to the same path as input (causes field tree corruption
     because PdfReader uses lazy reading — writing truncates the file while the
     reader still has references into it).
  2. Always use auto_regenerate=False (the default True removes /AP appearance
     streams, making some PDF viewers show blank fields even though /V has a value).
  3. Iterate all pages (some IRS forms silently split fields across pages).

Usage:
    python scripts/update_form.py INPUT_PDF OUTPUT_PDF [--set FIELD=VALUE ...] [--clear FIELD ...]

Examples:
    # Fix a single field
    python scripts/update_form.py Form1040NR.pdf /tmp/Form1040NR_fixed.pdf --set "f1_53=5000"

    # Fix multiple fields and clear one
    python scripts/update_form.py Form8843.pdf /tmp/Form8843_fixed.pdf \
        --set "f1_14=338" "f1_17=338" --clear "f1_15"

    # Can also be imported and used as a library
    from scripts.update_form import update_form
    update_form("in.pdf", "/tmp/out.pdf", {"f1_53": "5000"}, clear_fields=["f1_65"])
"""

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("ERROR: pypdf is not installed. Run: pip install pypdf --break-system-packages")
    sys.exit(1)


def update_form(input_path: str, output_path: str, field_updates: dict, clear_fields: list = None):
    """
    Update PDF form fields safely.

    Args:
        input_path:     Path to the source PDF (will not be modified).
        output_path:    Path to write the updated PDF. MUST differ from input_path.
        field_updates:  Dict of {field_name: new_value} to set.
        clear_fields:   Optional list of field names to blank out.

    Raises:
        AssertionError: If output_path == input_path.
        FileNotFoundError: If input_path doesn't exist.
    """
    input_path = str(Path(input_path).resolve())
    output_path = str(Path(output_path).resolve())
    assert input_path != output_path, (
        f"output_path must differ from input_path to prevent corruption. "
        f"Got: {input_path}"
    )

    reader = PdfReader(input_path)
    writer = PdfWriter()
    writer.append(reader)

    # Apply updates across all pages (rule #3: fields can span pages silently)
    for page_idx in range(len(writer.pages)):
        writer.update_page_form_field_values(
            writer.pages[page_idx],
            field_updates,
            auto_regenerate=False  # rule #2: preserve appearance streams
        )

    # Clear specified fields
    if clear_fields:
        clear_dict = {f: "" for f in clear_fields}
        for page_idx in range(len(writer.pages)):
            writer.update_page_form_field_values(
                writer.pages[page_idx],
                clear_dict,
                auto_regenerate=False
            )

    with open(output_path, "wb") as f:
        writer.write(f)

    # Verify the output is readable and fields survived
    verify_reader = PdfReader(output_path)
    fields = verify_reader.get_form_text_fields()
    if not fields:
        print("WARNING: Output PDF has no text fields. Possible corruption — check references/pypdf-recovery.md")
    else:
        print(f"OK: {len(fields)} text fields in output.")
        for name, value in field_updates.items():
            # Match by short name (last segment without [0])
            matched = [v for k, v in fields.items() if name in k]
            if matched and str(matched[0]) == str(value):
                print(f"  Verified: {name} = {value}")
            elif matched:
                print(f"  WARNING: {name} expected '{value}' but got '{matched[0]}'")
            else:
                print(f"  WARNING: {name} not found in output fields")


def main():
    parser = argparse.ArgumentParser(description="Safely update IRS PDF form fields")
    parser.add_argument("input_pdf", help="Path to the source PDF")
    parser.add_argument("output_pdf", help="Path to write the updated PDF (must differ from input)")
    parser.add_argument("--set", nargs="+", metavar="FIELD=VALUE",
                        help="Fields to set, as FIELD=VALUE pairs")
    parser.add_argument("--clear", nargs="+", metavar="FIELD",
                        help="Fields to blank out")
    args = parser.parse_args()

    field_updates = {}
    if args.set:
        for pair in args.set:
            if "=" not in pair:
                print(f"ERROR: --set argument '{pair}' must be FIELD=VALUE format")
                sys.exit(1)
            key, value = pair.split("=", 1)
            field_updates[key] = value

    if not field_updates and not args.clear:
        print("Nothing to do. Provide --set and/or --clear arguments.")
        sys.exit(0)

    update_form(args.input_pdf, args.output_pdf, field_updates, args.clear)


if __name__ == "__main__":
    main()
