#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_how.py — objective signal collection for the HOW axis of four-axis debloating (skill-debloater Step 2, symmetric to triage.py).

HOW axis (from AIP): AIP's core is compiling "prose describing a deterministic process" into a deterministic script/pseudocode.
Flaky execution is often caused by: logic that should execute deterministically was written as "natural language the
model re-derives every time" — reasoned correctly one time, incorrectly the next.

This script gives two kinds of signal:
  [strong] Already written as code, but in the wrong layer — a large code block in the body (layer 2).
           Objective, high-precision, judged directly. This is the degenerate case — the code is already
           written, it just hasn't been moved to scripts/ (layer 3), which is "should have been externalized
           but wasn't" — it both dilutes attention and wastes tokens by reloading into context every time.
  [weak]  Should be code, but is still prose — a paragraph of plain prose describes a deterministic process
          but wasn't written as code. This is AIP's real battleground, but judging it is fundamentally a
          "judgment call"; the script can only scan for deterministic keywords and give a hint, it can't
          make the final call.

Limitation (important to know): the script can't catch the hidden case of "prose that doesn't look like code
but is actually a deterministic process" — that requires the agent to read the body (the same pass as
WHAT/WHERE). **Zero code blocks does not mean HOW is healthy** — the weak signal is only a hint.
Whether to externalize is ultimately the agent's judgment call: steps needing judgment/interaction stay as
prose, only deterministic steps get externalized.

Usage:
    python3 scan_how.py "<SKILL.md file or skill directory>" [--json]
Standard library only, no third-party dependencies.
"""
import sys
import re
import json
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

EXTERNALIZE_MIN_LINES = 8   # body code blocks longer than this are suggested for externalization into a script file
CODE_LANGS = {"python", "py", "bash", "sh", "shell", "js", "javascript",
              "ts", "typescript", "ruby", "rb", "go", "java", "rust", "rs",
              "c", "cpp", "php", "perl", "lua", "r"}  # only these count as externalizable deterministic code
FENCE = re.compile(r"```([\w+-]*)\n(.*?)```", re.S)
DET_HINT = re.compile(
    r"(sort|sorted|for |while |def |json\.|subprocess|replace\(|"
    r"format|parse|iterate|calculate|compute|resolve|format)", re.I)

# --- Weak signal: paragraphs of prose describing a deterministic process (AIP's main battleground, hint only) ---
PROSE_DET = re.compile(
    r"sort|calculate|compute|format|parse|iterate|convert|concatenate|dedup(?:e|licate)?|"
    r"filter|aggregate|encode|decode|sum|accumulate", re.I)
STEP_LIST = re.compile(r"(?m)^\s*\d+[\.)]\s|^\s*Step\s+\d+")
SEQ_CUE = re.compile(r"first.{0,8}(then|next)|then.{0,8}(finally|lastly)|in order|one by one|sequentially", re.I)
# Presence of these words = this step needs judgment/interaction, should stay as prose, don't report it as a weak signal (reduce noise + maintain discipline)
JUDGMENT_CUE = re.compile(
    r"judge|depends on|case[- ]by[- ]case|ask the user|inquire|confirm|clarify|\bASK\b|decide based on|use your judgment",
    re.I)


def strip_frontmatter(md: str) -> str:
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            return md[end + 4:]
    return md


def mask_fences(body: str) -> str:
    """Replace fenced code blocks with an equal number of blank lines, preserving line alignment, leaving only prose for weak-signal scanning."""
    return FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), body)


def mask_nonprose(prose: str) -> str:
    """Blank out heading/table/blockquote lines (treat as block separators, preserve line numbers).
    Otherwise a body paragraph right after a heading would get merged into the same block and skipped along with the heading."""
    out = []
    for ln in prose.split("\n"):
        s = ln.lstrip()
        out.append("" if (s.startswith("#") or s.startswith("|") or s.startswith(">")) else ln)
    return "\n".join(out)


def iter_blocks(prose: str):
    """Split into blocks on blank lines, yielding (1-based start line, block text)."""
    lines = prose.split("\n")
    i, n = 0, len(lines)
    while i < n:
        if not lines[i].strip():
            i += 1
            continue
        start = i
        buf = []
        while i < n and lines[i].strip():
            buf.append(lines[i])
            i += 1
        yield start + 1, "\n".join(buf)


def scan_prose_hints(prose: str):
    """Weak signal: find paragraphs suspected of being 'a deterministic process written as prose'. Low precision, only a pointer for the agent's judgment.
    Input should already have mask_fences + mask_nonprose applied."""
    hints = []
    for start, block in iter_blocks(prose):
        if JUDGMENT_CUE.search(block):
            continue  # contains judgment/interaction cues -> should stay as prose, don't report
        steps = len(STEP_LIST.findall(block))
        det_kw = sorted(set(m.group(0) for m in PROSE_DET.finditer(block)))
        seq = bool(SEQ_CUE.search(block))
        # Trigger: a multi-step list/ordered process, or a paragraph with >=2 deterministic verbs
        if (steps >= 3) or (seq and len(det_kw) >= 1) or (len(det_kw) >= 2):
            first = next((ln.strip() for ln in block.split("\n") if ln.strip()), "")
            hints.append({
                "line": start,
                "snippet": (first[:48] + "…") if len(first) > 48 else first,
                "steps": steps,
                "keywords": det_kw,
            })
    return hints


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print('Usage: python3 scan_how.py "<SKILL.md file or skill directory>" [--json]')
        sys.exit(1)

    target = Path(args[0])
    skill_md = target / "SKILL.md" if target.is_dir() else target
    if not skill_md.is_file():
        print(f"SKILL.md not found: {skill_md}")
        sys.exit(1)

    body = strip_frontmatter(skill_md.read_text(encoding="utf-8", errors="ignore"))
    total_lines = body.count("\n") + 1

    # --- Strong signal: large code blocks in the body ---
    blocks, code_lines = [], 0
    for m in FENCE.finditer(body):
        content = m.group(2)
        nlines = content.count("\n")
        code_lines += nlines
        blocks.append({
            "line": body[:m.start()].count("\n") + 1,
            "lang": m.group(1) or "(none)",
            "lines": nlines,
            "deterministic_hint": bool(DET_HINT.search(content)),
        })
    candidates = [b for b in blocks
                  if b["lines"] >= EXTERNALIZE_MIN_LINES and b["lang"].lower() in CODE_LANGS]

    # --- Weak signal: deterministic processes in prose (after masking code blocks/headings/tables) ---
    prose_hints = scan_prose_hints(mask_nonprose(mask_fences(body)))

    code_ratio = round(code_lines / total_lines, 3) if total_lines else 0
    result = {
        "skill": skill_md.parent.name,
        "body_lines": total_lines,
        "code_blocks": len(blocks),
        "code_lines": code_lines,
        "code_ratio": code_ratio,
        "externalize_candidates": candidates,   # strong signal
        "prose_hints": prose_hints,             # weak signal
    }

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"\n=== HOW axis scan: {result['skill']} ===\n")
    print(f"Body: {total_lines} lines, {len(blocks)} code block(s) / {code_lines} lines of code"
          f" ({code_ratio*100:.0f}% of body)\n")

    # Strong signal
    if not candidates:
        print("[strong signal] No body code blocks >= 8 lines (no 'code in the wrong layer' case).")
    else:
        print(f"[strong signal · externalize] {len(candidates)} large code block(s) should be externalized into a script:")
        for i, b in enumerate(candidates, 1):
            tag = " · contains deterministic-logic keywords" if b["deterministic_hint"] else ""
            print(f"  {i}) body line {b['line']}, {b['lang']}, {b['lines']} lines{tag}")
            print("       -> externalize into a scripts/ script, leave only 'run it' in the body")
    print()

    # Weak signal
    if not prose_hints:
        print("[weak signal] No obvious 'deterministic process written as prose' paragraphs found.")
    else:
        print(f"[weak signal · prose-hint] {len(prose_hints)} paragraph(s) suspected of being a deterministic process (needs your judgment):")
        for i, h in enumerate(prose_hints, 1):
            meta = []
            if h["steps"]:
                meta.append(f"{h['steps']} steps")
            if h["keywords"]:
                meta.append("contains " + ", ".join(h["keywords"]))
            print(f"  {i}) body line {h['line']}: \"{h['snippet']}\""
                  + (f"  ({' / '.join(meta)})" if meta else ""))
            print("       -> if deterministic and no judgment/interaction needed -> compile into a scripts/ script; otherwise keep as prose")
    print()

    print("Limitation: strong signals are high-precision and can be judged directly; weak signals are low-precision, only a pointer. "
          "The script can't fully catch 'prose that doesn't look like code but is actually a deterministic process' — "
          "that requires the agent to read the body and judge (same as WHAT/WHERE). Zero code blocks != HOW healthy.\n")


if __name__ == "__main__":
    main()
