# Worksheet Standards

## Format

Follow explicit student and parent output-language preferences. Otherwise preserve the source question language for the worksheet and use the conversation language for explanations. Translate all generated labels consistently; the Chinese labels below are examples for Chinese worksheets. Use the learner's actual curriculum and units, not assumptions based on language.

Generate a student-facing printable PDF. The model may design a PDF directly or use editable HTML, as described in `worksheet-generation.md`. The PDF is the primary file to send to the parent or student because it opens and prints consistently outside GitHub Pages. When the parent asks for a paper and answers, provide a separate printable answer PDF too.

For the HTML/spec route, use the bundled generator:

```bash
python3 {baseDir}/scripts/generate_worksheet.py \
  worksheets/YYYY-MM-DD-topic/worksheet-spec.json
```

The generator writes:

- `worksheet.html`: child-facing practice.
- `worksheet.pdf`: child-facing printable PDF when Chrome/Chromium is available.
- `answer-key.md`: parent-facing answers and grading rules.

If browser export is unavailable, use an available direct-PDF tool; otherwise return the HTML path and accurately report the missing export capability. If the worksheet is published to GitHub Pages, publish only the child-facing worksheet HTML/PDF. Do not put answers, diagnosis records, memory files, or source photos under `site/`.

## Shared A4 Typography

Use A4 with about 12 mm margins. For a full variant paper based on a photo, prefer body 12 pt, headings 13–14 pt, title 18–20 pt and line height about 1.4; meaningful figure labels should normally be at least 10.5–11 pt. For short remedial drills, use the larger-type profile in `assets/worksheet/a4-print.css`: body 14 pt, title 22 pt, line height 1.5, letter spacing 0.02 em. The HTML generator currently applies the larger profile; direct-PDF tools apply the measurements in their layout code. Allow natural pagination instead of shrinking text to fit one page. Preview images must come from the actual printable PDF.

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

Keep the answer key in Markdown, and generate a separate answer PDF for printable paper-and-answer delivery. Include:

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
