# Worksheet Standards

## Format

Generate printable worksheets as HTML plus a student-facing PDF by default. The PDF is the primary file to send to the parent or student because it opens and prints consistently outside GitHub Pages.

Use the bundled generator whenever possible:

```bash
python3 {baseDir}/scripts/generate_worksheet.py \
  worksheets/YYYY-MM-DD-topic/worksheet-spec.json
```

The generator writes:

- `worksheet.html`: child-facing practice.
- `worksheet.pdf`: child-facing printable PDF when Chrome/Chromium is available.
- `answer-key.md`: parent-facing answers and grading rules.

If PDF export is skipped because Chrome/Chromium is unavailable, return the HTML path and mention the missing browser dependency. If the worksheet is published to GitHub Pages, publish only the child-facing worksheet HTML/PDF. Do not put answers, diagnosis records, memory files, or source photos under `site/`.

## Child-Facing Page

- Title names the target topic directly.
- Include `姓名`、`日期`、`用时`、`正确题数`.
- Keep reminders short; never put answers on the worksheet.
- Do not include student names, school names, source-file names, or diagnosis labels when the page will be public.
- Use section names such as `先判断`、`再计算`、`挑战一下`.
- Leave visible working space for drawing, vertical forms, or equations.
- For classification tasks, prefer `圈一圈`、`打勾`、`连线` or printed choices over writing difficult Chinese characters.
- If two-digit horizontal addition/subtraction appears, remind: `两位数横式先写规范竖式或清楚标记进退位`.
- Include a checking habit reminder when relevant: `做完后自己选 1 道最容易错的题检查`.
- Prefer clear, targeted practice over forcing the page to be completely full.
- Multiple pages are acceptable when clarity improves.

## Answer Key

Keep the answer key in Markdown and include:

- Correct answer and equation for each item.
- Error labels the parent can use while grading.
- Reassessment rules: weak / consolidating / mastered.
- Recommended next practice focus.

## Difficulty Defaults

- Infer grade and semester from local memory before setting number range.
- Use current-grade scope unless the request is explicitly remedial.
- For a weak point, prefer short focused sets over broad mixed drills.
- For fluency practice, use small daily sets and track time gently.
- For word problems, vary scenario and question wording when testing transfer.
