import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("route", ROOT / "scripts/route.py")
route = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route)


class RoutingTests(unittest.TestCase):
    def test_positive_negative_proposed_phrase_routes(self):
        for line in (ROOT / "routing-eval.jsonl").read_text().splitlines():
            case = json.loads(line)
            with self.subTest(id=case["id"]):
                output = route.resolve(case["input"])
                self.assertEqual(output["route"], case["expected"])
                self.assertFalse(output["llm_evaluation"])
                self.assertFalse(output["global_resolver_registration_verified"])

    def test_manifest_skill_trigger_alignment_and_reachable_local_script(self):
        skill = (ROOT / "SKILL.md").read_text()
        trigger_text = skill.split("triggers:\n", 1)[1].split("tools:\n", 1)[0]
        triggers = re.findall(r'^  - "(.+)"$', trigger_text, re.MULTILINE)
        proposal = json.loads((ROOT / "references/routing-proposal.json").read_text())
        self.assertEqual(triggers, proposal["resolver_triggers"])
        self.assertIn("name: " + proposal["name"], skill)
        done = subprocess.run([sys.executable, str(ROOT / "scripts/route.py"), "CAPTURE GOOGLE AI CITATIONS FOR A REGIONAL COMPARISON!"], capture_output=True, text=True, timeout=5)
        self.assertEqual(done.returncode, 0)
        self.assertEqual(json.loads(done.stdout)["route"], "proxylane-web-evidence")

    def test_trigger_to_fixture_evidence_side_effect(self):
        import tempfile
        phrase = "fetch YouTube transcripts through my proxy for RAG"
        self.assertEqual(route.resolve(phrase)["route"], "proxylane-web-evidence")
        with tempfile.TemporaryDirectory() as temporary:
            done = subprocess.run([sys.executable, str(ROOT / "scripts/collect.py"), "--mode", "youtube-transcript", "--fixture", "--out", temporary], capture_output=True, text=True, timeout=10)
            self.assertEqual(done.returncode, 0)
            outcome = json.loads((Path(temporary) / "outcome.json").read_text())
            self.assertEqual(outcome["proof_mode"], "fixture")
            self.assertEqual(len(outcome["observations"]), 2)
            self.assertTrue((Path(temporary) / outcome["evidence"][0]["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
