#!/usr/bin/env python3
"""record_booking.py: write the traveller's decision into the plan, refuse anything that is not one.

Run:  python tests/test_record_booking.py
      python -m pytest tests/test_record_booking.py
"""

from __future__ import annotations

import contextlib
import datetime as dt
import io
import json
import os
import stat
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import record_booking as rb  # noqa: E402

SELF_DRIVE = ROOT / "tests" / "self-drive-fixture.json"
TODAY = dt.date.today()
YESTERDAY = (TODAY - dt.timedelta(days=1)).isoformat()

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def run(path: Path, *argv: str) -> tuple[int, str]:
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = rb.main([str(path), *argv])
    except Exception as exc:  # noqa: BLE001 - a crash is a failed case with a name, not a traceback
        return 99, out.getvalue() + f"\nCRASHED: {type(exc).__name__}: {exc}"
    return code, out.getvalue()


def fresh(tmp: str) -> Path:
    path = Path(tmp) / "plan.json"
    path.write_text(SELF_DRIVE.read_text(encoding="utf-8"), encoding="utf-8")
    os.chmod(path, 0o644)
    return path


def plan_of(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def end_to_end_case() -> None:
    """A verified save, a hotel booked that the days already sleep at, a re-save: still verified;
    then a switch to the other hotel: the save asks for exactly those days' recheck."""
    import copy  # noqa: PLC0415
    import subprocess  # noqa: PLC0415
    sys.path.insert(0, str(ROOT / "tests"))
    from test_plan_consistency import full_verification  # noqa: PLC0415
    save_script = ROOT / "scripts" / "save_trip_deliverables.py"
    plan = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        stem = f"{plan['trip']['start_date']}-trip"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = source.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        save = [sys.executable, str(save_script), str(source), "--workspace", str(tmp / "ws"), "--slug", "trip"]
        first = subprocess.run(save + ["--verification", str(report_path)], capture_output=True, text=True)
        check("e2e: verified save", first.returncode == 0, (first.stdout + first.stderr)[-500:])
        code, out = run(source, "--option", "stay-a", "--booked", "--on", YESTERDAY, "--via", "hotel website")
        again = subprocess.run(save + ["--overwrite", "--verification", str(report_path)], capture_output=True, text=True)
        check("e2e: booking the planned hotel keeps the plan verified", code == 0 and again.returncode == 0,
              (out[-200:], (again.stdout + again.stderr)[-600:]))
        code, out = run(source, "--option", "stay-b", "--booked", "--on", YESTERDAY, "--via", "hotel website")
        unedited = subprocess.run(save + ["--overwrite", "--verification", str(report_path)], capture_output=True, text=True)
        check("e2e: a switch whose days still name the old hotel is refused at the save, naming it",
              code == 0 and "EDIT: " in out and unedited.returncode != 0
              and "still name Fixture Hotel A" in unedited.stdout + unedited.stderr,
              (out[-400:], (unedited.stdout + unedited.stderr)[-600:]))
        # The edit an agent makes for the EDIT lines: the days now name the hotel actually taken.
        edited = json.loads(source.read_text(encoding="utf-8"))
        edited["days"] = json.loads(json.dumps(edited["days"], ensure_ascii=False).replace("Fixture Hotel A", "Fixture Hotel B"))
        source.write_text(json.dumps(edited, ensure_ascii=False), encoding="utf-8")
        switched = subprocess.run(save + ["--overwrite", "--verification", str(report_path)], capture_output=True, text=True)
        check("e2e: a switched hotel asks for its days' recheck", code == 0 and "STAY SWITCHED" in out
              and switched.returncode != 0 and "days[" in switched.stderr
              and "still name Fixture Hotel A" not in switched.stdout + switched.stderr,
              (out[-200:], (switched.stdout + switched.stderr)[-600:]))

        # On the DELIVERED copy (the one a later conversation edits), the printed save runs as printed.
        delivered = tmp / "ws" / "plans" / f"{stem}.json"
        code, out = run(delivered, "--option", "stay-a", "--chosen")
        line = next((l for l in out.splitlines() if l.startswith("NEXT: ")), "")
        import shlex  # noqa: PLC0415
        ran = subprocess.run(shlex.split(line[len("NEXT: "):]), capture_output=True, text=True) if line else None
        check("e2e: the NEXT command on a delivered copy runs as printed",
              code == 0 and ran is not None and ran.returncode == 0,
              (out[-300:], (ran.stdout + ran.stderr)[-500:] if ran else "no NEXT line"))


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        path = fresh(tmp)
        code, out = run(path, "--option", "gt-lner", "--booked", "--on", YESTERDAY, "--via", "LNER website",
                        "--paid", "180", "gbp")
        record = (plan_of(path).get("bookings") or [{}])[0]
        check("a booking is recorded", code == 0 and "RECORDED" in out and record == {
            "option_id": "gt-lner", "state": "booked", "booked_on": YESTERDAY, "booked_via": "LNER website",
            "paid_total": 180, "paid_currency": "GBP"}, (code, out[-300:], record))
        check("paid_formats: currency upper-cased", record.get("paid_currency") == "GBP")
        check("the file keeps its mode", stat.S_IMODE(path.stat().st_mode) == 0o644, oct(stat.S_IMODE(path.stat().st_mode)))
        check("a NEXT line follows", "NEXT:" in out, out[-300:])

        code, out = run(path, "--option", "gt-lumo", "--chosen")
        recs = plan_of(path)["bookings"]
        check("another option in the group replaces the first", code == 0 and "REPLACED" in out and "gt-lner" in out
              and [r["option_id"] for r in recs] == ["gt-lumo"], (out[-300:], recs))

        code, out = run(path, "--clear", "gt-lumo")
        check("clear removes the record", code == 0 and "CLEARED" in out and plan_of(path)["bookings"] == [], out[-300:])

        before = path.read_text(encoding="utf-8")
        for label, argv in (
            ("an unknown option", ["--option", "nope-1", "--chosen"]),
            ("booked without a date", ["--option", "gt-lner", "--booked", "--via", "x"]),
            ("booked without a channel", ["--option", "gt-lner", "--booked", "--on", YESTERDAY]),
            ("a future booking date", ["--option", "gt-lner", "--booked", "--on", (TODAY + dt.timedelta(days=2)).isoformat(), "--via", "x"]),
            ("paid_formats: a comma amount", ["--option", "gt-lner", "--booked", "--on", YESTERDAY, "--via", "x", "--paid", "1,015", "GBP"]),
            ("a negative amount", ["--option", "gt-lner", "--booked", "--on", YESTERDAY, "--via", "x", "--paid", "-5", "GBP"]),
            ("paid on a chosen record", ["--option", "gt-lner", "--chosen", "--paid", "5", "GBP"]),
            ("clearing what is not recorded", ["--clear", "gt-lner"]),
        ):
            code, out = run(path, *argv)
            check(f"{label} is refused and nothing is written", code == 1 and "ERROR:" in out
                  and path.read_text(encoding="utf-8") == before, (code, out[-300:]))

    with tempfile.TemporaryDirectory() as tmp:
        path = fresh(tmp)
        code, out = run(path, "--option", "acc-pit-2", "--chosen")
        plan = plan_of(path)
        check("a hotel switch re-points that stay's days", code == 0 and "STAY SWITCHED" in out
              and [d["accommodation_option_id"] for d in plan["days"]] == ["acc-pit-2", "acc-pit-2", "acc-sta-1", "acc-sta-1"],
              (out[-300:], [d["accommodation_option_id"] for d in plan["days"]]))
        check("switch_touches_only_its_group", plan["days"][2]["accommodation_option_id"] == "acc-sta-1")
        import bookings  # noqa: PLC0415
        check("the result passes the rules", not bookings.record_problems(plan, TODAY), bookings.record_problems(plan, TODAY))
        edits = [l for l in out.splitlines() if l.startswith("EDIT: ")]
        nxt = next((l for l in out.splitlines() if l.startswith("NEXT: ")), "")
        check("a switch names every day still pointing the traveller at the old hotel",
              "was Atholl Palace Hotel" in out and any("day 1" in l and "days[0].route.end" in l for l in edits)
              and any("day 3" in l and "days[2].activities[0].name" in l for l in edits)
              and nxt.startswith("NEXT: edit") and "Pitlochry Hydro Hotel" in nxt, out[-1500:])

    end_to_end_case()

    help_text = io.StringIO()
    with contextlib.redirect_stdout(help_text):
        try:
            rb.main(["--help"])
        except SystemExit:
            pass
    check("--today is hidden from --help", "--today" not in help_text.getvalue())

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("record booking cases passed")
    return 0


def test_record_booking() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
