from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class AddCaseScriptTestCase(unittest.TestCase):
    def test_add_case_script_accepts_stdin(self) -> None:
        sample_case = {
            "id": "han-wen-di-xing-jian",
            "title": "汉文帝轻徭薄赋与休养生息",
            "dynasty": "西汉",
            "era": "文景之治前期",
            "year_range": "前180年-前157年",
            "main_figures": ["汉文帝"],
            "summary": "在经历大规模动荡后，通过减负与节制动作修复基本盘。",
            "situation_tags": ["守攻抉择", "改革推进"],
            "decision_maker": "汉文帝",
            "objective": "先稳住社会与财政，再逐步恢复国家能力。",
            "visible_information": ["社会经历前期动荡", "民生恢复优先级高"],
            "hidden_constraints": ["过快扩张会重新压垮基本盘", "过强动作会刺激旧伤复发"],
            "options_available": ["继续高压征发", "先休养生息", "局部调整"],
            "chosen_action": "主动放慢动作，以恢复秩序和承受力为先。",
            "short_term_outcome": "社会压力下降，基本秩序稳定。",
            "long_term_outcome": "为后续发展积累了承受力和财政空间。",
            "success_or_failure": "success",
            "key_reasons": ["识别优先级正确", "没有在脆弱阶段过度用力"],
            "transferable_principles": ["组织脆弱时先修复承受力，往往比立刻扩张更重要。"],
            "non_transferable_factors": ["古代国家治理与现代组织经营环境不同。"],
            "modern_analogy_keywords": ["休养生息", "先稳基本盘", "减负", "恢复承受力"],
            "source_note": "《史记·孝文本纪》",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            user_cases_path = Path(temp_dir) / "user_cases.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "add_case.py"),
                    "--stdin",
                    "--user-cases-path",
                    str(user_cases_path),
                ],
                input=json.dumps(sample_case, ensure_ascii=False),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn(sample_case["id"], result.stdout)
            saved_cases = json.loads(user_cases_path.read_text(encoding="utf-8"))
            self.assertEqual(saved_cases[0]["id"], sample_case["id"])


if __name__ == "__main__":
    unittest.main()
