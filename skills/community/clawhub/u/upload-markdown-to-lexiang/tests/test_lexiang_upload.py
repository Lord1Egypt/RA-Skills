from argparse import Namespace
from contextlib import redirect_stdout
import io
from pathlib import Path
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import sys

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from lexiang_upload_core import (  # noqa: E402
    PreflightError,
    VerificationError,
    build_plan,
    convert_math,
    demote_caption_headings,
    parse_portable_callouts,
    split_large_gfm_tables,
    verify_remote,
)
from lexiang_upload import (  # noqa: E402
    AuthError,
    DEFAULT_CREDENTIALS,
    PROFILE_CREDENTIALS_DIR,
    CredentialSelector,
    PersonalCredential,
    credentials_path,
    execute_plan,
    latex_to_unicode,
    load_credential,
    materialize_formula_fallback,
    prepend_source_link,
    resolve_credential_selector,
    resolve_source,
    save_credential,
    upload,
    verify_page,
)


class CredentialTests(unittest.TestCase):
    def test_default_profile_preserves_legacy_path(self) -> None:
        selector = resolve_credential_selector(environ={})
        self.assertEqual(selector.profile, "default")
        self.assertEqual(selector.path, DEFAULT_CREDENTIALS)
        self.assertEqual(credentials_path(selector), DEFAULT_CREDENTIALS)

    def test_named_profile_uses_profiles_directory(self) -> None:
        selector = resolve_credential_selector("obsidian-sync", environ={})
        self.assertEqual(selector.profile, "obsidian-sync")
        self.assertEqual(
            selector.path,
            PROFILE_CREDENTIALS_DIR / "obsidian-sync.json",
        )

    def test_explicit_default_profile_uses_legacy_path(self) -> None:
        selector = resolve_credential_selector("default", environ={})
        self.assertEqual(selector.profile, "default")
        self.assertEqual(selector.path, DEFAULT_CREDENTIALS)

    def test_explicit_file_precedes_explicit_profile_and_environment(self) -> None:
        selector = resolve_credential_selector(
            "obsidian-sync",
            "~/chosen.json",
            {
                "LEXIANG_UPLOAD_CREDENTIALS": "/tmp/env-file.json",
                "LEXIANG_UPLOAD_PROFILE": "env-profile",
            },
        )
        self.assertIsNone(selector.profile)
        self.assertEqual(selector.path, Path("~/chosen.json").expanduser())

    def test_environment_file_precedes_environment_profile(self) -> None:
        selector = resolve_credential_selector(
            environ={
                "LEXIANG_UPLOAD_CREDENTIALS": "/tmp/env-file.json",
                "LEXIANG_UPLOAD_PROFILE": "env-profile",
            }
        )
        self.assertIsNone(selector.profile)
        self.assertEqual(selector.path, Path("/tmp/env-file.json"))

    def test_environment_profile_is_used_without_file_override(self) -> None:
        selector = resolve_credential_selector(
            environ={"LEXIANG_UPLOAD_PROFILE": "environment-profile"}
        )
        self.assertEqual(selector.profile, "environment-profile")
        self.assertEqual(
            selector.path,
            PROFILE_CREDENTIALS_DIR / "environment-profile.json",
        )

    def test_explicit_profile_precedes_environment_file(self) -> None:
        selector = resolve_credential_selector(
            "explicit",
            environ={"LEXIANG_UPLOAD_CREDENTIALS": "/tmp/env-file.json"},
        )
        self.assertEqual(selector.profile, "explicit")
        self.assertEqual(selector.path, PROFILE_CREDENTIALS_DIR / "explicit.json")

    def test_rejects_unsafe_profiles(self) -> None:
        for profile in ("../escape", "nested/profile", "white space", ""):
            with self.subTest(profile=profile), self.assertRaises(AuthError):
                resolve_credential_selector(profile, environ={})

    def test_personal_credential_accepts_page_field_names(self) -> None:
        credential = PersonalCredential.from_dict(
            {
                "access_token": "lxmcp_test_token",
                "mcp_company_from": "company",
            }
        )
        credential.validate_shape()
        self.assertEqual(credential.mcp_token, "lxmcp_test_token")

    def test_personal_credential_accepts_nested_export(self) -> None:
        credential = PersonalCredential.from_dict(
            {
                "mcp": {
                    "mcp_token": "lxmcp_test_token",
                    "company_from": "company",
                }
            }
        )
        credential.validate_shape()
        self.assertEqual(credential.mcp_token, "lxmcp_test_token")

    def test_personal_credential_parses_copied_install_command(self) -> None:
        credential = PersonalCredential.from_text(
            'url="https://mcp.lexiang-app.com/mcp?company_from=csig" '
            'Authorization="Bearer lxmcp_test_token"'
        )
        credential.validate_shape()
        self.assertEqual(credential.company_from, "csig")
        self.assertEqual(credential.mcp_token, "lxmcp_test_token")

    def test_credential_is_saved_outside_skill_with_private_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "credentials.json"
            with patch.dict(os.environ, {"LEXIANG_UPLOAD_CREDENTIALS": str(path)}):
                save_credential(PersonalCredential("lxmcp_test_token", "company"))
                loaded = load_credential()
            self.assertEqual(loaded.company_from, "company")
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(
                set(json.loads(path.read_text())),
                {"mcp_token", "company_from"},
            )

    def test_rejects_non_personal_mcp_token(self) -> None:
        with self.assertRaises(AuthError):
            PersonalCredential("not-an-lxmcp-token", "company").validate_shape()


class SourceMetadataTests(unittest.TestCase):
    def test_meta_source_fields_precede_meta_title(self) -> None:
        source_url, source_title = resolve_source(
            "",
            "",
            {
                "source_url": "https://example.com/source",
                "source_title": "Source title",
                "title": "Page title",
            },
            True,
            credential_loader=lambda: self.fail("credential should not be loaded"),
        )
        self.assertEqual(source_url, "https://example.com/source")
        self.assertEqual(source_title, "Source title")

    def test_explicit_source_fields_have_highest_priority(self) -> None:
        source_url, source_title = resolve_source(
            "https://explicit.example",
            "Explicit",
            {
                "source_url": "https://meta.example",
                "source_title": "Meta",
                "title": "Page",
            },
            True,
            credential_loader=lambda: self.fail("credential should not be loaded"),
        )
        self.assertEqual(source_url, "https://explicit.example")
        self.assertEqual(source_title, "Explicit")

    def test_entry_id_falls_back_to_lexiang_page_url(self) -> None:
        source_url, source_title = resolve_source(
            "",
            "",
            {"entry_id": "entry-123", "title": "Archived page"},
            True,
            credential_loader=lambda: PersonalCredential("lxmcp_test", "tenant"),
        )
        self.assertEqual(
            source_url,
            "https://lexiangla.com/pages/entry-123?company_from=tenant",
        )
        self.assertEqual(source_title, "Archived page")

    def test_dry_run_reports_local_callouts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown = root / "article.md"
            markdown.write_text(
                "> [!stat] **73%**\n> English statistic.\n> 中文统计。",
                encoding="utf-8",
            )
            output = io.StringIO()
            args = Namespace(
                work_dir=None,
                md_name=None,
                md_path=str(markdown),
                meta_file=None,
                source_url="",
                source_title="",
                source_from_meta=False,
                formula_mode="unicode",
                name="",
                name_suffix="",
                parent_id="parent",
                parent_from_meta=False,
                entry_id="",
                dry_run=True,
                pin=False,
                json=True,
            )
            with redirect_stdout(output):
                upload(args)
            summary = json.loads(output.getvalue())
            self.assertEqual(summary["local_callouts"], 1)
            self.assertNotIn("remote_callouts", summary)
            self.assertEqual(summary["credential_profile"], "default")
            self.assertEqual(summary["credential_file"], str(DEFAULT_CREDENTIALS))

    def test_dry_run_does_not_load_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            markdown = Path(directory) / "article.md"
            markdown.write_text("# Title\n\nBody", encoding="utf-8")
            args = self._upload_args(markdown, dry_run=True)
            with patch(
                "lexiang_upload.load_credential",
                side_effect=AssertionError("must not read credentials"),
            ):
                with redirect_stdout(io.StringIO()):
                    upload(args)

    def test_upload_uses_selected_credential(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown = root / "article.md"
            markdown.write_text("# Title\n\nBody", encoding="utf-8")
            credential_file = root / "selected.json"
            credential_file.write_text(
                json.dumps(
                    {
                        "mcp_token": "lxmcp_selected_token",
                        "company_from": "selected-company",
                    }
                ),
                encoding="utf-8",
            )
            args = self._upload_args(
                markdown,
                credential_file=str(credential_file),
            )
            output = io.StringIO()
            clients = []

            class SelectedClient:
                def __init__(self, credential):
                    clients.append(credential)

            with (
                patch("lexiang_upload.MCPClient", SelectedClient),
                patch("lexiang_upload.create_page", return_value="entry"),
                patch("lexiang_upload.execute_plan"),
                patch("lexiang_upload.verify_page", return_value=(0, 0)),
                redirect_stdout(output),
            ):
                upload(args)

            summary = json.loads(output.getvalue())
            self.assertEqual(clients[0].mcp_token, "lxmcp_selected_token")
            self.assertEqual(summary["credential_file"], str(credential_file))
            self.assertIsNone(summary["credential_profile"])
            self.assertEqual(summary["company_from"], "selected-company")

    @staticmethod
    def _upload_args(markdown: Path, **overrides) -> Namespace:
        values = {
            "work_dir": None,
            "md_name": None,
            "md_path": str(markdown),
            "meta_file": None,
            "source_url": "",
            "source_title": "",
            "source_from_meta": False,
            "formula_mode": "unicode",
            "name": "",
            "name_suffix": "",
            "parent_id": "parent",
            "parent_from_meta": False,
            "entry_id": "",
            "dry_run": False,
            "pin": False,
            "json": True,
            "profile": None,
            "credential_file": None,
        }
        values.update(overrides)
        return Namespace(**values)

    def test_existing_source_link_is_not_prepended_twice(self) -> None:
        url = "https://example.com/source"
        markdown = f"# Title\n\n> 原文链接: {url}\n\nBody"
        self.assertEqual(prepend_source_link(markdown, url, "Source"), markdown)


class MathConversionTests(unittest.TestCase):
    def test_converts_inline_and_display_math(self) -> None:
        converted, formulas = convert_math("A $K_V/\\rho$ value.\n\n$$\\Phi=n\\cdot d$$")
        self.assertIn("$`K_V/\\rho`$", converted)
        self.assertEqual([formula.display for formula in formulas], [False, True])

    def test_does_not_touch_code(self) -> None:
        source = "Use `$HOME` and:\n```sh\necho '$x$'\n```\nThen $x^2$."
        converted, formulas = convert_math(source)
        self.assertIn("echo '$x$'", converted)
        self.assertEqual(len(formulas), 1)

    def test_does_not_treat_currency_as_math(self) -> None:
        source = "CapEx is $7.6tn, rising from $494.5bn to $1.13tn."
        converted, formulas = convert_math(source)
        self.assertEqual(converted, source)
        self.assertEqual(formulas, ())

    def test_unicode_formula_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            converted, count = materialize_formula_fallback(
                "# Formula\n\nSpecific stiffness is $K_V/\\rho$.",
                Path(directory),
                render_images=False,
            )
            self.assertEqual(count, 1)
            self.assertIn("Kᵥ/ρ", converted)

    def test_latex_to_unicode(self) -> None:
        self.assertEqual(latex_to_unicode(r"B_4C"), "B₄C")
        self.assertEqual(latex_to_unicode(r"C_{11} > 1,000"), "C₁₁ > 1,000")


class PlanTests(unittest.TestCase):
    def test_requires_all_images(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(PreflightError):
                build_plan("# Title\n\n![](images/missing.png)", Path(directory))

    def test_supports_arbitrary_relative_image_paths_and_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "assets").mkdir()
            image = root / "assets" / "figure one.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\n")
            plan = build_plan(
                "# Title\n\nText\n\n![](assets/figure%20one.png)\n\n"
                "More text.\n\n![](assets/figure%20one.png)",
                root,
            )
            self.assertEqual(len(plan.image_paths), 2)
            self.assertEqual([segment.kind for segment in plan.segments], ["text", "image", "text", "image"])

    def test_supports_unescaped_and_angle_bracket_image_paths_with_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "images").mkdir()
            image = root / "images" / "Pasted image 20260711234206.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\n")
            plan = build_plan(
                "# Title\n\n"
                "![first](images/Pasted image 20260711234206.png)\n\n"
                "Text\n\n"
                "![second](<images/Pasted image 20260711234206.png>)",
                root,
            )
            self.assertEqual(plan.image_paths, (image.resolve(), image.resolve()))
            self.assertEqual(
                [segment.kind for segment in plan.segments],
                ["text", "image", "text", "image"],
            )

    def test_image_path_with_spaces_and_title_is_preflighted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "images").mkdir()
            image = root / "images" / "figure one.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\n")
            plan = build_plan(
                '# Title\n\n![alt](images/figure one.png "Figure title")',
                root,
            )
            self.assertEqual(plan.image_paths, (image.resolve(),))

    def test_missing_unescaped_image_path_with_spaces_fails_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(PreflightError):
                build_plan(
                    "# Title\n\n![](images/Pasted image missing.png)",
                    Path(directory),
                )

    def test_rejects_image_path_outside_document_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(PreflightError):
                build_plan("# Title\n\n![](../secret.png)", Path(directory))

    def test_document_starting_with_image_initializes_page_before_upload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "cover.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\n")
            plan = build_plan("![](cover.png)\n\n# Title\n\nBody", root)
            events = []
            with (
                patch("lexiang_upload.replace_page_text", side_effect=lambda *_: events.append("replace")),
                patch("lexiang_upload.upload_image", side_effect=lambda *_: events.append("image")),
                patch("lexiang_upload.append_page_text", side_effect=lambda *_: events.append("append")),
            ):
                execute_plan(object(), "entry", plan)
            self.assertEqual(events, ["replace", "image", "append"])

    def test_large_table_is_split(self) -> None:
        table = "| Name |\n|---|\n" + "\n".join(f"| row-{index} |" for index in range(20))
        converted = split_large_gfm_tables(table, max_rows=10)
        self.assertEqual(converted.count("| Name |"), 3)

    def test_figure_caption_is_not_heading(self) -> None:
        converted = demote_caption_headings("# Results\n\n## FIG. 1. Result chart.")
        self.assertIn("# Results", converted)
        self.assertNotIn("## FIG.", converted)

    def test_recognizes_stat_and_definition_callouts(self) -> None:
        markdown = (
            "> [!stat] **73%**\n"
            "> English statistic.\n"
            "> 中文统计。\n\n"
            "> [!definition] **Specific stiffness**\n"
            "> English definition.\n"
            "> 中文定义。"
        )
        callouts, _ = parse_portable_callouts(markdown)
        self.assertEqual([callout.kind for callout in callouts], ["stat", "definition"])
        self.assertEqual([callout.icon for callout in callouts], ["📊", "📖"])
        plan = build_plan(markdown, Path("."))
        self.assertEqual([segment.kind for segment in plan.segments], ["callout", "callout"])

    def test_recognizes_note_callout_with_list_body(self) -> None:
        markdown = (
            "> [!note] **文章亮点**\n"
            "> - **亮点一：**组织管理类比\n"
            "> - **亮点二：**Evals 是新的 OKRs\n"
            "> - **亮点三：**Palantir 销售的是转型"
        )
        callouts, _ = parse_portable_callouts(markdown)
        self.assertEqual(len(callouts), 1)
        self.assertEqual(callouts[0].kind, "note")
        self.assertEqual(callouts[0].icon, "💡")
        self.assertIn("- **亮点二：**", callouts[0].markdown)

    def test_does_not_misrecognize_regular_blockquote(self) -> None:
        markdown = "> A regular quotation.\n> It remains ordinary Markdown."
        callouts, _ = parse_portable_callouts(markdown)
        self.assertEqual(callouts, ())
        plan = build_plan(markdown, Path("."))
        self.assertEqual([segment.kind for segment in plan.segments], ["text"])

    def test_callout_plan_creates_native_descendant(self) -> None:
        plan = build_plan(
            "> [!stat] **73%**\n> English statistic.\n> 中文统计。",
            Path("."),
        )
        client = FakeClient(plan)
        execute_plan(client, "entry", plan)
        created = [
            arguments
            for tool, arguments in client.json_calls
            if tool == "block_create_block_descendant"
        ]
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0]["descendant"][0]["block_type"], "callout")
        self.assertEqual(created[0]["descendant"][0]["callout"]["icon"], "📊")
        self.assertEqual(verify_page(client, "entry", plan), (0, 1))


class VerificationTests(unittest.TestCase):
    def test_remote_verification_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = build_plan(
                "# Mechanical Properties / 机械性能\n\n"
                "An important caveat applies to layered materials and this paragraph "
                "contains enough detail to be used as a stable content anchor for testing.",
                Path(directory),
            )
            verify_remote(plan, plan.markdown, plan.markdown, 0)

    def test_remote_verification_detects_loss(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = build_plan(
                "# Mechanical Properties\n\n"
                "This is a deliberately long source paragraph whose disappearance "
                "must be detected rather than silently accepted after upload.",
                Path(directory),
            )
            with self.assertRaises(VerificationError):
                verify_remote(plan, "Mechanical Properties", "", 0)

    def test_remote_verification_detects_callout_count_loss(self) -> None:
        plan = build_plan(
            "> [!definition] **Term**\n> English definition.\n> 中文定义。",
            Path("."),
        )
        with self.assertRaises(VerificationError):
            verify_remote(plan, plan.markdown, plan.markdown, 0, 0)

    def test_page_verification_retries_eventually_consistent_reads(self) -> None:
        plan = build_plan(
            "# Title\n\n"
            "This deliberately long paragraph becomes visible after the first "
            "eventually consistent page read and must pass on retry.",
            Path("."),
        )
        client = FlakyVerificationClient(plan)
        with patch("lexiang_upload.time.sleep"):
            self.assertEqual(verify_page(client, "entry", plan, attempts=2), (0, 0))
        self.assertEqual(client.clean_fetches, 2)


class FakeClient:
    def __init__(self, plan) -> None:
        self.plan = plan
        self.json_calls = []

    def json(self, tool, arguments):
        self.json_calls.append((tool, arguments))
        if tool == "block_convert_content_to_blocks":
            return {
                "data": {
                    "descendant": [
                        {
                            "block_id": "paragraph",
                            "block_type": "p",
                            "text": {"elements": []},
                        }
                    ],
                    "children": ["paragraph"],
                }
            }
        if tool == "block_list_block_children":
            return {"data": {"blocks": [{"block_type": "callout"}]}}
        return {"data": {}}

    def text(self, tool, arguments):
        if tool == "block_update_page":
            return "succeeded"
        if tool == "block_fetch_page":
            return self.plan.markdown
        return ""


class FlakyVerificationClient(FakeClient):
    def __init__(self, plan) -> None:
        super().__init__(plan)
        self.clean_fetches = 0

    def text(self, tool, arguments):
        if tool == "block_fetch_page" and arguments.get("render_mode") == "clean":
            self.clean_fetches += 1
            return "" if self.clean_fetches == 1 else self.plan.markdown
        return super().text(tool, arguments)

    def json(self, tool, arguments):
        if tool == "block_list_block_children":
            return {"data": {"blocks": []}}
        return super().json(tool, arguments)


if __name__ == "__main__":
    unittest.main()
