#!/usr/bin/env python3
"""
Extract resume content from PDF and structure into JSON format.
Supports extraction of personal info, education, experience, projects, and skills.
"""

import json
import re
import sys
from pathlib import Path

from resume_utils import normalize_resume_data

# Use PyMuPDF (fitz) for PDF text extraction
try:
    import fitz
except ImportError:
    print("Error: PyMuPDF (fitz) not installed. Run: pip install pymupdf")
    sys.exit(1)


def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def split_bullets(text):
    """Split a bullet-like line into cleaned items."""
    text = re.sub(r"^[\-\u2022\u2023\u25E6\u2043\u2219]\s*", "", text).strip()
    if not text:
        return []

    if "  " in text:
        parts = [part.strip() for part in text.split("  ") if part.strip()]
        if len(parts) > 1:
            return parts

    return [text]


def parse_header(lines):
    """Best-effort extraction of personal info from the top of the document."""
    personal = {}
    header_lines = lines[:8]

    if header_lines:
        personal["name"] = header_lines[0]

    for line in header_lines[1:]:
        if "@" in line and "email" not in personal:
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line)
            if email_match:
                personal["email"] = email_match.group()

        if "linkedin.com/" in line.lower() and "linkedin" not in personal:
            url_match = re.search(r'https?://\S+|www\.\S+|linkedin\.com/\S+', line, re.I)
            if url_match:
                personal["linkedin"] = url_match.group().rstrip(".,;)")

        if "github.com/" in line.lower() and "github" not in personal:
            url_match = re.search(r'https?://\S+|www\.\S+|github\.com/\S+', line, re.I)
            if url_match:
                personal["github"] = url_match.group().rstrip(".,;)")

        if "location" not in personal and re.search(r"(china|beijing|shanghai|shenzhen|new york|london|singapore|tokyo|paris|berlin)", line, re.I):
            personal["location"] = line

        if "phone" not in personal:
            phone_match = re.search(r'(\+?\d[\d\s\-\(\)]{6,}\d)', line)
            if phone_match:
                personal["phone"] = phone_match.group().strip()

    return personal


def is_period_like(text):
    """Return True if the string looks like a date range."""
    return bool(re.search(r'((19|20)\d{2}|present|至今|current|now)', text, re.I))


def looks_like_company_or_institution(text):
    """Heuristic for title lines in experience or education sections."""
    keywords = [
        "inc", "corp", "ltd", "llc", "company", "university", "college", "institute",
        "学校", "大学", "学院", "公司", "集团", "laboratory", "lab"
    ]
    lowered = text.lower()
    return any(keyword in lowered for keyword in keywords) or len(text.split()) <= 8


def parse_education_line(line):
    """Best-effort parse of a single education line."""
    entry = {"raw": line}
    parts = [part.strip(" ,|-") for part in re.split(r"\s+[|\u2022\-]\s+|,\s*", line) if part.strip()]
    if parts:
        entry["institution"] = parts[0]
    if len(parts) > 1:
        entry["degree"] = parts[1]
    if len(parts) > 2 and is_period_like(parts[-1]):
        entry["period"] = parts[-1]
    return entry


def parse_experience_header(line):
    """Best-effort parse of an experience header line."""
    entry = {"raw": line}
    if " at " in line.lower():
        left, right = re.split(r"\bat\b", line, maxsplit=1, flags=re.I)
        entry["position"] = left.strip(" ,|-")
        entry["company"] = right.strip(" ,|-")
    else:
        parts = [part.strip(" ,|-") for part in re.split(r"\s+[|\u2022\-]\s+|,\s*", line) if part.strip()]
        if parts:
            entry["company"] = parts[0]
        if len(parts) > 1:
            entry["position"] = parts[1]
        if len(parts) > 2 and is_period_like(parts[-1]):
            entry["period"] = parts[-1]
    return entry


def parse_project_header(line):
    """Best-effort parse of a project header line."""
    entry = {"raw": line}
    parts = [part.strip(" ,|-") for part in re.split(r"\s+[|\u2022\-]\s+|,\s*", line) if part.strip()]
    if parts:
        entry["name"] = parts[0]
    if len(parts) > 1 and not is_period_like(parts[1]):
        entry["role"] = parts[1]
    if parts and is_period_like(parts[-1]):
        entry["period"] = parts[-1]
    return entry


def parse_resume_text(text):
    """
    Parse resume text into structured JSON format.
    This is a basic parser - for production use, consider more sophisticated NLP.
    """
    resume = {
        "personal": {},
        "summary": "",
        "education": [],
        "experience": [],
        "projects": [],
        "skills": {}
    }

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    current_section = None
    current_entry = None

    # Simple section detection
    section_patterns = {
        "summary": ["summary", "个人简介", "简介", "about"],
        "education": ["education", "教育背景", "学历", "academic"],
        "experience": ["experience", "work experience", "工作经历", "工作", "employment"],
        "projects": ["projects", "项目", "project experience"],
        "skills": ["skills", "技能", "技术栈", "technologies"]
    }

    resume["personal"] = parse_header(lines)

    for line in lines:
        # Detect section headers
        line_lower = line.lower()
        new_section = None
        for section, patterns in section_patterns.items():
            if any(pattern in line_lower for pattern in patterns):
                new_section = section
                break

        if new_section:
            current_section = new_section
            current_entry = None
            continue

        # Parse content based on current section
        if current_section == "summary" and not resume["summary"]:
            resume["summary"] = line
        elif current_section == "education":
            if any(char.isdigit() for char in line) and looks_like_company_or_institution(line):
                entry = parse_education_line(line)
                resume["education"].append(entry)
                current_entry = entry
            elif current_entry and not current_entry.get("location"):
                current_entry["location"] = line
        elif current_section == "experience":
            if looks_like_company_or_institution(line) and not line.startswith(("•", "-", "*")):
                entry = parse_experience_header(line)
                resume["experience"].append(entry)
                current_entry = entry
            elif current_entry:
                bullet_items = split_bullets(line)
                if line.startswith(("•", "-", "*")) or len(bullet_items) > 1:
                    current_entry.setdefault("achievements", []).extend(bullet_items)
                elif not current_entry.get("description"):
                    current_entry["description"] = line
                else:
                    current_entry.setdefault("achievements", []).append(line)
        elif current_section == "projects":
            if len(line.split()) > 2 and not line.startswith(("•", "-", "*")):
                entry = parse_project_header(line)
                resume["projects"].append(entry)
                current_entry = entry
            elif current_entry:
                bullet_items = split_bullets(line)
                if line.startswith(("•", "-", "*")) or len(bullet_items) > 1:
                    current_entry.setdefault("achievements", []).extend(bullet_items)
                elif not current_entry.get("description"):
                    current_entry["description"] = line
                else:
                    current_entry.setdefault("achievements", []).append(line)
        elif current_section == "skills":
            if ":" in line:
                category, values = line.split(":", 1)
                resume["skills"][category.strip()] = split_bullets(values)
            else:
                resume["skills"].setdefault("general", [])
                resume["skills"]["general"].extend(split_bullets(line))

    return normalize_resume_data(resume)


def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_from_pdf.py <input.pdf> <output.json>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_json = sys.argv[2]

    if not Path(input_pdf).exists():
        print(f"Error: PDF file not found: {input_pdf}")
        sys.exit(1)

    print(f"Extracting content from: {input_pdf}")

    # Extract text from PDF
    text = extract_text_from_pdf(input_pdf)

    # Parse into structured format
    resume = parse_resume_text(text)

    # Save to JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(resume, f, ensure_ascii=False, indent=2)

    print(f"Resume data extracted and saved to: {output_json}")
    print("\nExtracted structure:")
    print(f"  Personal info: {len(resume['personal'])} fields")
    print(f"  Summary: {len(resume['summary'])} chars")
    print(f"  Education: {len(resume['education'])} entries")
    print(f"  Experience: {len(resume['experience'])} entries")
    print(f"  Projects: {len(resume['projects'])} entries")
    print(f"  Skills: {len(resume['skills'])} categories")


if __name__ == "__main__":
    main()
