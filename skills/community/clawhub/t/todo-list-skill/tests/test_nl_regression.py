# todos/tests/test_nl_regression.py
# NLP 回归测试（用 data/test_cases.json 驱动）
# 版本：v1.0 | 日期：2026-06-11

import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.nl_parser import NLParser


class TestNLRegression(unittest.TestCase):
    """从 data/test_cases.json 加载并跑回归测试"""

    @classmethod
    def setUpClass(cls):
        cls.test_cases_path = Path(__file__).parent.parent / "data" / "test_cases.json"
        with open(cls.test_cases_path, encoding="utf-8") as f:
            cls.cases = json.load(f)
        cls.parser = NLParser()

    def test_case_count(self):
        """[OK] test_cases.json 至少 20 个 case"""
        self.assertGreaterEqual(len(self.cases), 20)

    def test_all_cases(self):
        """[OK] 所有 case 通过"""
        failed = []
        for case in self.cases:
            input_text = case["input"]
            expected = case["expected"]
            actual = self.parser.parse(input_text)

            # 检查 action
            if "action" in expected:
                if actual["action"] != expected["action"]:
                    failed.append(
                        f"Case {case['id']} '{input_text}': "
                        f"action expected={expected['action']}, got={actual['action']}"
                    )
                    continue

            # 检查 content_contains
            if "content_contains" in expected:
                if expected["content_contains"] not in actual["content"]:
                    failed.append(
                        f"Case {case['id']} '{input_text}': "
                        f"content should contain '{expected['content_contains']}', got='{actual['content']}'"
                    )
                    continue

            # 检查 due_at
            if "due_at_contains" in expected:
                if actual["due_at"] is None or expected["due_at_contains"] not in actual["due_at"]:
                    failed.append(
                        f"Case {case['id']} '{input_text}': "
                        f"due_at should contain '{expected['due_at_contains']}', got='{actual['due_at']}'"
                    )
                    continue

            if "due_at" in expected and expected["due_at"] is None:
                if actual["due_at"] is not None:
                    failed.append(
                        f"Case {case['id']} '{input_text}': "
                        f"due_at should be None, got='{actual['due_at']}'"
                    )
                    continue

            # 检查 priority
            if "priority" in expected:
                if actual["priority"] != expected["priority"]:
                    failed.append(
                        f"Case {case['id']} '{input_text}': "
                        f"priority expected={expected['priority']}, got={actual['priority']}"
                    )
                    continue

            # 检查 tags_contains
            if "tags_contains" in expected:
                for tag in expected["tags_contains"]:
                    if tag not in actual["tags"]:
                        failed.append(
                            f"Case {case['id']} '{input_text}': "
                            f"tags should contain '{tag}', got={actual['tags']}"
                        )
                        break
                continue

        if failed:
            self.fail("\n".join(failed))

    def test_data_directory(self):
        """[OK] data/ 目录存在"""
        data_dir = Path(__file__).parent.parent / "data"
        self.assertTrue(data_dir.exists())
        self.assertTrue((data_dir / "user_dict.txt").exists())
        self.assertTrue((data_dir / "time_keywords.txt").exists())
        self.assertTrue((data_dir / "test_cases.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)