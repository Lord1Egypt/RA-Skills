#!/usr/bin/env python3
"""
Validate a rebuilt website for common routing, embed, and SEO mistakes.

Usage:
  python3 validate_links.py <site_dir> <original_domain>
  python3 validate_links.py <site_dir> <original_domain> --fix
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


ALWAYS_EXTERNAL_OK = [
    "shop.",
    "cdn.prod.",
    "fonts.googleapis",
    "fonts.gstatic",
    "google.com/maps",
    "maps.googleapis",
    "/templates/licensing",
]

BOOKING_DIR_NAMES = {"book", "booking", "appointments"}

HEAD_REQUIRED = [
    (r"<title>[^<]{4,}</title>", "Missing or empty <title>"),
    (r'<meta\s+name="description"\s+content="[^"]{20,}"', "Missing or short <meta description>"),
    (r'<link\s+rel="canonical"\s+href="[^"]{10,}"', "Missing canonical link"),
]


@dataclass
class Violation:
    gate: str
    severity: str
    file: str
    detail: str
    snippet: str = ""


@dataclass
class ValidationResult:
    violations: list[Violation] = field(default_factory=list)
    warnings: list[Violation] = field(default_factory=list)
    files_scanned: int = 0
    files_fixed: int = 0


def split_head_body(content: str) -> tuple[str, str]:
    marker = content.lower().find("</head>")
    if marker == -1:
        return "", content
    return content[: marker + len("</head>")], content[marker + len("</head>") :]


def html_files(site_dir: Path) -> list[Path]:
    return [path for path in site_dir.rglob("*.html") if not path.name.startswith("_")]


def is_allowed_external(url: str) -> bool:
    return any(token in url for token in ALWAYS_EXTERNAL_OK)


def has_blank_target(tag: str) -> bool:
    return 'target="_blank"' in tag or "target='_blank'" in tag


def page_stems(site_dir: Path) -> set[str]:
    return {path.stem for path in html_files(site_dir)}


def gate_nav_leaks(body: str, rel: str, domain: str) -> list[Violation]:
    pattern = re.compile(
        rf'<a\b([^>]*)href="(https?://(?:www\.)?{re.escape(domain)}[^"]*)"([^>]*)>',
        re.I,
    )
    found: list[Violation] = []
    for match in pattern.finditer(body):
        tag = match.group(0)
        url = match.group(2)
        if is_allowed_external(url) or has_blank_target(tag):
            continue
        found.append(
            Violation(
                gate="G1:NavLeak",
                severity="ERROR",
                file=rel,
                detail=f"Original-domain link without target=_blank: {url}",
                snippet=tag[:120],
            )
        )
    return found


def gate_mailto(body: str, rel: str) -> list[Violation]:
    found: list[Violation] = []
    for match in re.finditer(r'<a\b([^>]*)href="(mailto:[^"]*)"([^>]*)>', body, re.I):
        tag = match.group(0)
        if has_blank_target(tag):
            continue
        found.append(
            Violation(
                gate="G2:Mailto",
                severity="ERROR",
                file=rel,
                detail=f"mailto link without target=_blank: {match.group(2)}",
                snippet=tag[:120],
            )
        )
    return found


def gate_booking_iframe(content: str, rel: str, path: Path) -> list[Violation]:
    if path.parent.name.lower() not in BOOKING_DIR_NAMES:
        return []
    if "<iframe" in content.lower():
        return []
    return [
        Violation(
            gate="G3:BookingNoIframe",
            severity="ERROR",
            file=rel,
            detail="Booking wrapper page is missing an iframe embed.",
        )
    ]


def gate_relative_links(body: str, rel: str, domain: str, site_dir: Path) -> list[Violation]:
    stems = page_stems(site_dir)
    pattern = re.compile(rf'href="https?://(?:www\.)?{re.escape(domain)}/([^"#?]*)"', re.I)
    found: list[Violation] = []
    for match in pattern.finditer(body):
        slug = match.group(1).rstrip("/")
        candidate = slug.split("/")[-1] if slug else "index"
        if candidate in stems:
            found.append(
                Violation(
                    gate="G4:ShouldBeRelative",
                    severity="ERROR",
                    file=rel,
                    detail=f"Recreated page '/{slug}' still links to the original domain.",
                    snippet=match.group(0),
                )
            )
    return found


def gate_dead_hash(body: str, rel: str) -> list[Violation]:
    if 'href="#"' not in body.lower():
        return []
    return [
        Violation(
            gate="G5:DeadLink",
            severity="WARNING",
            file=rel,
            detail='Placeholder link `href="#"` still exists.',
        )
        for _ in re.finditer(r'href="#"', body, re.I)
    ]


def gate_seo_head(head: str, rel: str) -> list[Violation]:
    found: list[Violation] = []
    for pattern, detail in HEAD_REQUIRED:
        if not re.search(pattern, head, re.I):
            found.append(
                Violation(
                    gate="G6:SEOMissing",
                    severity="ERROR",
                    file=rel,
                    detail=detail,
                )
            )
    return found


def autofix(content: str, domain: str) -> tuple[str, int]:
    fixes = 0
    head, body = split_head_body(content)

    nav_pattern = re.compile(
        rf'(<a\b(?![^>]*target=)[^>]*href=")(https?://(?:www\.)?{re.escape(domain)}(?!/templates/licensing)[^"]*)"([^>]*>)',
        re.I,
    )
    mailto_pattern = re.compile(r'(<a\b(?![^>]*target=)[^>]*href="mailto:[^"]*"[^>]*>)', re.I)

    def fix_nav(match: re.Match[str]) -> str:
        nonlocal fixes
        if is_allowed_external(match.group(2)):
            return match.group(0)
        fixes += 1
        return match.group(0)[:-1] + ' target="_blank" rel="noopener">'

    def fix_mailto(match: re.Match[str]) -> str:
        nonlocal fixes
        fixes += 1
        return match.group(1)[:-1] + ' target="_blank" rel="noopener">'

    body = nav_pattern.sub(fix_nav, body)
    body = mailto_pattern.sub(fix_mailto, body)
    return head + body, fixes


def run(site_dir: Path, domain: str, fix_mode: bool) -> ValidationResult:
    result = ValidationResult(files_scanned=len(html_files(site_dir)))
    for path in sorted(html_files(site_dir)):
        rel = str(path.relative_to(site_dir))
        content = path.read_text(encoding="utf-8", errors="replace")
        head, body = split_head_body(content)
        checks: list[Violation] = []
        checks.extend(gate_nav_leaks(body, rel, domain))
        checks.extend(gate_mailto(body, rel))
        checks.extend(gate_booking_iframe(content, rel, path))
        checks.extend(gate_relative_links(body, rel, domain, site_dir))
        checks.extend(gate_dead_hash(body, rel))
        checks.extend(gate_seo_head(head, rel))

        for item in checks:
            if item.severity == "ERROR":
                result.violations.append(item)
            else:
                result.warnings.append(item)

        if fix_mode and any(v.gate in {"G1:NavLeak", "G2:Mailto"} for v in checks):
            updated, count = autofix(content, domain)
            if count:
                path.write_text(updated, encoding="utf-8")
                result.files_fixed += 1
    return result


def print_section(title: str, items: Iterable[Violation], limit: int) -> None:
    items = list(items)
    if not items:
        return
    print(f"\n{title} ({len(items)}):")
    for item in items[:limit]:
        print(f"- [{item.gate}] {item.file}: {item.detail}")
        if item.snippet:
            print(f"  {item.snippet}")
    if len(items) > limit:
        print(f"- ... and {len(items) - limit} more")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a rebuilt website.")
    parser.add_argument("site_dir", help="Path to the output site directory")
    parser.add_argument("domain", help="Original domain, for example example.com")
    parser.add_argument("--fix", action="store_true", help="Auto-fix G1 and G2 issues")
    args = parser.parse_args()

    site_dir = Path(args.site_dir).resolve()
    if not site_dir.exists():
        print(f"ERROR: {site_dir} does not exist.")
        return 2

    result = run(site_dir, args.domain, args.fix)
    print(f"Files scanned: {result.files_scanned}")
    if args.fix:
        print(f"Files auto-fixed: {result.files_fixed}")
    print_section("Errors", result.violations, 40)
    print_section("Warnings", result.warnings, 20)

    if result.violations:
        print("\nFAIL")
        return 1

    print("\nPASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
