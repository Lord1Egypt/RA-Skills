import unittest

import latex_convert.candidate_pipeline as candidate_pipeline
from latex_convert.detect import is_formula_like, split_formula_spans
from latex_convert.math_parser import Frac, Seq, parse_formula
from latex_convert.omml import node_to_omath
from latex_convert.ooxml_transform import is_bibliography_entry, is_bibliography_heading
from latex_convert.candidate_pipeline import Candidate, ScanResult, decide_with_ai, default_action_for, score_candidate
from latex_convert.preview import formula_to_latex


class MathParserTests(unittest.TestCase):
    def test_fraction_binds_to_adjacent_terms(self) -> None:
        ast = parse_formula("(P_A-MC_i)/P_A=s_i/ε_A")
        self.assertIsInstance(ast, Seq)
        self.assertEqual(sum(isinstance(item, Frac) for item in ast.items), 2)

    def test_omml_contains_editable_fraction_nodes(self) -> None:
        omath = node_to_omath(parse_formula("(P_A-MC_i)/P_A=s_i/ε_A"))
        ns = {"m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}
        self.assertEqual(len(omath.xpath(".//m:f", namespaces=ns)), 2)
        self.assertIn("MC", "".join(omath.xpath(".//m:t/text()", namespaces=ns)))

    def test_latex_fraction_from_ai_output(self) -> None:
        omath = node_to_omath(parse_formula(r"$\frac{P_A - MC_i}{P_A} = \frac{s_i}{\epsilon_A}$"))
        ns = {"m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}
        self.assertEqual(len(omath.xpath(".//m:f", namespaces=ns)), 2)
        text = "".join(omath.xpath(".//m:t/text()", namespaces=ns))
        self.assertIn("ε", text)

    def test_split_sum_script_from_word_runs(self) -> None:
        omath = node_to_omath(parse_formula("∑_iD_{i,t}≤D_t"))
        xml = str(omath.xpath(".//m:t/text()", namespaces={
            "m": "http://schemas.openxmlformats.org/officeDocument/2006/math"
        }))
        self.assertIn("∑", xml)
        self.assertIn("≤", xml)

    def test_bibliography_detection(self) -> None:
        self.assertTrue(is_bibliography_heading("参考文献："))
        self.assertTrue(is_bibliography_heading("References"))
        self.assertTrue(
            is_bibliography_entry(
                "[12] Aghion, P. Econometrica, 1992, 60(2): 323-351. https://doi.org/x"
            )
        )
        self.assertFalse(is_bibliography_entry("P_A<P_H   且   P_A>MC_A。"))

    def test_candidate_scoring_keeps_links_low_confidence(self) -> None:
        score, _ = score_candidate("https://doi.org/10.1257/aer.20160696", "https://doi.org/10.1257/aer.20160696")
        self.assertLess(score, 0.55)
        self.assertEqual(default_action_for("A_t", "变量 A_t 上升。", 0.57, "balanced"), "convert")

    def test_english_prose_and_feature_codes_are_not_auto_converted(self) -> None:
        self.assertFalse(is_formula_like("10.3 Train/Validation/Testing Split"))
        self.assertFalse(
            is_formula_like(
                "Common evaluation metrics include accuracy, precision, recall, F1-score, and the area under the receiver operating characteristic (AUC-ROC) curve."
            )
        )
        score, _ = score_candidate("RET_1, RET_3, RET_7", "RET_1, RET_3, RET_7")
        self.assertEqual(default_action_for("RET_1, RET_3, RET_7", "RET_1, RET_3, RET_7", score, "balanced"), "review")
        formula = "Π_{m,t}^{after}=∑_{i=1}^{N}θ_{m,i,t}Π_{i,t}^{after}"
        score, _ = score_candidate(formula, formula)
        self.assertEqual(default_action_for(formula, formula, score, "balanced"), "convert")
        budget = "P_{C,t}C_{m,t}+B_{m,t+1}+Q_tK_{m,t+1}=(1+r_t)B_{m,t}+[R_{K,t}+(1-δ)Q_t]K_{m,t}+(1-τ^L_t)(W_{O,t}e_{O,m}L^O_{m,t}+W_{A,t}e_{A,m}L^A_{m,t})+Π^{after}_{m,t}+RD_{m,t}+TR_{m,t}-TAX^{lump}_{m,t}"
        self.assertTrue(is_formula_like(budget))

    def test_script_with_script_ell_is_not_split(self) -> None:
        text = "生产函数为 Y_{i,t}=A_tD_{i,t}^{γ}(K_{i,t}^{α}T_{i,t}^{1-α})^{η}L_{A,i,t}^{ℓ}，其中 ℓ≥0。"
        formulas = [value for value, is_formula, *_ in split_formula_spans(text) if is_formula]
        self.assertIn("Y_{i,t}=A_tD_{i,t}^{γ}(K_{i,t}^{α}T_{i,t}^{1-α})^{η}L_{A,i,t}^{ℓ}", formulas)
        self.assertIn("ℓ≥0", formulas)

    def test_script_capital_r_is_not_split(self) -> None:
        text = "数据存量演化为 D_{t+1}=(1-δ_D)D_t+Ψ(Y_{A,t},C_{A,t},U_t,ℛ_t)-χ_PPrivacy_t，其中 ℛ_t 表示规则。"
        formulas = [value for value, is_formula, *_ in split_formula_spans(text) if is_formula]
        self.assertIn("D_{t+1}=(1-δ_D)D_t+Ψ(Y_{A,t},C_{A,t},U_t,ℛ_t)-χ_PPrivacy_t", formulas)
        self.assertIn("ℛ_t", formulas)
        self.assertNotIn("_t", formulas)

    def test_latex_preview_separates_greek_commands_from_letters(self) -> None:
        self.assertIn(r"\beta E", formula_to_latex("βE_t"))
        self.assertNotIn(r"\betaE", formula_to_latex("βE_t"))
        self.assertIn(r"\mu E", formula_to_latex("μE_t"))

    def test_ai_failure_falls_back_to_rule_decisions(self) -> None:
        scan = ScanResult(
            input="input.docx",
            prepared_docx="prepared.docx",
            engine="already-docx",
            mode="balanced",
            source_sha256="abc",
            candidates=[
                Candidate("F00001", "word/document.xml", 1, 1, 1, 0, 3, "A_t", "A_t", "A_t", 0.57, "convert", "script"),
                Candidate("F00002", "word/document.xml", 1, 2, 1, 0, 5, "RET_1", "RET_1", "RET_1", 0.1, "review", "feature-code-like"),
            ],
        )
        original = candidate_pipeline._decide_candidates_with_ai
        failures = []
        progress = []

        def fail(*args, **kwargs):
            raise RuntimeError("simulated AI failure")

        try:
            candidate_pipeline._decide_candidates_with_ai = fail
            decisions = decide_with_ai(
                scan,
                api_key="x",
                base_url="https://invalid.localhost/v1",
                model="test",
                batch_size=2,
                max_workers=1,
                retries=1,
                failure_fallback="rule",
                failure_callback=lambda *event: failures.append(event),
                progress_callback=lambda *event: progress.append(event),
            )
        finally:
            candidate_pipeline._decide_candidates_with_ai = original

        self.assertEqual(decisions, {"F00001": "convert", "F00002": "review"})
        self.assertEqual(len(failures), 1)
        self.assertEqual(len(progress), 2)
        self.assertIn("fallback-rule", progress[0][3])


if __name__ == "__main__":
    unittest.main()
