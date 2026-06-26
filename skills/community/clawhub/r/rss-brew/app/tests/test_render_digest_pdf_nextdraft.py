from rss_brew.compat.render_digest_pdf_nextdraft import parse_digest


def test_parse_digest_parses_all_other_items_and_fields(tmp_path):
    md = tmp_path / "daily-digest-2026-03-12.md"
    md.write_text(
        """# RSS Brew Daily Digest — 2026-03-12

## Deep Set

### 1. Deep article
- Score: 5/5
- Category: vc-investment
- Source: Example Source
- URL: https://example.com/deep
- English Summary: Deep summary
- 中文摘要: 深度摘要

## Other New Articles

- Other article A
  - Score: 1/5
  - URL: https://example.com/a
  - 备注: Note A
- Other article B
  - Score: 3/5
  - URL: https://example.com/b
  - 备注: Note B

## Pipeline Status
- total_new_articles: 3
""",
        encoding="utf-8",
    )

    data = parse_digest(md)

    assert len(data["articles"]) == 1
    assert len(data["others"]) == 2
    assert [item["title"] for item in data["others"]] == [
        "Other article A",
        "Other article B",
    ]
    assert data["others"][0]["score"] == "1/5"
    assert data["others"][0]["url"] == "https://example.com/a"
    assert data["others"][0]["note"] == "Note A"
    assert data["others"][1]["score"] == "3/5"
    assert data["others"][1]["url"] == "https://example.com/b"
    assert data["others"][1]["note"] == "Note B"
