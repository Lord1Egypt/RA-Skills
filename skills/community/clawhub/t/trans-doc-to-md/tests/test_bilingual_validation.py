import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from bilingual_validation_core import (  # noqa: E402
    ValidationError,
    validate_attributed_quotes_are_blockquoted,
    validate_bilingual_source,
    validate_bilingual_list_items_paired,
    validate_document,
    validate_local_images_preserved,
    validate_markdown_structure,
    validate_no_unsafe_tildes,
    validate_toc_categories_attested,
    validate_toc_titles_preserved,
)


class BilingualValidationTests(unittest.TestCase):
    def test_generic_article_without_toc_passes(self) -> None:
        source = (
            "# An Ordinary Article\n\n"
            "This ordinary article has no table of contents and keeps every source paragraph."
        )
        bilingual = (
            "# An Ordinary Article / 一篇普通文章\n\n"
            "This ordinary article has no table of contents and keeps every source paragraph.\n\n"
            "这篇普通文章没有目录，并保留了每一个源文段落。"
        )
        validate_document(source, bilingual)

    def test_accepts_preserved_english_with_chinese_translation(self) -> None:
        source = "# Title\n\nThe first source paragraph contains enough words for validation."
        bilingual = (
            "# Title / 标题\n\n"
            "The first source paragraph contains enough words for validation.\n\n"
            "第一段中文译文。"
        )
        validate_bilingual_source(source, bilingual)

    def test_rejects_missing_source_paragraph(self) -> None:
        source = (
            "# Title\n\n"
            "The first source paragraph contains enough words for validation.\n\n"
            "The second source paragraph must also remain in the translated document."
        )
        bilingual = (
            "# Title / 标题\n\n"
            "The first source paragraph contains enough words for validation.\n\n"
            "第一段中文译文。"
        )
        with self.assertRaises(ValidationError):
            validate_bilingual_source(source, bilingual)

    def test_rejects_missing_local_image(self) -> None:
        source = (
            "A source paragraph with enough words to be checked in full.\n\n"
            "![Original caption](images/chart-one.png)"
        )
        bilingual = (
            "A source paragraph with enough words to be checked in full.\n\n"
            "源文段落的中文译文。"
        )
        with self.assertRaises(ValidationError):
            validate_document(source, bilingual)

    def test_rejects_reordered_local_images(self) -> None:
        source = (
            "A source paragraph with enough words to be checked in full.\n\n"
            "![One](images/one.png)\n\n![Two](images/two.png)"
        )
        bilingual = (
            "A source paragraph with enough words to be checked in full.\n\n"
            "源文段落的中文译文。\n\n"
            "![二](images/two.png)\n\n![一](images/one.png)"
        )
        with self.assertRaises(ValidationError):
            validate_local_images_preserved(source, bilingual)

    def test_accepts_translated_alt_with_same_image_path(self) -> None:
        source = "![Original caption](images/chart.png)"
        bilingual = "![翻译后的图注](images/chart.png)"
        validate_local_images_preserved(source, bilingual)

    def test_section_validation_limits_source_scope(self) -> None:
        source = (
            "# One\n\nA paragraph outside the selected section should not be checked.\n\n"
            "# Two\n\nThe selected section paragraph is preserved in full here."
        )
        bilingual = (
            "# Two / 二\n\nThe selected section paragraph is preserved in full here.\n\n"
            "所选章节的中文译文。"
        )
        validate_bilingual_source(source, bilingual, section="Two")

    def test_accepts_consistent_toc_categories_and_nested_headings(self) -> None:
        markdown = (
            "## Contents / 目录\n\n"
            "- **Section 01 / 第一部分**: Main / 正文 · p.1\n"
            "- **Directory / 名录**: Leadership / 领导团队 · p.2\n\n"
            "# SECTION 01 · Main / 第一部分 · 正文\n\n"
            "## Theme / 主题\n\n"
            "### Discussion / 论述\n"
        )
        validate_markdown_structure(markdown)

    def test_pdf_rich_profile_runs_strict_toc_and_heading_checks(self) -> None:
        source = (
            "## Contents\n\n"
            "- **Section 01**: Main · p.1\n\n"
            "# SECTION 01 · Main\n\n"
            "A complete source paragraph remains available for strict validation."
        )
        bilingual = (
            "## Contents / 目录\n\n"
            "- **Section 01 / 第一部分**: Main / 正文 · p.1\n\n"
            "# SECTION 01 · Main / 正文\n\n"
            "A complete source paragraph remains available for strict validation.\n\n"
            "严格校验仍保留完整的源文段落。"
        )
        validate_document(source, bilingual, profile="pdf-rich")

    def test_pdf_rich_profile_requires_toc(self) -> None:
        source = "# Report\n\nA complete source paragraph is present for validation."
        bilingual = (
            "# Report / 报告\n\n"
            "A complete source paragraph is present for validation.\n\n"
            "这里保留了完整源文段落。"
        )
        with self.assertRaises(ValidationError):
            validate_document(source, bilingual, profile="pdf-rich")

    def test_accepts_toc_item_without_fabricated_category(self) -> None:
        markdown = (
            "## Contents / 目录\n\n"
            "- **Section 01 / 第一部分**: Main / 正文 · p.1\n"
            "- **Leadership / 领导团队** · p.2\n\n"
            "# Main / 正文\n"
        )
        validate_markdown_structure(markdown)

    def test_rejects_malformed_unbolded_toc_item(self) -> None:
        markdown = (
            "## Contents / 目录\n\n"
            "- Leadership / 领导团队 · p.2\n\n"
            "# Main / 正文\n"
        )
        with self.assertRaises(ValidationError):
            validate_markdown_structure(markdown)

    def test_rejects_adjacent_same_level_headings(self) -> None:
        markdown = "## Parent / 父标题\n\n## Child / 子标题\n"
        with self.assertRaises(ValidationError):
            validate_markdown_structure(markdown)

    def test_rejects_truncated_toc_title_without_document_specific_names(self) -> None:
        raw = (
            "# Contents\n\n"
            "7 A Complete Source Title With Its Final Qualifier\n\n"
            '<!-- "type": "page-number", "value": 1 -->\n'
        )
        cleaned = (
            "## Contents\n\n"
            "- **Directory**: A Complete Source Title · p.7\n\n"
            "# SECTION 01 · Body\n"
        )
        with self.assertRaises(ValidationError):
            validate_toc_titles_preserved(raw, cleaned)

    def test_accepts_complete_toc_title_with_added_category_and_translation(self) -> None:
        raw = (
            "# Contents\n\n"
            "7 A Complete Source Title With Its Final Qualifier\n\n"
            '<!-- "type": "page-number", "value": 1 -->\n'
        )
        bilingual = (
            "## Contents / 目录\n\n"
            "- **Directory / 名录**: A Complete Source Title With Its Final Qualifier / 完整标题 · p.7\n\n"
            "# SECTION 01 · Body / 正文\n"
        )
        validate_toc_titles_preserved(raw, bilingual)

    def test_rejects_fabricated_toc_category(self) -> None:
        raw = (
            "# Contents\n\n"
            "7 A Complete Source Title\n\n"
            '<!-- "type": "page-number", "value": 1 -->\n'
        )
        target = (
            "## Contents / 目录\n\n"
            "- **Directory / 名录**: A Complete Source Title / 完整标题 · p.7\n\n"
            "# Main / 正文\n"
        )
        with self.assertRaises(ValidationError):
            validate_toc_categories_attested(raw, target)

    def test_rejects_h1_inside_numbered_chapter(self) -> None:
        markdown = (
            "# Report\n\n"
            "# SECTION 01 · Main\n\n"
            "# A long argumentative heading inside the chapter\n\n"
            "Body text.\n"
        )
        with self.assertRaises(ValidationError):
            validate_markdown_structure(markdown)

    def test_accepts_h2_inside_numbered_chapter(self) -> None:
        markdown = (
            "# Report\n\n"
            "# SECTION 01 · Main\n\n"
            "## A long argumentative heading inside the chapter\n\n"
            "Body text.\n\n"
            "# Endnotes\n"
        )
        validate_markdown_structure(markdown)

    def test_rejects_approximation_tilde_outside_code_and_url(self) -> None:
        with self.assertRaises(ValidationError):
            validate_no_unsafe_tildes("Metric: ~$5tn and ~5%")

    def test_accepts_unicode_approximation_and_ignored_code_tildes(self) -> None:
        validate_no_unsafe_tildes(
            "Metric: ≈$5tn and ≈5%\n\n"
            "`literal ~5`\n\n"
            "```\nvalue = ~5\n```\n"
        )

    def test_rejects_unblocked_quote_with_attribution(self) -> None:
        markdown = (
            "“A complete attributed quotation.”\n\n"
            "Alex Example | Chief Example Officer\n"
        )
        with self.assertRaises(ValidationError):
            validate_attributed_quotes_are_blockquoted(markdown)

    def test_accepts_standard_blockquote_with_attribution(self) -> None:
        markdown = (
            "> “A complete attributed quotation.”\n"
            ">\n"
            "> “一条完整引语。”\n"
            ">\n"
            "> **Alex Example | Chief Example Officer**\n"
        )
        validate_attributed_quotes_are_blockquoted(markdown)

    def test_accepts_list_items_paired_on_one_line(self) -> None:
        validate_bilingual_list_items_paired(
            "- *Tokens are faster than humans.* / *Token 比人类更快。*\n"
            "- Context hoarding / 上下文囤积"
        )

    def test_rejects_stacked_english_then_chinese_list_items(self) -> None:
        markdown = (
            "- *Tokens are faster than humans.*\n"
            "- *Tokens can be trusted.*\n"
            "- *Token 比人类更快。*\n"
            "- *Token 值得信任。*"
        )
        with self.assertRaises(ValidationError):
            validate_bilingual_list_items_paired(markdown)

    def test_cli_json_is_stable_on_success_and_failure(self) -> None:
        script = SCRIPTS / "bilingual_validate.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.md"
            final = root / "final.md"
            source.write_text(
                "A complete source paragraph contains enough words for validation.",
                encoding="utf-8",
            )
            final.write_text(
                "A complete source paragraph contains enough words for validation.\n\n"
                "完整源文段落的中文译文。",
                encoding="utf-8",
            )
            passed = subprocess.run(
                [sys.executable, str(script), str(source), str(final), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(passed.returncode, 0)
            self.assertEqual(
                json.loads(passed.stdout),
                {
                    "error": None,
                    "ok": True,
                    "profile": "generic",
                    "scope": "full document",
                    "status": "pass",
                },
            )

            final.write_text("Only a summary remains.", encoding="utf-8")
            failed = subprocess.run(
                [sys.executable, str(script), str(source), str(final), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(failed.returncode, 1)
            payload = json.loads(failed.stdout)
            self.assertEqual(payload["status"], "fail")
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["profile"], "generic")


if __name__ == "__main__":
    unittest.main()
