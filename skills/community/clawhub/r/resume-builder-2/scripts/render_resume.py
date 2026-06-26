#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL_KEYS = ("name", "summary", "skills", "experience", "education")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a premium resume to Typst and PDF."
    )
    parser.add_argument("--input", required=True, help="Path to input JSON resume data")
    parser.add_argument(
        "--output-dir", required=True, help="Directory where resume.typ and resume.pdf are written"
    )
    return parser.parse_args()


def ensure_list(value, field_name):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    raise ValueError(f"{field_name} must be a list")


def normalize_entry(entry, required=None):
    if not isinstance(entry, dict):
        raise ValueError("section entries must be objects")
    required = required or ()
    for key in required:
        if not entry.get(key):
            raise ValueError(f"missing required field '{key}' in section entry")
    return entry


def normalize_resume(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("input resume must be a JSON object")

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in data or data[key] in ("", None, []):
            raise ValueError(f"missing required top-level field '{key}'")

    normalized = {
        "name": data["name"],
        "title": data.get("title", ""),
        "location": data.get("location", ""),
        "phone": data.get("phone", ""),
        "email": data.get("email", ""),
        "website": data.get("website", ""),
        "linkedin": data.get("linkedin", ""),
        "summary": ensure_list(data.get("summary"), "summary"),
        "skills": ensure_list(data.get("skills"), "skills"),
        "experience": [
            normalize_entry(item, required=("company", "title", "bullets"))
            for item in ensure_list(data.get("experience"), "experience")
        ],
        "projects": [
            normalize_entry(item, required=("name", "bullets"))
            for item in ensure_list(data.get("projects"), "projects")
        ],
        "education": [
            normalize_entry(item, required=("school",))
            for item in ensure_list(data.get("education"), "education")
        ],
        "certifications": ensure_list(data.get("certifications"), "certifications"),
        "languages": ensure_list(data.get("languages"), "languages"),
    }

    if not normalized["summary"]:
        raise ValueError("summary must contain at least one bullet")
    if not normalized["skills"]:
        raise ValueError("skills must contain at least one item")
    if not normalized["experience"]:
        raise ValueError("experience must contain at least one entry")
    if not normalized["education"]:
        raise ValueError("education must contain at least one entry")

    for entry in normalized["experience"]:
        entry["bullets"] = ensure_list(entry.get("bullets"), "experience.bullets")
        if not entry["bullets"]:
            raise ValueError("each experience entry must contain at least one bullet")

    for entry in normalized["projects"]:
        entry["bullets"] = ensure_list(entry.get("bullets"), "projects.bullets")
        if not entry["bullets"]:
            raise ValueError("each project entry must contain at least one bullet")

    return normalized


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    template_path = skill_root / "assets" / "resume.typ"

    if shutil.which("typst") is None:
        print("error: 'typst' is required but not installed", file=sys.stderr)
        return 1

    with input_path.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)
    data = normalize_resume(raw)

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "resume.json"
    typ_path = output_dir / "resume.typ"
    pdf_path = output_dir / "resume.pdf"

    with json_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    shutil.copyfile(template_path, typ_path)

    cmd = ["typst", "compile", str(typ_path), str(pdf_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        if pdf_path.exists():
            pdf_path.unlink()
        sys.stderr.write(result.stderr)
        return result.returncode

    print(f"Generated Typst source: {typ_path}")
    print(f"Generated PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
