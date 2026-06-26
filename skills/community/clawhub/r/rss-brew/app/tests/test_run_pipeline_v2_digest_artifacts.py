from pathlib import Path

from rss_brew.compat.run_pipeline_v2 import publish_staging_to_versioned, promote_winner_outputs


def test_publish_and_promote_digest_artifacts(tmp_path):
    staging_dir = tmp_path / "staging"
    publish_dir = tmp_path / "published"
    data_root = tmp_path / "data-root"

    (staging_dir / "digests").mkdir(parents=True)
    (data_root / "digests").mkdir(parents=True)

    digest_md = staging_dir / "digests" / "daily-digest-2026-03-12.md"
    digest_html = staging_dir / "digests" / "rss-brew-digest-2026-03-12.html"
    digest_pdf = staging_dir / "digests" / "rss-brew-digest-2026-03-12.pdf"
    deep_set = staging_dir / "deep-set.json"
    scored = staging_dir / "scored-articles.json"
    new_articles = staging_dir / "new-articles.json"
    metadata = staging_dir / "metadata.json"
    processed = staging_dir / "processed-index.json"

    digest_md.write_text("digest md", encoding="utf-8")
    digest_html.write_text("digest html", encoding="utf-8")
    digest_pdf.write_bytes(b"%PDF-1.4 test")
    deep_set.write_text("{}", encoding="utf-8")
    scored.write_text("{}", encoding="utf-8")
    new_articles.write_text("{}", encoding="utf-8")
    metadata.write_text("{}", encoding="utf-8")
    processed.write_text("{}", encoding="utf-8")

    publish_staging_to_versioned(staging_dir, publish_dir, digest_md, digest_html, digest_pdf)

    assert (publish_dir / digest_md.name).read_text(encoding="utf-8") == "digest md"
    assert (publish_dir / digest_html.name).read_text(encoding="utf-8") == "digest html"
    assert (publish_dir / digest_pdf.name).read_bytes() == b"%PDF-1.4 test"

    target_digest = data_root / "digests" / "custom-output.md"
    promoted = promote_winner_outputs(
        publish_dir,
        data_root,
        data_root / "new-articles.json",
        data_root / "scored-articles.json",
        data_root / "deep-set.json",
        target_digest,
        data_root / "processed-index.json",
        data_root / "metadata.json",
    )

    assert promoted is True
    assert target_digest.read_text(encoding="utf-8") == "digest md"
    assert target_digest.with_suffix(".html").read_text(encoding="utf-8") == "digest html"
    assert target_digest.with_suffix(".pdf").read_bytes() == b"%PDF-1.4 test"
