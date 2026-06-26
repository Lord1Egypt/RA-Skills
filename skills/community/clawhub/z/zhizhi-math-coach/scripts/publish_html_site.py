#!/usr/bin/env python3
"""Publish child-facing worksheet HTML/PDF files into a GitHub Pages site directory."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


FORBIDDEN_SITE_PARTS = {
    "answer-key.md",
    "records",
    "mistakes",
    "memory",
    "weak-points",
    "knowledge-points",
    "curriculum",
    "uploads",
    "textbooks",
    "ocr-output",
}
FORBIDDEN_HTML_MARKERS = {
    "answer_detail",
    "答案与批改标准",
    "## 答案",
    "批改重点",
    "复评标准",
}


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_json_if_exists(path: Path) -> dict:
    if not path.exists():
        return {}
    return load_json(path)


def rel_to(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def discover_worksheet_dirs(roots: list[Path]) -> list[Path]:
    dirs: set[Path] = set()
    for root in roots:
        if root.is_file() and root.name == "worksheet.html":
            dirs.add(root.parent)
        elif root.is_dir() and (root / "worksheet.html").exists():
            dirs.add(root)
        elif root.is_dir():
            for html_path in root.rglob("worksheet.html"):
                dirs.add(html_path.parent)
    return sorted(dirs)


def safe_slug(worksheet_dir: Path, workspace: Path) -> str:
    try:
        rel = worksheet_dir.resolve().relative_to(workspace.resolve())
        parts = [part for part in rel.parts if part not in {"worksheets", "examples", "student-workspace"}]
        if parts:
            return "-".join(parts)
    except ValueError:
        pass
    return worksheet_dir.name


def assert_public_html_safe(html_path: Path) -> None:
    text = html_path.read_text(encoding="utf-8")
    for marker in FORBIDDEN_HTML_MARKERS:
        if marker in text:
            raise ValueError(f"{html_path} contains forbidden public marker: {marker}")


def assert_site_safe(site_dir: Path) -> None:
    if not site_dir.exists():
        return
    for path in site_dir.rglob("*"):
        parts = set(path.parts)
        if parts & FORBIDDEN_SITE_PARTS:
            raise ValueError(f"forbidden path in public site: {path}")
        if path.name == "answer-key.md":
            raise ValueError(f"answer key must not be published: {path}")
        if path.is_file() and path.suffix.lower() == ".html":
            assert_public_html_safe(path)


def page_url(base_url: str | None, slug: str) -> str | None:
    if not base_url:
        return None
    return base_url.rstrip("/") + f"/worksheets/{slug}/"


def pdf_url(base_url: str | None, slug: str) -> str | None:
    worksheet_url = page_url(base_url, slug)
    if not worksheet_url:
        return None
    return worksheet_url + "worksheet.pdf"


def clean_cell(value: str) -> str:
    return value.strip().strip("`").strip()


def split_markdown_row(line: str) -> list[str]:
    return [clean_cell(cell) for cell in line.strip().strip("|").split("|")]


def load_status_rows(workspace: Path) -> tuple[dict[str, dict], dict[str, dict]]:
    path_rows: dict[str, dict] = {}
    title_rows: dict[str, dict] = {}
    status_path = workspace / "worksheets" / "status.md"
    if not status_path.exists():
        return path_rows, title_rows

    section = ""
    for raw_line in status_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            section = line.lstrip("#").strip()
            continue
        if not line.startswith("|") or "---" in line:
            continue

        cells = split_markdown_row(line)
        if len(cells) < 4 or cells[0] == "日期":
            continue

        if "已完成" in section:
            row = {
                "date": cells[0],
                "title": cells[1],
                "worksheet_path": cells[2],
                "practice_status": "已练习",
                "completion": cells[3],
            }
        elif "待" in section or "未" in section:
            row = {
                "date": cells[0],
                "title": cells[1],
                "worksheet_path": cells[2],
                "practice_status": "未练习",
                "completion": cells[3],
            }
        else:
            continue

        if row["worksheet_path"] and row["worksheet_path"] != "暂无":
            path_rows[row["worksheet_path"]] = row
        if row["title"] and row["title"] != "暂无":
            title_rows[row["title"]] = row

    return path_rows, title_rows


def date_from_slug(slug: str) -> str:
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", slug)
    return match.group(1) if match else ""


def count_items(spec: dict) -> int | None:
    sections = spec.get("sections")
    if not isinstance(sections, list):
        return None
    total = 0
    for section in sections:
        if isinstance(section, dict) and isinstance(section.get("items"), list):
            total += len(section["items"])
    return total


def status_for(
    worksheet_dir: Path,
    workspace: Path,
    title: str,
    path_status: dict[str, dict],
    title_status: dict[str, dict],
) -> dict:
    worksheet_rel = rel_to(worksheet_dir / "worksheet.html", workspace)
    row = path_status.get(worksheet_rel) or title_status.get(title)
    if row:
        return row
    return {
        "practice_status": "未练习",
        "completion": "待完成",
        "worksheet_path": worksheet_rel,
    }


def entry_for(
    worksheet_dir: Path,
    workspace: Path,
    site_dir: Path,
    base_url: str | None,
    path_status: dict[str, dict],
    title_status: dict[str, dict],
) -> dict:
    slug = safe_slug(worksheet_dir, workspace)
    spec_path = worksheet_dir / "worksheet-spec.json"
    publish_path = worksheet_dir / "publish.json"
    spec = load_json_if_exists(spec_path)
    published = load_json_if_exists(publish_path)
    title = spec.get("title") or published.get("title") or slug
    status = status_for(worksheet_dir, workspace, title, path_status, title_status)
    if title == slug and status.get("title"):
        title = status["title"]
    item_count = count_items(spec)
    url = page_url(base_url, slug) or published.get("url")
    site_path = rel_to(site_dir / "worksheets" / slug / "index.html", workspace)
    pdf_path = worksheet_dir / "worksheet.pdf"
    has_pdf = pdf_path.exists()
    site_pdf_path = site_dir / "worksheets" / slug / "worksheet.pdf"
    pdf_location = pdf_url(base_url, slug) if has_pdf else published.get("pdf_url")
    return {
        "slug": slug,
        "title": title,
        "date": spec.get("date") or published.get("date") or status.get("date") or date_from_slug(slug),
        "topic": spec.get("topic") or published.get("topic") or "",
        "grade": spec.get("grade") or "",
        "target": spec.get("target") or "",
        "strategy": spec.get("strategy") or published.get("strategy") or "",
        "item_count": item_count,
        "practice_status": status.get("practice_status") or "未练习",
        "completion": status.get("completion") or "待完成",
        "source_worksheet": rel_to(worksheet_dir / "worksheet.html", workspace),
        "source_pdf": rel_to(pdf_path, workspace) if has_pdf else published.get("source_pdf", ""),
        "source_spec": rel_to(spec_path, workspace) if spec_path.exists() else "",
        "site_path": site_path,
        "site_pdf_path": rel_to(site_pdf_path, workspace) if has_pdf else published.get("site_pdf_path", ""),
        "url": url,
        "pdf_url": pdf_location,
        "visibility": "public-child-facing",
    }


def write_index(site_dir: Path, entries: list[dict]) -> None:
    rows = []
    cards = []
    for entry in sorted(entries, key=lambda item: (item.get("date", ""), item.get("title", "")), reverse=True):
        title = e(entry.get("title") or entry["slug"])
        date = e(entry.get("date") or "")
        topic = e(entry.get("topic") or "")
        grade = e(entry.get("grade") or "")
        item_count = entry.get("item_count")
        count_text = e(f"{item_count}题" if item_count is not None else "")
        status = e(entry.get("practice_status") or "未练习")
        completion = e(entry.get("completion") or "待完成")
        href = e(f"worksheets/{entry['slug']}/")
        pdf_href = e(f"worksheets/{entry['slug']}/worksheet.pdf") if entry.get("pdf_url") or entry.get("site_pdf_path") else ""
        pdf_link = f'<a href="{pdf_href}">PDF</a>' if pdf_href else ""
        status_class = "done" if entry.get("practice_status") == "已练习" else "todo"
        rows.append(
            "          <tr>"
            f"<td>{date}</td>"
            f'<td><span class="status {status_class}">{status}</span></td>'
            f'<td><a href="{href}">{title}</a></td>'
            f'<td class="links"><a href="{href}">HTML</a>{pdf_link}</td>'
            f"<td>{topic}</td>"
            f"<td>{grade}</td>"
            f"<td>{count_text}</td>"
            f"<td>{completion}</td>"
            "</tr>"
        )
        details = " / ".join(part for part in [date, topic, grade, count_text] if part)
        cards.append(
            "      <li>"
            f'<div><span class="status {status_class}">{status}</span></div>'
            f'<a href="{href}">{title}</a>'
            + (f'<span class="meta">{e(details)}</span>' if details else "")
            + (f'<span class="meta">文件：<a href="{href}">HTML</a>{" / " + pdf_link if pdf_link else ""}</span>')
            + f'<span class="meta">完成情况：{completion}</span>'
            + "</li>"
        )

    html_text = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Zhizhi Math Coach Worksheets</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #111; background: #f7f7f7; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 32px 18px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    p {{ margin: 0 0 20px; color: #555; }}
    .table-wrap {{ overflow-x: auto; background: #fff; border: 1px solid #ddd; border-radius: 6px; }}
    table {{ width: 100%; min-width: 900px; border-collapse: collapse; }}
    th, td {{ padding: 12px 14px; border-bottom: 1px solid #e6e6e6; text-align: left; vertical-align: top; font-size: 14px; }}
    th {{ background: #f1f3f5; color: #333; font-weight: 700; white-space: nowrap; }}
    tr:last-child td {{ border-bottom: 0; }}
    a {{ color: #0645d8; font-weight: 650; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .links a + a {{ margin-left: 10px; }}
    .status {{ display: inline-block; min-width: 48px; padding: 3px 8px; border-radius: 999px; font-size: 13px; font-weight: 700; text-align: center; }}
    .status.done {{ color: #116329; background: #dafbe1; }}
    .status.todo {{ color: #7d4e00; background: #fff1c2; }}
    ul {{ list-style: none; margin: 0; padding: 0; display: none; gap: 10px; }}
    li {{ background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 14px 16px; }}
    .meta {{ display: block; margin-top: 6px; font-size: 14px; color: #666; }}
    @media (max-width: 760px) {{
      .table-wrap {{ display: none; }}
      ul {{ display: grid; }}
    }}
  </style>
</head>
<body>
  <main>
    <h1>Zhizhi Math Coach 练习卷</h1>
    <p>按日期倒序展示学生可见练习卷；答案、批改记录和学习档案不进入公开站点。</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>日期</th>
            <th>状态</th>
            <th>练习卷</th>
            <th>文件</th>
            <th>主题</th>
            <th>年级</th>
            <th>题量</th>
            <th>完成情况</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(rows) if rows else '          <tr><td colspan="8">暂无练习卷</td></tr>'}
        </tbody>
      </table>
    </div>
    <ul>
{chr(10).join(cards) if cards else "      <li>暂无练习卷</li>"}
    </ul>
  </main>
</body>
</html>
"""
    (site_dir / "index.html").write_text(html_text, encoding="utf-8")


def publish_one(worksheet_dir: Path, workspace: Path, site_dir: Path, base_url: str | None) -> dict:
    html_path = worksheet_dir / "worksheet.html"
    if not html_path.exists():
        raise ValueError(f"missing worksheet.html in {worksheet_dir}")
    assert_public_html_safe(html_path)

    slug = safe_slug(worksheet_dir, workspace)
    target_dir = site_dir / "worksheets" / slug
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(html_path, target_dir / "index.html")
    pdf_path = worksheet_dir / "worksheet.pdf"
    has_pdf = pdf_path.exists()
    if has_pdf:
        shutil.copy2(pdf_path, target_dir / "worksheet.pdf")
    elif (target_dir / "worksheet.pdf").exists():
        (target_dir / "worksheet.pdf").unlink()

    spec_path = worksheet_dir / "worksheet-spec.json"
    spec = load_json_if_exists(spec_path)
    url = page_url(base_url, slug)
    existing_manifest = load_json_if_exists(worksheet_dir / "publish.json")
    published_at = existing_manifest.get("published_at") or datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest = {
        "title": spec.get("title") or slug,
        "date": spec.get("date", ""),
        "topic": spec.get("topic", ""),
        "strategy": spec.get("strategy", ""),
        "source_worksheet": rel_to(html_path, workspace),
        "source_pdf": rel_to(pdf_path, workspace) if has_pdf else "",
        "source_spec": rel_to(spec_path, workspace) if spec_path.exists() else "",
        "site_path": rel_to(target_dir / "index.html", workspace),
        "site_pdf_path": rel_to(target_dir / "worksheet.pdf", workspace) if has_pdf else "",
        "url": url,
        "pdf_url": pdf_url(base_url, slug) if has_pdf else "",
        "visibility": "public-child-facing",
        "published_at": published_at,
    }
    (worksheet_dir / "publish.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"slug": slug, **manifest}


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish child-facing worksheet HTML/PDF files to a static site directory.")
    parser.add_argument("paths", nargs="*", type=Path, help="Worksheet directories, worksheet.html files, or roots to scan.")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="Learning workspace root. Defaults to cwd.")
    parser.add_argument("--site-dir", type=Path, default=Path("site"), help="Output site directory relative to workspace.")
    parser.add_argument("--base-url", help="Optional GitHub Pages base URL, such as https://user.github.io/repo")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    site_dir = args.site_dir if args.site_dir.is_absolute() else workspace / args.site_dir
    roots = args.paths or [workspace / "worksheets", workspace / "examples" / "student-workspace" / "worksheets"]
    roots = [path if path.is_absolute() else workspace / path for path in roots]
    publish_dirs = discover_worksheet_dirs(roots)
    if not publish_dirs:
        raise ValueError("no worksheet.html files found")

    site_dir.mkdir(parents=True, exist_ok=True)
    (site_dir / ".nojekyll").write_text("", encoding="utf-8")

    all_dirs = discover_worksheet_dirs([workspace / "worksheets"])
    if not all_dirs:
        all_dirs = publish_dirs
    for path in all_dirs:
        publish_one(path, workspace, site_dir, args.base_url)

    path_status, title_status = load_status_rows(workspace)
    entries = [entry_for(path, workspace, site_dir, args.base_url, path_status, title_status) for path in all_dirs]
    write_index(site_dir, entries)
    assert_site_safe(site_dir)

    print(f"published: {site_dir}")
    for entry in entries:
        location = entry.get("url") or entry["site_path"]
        print(f"- {entry['title']}: {location}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
