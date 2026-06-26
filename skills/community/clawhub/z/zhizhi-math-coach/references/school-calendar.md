# China School Calendar

## Default Model

Use these defaults unless local files override them:

- School year starts on September 1 and ends the next August.
- First semester: September 1 to January 31.
- Second semester: February 1 to August 31.
- Midterm and final windows are school-specific and must be configurable.
- Winter break and summer break are school-specific and must be configurable.

## Phase Labels

Use one primary phase when recording or planning:

- `in_semester`: normal school weeks.
- `midterm_window`: midterm review or exam period.
- `final_window`: final review or exam period.
- `semester_ended`: exam finished, summary and archiving needed.
- `winter_break`: winter break.
- `summer_break`: summer break.
- `new_semester_warmup`: short preview before school starts.

## Grade Inference

Use `school_entry_year` as the stable input. In mainland China primary school, students normally move to the next grade each September.

Example:

```text
school_entry_year: 2025
date: 2026-05-18
grade: 一年级
semester: 下学期
```

Respect `grade_override` when present.

## Planning Rules

- Normal semester: use current textbook progress and recent mistakes.
- Midterm: cover learned content in the current semester plus this semester's wrong questions.
- Final: cover the full semester, weighted by repeated weak points and relapse risk.
- Semester ended: generate summary, archive evidence, and prepare a holiday review pool.
- Winter break: repair first-semester weak points; preview only when old issues are stable.
- Summer break: review the whole school year; preview next grade lightly.

## Record Fields

Add these where practical:

```text
school_year / grade / semester / term_phase / exam_window / break_phase
```

Do not infer actual teaching progress from date alone. Always combine date, curriculum progress, and school work evidence.
