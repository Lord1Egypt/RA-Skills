# -*- coding: utf-8 -*-
"""百度知道回答发布 Service 层契约测试。

覆盖三类常见契约：
1. 成功路径（mock 档位返回 success）
2. 参数校验（缺 question_url / input_id / 文件不存在）
3. 幂等预检（重复 idempotency_key 不重复发布）

所有用例走 mock 档位（OPENCLAW_TEST_TARGET 未设置或为 unit/mock），
不触网、不启动浏览器、不调用 account-manager。
"""
from __future__ import annotations

import io
import json
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout

from _support import IsolatedDataRoot


class TestPublishAnswerContract(unittest.TestCase):
    """百度知道回答发布契约测试（mock 档位）。"""

    def setUp(self) -> None:
        # 确保走 mock 档位
        self._old_target = os.environ.get("OPENCLAW_TEST_TARGET")
        os.environ["OPENCLAW_TEST_TARGET"] = "mock"
        # 关闭鉴权外呼
        self._old_auth = os.environ.pop("JIANGCHANG_AUTH_BASE_URL", None)
        # 关闭录屏
        self._old_record = os.environ.get("OPENCLAW_RECORD_VIDEO")
        os.environ["OPENCLAW_RECORD_VIDEO"] = "0"

    def tearDown(self) -> None:
        if self._old_target is None:
            os.environ.pop("OPENCLAW_TEST_TARGET", None)
        else:
            os.environ["OPENCLAW_TEST_TARGET"] = self._old_target
        if self._old_auth is not None:
            os.environ["JIANGCHANG_AUTH_BASE_URL"] = self._old_auth
        if self._old_record is None:
            os.environ.pop("OPENCLAW_RECORD_VIDEO", None)
        else:
            os.environ["OPENCLAW_RECORD_VIDEO"] = self._old_record

    def _write_answer_file(self, content: str = "这是一段测试回答内容。") -> str:
        """在隔离数据目录下写一个临时回答文稿，返回路径。"""
        path = os.path.join(os.environ["JIANGCHANG_DATA_ROOT"], "answer.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_run_without_question_url_returns_structured_error(self) -> None:
        """缺 --question-url 时返回结构化错误 JSON，而不是抛异常。"""
        with IsolatedDataRoot(user_id="_contract_no_url"):
            from cli.app import main
            from jiangchang_skill_core import config
            config.reset_cache()

            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["run", "--input-id", "dummy.md"])
            self.assertNotEqual(rc, 0)
            out = buf.getvalue().strip()
            # 最后一行应为 JSON
            last_line = [ln for ln in out.splitlines() if ln.strip()][-1]
            payload = json.loads(last_line)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error"]["code"], "QUESTION_URL_EMPTY")

    def test_run_without_input_id_returns_structured_error(self) -> None:
        """缺 --input-id 时返回结构化错误 JSON。"""
        with IsolatedDataRoot(user_id="_contract_no_input"):
            from cli.app import main
            from jiangchang_skill_core import config
            config.reset_cache()

            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["run", "--question-url",
                           "https://zhidao.baidu.com/question/123456"])
            self.assertNotEqual(rc, 0)
            out = buf.getvalue().strip()
            last_line = [ln for ln in out.splitlines() if ln.strip()][-1]
            payload = json.loads(last_line)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error"]["code"], "ANSWER_PATH_EMPTY")

    def test_run_with_invalid_question_url_returns_structured_error(self) -> None:
        """问题 URL 格式不正确时返回结构化错误。"""
        with IsolatedDataRoot(user_id="_contract_bad_url"):
            from cli.app import main
            from jiangchang_skill_core import config
            config.reset_cache()

            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["run",
                           "--question-url", "https://example.com/question/123",
                           "--input-id", "dummy.md"])
            self.assertNotEqual(rc, 0)
            out = buf.getvalue().strip()
            last_line = [ln for ln in out.splitlines() if ln.strip()][-1]
            payload = json.loads(last_line)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error"]["code"], "QUESTION_URL_INVALID")

    def test_run_with_nonexistent_answer_file_returns_structured_error(self) -> None:
        """回答文稿不存在时返回结构化错误。"""
        with IsolatedDataRoot(user_id="_contract_no_file"):
            from cli.app import main
            from jiangchang_skill_core import config
            config.reset_cache()

            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["run",
                           "--question-url", "https://zhidao.baidu.com/question/123456",
                           "--input-id", r"D:\nonexistent\answer.md"])
            self.assertNotEqual(rc, 0)
            out = buf.getvalue().strip()
            last_line = [ln for ln in out.splitlines() if ln.strip()][-1]
            payload = json.loads(last_line)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error"]["code"], "ANSWER_FILE_NOT_FOUND")

    def test_mock_run_success_returns_success_true(self) -> None:
        """mock 档位下，合法参数应返回 success=True。"""
        with IsolatedDataRoot(user_id="_contract_mock_ok"):
            from cli.app import main
            from jiangchang_skill_core import config
            config.reset_cache()

            answer_path = self._write_answer_file("这是一段测试回答内容，足够长。")

            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["run",
                           "--question-url", "https://zhidao.baidu.com/question/123456",
                           "--input-id", answer_path])
            self.assertEqual(rc, 0)
            out = buf.getvalue().strip()
            last_line = [ln for ln in out.splitlines() if ln.strip()][-1]
            payload = json.loads(last_line)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["status"], "success")
            self.assertFalse(payload["duplicate"])
            self.assertIsNotNone(payload["publish_record_id"])

    def test_idempotency_key_prevents_duplicate_publish(self) -> None:
        """同一 idempotency_key 第二次运行应返回 duplicate=True，不重复写记录。"""
        with IsolatedDataRoot(user_id="_contract_idem"):
            from cli.app import main
            from jiangchang_skill_core import config
            config.reset_cache()

            answer_path = self._write_answer_file("测试回答内容。")
            url = "https://zhidao.baidu.com/question/999999"
            key = "batch-test-001"

            # 第一次运行
            buf1 = io.StringIO()
            with redirect_stdout(buf1), redirect_stderr(io.StringIO()):
                rc1 = main(["run",
                            "--question-url", url,
                            "--input-id", answer_path,
                            "--idempotency-key", key])
            self.assertEqual(rc1, 0)
            last1 = [ln for ln in buf1.getvalue().splitlines() if ln.strip()][-1]
            payload1 = json.loads(last1)
            self.assertFalse(payload1["duplicate"])
            first_record_id = payload1["publish_record_id"]

            # 第二次运行（应命中幂等）
            buf2 = io.StringIO()
            with redirect_stdout(buf2), redirect_stderr(io.StringIO()):
                rc2 = main(["run",
                            "--question-url", url,
                            "--input-id", answer_path,
                            "--idempotency-key", key])
            self.assertEqual(rc2, 0)
            last2 = [ln for ln in buf2.getvalue().splitlines() if ln.strip()][-1]
            payload2 = json.loads(last2)
            self.assertTrue(payload2["duplicate"])
            self.assertEqual(payload2["publish_record_id"], first_record_id)


if __name__ == "__main__":
    unittest.main()
