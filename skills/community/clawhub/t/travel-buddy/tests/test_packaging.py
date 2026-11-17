#!/usr/bin/env python3
"""Packaging and contract-integrity checks.

The skill ships three ways -- `npx skills add`, the Claude Code plugin manifests, and a plain
clone -- and all three copy the repository as-is. So the things that break installation are not
build errors but drift: a manifest whose versions disagree, a SKILL.md pointing at a file that no
longer exists, a reference file nobody links to (which is the same as deleting it), and a data
contract that omits fields the gates now require.

That last one is what motivated this file. `check_plan_consistency.py` gained required dining and
budget fields, and `templates/final-trip-plan.json` -- the contract people actually copy -- was
not updated with them, so anyone following the template would have walked straight into a failing
gate with no hint why.

Run:  python tests/test_packaging.py
      python -m pytest tests/test_packaging.py
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Fields the deterministic gate requires, and where a plan author would look for them.
#
# The last two entries were added after the same drift happened again, one release later and in
# both directions at once. `untyped_constraints` shipped live in four places -- the skeleton wrote
# it, check_plan_consistency refused a plan carrying it, check_walking_budget read it, and
# required_domains_for withheld the light verification tier over it -- while `grep -c
# untyped_constraints templates/final-trip-plan.json` returned 0, so an author filling in the
# contract met a refusal naming a key the contract had never shown them. `imagery_sidecar` was the
# quieter half of the same gap: fetch_plan_imagery.py writes it into the plan and two consumers
# refuse loudly when it names a file that is not there, and the contract said nothing at all. Key
# PRESENCE is all this asserts -- the template's own values are `{}` and `null`, both of which mean
# "not filled in" to every reader -- because presence is exactly what was missing.
CONTRACT_FIELDS = {
    "dining card": ("days.0.dining.0", {"route_anchor", "off_route_justification",
                                        "venue_hours", "hours_status"}),
    "budget": ("budget", {"cap_per_person", "overrun_acknowledged"}),
    "plan root": ("", {"verification_status", "verification_report", "imagery_sidecar"}),
    "traveler constraints": ("trip.traveler_constraints", {"untyped_constraints"}),
}


# Files removed on purpose, each with the reason, because this repository had nowhere to write
# one down. A deletion and an accident look identical in a tree: the file is simply not there, and
# the next author who misses it restores it in good faith. `CHECKS_WITHOUT_A_REFERENCE` already
# established the shape of the answer for gate checks -- an explicit entry carrying a reason, so
# that silence is never mistaken for a decision -- and this is that idiom applied to files.
#
# Entries stay forever; this is a register, not a to-do list. Removing one re-opens the question.
DELETED_ON_PURPOSE = {
    "assets/final-trip-template.html": (
        "A hand-assembly starting point in a skill that forbids hand assembly. SKILL.md's "
        "final-delivery gate says 'Never hand the traveller a page you assembled yourself', "
        "because every check here is a script and a script runs only when it is called, so a "
        "hand-written page bypasses all of them and otherwise looks identical. The file was "
        "offered as 'the structural starting point' in a sentence that then told the reader to "
        "prefer the renderer instead, which is advice arguing with itself. Nothing loaded it: no "
        "script referenced it (the two intake servers reach assets/ by pathlib, for the two forms "
        "they serve), and it was named only in SKILL.md and references/booking-html-output.md, "
        "both pointing at the path this skill refuses to take. Run through its own validator with "
        "the manual flags it allows, the file was INVALID -- exit 1, and among the findings, "
        "unsupported booking type '{{booking_type}}', map links that are not directions URLs, a "
        "missing verification banner, and 'Final HTML still contains a template token or TODO'. "
        "The renderer emits the same structure and is gated; the JSON contract carries the "
        "fields. Neither job needed this file. Deleted deliberately at 2.4.0; git history holds "
        "it at 64b8b34 if the shape is ever wanted again."),
}


def dig(plan: dict, path: str):
    node = plan
    for part in filter(None, path.split(".")):
        node = node[int(part)] if part.isdigit() else node[part]
    return node


def main() -> int:
    failures: list[str] = []

    # 1. Manifest agreement. Two files describe the same plugin; a version skew ships a plugin
    #    whose marketplace entry advertises something the manifest does not.
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    entry = market["plugins"][0]

    versions = {plugin["version"], market["metadata"]["version"], entry["version"]}
    if len(versions) != 1:
        failures.append(f"manifest versions disagree: {sorted(versions)}")
    for field in ("name", "description", "homepage", "repository", "license", "version"):
        if field in entry and plugin.get(field) != entry.get(field):
            failures.append(
                f"manifest field {field!r} differs: plugin.json={plugin.get(field)!r} "
                f"marketplace.json={entry.get(field)!r}")

    # 1b. The fourth copy of the version, which the check above cannot see. Wikimedia asks
    #     clients to identify themselves, so fetch_plan_imagery.py sends the release in its
    #     User-Agent -- and being a string in a Python file rather than a manifest field, it is
    #     the one that drifts: nothing failed when the manifests went to 2.2.0 and it did not.
    #     Only major.minor is carried there, so only major.minor is compared.
    agent_source = (ROOT / "scripts" / "fetch_plan_imagery.py").read_text(encoding="utf-8")
    agent_match = re.search(r"travel-buddy/(\d+\.\d+)", agent_source)
    expected_agent = ".".join(plugin["version"].split(".")[:2])
    if not agent_match:
        failures.append("fetch_plan_imagery.py sends no travel-buddy/<version> User-Agent")
    elif agent_match.group(1) != expected_agent:
        failures.append(
            f"User-Agent version {agent_match.group(1)!r} does not match the manifest's "
            f"{expected_agent!r} (plugin.json says {plugin['version']!r})")

    # 2. SKILL.md must not point at anything that is not shipped.
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    referenced = set(re.findall(r"\]\((references/[^)]+|templates/[^)]+|assets/[^)]+)\)", skill))
    referenced |= set(re.findall(r"`?python (scripts/[a-z_]+\.py)", skill))
    referenced |= set(re.findall(r"`(scripts/[a-z_]+\.py)`", skill))
    for target in sorted(referenced):
        if not (ROOT / target).exists():
            failures.append(f"SKILL.md references {target}, which does not exist")

    # 2a-ii. A count written into prose drifts, and nothing was watching this one: SKILL.md said
    #        "the same 24 PLAN_CHECKS" while the tuple held 29. That is the attestation-versus-check
    #        problem in the skill's own documentation -- the sentence claimed a number instead of
    #        naming the thing, and a reader budgeting a run believed it. The fix was to stop writing
    #        the number; this asserts that nobody writes one back.
    import re as _re
    _sys_path_added = str(ROOT / "scripts")
    if _sys_path_added not in sys.path:
        sys.path.insert(0, _sys_path_added)
    from check_plan_consistency import PLAN_CHECKS as _CHECKS  # noqa: PLC0415
    for _doc in ("SKILL.md", "README.md", "README_CN.md"):
        _text = (ROOT / _doc).read_text(encoding="utf-8")
        for _match in _re.finditer(r"(\d+)\s*(?:个\s*)?`?PLAN_CHECKS", _text):
            _claimed = int(_match.group(1))
            if _claimed != len(_CHECKS):
                _line = _text[:_match.start()].count("\n") + 1
                failures.append(
                    f"{_doc}:{_line} says {_claimed} PLAN_CHECKS and the tuple holds "
                    f"{len(_CHECKS)}. Name the tuple instead of counting it, or update the number "
                    f"-- a stale count in prose is read as a measurement.")

    # 2a-iii. Every gate that exits clean must name the next command, and the command it names
    #         must exist. Measured with a different assistant on a deliberately broken plan: codex
    #         ran check_plan_contract and check_plan_consistency, fixed everything both reported,
    #         saw two clean exits and reported the plan fixed -- while a third defect survived,
    #         because the rule that catches it lives in render_final_trip_html.validate_plan, a
    #         command it never reached. Nothing was wrong with its reasoning. The pipeline did not
    #         say where it continues, and an assistant that cannot hold 110KB of prose rebuilds the
    #         order from whatever the last command printed. A clean gate is the most dangerous
    #         place to stay silent, which is why this is asserted on the SUCCESS path.
    _chain = {
        "new_plan_skeleton.py": "check_plan_contract.py",
        "check_plan_contract.py": "check_plan_consistency.py",
        "check_plan_consistency.py": "render_final_trip_html.py",
        "render_final_trip_html.py": "validate_trip_html.py",
        "validate_trip_html.py": "check_link_targets.py",
    }
    for _script, _next in _chain.items():
        _source = (ROOT / "scripts" / _script).read_text(encoding="utf-8")
        if "NEXT:" not in _source:
            failures.append(
                f"scripts/{_script} never prints a NEXT: line. A gate that exits clean without "
                f"naming the next command is where an assistant stops, believing the pipeline "
                f"finished.")
        elif _next not in _source:
            failures.append(
                f"scripts/{_script} prints a NEXT: line that does not name scripts/{_next}, which "
                f"is the step that follows it. A pointer to the wrong command is worse than none.")
        if not (ROOT / "scripts" / _next).exists():
            failures.append(f"scripts/{_script} points at scripts/{_next}, which does not exist.")

    # The waiver branch is, by its own name, the moment a report is still owed -- so it is the one
    # place that has to say how one is started. Before it did, an assistant following the printed
    # order went from here straight to the renderer and reached delivery with --unverified having
    # never learned a scaffold existed. Every plan in the author's workspace took that path:
    # seventeen delivered, zero surviving verification reports.
    _waiver = (ROOT / "scripts" / "check_plan_consistency.py").read_text(encoding="utf-8")
    if "new_verification_report.py" not in _waiver:
        failures.append(
            "check_plan_consistency.py never names scripts/new_verification_report.py. The "
            "--no-verification-yet branch is the moment the report is still owed, and an assistant "
            "that is not told how to start one delivers with --unverified instead.")

    # 2b. The other direction of check 2, and the one nothing was watching: a file deleted on
    #     purpose must stay deleted, and must stay unmentioned.
    #
    #     Check 2 catches a pointer to a file that is gone. It cannot catch the opposite repair,
    #     which is the likelier one -- an author meets a reference to a file that does not exist,
    #     assumes the deletion was the mistake, and restores the file from git. That reading is
    #     reasonable, and here it would be wrong, so the reason is written in DELETED_ON_PURPOSE
    #     and this check makes it unmissable rather than leaving it to be rediscovered.
    #
    #     Both halves are asserted because either alone is passable while the intent is defeated.
    #     Restoring the file with no pointer leaves dead weight in the package that the next
    #     reader takes for something shipped; adding a pointer back without the file trips check 2
    #     with a message about a missing file, which invites exactly the wrong repair. The reason
    #     is required to be substantial for the same motive check 5c has: an entry with an empty
    #     string in it is a deletion nobody explained, which is the state this register exists to
    #     end.
    for path, reason in sorted(DELETED_ON_PURPOSE.items()):
        if len(reason.split()) < 12:
            failures.append(
                f"DELETED_ON_PURPOSE[{path!r}] gives no real reason. Write why the file was "
                f"removed and what replaced it; a bare entry is the silence this register "
                f"replaces.")
        if (ROOT / path).exists():
            failures.append(
                f"{path} is back, but it was deleted on purpose. If restoring it is right, delete "
                f"its DELETED_ON_PURPOSE entry in the same change and say why the reason no "
                f"longer holds. The recorded reason was: {reason}")
        pointing = [name for name, text in (("SKILL.md", skill),) + tuple(
            (ref.relative_to(ROOT).as_posix(), ref.read_text(encoding="utf-8"))
            for ref in sorted((ROOT / "references").glob("*.md"))) if path in text]
        if pointing:
            failures.append(
                f"{', '.join(pointing)} still points at {path}, which was deleted on purpose, so "
                f"a reader is sent to a file that is not shipped. The recorded reason was: "
                f"{reason}")

    # 3. A reference file with no pointer in SKILL.md is unreachable, which is indistinguishable
    #    from having deleted it -- the model never learns it should be read.
    for ref in sorted((ROOT / "references").glob("*.md")):
        if ref.relative_to(ROOT).as_posix() not in skill:
            failures.append(f"{ref.relative_to(ROOT)} has no pointer in SKILL.md; nothing would read it")

    # 4. The shipped contract must carry every field the gates require.
    template = json.loads((ROOT / "templates" / "final-trip-plan.json").read_text(encoding="utf-8"))
    for label, (path, required) in CONTRACT_FIELDS.items():
        try:
            node = dig(template, path)
        except (KeyError, IndexError, TypeError):
            failures.append(f"template has no {label} at {path!r}")
            continue
        missing = required - set(node)
        if missing:
            failures.append(
                f"templates/final-trip-plan.json {label} is missing {sorted(missing)}. Anyone "
                f"copying the contract would fail check_plan_consistency.py with no hint why.")

    # 4b. The verification contract people copy must satisfy the checker that consumes it.
    report = json.loads((ROOT / "templates" / "verification-report.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT / "scripts"))
    from check_plan_consistency import REQUIRED_DOMAINS  # noqa: PLC0415 - import after path setup

    shipped = {d.get("domain") for d in report.get("domains", [])}
    if shipped != REQUIRED_DOMAINS:
        failures.append(
            f"templates/verification-report.json covers {sorted(shipped)} but the checker requires "
            f"exactly {sorted(REQUIRED_DOMAINS)}")
    #    claims_checked stopped being a count and became the list of plan pointers each block
    #    opened, because a count is a promise the same run writes about itself. The template is
    #    what operators copy, so a template still carrying `"claims_checked": 0` teaches the one
    #    shape the checker now rejects, and the author's first contact with the change is a failing
    #    gate on their own trip rather than a line in the file they copied.
    for block, label in ([(d, f"domain {d.get('domain')!r}") for d in report.get("domains", [])]
                         + [(a, f"audit {a.get('audit')!r}") for a in report.get("audits", [])]):
        if "claims_checked" not in block:
            failures.append(
                f"verification-report template {label} omits claims_checked, "
                f"which the checker requires — the template would teach the wrong shape")
        elif not isinstance(block["claims_checked"], list):
            failures.append(
                f"verification-report template {label} sets claims_checked to "
                f"{block['claims_checked']!r}. The checker now requires a list of plan pointers, "
                f'e.g. ["days[0].dining[0].venue_hours"], and rejects a number outright.')

    # 5. Every shipped template must be reachable from SKILL.md or a reference it points at.
    #    A template nobody links to is a template nobody copies, which is the same as not
    #    shipping it -- and the README is not a valid home for that pointer, since it is
    #    documentation for humans browsing GitHub rather than context the model receives.
    #    Missing files are skipped rather than opened: check 2 above already reports every
    #    SKILL.md reference that does not exist, and reading one here raised FileNotFoundError
    #    before any failure was printed -- so a single missing reference replaced the whole
    #    packaging report with a stack trace naming one file, which is how a checkable failure
    #    turns into a mystery.
    reachable = skill + "\n".join(
        (ROOT / ref).read_text(encoding="utf-8")
        for ref in referenced if ref.startswith("references/") and (ROOT / ref).exists())
    for template in sorted((ROOT / "templates").glob("*.json")):
        name = template.name
        if name.endswith(".example.json"):
            continue  # opt-in example, named in SKILL.md prose only when the case arises
        if name not in reachable:
            failures.append(
                f"templates/{name} is shipped but nothing in SKILL.md or its references points at "
                f"it; nobody would know to copy it")

    # 5b. Every `references/<file>.md#<anchor>` a gate can print must resolve to an anchor that
    #     exists. The four gates now append the owning reference to their findings -- several
    #     hundred places could refuse a plan and a handful said where the rule was written, which
    #     is what this change is against -- and a citation that
    #     404s is worse than no citation at all: it costs a reader a lookup and then teaches them
    #     that the pointers cannot be trusted, which retires the whole mechanism.
    #
    #     This has to be a test rather than a convention because the two halves drift apart in
    #     silence. Renaming a heading in a reference, or fixing a typo in a rule id, breaks a
    #     pointer that nothing executes: the citation is a string in an f-string, so no import
    #     fails, no gate errors, and the suite stays green while every author who trips that rule
    #     is sent to a fragment that does not exist. The scripts' own tests cannot catch it either
    #     -- they assert on the message, and the message is fine.
    #
    #     Anchors are matched against `<a id="...">` markers rather than against heading slugs on
    #     purpose. A slug is derived from the heading text, so rewording a heading silently moves
    #     it; an explicit id survives every rewording, and the failure mode when someone deletes
    #     one is this test, which is the loud outcome. Both forms are accepted when reading, so a
    #     citation may point at a heading slug -- but nothing does, and nothing needs to.
    #
    #     Scanned as text, not by importing the four gates and reading their registries. Two
    #     reasons: a citation written inline in a message rather than routed through a registry is
    #     still a citation a traveller's author will see, and this test must fail on it too; and
    #     scanning cannot be fooled by a registry entry that no code path can actually emit.
    #
    #     The `references/` prefix is OPTIONAL in this pattern, and that detail is the whole test.
    #     Written as a required prefix first -- which is how the citation reads once printed --
    #     this check passed while `<a id="map-endpoints">` was deleted from booking-html-output.md
    #     and four live citations pointed at nothing. The gates do not store the printed form: the
    #     registries hold `"booking-html-output.md#map-endpoints"` and the f-string supplies
    #     `references/` at call time, so in the SOURCE the two halves are never adjacent and a
    #     pattern anchored on the prefix matched zero of them. It reported success by checking
    #     nothing, which is the exact defect class this repo keeps paying for -- a green gate over
    #     unexamined output -- reproduced inside the test written to prevent it. Hence the floor
    #     below: a scan that finds almost nothing is now a failure rather than a pass.
    CITATION = re.compile(r"(?:references/)?([A-Za-z0-9._-]+\.md)#([A-Za-z0-9._-]+)")
    anchors: dict[str, set[str]] = {}
    for ref in (ROOT / "references").glob("*.md"):
        text = ref.read_text(encoding="utf-8")
        found = set(re.findall(r'<a\s+id="([^"]+)"\s*>', text))
        #    A heading slug is accepted as a fallback so a citation is never wrong merely for
        #    pointing at a heading that has no explicit id yet.
        for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE):
            slug = re.sub(r"[^a-z0-9\s-]", "", heading.casefold()).strip().replace(" ", "-")
            found.add(slug)
        anchors[ref.name] = found

    checked_citations = 0
    for script in sorted((ROOT / "scripts").glob("*.py")):
        source = script.read_text(encoding="utf-8")
        for filename, anchor in sorted(set(CITATION.findall(source))):
            checked_citations += 1
            if filename not in anchors:
                failures.append(
                    f"scripts/{script.name} can print a citation to references/{filename}, which "
                    f"does not exist. A failing run would be sent to a missing file.")
            elif anchor not in anchors[filename]:
                failures.append(
                    f"scripts/{script.name} can print references/{filename}#{anchor}, but that "
                    f"file has no <a id=\"{anchor}\"> and no heading with that slug. Add the "
                    f"anchor to the reference, or fix the citation -- a pointer that 404s teaches "
                    f"an author that the pointers are not worth following.")

    # 5c. Every check in the two gate tuples must have DECIDED about its reference: either it
    #     names the section that states its rule, or it is listed as deliberately having none.
    #
    #     Without this, the citations rot in the one direction nobody watches. A check added next
    #     release lands in PLAN_CHECKS, runs, refuses plans, and says nothing about where its rule
    #     is written -- and no test fails, because every anchor that IS emitted still resolves.
    #     The gate would be correct and the pointer simply absent, which is precisely the state
    #     this whole change was made to end, reappearing one check at a time.
    #
    #     Silence is not accepted as a decision, which is the entire point of reading an explicit
    #     exemption dict rather than treating "missing from the registry" as "needs no reference".
    #     Those two look identical from here and only one of them is a choice somebody made.
    for module_name, tuple_name, extra in (
            ("check_plan_consistency", "PLAN_CHECKS", ("check_verification",)),
            ("check_shortlist_consistency", "SHORTLIST_CHECKS", ("check_constraint_coverage",))):
        module = __import__(module_name)
        cited_checks = set(getattr(module, "CHECK_REFERENCES", {}))
        exempt = set(getattr(module, "CHECKS_WITHOUT_A_REFERENCE", {}))
        names = [check.__name__ for check in getattr(module, tuple_name)] + list(extra)
        for name in names:
            if name not in cited_checks and name not in exempt:
                failures.append(
                    f"{module_name}.{name} refuses plans but names no reference. Add it to "
                    f"CHECK_REFERENCES with the section that states its rule, or to "
                    f"CHECKS_WITHOUT_A_REFERENCE with the reason it needs none. Leaving it out of "
                    f"both is not a decision, and it is indistinguishable from forgetting.")
            if name in cited_checks and name in exempt:
                failures.append(
                    f"{module_name}.{name} is in both CHECK_REFERENCES and "
                    f"CHECKS_WITHOUT_A_REFERENCE, so the two disagree about whether it has a "
                    f"reference. Pick one.")

    # 5d. The same "silence is not a decision" rule, for the two gates that cite per CALL SITE.
    #
    #     5c holds check_plan_consistency and check_shortlist_consistency, and it can only hold
    #     them because their citations go on a decorator: the unit is a named function, so a check
    #     that cites nothing is a name missing from a dict and a dict is something a test can read.
    #     render_final_trip_html and validate_trip_html cite on the call instead -- their rules all
    #     live inside one validate() and one parser class, with no per-rule function to decorate --
    #     and that left a hole those files documented in their own comments and could not close:
    #     a new `errors.append("...")` ships uncited and every test stays green. That is the exact
    #     drift this change was made to end, arriving one site at a time through the back door.
    #
    #     So the census is taken from the AST rather than from a registry. Every `<sink>.append(x)`
    #     where x is not a `cite(...)` call is an uncited site, and its enclosing function must be
    #     declared in that module's SITES_WITHOUT_A_REFERENCE with a count.
    #
    #     Why the COUNT and not just the function name. validate_plan() carries 61 uncited shape
    #     rules AND cited map/booking/dining rules in the same body. Exempting the function
    #     wholesale would make it the one place in the repo where a new uncited map rule is
    #     invisible -- the largest function in the largest gate, which is precisely where nobody
    #     would look. Holding the number means a new uncited site there fails here and forces the
    #     decision to be made out loud, which is all the decorator does for the other two files.
    #
    #     Keyed by enclosing function, never by line number: line numbers move on every edit above
    #     them, and a registry that has to be renumbered to stay true will be renumbered wrongly.
    #
    #     The exemption list is checked in BOTH directions. A function that no longer has as many
    #     uncited sites as it claims is reported too -- otherwise the numbers only ever ratchet up,
    #     the dict slowly stops describing the file, and the next person to trust it is misled.
    #     Grepping for `.append(` would not do here and was tried first: it cannot see which
    #     argument is a cite() call, it counts `.append(` inside strings and comments, and it
    #     misses a call split across lines. That is a scan that reports success by matching the
    #     wrong thing, which this file has already shipped once (see the prefix bug in 5b).
    SINKS = {"errors", "findings", "problems", "issues", "warnings", "out"}
    for module_name in ("render_final_trip_html", "validate_trip_html"):
        path = ROOT / "scripts" / f"{module_name}.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))

        parents: dict[ast.AST, ast.AST] = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node

        def enclosing_function(node: ast.AST) -> str:
            cursor = parents.get(node)
            while cursor is not None:
                if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return cursor.name
                cursor = parents.get(cursor)
            return "<module>"

        uncited: dict[str, int] = {}
        total_sites = 0
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not (isinstance(func, ast.Attribute) and func.attr == "append"):
                continue
            base = func.value
            sink = base.id if isinstance(base, ast.Name) else (
                base.attr if isinstance(base, ast.Attribute) else None)
            if sink not in SINKS:
                continue
            total_sites += 1
            first = node.args[0] if node.args else None
            cited = (isinstance(first, ast.Call) and isinstance(first.func, ast.Name)
                     and first.func.id == "cite")
            if not cited:
                uncited[enclosing_function(node)] = uncited.get(enclosing_function(node), 0) + 1

        module = __import__(module_name)
        declared = getattr(module, "SITES_WITHOUT_A_REFERENCE", None)
        if declared is None:
            failures.append(
                f"scripts/{module_name}.py cites its findings per call site but declares no "
                f"SITES_WITHOUT_A_REFERENCE. Add it -- empty if every site is cited -- so 'no "
                f"uncited sites' can be told apart from 'nobody checked'.")
            continue
        #     Typed loudly rather than assumed. Written as a set -- which is the shape
        #     CHECKS_WITHOUT_A_REFERENCE's callers reach for, and this dict sits next to a registry
        #     that IS keyed the same way -- the count lookup below raises TypeError and pytest
        #     reports a crash in the packaging test rather than the one sentence that says what to
        #     fix. A gate whose failure mode is a traceback teaches people to skip it.
        if not isinstance(declared, dict) or not all(
                isinstance(k, str) and isinstance(v, int) and not isinstance(v, bool)
                for k, v in declared.items()):
            failures.append(
                f"scripts/{module_name}.py declares SITES_WITHOUT_A_REFERENCE as "
                f"{type(declared).__name__}, but it must be a dict of {{function name: number of "
                f"uncited findings}}. The count is the part that does the work -- without it a "
                f"function is exempt wholesale and a new uncited rule hides inside it.")
            continue

        for function_name, count in sorted(uncited.items()):
            if function_name not in declared:
                failures.append(
                    f"{module_name}.{function_name}() appends {count} finding(s) with no cite() "
                    f"call and is not in SITES_WITHOUT_A_REFERENCE. Either wrap the message in "
                    f"cite() with the section that states the rule, or declare the function there "
                    f"with its count and the reason the rule needs no reference. A finding that "
                    f"names no reference is a dead end for a run that never opened the file.")
            elif declared[function_name] != count:
                failures.append(
                    f"{module_name}.{function_name}() has {count} uncited finding(s) but "
                    f"SITES_WITHOUT_A_REFERENCE claims {declared[function_name]}. If a site was "
                    f"added, cite it or raise the number deliberately; if one was cited or "
                    f"removed, lower the number so the dict keeps describing the file.")

        for function_name in sorted(set(declared) - set(uncited)):
            failures.append(
                f"{module_name}.SITES_WITHOUT_A_REFERENCE lists {function_name}(), which now has "
                f"no uncited findings at all. Drop the entry -- a stale exemption grants silence "
                f"to whatever is written there next.")

        #     A floor, for the same reason 5b has one: this census reports only what it FINDS, and
        #     finding nothing looks identical to a clean file. If the AST walk stops matching --
        #     a sink renamed, the gates refactored to a helper -- every uncited site in both files
        #     becomes invisible and this section passes by checking nothing.
        if total_sites < 40:
            failures.append(
                f"the AST census found only {total_sites} error-append site(s) in "
                f"scripts/{module_name}.py, which is far below what a gate this size carries. The "
                f"walk has stopped matching rather than found a clean file, and it will report "
                f"success over every uncited finding in it.")

    #     The non-vacuity floor. Every check above reports a problem it FINDS; none of them can
    #     report that they looked at nothing, and looking at nothing is how this one first passed.
    #     The floor is deliberately far below the count the four gates currently carry -- it is
    #     here to catch a scan that has stopped working, not to freeze the number of citations, so
    #     removing a rule must not fail it while breaking the pattern must.
    MINIMUM_CITATIONS = 12
    if checked_citations < MINIMUM_CITATIONS:
        failures.append(
            f"the citation scan resolved only {checked_citations} distinct reference anchors "
            f"across scripts/, below the floor of {MINIMUM_CITATIONS}. The gates cite their "
            f"references through per-script registries; a scan that suddenly finds almost none of "
            f"them has stopped matching rather than found a clean tree, and it will report "
            f"success over every broken anchor in the repo.")

    # 6. Nothing the skill needs may be excluded from the package.
    for path in ("scripts/check_plan_consistency.py", "references/verification.md",
                 "SKILL.md", "templates/final-trip-plan.json"):
        ignored = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT).returncode == 0
        if ignored:
            failures.append(f"{path} is gitignored and would not ship")

    # 7. Both languages document the gate; a one-sided update leaves the other language wrong.
    #
    # "The docs" is a README plus its internals page, not the README alone. The READMEs used to
    # carry everything, which made them 78k and 36k characters of gate-by-gate engineering record
    # in front of a reader who wanted to know what the tool does -- so the machinery moved to
    # docs/internals*.md and the README went back to being about the trip. This check follows the
    # content instead of pinning it: what it has always been for is that no script ships
    # undocumented, and that is just as true in either file. Reading the pair also keeps the
    # failure honest in the other direction -- deleting a script's paragraph outright still fails,
    # which a relaxed-to-one-file version of this test would not have caught.
    DOCS = {"en": ("README.md", "docs/internals.md"),
            "zh": ("README_CN.md", "docs/internals_CN.md")}
    for language, files in DOCS.items():
        for name in files:
            if not (ROOT / name).exists():
                failures.append(f"{name} is missing; the {language} documentation is incomplete")
    readmes = {" + ".join(files): "\n".join((ROOT / n).read_text(encoding="utf-8")
                                            for n in files if (ROOT / n).exists())
               for files in DOCS.values()}
    for readme, text in readmes.items():
        if "check_plan_consistency.py" not in text:
            failures.append(f"{readme} does not mention check_plan_consistency.py")
        if "verification.md" not in text:
            failures.append(f"{readme} does not link references/verification.md")

    # 7b. Every user-facing script must appear in both. Naming only two files let
    #     check_link_targets.py and new_plan_skeleton.py ship undocumented: the READMEs
    #     described seven scripts while eleven existed, and nothing objected. The exemptions
    #     are listed rather than inferred, so each one stays a decision somebody made.
    INTERNAL = {
        # Launched by start_intake_workflow.py; a reader never invokes these directly.
        "serve_profile_intake.py": "started by start_intake_workflow.py",
        "serve_trip_intake.py": "started by start_intake_workflow.py",
    }
    for script in sorted((ROOT / "scripts").glob("*.py")):
        if script.name in INTERNAL:
            continue
        for readme, text in readmes.items():
            if script.name not in text:
                failures.append(
                    f"{readme} does not mention scripts/{script.name}. Either document it (the "
                    f"README if a user needs it, docs/internals*.md if only a maintainer does), "
                    f"or add it to INTERNAL in this test with the reason it needs no entry.")

    # 7c. Every flag the intake launcher takes is named where an agent reads. The launcher is the
    #     skill's mandatory first step, and a flag only its --help mentions is one no run uses:
    #     --language was added so an English conversation could open English forms, and an agent
    #     that never reads the script's source would keep opening Chinese ones.
    #     Matched per paragraph, beside the launcher's own name: the skeleton also has a --language,
    #     so "the flag appears somewhere" passed before the launcher's was documented at all.
    launcher = (ROOT / "scripts" / "start_intake_workflow.py").read_text(encoding="utf-8")
    agent_docs = "\n".join(path.read_text(encoding="utf-8")
                           for path in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))])
    launcher_paragraphs = [block for block in re.split(r"\n\s*\n", agent_docs)
                           if "start_intake_workflow.py" in block]
    for flag in sorted(set(re.findall(r'add_argument\(\s*"(--[a-z-]+)"', launcher))):
        if not any(flag in block for block in launcher_paragraphs):
            failures.append(f"start_intake_workflow.py takes {flag}, but no paragraph of SKILL.md or "
                            f"references/*.md that names the launcher mentions it, so no run will use it.")

    if failures:
        print(f"PACKAGING FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("packaging and contract integrity OK")
    return 0


def test_packaging_and_contract_integrity() -> None:
    """Pytest surface: with no test_* function pytest collects nothing from this file and prints
    "no tests ran", which a contributor or CI reads as green. Running the file directly is
    unchanged."""
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
