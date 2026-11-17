"""Credential-free tests for Social helper CLIs and shared client helpers."""

from __future__ import annotations

import json
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import inspect_post  # noqa: E402
import list_brands  # noqa: E402
import list_channels  # noqa: E402
import list_drafts  # noqa: E402
import list_media  # noqa: E402
import list_portals  # noqa: E402
import list_published  # noqa: E402
import list_schedules  # noqa: E402
import social_client  # noqa: E402
import upload_media  # noqa: E402


class SocialClientHelperTests(unittest.TestCase):
    def test_rows_unwraps_nested_data_lists(self):
        result = {"data": {"data": [{"id": "1"}, {"id": "2"}]}}
        self.assertEqual(social_client.rows(result), [{"id": "1"}, {"id": "2"}])

    def test_rows_unwraps_brands_key(self):
        result = {"data": {"brands": [{"id": "b1"}]}}
        self.assertEqual(social_client.rows(result), [{"id": "b1"}])

    def test_rows_returns_empty_on_error(self):
        self.assertEqual(social_client.rows({"error": "boom"}), [])

    def test_field_reads_nested_name(self):
        record = {"created_by": {"name": "Ada Lovelace", "id": "9"}}
        self.assertEqual(social_client.field(record, ["created_by"]), "Ada Lovelace")

    def test_positive_int_rejects_zero(self):
        with self.assertRaises(Exception):
            social_client.positive_int("0")

    def test_runtime_tool_prefixes_once(self):
        self.assertEqual(social_client.runtime_tool("getSocialPortals"), "ZohoSocial_getSocialPortals")
        self.assertEqual(
            social_client.runtime_tool("ZohoSocial_getSocialPortals"),
            "ZohoSocial_getSocialPortals",
        )


class HelperParserTests(unittest.TestCase):
    def test_list_portals_help_exits_zero(self):
        with self.assertRaises(SystemExit) as ctx:
            list_portals.build_parser().parse_args(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_list_portals_unknown_option_exits_two(self):
        with self.assertRaises(SystemExit) as ctx:
            list_portals.build_parser().parse_args(["--not-a-real-flag"])
        self.assertEqual(ctx.exception.code, 2)

    def test_list_brands_requires_portal(self):
        code = list_brands.main([])
        self.assertEqual(code, 2)

    def test_list_channels_requires_portal_and_brand(self):
        code = list_channels.main(["--portal-id", "p1"])
        self.assertEqual(code, 2)

    def test_list_published_requires_network(self):
        with self.assertRaises(SystemExit) as ctx:
            list_published.build_parser().parse_args(["--portal-id", "p1", "--brand-id", "b1"])
        self.assertEqual(ctx.exception.code, 2)

    def test_inspect_published_requires_network(self):
        with mock.patch.object(inspect_post.ENDPOINT, "configure"):
            code = inspect_post.main(["123", "--kind", "published", "--portal-id", "p1", "--brand-id", "b1"])
        self.assertEqual(code, 2)

    def test_upload_media_requires_file_or_url(self):
        with self.assertRaises(SystemExit) as ctx:
            upload_media.build_parser().parse_args(["--portal-id", "p1", "--brand-id", "b1"])
        self.assertEqual(ctx.exception.code, 2)

    def test_list_portals_without_endpoint_exits_one(self):
        with mock.patch.object(list_portals.ENDPOINT, "configure"):
            with mock.patch.object(
                list_portals,
                "call",
                return_value={"error": "no Zoho Social MCP endpoint configured"},
            ):
                code = list_portals.main([])
        self.assertEqual(code, 1)


class UploadMediaTests(unittest.TestCase):
    def test_encode_local_png_is_complete_data_uri(self):
        png = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
            b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18"
            b"\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "pixel.png"
            path.write_bytes(png)
            data_uri, name = upload_media.encode_local(path, max_bytes=1024)
        self.assertEqual(name, "pixel.png")
        self.assertTrue(data_uri.startswith("data:image/png;base64,"))
        self.assertNotIn("...", data_uri)
        payload = data_uri.split(",", 1)[1]
        import base64
        self.assertEqual(base64.b64decode(payload), png)

    def test_encode_local_rejects_unsupported_type(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "note.txt"
            path.write_text("nope", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                upload_media.encode_local(path, max_bytes=1024)
        self.assertEqual(ctx.exception.code, 2)

    def test_upload_success_without_file_id_is_failure(self):
        with mock.patch.object(upload_media.ENDPOINT, "configure"):
            with mock.patch.object(upload_media, "headers_from", return_value={"portal_id": "p", "brand_id": "b"}):
                with mock.patch.object(upload_media, "call", return_value={"status": "success", "data": {"data": {}}}):
                    code = upload_media.main(
                        ["--portal-id", "p", "--brand-id", "b", "--image-url", "https://example.com/a.png"]
                    )
        self.assertEqual(code, 1)

    def test_upload_live_shape_reports_file_path_as_id(self):
        live_shape = {
            "status": "success",
            "data": {
                "data": {
                    "file_path": "4662442000000184002",
                    "file_name": "hero.png",
                    "file_size": "1060",
                    "width": 400,
                    "height": 400,
                    "status": "success",
                }
            },
        }
        with mock.patch.object(upload_media.ENDPOINT, "configure"):
            with mock.patch.object(upload_media, "headers_from", return_value={"portal_id": "p", "brand_id": "b"}):
                with mock.patch.object(upload_media, "call", return_value=live_shape):
                    with mock.patch("sys.stdout", new_callable=io.StringIO) as out:
                        code = upload_media.main(
                            ["--portal-id", "p", "--brand-id", "b", "--image-url", "https://example.com/a.png"]
                        )
        self.assertEqual(code, 0)
        self.assertIn("4662442000000184002", out.getvalue())

    def test_upload_degenerate_image_fake_success_is_failure(self):
        fake = {
            "status": "success",
            "data": {
                "data": {
                    "file_path": "",
                    "file_name": "",
                    "preview_url": "",
                    "file_size": "",
                    "status": "",
                }
            },
        }
        with mock.patch.object(upload_media.ENDPOINT, "configure"):
            with mock.patch.object(upload_media, "headers_from", return_value={"portal_id": "p", "brand_id": "b"}):
                with mock.patch.object(upload_media, "call", return_value=fake):
                    code = upload_media.main(
                        ["--portal-id", "p", "--brand-id", "b", "--image-url", "https://example.com/a.png"]
                    )
        self.assertEqual(code, 1)

    def test_upload_from_url_prints_file_id(self):
        with mock.patch.object(upload_media.ENDPOINT, "configure"):
            with mock.patch.object(upload_media, "headers_from", return_value={"portal_id": "p", "brand_id": "b"}):
                with mock.patch.object(
                    upload_media,
                    "call",
                    return_value={"status": "success", "data": {"data": {"id": "file-9", "file_name": "a.png"}}},
                ):
                    code = upload_media.main(
                        ["--portal-id", "p", "--brand-id", "b", "--image-url", "https://example.com/a.png"]
                    )
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
