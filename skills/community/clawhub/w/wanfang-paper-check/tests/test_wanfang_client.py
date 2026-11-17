from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "wanfang_client.py"
SPEC = importlib.util.spec_from_file_location("wanfang_client", SCRIPT)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(CLIENT := importlib.util.module_from_spec(SPEC))

DOMAIN = {"owner_user_id": 2, "base_url": "https://wanfang.cqccjy.cn", "pages": {"entry": "https://wanfang.cqccjy.cn/pwf", "payment": "https://wanfang.cqccjy.cn/pwf?orderNo={order_no}&stage=payment", "progress": "https://wanfang.cqccjy.cn/pwf/check?orderNo={order_no}&stage=progress", "report": "https://wanfang.cqccjy.cn/pwf/check?orderNo={order_no}", "verify_funnel": "https://vpcs.cqccjy.cn/pwp/verify", "verify_official": "https://truth.wanfangdata.com.cn/"}, "api": {"config": "/api/paper/wanfang/public/config", "presign": "/api/paper/wanfang/public/upload/presign", "create": "/api/paper/wanfang/public/order/create", "order": "/api/paper/wanfang/public/order/{order_no}", "report_download_url": "/api/paper/wanfang/public/order/{order_no}/report-download-url"}}
CONFIG = {"limits": {"max_file_bytes": 1024 * 1024, "max_title_chars": 255, "min_author_chars": 2, "max_author_chars": 64, "supported_extensions": [".doc", ".docx", ".txt", ".pdf", ".rtf"]}, "runtime_snapshot": {"enabled": True, "payment_channels": []}}
CATALOG = {"captured_at": "2026-10-02", "products": [{"productCode": "WF_UNDERGRADUATE", "productName": "万方本科版", "fileType": "doc,docx,txt,pdf,rtf", "acceptTimeRequired": False, "salePrice": "2.40"}, {"productCode": "WF_TITLE", "productName": "万方职称版", "fileType": "doc,docx,txt,pdf,rtf", "acceptTimeRequired": True, "salePrice": "4.00"}, {"productCode": "WF_TEXT_AIGC", "productName": "万方文本AIGC检测", "fileType": "doc,docx,txt,pdf", "acceptTimeRequired": False, "salePrice": "1.60"}]}


class FakeClient:
    dry_run = False

    def __init__(self):
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        if url.endswith("/upload/presign"):
            return {"uploadUrl": "https://upload.example.test/paper", "objectKey": "private/wanfang/paper.docx", "headers": {"x-test": "1"}}
        if url.endswith("/order/create"):
            return {"orderNo": "123", "productCode": "WF_UNDERGRADUATE", "productName": "万方本科版", "status": "WAIT_PAY", "payStatus": "UNPAID", "payAmount": "2.40"}
        return None


class WanfangClientTest(unittest.TestCase):
    def test_cli_commands(self):
        parser = CLIENT.build_parser()
        choices = set(parser._subparsers._group_actions[0].choices)
        self.assertEqual(choices, {"products", "submit", "status", "report", "verify"})

    def test_product_aliases(self):
        self.assertEqual(CLIENT.normalize_product("万方本科查重"), "WF_UNDERGRADUATE")
        self.assertEqual(CLIENT.normalize_product("万方硕博版"), "WF_GRADUATE")
        self.assertEqual(CLIENT.normalize_product("万方文本AIGC检测"), "WF_TEXT_AIGC")
        self.assertEqual(CLIENT.normalize_product("职称版"), "WF_TITLE")

    def test_browser_urls_encode_order_number(self):
        urls = CLIENT.browser_urls(DOMAIN, "A/B 1")
        self.assertEqual(urls["payment"], "https://wanfang.cqccjy.cn/pwf?orderNo=A%2FB%201&stage=payment")

    def test_unpaid_order_selects_payment(self):
        output = CLIENT.result("status", DOMAIN, {"orderNo": "123", "status": "WAIT_PAY", "payStatus": "UNPAID"})
        self.assertEqual(output["browser_url"], output["browser_urls"]["payment"])

    def test_paid_order_selects_progress(self):
        output = CLIENT.result("status", DOMAIN, {"orderNo": "123", "status": "DETECTING", "payStatus": "PAID"})
        self.assertEqual(output["browser_url"], output["browser_urls"]["progress"])

    def test_completed_order_selects_report(self):
        output = CLIENT.result("status", DOMAIN, {"orderNo": "123", "status": "COMPLETED", "reportNum": "masked"})
        self.assertEqual(output["browser_url"], output["browser_urls"]["report"])

    def test_aigc_file_type_is_enforced(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "paper.rtf"
            path.write_text("fixture", encoding="utf-8")
            with self.assertRaises(CLIENT.WanfangError):
                CLIENT.validate_file(str(path), CONFIG, CATALOG["products"][2])

    def test_required_accept_time_is_enforced(self):
        args = type("Args", (), {"title": "论文", "author": "作者", "accept_time": None})()
        with self.assertRaises(CLIENT.WanfangError):
            CLIENT.validate_metadata(args, CATALOG["products"][1], CONFIG)

    def test_submit_dry_run_uses_snapshot_and_no_network(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "paper.docx"
            path.write_bytes(b"fixture")
            args = type("Args", (), {"product_code": "万方本科版", "title": "论文题目", "author": "作者", "file": str(path), "accept_time": None, "check_dbs": None})()
            output = CLIENT.submit_order(CLIENT.RestClient(timeout=5, dry_run=True), CONFIG, DOMAIN, CATALOG, args)
        self.assertTrue(output["dry_run"])
        self.assertIsNone(output["order_no"])
        self.assertEqual(output["product_code"], "WF_UNDERGRADUATE")
        self.assertEqual(output["browser_url"], DOMAIN["pages"]["entry"])

    def test_submit_omits_internal_channel_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "paper.docx"
            path.write_bytes(b"fixture")
            args = type("Args", (), {"product_code": "WF_UNDERGRADUATE", "title": "论文题目", "author": "作者", "file": str(path), "accept_time": None, "check_dbs": None})()
            client = FakeClient()
            live = {"enabled": True, "products": CATALOG["products"]}
            with patch.object(CLIENT, "load_live_config", return_value=live), patch.object(CLIENT, "upload_with_ticket", return_value="private/wanfang/paper.docx"):
                output = CLIENT.submit_order(client, CONFIG, DOMAIN, CATALOG, args)
        presign_payload = client.calls[0][2]["payload"]
        create_payload = client.calls[1][2]["payload"]
        self.assertEqual(presign_payload, {"fileName": "paper.docx", "productCode": "WF_UNDERGRADUATE"})
        self.assertNotIn("channelCode", create_payload)
        self.assertNotIn("processMode", create_payload)
        self.assertEqual(output["order_no"], "123")

    def test_non_https_report_url_is_not_exposed(self):
        output = CLIENT.result("report", DOMAIN, {"orderNo": "123", "status": "COMPLETED"}, report_download_url="http://supplier.invalid/report.zip")
        self.assertIsNone(output["report_download_url"])
        self.assertNotIn("report_download", output["browser_urls"])

    def test_failed_report_query_keeps_failure_guidance(self):
        class FailedClient:
            dry_run = False
            def request(self, method, url, **kwargs):
                return {"orderNo": "123", "status": "FAILED", "failReason": "供应商处理失败"}
        output = CLIENT.report_result(FailedClient(), DOMAIN, "123")
        self.assertEqual(output["browser_url"], output["browser_urls"]["progress"])
        self.assertIn("处理失败", output["next_action"])


if __name__ == "__main__":
    unittest.main()
