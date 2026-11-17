from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vpcs_client.py"
SPEC = importlib.util.spec_from_file_location("vpcs_client", SCRIPT)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(CLIENT := importlib.util.module_from_spec(SPEC))

DOMAIN = {
    "base_url": "https://vpcs.cqccjy.cn",
    "pages": {
        "entry": "https://vpcs.cqccjy.cn/pwp",
        "payment": "https://vpcs.cqccjy.cn/pwp?orderNo={order_no}&stage=payment",
        "progress": "https://vpcs.cqccjy.cn/pwp?orderNo={order_no}&stage=progress",
        "reports": "https://vpcs.cqccjy.cn/reports?orderNo={order_no}",
        "verify": "https://vpcs.cqccjy.cn/pwp/verify",
    },
    "api": {
        "order": "/api/paper/check/public/order/{order_no}",
    },
}


class _Response:
    status = 200

    def read(self, _size=-1):
        return b""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


class VpcsClientTest(unittest.TestCase):
    def test_cli_exposes_only_submit_and_status(self):
        parser = CLIENT.build_parser()
        choices = set(parser._subparsers._group_actions[0].choices)
        self.assertEqual(choices, {"submit", "status"})

    def test_product_alias_and_browser_urls(self):
        self.assertEqual(CLIENT.normalize_product("维普查重大学生版"), "dxs")
        urls = CLIENT.browser_urls(DOMAIN, "A/B 1")
        self.assertEqual(
            urls["payment"],
            "https://vpcs.cqccjy.cn/pwp?orderNo=A%2FB%201&stage=payment",
        )
        self.assertEqual(
            urls["reports"],
            "https://vpcs.cqccjy.cn/reports?orderNo=A%2FB%201",
        )

    def test_unpaid_order_returns_payment_url(self):
        output = CLIENT.result(
            "status",
            DOMAIN,
            {"orderNo": "123", "status": "WAIT_PAYMENT", "payStatus": "UNPAID"},
        )
        self.assertEqual(output["browser_url"], output["browser_urls"]["payment"])
        self.assertEqual(output["order_no"], "123")

    def test_paid_order_returns_progress_url(self):
        output = CLIENT.result(
            "status",
            DOMAIN,
            {"status": "WAIT_SUBMIT", "payStatus": "PAID", "canSubmitDetect": True},
            order_no="123",
        )
        self.assertEqual(output["browser_url"], output["browser_urls"]["progress"])

    def test_completed_order_returns_reports_url(self):
        output = CLIENT.result(
            "status",
            DOMAIN,
            {"status": "REPORT_READY", "canDownloadReport": True},
            order_no="123",
        )
        self.assertEqual(output["browser_url"], output["browser_urls"]["reports"])

    def test_signed_url_upload_uses_returned_object_key(self):
        ticket = {
            "uploadUrl": "https://upload.example.test/object",
            "objectKey": "private/order/paper.docx",
        }
        with patch.object(
            CLIENT.urllib.request, "urlopen", return_value=_Response()
        ) as urlopen:
            key = CLIENT.upload_with_ticket(
                CLIENT.RestClient(timeout=5),
                ticket,
                b"fixture",
                "application/octet-stream",
            )
        self.assertEqual(key, "private/order/paper.docx")
        self.assertEqual(urlopen.call_args.args[0].full_url, ticket["uploadUrl"])

    def test_submit_dry_run_returns_entry_without_network(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "paper.docx"
            path.write_bytes(b"fixture")
            args = type(
                "Args",
                (),
                {
                    "product_type": "维普查重大学生版",
                    "title": "论文题目",
                    "author": "作者",
                    "file": str(path),
                    "publish_date": None,
                },
            )()
            config = {
                "limits": {
                    "supported_extensions": [".docx"],
                    "max_file_bytes": 1024,
                    "max_title_chars": 128,
                    "min_author_chars": 2,
                    "max_author_chars": 20,
                }
            }
            output = CLIENT.submit_order(
                CLIENT.RestClient(timeout=5, dry_run=True), config, DOMAIN, args
            )
            self.assertIsNone(output["order_no"])
            self.assertEqual(output["product_type"], "dxs")
            self.assertEqual(output["browser_url"], DOMAIN["pages"]["entry"])

    def test_status_query_uses_order_endpoint(self):
        client = CLIENT.RestClient(timeout=5)
        with patch.object(
            client,
            "request",
            return_value={"status": "WAIT_PAYMENT", "payStatus": "UNPAID"},
        ) as request:
            order = CLIENT.load_order(client, DOMAIN, "123")
        self.assertEqual(order["status"], "WAIT_PAYMENT")
        self.assertEqual(
            request.call_args.args[:2],
            ("GET", "https://vpcs.cqccjy.cn/api/paper/check/public/order/123"),
        )


if __name__ == "__main__":
    unittest.main()
