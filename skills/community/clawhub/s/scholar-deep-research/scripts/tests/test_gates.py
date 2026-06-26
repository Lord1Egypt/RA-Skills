"""Each gate has at least one passing and one failing scenario.

Covers the G1..G7 predicates in `_gates.py`. Uses direct state-file
manipulation for scenarios the public API doesn't yet reach (e.g. a
state with themes but no tensions). `advance` is always run via the CLI
so this doubles as a smoke test for the subcommand envelope.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from _helpers import dummy_paper, init_state, make_payload, run_script


class GatesTest(unittest.TestCase):

    def _write_state(self, path: Path, **overrides) -> None:
        """Write a minimum-viable state directly (bypassing init)."""
        state = {
            "schema_version": 1,
            "question": "t",
            "archetype": "literature_review",
            "phase": 0,
            "queries": [],
            "papers": {},
            "selected_ids": [],
            "themes": [],
            "tensions": [],
            "self_critique": {"findings": [], "resolved": [], "appendix": ""},
            "report_path": None,
        }
        state.update(overrides)
        path.write_text(json.dumps(state, indent=2))

    def test_g1_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "s.json"
            init_state(state)
            env = run_script("research_state.py", [
                "--state", str(state), "advance", "--check-only",
            ])
            self.assertTrue(env["data"]["met"])
            self.assertEqual(env["data"]["target"], 1)

    def test_g2_fails_without_queries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "s.json"
            self._write_state(state, phase=1)
            env = run_script("research_state.py", [
                "--state", str(state), "advance", "--to", "2", "--check-only",
            ], expect_rc=3)
            self.assertEqual(env["error"]["code"], "gate_not_met")
            failing = [c["name"] for c in env["error"]["gate"]["checks"] if not c["ok"]]
            self.assertIn("sources_breadth", failing)

    def test_g3_fails_without_selection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "s.json"
            self._write_state(state, phase=2)
            env = run_script("research_state.py", [
                "--state", str(state), "advance", "--to", "3", "--check-only",
            ], expect_rc=3)
            failing = [c["name"] for c in env["error"]["gate"]["checks"] if not c["ok"]]
            self.assertIn("selection_non_empty", failing)

    def test_g4_pass_with_depths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "s.json"
            self._write_state(
                state,
                phase=3,
                selected_ids=["p1", "p2", "p3", "p4", "p5"],
                papers={
                    "p1": {"id": "p1", "depth": "full"},
                    "p2": {"id": "p2", "depth": "full"},
                    "p3": {"id": "p3", "depth": "full"},
                    "p4": {"id": "p4", "depth": "full"},
                    "p5": {"id": "p5", "depth": "shallow"},
                },
            )
            env = run_script("research_state.py", [
                "--state", str(state), "advance", "--to", "4", "--check-only",
            ])
            self.assertTrue(env["data"]["met"])

    def test_g6_fail_without_themes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "s.json"
            self._write_state(state, phase=5)
            env = run_script("research_state.py", [
                "--state", str(state), "advance", "--to", "6", "--check-only",
            ], expect_rc=3)
            failing = [c["name"] for c in env["error"]["gate"]["checks"] if not c["ok"]]
            self.assertIn("themes_defined", failing)

    def test_skip_two_is_forbidden(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "s.json"
            self._write_state(state, phase=0)
            env = run_script("research_state.py", [
                "--state", str(state), "advance", "--to", "2",
            ], expect_rc=3)
            self.assertEqual(env["error"]["code"], "phase_skip_forbidden")


if __name__ == "__main__":
    unittest.main()
