import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "task_efficiency_advisor.py"
SPEC = importlib.util.spec_from_file_location("task_efficiency_advisor", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def base_request(task):
    return {
        "task": task,
        "available_device": "fictional laptop",
        "privacy_requirement": "local processing only",
        "user_preferences": {"tone": "concise"},
        "data_classification": "synthetic",
    }


class AdvisorTests(unittest.TestCase):
    def test_demo_subcommand_returns_complete_synthetic_recommendation(self):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = MODULE.main(["demo"])
        result = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(result["data_classification"], "synthetic")
        self.assertEqual(result["missing_information"], [])
        self.assertEqual([item["vendor"] for item in result["quote_comparison"]], ["Fictional Cafe B", "Fictional Cafe A"])

    def test_missing_information_is_explicit(self):
        with tempfile.TemporaryDirectory() as temp:
            result = MODULE.recommend({"task": "organize work"}, Path(temp))
        self.assertEqual(result["status"], "needs_information")
        self.assertEqual(
            result["missing_information"],
            ["available_device", "privacy_requirement", "user_preferences"],
        )
        self.assertNotIn("organized_tasks", result)

    def test_total_price_comparison_includes_all_fees(self):
        request = base_request({
            "type": "compare_food_quotes",
            "quotes": [
                {"vendor": "Fictional A", "subtotal": "20.00", "fees": {"delivery": "4.00", "service": "1.50"}},
                {"vendor": "Fictional B", "subtotal": "22.00", "fees": {"delivery": "1.00", "service": "0.25"}},
            ],
        })
        with tempfile.TemporaryDirectory() as temp:
            result = MODULE.recommend(request, Path(temp))
        self.assertEqual([item["vendor"] for item in result["quote_comparison"]], ["Fictional B", "Fictional A"])
        self.assertEqual(result["quote_comparison"][0]["total"], "23.25")
        self.assertEqual(result["quote_comparison"][1]["total"], "25.50")

    def test_user_scenario_returns_no_qualifying_option(self):
        request = base_request({
            "type": "compare_food_quotes",
            "budget": "under 25",
            "party_size": 2,
            "allergies": ["peanut"],
            "quotes": [
                {"vendor": "Cafe A", "subtotal": "24.00", "fees": {"delivery": "3.80"}, "tip": "1.00", "charges_confirmed": True, "serves": 2},
                {"vendor": "Cafe B", "subtotal": "22.00", "fees": {"service": "2.00"}, "tip": "2.00", "charges_confirmed": True, "serves": 2},
            ],
        })
        with tempfile.TemporaryDirectory() as temp:
            result = MODULE.recommend(request, Path(temp))
        self.assertEqual(result["decision"], "no qualifying option")
        self.assertEqual([quote["total"] for quote in result["quote_comparison"]], ["26.00", "28.80"])
        self.assertTrue(all(not quote["qualifies"] for quote in result["quote_comparison"]))
        self.assertTrue(all(any("peanut allergen information is missing" in item for item in quote["unresolved_requirements"]) for quote in result["quote_comparison"]))
        self.assertTrue(any("below 25.00" in question for question in result["clarification_questions"]))

    def test_strict_under_budget_rejects_exact_boundary(self):
        request = base_request({
            "type": "compare_food_quotes",
            "budget": {"operator": "under", "amount": "25.00"},
            "quotes": [{"vendor": "Boundary Cafe", "subtotal": "20.00", "fees": {"delivery": "5.00"}, "tip": "0", "charges_confirmed": True}],
        })
        with tempfile.TemporaryDirectory() as temp:
            result = MODULE.recommend(request, Path(temp))
        self.assertEqual(result["decision"], "no qualifying option")
        quote = result["quote_comparison"][0]
        self.assertEqual(quote["total"], "25.00")
        self.assertIn("does not satisfy required budget < 25.00", quote["disqualifying_reasons"][0])

    def test_missing_fees_and_unknown_charges_are_unresolved(self):
        request = base_request({
            "type": "compare_food_quotes",
            "budget": "under 25",
            "quotes": [{"vendor": "Unknown Fee Cafe", "subtotal": "18.00", "unknown_charges": ["delivery", "required tip"], "charges_confirmed": False}],
        })
        with tempfile.TemporaryDirectory() as temp:
            result = MODULE.recommend(request, Path(temp))
        self.assertEqual(result["decision"], "no qualifying option")
        quote = result["quote_comparison"][0]
        self.assertIsNone(quote["total"])
        self.assertIn("fees are missing or not itemized", quote["unresolved_requirements"])
        self.assertEqual(quote["unknown_charges"], ["delivery", "required tip"])
        self.assertTrue(any("confirm the amounts" in question for question in result["clarification_questions"]))

    def test_insufficient_portions_do_not_qualify(self):
        request = base_request({
            "type": "compare_food_quotes",
            "party_size": 2,
            "quotes": [{"vendor": "Single Serve Cafe", "subtotal": "15.00", "fees": {}, "tip": "0", "charges_confirmed": True, "serves": 1}],
        })
        with tempfile.TemporaryDirectory() as temp:
            result = MODULE.recommend(request, Path(temp))
        self.assertEqual(result["decision"], "no qualifying option")
        self.assertIn("serves 1, fewer than requested party size 2", result["quote_comparison"][0]["disqualifying_reasons"])

    def test_missing_allergy_and_cross_contamination_info_stays_unresolved(self):
        request = base_request({
            "type": "compare_food_quotes",
            "allergies": ["peanut"],
            "quotes": [{"vendor": "No Allergy Data Cafe", "subtotal": "18.00", "fees": {}, "tip": "0", "charges_confirmed": True}],
        })
        with tempfile.TemporaryDirectory() as temp:
            result = MODULE.recommend(request, Path(temp))
        self.assertEqual(result["decision"], "no qualifying option")
        quote = result["quote_comparison"][0]
        self.assertFalse(quote["qualifies"])
        self.assertIn("peanut allergen information is missing", quote["unresolved_requirements"])
        self.assertIn("peanut cross-contamination information is missing", quote["unresolved_requirements"])
        self.assertTrue(any("cross-contamination" in question for question in result["clarification_questions"]))

    def test_feedback_persists_and_reuses_successful_workflow(self):
        request = base_request({
            "type": "organize_tasks_by_deadline",
            "tasks": [
                {"title": f"Fictional task {number}", "deadline": f"2027-01-0{6-number}T09:00:00"}
                for number in range(1, 6)
            ],
        })
        learned = "Use the previously successful compact deadline table."
        with tempfile.TemporaryDirectory() as temp:
            state_dir = Path(temp)
            saved = MODULE.record_feedback({
                "request": request,
                "successful": True,
                "recommended_workflow": learned,
                "feedback_note": "The compact ordering worked.",
            }, state_dir)
            self.assertTrue(saved["saved"])
            state = json.loads((state_dir / MODULE.STATE_FILE).read_text(encoding="utf-8"))
            self.assertNotIn("Fictional task", json.dumps(state))
            result = MODULE.recommend(request, state_dir)
        self.assertTrue(result["workflow_learning"]["reused"])
        self.assertEqual(result["recommended_workflow"], learned)

    def test_approval_requirements_are_marked_and_not_executed(self):
        request = base_request({
            "type": "dictated_notes_to_email_draft",
            "dictated_notes": "Thank the fictional team and request a review.",
            "recipient": "fictional@example.invalid",
            "tone": "concise",
        })
        with tempfile.TemporaryDirectory() as temp:
            result = MODULE.recommend(request, Path(temp))
        self.assertEqual(result["draft"]["send_status"], "not_sent")
        self.assertEqual(result["approval_required_actions"][0]["status"], "not_executed")
        self.assertTrue(result["steps"][-1]["approval_required"])


if __name__ == "__main__":
    unittest.main()
