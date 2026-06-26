from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class CLITestCase(unittest.TestCase):
    def test_cli_outputs_required_sections(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "src" / "main.py"),
                "--question",
                "公司内部两派冲突严重，我资源偏弱，但两个月内必须推进新制度。",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        for section in [
            "【局面判断】",
            "【历史参照】",
            "【关键变量】",
            "【可选路径】",
            "【沙盘推演】",
            "【借鉴原则】",
            "【边界提醒】",
        ]:
            self.assertIn(section, result.stdout)

    def test_cli_can_print_case_template(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "src" / "main.py"),
                "--print-case-template",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn('"id": "new-historical-case-id"', result.stdout)

    def test_cli_can_add_case_from_json(self) -> None:
        sample_case = {
            "id": "ming-zhang-ju-zheng-kao-cheng",
            "title": "张居正推行考成法",
            "dynasty": "明",
            "era": "明神宗初年",
            "year_range": "1573年-1582年",
            "main_figures": ["张居正", "明神宗"],
            "summary": "通过考核与责任链压实执行，短期提升行政效率，但也累积了政治反弹。",
            "situation_tags": ["改革推进", "内部冲突"],
            "decision_maker": "张居正",
            "objective": "整顿行政执行链，提高政策落地能力。",
            "visible_information": ["行政疲沓", "顶层支持仍在"],
            "hidden_constraints": ["改革得罪既得利益", "执行强化会带来后续政治反弹"],
            "options_available": ["维持旧制", "局部整顿", "全面考成"],
            "chosen_action": "推动考成法，强化考核和责任追踪。",
            "short_term_outcome": "执行效率提升，政策推动速度加快。",
            "long_term_outcome": "改革成果部分保留，但政治反扑也很明显。",
            "success_or_failure": "mixed",
            "key_reasons": ["执行链压实", "顶层背书存在", "利益受损方反弹强"],
            "transferable_principles": ["改革要同时考虑执行效率提升和后续反弹管理。"],
            "non_transferable_factors": ["晚明政治结构与现代组织不同。"],
            "modern_analogy_keywords": ["执行链", "考核压实", "改革反弹", "责任追踪"],
            "source_note": "《明史·张居正传》",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            user_cases_path = Path(temp_dir) / "user_cases.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "src" / "main.py"),
                    "--add-case-json",
                    json.dumps(sample_case, ensure_ascii=False),
                    "--user-cases-path",
                    str(user_cases_path),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn(sample_case["id"], result.stdout)
            saved_cases = json.loads(user_cases_path.read_text(encoding="utf-8"))
            self.assertEqual(saved_cases[0]["id"], sample_case["id"])


if __name__ == "__main__":
    unittest.main()
