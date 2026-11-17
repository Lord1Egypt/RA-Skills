#!/usr/bin/env python3
"""A path inside a plan is a request, not an instruction.

Two places took a filesystem path out of the plan JSON and opened it:
`check_preferences_came_from_the_intake` reads `intake_context.intake_file`, and
`resolve_plan_imagery` reads `imagery_sidecar`. Both are load-bearing and neither may be removed --
the first is the only thing that compares a plan against what the traveller actually typed, and the
second is how photographs stay out of a two-megabyte plan file.

Why that is a security question and not a style one: this repo deliberately treats a plan as a
PORTABLE document. SKILL.md and the imagery module both say so in as many words -- re-rendered,
replanned weeks later, audited from a moved workspace, restored from backup. A document that
travels is a document that can arrive from somebody else, and running a gate on it should not open
`~/.ssh/id_rsa`.

The two leaks were not symmetrical, and the sidecar was the worse one. The intake path yields an
existence oracle (the note quotes the OS error, which separates "no such file" from "permission
denied") plus the strings of any JSON object that happens to carry `experience.ranked_must_haves`.
The sidecar's bytes are decoded and embedded into the delivered page as data: URIs -- so anything
readable that parses as image slots leaves the machine inside an artifact the traveller then shares.

Neither is fixed by refusing to read: both fixes keep every legitimate path working, and are scoped
to what the contract already promised those files would be.

Run:  python tests/test_path_scoping.py
      python -m pytest tests/test_path_scoping.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_plan_consistency import check_preferences_came_from_the_intake  # noqa: E402
from fetch_plan_imagery import ImagerySidecarError, resolve_plan_imagery  # noqa: E402

# Real targets, named rather than genericised, because "a path outside the workspace" is the kind of
# phrasing a later refactor satisfies while still opening the file.
OFF_LIMITS = (
    "/etc/passwd",
    "~/.ssh/id_rsa",
    "~/.aws/credentials",
    "/proc/self/environ",
    "~/Library/Cookies/Cookies.binarycookies",
    "/a/workspace/plans/../../../../etc/hosts",
)


def main() -> int:
    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{label}{': ' + detail if detail else ''}")

    # 1. intake_file. Scoped by FILENAME, because the directory cannot be: --from-intake accepts
    #    any file the operator names, and the first version of this fix demanded a parent named
    #    `plans` and broke this repo's own fixtures. Nothing worth stealing is called intake*.json.
    for target in OFF_LIMITS:
        notes: list[str] = []
        errors: list[str] = []
        check_preferences_came_from_the_intake(
            {"intake_context": {"intake_file": target}, "trip": {}}, errors, notes)
        check(f"intake_file refuses {target}",
              bool(notes) and "NOT opened" in notes[0],
              f"errors={errors[:1]} notes={notes[:1]}")
        # The refusal must not become an error, or a plan whose workspace moved stops rendering --
        # the exact regression this file's docstring says was tried and reverted once already.
        check(f"refusing {target} is a note, never an error", not errors, f"{errors[:1]}")

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        # 2. The legitimate case must still CROSS-CHECK, not merely not-crash. A guard that quietly
        #    stops the comparison from ever running would pass a test that only looked for silence.
        for name in ("intake.json", "intake-20260902-1200-lisbon.json"):
            intake = tmp / name
            intake.write_text(json.dumps(
                {"experience": {"ranked_must_haves": ["海岸线", "老城"]}}, ensure_ascii=False),
                encoding="utf-8")
            errors, notes = [], []
            check_preferences_came_from_the_intake(
                {"intake_context": {"intake_file": str(intake)},
                 "trip": {"traveler_preferences": {"ranked_must_haves": ["海岸线"]}}}, errors, notes)
            check(f"{name} is still read and still catches a dropped must-have",
                  bool(errors) and "老城" in errors[0], f"errors={errors[:1]} notes={notes[:1]}")

        # A FIFO is a regular-looking path that never returns, and `is_file()` is what refuses
        # it. Probed in a SUBPROCESS with a timeout, because the obvious version of this test --
        # call the check directly -- does not fail when the guard is removed. It HANGS, taking the
        # whole suite with it, which is worse than the bug: a run that never finishes reports
        # nothing at all. Measured while mutation-testing this very file.
        fifo = tmp / "intake-fifo.json"
        try:
            import os
            os.mkfifo(fifo)
        except (AttributeError, OSError):
            fifo = None
        if fifo is not None:
            probe = (
                "import sys, json; sys.path.insert(0, %r);"
                "from check_plan_consistency import check_preferences_came_from_the_intake as c;"
                "n = []; c({'intake_context': {'intake_file': %r}, 'trip': {}}, [], n);"
                "print(json.dumps(n))" % (str(ROOT / "scripts"), str(fifo))
            )
            try:
                done = subprocess.run([sys.executable, "-c", probe],
                                      capture_output=True, text=True, timeout=10)
                reported = json.loads(done.stdout or "[]")
                check("a FIFO named intake*.json is refused rather than opened",
                      bool(reported) and "not a regular file" in reported[0], f"{reported[:1]}")
            except subprocess.TimeoutExpired:
                failures.append("opening a FIFO named intake*.json blocked forever; the "
                                "is_file() guard is gone and this gate can be hung by a plan")
            except ValueError:
                failures.append(f"the FIFO probe printed nothing usable: {done.stdout[:120]!r}")

        # 3. imagery_sidecar. Scoped to the plan's own DIRECTORY, which is what the sidecar contract
        #    already promised ("beside the plan"), so an absolute path that really is beside the
        #    plan keeps working -- the module documents that hand-edited absolute values must.
        plan_path = tmp / "plan.json"
        beside = tmp / "plan-imagery.json"
        beside.write_text(json.dumps({"hero": {}}), encoding="utf-8")

        payload, found = resolve_plan_imagery({"imagery_sidecar": "plan-imagery.json"}, plan_path)
        check("a sidecar beside the plan is read", found is not None and found.name == beside.name,
              f"{found}")
        payload, found = resolve_plan_imagery({"imagery_sidecar": str(beside)}, plan_path)
        check("an absolute path that is beside the plan still works", found is not None, f"{found}")
        # The reported path must not be silently rewritten through symlinks: on macOS the temp dir
        # is /var/... and resolves to /private/var/..., and returning the resolved form changed what
        # every caller and test saw for a check that had already passed.
        check("the reported path is not rewritten by the check",
              found is not None and str(found).startswith(str(tmp)), f"{found} vs {tmp}")

        for escape in ("../../../../etc/hosts", "/etc/hosts", "~/.ssh/id_rsa"):
            try:
                resolve_plan_imagery({"imagery_sidecar": escape}, plan_path)
            except ImagerySidecarError as exc:
                check(f"the sidecar refusal of {escape} says where it may live",
                      "outside the plan's own directory" in str(exc), str(exc)[:160])
            else:
                failures.append(f"imagery_sidecar opened {escape}; its bytes reach the page as "
                                f"data: URIs, so this leaves the machine inside a shared artifact")

    if failures:
        print(f"PATH SCOPING FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all path-scoping cases passed")
    return 0


def test_path_scoping() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
