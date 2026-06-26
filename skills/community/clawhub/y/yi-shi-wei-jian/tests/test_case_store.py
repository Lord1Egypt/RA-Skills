from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from case_store import CaseStore  # noqa: E402


class CaseStoreTestCase(unittest.TestCase):
    def test_add_case_appends_to_user_case_file(self) -> None:
        sample_case = {
            "id": "tang-li-jing-ping-tujue",
            "title": "李靖突袭平定东突厥",
            "dynasty": "唐",
            "era": "唐太宗时期",
            "year_range": "630年",
            "main_figures": ["李靖", "李世民"],
            "summary": "唐朝在北方威胁尚未完全整合前，抓住窗口发起快速打击，改变边境压力格局。",
            "situation_tags": ["守攻抉择", "以弱对强"],
            "decision_maker": "李世民",
            "objective": "通过主动出击削弱持续性边境威胁。",
            "visible_information": ["东突厥内部并不稳固", "唐军需要速战速决"],
            "hidden_constraints": ["补给线拉长风险高", "如果首击失利会暴露北线空虚"],
            "options_available": ["继续防守", "小规模试探", "集中突袭"],
            "chosen_action": "抓住对手失序窗口，授权李靖快速突袭。",
            "short_term_outcome": "东突厥主力受挫，北方压力显著下降。",
            "long_term_outcome": "唐朝边境形势改善，战略主动权提升。",
            "success_or_failure": "success",
            "key_reasons": ["抓住窗口期", "指挥权集中", "行动速度快于对手调整速度"],
            "transferable_principles": ["窗口期来临时，有限但果断的出击可能优于长期被动消耗"],
            "non_transferable_factors": ["古代骑兵与边境战略环境无法直接照搬到现代组织"],
            "modern_analogy_keywords": ["窗口期", "主动出击", "速战速决", "先发制人"],
            "source_note": "《旧唐书·李靖传》",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            user_cases_path = Path(temp_dir) / "user_cases.json"
            store = CaseStore(REPO_ROOT / "data" / "historical_cases.json", user_cases_path)
            added_case = store.add_case(sample_case)

            self.assertEqual(added_case["id"], sample_case["id"])
            saved_cases = json.loads(user_cases_path.read_text(encoding="utf-8"))
            self.assertEqual(len(saved_cases), 1)
            self.assertEqual(saved_cases[0]["title"], sample_case["title"])

    def test_retriever_can_load_user_cases(self) -> None:
        sample_case = {
            "id": "song-yue-fei-bei-fa",
            "title": "岳飞北伐与后方掣肘",
            "dynasty": "南宋",
            "era": "宋金对峙",
            "year_range": "1140年-1141年",
            "main_figures": ["岳飞", "宋高宗", "秦桧"],
            "summary": "前线推进存在战机，但后方政治目标与前线战略目标并不一致，导致节奏被打断。",
            "situation_tags": ["守攻抉择", "内部冲突"],
            "decision_maker": "宋高宗",
            "objective": "在前线作战与内部政治稳定之间做取舍。",
            "visible_information": ["前线已有战果", "内部意见并不统一"],
            "hidden_constraints": ["和战路线冲突", "前线胜利可能反过来改变内部权力平衡"],
            "options_available": ["继续北伐", "转入守势", "边打边谈"],
            "chosen_action": "通过召回与议和打断前线节奏。",
            "short_term_outcome": "内部控制更稳，但错失前线扩大战果的窗口。",
            "long_term_outcome": "长期战略主动权受损，内部与外部目标持续错位。",
            "success_or_failure": "mixed",
            "key_reasons": ["内部目标不一致", "前后方节奏失配", "政治安全压过战略收益"],
            "transferable_principles": ["前线动作必须和后方真实目标一致，否则战果难以转化为结构优势"],
            "non_transferable_factors": ["宋金时期的军政结构与现代组织决策环境不同"],
            "modern_analogy_keywords": ["后方掣肘", "前后方目标不一致", "内部目标冲突", "推进被叫停"],
            "source_note": "《宋史·岳飞传》",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            user_cases_path = Path(temp_dir) / "user_cases.json"
            store = CaseStore(REPO_ROOT / "data" / "historical_cases.json", user_cases_path)
            store.add_case(sample_case)
            cases = store.load_all_cases()

            self.assertTrue(any(case["id"] == sample_case["id"] for case in cases))
