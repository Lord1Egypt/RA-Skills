#!/usr/bin/env python3
"""A verification covers the content it read, and an edit afterwards is rechecked by section.

The report used to bind a plan by file name and date only. Measured 2026-09-24 on a copy of the one
verified real plan: day 3 moved from 13:30 to 14:00, re-saved with the same report, saved, no
banner, and the page showed 14:00 under a verification that never saw it. The owner chose the
section design over "any change voids the report": a verified save stamps a fingerprint per
section -- each day by its date, each booking option by its id, each other block -- and a later
save against the same report must recheck exactly the sections that changed. Everything else keeps
its verification, which is what makes a light post-delivery edit affordable.

Run:  python tests/test_verification_rechecks.py
      python -m pytest tests/test_verification_rechecks.py
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

import check_plan_consistency as cpc  # noqa: E402
from test_plan_consistency import full_verification  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"
SAVE = ROOT / "scripts" / "save_trip_deliverables.py"
SCAFFOLD = ROOT / "scripts" / "new_verification_report.py"
TODAY = dt.date.today().isoformat()

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def base_plan() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def sections_module():
    try:
        import verification_sections  # noqa: PLC0415
    except ImportError as exc:
        failures.append(f"scripts/verification_sections.py cannot be imported: {exc}")
        return None
    return verification_sections


def verify(report: dict, plan: dict, plan_path: Path) -> list[str]:
    errors: list[str] = []
    cpc.check_verification(report, errors, [], plan=plan, plan_path=str(plan_path))
    return errors


def fill(node: object) -> object:
    """An author filling in the scaffold: every placeholder becomes a concrete sentence."""
    if isinstance(node, dict):
        out = {k: fill(v) for k, v in node.items()}
        if "verdict" in out:
            out.update(verdict="confirmed", severity="minor",
                       evidence_url="https://official-source.test/checked")
        return out
    if isinstance(node, list):
        return [fill(v) for v in node]
    if isinstance(node, str) and node.startswith("TODO:"):
        return "Re-opened the venue page for the new time and read its hours."
    return node


def printed_command(text: str, script: str) -> list[str] | None:
    """The next step a script printed for `script`: a `NEXT:` line that is a whole command."""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("NEXT:") and script in line:
            try:
                return shlex.split(line[len("NEXT:"):])
            except ValueError:
                return None
    return None


def main() -> int:
    vs = sections_module()
    if vs is None:
        return report_failures()

    # 0. The gate now reads a sibling module, and it must still load by path from anywhere --
    #    tests and callers do that, and pytest's shared sys.path hid the first version's failure.
    loader = ("import importlib.util, sys; "
              f"spec = importlib.util.spec_from_file_location('gate', {str(ROOT / 'scripts' / 'check_plan_consistency.py')!r}); "
              "module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); "
              "print(len(module.PLAN_CHECKS))")
    loaded = subprocess.run([sys.executable, "-c", loader], capture_output=True, text=True,
                            cwd="/")
    check("the gate loads by path with scripts/ off sys.path", loaded.returncode == 0,
          loaded.stderr[-300:])

    # 1. Section identity: days by date, options by id, stable under reordering.
    plan = base_plan()
    digests = vs.section_digests(plan)
    day0 = plan["days"][0]["date"]
    check("days are keyed by date", f"days[{day0}]" in digests, sorted(digests)[:6])
    check("booking options are keyed by id",
          "booking_options.accommodations[stay-a]" in digests, sorted(digests))
    reordered = copy.deepcopy(plan)
    reordered["booking_options"]["accommodations"].reverse()
    check("reordering options changes no section",
          vs.changed_sections(digests, reordered) == ([], []),
          vs.changed_sections(digests, reordered))
    edited = copy.deepcopy(plan)
    edited["days"][0]["activities"][0]["time"] = "09:30"
    check("editing one activity changes exactly its day",
          vs.changed_sections(digests, edited) == ([f"days[{day0}]"], []),
          vs.changed_sections(digests, edited))
    added = copy.deepcopy(plan)
    extra = copy.deepcopy(plan["days"][0])
    extra["date"] = "2099-01-01"
    added["days"].append(extra)
    check("inserting a day adds exactly one section",
          vs.changed_sections(digests, added) == (["days[2099-01-01]"], []),
          vs.changed_sections(digests, added))
    meta = copy.deepcopy(plan)
    meta["verification_status"] = "verified"
    meta["gates_passed"] = {"checks": 99}
    check("script-written keys are not content", vs.changed_sections(digests, meta) == ([], []),
          vs.changed_sections(digests, meta))

    # 2. A claims pointer maps to the section it lives in.
    check("a day pointer maps to its day",
          vs.section_of_pointer(plan, "days[0].dining[0].venue_hours") == f"days[{day0}]",
          vs.section_of_pointer(plan, "days[0].dining[0].venue_hours"))
    check("an option pointer maps to its option",
          vs.section_of_pointer(plan, "booking_options.accommodations[1].nightly_cost_low")
          == "booking_options.accommodations[stay-b]",
          vs.section_of_pointer(plan, "booking_options.accommodations[1].nightly_cost_low"))
    check("a block pointer maps to its block",
          vs.section_of_pointer(plan, "budget.breakdown[0].category") == "budget",
          vs.section_of_pointer(plan, "budget.breakdown[0].category"))

    # 3. End to end through the real save path.
    stem = f"{plan['trip']['start_date']}-trip"
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "ws"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = source.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        first = subprocess.run([sys.executable, str(SAVE), str(source), "--workspace",
                                str(workspace), "--slug", "trip", "--verification",
                                str(report_path)], capture_output=True, text=True)
        check("a verified save succeeds", first.returncode == 0, first.stdout + first.stderr)
        saved_path = workspace / "plans" / f"{stem}.json"
        saved_report_path = workspace / "plans" / f"{stem}-verification.json"
        if first.returncode != 0 or not saved_path.exists():
            return report_failures()
        saved = json.loads(saved_path.read_text(encoding="utf-8"))
        receipt = saved.get("verification_receipt") or {}
        check("the saved plan carries a section receipt",
              f"days[{day0}]" in (receipt.get("sections") or {}), receipt)
        check("the receipt names the report date it binds to",
              receipt.get("report_checked_at") == report["checked_at"], receipt)

        ws_report = json.loads(saved_report_path.read_text(encoding="utf-8"))
        check("an unchanged re-check raises nothing",
              not [e for e in verify(ws_report, saved, saved_path) if "changed after" in e],
              verify(ws_report, saved, saved_path))

        # The workspace audit names a verified plan whose content moved after it was verified --
        # the case a traveller reopening a saved trip would otherwise never see.
        import audit_workspace  # noqa: PLC0415
        check("the audit is quiet about an untouched verified plan",
              audit_workspace._changed_since_verified(saved) == [],
              audit_workspace._changed_since_verified(saved))
        saved["days"][0]["activities"][0]["time"] = "09:30"
        check("the audit names the section a verified plan changed afterwards",
              audit_workspace._changed_since_verified(saved) == [f"days[{day0}]"],
              audit_workspace._changed_since_verified(saved))
        found = verify(ws_report, saved, saved_path)
        check("an edit after verification is named by section",
              any(f"days[{day0}]" in e and "changed after" in e for e in found), found)

        good = copy.deepcopy(ws_report)
        good["rechecks"] = [{"section": f"days[{day0}]", "checked_at": TODAY,
                             "section_digest": vs.section_digests(saved)[f"days[{day0}]"],
                             "reason": "The traveller asked to start the day later.",
                             "claims_checked": ["days[0].activities[0]"], "findings": []}]
        found = verify(good, saved, saved_path)
        check("a recheck of the changed section clears it",
              not [e for e in found if "changed after" in e or "recheck" in e], found)

        outside = copy.deepcopy(good)
        outside["rechecks"][0]["claims_checked"] = ["budget.breakdown[0]"]
        found = verify(outside, saved, saved_path)
        check("a recheck citing another section is refused",
              any("outside" in e for e in found), found)

        early = copy.deepcopy(good)
        early["rechecks"][0]["checked_at"] = "2026-01-01"
        found = verify(early, saved, saved_path)
        check("a recheck dated before its report is refused",
              any("before the report" in e for e in found), found)

        bare = copy.deepcopy(good)
        bare["rechecks"][0]["findings"] = [{"claim": "the park opens at 09:30", "verdict": "wrong",
                                            "severity": "major", "resolved": True}]
        found = verify(bare, saved, saved_path)
        check("a recheck's findings follow the report's rules",
              any("no resolution" in e for e in found), found)

        # Re-save with the recheck: accepted, and the page says which part was rechecked.
        saved_path.write_text(json.dumps(saved, ensure_ascii=False), encoding="utf-8")
        saved_report_path.write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")
        second = subprocess.run([sys.executable, str(SAVE), str(saved_path), "--workspace",
                                 str(workspace), "--slug", "trip", "--overwrite", "--verification",
                                 str(saved_report_path)], capture_output=True, text=True)
        check("a re-save covered by its recheck succeeds", second.returncode == 0,
              second.stdout + second.stderr)
        page = (workspace / "html" / f"{stem}.html").read_text(encoding="utf-8")
        check("the page says which part was rechecked after the main verification",
              'class="meta rechecked-sections"' in page, "no rechecked-sections line")
        check("the page names the rechecked day as a day, not as a JSON key",
              f"days[{day0}]" not in page.split('rechecked-sections', 1)[-1][:600])

        # The same line on a Chinese page carries no renderer English, whichever kind of part it
        # names: a day, a booking option, or a block.
        import render_final_trip_html as renderer  # noqa: PLC0415
        chinese = json.loads(saved_path.read_text(encoding="utf-8"))
        chinese["trip"]["language"] = "zh-CN"
        chinese["verification_receipt"]["rechecked"] = {
            f"days[{day0}]": TODAY, "booking_options.accommodations[stay-a]": TODAY,
            "budget": TODAY, "transport_overview": TODAY}
        line = renderer.render(chinese).split('class="meta rechecked-sections"', 1)[-1][:900]
        check("a Chinese page translates the rechecked line",
              "Re-checked" not in line and "Budget" not in line and "Other trip details" not in line
              and "Day " not in line.split("</p>", 1)[0], line[:400])

        # A party change rechecks a dozen parts at once. Read on the page on 2026-09-24: the line
        # printed the same date sixteen times, called both the transport overview and the trip
        # block "Other trip details", and listed hotels before days. One date per group, each part
        # once, days first.
        many = json.loads(saved_path.read_text(encoding="utf-8"))
        many["verification_receipt"]["rechecked"] = {
            "trip": TODAY, "transport_overview": TODAY, "budget": TODAY,
            "booking_options.accommodations[stay-a]": TODAY, f"days[{day0}]": TODAY}
        english = renderer.render(many).split('class="meta rechecked-sections"', 1)[-1]
        english = english.split("</p>", 1)[0]
        check("the rechecked line prints a date once for parts rechecked together",
              english.count(TODAY) == 1, english[:600])
        check("the transport overview has its own name on the page",
              "Transport overview" in english and english.count("Other trip details") == 1,
              english[:600])
        check("the rechecked line reads days before bookings",
              english.find("Day ") < english.find(many["booking_options"]["accommodations"][0]
                                                  ["property_name"]), english[:600])
        # From the fresh review: groups were keyed by the whole stamp and ordered by plan position,
        # so two times on one day made two groups and a later date could come first.
        dated = copy.deepcopy(many)
        dated["verification_receipt"]["rechecked"] = {
            f"days[{day0}]": "2026-09-24", "budget": "2026-09-20T10:00:00",
            "transport_overview": "2026-09-20T16:30:00"}
        dated_line = renderer.render(dated).split('class="meta rechecked-sections"', 1)[-1]
        dated_line = dated_line.split("</p>", 1)[0]
        check("rechecks on one day form one group, and the groups read in date order",
              dated_line.count("2026-09-20") == 1
              and 0 <= dated_line.find("2026-09-20") < dated_line.find("2026-09-24"), dated_line[:600])
        dated["trip"]["language"] = "zh-CN"
        dated_zh = renderer.render(dated).split('class="meta rechecked-sections"', 1)[-1]
        dated_zh = dated_zh.split("</p>", 1)[0]
        check("a Chinese page separates the date groups with a Chinese semicolon",
              "；" in dated_zh and "; " not in dated_zh, dated_zh[:600])
        many["trip"]["language"] = "zh-CN"
        chinese_line = renderer.render(many).split('class="meta rechecked-sections"', 1)[-1]
        chinese_line = chinese_line.split("</p>", 1)[0]
        check("a Chinese page names the transport overview in Chinese",
              "Transport overview" not in chinese_line and "交通总览" in chinese_line,
              chinese_line[:600])

        # 6. The scaffold writes the recheck entries for exactly the sections that moved.
        resaved = json.loads(saved_path.read_text(encoding="utf-8"))
        resaved["booking_options"]["accommodations"][1]["selection_rationale"] = (
            "Closer to the ferry, which the traveller now prefers.")
        saved_path.write_text(json.dumps(resaved, ensure_ascii=False), encoding="utf-8")
        scaffolded_path = tmp / "rechecks.json"
        scaffold = subprocess.run([sys.executable, str(SCAFFOLD), "--recheck", "--from-plan",
                                   str(saved_path), "--report", str(saved_report_path), "--out",
                                   str(scaffolded_path)], capture_output=True, text=True)
        check("the recheck scaffold runs", scaffold.returncode == 0,
              scaffold.stdout + scaffold.stderr)
        if scaffold.returncode == 0:
            scaffolded = json.loads(scaffolded_path.read_text(encoding="utf-8"))
            moved = "booking_options.accommodations[stay-b]"
            new = [r for r in scaffolded.get("rechecks", []) if r.get("section") == moved]
            check("the scaffold appends one recheck for the changed option", len(new) == 1,
                  scaffolded.get("rechecks"))
            check("the scaffold keeps the earlier recheck",
                  any(r.get("section") == f"days[{day0}]" for r in scaffolded.get("rechecks", [])))
            found = verify(scaffolded, resaved, saved_path)
            check("an unfilled recheck is refused", any("placeholder" in e for e in found), found)
            found = verify(fill(scaffolded), resaved, saved_path)
            check("a filled recheck passes",
                  not [e for e in found if "changed after" in e or "recheck" in e
                       or "placeholder" in e], found)

    # 7. The way out the entry rule names has to be open. A plan once saved verified, whose entry
    #    answer is still unverified, is refused with "or save with --unverified so the page says
    #    so" -- and saving it --unverified was refused by the same rule, because the save ran every
    #    check against the status of the page being replaced before recording the new one.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        open_entry = base_plan()
        open_entry["verification_status"] = "verified"
        open_entry["entry_context"] = {
            "status": "unverified", "summary": "Not yet read against the official page.",
            "traveler_basis": "short_stay_visa_or_visa_free", "source_url": "https://esta.cbp.dhs.gov/",
            "checked_at": "2026-09-12"}
        source = tmp / "plan.json"
        source.write_text(json.dumps(open_entry, ensure_ascii=False), encoding="utf-8")
        saved = subprocess.run([sys.executable, str(SAVE), str(source), "--workspace", str(tmp / "ws"),
                                "--slug", "trip", "--unverified"], capture_output=True, text=True)
        check("a once-verified plan with an open entry answer can be saved --unverified",
              saved.returncode == 0, (saved.stdout + saved.stderr)[-900:])

    def save(path: Path, workspace: Path, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SAVE), str(path), "--workspace", str(workspace),
                               "--slug", "trip", *extra], capture_output=True, text=True)

    # 8. An edit to the author's own working file after a verified save is still an edit. The
    #    receipt is written into the delivered workspace copy, never into the file the author keeps
    #    editing -- so re-saving that file over its verified copy arrived with no receipt, read as a
    #    plan from before receipts existed, and re-stamped the edit as verified: exit 0, no banner.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "ws"
        working = base_plan()
        stem = f"{working['trip']['start_date']}-trip"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(working, ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = source.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        first = save(source, workspace, "--verification", str(report_path))
        check("the working file's verified save succeeds", first.returncode == 0,
              (first.stdout + first.stderr)[-600:])
        working["days"][0]["activities"][0]["time"] = "09:30"
        source.write_text(json.dumps(working, ensure_ascii=False), encoding="utf-8")
        again = save(source, workspace, "--overwrite", "--verification", str(report_path))
        check("re-saving the edited working file over its verified copy asks for a recheck",
              again.returncode != 0 and f"days[{day0}]" in again.stderr and "changed after" in again.stderr,
              f"exit {again.returncode}: {(again.stdout + again.stderr)[-600:]}")
        # The receipt is in the delivered copy, not in this working file, so the scaffold the
        # refusal names has to be told where it is -- run on the working file alone it answered
        # "no receipt ... run a full verification".
        command = printed_command(again.stderr, "new_verification_report.py")
        ran = subprocess.run(command, capture_output=True, text=True) if command else None
        check("the recheck command printed for a working file runs as printed",
              ran is not None and ran.returncode == 0,
              (ran.stdout + ran.stderr)[-500:] if ran else again.stderr[-600:])
        if ran is not None and ran.returncode == 0:
            report_path.write_text(json.dumps(fill(json.loads(report_path.read_text(
                encoding="utf-8"))), ensure_ascii=False), encoding="utf-8")
            follow = printed_command(ran.stderr, "save_trip_deliverables.py")
            closed = subprocess.run(follow, capture_output=True, text=True) if follow else None
            delivered_copy = workspace / "plans" / f"{stem}.json"
            check("and the save it prints replaces the verified copy with the edit",
                  closed is not None and closed.returncode == 0
                  and json.loads(delivered_copy.read_text(encoding="utf-8"))["days"][0]
                  ["activities"][0]["time"] == "09:30",
                  (closed.stdout + closed.stderr)[-600:] if closed else ran.stderr[-600:])

    # 9. A recheck covers the content it checked, not its section from then on. After one recheck
    #    of a day and a covered re-save, a second edit of that day re-saved as verified with no
    #    banner -- and the page said the day had been "re-checked after the main verification".
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "ws"
        working = base_plan()
        stem = f"{working['trip']['start_date']}-trip"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(working, ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = source.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        first = save(source, workspace, "--verification", str(report_path))
        saved_path = workspace / "plans" / f"{stem}.json"
        ws_report = workspace / "plans" / f"{stem}-verification.json"
        check("the second flow's verified save succeeds", first.returncode == 0,
              (first.stdout + first.stderr)[-600:])
        if first.returncode == 0:
            edited = json.loads(saved_path.read_text(encoding="utf-8"))
            edited["days"][0]["activities"][0]["time"] = "09:30"
            saved_path.write_text(json.dumps(edited, ensure_ascii=False), encoding="utf-8")
            amended_path = tmp / "amended.json"
            scaffolded = subprocess.run([sys.executable, str(SCAFFOLD), "--recheck", "--from-plan",
                                         str(saved_path), "--report", str(ws_report), "--out",
                                         str(amended_path)], capture_output=True, text=True)
            check("the recheck scaffold runs on the edited copy", scaffolded.returncode == 0,
                  scaffolded.stderr[-400:])
            amended = fill(json.loads(amended_path.read_text(encoding="utf-8")))
            check("the scaffold binds the recheck to the content it is about",
                  all(isinstance(r.get("section_digest"), str) and r["section_digest"]
                      for r in amended.get("rechecks", [])), amended.get("rechecks"))
            amended_path.write_text(json.dumps(amended, ensure_ascii=False), encoding="utf-8")
            covered = save(saved_path, workspace, "--overwrite", "--verification", str(amended_path))
            check("the recheck covers the edit it was written for", covered.returncode == 0,
                  (covered.stdout + covered.stderr)[-600:])
            page = (workspace / "html" / f"{stem}.html").read_text(encoding="utf-8")
            check("the page names the rechecked day", 'class="meta rechecked-sections"' in page)
            check("the gate's summary still counts the report's five domains",
                  "verification covered 5 domains" in covered.stdout, covered.stdout[-500:])

            again = json.loads(saved_path.read_text(encoding="utf-8"))
            again["days"][0]["activities"][0]["time"] = "10:15"
            saved_path.write_text(json.dumps(again, ensure_ascii=False), encoding="utf-8")
            second_edit = save(saved_path, workspace, "--overwrite", "--verification", str(amended_path))
            check("a second edit of a rechecked day asks for its own recheck",
                  second_edit.returncode != 0 and f"days[{day0}]" in second_edit.stderr,
                  f"exit {second_edit.returncode}: {(second_edit.stdout + second_edit.stderr)[-600:]}")

            # An unverified save keeps the receipt (a later verified save compares against it) but
            # its page claims no verification at all -- so it cannot claim a recheck either.
            unverified = save(saved_path, workspace, "--overwrite", "--unverified")
            check("the plan can be saved --unverified meanwhile", unverified.returncode == 0,
                  (unverified.stdout + unverified.stderr)[-600:])
            page = (workspace / "html" / f"{stem}.html").read_text(encoding="utf-8")
            check("an unverified page does not say a part was re-checked",
                  'class="meta rechecked-sections"' not in page)

    # 10. Every booking option has its own id. The receipt keys an option by its id, so two rental
    #     cars (or tickets) sharing one were a single fingerprint, and edits to the first escaped
    #     every recheck. Flights, ground transport and hotels already required distinct ids.
    import render_final_trip_html as renderer  # noqa: PLC0415
    selfdrive = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))
    check("the self-drive fixture is valid as shipped", not renderer.validate_plan(selfdrive),
          renderer.validate_plan(selfdrive)[:3])
    twins = copy.deepcopy(selfdrive)
    twins["booking_options"]["rental_cars"][1]["id"] = twins["booking_options"]["rental_cars"][0]["id"]
    problems = renderer.validate_plan(twins)
    check("two rental cars sharing an id are refused",
          any("distinct" in p and "ental" in p for p in problems), problems[:4])
    twins = copy.deepcopy(selfdrive)
    twins["booking_options"]["attraction_tickets"].append(copy.deepcopy(
        twins["booking_options"]["attraction_tickets"][0]))
    problems = renderer.validate_plan(twins)
    check("two tickets sharing an id are refused",
          any("distinct" in p and "icket" in p for p in problems), problems[:4])

    # 4. A plan saved before receipts existed is not asked for rechecks.
    legacy = base_plan()
    legacy["days"][0]["activities"][0]["time"] = "09:30"
    found = verify(full_verification(), legacy, Path("plan.json"))
    check("a plan with no receipt owes no recheck",
          not [e for e in found if "changed after" in e], found)

    # 5. A new full report is a new verification: the old receipt does not bind it.
    fresh = base_plan()
    fresh["verification_receipt"] = {"report_checked_at": "2026-07-31",
                                     "sections": {f"days[{day0}]": "0000000000000000"},
                                     "rechecked": {}}
    found = verify(full_verification(), fresh, Path("plan.json"))
    check("a receipt from another report date is ignored",
          not [e for e in found if "changed after" in e], found)

    # 11. A section's verification holds only while the trip facts it was checked against hold.
    #     Walked on 2026-09-24: a party that grew 4 -> 5 after a verified save was rechecked as
    #     "trip" alone and re-saved VERIFIED, every hotel card still for four guests and its search
    #     link for 2 adults + 2 children -- the cards' own text had not changed, so nothing moved.
    plan = base_plan()
    digests = vs.section_digests(plan)
    options = [f"booking_options.{kind}[{option['id']}]"
               for kind, items in plan["booking_options"].items() if isinstance(items, list)
               for option in items if isinstance(option, dict) and option.get("id")]
    all_days = [f"days[{day['date']}]" for day in plan["days"]]
    grown = copy.deepcopy(plan)
    grown["trip"]["traveler_count"] = plan["trip"]["traveler_count"] + 1
    moved, _ = vs.changed_sections(digests, grown)
    party_parts = set(options + all_days + ["budget", "transport_overview", "trip"])
    check("a party change moves every section priced, roomed or seated for the party",
          party_parts <= set(moved), sorted(party_parts - set(moved)))
    stricter = copy.deepcopy(plan)
    constraints = stricter["trip"].setdefault("traveler_constraints", {})
    constraints["allergy_severity"] = "none" if constraints.get("allergy_severity") == "severe" else "severe"
    moved, _ = vs.changed_sections(digests, stricter)
    check("a constraint change moves every day and booking option",
          set(options + all_days) <= set(moved), sorted(set(options + all_days) - set(moved)))
    check("a constraint change leaves the budget alone", "budget" not in moved, moved)
    retitled = copy.deepcopy(plan)
    retitled["trip"]["title"] = "The same trip under a new name"
    check("a trip field nothing depends on moves only the trip",
          vs.changed_sections(digests, retitled) == (["trip"], []),
          vs.changed_sections(digests, retitled))

    # 12. A receipt stamped before dependencies were folded in (plain digests) keeps its meaning:
    #     unchanged content is not "changed", an edited day is still named, and a changed trip still
    #     moves every section that depends on it.
    old = {key: vs._digest(value) for key, value in vs.sections(plan).items()}
    check("an old receipt of an unchanged plan reports nothing",
          vs.changed_sections(old, plan) == ([], []), vs.changed_sections(old, plan))
    edited = copy.deepcopy(plan)
    edited["days"][0]["activities"][0]["time"] = "09:30"
    check("an old receipt still names an edited day",
          vs.changed_sections(old, edited) == ([f"days[{day0}]"], []), vs.changed_sections(old, edited))
    check("an old receipt still moves the party's sections when the trip changed",
          set(options) <= set(vs.changed_sections(old, grown)[0]), vs.changed_sections(old, grown))

    # 13. An emptied section has nothing left to verify. Its recheck had no pointer to write, and
    #     the gate refused the recheck as "checked nothing" -- a loop whose only exits were a full
    #     re-verification or --unverified.
    emptied = copy.deepcopy(plan)
    emptied["assumptions"] = []
    moved, removed = vs.changed_sections(digests, emptied)
    check("an emptied section counts as removed, not changed",
          "assumptions" in removed and "assumptions" not in moved, (moved, removed))

    # 13b. Found by the fresh review: a recheck that carries a pre-v2 digest saw its section alone,
    #      so it cannot vouch for a section that depends on the party; an already-empty dependent
    #      section is not "removed" by a party change; and the entry answer is about who travels.
    stamped = copy.deepcopy(plan)
    stamped["transport_overview"] = []
    stamped["entry_context"] = {"status": "not_required", "summary": "Domestic trip.",
                                "traveler_basis": "not_applicable_domestic",
                                "source_url": "https://www.gov.uk/", "checked_at": "2026-08-03"}
    stamps = vs.section_digests(stamped)
    grown_again = copy.deepcopy(stamped)
    grown_again["trip"]["traveler_count"] += 1
    moved, removed = vs.changed_sections(stamps, grown_again)
    check("an already-empty dependent section is not 'removed' by a party change",
          "transport_overview" not in removed and "transport_overview" not in moved, (moved, removed))
    check("a party change asks for the entry answer again", "entry_context" in moved, moved)
    check("a pre-v2 recheck digest does not vouch for a party-dependent section",
          not vs.digest_is_current(grown_again, f"days[{day0}]",
                                   vs._digest(vs.sections(grown_again)[f"days[{day0}]"])))

    # 14. The recheck loop runs on the commands the scripts print, and nothing else. Walked
    #     literally on 2026-09-24: re-saving the delivered copy with --overwrite alone answered "No
    #     verification report ... run the parallel-verify stage" although SKILL.md says the edit
    #     keeps its report; the recheck command the gate printed carried <plan.json>/<report.json>
    #     placeholders; and run as printed it wrote the amended report to standard output and saved
    #     nothing. The workspace path has a space in it, like the real default.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "Travel Buddy"
        working = base_plan()
        stem = f"{working['trip']['start_date']}-trip"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(working, ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = source.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        first = save(source, workspace, "--verification", str(report_path))
        check("the loop's verified save succeeds", first.returncode == 0,
              (first.stdout + first.stderr)[-600:])
        delivered = workspace / "plans" / f"{stem}.json"
        delivered_report = workspace / "plans" / f"{stem}-verification.json"
        if first.returncode == 0:
            copy_of = json.loads(delivered.read_text(encoding="utf-8"))
            copy_of["days"][0]["activities"][0]["time"] = "10:05"
            delivered.write_text(json.dumps(copy_of, ensure_ascii=False), encoding="utf-8")
            # No --slug and no --verification: the delivered copy names both itself.
            resave = subprocess.run([sys.executable, str(SAVE), str(delivered), "--workspace",
                                     str(workspace), "--overwrite"], capture_output=True, text=True)
            check("re-saving the delivered copy with --overwrite alone checks it against its report",
                  resave.returncode != 0 and f"days[{day0}]" in resave.stderr
                  and "No verification report" not in resave.stderr,
                  f"exit {resave.returncode}: {(resave.stdout + resave.stderr)[-700:]}")
            check("that re-save writes no second plan under another name",
                  sorted(p.name for p in (workspace / "plans").glob("*.json"))
                  == sorted([delivered.name, delivered_report.name]),
                  sorted(p.name for p in (workspace / "plans").glob("*.json")))
            command = printed_command(resave.stderr, "new_verification_report.py")
            check("the refusal prints the recheck command with real paths",
                  command is not None and not any("<" in part for part in command)
                  and str(delivered_report.resolve()) in command, resave.stderr[-900:])
            if command:
                ran = subprocess.run(command, capture_output=True, text=True)
                check("the printed recheck command runs as printed", ran.returncode == 0,
                      (ran.stdout + ran.stderr)[-500:])
                amended = json.loads(delivered_report.read_text(encoding="utf-8"))
                check("run as printed, it amends the report it names",
                      any(r.get("section") == f"days[{day0}]" for r in amended.get("rechecks", [])),
                      amended.get("rechecks"))
                delivered_report.write_text(json.dumps(fill(amended), ensure_ascii=False),
                                            encoding="utf-8")
                follow = printed_command(ran.stderr, "save_trip_deliverables.py")
                check("the scaffold then prints the save that closes the loop, with real paths",
                      follow is not None and not any("<" in part for part in follow)
                      and "--overwrite" in follow, ran.stderr[-700:])
                if follow:
                    closed = subprocess.run(follow, capture_output=True, text=True)
                    check("the save it prints succeeds", closed.returncode == 0,
                          (closed.stdout + closed.stderr)[-700:])
                    # The checker's own next step on a delivered plan is the save, not the
                    # renderer: rendering over the page by hand leaves the receipt behind.
                    gate = subprocess.run([sys.executable, str(ROOT / "scripts" /
                                                               "check_plan_consistency.py"),
                                           str(delivered), "--verification", str(delivered_report)],
                                          capture_output=True, text=True)
                    after_gate = printed_command(gate.stderr, "save_trip_deliverables.py")
                    check("a clean check of a delivered plan names the save that re-delivers it",
                          gate.returncode == 0 and after_gate is not None
                          and not any("<" in part for part in after_gate),
                          f"exit {gate.returncode}: {gate.stderr[-500:]}")

                    # 15. Bumping generated_at after a covered edit is not a new plan. The
                    #     receipt already proves which content the report and its rechecks saw;
                    #     the older "report dated before the plan" rule refused the valid recheck.
                    bumped = json.loads(delivered.read_text(encoding="utf-8"))
                    bumped["generated_at"] = TODAY
                    delivered.write_text(json.dumps(bumped, ensure_ascii=False), encoding="utf-8")
                    later = subprocess.run([sys.executable, str(SAVE), str(delivered), "--workspace",
                                            str(workspace), "--overwrite"], capture_output=True,
                                           text=True)
                    check("a covered plan whose generated_at moved still saves verified",
                          later.returncode == 0, (later.stdout + later.stderr)[-700:])

    # 16. The same walk's party change, through the real save: every card for the old party is
    #     named, and a hotel card for fewer guests than the trip is refused outright -- verified or
    #     not, because a room for two is the wrong room for three either way.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "ws"
        working = base_plan()
        stem = f"{working['trip']['start_date']}-trip"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(working, ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = source.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        first = save(source, workspace, "--verification", str(report_path))
        check("the party walk's verified save succeeds", first.returncode == 0,
              (first.stdout + first.stderr)[-600:])
        if first.returncode == 0:
            delivered = workspace / "plans" / f"{stem}.json"
            party = json.loads(delivered.read_text(encoding="utf-8"))
            party["trip"]["traveler_count"] += 1
            delivered.write_text(json.dumps(party, ensure_ascii=False), encoding="utf-8")
            grown_save = save(delivered, workspace, "--overwrite")
            check("a party change names the hotel cards for the old party",
                  grown_save.returncode != 0
                  and "booking_options.accommodations[stay-a]" in grown_save.stderr,
                  f"exit {grown_save.returncode}: {grown_save.stderr[-900:]}")
            check("a hotel card for fewer guests than the trip is refused",
                  "stay-a" in grown_save.stderr and "guest" in grown_save.stderr
                  and str(party["trip"]["traveler_count"]) in grown_save.stderr,
                  grown_save.stderr[-900:])
            unverified = save(delivered, workspace, "--overwrite", "--unverified")
            check("the room check holds on an unverified save too",
                  unverified.returncode != 0 and "guest" in unverified.stderr,
                  f"exit {unverified.returncode}: {unverified.stderr[-600:]}")

    # 17-20 were found by a fresh review of the fixes above (2026-09-24), each reproduced first.
    def run_printed(text: str, script: str) -> subprocess.CompletedProcess | None:
        command = printed_command(text, script)
        return subprocess.run(command, capture_output=True, text=True) if command else None

    # 17. A plan delivered verified before receipts existed has nothing recording what its report
    #     covered. Adopting its report on --overwrite re-certified an edit to it: exit 0, verified,
    #     no banner -- where the parent commit refused the same command.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "ws"
        working = base_plan()
        stem = f"{working['trip']['start_date']}-trip"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(working, ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = source.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        first = save(source, workspace, "--verification", str(report_path))
        delivered = workspace / "plans" / f"{stem}.json"
        if first.returncode == 0:
            legacy = json.loads(delivered.read_text(encoding="utf-8"))
            legacy.pop("verification_receipt", None)
            legacy["days"][0]["activities"][0]["time"] = "09:30"
            delivered.write_text(json.dumps(legacy, ensure_ascii=False), encoding="utf-8")
            again = save(delivered, workspace, "--overwrite")
            check("an edit to a plan delivered before receipts existed is not re-certified",
                  again.returncode != 0 and "receipt" in again.stderr,
                  f"exit {again.returncode}: {(again.stdout + again.stderr)[-700:]}")
            fresh = printed_command(again.stderr, "new_verification_report.py")
            check("and the refusal prints the command that starts a fresh report",
                  fresh is not None and "--from-plan" in fresh and "--recheck" not in fresh,
                  again.stderr[-700:])
        else:
            check("the legacy walk's verified save succeeds", False, first.stderr[-600:])

    # 18. SKILL.md has the skeleton written to `plan.json`, so the report names plan.json while the
    #     delivered copy is <start>-<slug>.json. Copied beside it unchanged, the report no longer
    #     matched the plan it sat next to: the delivered copy could not be re-saved or checked.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "ws"
        source = tmp / "plan.json"
        source.write_text(json.dumps(base_plan(), ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = str(source)
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        first = save(source, workspace, "--verification", str(report_path))
        delivered = workspace / "plans" / f"{base_plan()['trip']['start_date']}-trip.json"
        delivered_report = delivered.with_name(delivered.stem + "-verification.json")
        check("the plan.json walk's verified save succeeds", first.returncode == 0,
              (first.stdout + first.stderr)[-600:])
        if first.returncode == 0:
            gate = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_plan_consistency.py"),
                                   str(delivered), "--verification", str(delivered_report)],
                                  capture_output=True, text=True)
            check("the delivered copy checks clean against the report saved beside it",
                  gate.returncode == 0, gate.stderr[-600:])
            copy_of = json.loads(delivered.read_text(encoding="utf-8"))
            copy_of["days"][0]["activities"][0]["time"] = "10:20"
            delivered.write_text(json.dumps(copy_of, ensure_ascii=False), encoding="utf-8")
            refused = save(delivered, workspace, "--overwrite")
            ran = run_printed(refused.stderr, "new_verification_report.py")
            check("the delivered copy of plan.json can start its recheck",
                  refused.returncode != 0 and ran is not None and ran.returncode == 0,
                  (refused.stderr + (ran.stderr if ran else ""))[-800:])
            if ran is not None and ran.returncode == 0:
                delivered_report.write_text(json.dumps(fill(json.loads(delivered_report.read_text(
                    encoding="utf-8"))), ensure_ascii=False), encoding="utf-8")
                closed = run_printed(ran.stderr, "save_trip_deliverables.py")
                check("and finish it with the save it prints",
                      closed is not None and closed.returncode == 0,
                      (closed.stdout + closed.stderr)[-700:] if closed else ran.stderr[-500:])

    # 19. A working copy kept inside <workspace>/plans under a name that is not dated: the printed
    #     save dropped --slug, and the edit landed as a second plan while the delivered one stayed
    #     verified with the old time.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "ws"
        (workspace / "plans").mkdir(parents=True)
        draft = workspace / "plans" / "draft.json"
        draft.write_text(json.dumps(base_plan(), ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = draft.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        first = save(draft, workspace, "--verification", str(report_path))
        if first.returncode == 0:
            edited = json.loads(draft.read_text(encoding="utf-8"))
            edited["days"][0]["activities"][0]["time"] = "11:40"
            draft.write_text(json.dumps(edited, ensure_ascii=False), encoding="utf-8")
            refused = save(draft, workspace, "--overwrite", "--verification", str(report_path))
            ran = run_printed(refused.stderr, "new_verification_report.py")
            if ran is not None and ran.returncode == 0:
                report_path.write_text(json.dumps(fill(json.loads(report_path.read_text(
                    encoding="utf-8"))), ensure_ascii=False), encoding="utf-8")
                closed = run_printed(ran.stderr, "save_trip_deliverables.py")
            plans = sorted(p.name for p in (workspace / "plans").glob("*.json")
                           if not p.name.endswith("-verification.json"))
            delivered = workspace / "plans" / f"{base_plan()['trip']['start_date']}-trip.json"
            check("a working copy inside plans/ replaces its delivered plan rather than adding one",
                  plans == sorted(["draft.json", delivered.name])
                  and json.loads(delivered.read_text(encoding="utf-8"))["days"][0]["activities"][0]
                  ["time"] == "11:40", plans)
        else:
            check("the draft walk's verified save succeeds", False, first.stderr[-600:])

    # 21. The scaffold's other exits run as printed too, and a folder that merely happens to be
    #     called "plans" is not a workspace.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "ws"
        working = base_plan()
        stem = f"{working['trip']['start_date']}-trip"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(working, ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = source.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        first = save(source, workspace, "--verification", str(report_path))
        delivered = workspace / "plans" / f"{stem}.json"
        if first.returncode == 0:
            loose = tmp / "loose"
            loose.mkdir()
            outside = loose / f"{stem}.json"
            edited = json.loads(delivered.read_text(encoding="utf-8"))
            edited["days"][0]["activities"][0]["time"] = "08:15"
            outside.write_text(json.dumps(edited, ensure_ascii=False), encoding="utf-8")
            loose_report = loose / "report.json"
            loose_report.write_text(delivered.with_name(f"{stem}-verification.json").read_text(
                encoding="utf-8"), encoding="utf-8")
            ran = subprocess.run([sys.executable, str(SCAFFOLD), "--recheck", "--from-plan",
                                  str(outside), "--report", str(loose_report)],
                                 capture_output=True, text=True)
            follow = printed_command(ran.stderr, "check_plan_consistency.py")
            check("outside a workspace the scaffold prints a check that runs as printed",
                  ran.returncode == 0 and follow is not None and Path(follow[0]).is_absolute()
                  and Path(follow[1]).exists(), ran.stderr[-600:])
            # A working file with no receipt, pointed at a "delivered copy" that has none either.
            bare = tmp / "bare.json"
            bare.write_text(json.dumps(base_plan(), ensure_ascii=False), encoding="utf-8")
            unreceipted = tmp / "working-no-receipt.json"
            unreceipted.write_text(json.dumps(base_plan(), ensure_ascii=False), encoding="utf-8")
            no_receipt = subprocess.run([sys.executable, str(SCAFFOLD), "--recheck", "--from-plan",
                                         str(unreceipted), "--report", str(report_path),
                                         "--receipt-from", str(bare)], capture_output=True, text=True)
            check("--receipt-from a plan with no receipt says so and prints a fresh start",
                  no_receipt.returncode == 2 and "--receipt-from <" not in no_receipt.stderr
                  and printed_command(no_receipt.stderr, "new_verification_report.py") is not None,
                  no_receipt.stderr[-600:])
            locked = tmp / "locked.json"
            locked.write_text(loose_report.read_text(encoding="utf-8"), encoding="utf-8")
            locked.chmod(0o444)
            unwritable = subprocess.run([sys.executable, str(SCAFFOLD), "--recheck", "--from-plan",
                                         str(outside), "--report", str(locked)],
                                        capture_output=True, text=True)
            locked.chmod(0o644)
            check("a report it cannot write is an error, not a traceback",
                  unwritable.returncode == 2 and "Traceback" not in unwritable.stderr,
                  unwritable.stderr[-500:])
            projects = tmp / "projects" / "plans"
            projects.mkdir(parents=True)
            copied = projects / delivered.name
            copied.write_text(delivered.read_text(encoding="utf-8"), encoding="utf-8")
            copied_report = projects / f"{stem}-verification.json"
            copied_report.write_text(delivered.with_name(f"{stem}-verification.json").read_text(
                encoding="utf-8"), encoding="utf-8")
            gate = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_plan_consistency.py"),
                                   str(copied), "--verification", str(copied_report)],
                                  capture_output=True, text=True)
            check("a folder named plans without a workspace around it gets no save printed",
                  printed_command(gate.stderr, "save_trip_deliverables.py") is None,
                  gate.stderr[-500:])

    # 20. A working copy carrying the receipt of an older verification must be compared against
    #     the receipt bound to the report in use, not skip the comparison because its own receipt
    #     binds a different report date.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        workspace = tmp / "ws"
        working = base_plan()
        stem = f"{working['trip']['start_date']}-trip"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(working, ensure_ascii=False), encoding="utf-8")
        older, newer = full_verification(), full_verification()
        older["plan"] = newer["plan"] = source.name
        newer["checked_at"] = "2026-08-04"
        older_path, newer_path = tmp / "older.json", tmp / "newer.json"
        older_path.write_text(json.dumps(older, ensure_ascii=False), encoding="utf-8")
        newer_path.write_text(json.dumps(newer, ensure_ascii=False), encoding="utf-8")
        first = save(source, workspace, "--verification", str(older_path))
        delivered = workspace / "plans" / f"{stem}.json"
        if first.returncode == 0:
            stale_copy = json.loads(delivered.read_text(encoding="utf-8"))   # receipt of `older`
            second = save(source, workspace, "--overwrite", "--verification", str(newer_path))
            check("a fresh full report re-verifies the delivered plan", second.returncode == 0,
                  second.stderr[-600:])
            stale_copy["days"][0]["activities"][0]["time"] = "12:10"
            stale_path = tmp / f"{stem}-old-copy.json"
            stale_path.write_text(json.dumps(stale_copy, ensure_ascii=False), encoding="utf-8")
            third = save(stale_path, workspace, "--slug", "trip", "--overwrite", "--verification",
                         str(newer_path))
            check("an old working copy's own stale receipt does not excuse its edit",
                  third.returncode != 0 and f"days[{day0}]" in third.stderr,
                  f"exit {third.returncode}: {(third.stdout + third.stderr)[-600:]}")

    return report_failures()


def report_failures() -> int:
    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("verification recheck cases passed")
    return 0


def test_verification_rechecks() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
