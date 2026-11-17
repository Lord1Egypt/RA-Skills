#!/usr/bin/env python3
"""Regression tests for scripts/save_trip_deliverables.py.

This script is the only path that writes the two files a traveller keeps, and it is the only
place that can refuse to write them. Until this file existed it had no test at all -- the gate
with the most authority in the skill was the one nothing measured. Everything here is about the
refusals rather than the happy path: a save that succeeds when it should have refused produces a
page that looks exactly like a verified one.
"""

from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"
SCRIPT = ROOT / "scripts" / "save_trip_deliverables.py"


# Imported rather than rewritten. The first draft of this file hand-wrote a seven-block report
# with plausible-looking pointers -- five of which did not resolve against the fixture, so three
# cases failed for a reason unrelated to what they test. There is exactly one report in this repo
# known to satisfy check_verification, and every pointer in it is maintained against the fixture
# by the cases that use it. A second copy is a second thing to keep true.
sys.path.insert(0, str(ROOT / "tests"))
from test_plan_consistency import full_verification  # noqa: E402


def run(plan: dict, workspace: Path, *args: str,
        verification: dict | None = None) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        plan_path = Path(tmp) / "plan.json"
        plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        command = [sys.executable, str(SCRIPT), str(plan_path),
                   "--workspace", str(workspace), *args]
        if verification is not None:
            report_path = Path(tmp) / "report.json"
            report = copy.deepcopy(verification)
            report["plan"] = plan_path.name
            report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
            command += ["--verification", str(report_path)]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr


def save_refuses_bannerless_page(workspace: Path) -> bool:
    """Run the save path in-process with a renderer that emits no verification notice.

    Returns True when the save is refused. Done in-process because the flag under test is passed
    from save_trip_deliverables to validate_trip_html inside one call; from a subprocess the
    banner is always present, so the wiring is invisible either way.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    import save_trip_deliverables as save_module  # noqa: PLC0415

    plan = json.loads(FIXTURE.read_text(encoding="utf-8"))
    original_render = save_module.render
    try:
        save_module.render = lambda p: re.sub(
            r'<section id="verification-notice".*?</section>', "",
            original_render(p), flags=re.DOTALL)
        with tempfile.TemporaryDirectory() as tmp:
            plan_path = Path(tmp) / "plan.json"
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            argv = sys.argv
            try:
                sys.argv = ["save_trip_deliverables.py", str(plan_path),
                            "--workspace", str(workspace), "--unverified",
                            "--slug", "bannerless"]
                return save_module.main() != 0
            finally:
                sys.argv = argv
    finally:
        save_module.render = original_render


def main() -> int:
    base = json.loads(FIXTURE.read_text(encoding="utf-8"))
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{name}\n{detail}")

    with tempfile.TemporaryDirectory() as workspace_dir:
        workspace = Path(workspace_dir)

        # Intake provenance. SKILL.md has always made the loopback HTML form the required path
        # and the chat questionnaire a fallback the TRAVELLER chooses, and measured on other
        # harnesses assistants opened no form at all and went straight to chat -- because prose
        # cannot fail a run. These cases are what makes it fail one. Each method must arrive with
        # its own evidence, so the shortcut costs more than the form rather than less.
        missing = copy.deepcopy(base)
        del missing["intake_context"]
        code, out = run(missing, workspace, "--unverified", "--slug", "nointake")
        check("a plan that will not say how intake happened is refused",
              code == 1 and "INTAKE PROVENANCE MISSING" in out, out)
        check("the refusal names the form command rather than only complaining",
              "start_intake_workflow.py" in out, out)
        check("a refused save writes no intake-less plan",
              not list((workspace / "plans").glob("*nointake*")), out)

        for bad, label in (
            ({"method": "form"}, "an invented method"),
            ({"method": "html_form"}, "html_form with no intake file"),
            ({"method": "html_form",
              "intake_file": "<workspace>/plans/trip-intake-<timestamp>.json"},
             "html_form still holding the template's bracketed placeholder"),
            ({"method": "user_supplied"}, "user_supplied with no source note"),
            ({"method": "chat_fallback"}, "chat_fallback with no traveller words"),
            ({"method": "chat_fallback", "declined_verbatim": "TODO: their words",
              "declined_at": "2026-08-22"}, "chat_fallback still holding a placeholder"),
            ({"method": "chat_fallback", "declined_verbatim": "不用表单了，直接问我吧",
              "declined_at": "sometime"}, "chat_fallback with an unparseable date"),
            # A valid ISO date that is nonetheless invented. The skeleton stamps every date it
            # cannot know as the epoch, and on the record that says the traveller authorised the
            # shortcut, shipping it would be a fabricated fact rather than a visible blank.
            ({"method": "chat_fallback", "declined_verbatim": "不用表单了，直接问我吧",
              "declined_at": "1970-01-01"}, "chat_fallback still stamped with the epoch sentinel"),
            # Self-contradictory: the traveller's declining words beside the path of the form
            # intake they supposedly never filled. Only one of those can be true, and a record
            # that contradicts itself reads as evidence.
            ({"method": "chat_fallback", "declined_verbatim": "不用表单了，直接问我吧",
              "declined_at": "2026-08-22", "intake_file": "/w/plans/intake-20260822.json"},
             "chat_fallback that also names a form intake file"),
        ):
            plan = copy.deepcopy(base)
            plan["intake_context"] = bad
            code, out = run(plan, workspace, "--unverified", "--slug", "badintake")
            check(f"{label} is refused", code == 1 and "INTAKE PROVENANCE MISSING" in out, out)

        # And the three legitimate routes must all pass, or the gate is just a wall. In their own
        # workspace: these are the cases that succeed, and a later case here asserts that a
        # refused save left the plans folder empty.
        with tempfile.TemporaryDirectory() as accepted_dir:
            for index, (good, label) in enumerate((
                ({"method": "html_form",
                  "intake_file": "/w/plans/intake-20260822-ams.json"},
                 "html_form naming its intake file"),
                ({"method": "user_supplied",
                  "source_note": "Traveller pasted a complete brief with dates, budget and party."},
                 "user_supplied saying what arrived instead"),
                # Ordinary prose that happens to compare two numbers. The placeholder rule was
                # written as `<[^<>]{1,60}>` first and refused this on the delivery path.
                ({"method": "user_supplied",
                  "source_note": "Budget stated as < 2000 > per person, dates fixed."},
                 "user_supplied whose note contains a spaced comparison"),
                ({"method": "chat_fallback", "declined_verbatim": "不用开表单了，直接在这里问我",
                  "declined_at": "2026-08-22"},
                 "chat_fallback carrying the traveller's own words"),
            )):
                plan = copy.deepcopy(base)
                plan["intake_context"] = good
                code, out = run(plan, Path(accepted_dir), "--unverified",
                                "--slug", f"ok-{index}-{good['method']}")
                check(f"{label} is accepted", code == 0, out)

        # The refusal that matters most: no report, no flag, no files. A structure gate cannot
        # tell you whether a fare or an opening time is true, so saving without either is the
        # one outcome that must be impossible.
        code, out = run(copy.deepcopy(base), workspace)
        check("neither --verification nor --unverified must refuse",
              code == 1 and "No verification report" in out, out)
        check("a refused save must write nothing",
              not list((workspace / "plans").glob("*.json")) if (workspace / "plans").exists()
              else True,
              "files were written despite a refusal")

        # --unverified saves, and both the JSON field and the page banner must carry the gap.
        # The JSON alone was the state SKILL.md calls out: a gap the traveller never sees.
        code, out = run(copy.deepcopy(base), workspace, "--unverified", "--slug", "unver")
        check("--unverified saves", code == 0, out)
        saved = list((workspace / "plans").glob("*unver*.json"))
        check("--unverified writes a plan file", len(saved) == 1, out)
        if saved:
            stored = json.loads(saved[0].read_text(encoding="utf-8"))
            check("--unverified records the gap in the JSON",
                  stored.get("verification_status") == "unverified",
                  json.dumps(stored.get("verification_status")))
        pages = list((workspace / "html").glob("*unver*.html"))
        check("--unverified writes a page", len(pages) == 1, out)
        if pages:
            page = pages[0].read_text(encoding="utf-8")
            check("the unverified page carries the banner the traveller reads",
                  'id="verification-notice"' in page,
                  "page saved with no 'not fact-checked' notice")

        # The assertion itself has to bite, which is a different claim from "the renderer emits a
        # banner" and was found by mutation: disabling require_unverified_banner in the save path
        # left every case above green, because they all measured the renderer. So strip the banner
        # out of a rendered page and confirm the validator refuses it. Without this, the backstop
        # for the banner would itself have had no backstop.
        sys.path.insert(0, str(ROOT / "scripts"))
        from render_final_trip_html import render  # noqa: PLC0415 - import after path setup
        from validate_trip_html import validate  # noqa: PLC0415

        unverified_plan = copy.deepcopy(base)
        unverified_plan["verification_status"] = "unverified"
        page_html = render(unverified_plan)
        stripped_html = re.sub(r'<section id="verification-notice".*?</section>', "",
                               page_html, flags=re.DOTALL)
        check("the banner was actually removed by the test itself",
              'id="verification-notice"' not in stripped_html,
              "the strip did not match, so the case below proves nothing")
        errors = validate(stripped_html, len(unverified_plan["days"]), {"hotel"},
                          unverified_plan["transport_preference"]["mode"],
                          require_unverified_banner=True)
        check("the validator refuses an unverified page with no banner",
              any("verification notice" in e for e in errors), "; ".join(errors))
        errors = validate(page_html, len(unverified_plan["days"]), {"hotel"},
                          unverified_plan["transport_preference"]["mode"],
                          require_unverified_banner=True)
        check("the banner requirement does not fire on a page that has one",
              not any("verification notice" in e for e in errors), "; ".join(errors))

        # And that the save path actually asks for it. The two cases above pass whether or not it
        # does -- they call the validator directly -- so hard-coding require_unverified_banner to
        # False in save_trip_deliverables.py left the whole file green. The only way to see the
        # wiring is to make the renderer produce a page with no banner and check that saving it
        # is refused, which is what patching `render` in the module under test does.
        check("the save path requests the banner check",
              save_refuses_bannerless_page(workspace),
              "a page with no verification notice was saved for an unverified plan")

        # --- the photographs, which are no longer inside the plan --------------------------
        # fetch_plan_imagery.py writes them to <plan-stem>-imagery.json beside the plan, because
        # writing them inline made 96% of one delivered plan base64 and every gate re-read of it
        # cost ~576k tokens. This path is the one that hands a traveller their files, so it has
        # two jobs the renderer does not: render WITH the photographs while saving a plan file
        # WITHOUT them, and copy the sidecar next to the plan it saves -- otherwise the workspace
        # copy would point back at a scratch directory and the first re-render from the workspace
        # would refuse, correctly and uselessly.
        # ROOT/"tests" is already on sys.path from the full_verification import at the top.
        from test_plan_imagery import photo, render_page  # noqa: PLC0415 - one fixture shape only

        payload = {"hero": photo("Chengdu", "Chengdu"),
                   "anchor:0": photo("Central-city rhythm", "Jinli")}
        for label, slug, plan_extra, sidecar in (
            ("a plan whose photographs are in a sidecar", "imgsidecar",
             {"imagery_sidecar": "src-imagery.json"}, payload),
            # The migration case. A plan delivered before the split carries the bytes inline and
            # is a document a traveller may open at any time, so it must save rather than be
            # refused -- and the workspace copy it produces must be the small shape.
            ("a plan delivered before the split, with the bytes inline", "imginline",
             {"imagery": payload}, None),
        ):
            with tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "src.json"
                source.write_text(json.dumps({**base, **plan_extra}, ensure_ascii=False),
                                  encoding="utf-8")
                if sidecar is not None:
                    (Path(tmp) / "src-imagery.json").write_text(
                        json.dumps(sidecar, ensure_ascii=False), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), str(source), "--workspace", str(workspace),
                     "--unverified", "--slug", slug], capture_output=True, text=True)
                out = result.stdout + result.stderr
                check(f"{label}: saves", result.returncode == 0, out)
                plans = list((workspace / "plans").glob(f"*{slug}.json"))
                pages = list((workspace / "html").glob(f"*{slug}.html"))
                if not (plans and pages):
                    check(f"{label}: writes both files", False, out)
                    continue
                stored = json.loads(plans[0].read_text(encoding="utf-8"))
                beside = plans[0].with_name(plans[0].stem + "-imagery.json")
                check(f"{label}: the saved plan keeps no image bytes",
                      "imagery" not in stored and "base64" not in plans[0].read_text(encoding="utf-8"),
                      f"saved plan is {plans[0].stat().st_size} bytes")
                check(f"{label}: the sidecar is written beside the saved plan, under its stem",
                      beside.is_file() and stored.get("imagery_sidecar") == beside.name,
                      f"{stored.get('imagery_sidecar')!r}; sidecar exists: {beside.exists()}")
                check(f"{label}: the saved page still shows both photographs",
                      pages[0].read_text(encoding="utf-8").count("<img") == 2,
                      f"{pages[0].read_text(encoding='utf-8').count('<img')} image(s)")
                # The loop SKILL.md mandates: every gate finding sends the reader back to the
                # saved plan. Re-rendering it must produce the same page, or the split would have
                # quietly cost the traveller their photographs one save later.
                code, html = render_page(plans[0])
                check(f"{label}: re-rendering the saved plan finds the photographs again",
                      code == 0 and html.count("<img") == 2, html[:300])

        # A save that cannot find the payload must refuse, and refuse before writing anything.
        # Nothing downstream counts images: `imagery` appears zero times in
        # check_plan_consistency.py and validate_trip_html.py, so a page missing every photograph
        # passes every gate and looks exactly like a correct one.
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "src.json"
            source.write_text(
                json.dumps({**base, "imagery_sidecar": "not-here-imagery.json"},
                           ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), "--workspace", str(workspace),
                 "--unverified", "--slug", "lostphotos"], capture_output=True, text=True)
            out = result.stdout + result.stderr
            check("a plan naming a sidecar that is not there refuses to save",
                  result.returncode != 0 and "not-here-imagery.json" in out
                  and "Traceback" not in out, out[:600])
            check("the refused save wrote no files",
                  not list((workspace / "plans").glob("*lostphotos*"))
                  and not list((workspace / "html").glob("*lostphotos*")), out)

        # A migration that produces a file the rest of the skill cannot open is not a migration.
        #
        # A pre-split plan carrying its photographs inline is exactly the case the resolve step
        # deliberately does not refuse -- it is a document a traveller already has. But the saved
        # copy is written to a SIDECAR, and resolve_plan_imagery stats a sidecar and refuses
        # anything over the 4,000,000-byte ceiling before it parses. Measured on a 4.9MB inline
        # plan: the save exited 0 printing a `note:` among six other notes, and from then on
        # `render_final_trip_html.py <saved plan>` exited 2 and `save_trip_deliverables.py <saved
        # plan>` exited 2 -- the save permanently bricked the workspace plan it had just written.
        sys.path.insert(0, str(ROOT / "scripts"))
        from fetch_plan_imagery import MAX_IMAGERY_TOTAL_BYTES  # noqa: PLC0415

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "legacy.json"
            oversize = {"hero": {**photo("Chengdu", "Chengdu"),
                                 "data_uri": "data:image/png;base64,"
                                             + "A" * MAX_IMAGERY_TOTAL_BYTES}}
            source.write_text(json.dumps({**base, "imagery": oversize}, ensure_ascii=False),
                              encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), "--workspace", str(workspace),
                 "--unverified", "--slug", "oversize"], capture_output=True, text=True)
            out = result.stdout + result.stderr
            check("a save that would write an unreadable sidecar refuses instead",
                  result.returncode != 0 and "ceiling" in out and "Traceback" not in out, out[-600:])
            check("and the refused save leaves no half-migrated deliverables behind",
                  not list((workspace / "plans").glob("*oversize*"))
                  and not list((workspace / "html").glob("*oversize*")), out[-400:])
            # The refusal has to be actionable, and the message it used to print was not: it told
            # the operator to "Lower --max-images (default 6) and re-run" on a script that has no
            # such flag. An instruction that cannot be carried out reads as the tool not knowing
            # what it is doing, and the next thing tried is ignoring it.
            flagless = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), "--workspace", str(workspace),
                 "--unverified", "--max-images", "3"], capture_output=True, text=True)
            check("the flag the old message named really is not on this script",
                  flagless.returncode == 2 and "unrecognized arguments" in flagless.stderr,
                  flagless.stderr[:300])
            check("so the refusal names the script that does own it, and this one by name",
                  "fetch_plan_imagery.py" in out and "save_trip_deliverables.py has no "
                  "--max-images" in out, out[-600:])

        # The two saved deliverables must never disagree about the same trip.
        #
        # Save A writes <stem>.json + <stem>-imagery.json. Save B for the same slug with
        # --overwrite, from a plan whose photographs were never fetched, used to write no sidecar,
        # set no key, and delete nothing -- there was no unlink anywhere in the script. Measured:
        # the delivered page carried 0 photographs while re-rendering the delivered plan beside the
        # leftover sidecar carried 2, because the sidecar is found by name. The name check cannot
        # catch this one either: a stale sidecar for the SAME slug names the same destination and
        # the same anchors, so it is genuinely this trip's payload -- just the payload of a save
        # that has been replaced.
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "with-photos.json"
            first.write_text(
                json.dumps({**base, "imagery_sidecar": "with-photos-imagery.json"},
                           ensure_ascii=False), encoding="utf-8")
            (Path(tmp) / "with-photos-imagery.json").write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            code_a = subprocess.run(
                [sys.executable, str(SCRIPT), str(first), "--workspace", str(workspace),
                 "--unverified", "--slug", "samestem"], capture_output=True, text=True)
            check("save A, with photographs, succeeds", code_a.returncode == 0,
                  code_a.stdout + code_a.stderr)

            second = Path(tmp) / "without-photos.json"
            second.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(second), "--workspace", str(workspace),
                 "--unverified", "--slug", "samestem", "--overwrite"],
                capture_output=True, text=True)
            out = result.stdout + result.stderr
            check("save B, without photographs, succeeds", result.returncode == 0, out[-400:])
            saved_plan = next(iter((workspace / "plans").glob("*samestem.json")), None)
            saved_page = next(iter((workspace / "html").glob("*samestem.html")), None)
            if not (saved_plan and saved_page):
                check("the overwrite wrote both files", False, out[-400:])
            else:
                stale = saved_plan.with_name(saved_plan.stem + "-imagery.json")
                check("the previous save's photographs do not outlive it",
                      not stale.exists(), f"{stale} is still on disk")
                # Deleting a traveller's photographs is not something to do quietly.
                check("and their removal is said out loud",
                      "removed" in out and stale.name in out, out[-400:])
                delivered = saved_page.read_text(encoding="utf-8")
                code, rerendered = render_page(saved_plan)
                check("the delivered page and a re-render of the delivered plan now agree",
                      code == 0 and rerendered.count("<img") == delivered.count("<img") == 0,
                      f"delivered={delivered.count('<img')} "
                      f"re-rendered={rerendered.count('<img')}\n{rerendered[:200]}")

            # And the unlink must be narrow: a photographed save over a photographed slug replaces
            # the sidecar rather than losing it. A cleanup that fires on the wrong branch would
            # delete the photographs of every save that has them.
            replacement = {"hero": photo("Chengdu", "Chengdu")}
            third = Path(tmp) / "again.json"
            third.write_text(json.dumps({**base, "imagery_sidecar": "again-imagery.json"},
                                        ensure_ascii=False), encoding="utf-8")
            (Path(tmp) / "again-imagery.json").write_text(
                json.dumps(replacement, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(third), "--workspace", str(workspace),
                 "--unverified", "--slug", "samestem", "--overwrite"],
                capture_output=True, text=True)
            saved_plan = next(iter((workspace / "plans").glob("*samestem.json")), None)
            restored = saved_plan.with_name(saved_plan.stem + "-imagery.json")
            check("a photographed save over the same slug keeps its photographs",
                  result.returncode == 0 and restored.is_file()
                  and len(json.loads(restored.read_text(encoding="utf-8"))) == 1,
                  result.stdout + result.stderr)

        # The documented `-` mode, on the skill's own normal output. `imagery_sidecar` is a name
        # relative to the plan, and a piped plan has no location for it to be relative to, so the
        # name was resolved against whatever directory the command ran from: measured, the pipe
        # delivered a DIFFERENT trip's photograph, with that trip's photographer and licence
        # printed underneath, whenever the cwd happened to hold a file of the same name.
        with tempfile.TemporaryDirectory() as tmp:
            elsewhere = Path(tmp) / "elsewhere"
            elsewhere.mkdir()
            foreign = {"hero": {**photo("Larnaca", "Larnaca"),
                                "artist": "Another Trip's Photographer"}}
            (elsewhere / "piped-imagery.json").write_text(json.dumps(foreign, ensure_ascii=False),
                                                          encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "-", "--workspace", str(workspace),
                 "--unverified", "--slug", "piped"],
                input=json.dumps({**base, "imagery_sidecar": "piped-imagery.json"},
                                 ensure_ascii=False),
                capture_output=True, text=True, cwd=str(elsewhere))
            out = result.stdout + result.stderr
            check("a piped plan does not adopt a same-named payload from the current directory",
                  result.returncode != 0 and "Traceback" not in out, out[:400])
            check("and no page is delivered carrying another trip's photograph",
                  not list((workspace / "html").glob("*piped*")), out[:200])
            # The mode still works where nothing has to be guessed, which is what keeps the
            # refusal above a fix rather than an amputation.
            plain = subprocess.run(
                [sys.executable, str(SCRIPT), "-", "--workspace", str(workspace),
                 "--unverified", "--slug", "pipedplain"],
                input=json.dumps(base, ensure_ascii=False), capture_output=True, text=True,
                cwd=str(elsewhere))
            check("a piped plan with no photographs still saves",
                  plain.returncode == 0 and len(list((workspace / "html").glob("*pipedplain*"))) == 1,
                  (plain.stdout + plain.stderr)[-400:])

        # A plan whose verification_status is missing entirely must be treated as unverified,
        # not as verified. Every skeleton starts in this state and replan_trip.py returns to it.
        stripped = copy.deepcopy(base)
        stripped.pop("verification_status", None)
        code, out = run(stripped, workspace, "--unverified", "--slug", "nostatus")
        nostatus = list((workspace / "html").glob("*nostatus*.html"))
        check("a plan with no verification_status still gets the banner",
              code == 0 and len(nostatus) == 1
              and 'id="verification-notice"' in nostatus[0].read_text(encoding="utf-8"), out)

        # With a real report it saves clean and the banner is correctly absent.
        code, out = run(copy.deepcopy(base), workspace, "--slug", "ver",
                        verification=full_verification())
        check("a verified plan saves", code == 0, out)
        verified_pages = list((workspace / "html").glob("*-ver.html"))
        check("a verified page carries no unverified banner",
              len(verified_pages) == 1
              and 'id="verification-notice"' not in verified_pages[0].read_text(encoding="utf-8"),
              out)

        # A consistency failure must stop the write, not merely be printed. The two are easy to
        # confuse when the script prints errors and then continues to the file-writing lines.
        broken = copy.deepcopy(base)
        broken["days"][0]["route"]["duration_minutes"] = 999
        code, out = run(broken, workspace, "--unverified", "--slug", "broken")
        check("a consistency failure refuses", code == 1, out)
        check("a consistency failure writes nothing",
              not (workspace / "plans" / "broken.json").exists()
              and not (workspace / "html" / "broken.html").exists(),
              "files were written despite failing consistency")

        # Adding a check to PLAN_CHECKS must arm this path too -- that is the entire reason the
        # tuple is imported rather than restated. The market rule is the newest entry, so it is
        # the one that proves the wiring is still live.
        #
        # The case is chosen to sit outside render_final_trip_html's map_link_allowed, or it would
        # prove only that validate_plan still runs and would pass with PLAN_CHECKS unwired
        # entirely. That rule keys on the market string being exactly "mainland_china"; a plan
        # that writes the same market in Chinese, with access still unestablished, is invisible
        # to it and visible to this one.
        market = copy.deepcopy(base)
        market["regional_service_context"]["destination_service_market"] = "中国大陆"
        market["regional_service_context"]["google_services_access"] = "unknown"
        code, out = run(market, workspace, "--unverified", "--slug", "market")
        check("the newest PLAN_CHECKS entry runs on the save path",
              code == 1 and "the honest value is 'unavailable'" in out, out)

        # An overwrite must be asked for. Two plans for one trip, silently replacing each other,
        # is the shape of the incident SKILL.md records under the intake workflow.
        code, out = run(copy.deepcopy(base), workspace, "--unverified", "--slug", "unver")
        check("saving over an existing slug refuses without --overwrite",
              code == 2 and "already exists" in out, out)
        code, out = run(copy.deepcopy(base), workspace, "--unverified", "--slug", "unver",
                        "--overwrite")
        check("--overwrite replaces deliberately", code == 0, out)

        # A malformed report is a refusal, not a traceback: an operator who sees a stack trace
        # learns nothing about their plan and tends to stop running the gate.
        with tempfile.TemporaryDirectory() as tmp:
            plan_path = Path(tmp) / "plan.json"
            plan_path.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
            bad_report = Path(tmp) / "bad.json"
            bad_report.write_text("{not json", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(plan_path), "--workspace", str(workspace),
                 "--verification", str(bad_report), "--slug", "badreport"],
                capture_output=True, text=True)
            check("an unreadable verification report refuses cleanly",
                  result.returncode == 2 and "Traceback" not in result.stderr,
                  result.stdout + result.stderr)

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all save-deliverables regression cases passed")
    return 0


def test_save_deliverables() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
