from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from classifier import SituationClassifier  # noqa: E402
from retriever import CaseRetriever  # noqa: E402


class RetrievalTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.classifier = SituationClassifier()
        self.retriever = CaseRetriever(REPO_ROOT / "data" / "historical_cases.json")

    def test_alliance_query_prefers_alliance_cases(self) -> None:
        question = "我们必须联合一个不完全信任的合作方，对抗更强的头部竞争者，但我担心项目一推进对方就翻脸。"
        assessment = self.classifier.classify(question)
        cases = self.retriever.retrieve(question, assessment, top_k=3)
        titles = {case["title"] for case in cases}

        self.assertEqual(assessment.primary, "联盟不稳")
        self.assertIn("孙刘联盟赤壁抗曹", titles)
        self.assertTrue(
            {"郭子仪单骑说回纥", "六国合纵抗秦反复失效"} & titles,
            msg=f"联盟查询未命中预期案例: {titles}",
        )

    def test_reform_query_keeps_counterexample(self) -> None:
        question = "团队里很多人表面支持改革，实际拖延执行，我资源不多，但要推动新制度上线。"
        assessment = self.classifier.classify(question)
        cases = self.retriever.retrieve(question, assessment, top_k=3)

        self.assertEqual(assessment.primary, "改革推进")
        self.assertTrue(any(case["success_or_failure"] != "success" for case in cases))

    def test_branch_control_query_hits_split_and_centralization_cases(self) -> None:
        question = "几个大区负责人已经尾大不掉，总部一直拖着不敢动。我如果现在收权，可能一起反弹。"
        assessment = self.classifier.classify(question)
        cases = self.retriever.retrieve(question, assessment, top_k=3)
        titles = {case["title"] for case in cases}

        self.assertIn(assessment.primary, {"权力控制", "内部冲突"})
        self.assertTrue(
            {"汉武帝行推恩令", "康熙削三藩并平定叛乱", "裴度督战平淮西"} & titles,
            msg=f"地方割据/收权查询未命中预期案例: {titles}",
        )

    def test_user_case_can_be_retrieved(self) -> None:
        sample_case = {
            "id": "jin-xie-an-fei-shui",
            "title": "谢安统筹淝水之战前后方协同",
            "dynasty": "东晋",
            "era": "东晋十六国",
            "year_range": "383年",
            "main_figures": ["谢安", "谢玄", "苻坚"],
            "summary": "前线作战与后方统筹需要同步稳定，否则临战易失序。",
            "situation_tags": ["守攻抉择", "内部冲突"],
            "decision_maker": "谢安",
            "objective": "在强敌来压时维持前后方节奏一致，避免内部自乱。",
            "visible_information": ["前线压力很大", "内部必须保持稳定"],
            "hidden_constraints": ["前后方节奏失配会放大战场风险", "内部恐慌会削弱执行力"],
            "options_available": ["全面收缩", "稳定后方后有限应对", "仓促决战"],
            "chosen_action": "稳住后方节奏，同时支持前线抓住战机。",
            "short_term_outcome": "内部秩序稳定，前线执行更集中。",
            "long_term_outcome": "前后方目标一致时，弱势方也能放大战果。",
            "success_or_failure": "success",
            "key_reasons": ["后方稳定", "前后方目标一致", "没有被恐慌打乱节奏"],
            "transferable_principles": ["关键阶段要先稳住后方节奏，再让前线动作兑现。"],
            "non_transferable_factors": ["古代战场环境与现代组织场景并不相同。"],
            "modern_analogy_keywords": ["后方掣肘", "前后方协同", "推进被叫停", "内部先稳住"],
            "source_note": "《晋书·谢安传》",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            user_cases_path = Path(temp_dir) / "user_cases.json"
            user_cases_path.write_text(json.dumps([sample_case], ensure_ascii=False, indent=2), encoding="utf-8")
            retriever = CaseRetriever(REPO_ROOT / "data" / "historical_cases.json", user_cases_path)
            question = "前线已经有成果，但后方一直掣肘，推进总被叫停，我该先稳内部还是继续往前推？"
            assessment = self.classifier.classify(question)
            cases = retriever.retrieve(question, assessment, top_k=3)

            self.assertTrue(any(case["id"] == sample_case["id"] for case in cases))


if __name__ == "__main__":
    unittest.main()
