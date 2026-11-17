#!/usr/bin/env python3
"""Regression tests for scripts/save_discovery_deliverables.py.

The defect this file exists for is an absence, which is why it needs a test rather than a reader.
check_shortlist_consistency.py is the largest gate in this skill after the plan checker -- it refuses a winner that
fails a hard constraint, a winner named when no candidate was feasible, a candidate scored with no
evidence, a per-person figure compared against a whole-party one. In a real workspace holding
fifteen saved intakes, the number of shortlist files was ZERO: the gate had never run on a single
real Discovery, so none of what it refuses had ever been refused.

The reason was structural. Construction has one mandatory door that prints two paths, and SKILL.md
makes a task incomplete without them. Discovery had the gate and no door -- a command inside a
paragraph, an output nobody was told where to put, and a run that skipped both looking exactly like
a run that did neither.

So what is asserted here is not "the script works". It is the four properties that make a Discovery
run observable at all: the gate cannot be disarmed by silence, a failing shortlist writes nothing,
the saved file records whether the constraint check was armed, and the path is printed.

Run:  python tests/test_save_discovery.py
      python -m pytest tests/test_save_discovery.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "save_discovery_deliverables.py"
FIXTURE = ROOT / "tests" / "discovery-shortlist-fixture.json"


def run(*args: str) -> tuple[int, str, str]:
    proc = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def saved_files(workspace: Path) -> list[Path]:
    return sorted((workspace / "plans").glob("shortlist-*.json"))


def main() -> int:
    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{label}{': ' + detail if detail else ''}")

    shortlist = json.loads(FIXTURE.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        path = tmp / "shortlist.json"
        path.write_text(json.dumps(shortlist, ensure_ascii=False), encoding="utf-8")
        intake = tmp / "intake.json"
        intake.write_text(json.dumps({"constraint_registry": [], "feasibility": {}},
                                     ensure_ascii=False), encoding="utf-8")

        # 1. Silence must not be an answer. This is the same pair as --verification/--unverified
        #    and check_shortlist_consistency's own --intake/--no-intake, and for the reason written
        #    at all three: an exit 0 is what an assistant reads, so a check that can be skipped by
        #    saying nothing is a check that reports clean on the run that motivated it.
        code, out, err = run(str(path), "--workspace", str(tmp / "silent"))
        check("neither flag is refused", code != 0, f"exit {code}")
        check("the refusal names both ways out",
              "--intake" in err and "--no-intake" in err, err[:200])
        check("nothing was written on a refusal", not (tmp / "silent").exists(),
              "a workspace was created for a run that refused")

        code, out, err = run(str(path), "--workspace", str(tmp / "both"),
                             "--intake", str(intake), "--no-intake")
        check("both flags together are refused", code != 0, f"exit {code}: {out}{err}")

        # 2. The armed path writes, prints the receipt, and records that it was armed.
        armed = tmp / "armed"
        code, out, err = run(str(path), "--workspace", str(armed), "--intake", str(intake))
        check("an armed save succeeds", code == 0, f"exit {code}: {out}{err}")
        files = saved_files(armed)
        check("exactly one shortlist was written", len(files) == 1, f"{files}")
        check("the path is printed", "Shortlist JSON:" in out, out)
        if files:
            check("the printed path is the file that exists", str(files[0]) in out, out)
            stamp = json.loads(files[0].read_text(encoding="utf-8")).get("gates_passed") or {}
            check("the stamp records the armed constraint check",
                  stamp.get("constraint_coverage") == "armed", f"{stamp}")
            check("the stamp records what ran",
                  isinstance(stamp.get("checks"), int) and stamp["checks"] > 1, f"{stamp}")

        # 3. The escape hatch costs visibility, not silence -- and it is recorded IN THE FILE,
        #    because the printed note scrolls past and the file is what a later audit reads.
        opted = tmp / "opted"
        code, out, err = run(str(path), "--workspace", str(opted), "--no-intake")
        check("a --no-intake save succeeds", code == 0, f"exit {code}: {out}{err}")
        check("--no-intake says so on the way out", "NOT been tested" in out, out)
        files = saved_files(opted)
        if files:
            stamp = json.loads(files[0].read_text(encoding="utf-8")).get("gates_passed") or {}
            check("the file itself records that the check did not run",
                  stamp.get("constraint_coverage") == "not run", f"{stamp}")

        # 4. A shortlist that fails its gate writes NOTHING. A partial artifact is worse than
        #    none: it is indistinguishable from a passing one to everything downstream.
        broken = dict(shortlist)
        broken["outcome"] = {"state": "shortlist"}
        broken["candidates"] = []
        bad_path = tmp / "broken.json"
        bad_path.write_text(json.dumps(broken, ensure_ascii=False), encoding="utf-8")
        failing = tmp / "failing"
        code, out, err = run(str(bad_path), "--workspace", str(failing), "--no-intake")
        if code == 0:
            failures.append("a shortlist claiming a shortlist outcome with no candidates was "
                            "saved; the gate has to refuse before anything is written")
        else:
            check("a failing shortlist writes nothing", not saved_files(failing),
                  f"{saved_files(failing)}")
            check("the failure says what to do", "Nothing was written" in err, err[-300:])

        # 5. Two saves of one run collide, so a second one has to announce itself. The measured
        #    version of the alternative is in SKILL.md: two plans in one workspace differing only
        #    by origin, one of them wrong, and nothing to tell a reader which was which.
        code, out, err = run(str(path), "--workspace", str(armed), "--intake", str(intake))
        check("a second save of the same run collides", code != 0, f"exit {code}: {out}")
        check("the collision names the way through",
              "--overwrite" in err or "--slug" in err, err[-200:])
        code, out, err = run(str(path), "--workspace", str(armed), "--intake", str(intake),
                             "--overwrite")
        check("--overwrite goes through", code == 0, f"exit {code}: {out}{err}")
        check("and still exactly one file", len(saved_files(armed)) == 1, f"{saved_files(armed)}")

        # 6. The shapes a caller can actually hand over. A traceback here is a worse answer than a
        #    refusal, because it names a Python type instead of the file that was wrong.
        for label, body in (("a bare list", "[]"), ("a string", '"nope"'),
                            ("truncated JSON", '{"candidates":'), ("empty file", "")):
            odd = tmp / f"odd-{abs(hash(label))}.json"
            odd.write_text(body, encoding="utf-8")
            code, out, err = run(str(odd), "--workspace", str(tmp / "odd"), "--no-intake")
            check(f"{label} is refused", code != 0, f"exit {code}")
            check(f"{label} refuses without a traceback", "Traceback" not in err, err[-200:])
        code, out, err = run(str(tmp / "does-not-exist.json"), "--workspace", str(tmp / "missing"),
                             "--no-intake")
        check("a missing shortlist is refused without a traceback",
              code != 0 and "Traceback" not in err, err[-200:])

        # 7. CJK in the slug, because the workspace this runs on is majority Chinese and a name
        #    that only survives ASCII would not survive a single real run.
        cjk = tmp / "cjk"
        code, out, err = run(str(path), "--workspace", str(cjk), "--no-intake",
                             "--slug", "阿姆斯特丹 出发 / 地中海")
        check("a CJK slug saves", code == 0, f"exit {code}: {out}{err}")
        files = saved_files(cjk)
        if files:
            check("the CJK slug survives unescaped and without a path separator",
                  "阿姆斯特丹" in files[0].name and "/" not in files[0].name, files[0].name)

    if failures:
        print(f"SAVE DISCOVERY FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all save-discovery cases passed")
    return 0


def test_save_discovery() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
