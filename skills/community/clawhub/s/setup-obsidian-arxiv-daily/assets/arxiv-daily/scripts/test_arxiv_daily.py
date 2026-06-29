import io
import json
import os
import re
import subprocess
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stdout
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import ANY, Mock, call, patch
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

import arxiv_daily
from arxiv_daily import (
    Config,
    FieldConfig,
    Paper,
    Summary,
    authors_yaml,
    archive_old_papers,
    build_arxiv_search_query,
    extract_arxiv_id,
    fetch_arxiv_papers,
    load_existing_arxiv_ids,
    log_line,
    main,
    markdown_bullets,
    normalize_space,
    fallback_summary,
    paper_note_path,
    parse_arxiv_feed,
    parse_config,
    parse_deepseek_summary,
    render_paper_markdown,
    run,
    sanitize_filename,
    summarize_paper,
    summarize_with_deepseek,
    build_summary_prompt,
    read_frontmatter_value,
    vault_wikilink,
    write_daily_summary,
    write_paper_note,
    yaml_quote,
)


class ArxivDailyHelperTests(unittest.TestCase):
    def _read_bytes_after_release(self, path: Path) -> bytes:
        return subprocess.check_output(
            [
                sys.executable,
                "-c",
                (
                    "from pathlib import Path; import sys; "
                    "sys.stdout.buffer.write(Path(sys.argv[1]).read_bytes())"
                ),
                str(path),
            ]
        )

    def test_normalize_space_collapses_whitespace(self):
        self.assertEqual(normalize_space(" A\n Test\tTitle "), "A Test Title")

    def test_sanitize_log_message_redacts_crlf_secret_and_bearer_tokens(self):
        secret = "sk-test-secret-123"
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": secret}, clear=False):
            self.assertEqual(
                arxiv_daily._sanitize_log_message(
                    f"hello\r\nBearer abc123 and {secret} and bearer XYZ"
                ),
                "hello Bearer [REDACTED] and [REDACTED] and Bearer [REDACTED]",
            )

    def test_log_line_appends_sanitized_utf8_entry_and_checks_path_safety(
        self,
    ):
        secret = "sk-test-secret-123"
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"

            with patch.dict(os.environ, {"DEEPSEEK_API_KEY": secret}, clear=False):
                arxiv_daily.log_line(
                    root,
                    date(2026, 6, 8),
                    f"hello\r\nBearer abc123 and {secret}",
                )

            log_path = root / "logs" / "2026-06-08.log"
            content = log_path.read_text(encoding="utf-8")

            self.assertTrue(
                re.match(
                    r"^\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
                    content,
                )
            )
            self.assertIn("hello Bearer [REDACTED] and [REDACTED]", content)
            self.assertNotIn("sk-test-secret-123", content)
            self.assertNotIn("Bearer abc123", content)
            self.assertTrue(content.endswith("\n"))

            self.assertEqual(
                content.count("\n"),
                1,
                "log_line should append exactly one line per call",
            )

            with patch.object(
                arxiv_daily,
                "_assert_safe_output_path",
                wraps=arxiv_daily._assert_safe_output_path,
            ) as safe_mock:
                arxiv_daily.log_line(root, date(2026, 6, 8), "second line")
                safe_mock.assert_any_call(
                    root / "logs",
                    root / "logs" / "2026-06-08.log",
                )

    def test_log_line_rejects_redirected_logs_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            outside = Path(temporary_directory) / "outside"
            logs_link = root / "logs"
            outside.mkdir()
            root.mkdir(parents=True, exist_ok=True)
            try:
                os.symlink(outside, logs_link, target_is_directory=True)
            except (OSError, NotImplementedError):
                if os.name != "nt":
                    self.fail("Unable to create a directory redirection")
                result = subprocess.run(
                    [
                        "cmd",
                        "/c",
                        "mklink",
                        "/J",
                        str(logs_link.resolve(strict=False)),
                        str(outside.resolve(strict=False)),
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

            try:
                with self.assertRaises(ValueError):
                    arxiv_daily.log_line(root, date(2026, 6, 8), "hello")
            finally:
                if logs_link.is_symlink():
                    logs_link.unlink(missing_ok=True)
                elif logs_link.exists():
                    os.rmdir(logs_link)

    def test_lock_file_path_is_stable_hash_based_and_outside_root(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            same_root = root / "."
            other_root = Path(temporary_directory) / "other-arxiv-daily"

            root_lock_path = arxiv_daily._lock_file_path(root)
            same_root_lock_path = arxiv_daily._lock_file_path(same_root)
            other_root_lock_path = arxiv_daily._lock_file_path(other_root)

        expected_parent = Path(tempfile.gettempdir()) / "obsidian-arxiv-daily-locks"
        self.assertEqual(root_lock_path.parent, expected_parent)
        self.assertEqual(same_root_lock_path.parent, expected_parent)
        self.assertEqual(other_root_lock_path.parent, expected_parent)
        self.assertEqual(root_lock_path, same_root_lock_path)
        self.assertNotEqual(root_lock_path, other_root_lock_path)
        self.assertRegex(root_lock_path.name, r"^[0-9a-f]{64}\.lock$")
        self.assertFalse(root_lock_path.is_relative_to(root))
        self.assertFalse(root_lock_path.is_relative_to(other_root))
        self.assertFalse(same_root_lock_path.is_relative_to(root))

    def test_single_instance_lock_persists_outside_root_and_can_be_read_after_release(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()
            lock_path = arxiv_daily._lock_file_path(root)

            with arxiv_daily._single_instance_lock(root):
                self.assertTrue(lock_path.exists())
                self.assertFalse(lock_path.is_relative_to(root))
                self.assertEqual(lock_path.stat().st_size, 1)

            self.assertTrue(lock_path.exists())
            content = self._read_bytes_after_release(lock_path)
            self.assertEqual(content, b"\x00")
            self.assertNotIn(b"sk-", content)
            self.assertNotIn(b"Bearer", content)

            with arxiv_daily._single_instance_lock(root):
                self.assertTrue(lock_path.exists())
                self.assertEqual(lock_path.stat().st_size, 1)

            self.assertEqual(self._read_bytes_after_release(lock_path), b"\x00")

    def test_build_arxiv_search_query_adds_fields_and_implicit_and(self):
        self.assertEqual(
            build_arxiv_search_query(
                "retrieval augmented generation OR RAG"
            ),
            "all:retrieval AND all:augmented AND all:generation OR all:RAG",
        )

    def test_build_arxiv_search_query_preserves_quoted_phrase(self):
        self.assertEqual(
            build_arxiv_search_query('"large language model" AND agent'),
            'all:"large language model" AND all:agent',
        )

    def test_build_arxiv_search_query_adds_implicit_and_before_or(self):
        self.assertEqual(
            build_arxiv_search_query("AI safety OR alignment"),
            "all:AI AND all:safety OR all:alignment",
        )

    def test_build_arxiv_search_query_preserves_fields_and_andnot(self):
        self.assertEqual(
            build_arxiv_search_query("cat:cs.AI ANDNOT ti:survey"),
            "cat:cs.AI ANDNOT ti:survey",
        )

    def test_build_arxiv_search_query_preserves_supported_fields(self):
        for prefix in (
            "ti",
            "au",
            "abs",
            "co",
            "jr",
            "cat",
            "rn",
            "id",
            "all",
        ):
            with self.subTest(prefix=prefix):
                self.assertEqual(
                    build_arxiv_search_query(f'{prefix}:"test value"'),
                    f'{prefix}:"test value"',
                )

    def test_build_arxiv_search_query_preserves_submitted_date_range(self):
        date_range = "submittedDate:[202605300102 TO 202606060102]"
        self.assertEqual(build_arxiv_search_query(date_range), date_range)

    def test_parse_arxiv_feed_returns_normalized_paper(self):
        xml_text = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2501.12345v2</id>
    <updated>2026-06-06T01:02:03Z</updated>
    <published>2026-06-05T01:02:03Z</published>
    <title> A Test Paper
Title </title>
    <summary> This is the abstract. </summary>
    <author><name>Alice</name></author>
    <author><name>Bob</name></author>
    <link title="pdf" href="http://arxiv.org/pdf/2501.12345v2" />
  </entry>
</feed>
"""

        papers = parse_arxiv_feed(
            xml_text,
            field="LLM Agent",
            matched_query='"large language model" AND agent',
        )

        self.assertEqual(
            papers,
            [
                Paper(
                    arxiv_id="2501.12345",
                    title="A Test Paper Title",
                    authors=["Alice", "Bob"],
                    published=date(2026, 6, 5),
                    updated=date(2026, 6, 6),
                    abstract="This is the abstract.",
                    url="https://arxiv.org/abs/2501.12345v2",
                    pdf_url="https://arxiv.org/pdf/2501.12345v2",
                    field="LLM Agent",
                    matched_query='"large language model" AND agent',
                )
            ],
        )

    def test_parse_arxiv_feed_derives_pdf_url_for_legacy_id(self):
        xml_text = """\
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/hep-ex/0307015v2</id>
    <updated>2026-06-06T01:02:03Z</updated>
    <published>2026-06-05T01:02:03Z</published>
    <title>Legacy Paper</title>
    <summary>Legacy abstract.</summary>
  </entry>
</feed>
"""

        paper = parse_arxiv_feed(xml_text, "Physics", "hep-ex")[0]

        self.assertEqual(paper.arxiv_id, "hep-ex/0307015")
        self.assertEqual(
            paper.url,
            "https://arxiv.org/abs/hep-ex/0307015v2",
        )
        self.assertEqual(
            paper.pdf_url,
            "https://arxiv.org/pdf/hep-ex/0307015",
        )
        self.assertEqual(paper.authors, [])

    @patch("arxiv_daily.urllib.request.urlopen")
    def test_fetch_arxiv_papers_builds_request(self, urlopen):
        response = urlopen.return_value.__enter__.return_value
        response.read.return_value = (
            b'<?xml version="1.0"?><feed '
            b'xmlns="http://www.w3.org/2005/Atom"></feed>'
        )
        config = Config(
            retention_days=90,
            per_field_limit=5,
            lookback_days=7,
            sort_by="submittedDate",
            sort_order="descending",
            summary_enabled=False,
            summary_provider="deepseek",
            deepseek_model="deepseek-v4-pro",
            deepseek_base_url="https://api.deepseek.com",
            request_timeout_seconds=30,
            fields=[],
        )
        field = FieldConfig(
            name="LLM Agent",
            query='"large language model" AND agent',
        )

        with patch(
            "arxiv_daily.utc_now",
            return_value=datetime(
                2026,
                6,
                6,
                1,
                2,
                tzinfo=timezone.utc,
            ),
        ):
            self.assertEqual(fetch_arxiv_papers(config, field), [])

        request = urlopen.call_args.args[0]
        parameters = parse_qs(urlparse(request.full_url).query)
        self.assertEqual(
            request.full_url.split("?", 1)[0],
            "https://export.arxiv.org/api/query",
        )
        self.assertEqual(
            parameters["search_query"],
            [
                '(all:"large language model" AND all:agent) '
                "AND submittedDate:[202605300102 TO 202606060102]"
            ],
        )
        self.assertEqual(parameters["start"], ["0"])
        self.assertEqual(parameters["max_results"], ["5"])
        self.assertEqual(parameters["sortBy"], ["submittedDate"])
        self.assertEqual(parameters["sortOrder"], ["descending"])
        self.assertEqual(
            request.get_header("User-agent"),
            "ObsidianArxivDaily/1.0",
        )
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 30)

    @patch("arxiv_daily.urllib.request.urlopen")
    def test_fetch_arxiv_papers_groups_or_query_before_date_filter(
        self,
        urlopen,
    ):
        response = urlopen.return_value.__enter__.return_value
        response.read.return_value = (
            b'<?xml version="1.0"?><feed '
            b'xmlns="http://www.w3.org/2005/Atom"></feed>'
        )
        config = Config(
            retention_days=90,
            per_field_limit=5,
            lookback_days=7,
            sort_by="submittedDate",
            sort_order="descending",
            summary_enabled=False,
            summary_provider="deepseek",
            deepseek_model="deepseek-v4-pro",
            deepseek_base_url="https://api.deepseek.com",
            request_timeout_seconds=30,
            fields=[],
        )
        field = FieldConfig(
            name="AI Safety",
            query="AI safety OR alignment",
        )

        with patch(
            "arxiv_daily.utc_now",
            return_value=datetime(
                2026,
                6,
                6,
                1,
                2,
                tzinfo=timezone.utc,
            ),
        ):
            fetch_arxiv_papers(config, field)

        request = urlopen.call_args.args[0]
        parameters = parse_qs(urlparse(request.full_url).query)
        self.assertEqual(
            parameters["search_query"],
            [
                "(all:AI AND all:safety OR all:alignment) "
                "AND submittedDate:[202605300102 TO 202606060102]"
            ],
        )

    def test_sanitize_filename_replaces_windows_invalid_characters(self):
        self.assertEqual(
            sanitize_filename('A/B:C*D?E"F<G>H|I'),
            "A B C D E F G H I",
        )

    def test_extract_arxiv_id_removes_url_prefix_and_version(self):
        self.assertEqual(
            extract_arxiv_id("https://arxiv.org/abs/2501.12345v2"),
            "2501.12345",
        )
        self.assertEqual(extract_arxiv_id("2501.12345v1"), "2501.12345")

    def test_extract_arxiv_id_preserves_legacy_category(self):
        self.assertEqual(
            extract_arxiv_id("hep-ex/0307015v1"),
            "hep-ex/0307015",
        )
        self.assertEqual(
            extract_arxiv_id(
                "https://arxiv.org/abs/hep-ex/0307015v2"
            ),
            "hep-ex/0307015",
        )

    def test_yaml_quote_escapes_double_quotes(self):
        self.assertEqual(
            yaml_quote('A "quoted" title'),
            '"A \\"quoted\\" title"',
        )

    def test_parse_config_reads_minimal_config_and_defaults(self):
        config_text = """\
retention_days: 90
per_field_limit: 5
lookback_days: 7
summary_enabled: true
fields:
  - name: LLM Agent
    query: '"large language model" AND agent'
"""
        with tempfile.TemporaryDirectory() as temporary_directory:
            config_path = Path(temporary_directory) / "config.yaml"
            config_path.write_text(config_text, encoding="utf-8")
            config = parse_config(config_path)

        self.assertEqual(config.retention_days, 90)
        self.assertEqual(config.per_field_limit, 5)
        self.assertEqual(config.lookback_days, 7)
        self.assertTrue(config.summary_enabled)
        self.assertEqual(config.sort_by, "submittedDate")
        self.assertEqual(config.sort_order, "descending")
        self.assertEqual(config.summary_provider, "deepseek")
        self.assertEqual(config.deepseek_model, "deepseek-v4-pro")
        self.assertEqual(config.deepseek_base_url, "https://api.deepseek.com")
        self.assertEqual(config.request_timeout_seconds, 60)
        self.assertEqual(len(config.fields), 1)
        self.assertEqual(config.fields[0].name, "LLM Agent")
        self.assertEqual(
            config.fields[0].query,
            '"large language model" AND agent',
        )

    def test_paper_note_path_uses_date_title_and_arxiv_id(self):
        paper = Paper(
            arxiv_id="2501.12345",
            title="A Very Useful Paper",
            authors=["Ada Lovelace"],
            published=date(2026, 6, 6),
            updated=date(2026, 6, 6),
            abstract="Useful research.",
            url="https://arxiv.org/abs/2501.12345",
            pdf_url="https://arxiv.org/pdf/2501.12345",
            field="LLM Agent",
            matched_query='"large language model" AND agent',
        )

        self.assertEqual(
            paper_note_path(Path("arxiv-daily"), paper),
            Path(
                "arxiv-daily/papers/2026/"
                "2026-06-06 - A Very Useful Paper (2501.12345).md"
            ),
        )

    def test_paper_note_path_sanitizes_legacy_arxiv_id_without_nesting(self):
        paper = Paper(
            arxiv_id="hep-ex/0307015",
            title="Legacy Paper",
            authors=["Ada Lovelace"],
            published=date(2026, 6, 6),
            updated=date(2026, 6, 6),
            abstract="Useful research.",
            url="https://arxiv.org/abs/hep-ex/0307015",
            pdf_url="https://arxiv.org/pdf/hep-ex/0307015",
            field="Physics",
            matched_query="hep-ex",
        )

        path = paper_note_path(Path("arxiv-daily"), paper)

        self.assertEqual(
            path,
            Path(
                "arxiv-daily/papers/2026/"
                "2026-06-06 - Legacy Paper (hep-ex 0307015).md"
            ),
        )
        self.assertEqual(path.parent, Path("arxiv-daily/papers/2026"))
        self.assertLessEqual(len(path.name), 180)

    def test_paper_note_path_caps_unexpectedly_long_arxiv_id_without_changing_frontmatter_id(
        self,
    ):
        long_arxiv_id = "x" * 200
        paper = Paper(
            arxiv_id=long_arxiv_id,
            title="Long ID Paper",
            authors=["Ada Lovelace"],
            published=date(2026, 6, 6),
            updated=date(2026, 6, 6),
            abstract="Useful research.",
            url=f"https://arxiv.org/abs/{long_arxiv_id}",
            pdf_url=f"https://arxiv.org/pdf/{long_arxiv_id}",
            field="Physics",
            matched_query="id",
        )

        path = paper_note_path(Path("arxiv-daily"), paper)

        self.assertLessEqual(len(path.name), 180)
        self.assertIn(long_arxiv_id[:20], path.name)
        self.assertTrue(path.name.endswith(".md"))

    def test_paper_note_path_truncates_very_long_title(self):
        paper = Paper(
            arxiv_id="2501.12345",
            title="A" * 300,
            authors=["Ada Lovelace"],
            published=date(2026, 6, 6),
            updated=date(2026, 6, 6),
            abstract="Useful research.",
            url="https://arxiv.org/abs/2501.12345",
            pdf_url="https://arxiv.org/pdf/2501.12345",
            field="LLM Agent",
            matched_query='"large language model" AND agent',
        )

        path = paper_note_path(Path("arxiv-daily"), paper)

        self.assertLessEqual(len(path.name), 180)
        self.assertTrue(path.name.startswith("2026-06-06 - "))
        self.assertTrue(path.name.endswith(" (2501.12345).md"))


class PaperNoteTests(unittest.TestCase):
    def make_paper(self, **overrides):
        values = {
            "arxiv_id": "2501.12345",
            "title": "A Very Useful Paper",
            "authors": ["Ada Lovelace", "Alan Turing"],
            "published": date(2026, 6, 5),
            "updated": date(2026, 6, 6),
            "abstract": "The original abstract.",
            "url": "https://arxiv.org/abs/2501.12345",
            "pdf_url": "https://arxiv.org/pdf/2501.12345",
            "field": "LLM Agent",
            "matched_query": '"large language model" AND agent',
        }
        values.update(overrides)
        return Paper(**values)

    def make_summary(self):
        return Summary(
            status="generated",
            chinese_summary="这是一篇中文摘要。",
            key_contributions=["贡献一", "贡献二"],
            method_summary="使用了一个简洁的方法。",
            reading_reason="结果值得进一步阅读。",
        )

    def test_write_paper_note_creates_utf8_markdown_with_required_content(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            paper = self.make_paper()

            path = write_paper_note(
                root,
                paper,
                self.make_summary(),
                date(2026, 6, 6),
                dry_run=False,
            )

            content = path.read_text(encoding="utf-8")

        self.assertTrue(content.startswith("---\ntype: arxiv-paper\n"))
        self.assertIn('arxiv_id: "2501.12345"\n', content)
        self.assertIn("authors: [\"Ada Lovelace\", \"Alan Turing\"]\n", content)
        self.assertIn("status: new\n", content)
        self.assertIn("summary_status: generated\n", content)
        self.assertIn("archived: false\n", content)
        self.assertIn("# A Very Useful Paper\n", content)
        for heading in (
            "## 基本信息",
            "## 中文摘要",
            "## 关键贡献",
            "## 方法简述",
            "## 值得阅读的原因",
            "## 原始 Abstract",
        ):
            self.assertIn(heading, content)
        self.assertIn("这是一篇中文摘要。", content)
        self.assertIn("- 贡献一\n- 贡献二", content)
        self.assertIn("Ada Lovelace", content)
        self.assertIn("The original abstract.", content)

    def test_load_existing_arxiv_ids_detects_created_note(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_paper_note(
                root,
                self.make_paper(),
                self.make_summary(),
                date(2026, 6, 6),
                dry_run=False,
            )

            self.assertEqual(load_existing_arxiv_ids(root), {"2501.12345"})

    def test_load_existing_arxiv_ids_searches_active_and_archive_frontmatter(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            active = root / "papers" / "2026" / "active.md"
            archived = root / "archive" / "papers" / "2025" / "archived.md"
            body_only = root / "papers" / "2026" / "body-only.md"
            active.parent.mkdir(parents=True)
            archived.parent.mkdir(parents=True)
            active.write_text(
                '---\narxiv_id: "2501.00001"\n---\n',
                encoding="utf-8",
            )
            archived.write_text(
                "---\narxiv_id: hep-ex/0307015\n---\n",
                encoding="utf-8",
            )
            body_only.write_text(
                "---\ntype: note\n---\narxiv_id: \"not-frontmatter\"\n",
                encoding="utf-8",
            )

            self.assertEqual(
                load_existing_arxiv_ids(root),
                {"2501.00001", "hep-ex/0307015"},
            )

    def test_write_paper_note_dry_run_returns_path_without_creating_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "not-created"
            paper = self.make_paper()

            path = write_paper_note(
                root,
                paper,
                self.make_summary(),
                date(2026, 6, 6),
                dry_run=True,
            )

            self.assertEqual(path, paper_note_path(root, paper))
            self.assertFalse(root.exists())
            self.assertFalse(path.exists())

    def test_write_paper_note_adds_numeric_suffix_without_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            paper = self.make_paper()
            intended = paper_note_path(root, paper)
            intended.parent.mkdir(parents=True)
            intended.write_text("original", encoding="utf-8")
            second = intended.with_name(f"{intended.stem} - 2.md")
            second.write_text("second", encoding="utf-8")

            path = write_paper_note(
                root,
                paper,
                self.make_summary(),
                date(2026, 6, 6),
                dry_run=False,
            )

            self.assertEqual(path, intended.with_name(f"{intended.stem} - 3.md"))
            self.assertEqual(intended.read_text(encoding="utf-8"), "original")
            self.assertEqual(second.read_text(encoding="utf-8"), "second")
            self.assertTrue(path.exists())

    def test_write_paper_note_raises_and_cleans_up_temp_file_when_os_link_fails(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            paper = self.make_paper()
            intended = paper_note_path(root, paper)
            intended.parent.mkdir(parents=True)
            intended.write_text("original", encoding="utf-8")
            second = intended.with_name(f"{intended.stem} - 2.md")
            second.write_text("second", encoding="utf-8")
            expected_path = intended.with_name(f"{intended.stem} - 3.md")
            with patch("arxiv_daily.os.link", side_effect=OSError("simulated publish interruption")):
                with self.assertRaisesRegex(OSError, "simulated publish interruption"):
                    write_paper_note(
                        root,
                        paper,
                        self.make_summary(),
                        date(2026, 6, 6),
                        dry_run=False,
                    )

            self.assertEqual(intended.read_text(encoding="utf-8"), "original")
            self.assertEqual(second.read_text(encoding="utf-8"), "second")
            self.assertFalse(expected_path.exists())
            self.assertEqual(list(expected_path.parent.glob("*.tmp")), [])

    def test_yaml_sensitive_values_are_quoted_deterministically(self):
        paper = self.make_paper(
            title='Title: "quoted"\nsecond line',
            authors=["Doe: Jane", 'O"Connor', "Line\nBreak"],
            field="AI: Safety",
            matched_query='ti:"agent" OR value: yes',
        )

        markdown = render_paper_markdown(
            paper,
            self.make_summary(),
            date(2026, 6, 6),
        )
        frontmatter = markdown.split("---\n", 2)[1]

        self.assertEqual(
            authors_yaml(paper.authors),
            '["Doe: Jane", "O\\"Connor", "Line\\nBreak"]',
        )
        self.assertEqual(markdown_bullets(["a", "b"]), "- a\n- b")
        self.assertIn(
            'title: "Title: \\"quoted\\"\\nsecond line"\n',
            frontmatter,
        )
        self.assertIn(
            'authors: ["Doe: Jane", "O\\"Connor", "Line\\nBreak"]\n',
            frontmatter,
        )
        self.assertIn('field: "AI: Safety"\n', frontmatter)
        self.assertIn(
            'matched_query: "ti:\\"agent\\" OR value: yes"\n',
            frontmatter,
        )


class DeepSeekSummaryTests(unittest.TestCase):
    def make_paper(self, **overrides):
        values = {
            "arxiv_id": "2501.12345",
            "title": "A Very Useful Paper",
            "authors": ["Ada Lovelace", "Alan Turing"],
            "published": date(2026, 6, 5),
            "updated": date(2026, 6, 6),
            "abstract": "The original abstract.",
            "url": "https://arxiv.org/abs/2501.12345",
            "pdf_url": "https://arxiv.org/pdf/2501.12345",
            "field": "LLM Agent",
            "matched_query": '"large language model" AND agent',
        }
        values.update(overrides)
        return Paper(**values)

    def make_config(self, **overrides):
        values = {
            "retention_days": 90,
            "per_field_limit": 5,
            "lookback_days": 7,
            "sort_by": "submittedDate",
            "sort_order": "descending",
            "summary_enabled": True,
            "summary_provider": "deepseek",
            "deepseek_model": "deepseek-v4-pro",
            "deepseek_base_url": "https://api.deepseek.com",
            "request_timeout_seconds": 30,
            "fields": [],
        }
        values.update(overrides)
        return Config(**values)

    def test_fallback_summary_uses_abstract_only_status_and_placeholders(self):
        paper = self.make_paper()

        summary = fallback_summary(paper)

        self.assertEqual(summary.status, "abstract_only")
        self.assertIn(paper.abstract, summary.chinese_summary)
        self.assertEqual(
            summary.key_contributions,
            ["暂未生成（使用原始摘要作为备用）"],
        )
        self.assertEqual(
            summary.method_summary,
            "DeepSeek 摘要暂不可用，未提取方法信息。",
        )
        self.assertEqual(
            summary.reading_reason,
            "如需判断价值，请先直接阅读原始摘要。",
        )

    def test_parse_deepseek_summary_accepts_strict_json(self):
        content = json.dumps(
            {
                "chinese_summary": "这篇论文提出了一个简洁的方法。",
                "key_contributions": ["贡献一", "贡献二"],
                "method_summary": "方法概述。",
                "reading_reason": "值得阅读。",
            },
            ensure_ascii=False,
        )

        summary = parse_deepseek_summary(content)

        self.assertEqual(summary.status, "deepseek_generated")
        self.assertEqual(summary.chinese_summary, "这篇论文提出了一个简洁的方法。")
        self.assertEqual(summary.key_contributions, ["贡献一", "贡献二"])
        self.assertEqual(summary.method_summary, "方法概述。")
        self.assertEqual(summary.reading_reason, "值得阅读。")

    def test_parse_deepseek_summary_accepts_json_code_fences(self):
        content = (
            "\n  ```json\n"
            + json.dumps(
                {
                    "chinese_summary": "摘要。",
                    "key_contributions": ["贡献一"],
                    "method_summary": "方法。",
                    "reading_reason": "原因。",
                },
                ensure_ascii=False,
            )
            + "\n```  \n"
        )

        summary = parse_deepseek_summary(content)

        self.assertEqual(summary.status, "deepseek_generated")
        self.assertEqual(summary.key_contributions, ["贡献一"])

    def test_parse_deepseek_summary_rejects_invalid_or_incomplete_json(self):
        cases = [
            '{"chinese_summary": "摘要。", "key_contributions": ["贡献一"], "method_summary": "方法。"}',
            '{"chinese_summary": "", "key_contributions": ["贡献一"], "method_summary": "方法。", "reading_reason": "原因。"}',
            '{"chinese_summary": "摘要。", "key_contributions": [], "method_summary": "方法。", "reading_reason": "原因。"}',
            '{"chinese_summary": "摘要。", "key_contributions": [" "], "method_summary": "方法。", "reading_reason": "原因。"}',
            'not json',
        ]

        for content in cases:
            with self.subTest(content=content):
                with self.assertRaises(ValueError):
                    parse_deepseek_summary(content)

    def test_build_summary_prompt_requests_strict_chinese_json(self):
        paper = self.make_paper()

        prompt = build_summary_prompt(paper)

        self.assertIn(paper.title, prompt)
        self.assertIn(paper.field, prompt)
        self.assertIn("Ada Lovelace", prompt)
        self.assertIn("Alan Turing", prompt)
        self.assertIn(paper.abstract, prompt)
        self.assertIn("请严格只返回 JSON 对象", prompt)
        self.assertIn('"chinese_summary"', prompt)
        self.assertIn('"key_contributions"', prompt)
        self.assertIn('"method_summary"', prompt)
        self.assertIn('"reading_reason"', prompt)

    @patch("arxiv_daily.urllib.request.urlopen")
    def test_summarize_with_deepseek_posts_expected_json(self, urlopen):
        response = urlopen.return_value.__enter__.return_value
        response.read.return_value = json.dumps(
            {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "chinese_summary": "摘要。",
                                    "key_contributions": ["贡献一"],
                                    "method_summary": "方法。",
                                    "reading_reason": "原因。",
                                },
                                ensure_ascii=False,
                            )
                        }
                    }
                ]
            },
            ensure_ascii=False,
        ).encode("utf-8")
        config = self.make_config(
            deepseek_base_url="https://api.deepseek.com/",
            request_timeout_seconds=45,
        )
        paper = self.make_paper()

        summary = summarize_with_deepseek(config, paper, "sk-test-key")

        request = urlopen.call_args.args[0]
        request_body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(
            request.full_url,
            "https://api.deepseek.com/chat/completions",
        )
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request_body["model"], "deepseek-v4-pro")
        self.assertEqual(request_body["temperature"], 0.2)
        self.assertEqual(
            request_body["response_format"],
            {"type": "json_object"},
        )
        self.assertEqual(len(request_body["messages"]), 2)
        self.assertIn(paper.title, request_body["messages"][1]["content"])
        self.assertEqual(request.get_header("Authorization"), "Bearer sk-test-key")
        self.assertEqual(
            request.get_header("Content-type"),
            "application/json",
        )
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 45)
        self.assertEqual(summary.status, "deepseek_generated")

    def test_summarize_with_deepseek_rejects_invalid_deepseek_base_url(self):
        paper = self.make_paper()
        invalid_base_urls = [
            "http://api.deepseek.com",
            "https://evil.example.com",
            "https://user:pass@api.deepseek.com",
            "https://api.deepseek.com?token=leak",
        ]

        for base_url in invalid_base_urls:
            with self.subTest(base_url=base_url):
                config = self.make_config(deepseek_base_url=base_url)
                with patch("arxiv_daily.urllib.request.urlopen") as urlopen:
                    with self.assertRaisesRegex(ValueError, "Invalid DeepSeek base URL"):
                        summarize_with_deepseek(config, paper, "sk-test-key")
                urlopen.assert_not_called()

    @patch("arxiv_daily.urllib.request.urlopen")
    def test_summarize_with_deepseek_rejects_malformed_response_schema(self, urlopen):
        paper = self.make_paper()
        config = self.make_config()
        malformed_payloads = [
            {},
            {"choices": []},
            {"choices": [{}]},
            {"choices": [{"message": {}}]},
            {"choices": [{"message": {"content": ""}}]},
        ]

        for payload in malformed_payloads:
            with self.subTest(payload=payload):
                response = urlopen.return_value.__enter__.return_value
                response.read.return_value = json.dumps(
                    payload,
                    ensure_ascii=False,
                ).encode("utf-8")
                with self.assertRaisesRegex(
                    ValueError,
                    "Invalid DeepSeek response schema",
                ):
                    summarize_with_deepseek(config, paper, "sk-test-key")

    @patch("arxiv_daily.urllib.request.urlopen")
    def test_summarize_paper_falls_back_on_malformed_deepseek_response(self, urlopen):
        paper = self.make_paper()
        config = self.make_config()
        response = urlopen.return_value.__enter__.return_value
        response.read.return_value = json.dumps(
            {"choices": []},
            ensure_ascii=False,
        ).encode("utf-8")

        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "sk-test"}, clear=True):
            self.assertEqual(summarize_paper(config, paper), fallback_summary(paper))

    def test_summarize_paper_returns_fallback_for_disabled_env_missing_and_errors(self):
        paper = self.make_paper()
        config = self.make_config(summary_enabled=False)

        self.assertEqual(summarize_paper(config, paper), fallback_summary(paper))

        config = self.make_config(summary_enabled=True)
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(summarize_paper(config, paper), fallback_summary(paper))

        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "sk-test"}, clear=True):
            with patch(
                "arxiv_daily.summarize_with_deepseek",
                side_effect=RuntimeError("network or parse problem"),
            ):
                self.assertEqual(
                    summarize_paper(config, paper),
                    fallback_summary(paper),
                )

    def test_summarize_paper_uses_only_deepseek_api_key_on_success(self):
        paper = self.make_paper()
        config = self.make_config()
        generated = Summary(
            status="deepseek_generated",
            chinese_summary="生成摘要。",
            key_contributions=["贡献一"],
            method_summary="方法。",
            reading_reason="原因。",
        )

        with patch.dict(
            os.environ,
            {
                "DEEPSEEK_API_KEY": "sk-test",
                "UNRELATED_SECRET": "ignore-me",
            },
            clear=True,
        ):
            with patch(
                "arxiv_daily.summarize_with_deepseek",
                return_value=generated,
            ) as summarize:
                result = summarize_paper(config, paper)

        summarize.assert_called_once_with(config, paper, "sk-test")
        self.assertEqual(result, generated)


class ArchiveAndDailySummaryTests(unittest.TestCase):
    def make_paper(self, **overrides):
        values = {
            "arxiv_id": "2501.12345",
            "title": "A Very Useful Paper",
            "authors": ["Ada Lovelace", "Alan Turing"],
            "published": date(2026, 3, 1),
            "updated": date(2026, 6, 6),
            "abstract": "The original abstract.",
            "url": "https://arxiv.org/abs/2501.12345",
            "pdf_url": "https://arxiv.org/pdf/2501.12345",
            "field": "LLM Agent",
            "matched_query": '"large language model" AND agent',
        }
        values.update(overrides)
        return Paper(**values)

    def make_summary(self, chinese_summary="这是中文摘要。", index=1):
        return Summary(
            status="generated",
            chinese_summary=chinese_summary,
            key_contributions=[f"贡献{index}"],
            method_summary=f"方法{index}。",
            reading_reason=f"阅读原因{index}。",
        )

    def project_link(self, root: Path, path: Path) -> str:
        return vault_wikilink(Path(root.name) / path.relative_to(root))

    def write_frontmatter_note(
        self,
        path: Path,
        *,
        arxiv_id: str | None = None,
        published: str | None,
        archived: str | None,
        body: str = "Test body",
        title: str = "Test Paper",
    ) -> None:
        lines = [
            "---",
            f'title: "{title}"',
        ]
        if arxiv_id is not None:
            lines.append(f'arxiv_id: "{arxiv_id}"')
        if published is not None:
            lines.append(f"published: {published}")
        if archived is not None:
            lines.append(f"archived: {archived}")
        lines.extend(["---", body])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def create_symlink(
        self,
        target: Path,
        link_path: Path,
        *,
        target_is_directory: bool = False,
    ) -> None:
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks are not supported on this platform")
        try:
            os.symlink(
                target,
                link_path,
                target_is_directory=target_is_directory,
            )
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink creation is unavailable: {exc}")

    def create_directory_redirection(self, target: Path, link_path: Path) -> None:
        target.mkdir(parents=True, exist_ok=True)
        link_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.create_symlink(target, link_path, target_is_directory=True)
            return
        except unittest.SkipTest:
            pass

        if os.name != "nt":
            self.skipTest("directory junction fallback is Windows-only")

        result = subprocess.run(
            [
                "cmd",
                "/c",
                "mklink",
                "/J",
                str(link_path.resolve(strict=False)),
                str(target.resolve(strict=False)),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            self.skipTest(
                f"directory junction creation is unavailable: {result.stderr or result.stdout}"
            )

    def remove_directory_link(self, link_path: Path) -> None:
        if not link_path.exists() and not link_path.is_symlink():
            return
        if link_path.is_symlink():
            link_path.unlink(missing_ok=True)
            return
        try:
            os.rmdir(link_path)
        except OSError:
            if link_path.is_symlink():
                link_path.unlink(missing_ok=True)
            else:
                raise

    def test_read_frontmatter_value_only_reads_first_frontmatter_block(self):
        text = (
            "---\n"
            'title: "Quoted Value"\n'
            "field: LLM Agent\n"
            "published: 2026-03-01\n"
            "---\n"
            "body title: body value\n"
            "field: body value\n"
        )

        self.assertEqual(read_frontmatter_value(text, "title"), "Quoted Value")
        self.assertEqual(read_frontmatter_value(text, "field"), "LLM Agent")
        self.assertEqual(read_frontmatter_value(text, "published"), "2026-03-01")
        self.assertIsNone(read_frontmatter_value(text, "body title"))

    def test_archive_old_papers_moves_and_updates_archived_flag_preserving_body(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            source = root / "papers" / "2026" / "old-paper.md"
            self.write_frontmatter_note(
                source,
                published=(today - timedelta(days=91)).isoformat(),
                archived="false",
                body="Line 1\nLine 2",
            )

            destinations = archive_old_papers(
                root,
                retention_days=90,
                today=today,
                dry_run=False,
            )

            expected = root / "archive" / "papers" / "2026" / "old-paper.md"
            self.assertEqual(destinations, [expected])
            self.assertFalse(source.exists())
            self.assertTrue(expected.exists())
            content = expected.read_text(encoding="utf-8")
            self.assertIn("archived: true", content)
            self.assertIn("Line 1", content)
            self.assertIn("Line 2", content)
            self.assertIn('title: "Test Paper"', content)

    def test_archive_old_papers_skips_redirected_outside_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            outside_root = Path(temporary_directory) / "outside"
            today = date(2026, 6, 7)
            safe_source = root / "papers" / "2026" / "safe.md"
            outside_dir = outside_root / "papers" / "2026"
            outside_note = outside_dir / "escaped.md"
            outside_link_dir = root / "papers" / "2026" / "escaped-dir"

            self.write_frontmatter_note(
                safe_source,
                published=(today - timedelta(days=91)).isoformat(),
                archived="false",
                body="Safe body",
            )
            self.write_frontmatter_note(
                outside_note,
                published=(today - timedelta(days=91)).isoformat(),
                archived="false",
                body="Outside body",
            )
            outside_dir.mkdir(parents=True, exist_ok=True)
            self.create_directory_redirection(outside_dir, outside_link_dir)
            try:
                destinations = archive_old_papers(
                    root,
                    retention_days=90,
                    today=today,
                    dry_run=False,
                )

                expected = root / "archive" / "papers" / "2026" / "safe.md"
                self.assertEqual(destinations, [expected])
                self.assertTrue(expected.exists())
                self.assertFalse(safe_source.exists())
                self.assertTrue(outside_note.exists())
                self.assertTrue(outside_link_dir.exists())
                self.assertFalse(
                    (root / "archive" / "papers" / "2026" / "escaped-dir").exists()
                )
            finally:
                self.remove_directory_link(outside_link_dir)

    def test_load_existing_arxiv_ids_skips_redirected_outside_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            outside_root = Path(temporary_directory) / "outside"
            today = date(2026, 6, 7)
            inside = root / "papers" / "2026" / "inside.md"
            outside_dir = outside_root / "papers" / "2026"
            outside_note = outside_dir / "escaped.md"
            outside_link_dir = root / "papers" / "2026" / "escaped-dir"
            archive_note = root / "archive" / "papers" / "2025" / "archive.md"

            self.write_frontmatter_note(
                inside,
                arxiv_id="2501.12345",
                published=(today - timedelta(days=1)).isoformat(),
                archived="false",
                body="Inside body",
            )
            self.write_frontmatter_note(
                outside_note,
                arxiv_id="2501.99999",
                published=(today - timedelta(days=1)).isoformat(),
                archived="false",
                body="Outside body",
            )
            self.write_frontmatter_note(
                archive_note,
                arxiv_id="2501.00002",
                published=(today - timedelta(days=120)).isoformat(),
                archived="true",
                body="Archive body",
            )
            outside_dir.mkdir(parents=True, exist_ok=True)
            self.create_directory_redirection(outside_dir, outside_link_dir)
            try:
                self.assertEqual(
                    load_existing_arxiv_ids(root),
                    {"2501.12345", "2501.00002"},
                )
            finally:
                self.remove_directory_link(outside_link_dir)

    def test_archive_old_papers_skips_exactly_90_days_and_archives_91_days(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            exact_90 = root / "papers" / "2026" / "exact-90.md"
            over_91 = root / "papers" / "2026" / "over-91.md"
            self.write_frontmatter_note(
                exact_90,
                published=(today - timedelta(days=90)).isoformat(),
                archived="false",
                body="Exact 90",
            )
            self.write_frontmatter_note(
                over_91,
                published=(today - timedelta(days=91)).isoformat(),
                archived="false",
                body="Over 91",
            )

            destinations = archive_old_papers(
                root,
                retention_days=90,
                today=today,
                dry_run=False,
            )

            expected = root / "archive" / "papers" / "2026" / "over-91.md"
            self.assertEqual(destinations, [expected])
            self.assertTrue(exact_90.exists())
            self.assertFalse(over_91.exists())
            self.assertTrue(expected.exists())
            self.assertIn("Exact 90", exact_90.read_text(encoding="utf-8"))
            self.assertIn("archived: true", expected.read_text(encoding="utf-8"))

    def test_archive_old_papers_leaves_invalid_or_already_archived_notes_untouched(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            invalid = root / "papers" / "2026" / "invalid.md"
            archived = root / "papers" / "2026" / "archived.md"
            self.write_frontmatter_note(
                invalid,
                published="not-a-date",
                archived="false",
                body="Invalid date",
            )
            self.write_frontmatter_note(
                archived,
                published=(today - timedelta(days=120)).isoformat(),
                archived="true",
                body="Already archived",
            )

            destinations = archive_old_papers(
                root,
                retention_days=90,
                today=today,
                dry_run=False,
            )

            self.assertEqual(destinations, [])
            self.assertTrue(invalid.exists())
            self.assertTrue(archived.exists())
            self.assertIn("Invalid date", invalid.read_text(encoding="utf-8"))
            self.assertIn("archived: true", archived.read_text(encoding="utf-8"))

    def test_archive_old_papers_dry_run_returns_destinations_without_touching_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            source = root / "papers" / "2026" / "dry-run.md"
            self.write_frontmatter_note(
                source,
                published=(today - timedelta(days=91)).isoformat(),
                archived="false",
                body="Dry run body",
            )

            destinations = archive_old_papers(
                root,
                retention_days=90,
                today=today,
                dry_run=True,
            )

            expected = root / "archive" / "papers" / "2026" / "dry-run.md"
            self.assertEqual(destinations, [expected])
            self.assertTrue(source.exists())
            self.assertFalse(expected.exists())
            self.assertIn("archived: false", source.read_text(encoding="utf-8"))

    def test_archive_old_papers_uses_numeric_suffix_without_overwriting_existing_archive_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            source = root / "papers" / "2026" / "collision.md"
            self.write_frontmatter_note(
                source,
                published=(today - timedelta(days=91)).isoformat(),
                archived="false",
                body="Collision body",
            )
            expected = root / "archive" / "papers" / "2026" / "collision.md"
            expected.parent.mkdir(parents=True, exist_ok=True)
            expected.write_text("existing", encoding="utf-8")
            expected_suffix_2 = expected.with_name("collision - 2.md")
            expected_suffix_2.write_text("existing-2", encoding="utf-8")

            destinations = archive_old_papers(
                root,
                retention_days=90,
                today=today,
                dry_run=False,
            )

            expected_suffix_3 = expected.with_name("collision - 3.md")
            self.assertEqual(destinations, [expected_suffix_3])
            self.assertTrue(expected.exists())
            self.assertTrue(expected_suffix_2.exists())
            self.assertTrue(expected_suffix_3.exists())
            self.assertFalse(source.exists())
            self.assertIn("archived: true", expected_suffix_3.read_text(encoding="utf-8"))
            self.assertIn("existing", expected.read_text(encoding="utf-8"))
            self.assertIn("existing-2", expected_suffix_2.read_text(encoding="utf-8"))

    def test_archive_old_papers_cleans_temp_and_rolls_back_if_rewrite_fails(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            source = root / "papers" / "2026" / "failure.md"
            self.write_frontmatter_note(
                source,
                published=(today - timedelta(days=91)).isoformat(),
                archived="false",
                body="Failure body",
            )

            with patch(
                "arxiv_daily.os.replace",
                side_effect=OSError("simulated rewrite failure"),
            ):
                with self.assertRaisesRegex(
                    OSError,
                    "simulated rewrite failure",
                ):
                    archive_old_papers(
                        root,
                        retention_days=90,
                        today=today,
                        dry_run=False,
                    )

            self.assertTrue(source.exists())
            self.assertIn("Failure body", source.read_text(encoding="utf-8"))
            self.assertFalse((root / "archive" / "papers" / "2026" / "failure.md").exists())
            self.assertEqual(
                list((root / "archive" / "papers" / "2026").glob("*.tmp")),
                [],
            )

    def test_write_paper_note_rejects_redirected_output_path(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            outside_root = Path(temporary_directory) / "outside"
            paper = self.make_paper(
                arxiv_id="2501.54321",
                published=date(2026, 6, 7),
            )
            redirect_dir = root / "papers" / "2026"
            outside_dir = outside_root / "paper-out"
            self.create_directory_redirection(outside_dir, redirect_dir)
            try:
                with self.assertRaises(ValueError):
                    write_paper_note(
                        root,
                        paper,
                        self.make_summary("Test summary", 1),
                        date(2026, 6, 7),
                        dry_run=False,
                    )
                self.assertFalse((outside_dir / paper_note_path(root, paper).name).exists())
            finally:
                self.remove_directory_link(redirect_dir)

    def test_archive_old_papers_rejects_redirected_output_path_and_keeps_source(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            outside_root = Path(temporary_directory) / "outside"
            today = date(2026, 6, 7)
            source = root / "papers" / "2026" / "archive-me.md"
            self.write_frontmatter_note(
                source,
                arxiv_id="2501.77777",
                published=(today - timedelta(days=91)).isoformat(),
                archived="false",
                body="Archive body",
            )
            redirect_dir = root / "archive" / "papers" / "2026"
            outside_dir = outside_root / "archive-out"
            self.create_directory_redirection(outside_dir, redirect_dir)
            try:
                with self.assertRaises(ValueError):
                    archive_old_papers(
                        root,
                        retention_days=90,
                        today=today,
                        dry_run=False,
                    )
                self.assertTrue(source.exists())
                self.assertFalse((outside_dir / source.name).exists())
            finally:
                self.remove_directory_link(redirect_dir)

    def test_write_daily_summary_rejects_redirected_output_path(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            outside_root = Path(temporary_directory) / "outside"
            today = date(2026, 6, 7)
            paper = self.make_paper(
                arxiv_id="2501.88888",
                published=today,
            )
            redirect_dir = root / "daily"
            outside_dir = outside_root / "daily-out"
            self.create_directory_redirection(outside_dir, redirect_dir)
            try:
                with self.assertRaises(ValueError):
                    write_daily_summary(
                        root,
                        today,
                        [(paper, paper_note_path(root, paper), self.make_summary("Test summary", 1))],
                        [],
                        dry_run=False,
                    )
                self.assertFalse((outside_dir / f"{today.isoformat()}.md").exists())
            finally:
                self.remove_directory_link(redirect_dir)

    def test_vault_wikilink_formats_vault_relative_path(self):
        self.assertEqual(
            vault_wikilink(Path("/daily/2026-06-07.md")),
            "[[daily/2026-06-07.md]]",
        )

    def test_write_daily_summary_creates_report_with_counts_sections_and_links(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            items: list[tuple[Paper, Path, Summary]] = []
            papers = [
                self.make_paper(
                    arxiv_id="2501.00001",
                    title="Agent One",
                    field="LLM Agent",
                    published=date(2026, 6, 7),
                ),
                self.make_paper(
                    arxiv_id="2501.00002",
                    title="Safety Two",
                    field="AI Safety",
                    published=date(2026, 6, 7),
                ),
                self.make_paper(
                    arxiv_id="2501.00003",
                    title="Agent Three",
                    field="LLM Agent",
                    published=date(2026, 6, 7),
                ),
                self.make_paper(
                    arxiv_id="2501.00004",
                    title="Multimodal Four",
                    field="Multimodal",
                    published=date(2026, 6, 7),
                ),
                self.make_paper(
                    arxiv_id="2501.00005",
                    title="Agent Five",
                    field="LLM Agent",
                    published=date(2026, 6, 7),
                ),
                self.make_paper(
                    arxiv_id="2501.00006",
                    title="Safety Six",
                    field="AI Safety",
                    published=date(2026, 6, 7),
                ),
            ]
            summaries = [
                self.make_summary("第一篇中文摘要。", 1),
                self.make_summary("第二篇中文摘要。", 2),
                self.make_summary("第三篇中文摘要。", 3),
                self.make_summary("第四篇中文摘要。", 4),
                self.make_summary("第五篇中文摘要。", 5),
                self.make_summary("第六篇中文摘要。", 6),
            ]
            for paper, summary in zip(papers, summaries):
                items.append((paper, paper_note_path(root, paper), summary))

            archived_paths = [
                root / "archive" / "papers" / "2025" / "2025-01-01 - Old One.md",
                root / "archive" / "papers" / "2025" / "2025-01-02 - Old Two.md",
            ]

            path = write_daily_summary(
                root,
                today,
                items,
                archived_paths,
                dry_run=False,
            )

            content = path.read_text(encoding="utf-8")
            priority_block = content.split("## 优先阅读", 1)[1].split("## 分领域论文", 1)[0]

            self.assertEqual(path, root / "daily" / "2026-06-07.md")
            self.assertIn("每日 arXiv 论文速报 - 2026-06-07", content)
            self.assertIn("新增论文总数：6", content)
            self.assertIn("今日归档：2", content)
            self.assertIn("LLM Agent：3", content)
            self.assertIn("AI Safety：2", content)
            self.assertIn("Multimodal：1", content)
            self.assertIn("运行时间：", content)
            self.assertIn("日志：[[arxiv-daily/logs/2026-06-07.log]]", content)
            self.assertIn(self.project_link(root, items[0][1]), content)
            self.assertIn(self.project_link(root, items[5][1]), content)
            self.assertIn(self.project_link(root, archived_paths[0]), content)
            self.assertIn(self.project_link(root, archived_paths[1]), content)
            self.assertIn("第一篇中文摘要。", content)
            self.assertIn("第六篇中文摘要。", content)
            self.assertIn("Agent One", priority_block)
            self.assertIn("Safety Two", priority_block)
            self.assertIn("Agent Three", priority_block)
            self.assertIn("Multimodal Four", priority_block)
            self.assertIn("Agent Five", priority_block)
            self.assertNotIn("Safety Six", priority_block)
            self.assertLess(
                content.index("### LLM Agent（3）"),
                content.index("### AI Safety（2）"),
            )
            self.assertLess(
                content.index("### AI Safety（2）"),
                content.index("### Multimodal（1）"),
            )

    def test_write_daily_summary_zero_new_day_is_still_useful(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)

            path = write_daily_summary(
                root,
                today,
                [],
                [],
                dry_run=False,
            )

            content = path.read_text(encoding="utf-8")

            self.assertIn("新增论文总数：0", content)
            self.assertIn("今日没有新增论文", content)
            self.assertIn("今日归档：0", content)
            self.assertIn("日志：[[arxiv-daily/logs/2026-06-07.log]]", content)

    def test_write_daily_summary_preserves_existing_report_on_no_op_run(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            path = root / "daily" / "2026-06-07.md"
            existing_content = "# Existing daily report\n\n- Keep this paper\n"
            path.parent.mkdir(parents=True)
            path.write_text(existing_content, encoding="utf-8")

            result = write_daily_summary(
                root,
                today,
                [],
                [],
                dry_run=False,
            )

            self.assertEqual(result, path)
            self.assertEqual(path.read_text(encoding="utf-8"), existing_content)

    def test_write_daily_summary_keeps_and_deduplicates_same_day_archive_links(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            earlier_archive = (
                root / "archive" / "papers" / "2025" / "Earlier.md"
            )
            later_archive = (
                root / "archive" / "papers" / "2025" / "Later.md"
            )

            path = write_daily_summary(
                root,
                today,
                [],
                [earlier_archive],
                dry_run=False,
            )
            write_daily_summary(
                root,
                today,
                [],
                [later_archive, later_archive],
                dry_run=False,
            )

            content = path.read_text(encoding="utf-8")
            archive_section = content.split("## 今日归档", 1)[1].split(
                "## 运行信息",
                1,
            )[0]

            self.assertIn("今日归档：2", content)
            self.assertEqual(
                archive_section.count(self.project_link(root, earlier_archive)),
                1,
            )
            self.assertEqual(
                archive_section.count(self.project_link(root, later_archive)),
                1,
            )

    def test_merge_daily_items_prefers_stored_final_path_for_same_arxiv_id(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            paper = self.make_paper(
                arxiv_id="2501.99999",
                published=date(2026, 6, 7),
            )
            summary = self.make_summary("Final path summary", 1)
            active_path = root / "papers" / "2026" / "paper.md"
            archived_path = root / "archive" / "papers" / "2026" / "paper.md"

            merged = arxiv_daily._merge_daily_items(
                [(paper, archived_path, summary)],
                [(paper, active_path, summary)],
            )

            self.assertEqual(merged, [(paper, archived_path, summary)])

    def test_write_daily_summary_dry_run_does_not_write_file(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)

            path = write_daily_summary(
                root,
                today,
                [],
                [],
                dry_run=True,
            )

            self.assertEqual(path, root / "daily" / "2026-06-07.md")
            self.assertFalse(path.exists())
            self.assertFalse((root / "daily").exists())

    def test_write_daily_summary_overwrites_same_date_atomically_without_suffixes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            today = date(2026, 6, 7)
            first_paper = self.make_paper(
                arxiv_id="2501.10001",
                title="First Draft",
                field="LLM Agent",
                published=date(2026, 6, 7),
            )
            second_paper = self.make_paper(
                arxiv_id="2501.10002",
                title="Second Draft",
                field="AI Safety",
                published=date(2026, 6, 7),
            )
            first_items = [
                (first_paper, paper_note_path(root, first_paper), self.make_summary("第一次日报。", 1)),
            ]
            second_items = [
                (second_paper, paper_note_path(root, second_paper), self.make_summary("第二次日报。", 2)),
            ]

            first_path = write_daily_summary(
                root,
                today,
                first_items,
                [],
                dry_run=False,
            )
            first_content = first_path.read_text(encoding="utf-8")

            second_path = write_daily_summary(
                root,
                today,
                second_items,
                [],
                dry_run=False,
            )
            second_content = second_path.read_text(encoding="utf-8")

            self.assertEqual(first_path, second_path)
            self.assertIn("First Draft", first_content)
            self.assertIn("Second Draft", second_content)
            self.assertEqual(
                list((root / "daily").glob("2026-06-07*.md")),
                [second_path],
            )

            with patch("arxiv_daily.os.replace", side_effect=OSError("simulated replace failure")):
                with self.assertRaisesRegex(OSError, "simulated replace failure"):
                    write_daily_summary(
                        root,
                        today,
                        first_items,
                        [],
                        dry_run=False,
                    )

            self.assertEqual(second_path.read_text(encoding="utf-8"), second_content)
            self.assertEqual(list((root / "daily").glob("*.tmp")), [])


class RunOrchestrationTests(unittest.TestCase):
    def make_config(self, fields):
        return Config(
            retention_days=90,
            per_field_limit=5,
            lookback_days=7,
            sort_by="submittedDate",
            sort_order="descending",
            summary_enabled=True,
            summary_provider="deepseek",
            deepseek_model="deepseek-v4-pro",
            deepseek_base_url="https://api.deepseek.com",
            request_timeout_seconds=30,
            fields=fields,
        )

    def make_paper(self, arxiv_id: str, field: str, updated: date, **overrides):
        values = {
            "arxiv_id": arxiv_id,
            "title": f"{field} {arxiv_id}",
            "authors": ["Ada Lovelace"],
            "published": date(2026, 6, 1),
            "updated": updated,
            "abstract": f"Abstract for {arxiv_id}.",
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
            "field": field,
            "matched_query": f"query-{field}",
        }
        values.update(overrides)
        return Paper(**values)

    def make_summary(self, paper: Paper) -> Summary:
        return Summary(
            status="generated",
            chinese_summary=f"{paper.arxiv_id} summary",
            key_contributions=[f"{paper.arxiv_id} contribution"],
            method_summary=f"{paper.arxiv_id} method",
            reading_reason=f"{paper.arxiv_id} reason",
        )

    def test_run_happy_path_fetches_dedups_processes_archives_and_writes_daily(self):
        fields = [
            FieldConfig(name="Agents", query="agents"),
            FieldConfig(name="Safety", query="safety"),
            FieldConfig(name="Vision", query="vision"),
        ]
        config = self.make_config(fields)
        today = date(2026, 6, 8)
        existing_id = "2501.00001"
        agents_new_a = self.make_paper("2501.00003", "Agents", date(2026, 6, 7))
        agents_new_b = self.make_paper("2501.00004", "Agents", date(2026, 6, 7))
        agents_overlap = self.make_paper("2501.00002", "Agents", date(2026, 6, 6))
        safety_overlap = self.make_paper("2501.00002", "Safety", date(2026, 6, 8))
        safety_new = self.make_paper("2501.00005", "Safety", date(2026, 6, 5))
        vision_new = self.make_paper("2501.00006", "Vision", date(2026, 6, 4))
        expected_order = [
            agents_new_a,
            agents_new_b,
            agents_overlap,
            safety_new,
            vision_new,
        ]

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()
            archived_paths = [root / "archive" / "papers" / "2025" / "old.md"]

            with patch("arxiv_daily.parse_config", return_value=config) as parse_mock, patch(
                "arxiv_daily.load_existing_arxiv_ids",
                return_value={existing_id},
            ) as existing_mock, patch(
                "arxiv_daily.fetch_arxiv_papers",
                side_effect=[
                    [
                        self.make_paper(existing_id, "Agents", date(2026, 6, 8)),
                        agents_overlap,
                        agents_new_b,
                        agents_new_a,
                    ],
                    [safety_overlap, safety_new],
                    [vision_new],
                ],
            ) as fetch_mock, patch(
                "arxiv_daily.summarize_paper",
                side_effect=lambda cfg, paper: self.make_summary(paper),
            ) as summarize_mock, patch(
                "arxiv_daily.write_paper_note",
                side_effect=lambda output_root, paper, summary, current_day, dry_run: (
                    output_root / "papers" / f"{paper.arxiv_id}.md"
                ),
            ) as write_note_mock, patch(
                "arxiv_daily.archive_old_papers",
                return_value=archived_paths,
            ) as archive_mock, patch(
                "arxiv_daily.write_daily_summary",
                return_value=root / "daily" / f"{today.isoformat()}.md",
            ) as daily_mock, patch(
                "arxiv_daily.log_line"
            ) as log_mock, patch(
                "arxiv_daily.time",
                create=True,
            ) as time_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                result = run(root)

        self.assertEqual(result, 0)
        parse_mock.assert_called_once_with(root / "config.yaml")
        existing_mock.assert_called_once_with(root)
        self.assertEqual(
            fetch_mock.call_args_list,
            [call(config, field) for field in fields],
        )
        self.assertEqual(
            [mock_call.args[1] for mock_call in summarize_mock.call_args_list],
            expected_order,
        )
        self.assertNotIn(call(config, safety_overlap), summarize_mock.call_args_list)
        self.assertEqual(
            [mock_call.args[1] for mock_call in write_note_mock.call_args_list],
            expected_order,
        )
        archive_mock.assert_called_once_with(
            root,
            config.retention_days,
            today,
            dry_run=False,
        )
        daily_items = daily_mock.call_args.kwargs["new_items"]
        self.assertEqual(
            [paper.arxiv_id for paper, _, _ in daily_items],
            [paper.arxiv_id for paper in expected_order],
        )
        self.assertEqual(
            daily_mock.call_args.kwargs["archived_paths"],
            archived_paths,
        )
        self.assertFalse(daily_mock.call_args.kwargs["dry_run"])
        time_mock.sleep.assert_has_calls([call(3), call(3)])
        self.assertEqual(time_mock.sleep.call_count, 2)
        self.assertGreaterEqual(log_mock.call_count, 2)

    def test_run_same_day_incremental_rerun_keeps_earlier_and_new_papers_and_current_archives(
        self,
    ):
        fields = [FieldConfig(name="Agents", query="agents")]
        config = self.make_config(fields)
        today = date(2026, 6, 8)
        earlier = self.make_paper(
            "2501.00001",
            "Agents",
            date(2026, 6, 8),
            title="Earlier Paper",
        )
        later = self.make_paper(
            "2501.00002",
            "Agents",
            date(2026, 6, 8),
            title="Later Paper",
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()
            archived_path = (
                root / "archive" / "papers" / "2025" / "Archived Today.md"
            )

            with patch("arxiv_daily.parse_config", return_value=config), patch(
                "arxiv_daily.fetch_arxiv_papers",
                side_effect=[[earlier], [earlier, later]],
            ), patch(
                "arxiv_daily.summarize_paper",
                side_effect=lambda cfg, paper: self.make_summary(paper),
            ), patch(
                "arxiv_daily.archive_old_papers",
                side_effect=[[], [archived_path]],
            ), patch(
                "arxiv_daily.log_line"
            ), patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                self.assertEqual(run(root), 0)
                self.assertEqual(run(root), 0)

            content = (
                root / "daily" / f"{today.isoformat()}.md"
            ).read_text(encoding="utf-8")

        self.assertIn("Earlier Paper", content)
        self.assertIn("2501.00001 summary", content)
        self.assertIn("Later Paper", content)
        self.assertIn("2501.00002 summary", content)
        self.assertIn("Archived Today.md", content)

    def test_run_logs_safe_deepseek_failure_reason_and_writes_abstract_fallback(
        self,
    ):
        fields = [FieldConfig(name="Agents", query="agents")]
        config = self.make_config(fields)
        today = date(2026, 6, 8)
        paper = self.make_paper(
            "2501.00001",
            "Agents",
            date(2026, 6, 8),
        )
        api_key = "dummy-test-key"

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()

            with patch.dict(
                os.environ,
                {"DEEPSEEK_API_KEY": api_key},
                clear=True,
            ), patch(
                "arxiv_daily.parse_config",
                return_value=config,
            ), patch(
                "arxiv_daily.fetch_arxiv_papers",
                return_value=[paper],
            ), patch(
                "arxiv_daily.summarize_with_deepseek",
                side_effect=RuntimeError("timeout while decoding response"),
            ), patch(
                "arxiv_daily.archive_old_papers",
                return_value=[],
            ), patch(
                "arxiv_daily.log_line"
            ) as log_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                result = run(root)

            paper_note = next((root / "papers").rglob("*.md"))
            note_content = paper_note.read_text(encoding="utf-8")

        self.assertEqual(result, 0)
        self.assertIn("summary_status: abstract_only", note_content)
        messages = [mock_call.args[2] for mock_call in log_mock.call_args_list]
        self.assertIn(
            (
                "Paper 2501.00001 DeepSeek summary failed: "
                "RuntimeError: timeout while decoding response"
            ),
            messages,
        )
        combined_messages = "\n".join(messages)
        self.assertNotIn(api_key, combined_messages)
        self.assertNotIn("Authorization", combined_messages)
        self.assertNotIn("response body", combined_messages)

    def test_run_applies_max_total_before_processing_and_skips_remaining_fields(self):
        fields = [
            FieldConfig(name="Agents", query="agents"),
            FieldConfig(name="Safety", query="safety"),
            FieldConfig(name="Vision", query="vision"),
        ]
        config = self.make_config(fields)
        today = date(2026, 6, 8)
        agents_new = self.make_paper("2501.00001", "Agents", date(2026, 6, 8))
        safety_new_a = self.make_paper("2501.00002", "Safety", date(2026, 6, 7))
        safety_new_b = self.make_paper("2501.00003", "Safety", date(2026, 6, 6))

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()

            with patch("arxiv_daily.parse_config", return_value=config), patch(
                "arxiv_daily.load_existing_arxiv_ids",
                return_value=set(),
            ), patch(
                "arxiv_daily.fetch_arxiv_papers",
                side_effect=[
                    [agents_new],
                    [safety_new_b, safety_new_a],
                ],
            ) as fetch_mock, patch(
                "arxiv_daily.summarize_paper",
                side_effect=lambda cfg, paper: self.make_summary(paper),
            ) as summarize_mock, patch(
                "arxiv_daily.write_paper_note",
                side_effect=lambda output_root, paper, summary, current_day, dry_run: (
                    output_root / "papers" / f"{paper.arxiv_id}.md"
                ),
            ), patch(
                "arxiv_daily.archive_old_papers",
                return_value=[],
            ), patch(
                "arxiv_daily.write_daily_summary",
                return_value=root / "daily" / f"{today.isoformat()}.md",
            ) as daily_mock, patch(
                "arxiv_daily.log_line"
            ), patch(
                "arxiv_daily.time",
                create=True,
            ) as time_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                result = run(root, max_total=2)

        self.assertEqual(result, 0)
        self.assertEqual(fetch_mock.call_args_list, [call(config, fields[0]), call(config, fields[1])])
        self.assertEqual(
            [mock_call.args[1].arxiv_id for mock_call in summarize_mock.call_args_list],
            ["2501.00001", "2501.00002"],
        )
        self.assertEqual(
            [paper.arxiv_id for paper, _, _ in daily_mock.call_args.kwargs["new_items"]],
            ["2501.00001", "2501.00002"],
        )
        time_mock.sleep.assert_called_once_with(3)

    def test_run_sleeps_between_attempted_field_fetches_including_after_failures(self):
        fields = [
            FieldConfig(name="Agents", query="agents"),
            FieldConfig(name="Safety", query="safety"),
            FieldConfig(name="Vision", query="vision"),
        ]
        config = self.make_config(fields)
        today = date(2026, 6, 8)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()

            with patch("arxiv_daily.parse_config", return_value=config), patch(
                "arxiv_daily.load_existing_arxiv_ids",
                return_value=set(),
            ), patch(
                "arxiv_daily.fetch_arxiv_papers",
                side_effect=[[], RuntimeError("temporary\nfetch failure"), []],
            ) as fetch_mock, patch(
                "arxiv_daily.archive_old_papers",
                return_value=[],
            ), patch(
                "arxiv_daily.write_daily_summary",
                return_value=root / "daily" / f"{today.isoformat()}.md",
            ), patch(
                "arxiv_daily.log_line"
            ), patch(
                "arxiv_daily.time",
                create=True,
            ) as time_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                result = run(root)

        self.assertEqual(result, 0)
        self.assertEqual(fetch_mock.call_args_list, [call(config, field) for field in fields])
        self.assertEqual(arxiv_daily.ARXIV_REQUEST_DELAY_SECONDS, 3)
        self.assertEqual(time_mock.sleep.call_args_list, [call(3), call(3)])

    def test_run_returns_one_without_writing_digest_when_all_field_fetches_fail(self):
        fields = [FieldConfig(name="Agents", query="agents")]
        config = self.make_config(fields)
        today = date(2026, 6, 8)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()
            archived_paths = [root / "archive" / "papers" / "2025" / "old.md"]

            with patch("arxiv_daily.parse_config", return_value=config), patch(
                "arxiv_daily.load_existing_arxiv_ids",
                return_value=set(),
            ), patch(
                "arxiv_daily.fetch_arxiv_papers",
                side_effect=RuntimeError("bad\nxml response"),
            ), patch(
                "arxiv_daily.summarize_paper"
            ) as summarize_mock, patch(
                "arxiv_daily.write_paper_note"
            ) as write_note_mock, patch(
                "arxiv_daily.archive_old_papers",
                return_value=archived_paths,
            ) as archive_mock, patch(
                "arxiv_daily.write_daily_summary",
                return_value=root / "daily" / f"{today.isoformat()}.md",
            ) as daily_mock, patch(
                "arxiv_daily.log_line"
            ) as log_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                result = run(root)

        self.assertEqual(result, 1)
        summarize_mock.assert_not_called()
        write_note_mock.assert_not_called()
        archive_mock.assert_not_called()
        daily_mock.assert_not_called()
        self.assertTrue(
            any(
                mock_call.args[2]
                == "Field Agents fetch failed: RuntimeError: bad xml response"
                for mock_call in log_mock.call_args_list
            )
        )
        self.assertTrue(
            any(
                mock_call.args[2]
                == "Run failed: all configured arXiv field fetches failed"
                for mock_call in log_mock.call_args_list
            )
        )

    def test_run_continues_after_per_paper_processing_failures_and_excludes_failed_notes(self):
        fields = [FieldConfig(name="Agents", query="agents")]
        config = self.make_config(fields)
        today = date(2026, 6, 8)
        summarize_failure = self.make_paper("2501.00001", "Agents", date(2026, 6, 8))
        write_failure = self.make_paper("2501.00002", "Agents", date(2026, 6, 7))
        success = self.make_paper("2501.00003", "Agents", date(2026, 6, 6))

        def summarize_side_effect(cfg, paper):
            if paper.arxiv_id == "2501.00001":
                raise RuntimeError("llm\nfailure")
            return self.make_summary(paper)

        def write_side_effect(output_root, paper, summary, current_day, dry_run):
            if paper.arxiv_id == "2501.00002":
                raise OSError("disk\nfull")
            return output_root / "papers" / f"{paper.arxiv_id}.md"

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()

            with patch("arxiv_daily.parse_config", return_value=config), patch(
                "arxiv_daily.load_existing_arxiv_ids",
                return_value=set(),
            ), patch(
                "arxiv_daily.fetch_arxiv_papers",
                return_value=[success, summarize_failure, write_failure],
            ), patch(
                "arxiv_daily.summarize_paper",
                side_effect=summarize_side_effect,
            ) as summarize_mock, patch(
                "arxiv_daily.write_paper_note",
                side_effect=write_side_effect,
            ), patch(
                "arxiv_daily.archive_old_papers",
                return_value=[],
            ), patch(
                "arxiv_daily.write_daily_summary",
                return_value=root / "daily" / f"{today.isoformat()}.md",
            ) as daily_mock, patch(
                "arxiv_daily.log_line"
            ) as log_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                result = run(root)

        self.assertEqual(result, 0)
        self.assertEqual(
            [mock_call.args[1].arxiv_id for mock_call in summarize_mock.call_args_list],
            ["2501.00001", "2501.00002", "2501.00003"],
        )
        self.assertEqual(
            [paper.arxiv_id for paper, _, _ in daily_mock.call_args.kwargs["new_items"]],
            ["2501.00003"],
        )
        self.assertTrue(
            any(
                mock_call.args[2]
                == "Paper 2501.00001 processing failed: RuntimeError: llm failure"
                for mock_call in log_mock.call_args_list
            )
        )
        self.assertTrue(
            any(
                mock_call.args[2]
                == "Paper 2501.00002 processing failed: OSError: disk full"
                for mock_call in log_mock.call_args_list
            )
        )

    def test_run_returns_one_and_logs_when_config_parsing_fails(self):
        today = date(2026, 6, 8)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()

            with patch(
                "arxiv_daily.parse_config",
                side_effect=ValueError("bad\nconfig"),
            ), patch("arxiv_daily.log_line") as log_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                result = run(root)

        self.assertEqual(result, 1)
        log_mock.assert_called_once_with(
            root,
            today,
            "Run failed: ValueError: bad config",
        )

    def test_run_returns_one_and_logs_when_daily_summary_write_fails(self):
        fields = [FieldConfig(name="Agents", query="agents")]
        config = self.make_config(fields)
        today = date(2026, 6, 8)
        paper = self.make_paper("2501.00001", "Agents", date(2026, 6, 8))

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()

            with patch("arxiv_daily.parse_config", return_value=config), patch(
                "arxiv_daily.load_existing_arxiv_ids",
                return_value=set(),
            ), patch(
                "arxiv_daily.fetch_arxiv_papers",
                return_value=[paper],
            ), patch(
                "arxiv_daily.summarize_paper",
                return_value=self.make_summary(paper),
            ), patch(
                "arxiv_daily.write_paper_note",
                return_value=root / "papers" / f"{paper.arxiv_id}.md",
            ), patch(
                "arxiv_daily.archive_old_papers",
                return_value=[],
            ), patch(
                "arxiv_daily.write_daily_summary",
                side_effect=RuntimeError("daily\nbroken"),
            ), patch(
                "arxiv_daily.log_line"
            ) as log_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                result = run(root)

        self.assertEqual(result, 1)
        self.assertTrue(
            any(
                mock_call.args[2]
                == "Daily summary failed: RuntimeError: daily broken"
                for mock_call in log_mock.call_args_list
            )
        )

    def test_run_dry_run_selects_and_previews_without_logging_or_writing_files(self):
        fields = [
            FieldConfig(name="Agents", query="agents"),
            FieldConfig(name="Safety", query="safety"),
        ]
        config = self.make_config(fields)
        today = date(2026, 6, 8)
        existing_id = "2501.00001"
        agents_existing = self.make_paper(existing_id, "Agents", date(2026, 6, 8))
        agents_new = self.make_paper(
            "2501.00002",
            "Agents",
            date(2026, 6, 7),
            abstract="PRIVATE_ABSTRACT_MUST_NOT_BE_PRINTED",
        )
        safety_new = self.make_paper("2501.00003", "Safety", date(2026, 6, 6))

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()
            preview_paths = [
                root / "archive" / "papers" / "2025" / "preview-archive.md"
            ]
            stdout = io.StringIO()

            with patch("arxiv_daily.parse_config", return_value=config), patch(
                "arxiv_daily.load_existing_arxiv_ids",
                return_value={existing_id},
            ) as existing_mock, patch(
                "arxiv_daily.fetch_arxiv_papers",
                side_effect=[[agents_existing, agents_new], [safety_new]],
            ) as fetch_mock, patch(
                "arxiv_daily.summarize_paper"
            ) as summarize_mock, patch(
                "arxiv_daily.write_paper_note"
            ) as write_note_mock, patch(
                "arxiv_daily.archive_old_papers",
                return_value=preview_paths,
            ) as archive_mock, patch(
                "arxiv_daily.write_daily_summary",
                return_value=root / "daily" / f"{today.isoformat()}.md",
            ) as daily_mock, patch(
                "arxiv_daily.log_line"
            ) as log_mock, patch(
                "arxiv_daily.time",
                create=True,
            ) as time_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                with redirect_stdout(stdout):
                    result = run(root, dry_run=True, max_total=1)

            self.assertEqual(list(root.rglob("*")), [])
            preview = stdout.getvalue()
            expected_note_path = paper_note_path(root, agents_new).relative_to(root)
            expected_archive_path = preview_paths[0].relative_to(root)

        self.assertEqual(result, 0)
        self.assertIn("Dry run preview", preview)
        self.assertIn("Selected new papers (1)", preview)
        self.assertIn("2501.00002", preview)
        self.assertIn("Agents 2501.00002", preview)
        self.assertIn(expected_note_path.as_posix(), preview)
        self.assertIn("Archive candidates (1)", preview)
        self.assertIn(expected_archive_path.as_posix(), preview)
        self.assertNotIn("2501.00003", preview)
        self.assertNotIn(agents_new.abstract, preview)
        self.assertNotIn("Authorization", preview)
        self.assertNotIn("Bearer", preview)
        self.assertNotIn("DEEPSEEK_API_KEY", preview)
        existing_mock.assert_called_once_with(root)
        self.assertEqual(fetch_mock.call_args_list, [call(config, fields[0])])
        summarize_mock.assert_not_called()
        write_note_mock.assert_not_called()
        log_mock.assert_not_called()
        archive_mock.assert_called_once_with(
            root,
            config.retention_days,
            today,
            dry_run=True,
        )
        daily_mock.assert_called_once_with(
            root,
            today,
            new_items=[],
            archived_paths=preview_paths,
            dry_run=True,
        )
        time_mock.sleep.assert_not_called()

    def test_run_returns_one_without_fetch_when_another_instance_holds_lock(self):
        fields = [FieldConfig(name="Agents", query="agents")]
        config = self.make_config(fields)
        today = date(2026, 6, 8)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()

            with arxiv_daily._single_instance_lock(root):
                with patch("arxiv_daily.parse_config", return_value=config), patch(
                    "arxiv_daily.fetch_arxiv_papers"
                ) as fetch_mock, patch("arxiv_daily.log_line") as log_mock, patch(
                    "arxiv_daily.date"
                ) as date_mock:
                    date_mock.today.return_value = today

                    result = run(root)

        self.assertEqual(result, 1)
        fetch_mock.assert_not_called()
        log_mock.assert_called_once_with(
            root,
            today,
            "Another arXiv daily run is already active",
        )

    def test_run_returns_one_when_single_instance_lock_cannot_be_acquired(self):
        today = date(2026, 6, 8)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()

            with patch(
                "arxiv_daily._single_instance_lock",
                side_effect=PermissionError("lock\npermission denied"),
            ), patch("arxiv_daily.parse_config") as parse_mock, patch(
                "arxiv_daily.log_line"
            ) as log_mock, patch(
                "arxiv_daily.date"
            ) as date_mock:
                date_mock.today.return_value = today

                result = run(root)

        self.assertEqual(result, 1)
        parse_mock.assert_not_called()
        log_mock.assert_called_once_with(
            root,
            today,
            "Run failed: PermissionError: lock permission denied",
        )

    def test_single_instance_lock_releases_after_exception_and_can_be_reacquired(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()
            lock_path = arxiv_daily._lock_file_path(root)

            with self.assertRaisesRegex(RuntimeError, "boom"):
                with arxiv_daily._single_instance_lock(root):
                    self.assertTrue(lock_path.exists())
                    raise RuntimeError("boom")

            with arxiv_daily._single_instance_lock(root):
                self.assertTrue(lock_path.exists())
                self.assertEqual(lock_path.stat().st_size, 1)

    def test_single_instance_lock_uses_posix_fcntl_when_requested(self):
        fake_fcntl = types.SimpleNamespace(
            LOCK_EX=4,
            LOCK_NB=8,
            LOCK_UN=16,
            flock=Mock(),
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            root.mkdir()
            lock_path = arxiv_daily._lock_file_path(root)
            windows_path_cls = type(Path(tempfile.gettempdir()))

            with patch.object(arxiv_daily.os, "name", "posix"), patch.object(
                arxiv_daily,
                "Path",
                windows_path_cls,
            ), patch.dict(sys.modules, {"fcntl": fake_fcntl}, clear=False):
                with arxiv_daily._single_instance_lock(root):
                    self.assertTrue(lock_path.exists())

            self.assertEqual(
                fake_fcntl.flock.call_args_list,
                [
                    call(ANY, fake_fcntl.LOCK_EX | fake_fcntl.LOCK_NB),
                    call(ANY, fake_fcntl.LOCK_UN),
                ],
            )

    def test_main_passes_parsed_arguments_to_run(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "arxiv-daily"
            with patch("arxiv_daily.run", return_value=7) as run_mock:
                result = main(
                    [
                        "--root",
                        str(root),
                        "--dry-run",
                        "--max-total",
                        "2",
                    ]
                )

        self.assertEqual(result, 7)
        run_mock.assert_called_once_with(
            Path(root),
            dry_run=True,
            max_total=2,
        )

    def test_main_uses_parent_of_scripts_directory_by_default(self):
        expected_root = Path(arxiv_daily.__file__).resolve().parent.parent
        with patch("arxiv_daily.run", return_value=0) as run_mock:
            result = main([])

        self.assertEqual(result, 0)
        run_mock.assert_called_once_with(
            expected_root,
            dry_run=False,
            max_total=None,
        )

    def test_main_rejects_non_positive_max_total(self):
        for value in ("0", "-1"):
            with self.subTest(value=value):
                with self.assertRaises(SystemExit) as context:
                    main(["--max-total", value])
                self.assertEqual(context.exception.code, 2)

    def test_main_omits_max_total_as_none(self):
        with patch("arxiv_daily.run", return_value=0) as run_mock:
            result = main(["--root", str(Path(tempfile.gettempdir()) / "arxiv-daily")])

        self.assertEqual(result, 0)
        self.assertIsNone(run_mock.call_args.kwargs["max_total"])

    def test_module_has_main_guard_at_end(self):
        source = Path(arxiv_daily.__file__).read_text(encoding="utf-8").rstrip()
        self.assertTrue(
            source.endswith(
                'if __name__ == "__main__":\n    raise SystemExit(main())'
            )
        )


class ArxivDailyPowerShellWrapperTests(unittest.TestCase):
    def test_power_shell_wrapper_contains_required_tokens_and_no_secrets(self):
        wrapper_path = Path(__file__).with_name("arxiv_daily.ps1")
        source = wrapper_path.read_text(encoding="utf-8")

        required_tokens = [
            "param(",
            "[switch]$DryRun",
            "[int]$MaxTotal = 0",
            "$ErrorActionPreference = 'Stop'",
            "$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path",
            "$ArxivDailyRoot = Resolve-Path (Join-Path $ScriptDir '..')",
            "$PythonScript = Join-Path $ScriptDir 'arxiv_daily.py'",
            "Get-Command python.exe -ErrorAction SilentlyContinue",
            "Get-Command py.exe -ErrorAction SilentlyContinue",
            "$PythonPrefixArgs = @('-3')",
            "throw \"Unable to find python.exe or py.exe on PATH.",
            "$PythonArgs += '--root'",
            "$PythonArgs += $ArxivDailyRoot.Path",
            "if ($DryRun)",
            "$PythonArgs += '--dry-run'",
            "if ($MaxTotal -gt 0)",
            "$PythonArgs += '--max-total'",
            "& $PythonExe @PythonArgs",
            "$exitCode = $LASTEXITCODE",
            "exit $exitCode",
        ]

        for token in required_tokens:
            with self.subTest(token=token):
                self.assertIn(token, source)

        self.assertNotIn("Start-Process", source)
        self.assertNotIn("DEEPSEEK_API_KEY", source)
        self.assertNotIn("Write-Host", source)
        self.assertNotIn("Write-Output", source)


if __name__ == "__main__":
    unittest.main()
