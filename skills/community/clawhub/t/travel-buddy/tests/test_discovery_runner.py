#!/usr/bin/env python3
"""Regression tests for scripts/run_destination_discovery.py.

The runner streams a child assistant's output into a .md result file inside the workspace. Until
now the exit code landed only in the sibling .log, so a run that died left a result file that read
exactly like a finished answer. Measured in a real workspace: of three saved discovery results two
were failures -- one a CLI usage error ("Input must be provided either through stdin..."), one
"API Error: Connection closed mid-response" -- and neither file said so anywhere in its own text.

That is the same shape as every other defect this skill has fixed: the artifact of a failure is
indistinguishable from the artifact of a success, so nothing makes a noise.
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "run_destination_discovery", ROOT / "scripts" / "run_destination_discovery.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeProcess:
    """A child that prints some output and then exits with the given code."""

    def __init__(self, lines: list[str], return_code: int):
        self.stdout = iter(lines)
        # The claude branch writes the prompt to stdin and closes it, so this has to be a real
        # writable object rather than None.
        self.stdin = io.StringIO()
        self._return_code = return_code

    def wait(self) -> int:
        return self._return_code


class FakeStream:
    """A stream that reports whatever tty-ness the case is about, and keeps what was written.

    write()/flush() are real rather than stubs because resolve_assistant() now prints its
    stand-down notice through sys.stdout, which this class is standing in for. A FakeStream with
    only isatty() turned the first stand-down into an AttributeError inside the test helper --
    which is the harmless version of the same mistake the announcement exists to prevent: a
    stand-down nobody can see.
    """

    def __init__(self, tty: bool):
        self._tty = tty
        self.written: list[str] = []

    def isatty(self) -> bool:
        return self._tty

    def write(self, text: str) -> int:
        self.written.append(text)
        return len(text)

    def flush(self) -> None:
        return None


def resolve_and_capture(module, *, requested: str = "auto", env: dict[str, str] | None = None,
                        tty: bool = False, on_path: tuple[str, ...] = ("codex", "claude"),
                        ) -> tuple[str, str]:
    """Call resolve_assistant() with the environment, tty-ness and PATH of one scenario."""
    original_env = dict(os.environ)
    original_which = module.shutil.which
    original_stdin, original_stdout = sys.stdin, sys.stdout
    stdout = FakeStream(tty)
    try:
        for name in ("CLAUDECODE", "CLAUDE_CODE", "CODEX_THREAD_ID", "TRAVEL_BUDDY_ASSISTANT"):
            os.environ.pop(name, None)
        os.environ.update(env or {})
        module.shutil.which = lambda name: f"/usr/bin/{name}" if name in on_path else None
        sys.stdin, sys.stdout = FakeStream(tty), stdout
        return module.resolve_assistant(requested), "".join(stdout.written)
    finally:
        os.environ.clear()
        os.environ.update(original_env)
        module.shutil.which = original_which
        sys.stdin, sys.stdout = original_stdin, original_stdout


def resolved(module, **kwargs) -> str:
    return resolve_and_capture(module, **kwargs)[0]


def check_resolve_assistant(module, check) -> None:
    """Who is allowed to spawn a second planner, and who is not.

    The regression this guards: the old version recognised an already-driving assistant by name
    (CLAUDECODE, CLAUDE_CODE, CODEX_THREAD_ID) and treated every other harness as a bare terminal.
    Under Gemini CLI, Cursor, Copilot CLI, opencode or an SDK agent -- none of which set those --
    `--assistant auto` therefore resolved to "codex" and spawned a detached second planner behind
    an assistant that was already planning the same trip. That is the exact shape of the incident
    the module's own docstring records: two plans in one workspace, the unattended one built from
    the un-clarified intake and saved as verified.

    The second regression, which the first fix left open and this file used to assert as correct
    behaviour: the replacement test was "is stdin and stdout a tty", and opencode, Cursor and
    Cline allocate a full pty while setting none of the three env markers. On the owner's machine
    `codex` is on PATH, so `auto` resolved to "codex" on every one of those harnesses and spawned
    the competing planner exactly as before. There is no third signal to reach for -- so the rule
    is now flat: under `auto` nothing is ever spawned, and spawning is opt-in via --assistant or
    TRAVEL_BUDDY_ASSISTANT. Which means the cases below split in two: everything that reaches the
    `auto` default must be "none", and both opt-ins must still work, because they are now the
    only way a continuation can ever start.
    """
    check("an unknown harness does not get a spawn (the regression)",
          resolved(module, env={"SOME_OTHER_AGENT": "1"}) == "none",
          "a harness this module has never heard of must stand down, not fall through to codex")
    check("no markers and no terminal is still not a bare terminal",
          resolved(module) == "none",
          "a piped, redirected or CI run has something driving it already")
    check("Claude Code stands down", resolved(module, env={"CLAUDECODE": "1"}) == "none")
    check("Codex stands down", resolved(module, env={"CODEX_THREAD_ID": "abc"}) == "none")
    check("an env marker beats a pty",
          resolved(module, env={"CLAUDECODE": "1"}, tty=True) == "none",
          "a harness that allocates a terminal must still lose to proof it is already driving")

    # The pty case, which is the defect this whole block was rewritten for. opencode, Cursor and
    # Cline set none of the env markers and allocate a full pty, and `codex` is on the owner's
    # PATH -- so the previous expectation on this exact input, "a bare terminal still gets its
    # continuation == codex", was the bug written down as a passing test. A tty says a terminal
    # device is attached; it cannot say a human opened it with nothing already listening. So
    # `auto` never spawns now, and the cost -- a real human in a real bare terminal types one
    # more command -- is paid by announce_stand_down() telling them which one.
    check("a pty harness gets no spawn, however much it looks like a terminal (the P0-6 regression)",
          resolved(module, tty=True) == "none",
          "opencode/Cursor/Cline allocate a pty and set no markers; auto must not resolve to codex")
    check("a terminal with only claude installed still gets no spawn",
          resolved(module, tty=True, on_path=("claude",)) == "none")
    check("a terminal with neither CLI installed says so rather than guessing",
          resolved(module, tty=True, on_path=()) == "none")

    # A stand-down that prints nothing reads as "handled" to the model that called it, and that
    # is how a traveller ends up with neither planner: no discovery child, and an assistant that
    # believes one is running. The notice has to carry both halves -- whose job it is now, and
    # the command that would have spawned one on purpose.
    _, spoken = resolve_and_capture(module, tty=True)
    check("the stand-down is announced rather than silent",
          "SKIPPED" in spoken, repr(spoken))
    check("the announcement names the opt-in that does spawn",
          "--assistant codex" in spoken and "TRAVEL_BUDDY_ASSISTANT=codex" in spoken, repr(spoken))
    check("the announcement says the intake is the caller's to continue",
          "yours to continue" in spoken, repr(spoken))
    check("the announcement gives the reason, so a bare terminal is not left guessing at a bug",
          "never spawns" in spoken, repr(spoken))
    _, driving_reason = resolve_and_capture(module, env={"CLAUDECODE": "1"})
    check("an already-driving harness is told which marker stood it down",
          "CLAUDECODE" in driving_reason, repr(driving_reason))
    _, explicit = resolve_and_capture(module, requested="codex")
    check("an explicit request prints no stand-down notice",
          explicit == "", repr(explicit))

    check("an explicit --assistant wins over every heuristic",
          resolved(module, requested="codex", env={"CLAUDECODE": "1"}) == "codex",
          "a caller who names an assistant has decided on purpose")
    check("an explicit --assistant codex still spawns codex, from any harness",
          resolved(module, requested="codex", tty=True) == "codex"
          and resolved(module, requested="codex", env={"SOME_OTHER_AGENT": "1"}) == "codex",
          "opt-in is the only way to spawn now, so it has to actually work")
    check("an explicit --assistant claude still spawns claude",
          resolved(module, requested="claude") == "claude")
    check("TRAVEL_BUDDY_ASSISTANT is the other opt-in and still spawns",
          resolved(module, env={"TRAVEL_BUDDY_ASSISTANT": "claude"}) == "claude")
    check("TRAVEL_BUDDY_ASSISTANT=codex spawns codex from a pty harness",
          resolved(module, env={"TRAVEL_BUDDY_ASSISTANT": "codex"}, tty=True) == "codex")
    check("TRAVEL_BUDDY_ASSISTANT=none is still honoured as an explicit choice",
          resolved(module, env={"TRAVEL_BUDDY_ASSISTANT": "none"}, tty=True) == "none")
    check("an unrecognised TRAVEL_BUDDY_ASSISTANT value is ignored, not obeyed",
          resolved(module, env={"TRAVEL_BUDDY_ASSISTANT": "gemini"}, tty=True) == "none",
          "an unknown name must fall back to the auto default, never be passed through as a command")
    check("an empty TRAVEL_BUDDY_ASSISTANT is not a request for anything",
          resolved(module, env={"TRAVEL_BUDDY_ASSISTANT": "  "}, tty=True) == "none")
    check("the opt-in is case- and whitespace-insensitive, as an exported value usually is",
          resolved(module, env={"TRAVEL_BUDDY_ASSISTANT": " Codex "}, tty=True) == "codex")


def run_with_exit(module, workspace: Path, return_code: int, lines: list[str]) -> str:
    """Drive main() with a stubbed child process; return the result file's text."""
    plans = workspace / "plans"
    plans.mkdir(parents=True, exist_ok=True)
    intake = plans / "intake-test.json"
    intake.write_text(json.dumps({"mode": "discovery"}), encoding="utf-8")
    result_path = plans / f"result-{return_code}.md"
    log_path = plans / f"log-{return_code}.log"

    original_popen = module.subprocess.Popen
    original_which = module.shutil.which
    original_argv = sys.argv
    try:
        module.subprocess.Popen = lambda *a, **k: FakeProcess(lines, return_code)
        # command_for() resolves the assistant on PATH before anything is spawned, so stubbing
        # Popen alone is not enough. Without this the test passes only on a machine that happens
        # to have the Claude CLI installed -- which is why it went green locally and red on CI,
        # on CI's first real run. A test whose result depends on the developer's PATH is measuring
        # the developer.
        module.shutil.which = lambda name: f"/usr/bin/{name}"
        sys.argv = [
            "run_destination_discovery.py",
            "--assistant", "claude",
            "--workspace", str(workspace),
            "--intake", str(intake),
            "--result-path", str(result_path),
            "--log-path", str(log_path),
        ]
        module.main()
    finally:
        module.subprocess.Popen = original_popen
        module.shutil.which = original_which
        sys.argv = original_argv
    return result_path.read_text(encoding="utf-8")


def main() -> int:
    module = load_runner()
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{name}\n{detail}")

    check_resolve_assistant(module, check)

    partial = ["All research is in. Building the plan JSON now.\n",
               "API Error: Connection closed mid-response.\n"]

    with tempfile.TemporaryDirectory() as tmp:
        text = run_with_exit(module, Path(tmp), 1, partial)
        check("a failed run marks its own result file",
              "RUN FAILED" in text, text[-300:])
        check("the failure marker names the exit code",
              "exit code 1" in text, text[-300:])
        check("the failure marker says not to plan from it",
              "Do not plan from it" in text, text[-300:])
        check("the partial output is kept rather than discarded",
              "All research is in" in text,
              "the child's output was dropped; a partial answer is still evidence of what ran")

    # And the marker must not appear on a run that succeeded, or it becomes noise everyone learns
    # to ignore -- the same way a check that false-positives gets routed around.
    with tempfile.TemporaryDirectory() as tmp:
        text = run_with_exit(module, Path(tmp), 0, ["Shortlist ready. Three candidates.\n"])
        check("a successful run carries no failure marker",
              "RUN FAILED" not in text, text[-300:])
        check("a successful run keeps its output",
              "Shortlist ready" in text, text)

    # What a detached planner is told. Checked 2026-09-24 for assistants other than the one that
    # launched it: the prompt said "use the travel-buddy skill" and nothing more, so on a machine
    # with two installs -- this one had codex reading a clone 112 commits old -- the child read one
    # version's SKILL.md and ran another's scripts; and it never said which language the traveller
    # chose, so a planner started from an English form answered in whatever language it liked.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        intake = root / "intake.json"
        for stored, line in (
                ({"preferred_output_language": "en", "form_language": "en"}, "in English"),
                ({"preferred_output_language": "zh", "form_language": "en"}, "in Chinese"),
                ({"form_language": "en"}, "in English")):
            intake.write_text(json.dumps({"destination_scope": {"state": "open"}, **stored}),
                              encoding="utf-8")
            prompt = module.discovery_prompt(root, intake, None, project_root=ROOT)
            check(f"the prompt names the traveller's language for {stored}",
                  f"Write to the traveller {line}" in prompt, prompt[:600])
        intake.write_text(json.dumps({"destination_scope": {"state": "open"}}), encoding="utf-8")
        prompt = module.discovery_prompt(root, intake, None, project_root=ROOT)
        check("an intake that records no language names none",
              "Write to the traveller in" not in prompt, prompt[:600])
        check("the prompt pins the SKILL.md that belongs to these scripts",
              str(ROOT / "SKILL.md") in prompt, prompt[:600])
        original_which = module.shutil.which
        try:
            module.shutil.which = lambda name: f"/usr/bin/{name}"
            argv, _ = module.command_for("codex", ROOT, root, intake, None, root / "result.md")
            _, stdin = module.command_for("claude", ROOT, root, intake, None, root / "result.md")
        finally:
            module.shutil.which = original_which
        check("codex and claude children both get the pinned skill",
              str(ROOT / "SKILL.md") in argv[-1] and str(ROOT / "SKILL.md") in (stdin or ""),
              argv[-1][:300])

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all discovery-runner regression cases passed")
    return 0


def test_discovery_runner() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
