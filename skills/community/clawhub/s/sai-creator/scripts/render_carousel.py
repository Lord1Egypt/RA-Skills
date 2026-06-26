#!/usr/bin/env python3
"""
Render Carousel — substitute brief data ke template SVG carousel.

Usage:
    render_carousel.py --brief brief.json --candidate candidate.json \
                       --dimension 1080x1080 --output out/carousel.svg
    render_carousel.py --brief brief.json --candidate candidate.json \
                       --dimension 1200x675 --output-dir out/

Input:
    brief.json    — brief_for_next from SENKU (parsed dari plain text ke JSON)
    candidate.json — original candidate JSON dari CONAN

Output:
    SVG file(s) — combined (single file with all 7 slides) atau per-slide.

Exit codes:
    0 = success
    1 = bad input
    2 = template not found
    3 = substitution failed (placeholder unresolved)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

VALID_DIMENSIONS = {
    "1080x1080": "carousel-1080.svg.tpl",
    "1200x675":  "carousel-1200x675.svg.tpl",
}

# CTA varian catalog (mirror of references/cta-variants.md)
CTA_VARIANTS = {
    "upgrade-tampilan":     ("Upgrade Tampilan Jurnal Anda", "Tema OJS profesional siap pakai"),
    "tema-premium":         ("Lihat Tema OJS Premium", "Desain modern untuk jurnal akademik"),
    "langganan-tema":       ("Langganan Tema OJS", "Akses semua tema, update berkala"),
    "mulai-jurnal-baru":    ("Mulai Jurnal Baru", "Tema OJS siap deploy hari ini"),
    "revamp-jurnal":        ("Revamp Jurnal Lama Anda", "Update tampilan tanpa migrasi data"),
    "standar-internasional":("Tampilan Standar Internasional", "Tema OJS yang lolos uji indeksasi"),
    "kompatibel-ojs3":      ("Kompatibel OJS 3.x Terbaru", "Tema yang selalu update versi"),
    "siap-doaj-scopus":     ("Siap Indeks DOAJ & Scopus", "Tema dengan markup metadata lengkap"),
    "wcag-compliant":       ("Tema WCAG-Compliant", "Aksesibilitas untuk semua pembaca"),
    "lihat-koleksi":        ("Lihat Koleksi Tema OJS", "30+ desain untuk berbagai disiplin"),
    "temukan-tema":         ("Temukan Tema yang Pas", "Filter by audience, layout, palette"),
    "inspirasi-tampilan":   ("Inspirasi Tampilan Jurnal", "Browse showcase jurnal real"),
    "instal-hari-ini":      ("Instal Hari Ini", "Tema OJS plug-and-play"),
    "tanpa-koding":         ("Ganti Tema Tanpa Koding", "Konfigurasi via dashboard OJS"),
    "support-bahasa-id":    ("Support Bahasa Indonesia", "Dokumentasi & bantuan dalam Bahasa Indonesia"),
}


def wrap_text(text, max_chars_per_line, max_lines):
    """Greedy word-wrap. Return list of lines, padded with empty strings to max_lines."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        candidate = (current + " " + w).strip()
        if len(candidate) <= max_chars_per_line:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = w
            if len(lines) >= max_lines:
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    while len(lines) < max_lines:
        lines.append("")
    return lines[:max_lines]


def select_cta_variant(article_id, exclude_recent=None):
    """Hash-based selection, exclude recent variants."""
    exclude_recent = exclude_recent or []
    available = [k for k in CTA_VARIANTS if k not in exclude_recent]
    if not available:
        available = list(CTA_VARIANTS.keys())
    h = hash(article_id) % len(available)
    return available[h]


def domain_from_url(url):
    """Extract domain stem (no scheme, no trailing slash)."""
    m = re.match(r"https?://([^/]+)", url)
    return m.group(1) if m else url


def humanize_date(iso_date):
    """ISO-8601 → human Indonesian date."""
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        bulan = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
        return f"{dt.day} {bulan[dt.month-1]} {dt.year}"
    except (ValueError, IndexError):
        return iso_date


def build_substitution(brief, candidate, dimension):
    """Build placeholder→value mapping based on dimension."""
    if dimension == "1080x1080":
        wrap_title = (24, 2)
        wrap_keypoint = (28, 4)
        wrap_context = (38, 3)
        wrap_implication = (38, 5)
        wrap_cta = (22, 2)
    else:  # 1200x675
        wrap_title = (28, 2)
        wrap_keypoint = (34, 4)
        wrap_context = (50, 3)
        wrap_implication = (50, 5)
        wrap_cta = (26, 2)

    title = brief.get("title", candidate.get("title", ""))
    title_lines = wrap_text(title, *wrap_title)

    key_points = brief.get("key_points", candidate.get("key_points", []))
    while len(key_points) < 3:
        key_points.append("")
    kp1_lines = wrap_text(key_points[0], *wrap_keypoint)
    kp2_lines = wrap_text(key_points[1], *wrap_keypoint)
    kp3_lines = wrap_text(key_points[2], *wrap_keypoint)

    summary = candidate.get("summary_raw", "")
    context_lines = wrap_text(summary[:200], *wrap_context)

    implication = brief.get("implication") or "Periksa workflow editorial untuk dampak operasional."
    impl_lines = wrap_text(implication, *wrap_implication)

    cta_label = brief.get("cta_variant_used") or select_cta_variant(
        candidate.get("id", ""),
        exclude_recent=brief.get("recent_cta_variants", [])
    )
    cta_headline, cta_sub = CTA_VARIANTS[cta_label]
    cta_lines = wrap_text(cta_headline, *wrap_cta)

    source_url = candidate.get("source_url", "")
    source_domain = domain_from_url(source_url)

    published_at = candidate.get("published_at", "")
    date_human = humanize_date(published_at)

    relevance_tags = candidate.get("relevance_tags", [])
    icon_svg = pick_icon_svg(relevance_tags)

    return {
        "{{TITLE}}": title,
        "{{TITLE_LINE_1}}": title_lines[0],
        "{{TITLE_LINE_2}}": title_lines[1],
        "{{KEY_POINT_1}}": key_points[0],
        "{{KEY_POINT_2}}": key_points[1],
        "{{KEY_POINT_3}}": key_points[2],
        "{{KEY_POINT_1_LINE_1}}": kp1_lines[0],
        "{{KEY_POINT_1_LINE_2}}": kp1_lines[1],
        "{{KEY_POINT_1_LINE_3}}": kp1_lines[2],
        "{{KEY_POINT_1_LINE_4}}": kp1_lines[3],
        "{{KEY_POINT_2_LINE_1}}": kp2_lines[0],
        "{{KEY_POINT_2_LINE_2}}": kp2_lines[1],
        "{{KEY_POINT_2_LINE_3}}": kp2_lines[2],
        "{{KEY_POINT_2_LINE_4}}": kp2_lines[3],
        "{{KEY_POINT_3_LINE_1}}": kp3_lines[0],
        "{{KEY_POINT_3_LINE_2}}": kp3_lines[1],
        "{{KEY_POINT_3_LINE_3}}": kp3_lines[2],
        "{{KEY_POINT_3_LINE_4}}": kp3_lines[3],
        "{{CONTEXT_LINE_1}}": context_lines[0],
        "{{CONTEXT_LINE_2}}": context_lines[1],
        "{{CONTEXT_LINE_3}}": context_lines[2],
        "{{IMPLICATION_LINE_1}}": impl_lines[0],
        "{{IMPLICATION_LINE_2}}": impl_lines[1],
        "{{IMPLICATION_LINE_3}}": impl_lines[2],
        "{{IMPLICATION_LINE_4}}": impl_lines[3],
        "{{IMPLICATION_LINE_5}}": impl_lines[4],
        "{{CTA_HEADLINE}}": cta_headline,
        "{{CTA_HEADLINE_LINE_1}}": cta_lines[0],
        "{{CTA_HEADLINE_LINE_2}}": cta_lines[1],
        "{{CTA_SUB}}": cta_sub,
        "{{CTA_VARIANT_LABEL}}": cta_label,
        "{{SOURCE_DOMAIN}}": source_domain,
        "{{DATE_HUMAN}}": date_human,
        "{{ICON_SVG}}": icon_svg,
    }


def pick_icon_svg(relevance_tags):
    """Inline Heroicons outline SVG by primary tag (returned as <g> contents)."""
    primary = relevance_tags[0] if relevance_tags else "feature"
    icons = {
        "security":    '<circle cx="0" cy="0" r="60" fill="none" stroke="#F8FAFC" stroke-width="4"/><text x="0" y="20" text-anchor="middle" font-size="80" fill="#F8FAFC">⚠</text>',
        "release":     '<polygon points="-50,40 0,-50 50,40 0,15" fill="#F8FAFC"/>',
        "feature":     '<circle cx="0" cy="0" r="50" fill="none" stroke="#F8FAFC" stroke-width="4"/><circle cx="0" cy="0" r="20" fill="#F8FAFC"/>',
        "tutorial":    '<rect x="-50" y="-30" width="100" height="60" fill="none" stroke="#F8FAFC" stroke-width="4"/>',
        "community":   '<circle cx="-25" cy="0" r="22" fill="#F8FAFC"/><circle cx="25" cy="0" r="22" fill="#F8FAFC"/>',
        "integration": '<rect x="-50" y="-15" width="40" height="30" fill="#F8FAFC"/><rect x="10" y="-15" width="40" height="30" fill="#F8FAFC"/>',
        "policy":      '<rect x="-40" y="-50" width="80" height="100" fill="none" stroke="#F8FAFC" stroke-width="4"/>',
    }
    return icons.get(primary, icons["feature"])


def render(template_path, substitutions, output_path):
    """Read template, substitute placeholders, write output."""
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}", file=sys.stderr)
        return 2

    content = template_path.read_text(encoding="utf-8")
    for placeholder, value in substitutions.items():
        content = content.replace(placeholder, str(value))

    # Verify no unresolved placeholders remain
    unresolved = re.findall(r"\{\{[A-Z_0-9]+\}\}", content)
    if unresolved:
        print(f"⚠️  Unresolved placeholders: {set(unresolved)}", file=sys.stderr)
        # Replace remaining with empty string rather than fail hard
        for p in set(unresolved):
            content = content.replace(p, "")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"✅ Rendered: {output_path}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Render SAI carousel SVG from brief + candidate JSON")
    parser.add_argument("--brief", required=True, help="Path to brief JSON")
    parser.add_argument("--candidate", required=True, help="Path to candidate JSON")
    parser.add_argument("--dimension", required=True, choices=list(VALID_DIMENSIONS.keys()))
    parser.add_argument("--output", help="Output SVG path (single combined file)")
    parser.add_argument("--templates-dir", default="assets",
                        help="Directory containing carousel templates (default: assets)")
    args = parser.parse_args()

    if not args.output:
        print("❌ --output required", file=sys.stderr)
        return 1

    try:
        brief = json.loads(Path(args.brief).read_text(encoding="utf-8"))
        candidate = json.loads(Path(args.candidate).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Bad input: {e}", file=sys.stderr)
        return 1

    template_path = Path(args.templates_dir) / VALID_DIMENSIONS[args.dimension]
    substitutions = build_substitution(brief, candidate, args.dimension)
    return render(template_path, substitutions, Path(args.output))


if __name__ == "__main__":
    sys.exit(main())
