#!/usr/bin/env python3
"""Run a new, safe destination-discovery agent after a saved local intake.

This is intentionally a new non-interactive Codex/Claude task rather than
resuming the "last" CLI conversation, which could belong to another trip.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from intake_language import normalize_language  # noqa: E402

# The names a detached planner is told to write in, one per page language the forms speak.
LANGUAGE_NAMES = {"en": "English", "zh": "Chinese (简体中文)"}


ASSISTANTS = {"auto", "codex", "claude", "none"}


# Set by a running Codex/Claude CLI. Their presence proves an assistant is ALREADY driving
# this workspace and is waiting on the form -- it is the one situation where starting another
# one is wrong, not the trigger for it. This tuple is a shortcut, never the safety net: see
# interactive_terminal() for why enumerating assistants cannot be the test.
ASSISTANT_ALREADY_DRIVING = ("CLAUDECODE", "CLAUDE_CODE", "CODEX_THREAD_ID")


def interactive_terminal() -> bool:
    """True only when a human started this process at an interactive terminal.

    Auto-continuation exists for exactly one case: the traveller ran the intake themselves from a
    shell, submitted the form, and would otherwise be left holding a saved JSON file and no next
    step. Every other caller -- an assistant's tool call, a CI job, a cron entry, a redirected
    run -- already has something driving it, and a second planner there is the defect this whole
    module is about.

    That case has to be recognised POSITIVELY. The previous version tested for it by listing the
    assistants it knew (CLAUDECODE, CLAUDE_CODE, CODEX_THREAD_ID) and treating anything else as a
    bare terminal, which quietly made every other harness -- Gemini CLI, Cursor, Copilot CLI,
    opencode, an SDK agent -- fall through to the spawn branch and start a detached Codex behind
    an assistant that was already planning the same trip. A denylist of assistant names can only
    ever be as current as the day it was written; "did a human open this terminal" does not go
    stale. Both stdin and stdout are checked because a harness that pipes only one of them is
    still not a person at a keyboard.

    Residual gap, stated rather than hidden: a harness that allocates a full pty looks like a
    terminal here. The env markers above catch the two we know, and --assistant none or
    TRAVEL_BUDDY_ASSISTANT=none is the explicit escape for the rest.

    That residual gap is no longer a gap this function is allowed to lose, because it no longer
    gates the spawn at all. opencode, Cursor and Cline set none of the markers above AND allocate
    a full pty, so on the owner's own machine -- where `codex` sits on PATH at
    ~/.local/bin/codex -- `auto` read "human at a keyboard" and started exactly the detached
    second planner this whole module exists to prevent. The lesson is that a tty answers "is a
    terminal device attached", which is not the question: "did a human open this, with nothing
    else already listening" has no signal at all, because allocating a pty is the cheapest way
    for a harness to look like a shell. The prose escape this paragraph used to offer -- "pass
    --assistant none if you are in one" -- asked the harness to know it was the exception, which
    is the same losing bet as the assistant-name list one paragraph up, only phrased as
    documentation instead of code. So resolve_assistant() now stands down under `auto` whatever
    this returns, and this function survives to say WHY it stood down. Keep it: "no terminal
    here" and "a terminal, but auto still never spawns" send the caller to two different next
    steps, and a stand-down with no reason reads like a crash.
    """
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except (AttributeError, ValueError, OSError):
        # A closed or replaced stream is not a terminal, and guessing "yes" here spawns.
        return False


def announce_stand_down(reason: str) -> None:
    """Say out loud that `auto` launched nothing, and how to launch something on purpose.

    A stand-down that prints nothing is indistinguishable from a crash, from a no-op, and from a
    child that started and died -- and the caller here is usually a model, which will read the
    silence as "the runner handled it" and stop. That is how a traveller ends up with neither
    planner: the assistant believes a discovery task is running, the discovery task was never
    started, and nobody is left holding the intake. serve_trip_intake.py already prints its own
    "nothing was launched" line, but never how to get a child on purpose, so a caller who
    genuinely wanted one had no next command to type. One line, on stdout rather than stderr,
    because the harnesses that most need it redirect stdout to a file they poll.
    """
    print(
        f"AUTOMATIC DESTINATION DISCOVERY SKIPPED under --assistant auto ({reason}). The saved "
        "intake file named in this output is yours to continue from, in the assistant you already "
        "have open. To start a detached planner on purpose instead, rerun with --assistant codex "
        "or --assistant claude, or export TRAVEL_BUDDY_ASSISTANT=codex.",
        flush=True,
    )


def resolve_assistant(requested: str, *, announce: bool = True) -> str:
    """Decide whether to spawn a continuation assistant, and which one.

    This used to read CLAUDECODE and answer "claude" -- using the proof that an assistant was
    already handling this trip as the reason to launch a second, competing one. In the measured
    run the orphan produced a whole plan from a stale reading of the intake: wrong origin city,
    a superseded budget cap, no allergy data at all, and a Brauhaus dinner for a traveller with a
    severe dairy allergy, saved with verification_status "verified". The two assistants never saw
    each other's work, so nothing flagged the contradiction.

    So the default under "auto" is now to stand down, and spawning is what has to be earned: an
    explicit request, or positive evidence of an interactive terminal. An explicit --assistant or
    TRAVEL_BUDDY_ASSISTANT still wins, because a caller who names an assistant has decided on
    purpose.

    The "or positive evidence of an interactive terminal" half of that sentence is superseded; it
    is kept because it records what the second fix believed, and the belief is the thing that has
    to stay visible. opencode, Cursor and Cline set none of ASSISTANT_ALREADY_DRIVING and allocate
    a full pty, so the tty test saw a human; `codex` was on PATH; `auto` resolved to "codex" and
    spawned the competing planner anyway -- on precisely the harnesses this skill's owner runs it
    on. No third signal repairs that. The docstring above already argues that enumerating
    assistant names goes stale the day after it is written, and enumerating pty-allocating
    harnesses would go stale the same way, so answering the question at all is the mistake.

    So `auto` now NEVER spawns. Spawning became opt-in and nothing else: `--assistant codex`,
    `--assistant claude`, or TRAVEL_BUDDY_ASSISTANT=codex|claude. That has a real cost -- the
    traveller who submitted the form in a genuinely bare terminal now types one more command,
    and announce_stand_down() exists so they are told which one. It is the cheap side of the
    trade. What it buys is the end of the failure recorded above: a second unattended planner
    reading a stale intake and writing a Brauhaus dinner for a traveller with a severe dairy
    allergy into a plan stamped `verification_status: verified`. One extra command against a
    medical risk saved as verified is not a close call.

    Every earlier stand-down branch is kept below rather than collapsed into a single
    `return "none"`. They no longer change the answer, only the reason reported with it, and the
    reason is the whole remaining message: "an assistant is already driving this workspace",
    "nothing here is a terminal" and "auto never spawns" send a caller to three different next
    steps. Collapsing them would save four lines and delete the only thing this function still
    tells anyone.
    """
    if requested != "auto":
        return requested
    configured = os.environ.get("TRAVEL_BUDDY_ASSISTANT", "").strip().casefold()
    if configured in ASSISTANTS - {"auto"}:
        return configured
    if any(os.environ.get(name) for name in ASSISTANT_ALREADY_DRIVING):
        driving = ", ".join(name for name in ASSISTANT_ALREADY_DRIVING if os.environ.get(name))
        reason = f"an assistant is already driving this workspace: {driving} is set"
    elif not interactive_terminal():
        reason = "stdin and stdout are not both a terminal, so something is already driving this run"
    elif not (shutil.which("codex") or shutil.which("claude")):
        reason = "neither the codex nor the claude CLI is on PATH, so there is nothing to start"
    else:
        # The branch the pty harnesses land in: a terminal is attached, both CLIs may well be
        # installed, and the answer is still no. Naming that explicitly matters -- a caller who
        # sees "auto never spawns" knows the missing child was a decision, not a broken PATH.
        reason = ("`auto` never spawns a second planner: a terminal is not evidence that nobody "
                  "is already planning this trip")
    if announce:
        announce_stand_down(reason)
    return "none"


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def delivery_requirement(workspace: Path, intake: Path) -> str:
    """State the non-negotiable handoff based on the saved destination state."""
    try:
        value = json.loads(intake.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        value = {}
    scope = value.get("destination_scope") if isinstance(value, dict) else {}
    state = scope.get("state") if isinstance(scope, dict) else None
    named = [place for place in (scope.get("named_places") or []) if str(place).strip()] if isinstance(scope, dict) else []
    # A fixed scope with no named place is not a Construction task: there is nothing to
    # construct.  Only a named destination earns the mandatory final-delivery gate.
    if state == "fixed" and named:
        return f"""This is a Construction task because the destination is fixed. If dates, nights, party, budget basis, ground-transport mode, and (only when cross-border travel is considered) entry feasibility and every traveller's passport validity are decision-ready, you MUST finish with a verified persistent final delivery: build the complete final-trip-plan JSON, run `python scripts/save_trip_deliverables.py <plan.json> --workspace \"{workspace}\"`, and report both the exact `Plan JSON:` and `Final HTML:` paths. The HTML must contain a timed, geographically coherent itinerary, two-to-three comparable hotels in each stay group unless one has a researched reason, concrete flight legs and normally two candidates when flying, specific meal cards, destination-experience anchors, booking/ticket/rental links where relevant, a transparent per-person cost breakdown, source register, and caveats. Every price needs a basis, status, and check time. A round-trip flight button must prefill origin, destination, both dates, and travellers; a hotel comparison button must prefill destination, dates, guests, and rooms. Every route segment must name one primary mode plus service/instructions, walking/transfers, fare basis and fallback; its map button must be an actual directions URL, never a POI page. Label any start/end-only link as a route overview, never a full-day route, and make the segment buttons the navigation source of truth. For mainland China, use a researched Amap `uri.amap.com/navigation` link with `from`, `to`, and `mode`. Treat a final departure day as checkout/no overnight stay rather than an extra hotel night. Run every required validation; do not claim completion or call the itinerary final unless that HTML exists and validates. If an essential item is missing, ask only the smallest blocking question and explicitly state that final HTML delivery is pending."""
    if state == "fixed" and not named:
        return """The saved intake marks the destination as fixed but names no place. Treat this as blocked, not as a Construction task: ask only which destination was meant, and do not invent one or produce a final HTML."""
    return """This is an intermediate Discovery task because the destination has not been fixed. Produce a source-backed shortlist and the one smallest decision needed to select a destination. Do not call the trip complete and do not fabricate a booking-ready final HTML from an unconfirmed destination or dates. Once the traveller selects a destination and the essential fields are confirmed, the Construction task has a mandatory final HTML delivery gate."""


def traveller_language(intake: Path) -> str | None:
    """The language the saved intake says the traveller reads, or None when it records none."""
    try:
        value = json.loads(intake.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict):
        return None
    return (normalize_language(value.get("preferred_output_language"))
            or normalize_language(value.get("form_language")))


def discovery_prompt(workspace: Path, intake: Path, profile: Path | None,
                     project_root: Path = Path(__file__).resolve().parents[1]) -> str:
    """What the detached planner is told.

    The skill is named by the SKILL.md that belongs to the scripts it will run: "use the
    travel-buddy skill" alone let a child on a machine with two installs -- codex read one 112
    commits old -- follow one version's instructions while running another's scripts. And the
    traveller's language is stated, because the form they filled in is the only place it was said.
    """
    profile_text = str(profile) if profile else "No reusable profile is attached."
    language = traveller_language(intake)
    language_line = (
        f"\n\nWrite to the traveller in {LANGUAGE_NAMES[language]} -- the language this intake "
        f"records -- including your answer in this terminal; `new_plan_skeleton.py --from-intake` "
        f"carries the same language into the plan." if language else "")
    return f"""Continue this Travel Buddy request now. Use the travel-buddy skill in {project_root}: read {project_root / "SKILL.md"} before anything else and run its scripts from {project_root / "scripts"} -- another installed copy of travel-buddy may be a different version. Then read the saved current-trip intake at:
{intake}

Reusable profile (if any):
{profile_text}{language_line}

Start destination discovery immediately. The intake carries fields that are hard rules, not colour: `feasibility.dietary_or_religious_needs` constrains every meal recommendation, `destination_scope.excluded_places` is a hard filter, `travel_window.fixed_commitments` cannot be violated, `trip_purpose` shapes what a good day looks like, and `travel_window.start_date`/`end_date`, when present, are the confirmed dates rather than an approximation. Do not ask the traveller to repeat information already in those files and do not ask them to type \"continue\". Respect excluded places, regional service access, and all privacy rules. Read `trip_geography.scope`: for `domestic`, stay within the traveller’s domestic market and do not ask for or infer entry requirements; for `cross_border` or `domestic_or_cross_border`, apply the saved per-traveller entry constraints. Treat high-speed rail, conventional/night rail, intercity bus, ferry, flights, and self-drive as distinct transport modes; do not silently reduce rail/bus preferences to a flight-only search. The saved budget range uses `calculation_basis: per_person`: preserve that basis in comparisons and final HTML, and label any party total as a separate derived calculation. Use current, source-labeled research for volatile claims. Do not make purchases, log in, submit forms, or request credentials/payment/document data.

Resolve all choices in this order: (1) an explicit value in this current-trip intake, including selected trip geography and transport modes; (2) a compatible stable default from the reusable profile only where the current-trip field is empty or unspecified; (3) destination-market feasibility from current research. Never infer domestic versus cross-border scope from nationality, residence, language, or currency: the current `trip_geography.scope` is authoritative. If that selected scope conflicts with a named destination, explain the conflict and ask the smallest clarification instead of silently changing scope. Use profile exclusions as hard filters and visited/revisit settings as diversity rules, but let any current-trip override win. Use the selected transport modes to decide which comparisons and booking branches to research; apply a saved self-drive/cabin preference only as a tie-breaker when it does not conflict with this trip’s explicit choice. Select maps, booking platforms, and local operators by the actual destination/route market plus the traveller’s declared normal service access, not merely by the profile’s usual app.

{delivery_requirement(workspace, intake)}

Present the result in this terminal when ready."""


def command_for(
    assistant: str, project_root: Path, workspace: Path, intake: Path, profile: Path | None, result_path: Path
) -> tuple[list[str], str | None]:
    """Return the child command plus any prompt that must be fed on stdin.

    The second element is None when the prompt travels as an argument.
    """
    prompt = discovery_prompt(workspace, intake, profile, project_root=project_root)
    if assistant == "codex":
        executable = shutil.which("codex")
        if not executable:
            raise FileNotFoundError("Codex CLI was not found on PATH.")
        return [
            executable,
            "exec",
            "-C",
            str(project_root),
            "--add-dir",
            str(workspace),
            "--output-last-message",
            str(result_path),
            prompt,
        ], None
    if assistant == "claude":
        executable = shutil.which("claude")
        if not executable:
            raise FileNotFoundError("Claude Code CLI was not found on PATH.")
        # `--add-dir` is variadic (`--add-dir <directories...>`), so a prompt appended after
        # the workspace was parsed as a second directory and the CLI exited with "Input must
        # be provided either through stdin or as a prompt argument when using --print",
        # killing every automatic hand-off. Feeding the prompt on stdin removes the argv
        # ambiguity entirely and keeps a multi-kilobyte prompt clear of argument-length limits.
        return [executable, "-p", "--add-dir", str(workspace)], prompt
    raise ValueError(f"Unsupported assistant: {assistant}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Automatically continue a saved Travel Buddy intake with Codex or Claude.")
    parser.add_argument("--assistant", choices=sorted(ASSISTANTS), default="auto")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--intake", required=True)
    parser.add_argument("--profile", default=None)
    parser.add_argument("--project-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--result-path", required=True)
    parser.add_argument("--log-path", required=True)
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve(strict=True)
    intake = Path(args.intake).expanduser().resolve(strict=True)
    profile = Path(args.profile).expanduser().resolve(strict=True) if args.profile else None
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    result_path = Path(args.result_path).expanduser().resolve()
    log_path = Path(args.log_path).expanduser().resolve()
    if not inside(intake, workspace) or (profile and not inside(profile, workspace)):
        raise ValueError("The saved intake and profile must be inside the selected Travel Buddy workspace.")
    if not inside(result_path, workspace / "plans") or not inside(log_path, workspace / "plans"):
        raise ValueError("Automatic-discovery results must stay inside the workspace plans folder.")

    # announce=False because the branch below says the same thing with the concrete intake path
    # filled in, which is strictly more useful. Two near-identical paragraphs in a row is how a
    # reader learns to skim both, and the one worth reading is the one carrying the path.
    assistant = resolve_assistant(args.assistant, announce=False)
    if assistant == "none":
        print("AUTOMATIC DESTINATION DISCOVERY SKIPPED: no continuation assistant was started.", flush=True)
        print(
            f"The saved intake is at {intake}. If an assistant is already open in this workspace, "
            "hand it that path and continue there. `--assistant auto` starts nothing by itself, "
            "not even from a bare terminal: to start a detached planner on purpose, rerun with "
            "--assistant codex or --assistant claude, or export TRAVEL_BUDDY_ASSISTANT=codex.",
            flush=True,
        )
        return 0
    command, stdin_text = command_for(assistant, project_root, workspace, intake, profile, result_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"AUTOMATIC DESTINATION DISCOVERY STARTED WITH {assistant.upper()}.", flush=True)
    print(f"RESULT PATH: {result_path}", flush=True)
    print(f"RUN LOG: {log_path}", flush=True)
    with log_path.open("x", encoding="utf-8") as log:
        log.write(f"Started: {datetime.now().astimezone().isoformat()}\nAssistant: {assistant}\n\n")
        result = result_path.open("x", encoding="utf-8") if assistant == "claude" else None
        try:
            process = subprocess.Popen(
                command,
                cwd=project_root,
                stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if stdin_text is not None:
                # The prompt is a few kilobytes, comfortably inside the pipe buffer, so writing
                # and closing before draining stdout cannot deadlock. Closing is what signals
                # end-of-input to the CLI.
                assert process.stdin is not None
                process.stdin.write(stdin_text)
                process.stdin.close()
            assert process.stdout is not None
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log.write(line)
                log.flush()
                if result:
                    result.write(line)
                    result.flush()
            return_code = process.wait()
            log.write(f"\nFinished: {datetime.now().astimezone().isoformat()}\nExit code: {return_code}\n")
            # Mark the RESULT file too, not only the log. The exit code used to land exclusively
            # in the .log, so a run that died left a .md in plans/ that read like a deliverable.
            # Measured in a real workspace: of three saved discovery results, two were failures --
            # one a CLI usage error, one "API Error: Connection closed mid-response" -- and
            # neither file said so anywhere. A later reader, human or assistant, finds an error
            # message formatted exactly like a finished answer.
            if result and return_code:
                result.write(
                    f"\n\n---\n\n**RUN FAILED — exit code {return_code}.** "
                    f"Everything above is partial output from a discovery run that did not "
                    f"finish, not a result. Do not plan from it. Full log: {log_path}\n")
                result.flush()
        finally:
            if result:
                result.close()
    if return_code:
        print(f"AUTOMATIC DESTINATION DISCOVERY FAILED (exit {return_code}). See {log_path}", file=sys.stderr, flush=True)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
