---
name: srt-proofreader
description: Proofread SRT subtitles by using srts/source.md as terminology reference while preserving subtitle indices and timestamps. Use when users ask to proofread or correct srts/*.srt files and require git-tracked edits, optional large-file section splitting, and merge-back.
---

# SRT Proofreader

Execute the workflow in order. Keep edits minimal and deterministic.

## 1. Enter `srts/`

1. Change directory to the task's `srts/` folder.
2. Stop and report if `srts/` does not exist.

## 2. Ensure Git Baseline

1. Check whether `srts/` is already inside a git repository.
2. If not inside a git repository:
   - run `git init`
   - run `git add .`
   - run `git commit -m "init srt"`
3. Do not rewrite existing history.

## 3. Require and Read `source.md`

1. Check whether `srts/source.md` exists.
2. If missing, stop immediately and tell the user: `还没有创建 source.md`.
3. Read `source.md` before editing subtitles.
4. Extract terminology and proper nouns from `source.md`, then use them as authoritative wording.

## 4. Select the Main `.srt` File

1. List candidates in `srts/` with:
   - extension `.srt`
   - filename not starting with `.` or `_`
2. Require exactly one candidate.
3. If zero candidates, stop and report.
4. If multiple candidates, stop and ask the user which file is the main subtitle file.

## 5. Handle Large Files (`>400` lines)

1. Count lines in the main `.srt`.
2. If line count is `<=400`, edit directly.
3. If line count is `>400`:
   - split into `section-001.srt`, `section-002.srt`, ... using `scripts/srt_sections.mjs`
   - edit each section sequentially
   - merge sections back and overwrite the original main `.srt` using the same script
4. Use this script interface:
   - tool path: `scripts/srt_sections.mjs`
   - split: `node scripts/srt_sections.mjs split --input <main.srt> --output <dir> --chunk 400`
   - merge: `node scripts/srt_sections.mjs merge --input-dir <dir> --output <main.srt>`

## 6. Subtitle Editing Rules

1. Edit only typo-level text issues and term consistency.
2. Never modify subtitle sequence numbers.
3. Never modify timestamp lines (`-->`).
4. Preserve original line structure and blank-line boundaries.
5. Use `source.md` terminology as first priority.
6. Do not introduce new trailing punctuation on the final subtitle text line.

## 7. Final Verification

1. Review `git diff` and confirm index/timestamp lines are unchanged.
2. Confirm only subtitle text lines were modified.
3. Report completion with a short summary of corrected term categories.
