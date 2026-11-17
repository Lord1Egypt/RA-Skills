#!/usr/bin/env python3
"""
claude_check.py - the mechanical layer of the rabbit-claude-md skill.

Audits CLAUDE.md and AGENTS.md files: the memory files agent harnesses (Claude
Code, Codex, etc.) load at the start of every session. A root memory file is a
quick "where am I" plus rules, and the failure modes this script can measure are
the ones where it stops being that: the file grows past what a session should
carry, in lines or in raw characters, directly or through an `@import`,
bullets run long, emphasis is spent on every other line, fenced commands or slash commands point at nothing, an
`@path` import never resolves, the same fact lives in two files at once, open
work or a roadmap sits beside standing rules, and a re-check instruction asks
for verification the model already performs. Unless told otherwise it also
runs the active voice's rules over the prose, through the rabbit-writes engine
at register `docs`.

Everything here is something a regex or a counter can decide. Whether a line
is derivable from the code, whether it sits at the wrong altitude, whether it
survives the removal test ("would deleting this cause Claude or Codex to make
mistakes?"), and where a changelog-drift or TODO line should move are judgment
calls and stay in SKILL.md. The `claudemd-changelog-drift`, `claudemd-todo-marker`,
and `claudemd-session-state` findings are evidence for that judgment, never
the verdict.

For the root memory file only (the top-level CLAUDE.md or AGENTS.md, not a
nested module's or a local override), three extra facts are reported as
notes rather than findings, because none of them is a defect on their own:
which top-level directories the file never names, what harness config
(`.claude/settings.json`, `.mcp.json`, `.claude/commands/`, `.claude/agents/`)
exists in the tree, and how long ago the file last changed relative to the
repository's own activity.

There is no CLAUDE.md / AGENTS.md corpus to calibrate against, so every number
in LIMITS is pinned by the fixture tests beside this script rather than
measured the way the README thresholds were. Move a limit and the tests move
with it.

Usage:
    python3 claude_check.py CLAUDE.md
    python3 claude_check.py AGENTS.md
    python3 claude_check.py .                    # sweep a tree
    python3 claude_check.py CLAUDE.md --json
    python3 claude_check.py CLAUDE.md --check    # exit 1 on any P0
    python3 claude_check.py CLAUDE.md --no-voice

Discovery covers CLAUDE.md, CLAUDE.local.md, .claude.md, .claude.local.md,
AGENTS.md, AGENTS.override.md, .agents.md, and .agents.override.md. When
sweeping a directory, both families are audited together: a repository
running two harnesses often carries real content in both, and a same-directory
CLAUDE.md/AGENTS.md pair that is not a symlink but shares most of its content
raises `claudemd-dual-harness`, evidence that one real file should serve both
names. ~/.claude/CLAUDE.md and ~/.codex/AGENTS.md are never discovered
implicitly: pass one as the file argument to read it, or pass --global to
fold both into the duplicate check, read-only.

Exit codes: 0, or 1 with --check when a live P0 is present, or 2 when the
input cannot be read or --voice-rules names a profile that cannot be read.
A voice that cannot be *resolved* is a note and still exits 0. No claudemd-*
finding is ever P0: blocking stays reserved for the engine's safety band.
Stdlib only, 3.9+.
"""

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

from _bootstrap import SCAN_PATH, cli_error  # noqa: F401

from rwlib import findings as findings_mod   # noqa: E402
from rwlib import suppress                   # noqa: E402
from rwlib import voices as voices_mod       # noqa: E402
from rwlib.markdown import (FENCE_PARTS_RX, FENCE_RX, INLINE_CODE_RX,  # noqa: E402
                            LIST_ITEM_RX, blank, line_of, word_count)

VOICES_DIR = voices_mod.VOICES_DIR

# The four spellings Claude Code reads. CLAUDE.local.md is the documented
# local-override name and .claude.md/.claude.local.md are the older ones the
# claude-md-management plugin still discovers, so a sweep covers all four.
CLAUDE_NAMES = ("CLAUDE.md", "CLAUDE.local.md", ".claude.md", ".claude.local.md")

# AGENTS.md standard spellings (OpenAI Codex / multi-agent harness conventions).
AGENT_NAMES = ("AGENTS.md", "AGENTS.override.md", ".agents.md", ".agents.override.md")

ALL_MEMORY_NAMES = CLAUDE_NAMES + AGENT_NAMES

PRUNE_DIRS = {".git", "node_modules", "dist", "build", "scratch",
              "__pycache__", ".venv", "venv", "target"}

# One home for every threshold. SKILL.md points here rather than restating
# numbers, and tests/test_thresholds.py builds its boundary fixtures from
# these constants so a moved limit moves the tests with it.
LIMITS = {
    "bullet_words": 40,        # words in one list item before claudemd-bullet-length
    "emphasis_lines_abs": 8,   # emphasized lines allowed outright...
    "emphasis_lines_pct": 0.10,  # ...or this share of prose lines, whichever is larger
    "size_lines_p2": 300,      # non-blank lines before claudemd-oversize notes it
    "size_lines_p1": 600,      # ...and before it becomes a P1
    "char_budget_p2": 32000,   # 80% of the character budget: a nudge before the hard line
    "char_budget_p1": 40000,   # the character count commonly recommended as a memory file's ceiling
    "duplicate_min_chars": 40,  # normalized line length before it can count as a duplicate
}

# Shouting, not formatting. A bold lead-in on a definition bullet is layout,
# and an ALL-CAPS clause would count every JSON and YAML in a technical doc,
# so the budget counts only the marker words that mean "obey this line".
EMPHASIS_RX = re.compile(r"\b(?:IMPORTANT|CRITICAL|NEVER|ALWAYS|WARNING|"
                         r"MUST(?: NOT)?|DO NOT)\b")

# Evidence of a session log rather than a standing fact. Case-insensitive on
# purpose: "We fixed" and "we fixed" are the same tell.
DRIFT_RX = re.compile(r"(?i)\b(?:we (?:fixed|added|removed|renamed)"
                      r"|used to\b|no longer\b|previously\b"
                      r"|has been (?:moved|renamed|refactored)"
                      r"|as of (?:commit|version)"
                      r"|recently (?:added|changed|moved))")
COMMIT_HASH_RX = re.compile(r"\b[0-9a-f]{7,40}\b")
COMMIT_WORD_RX = re.compile(r"(?i)\b(?:commit|fix(?:ed|es)?)\b")

# A token inside a fenced command that reads as a repository path: only path
# characters, at least one slash. Requiring the slash drops bare filenames on
# purpose, because a `cd somewhere && python3 script.py` line makes a bare
# name unresolvable from the root without tracking the cd.
PATHISH_RX = re.compile(r"^(?:\.{1,2}/)?[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+/?$")
FENCE_LANGS = {"bash", "sh", "zsh", "shell", "console", "python", "py"}
# `gh repo clone owner/repo` and `npm install scope/pkg` name remote things
# that are path-shaped and never on disk.
REMOTE_VERBS = {"clone", "install", "pull", "add", "from"}

# An @path memory import. Narrowed to tokens whose last segment carries a dot
# or that start ./, ../, or ~/: a bare `@README` import is legal but the same
# shape as an @mention, and `@scope/package` in prose names an npm package,
# not a file.
IMPORT_RX = re.compile(r"(?:^|(?<=[\s(]))@((?:~/|\.{1,2}/)?"
                       r"[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*)", re.M)

# Claude Code follows @imports at most this many hops deep, so the effective
# size accounting stops where the harness does.
IMPORT_HOP_LIMIT = 5

# Forward-looking session state: work items wearing a rules costume. The
# backward-looking twin is DRIFT_RX. The bare markers are matched shouted,
# the phrases case-insensitively.
TODO_MARK_RX = re.compile(r"\b(?:TODO|FIXME|WIP)\b")
SESSION_STATE_RX = re.compile(
    r"(?i)\b(?:next steps?\b|roadmap\b|planned for\b|in progress\b"
    r"|not (?:yet )?implemented\b|coming soon\b"
    r"|as of (?:january|february|march|april|may|june|july|august"
    r"|september|october|november|december)\b)")

# Re-check instructions current models already perform unprompted. The
# judgment reasoning lives in references/criteria.md; these spellings are
# the greppable subset.
OVER_VERIFY_RX = re.compile(
    r"(?i)\b(?:double[- ]check|triple[- ]check|re-?verify\b"
    r"|verify (?:again|your (?:work|answer|output))|always verify\b"
    r"|be (?:extremely|very) careful"
    r"|make sure to (?:verify|double[- ]check))")

# Global memory files --global folds into the duplicate sweep. Read-only:
# they are never audited or edited, only compared against.
GLOBAL_MEMORY = (os.path.join("~", ".claude", "CLAUDE.md"),
                 os.path.join("~", ".codex", "AGENTS.md"))

MAX_PER_ID = 10


def finding(fid, label, priority, line, detail, match=""):
    """A structure finding, in the schema every other checker here uses."""
    return findings_mod.make(fid, label, "structure", priority, line,
                             match=match, excerpt=detail)


def prose_copy(raw):
    """Fences and code spans blanked, offsets stable."""
    out = FENCE_RX.sub(blank, raw)
    return INLINE_CODE_RX.sub(blank, out)


# ---------------------------------------------------------------------------
# per-file mechanical checks
# ---------------------------------------------------------------------------

def check_size(raw, findings, stats):
    nonblank = len([l for l in raw.splitlines() if l.strip()])
    stats["nonblank_lines"] = nonblank
    if nonblank > LIMITS["size_lines_p1"]:
        findings.append(finding(
            "claudemd-oversize", "%d non-blank lines" % nonblank, "P1", 1,
            "Past %d lines this is a manual, not a map, and it is loaded into "
            "every session whether the session needs it or not. Restructure: "
            "deep context to .claude/docs/, module facts to a CLAUDE.md in "
            "that module." % LIMITS["size_lines_p1"]))
    elif nonblank > LIMITS["size_lines_p2"]:
        findings.append(finding(
            "claudemd-oversize", "%d non-blank lines" % nonblank, "P2", 1,
            "Past %d lines, start asking each line the removal test: would "
            "deleting it cause Claude to make mistakes? A bloated file "
            "buries the rules that matter." % LIMITS["size_lines_p2"]))


def check_char_budget(raw, findings, stats):
    """The character-count ceiling, independent of the line-count bands.

    Line count and character count measure different failures: a file of
    short, terse lines can clear size_lines_p1 while sitting well under the
    character budget, and a file of few but very long lines can do the
    reverse. Both bands run, and either can fire on its own.
    """
    chars = len(raw)
    stats["char_count"] = chars
    if chars > LIMITS["char_budget_p1"]:
        findings.append(finding(
            "claudemd-char-budget", "%d characters" % chars, "P1", 1,
            "Past %d characters this is over the size commonly recommended "
            "as a memory file's ceiling. Break it down rather than trim it: "
            "deep context to .claude/docs/, module facts to a CLAUDE.md in "
            "that module, an occasional workflow to a command or skill."
            % LIMITS["char_budget_p1"]))
    elif chars > LIMITS["char_budget_p2"]:
        findings.append(finding(
            "claudemd-char-budget", "%d characters" % chars, "P2", 1,
            "Approaching the %d-character budget commonly recommended for "
            "a memory file. Start splitting now instead of waiting for the "
            "hard line." % LIMITS["char_budget_p1"]))


def check_bullets(raw, findings, stats):
    scored = FENCE_RX.sub(blank, raw)
    lines = scored.splitlines()
    items = 0
    i = 0
    while i < len(lines):
        if LIST_ITEM_RX.match(lines[i]):
            items += 1
            body = [lines[i]]
            j = i + 1
            # Continuation lines: indented, non-blank, not a new item.
            while (j < len(lines) and lines[j].strip()
                   and not LIST_ITEM_RX.match(lines[j])
                   and lines[j][:1] in (" ", "\t")):
                body.append(lines[j])
                j += 1
            words = word_count(" ".join(body))
            if words > LIMITS["bullet_words"]:
                findings.append(finding(
                    "claudemd-bullet-length",
                    "List item of %d words" % words, "P2", i + 1,
                    "The cap in force is %d. A bullet this long is a "
                    "paragraph wearing a dash: split it, cut it, or move the "
                    "depth to .claude/docs/." % LIMITS["bullet_words"]))
            i = j
        else:
            i += 1
    stats["list_items"] = items


def check_emphasis(raw, findings, stats):
    scored = prose_copy(raw)
    lines = scored.splitlines()
    nonblank = len([l for l in lines if l.strip()])
    hits = [i + 1 for i, l in enumerate(lines) if EMPHASIS_RX.search(l)]
    stats["emphasis_lines"] = len(hits)
    allowed = max(LIMITS["emphasis_lines_abs"],
                  int(LIMITS["emphasis_lines_pct"] * nonblank))
    if len(hits) > allowed:
        findings.append(finding(
            "claudemd-emphasis-budget",
            "%d emphasized lines, budget is %d" % (len(hits), allowed),
            "P2", hits[0],
            "When this many lines carry IMPORTANT-class markers, none of "
            "them stands out. Keep emphasis for the one or two rules that "
            "get skipped without it."))


INTRO_MIN_WORDS = 5


def check_intro(raw, findings, stats):
    """A one-line description between the title and the first ## heading.

    The single most valuable line in the file: a fresh session's first
    orientation. Anthropic's own guidance leads with it, and nothing here
    checked for it before this pass caught the omission on this repo's own
    root file at every draft.
    """
    lines = raw.splitlines()
    h1 = next((i for i, l in enumerate(lines) if l.lstrip().startswith("# ")), None)
    stats["has_intro"] = False
    if h1 is None:
        return
    body = []
    for l in lines[h1 + 1:]:
        if l.lstrip().startswith("#"):
            break
        body.append(l)
    text = FENCE_RX.sub(blank, "\n".join(body))
    text = re.sub(r"[`*_]", "", text)
    if word_count(text) >= INTRO_MIN_WORDS:
        stats["has_intro"] = True
        return
    findings.append(finding(
        "claudemd-no-intro", "No one-line description under the title", "P2",
        h1 + 1,
        "A fresh session's first orientation is a sentence saying what this "
        "repository or module is, before the first heading. This file goes "
        "straight from the title into structure with nothing in between."))


def check_forward_state(raw, findings, stats):
    """TODO/roadmap tells: session state wearing a rules costume.

    The backward-looking twin is check_changelog_tells. Both are evidence,
    not verdicts: a TODO worth keeping moves to TODO.md, an issue, or
    CLAUDE.local.md if it is personal, and the judgment pass decides which.
    """
    scored = prose_copy(raw)
    todo_hits = 0
    for m in TODO_MARK_RX.finditer(scored):
        todo_hits += 1
        if todo_hits > MAX_PER_ID:
            continue
        findings.append(finding(
            "claudemd-todo-marker", "%s marker in memory file" % m.group(0),
            "P2", line_of(scored, m.start()),
            "A memory file loads every session regardless of what is "
            "outstanding. Move open work to TODO.md, an issue tracker, or "
            "CLAUDE.local.md if it is personal, and keep this file to "
            "standing rules.", match=m.group(0)))
    stats["todo_markers"] = todo_hits

    state_hits = 0
    for m in SESSION_STATE_RX.finditer(scored):
        state_hits += 1
        if state_hits > MAX_PER_ID:
            continue
        findings.append(finding(
            "claudemd-session-state", "Roadmap or in-progress phrasing", "P2",
            line_of(scored, m.start()),
            "%r describes where the project is heading or standing right "
            "now, not a rule Claude needs every session. Move it to "
            "TODO.md, a roadmap document, or an issue tracker."
            % m.group(0), match=m.group(0)))
    stats["session_state_tells"] = state_hits


def check_over_verification(raw, findings, stats):
    """Re-check instructions current models already run unprompted.

    The reasoning is Anthropic's own Opus 5 prompting guidance: an
    instruction demanding verification the model performs anyway compounds
    with that behavior and adds cost without changing the outcome. The
    judgment call (is this project-specific enough to keep) stays with the
    agent; this is only the greppable spelling.
    """
    scored = prose_copy(raw)
    hits = 0
    for m in OVER_VERIFY_RX.finditer(scored):
        hits += 1
        if hits > MAX_PER_ID:
            continue
        findings.append(finding(
            "claudemd-over-verify", "Re-check instruction", "P2",
            line_of(scored, m.start()),
            "%r asks for a verification pass current models already "
            "perform unprompted. Keep it only if it names a "
            "project-specific check the model would otherwise skip."
            % m.group(0), match=m.group(0)))
    stats["over_verify_tells"] = hits


def _import_targets(raw, file_dir):
    """Resolved absolute paths of every @import in raw that exists on disk."""
    targets = []
    scored = prose_copy(raw)
    for m in IMPORT_RX.finditer(scored):
        token = m.group(1).rstrip(".")
        last = token.rsplit("/", 1)[-1]
        if "." not in last and not token.startswith(("./", "../", "~/")):
            continue
        target = os.path.expanduser(token)
        if not os.path.isabs(target):
            target = os.path.join(file_dir, target)
        if os.path.isfile(target):
            targets.append(target)
    return targets


def effective_size(raw, file_dir, hop=0, visited=None):
    """(own non-blank lines, total including resolved @imports).

    Follows imports up to IMPORT_HOP_LIMIT hops, the bound Claude Code
    itself applies, and a visited set stops a cycle between two files that
    import each other from recursing forever. A session pays for what an
    import pulls in, not just what is on screen in the file it was reading;
    moving content behind an import does not shrink that cost, only hides
    the count from a check that only looks at one file.
    """
    if visited is None:
        visited = set()
    own = len([l for l in raw.splitlines() if l.strip()])
    if hop >= IMPORT_HOP_LIMIT:
        return own, own
    total = own
    for target in _import_targets(raw, file_dir):
        real = os.path.realpath(target)
        if real in visited:
            continue
        visited.add(real)
        try:
            with open(target, encoding="utf-8-sig") as fh:
                child_raw = fh.read()
        except OSError:
            continue
        _, child_total = effective_size(child_raw, os.path.dirname(target),
                                        hop + 1, visited)
        total += child_total
    return own, total


def check_import_cost(raw, file_dir, findings, stats):
    """The loophole check_size alone leaves open.

    A file can pass its own size band by moving everything behind an
    `@import`, which the harness still loads every session. This only fires
    when the file's own size is under the limit but the resolved total
    crosses it, so it never duplicates claudemd-oversize on a file that was
    already over on its own.
    """
    own, total = effective_size(raw, file_dir)
    stats["effective_nonblank_lines"] = total
    if total <= own or own > LIMITS["size_lines_p2"]:
        return
    if total > LIMITS["size_lines_p1"]:
        pri, band = "P1", LIMITS["size_lines_p1"]
    elif total > LIMITS["size_lines_p2"]:
        pri, band = "P2", LIMITS["size_lines_p2"]
    else:
        return
    findings.append(finding(
        "claudemd-import-cost",
        "%d lines on screen, %d effective with @imports resolved"
        % (own, total), pri, 1,
        "A session pays for what @imports pull in, not just what is "
        "written in this file. Effective size crosses the %d-line band "
        "this file's own size stays under; moving content behind an "
        "import does not shrink the session." % band))


def check_fenced_paths(raw, repo_root, file_dir, findings, stats):
    checked, reported = 0, set()
    for m in FENCE_PARTS_RX.finditer(raw):
        if m.group(1).lower() not in FENCE_LANGS:
            continue
        body_start = m.start(2)
        for rel_off, line in enumerate(m.group(2).splitlines()):
            if line.lstrip().startswith("#"):
                continue
            tokens = line.split()
            for k, token in enumerate(tokens):
                token = token.strip("'\"`").rstrip(".,;:)")
                if ("://" in token or "path/to" in token
                        or any(c in token for c in "<>{}$*[]")):
                    continue
                if k:
                    prev = tokens[k - 1].strip("'\"`").lower()
                    # A remote name, or an output the command will create.
                    if (prev in REMOTE_VERBS or prev in {"-o", ">", ">>"}
                            or prev.startswith("--out")):
                        continue
                if token.startswith("~"):
                    continue
                if token.startswith("/"):
                    if not (repo_root and token.startswith(repo_root)):
                        continue
                    candidates = [token]
                elif PATHISH_RX.match(token):
                    candidates = [os.path.join(repo_root, token),
                                  os.path.join(file_dir, token)]
                else:
                    continue
                checked += 1
                if token in reported:
                    continue
                if not any(os.path.exists(c) for c in candidates):
                    reported.add(token)
                    if len(reported) > MAX_PER_ID:
                        continue
                    lineno = line_of(raw, body_start) + rel_off
                    findings.append(finding(
                        "claudemd-dead-path",
                        "Fenced command names a missing path", "P1", lineno,
                        "`%s` resolves from neither the repository root nor "
                        "this file's directory. A command that fails on "
                        "paste is worse than no command: the reader stops "
                        "trusting the rest of the file." % token,
                        match=token))
    stats["fenced_paths_checked"] = checked


def check_imports(raw, file_dir, findings, stats):
    scored = prose_copy(raw)
    found, missing = 0, 0
    for m in IMPORT_RX.finditer(scored):
        # A sentence-final dot belongs to the sentence, not the path.
        token = m.group(1).rstrip(".")
        last = token.rsplit("/", 1)[-1]
        if "." not in last and not token.startswith(("./", "../", "~/")):
            continue
        found += 1
        target = os.path.expanduser(token)
        if not os.path.isabs(target):
            target = os.path.join(file_dir, target)
        if not os.path.exists(target):
            missing += 1
            findings.append(finding(
                "claudemd-import-unresolved",
                "@%s does not resolve" % token, "P1",
                line_of(scored, m.start()),
                "An @import that points at nothing loads nothing, silently. "
                "Fix the path or drop the import.", match="@" + token))
    stats["imports"] = found
    stats["imports_missing"] = missing


def check_changelog_tells(raw, findings, stats):
    scored = prose_copy(raw)
    hits = 0
    for m in DRIFT_RX.finditer(scored):
        hits += 1
        if hits > MAX_PER_ID:
            continue
        findings.append(finding(
            "claudemd-changelog-drift", "Session-log phrasing", "P2",
            line_of(scored, m.start()),
            "%r narrates a change instead of stating what is true now. "
            "Evidence, not a verdict: rewrite it as the standing fact, or "
            "delete it if the history is the only content." % m.group(0),
            match=m.group(0)))
    for i, line in enumerate(scored.splitlines(), start=1):
        if COMMIT_WORD_RX.search(line) and COMMIT_HASH_RX.search(line):
            hits += 1
            if hits > MAX_PER_ID:
                continue
            findings.append(finding(
                "claudemd-changelog-drift", "Commit reference in prose", "P2",
                i,
                "A commit hash in a memory file is a log entry. Git already "
                "remembers it: state the standing rule instead.",
                match=COMMIT_HASH_RX.search(line).group(0)))
    stats["changelog_tells"] = hits


def normalize_line(line):
    s = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line.strip())
    return re.sub(r"\s+", " ", s).lower()


def duplicate_index(paths):
    """normalized line -> [(path, lineno)] over every discovered file.

    Deduplicated by realpath: a CLAUDE.md symlinked to AGENTS.md is one file
    with two names, and indexing it twice would report every long line in it
    as living in two files.
    """
    index = {}
    seen_real = set()
    for path in paths:
        real = os.path.realpath(path)
        if real in seen_real:
            continue
        seen_real.add(real)
        try:
            with open(path, encoding="utf-8-sig") as fh:
                text = fh.read()
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            norm = normalize_line(line)
            if len(norm) < LIMITS["duplicate_min_chars"]:
                continue
            index.setdefault(norm, []).append((path, i))
    return index


def display_dup_path(p, repo_root):
    """A path for a duplicate-finding excerpt: ~-shortened, repo-relative,
    or left absolute. A --global comparison path lives outside repo_root,
    where os.path.relpath produces a noisy ../../.. climb or, on Windows
    across drives, raises outright."""
    home = os.path.expanduser("~")
    if p.startswith(home + os.sep):
        return os.path.join("~", os.path.relpath(p, home))
    try:
        return os.path.relpath(p, repo_root)
    except ValueError:
        return p


def check_duplicates(path, raw, index, repo_root, findings):
    if not index:
        return
    seen = set()
    for i, line in enumerate(raw.splitlines(), start=1):
        norm = normalize_line(line)
        if len(norm) < LIMITS["duplicate_min_chars"] or norm in seen:
            continue
        entries = index.get(norm, [])
        others = [(p, ln) for p, ln in entries
                  if os.path.realpath(p) != os.path.realpath(path)]
        if not others:
            continue
        seen.add(norm)
        if len(seen) > MAX_PER_ID:
            continue
        where = ", ".join("%s:%d" % (display_dup_path(p, repo_root), ln)
                          for p, ln in others[:3])
        findings.append(finding(
            "claudemd-duplicate", "Same line in %d files" % (len(others) + 1),
            "P1", i,
            "Also at %s. One home per fact: keep the copy at the right "
            "altitude and link or delete the rest." % where,
            match=line.strip()[:80]))


COMMAND_REF_RX = re.compile(r"`/([a-zA-Z][a-zA-Z0-9_-]*)`")


def check_dead_command_refs(raw, repo_root, findings):
    """A `/slash-command` named in prose with no file behind it.

    Only checked when `.claude/commands/` exists: the convention has to be
    in use here before a missing file means anything. The same failure
    shape as claudemd-dead-path, one level up the harness.
    """
    commands_dir = os.path.join(repo_root, ".claude", "commands")
    if not os.path.isdir(commands_dir):
        return
    seen = set()
    for m in COMMAND_REF_RX.finditer(raw):
        name = m.group(1)
        if name in seen:
            continue
        if os.path.isfile(os.path.join(commands_dir, name + ".md")):
            continue
        seen.add(name)
        if len(seen) > MAX_PER_ID:
            continue
        findings.append(finding(
            "claudemd-dead-command",
            "Slash command `/%s` has no command file" % name, "P1",
            line_of(raw, m.start()),
            "`.claude/commands/%s.md` does not exist. A command mentioned "
            "here that the harness cannot actually run is the same failure "
            "as a dead fenced path." % name, match="/" + name))


def map_coverage_note(raw, repo_root):
    """Top-level directories the root file names nothing about, or None.

    A note, not a finding: whether an unmentioned directory belongs in the
    map is a judgment call this function cannot make, and a strict version
    of it would be noisy on any repo with build output or vendored
    directories PRUNE_DIRS does not happen to list.
    """
    try:
        entries = os.listdir(repo_root)
    except OSError:
        return None
    dirs = sorted(d for d in entries
                 if d not in PRUNE_DIRS and not d.startswith(".")
                 and os.path.isdir(os.path.join(repo_root, d)))
    lower_raw = raw.lower()
    missing = [d for d in dirs if d.lower() not in lower_raw]
    if not missing:
        return None
    return ("top-level director%s not named anywhere in this file: %s"
            % ("y" if len(missing) == 1 else "ies", ", ".join(missing)))


def harness_inventory_note(repo_root):
    """What of the harness's own config surface exists, as one fact.

    Existence only: whether a rule this file states is *also* enforced by
    one of these (a hook, a command) is a judgment call in
    references/criteria.md, not something this function decides.
    """
    parts = []
    if os.path.isfile(os.path.join(repo_root, ".claude", "settings.json")):
        parts.append(".claude/settings.json")
    mcp_path = os.path.join(repo_root, ".mcp.json")
    if os.path.isfile(mcp_path):
        try:
            with open(mcp_path, encoding="utf-8") as fh:
                servers = json.load(fh).get("mcpServers", {})
            parts.append(".mcp.json (%d server(s))" % len(servers))
        except (OSError, ValueError):
            parts.append(".mcp.json")
    for sub in ("commands", "agents"):
        d = os.path.join(repo_root, ".claude", sub)
        if os.path.isdir(d):
            n = len([f for f in os.listdir(d) if f.endswith(".md")])
            if n:
                parts.append(".claude/%s/ (%d)" % (sub, n))
    if not parts:
        return None
    return "harness config present: %s" % ", ".join(parts)


def git_currency_note(path, repo_root):
    """'last changed N commits ago' evidence for staleness, or None.

    Silent on any failure: no git binary, repo_root's `.git` is the bare
    marker the other checks use rather than a real repository, the file is
    untracked, or the command times out. This is evidence for the judgment
    pass, never a finding, so a failure to compute it is not worth a report
    of its own.
    """
    try:
        last = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", path], cwd=repo_root,
            capture_output=True, text=True, timeout=5)
        if last.returncode != 0 or not last.stdout.strip():
            return None
        commit = last.stdout.strip()
        count = subprocess.run(
            ["git", "rev-list", "--count", "%s..HEAD" % commit],
            cwd=repo_root, capture_output=True, text=True, timeout=5)
        when = subprocess.run(
            ["git", "log", "-1", "--format=%ar", "--", path], cwd=repo_root,
            capture_output=True, text=True, timeout=5)
        if count.returncode != 0 or when.returncode != 0:
            return None
        n = int(count.stdout.strip() or "0")
        ago = when.stdout.strip() or "some time ago"
        if n == 0:
            return "last changed %s, the most recent commit in the repository" % ago
        return "last changed %s, %d commit(s) to the repository since" % (ago, n)
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


# Share of shared long lines before a CLAUDE.md/AGENTS.md pair in one
# directory reads as one memory file duplicated by hand rather than two.
DUAL_HARNESS_OVERLAP = 0.3


def _qualifying_lines(path):
    try:
        with open(path, encoding="utf-8-sig") as fh:
            text = fh.read()
    except OSError:
        return set()
    return {normalize_line(l) for l in text.splitlines()
            if len(normalize_line(l)) >= LIMITS["duplicate_min_chars"]}


def dual_harness_findings(files):
    """{path: [finding, ...]} for a same-directory CLAUDE.md/AGENTS.md pair
    that is not already a symlink and shares enough content that a symlink,
    not two hand-maintained files, is probably what is wanted."""
    by_dir = {}
    for f in files:
        name = os.path.basename(f)
        if name in ("CLAUDE.md", "AGENTS.md"):
            by_dir.setdefault(os.path.dirname(f), {})[name] = f
    out = {}
    for pair in by_dir.values():
        if "CLAUDE.md" not in pair or "AGENTS.md" not in pair:
            continue
        c, a = pair["CLAUDE.md"], pair["AGENTS.md"]
        if os.path.realpath(c) == os.path.realpath(a):
            continue
        lines_c, lines_a = _qualifying_lines(c), _qualifying_lines(a)
        if not lines_c or not lines_a:
            continue
        overlap = len(lines_c & lines_a) / min(len(lines_c), len(lines_a))
        if overlap < DUAL_HARNESS_OVERLAP:
            continue
        pct = round(overlap * 100)

        def detail(companion):
            # Built fresh per companion rather than %-formatted twice: a
            # literal "%" left in the string by the first pass collides
            # with printf-style flags on the second (a literal "% of" reads
            # as the space flag plus the "o" conversion type, consuming an
            # argument that was never meant to be there).
            return ("This file and its %s companion share %d%% of their "
                    "substantial lines. Two files edited by hand drift; a "
                    "symlink (ln -s AGENTS.md CLAUDE.md, or the reverse) "
                    "keeps one real file serving both harnesses."
                    % (companion, pct))

        out.setdefault(c, []).append(finding(
            "claudemd-dual-harness", "%d%% overlap with AGENTS.md" % pct,
            "P2", 1, detail("AGENTS.md")))
        out.setdefault(a, []).append(finding(
            "claudemd-dual-harness", "%d%% overlap with CLAUDE.md" % pct,
            "P2", 1, detail("CLAUDE.md")))
    return out


# ---------------------------------------------------------------------------
# discovery
# ---------------------------------------------------------------------------

# The spellings people actually write to ignore .claude or its docs.
# Deliberately an exact set rather than a gitignore engine: a miss here
# costs one unnoticed warning, and a wildcard engine costs false alarms.
_CLAUDE_IGNORE_PATTERNS = {
    ".claude", ".claude/", "/.claude", "/.claude/",
    ".claude/*", ".claude/**",
    ".claude/docs", ".claude/docs/", "/.claude/docs", "/.claude/docs/",
}


def claude_docs_ignored(repo_root):
    """True when the repo's .gitignore hides .claude/docs from a clone."""
    try:
        with open(os.path.join(repo_root, ".gitignore"),
                  encoding="utf-8") as fh:
            lines = {line.strip() for line in fh}
    except OSError:
        return False
    return bool(lines & _CLAUDE_IGNORE_PATTERNS)


def check_docs_ignored(raw, repo_root, findings):
    """A memory file pointing into a .claude/docs a clone never receives.

    The restructure playbook moves depth to .claude/docs/, and a .gitignore
    that hides .claude turns every one of those links dead for anyone else
    who clones the repository. Local reads keep working, which is exactly
    why nobody notices.
    """
    if ".claude/docs" not in raw or not claude_docs_ignored(repo_root):
        return
    line = next((i for i, l in enumerate(raw.splitlines(), start=1)
                 if ".claude/docs" in l), 1)
    findings.append(finding(
        "claudemd-docs-ignored", ".claude/docs is gitignored", "P1", line,
        "This file points into .claude/docs while .gitignore hides .claude "
        "from the repository, so collaborators cloning it never receive "
        "those files and every link is dead for them. Track the docs (a "
        "negation such as !.claude/docs/ works) or move them to a tracked "
        "home."))


def find_repo_root(start, max_up=8):
    """Nearest ancestor of `start` holding .git, or None."""
    directory = os.path.abspath(start)
    for _ in range(max_up + 1):
        if os.path.isdir(os.path.join(directory, ".git")):
            return directory
        parent = os.path.dirname(directory)
        if parent == directory:
            return None
        directory = parent
    return None


def discover(root, names=CLAUDE_NAMES):
    """Every matching memory file spelling under `root`, pruned of vendored trees."""
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in PRUNE_DIRS and not d.startswith("."))
        for name in filenames:
            if name in names:
                hits.append(os.path.join(dirpath, name))
    return sorted(hits)


# ---------------------------------------------------------------------------
# the engine
# ---------------------------------------------------------------------------

def load_scan():
    if not os.path.exists(SCAN_PATH):
        return None
    spec = importlib.util.spec_from_file_location("hw_scan", SCAN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_SCAN = None


def run_prose_scan(raw, rules_path, required=False, ste="mechanical"):
    """(findings, stats, note, rules), same contract as readme_check.py.

    A voice that cannot be loaded never cancels the scan: the fingerprint and
    safety bands have nothing to do with whose voice the file is in.
    `required` is set when --voice-rules named the file by hand, and then the
    error is raised so main() exits 2 the way scan.py does.
    """
    global _SCAN
    if _SCAN is None:
        _SCAN = load_scan()
    if _SCAN is None:
        return [], {}, "rabbit-writes/scripts/scan.py not found, prose not scanned", None
    rules, note = None, None
    if rules_path:
        try:
            rules = voices_mod.load(rules_path, voices_dir=VOICES_DIR)
        except voices_mod.VoiceError as exc:
            if required:
                raise
            note = ("%s. No voice band in this report, everything else still "
                    "ran" % exc)
    # register 'docs': a CLAUDE.md is reference documentation by shape.
    # ste stated rather than inherited, so a default change upstream cannot
    # move this report silently.
    findings, stats = _SCAN.scan(raw, profile="docs", exempt=True,
                                 voice_rules=rules, suppressions=False,
                                 ste=ste)
    return findings, stats, note, rules


# ---------------------------------------------------------------------------
# one file
# ---------------------------------------------------------------------------

def check_claude_file(raw, path, repo_root, dup_index, use_voice=True,
                      voice_rules=None, no_ste=False):
    """(findings, stats, voice_name, notes) for one CLAUDE.md / AGENTS.md."""
    findings, stats, notes = [], {}, []
    file_dir = os.path.dirname(os.path.abspath(path))
    basename = os.path.basename(path)

    # Stated first, so the report opens with it: a symlinked pair is one
    # file serving two harnesses, and every finding below lands on the real
    # file whichever name was audited.
    if os.path.islink(path):
        notes.append("%s is a symlink to %s. One memory file serving both "
                     "harnesses: edits through either name land in the real "
                     "file." % (basename, os.readlink(path)))

    if basename in AGENT_NAMES:
        claude_companion = os.path.join(file_dir, "CLAUDE.md")
        if not os.path.exists(claude_companion):
            notes.append("AGENTS.md detected without a companion CLAUDE.md. "
                         "If using the Claude Code harness, consider symlinking: "
                         "ln -s %s CLAUDE.md" % basename)

    is_root_file = (repo_root
                    and os.path.abspath(file_dir) == os.path.abspath(repo_root)
                    and basename in ("CLAUDE.md", "AGENTS.md"))

    check_size(raw, findings, stats)
    check_char_budget(raw, findings, stats)
    check_bullets(raw, findings, stats)
    check_emphasis(raw, findings, stats)
    check_changelog_tells(raw, findings, stats)
    check_forward_state(raw, findings, stats)
    check_over_verification(raw, findings, stats)
    check_intro(raw, findings, stats)
    check_imports(raw, file_dir, findings, stats)
    check_import_cost(raw, file_dir, findings, stats)
    if repo_root:
        check_fenced_paths(raw, repo_root, file_dir, findings, stats)
        check_duplicates(path, raw, dup_index, repo_root, findings)
        check_docs_ignored(raw, repo_root, findings)
        check_dead_command_refs(raw, repo_root, findings)
        if is_root_file:
            for note in (map_coverage_note(raw, repo_root),
                        harness_inventory_note(repo_root),
                        git_currency_note(path, repo_root)):
                if note:
                    notes.append(note)
    else:
        notes.append("no .git root above this file, so the dead-path and "
                     "duplicate checks did not run")

    voice_name, rules_path = None, None
    if use_voice:
        rules_path = voice_rules
        if rules_path is None:
            rules_path, voice_name, note = voices_mod.resolve(
                path, voices_dir=VOICES_DIR)
            if note:
                notes.append(note)
        else:
            voice_name = voices_mod.strip_rules_suffix(
                os.path.basename(rules_path))

    # The engine's ste= is a tri-state and raises on anything else, None
    # included: "off" is the spelling for --no-ste.
    ste_mode = "off" if no_ste else "mechanical"
    prose_findings, prose_stats, note, rules = run_prose_scan(
        raw, rules_path, required=bool(use_voice and voice_rules),
        ste=ste_mode)
    if note:
        notes.append(note)
    findings.extend(prose_findings)
    for key in ("avg_sentence_words", "burstiness", "word_count"):
        if key in prose_stats:
            stats[key] = prose_stats[key]

    # One unified suppression pass over both halves, the readme_check shape:
    # scan ran with suppressions=False so an inline rabbit-allow can cover a
    # structure finding too, and a profile's engine_exemptions ride along.
    allowances, problems = suppress.parse(raw)
    allowances.extend(suppress.profile_allowances(rules))
    used, refused = suppress.apply(findings, allowances)
    findings.extend(suppress.audit(allowances, problems, used,
                                   findings_mod.make, refused))

    findings.sort(key=findings_mod.sort_key)
    return findings, stats, voice_name, notes


# ---------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------

PRIORITY_TITLES = {"P0": "P0  blocks: evidence of concealed or planted text",
                   "P1": "P1  clear defect in the memory file",
                   "P2": "P2  polish, and evidence for the judgment pass"}
BAND_TITLES = {"safety": "  safety (concealed text, or text aimed at an agent)",
               "structure": "  structure and format (rabbit-claude-md)",
               "voice": "  voice (this writer's own rules)",
               "fingerprint": "  fingerprints (evidence about production)",
               "craft": "  craft (bad writing regardless of author)"}


def report_file(path, findings, stats, voice_name, notes):
    out = ["%s" % path,
           "  voice: %s   non-blank lines: %d   list items: %d   "
           "emphasis lines: %d"
           % (voice_name or "none", stats.get("nonblank_lines", 0),
              stats.get("list_items", 0), stats.get("emphasis_lines", 0))]
    for note in notes:
        out.append("  note: %s" % note)

    allowed = suppress.suppressed(findings)
    live = suppress.live(findings)

    if not live:
        out.append("  No mechanical findings. The judgment pass still has to "
                   "happen: run references/criteria.md over every line.")
    for pri in ("P0", "P1", "P2"):
        group = [f for f in live if f["priority"] == pri]
        if not group:
            continue
        out.append(PRIORITY_TITLES[pri])
        for band in ("safety", "structure", "voice", "fingerprint", "craft"):
            sub = [f for f in group if f["band"] == band]
            if not sub:
                continue
            out.append(BAND_TITLES[band])
            shown = {}
            for f in sub:
                shown[f["id"]] = shown.get(f["id"], 0) + 1
                if shown[f["id"]] > 4:
                    continue
                out.append("    L%-4d %s" % (f["line"], f["label"]))
                if (band == "structure" or f["priority"] == "P0") and f["excerpt"]:
                    out.append("           %s" % f["excerpt"])
            for fid, n in shown.items():
                if n > 4:
                    out.append("    ... and %d more %s" % (n - 4, fid))

    if allowed:
        out.append("  suppressed (%d, not counted above)" % len(allowed))
        for f in allowed:
            out.append("    L%-4d %s" % (f["line"], f["label"]))
    return "\n".join(out)


def report(root, entries):
    out = ["claude check: %s" % root,
           "files found: %d" % len(entries), ""]
    for e in entries:
        out.append(report_file(e["file"], e["findings"], e["stats"],
                               e["voice"], e["notes"]))
        out.append("")
    if len(entries) > 1:
        out.append("inventory")
        for e in entries:
            c = e["counts"]
            out.append("  %-40s %5d lines   P0 %d  P1 %d  P2 %d"
                       % (e["file"], e["stats"].get("nonblank_lines", 0),
                          c["P0"], c["P1"], c["P2"]))
    return "\n".join(out)


# ---------------------------------------------------------------------------
# entry
# ---------------------------------------------------------------------------

def main():
    examples = [
        "python3 claude_check.py CLAUDE.md",
        "python3 claude_check.py AGENTS.md",
        "python3 claude_check.py .",
        "python3 claude_check.py CLAUDE.md --json",
        "python3 claude_check.py CLAUDE.md --check",
        "python3 claude_check.py CLAUDE.md --no-voice",
        "python3 claude_check.py CLAUDE.md --voice-rules path/to/dana.rules.json",
    ]
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=examples
    )
    ap.add_argument("path", help="a CLAUDE.md or AGENTS.md file, or a directory to sweep "
                                 "for memory files")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--no-voice", action="store_true",
                    help="apply no voice profile. Structure, fingerprints and "
                         "craft are still checked")
    ap.add_argument("--voice-rules", metavar="PATH",
                    help="a voice's <name>.rules.json; overrides .rabbit-voice "
                         "and ACTIVE")
    ap.add_argument("--no-ste", action="store_true",
                    help="disable STE readability rules (sentence length caps, "
                         "paragraph sentence counts, trailing conditions)")
    ap.add_argument("--repo-root", metavar="PATH",
                    help="override the repository root used for the dead-path "
                         "and duplicate checks. Default: nearest ancestor "
                         "holding .git")
    ap.add_argument("--global", action="store_true", dest="use_global",
                    help="fold ~/.claude/CLAUDE.md and ~/.codex/AGENTS.md "
                         "into the duplicate check, read-only")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any unsuppressed P0 finding is present")
    args = ap.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isdir(target):
        repo_root = args.repo_root or find_repo_root(target) or target
        # Both families are audited together: a directory with real content
        # in both a CLAUDE.md and an AGENTS.md is exactly the case
        # dual_harness_findings exists to catch, and auditing only one
        # family would hide the other file entirely. Deduped by realpath
        # first, CLAUDE spellings before AGENTS spellings, so a symlinked
        # pair is one report under the CLAUDE.md name rather than the same
        # content audited twice under two names.
        raw_files = discover(target, CLAUDE_NAMES) + discover(target, AGENT_NAMES)
        seen_real, files = set(), []
        for f in raw_files:
            real = os.path.realpath(f)
            if real in seen_real:
                continue
            seen_real.add(real)
            files.append(f)
        files.sort()
        if not files:
            print("no CLAUDE.md or AGENTS.md files under %s (looked for %s)"
                  % (target, ", ".join(ALL_MEMORY_NAMES)))
            return 0
        dual = dual_harness_findings(files)
    elif os.path.isfile(target):
        repo_root = args.repo_root or find_repo_root(os.path.dirname(target))
        files = [target]
        dual = {}
    else:
        print(cli_error.format_file_error(
            "claude_check.py", args.path, "path",
            expected_type="CLAUDE.md or AGENTS.md file or directory",
            details="path does not exist", examples=examples
        ), file=sys.stderr)
        return 2

    # The duplicate index reads the whole tree even for a single-file run, so
    # a fact that also lives in a sibling memory file is still reported.
    dup_paths = discover(repo_root, ALL_MEMORY_NAMES) if repo_root else list(files)
    if args.use_global:
        for g in GLOBAL_MEMORY:
            gp = os.path.expanduser(g)
            if os.path.isfile(gp):
                dup_paths.append(gp)
    dup_index = duplicate_index(dup_paths)

    entries = []
    for path in files:
        try:
            with open(path, encoding="utf-8-sig") as fh:
                raw = fh.read()
        except OSError as exc:
            print(cli_error.format_file_error(
                "claude_check.py", path, "path", expected_type="file path",
                details=str(exc), examples=examples
            ), file=sys.stderr)
            return 2
        try:
            findings, stats, voice_name, notes = check_claude_file(
                raw, path, repo_root, dup_index,
                use_voice=not args.no_voice, voice_rules=args.voice_rules,
                no_ste=args.no_ste)
        except voices_mod.VoiceError as exc:
            print(cli_error.format_file_error(
                "claude_check.py", args.voice_rules or "voice profile",
                "--voice-rules",
                expected_type="voice rules file path (.rules.json)",
                details=str(exc), examples=examples
            ), file=sys.stderr)
            return 2
        if dual.get(path):
            findings.extend(dual[path])
            findings.sort(key=findings_mod.sort_key)
        entries.append({"file": os.path.relpath(path, repo_root)
                        if repo_root else path,
                        "voice": voice_name, "notes": notes, "stats": stats,
                        "counts": findings_mod.counts(findings),
                        "findings": findings})

    total = {"P0": 0, "P1": 0, "P2": 0, "suppressed": 0}
    for e in entries:
        for key in total:
            total[key] += e["counts"].get(key, 0)

    if args.json:
        print(json.dumps({
            "schema_version": findings_mod.SCHEMA_VERSION,
            "root": repo_root,
            "limits": LIMITS,
            "counts": total,
            "files": entries,
        }, indent=2))
    else:
        print(report(repo_root or target, entries))

    if args.check and total["P0"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
