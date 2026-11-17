# Worksheet Generation

Standalone paper requests use `zhizhi-math-worksheet` when installed. That skill is self-contained, preserving the full-paper photo workflow alongside a general question-list branch; selected mistakes and weak-point questions use the latter, with optional diagnosis context. This reference retains the coach's compatibility workflow and bundled HTML tooling; it is not a dependency of the standalone skill.

## Product contract

The parent asks for a worksheet, not a renderer or a question-type registry. Deliver a readable A4 printable PDF and page preview images when rendering support is available. Keep answers separate. Do not ask the parent to choose SVG, HTML, templates or image APIs.

The model designs the paper from the parent's request, actual learned scope, photo evidence, knowledge assessment and due reviews. Fixed question templates are optional tools, not the default limit on creativity. A paper can mix reading, calculation, drawing, comparison, spatial tasks and meaningful variants in any suitable layout.

## Default model-designed flow

1. Build compact learning context. Read matching original papers and topic evidence when available; never claim to have seen prior uploads that are not accessible in the current workspace.
2. Write a short internal brief: learned scope, target concepts, observed difficulties, approximate duration, question count, preferred response actions and any original-paper references.
3. Design the questions, diagrams and page composition. Independently solve every question and check the diagram actually supports that solution. Test transfer by changing representations or relevant conditions, not only numbers.
4. Choose an available document tool internally. For a reference-photo paper with a custom composition, the model may author a local PDF layout program directly (for example with ReportLab); follow the direct-PDF flow below. For browser-based output, save `worksheet-spec.json` with `render_mode: model_html`: `student_html` is the complete student page and `questions` is the separate answer manifest. Neither route requires registering new question types.
5. Generate the student PDF and separate answers. In the HTML route, run the normal validator/generator, which applies the shared CSS, writes the Markdown answer key and attempts PDF export. In either route, render previews from the actual PDF and provide a separate printable answer PDF when the parent asks for a paper and answers.
6. Inspect page previews when available: no clipped questions, overlapping labels, tiny text, answer leaks or missing drawing/writing space. Revise and re-render if needed. Never report page count or visual verification without actually checking it.
7. Deliver the preview image(s) plus printable PDF. Report missing PDF/preview dependencies accurately; local HTML remains an editable fallback. Publish or sync only under the existing workspace configuration.

```bash
python3 {baseDir}/scripts/validate_worksheet_spec.py worksheets/YYYY-MM-DD-topic/worksheet-spec.json
python3 {baseDir}/scripts/generate_worksheet.py worksheets/YYYY-MM-DD-topic/worksheet-spec.json
```

## Model-authored spec

This schema and the commands above apply to the HTML route, not arbitrary PDF layout programs.

For English output, set `language: en` and author the complete `student_html`, questions and explanations in English, with `<html lang="en">`. The helper localizes answer-key labels for English and Chinese; absent an explicit language, it reads the HTML language and retains Chinese as the legacy fallback. It does not translate question content. Other output languages should use direct model-authored documents; the bundled record and fixed-template helpers are not fully localized.

```json
{
  "version": 2,
  "render_mode": "model_html",
  "title": "看图数学小练习",
  "date": "2026-10-01",
  "review_status": "model_reviewed",
  "brief": {"duration_minutes": 10, "scope": ["已确认学过的内容"], "focus": "本次验证的能力"},
  "questions": [
    {"id": "1", "knowledge_points": ["arithmetic.addition-within-20"], "answer": "12", "explanation": "7加3得10，再加2得12。"}
  ],
  "student_html": "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><title>看图数学小练习</title></head><body><main><h1>看图数学小练习</h1><p>姓名：________ 日期：________</p><section data-question-id=\"1\"><h2>1. 7 + 5 = ______</h2></section></main></body></html>"
}
```

Use `.question` or `data-question-id` for question blocks and `.work-line` for working space. Each answer ID must occur exactly once as `data-question-id` in the student page. Images must be self-contained; active scripts and external asset requests are rejected. The automatic validator checks document completeness and static content, **not mathematical truth or image recognition accuracy**. `model_reviewed` means the model actually performed a separate solution/diagram check, not merely that a flag was filled in.

The editable example is `examples/student-workspace/worksheets/sample-model-designed/` in the source repository.

## Shared print profile

Choose density from the task without requiring the parent to configure typography:

- A photo plus “类似的试卷 / 变式卷” means preserve the original section structure, approximate length and tested concepts. Use a school-paper layout: body 12 pt, headings 13–14 pt, title 18–20 pt, line height around 1.4, normal character spacing. Long options may use 11.5 pt; meaningful figure labels should normally be at least 10.5–11 pt. Do not copy student/school identifiers or handwritten answers.
- A short remedial drill benefits from larger type and more writing space: body 14 pt, title 22 pt, line height 1.5, letter spacing 0.02 em.
- Both use A4 portrait and approximately 12 mm margins. Keep each diagram with its question, preserve handwriting space and allow additional pages instead of shrinking the whole paper.

The bundled HTML generator currently applies the larger-type profile through `assets/worksheet/a4-print.css`:

- A4 portrait; 12 mm margins.
- Body/question text 14 pt; main title 22 pt; metadata 10.5 pt.
- Line height 1.5; letter spacing 0.02 em.
- Question and diagram stay together where possible; natural pagination is allowed.
- Keep diagram labels readable at final print size, normally at least 11 pt. Plan adequate handwritten answer space for the child's age.
- Never shrink the whole page to force one-sheet output. Change the number of questions or allow another page.

For direct PDF output, apply the chosen measurements in the layout program. CSS does not apply to a PDF canvas. Do not expose implementation choices in parent/student output.

## Direct-PDF flow

This is a model/tool workflow, not a new `render_mode` accepted by `generate_worksheet.py`.

1. Save an editable local layout program, such as `make_worksheet.py`, with the questions and separate solutions in the personal worksheet directory. Use available Chinese fonts and actual A4 dimensions; resolve dependencies locally rather than hardcoding another machine's paths. Keep question IDs, knowledge points and checked solutions in a private `answer-manifest.json` so later grading can recover the learning targets.
2. Generate `worksheet.pdf` and `answer-key.pdf` separately; retain `answer-key.md` for learning records. Never place solutions in the student PDF. Review model-authored code before execution and keep it limited to document generation in that directory.
3. Reopen both PDFs to verify page dimensions, page count, readable text and matching question/answer numbers. Rasterize every page with Poppler or `worksheet_preview.export_previews`; use separate preview directories for the paper and answers.
4. Inspect the rendered pages for clipped content, overlapping labels, character substitution and cramped writing space. Independently solve the rendered questions, including counting objects and station intervals. Fix and re-render before delivery.
5. Deliver the student PDF, answer PDF and previews locally. The existing Pages publisher discovers `worksheet.html`; PDF-only directories are not automatically published. If configured publishing is required, add a small student-only `worksheet.html` linking to `worksheet.pdf`, without embedding answers or private metadata, then use the existing publishing workflow.

### Content review

- Compare the new paper with the source: retain intended knowledge points and difficulty, while changing quantities, context and at least some reasoning or representation when transfer is requested.
- Same-structure numerical variants are valid for parallel practice; do not describe them as evidence of transfer mastery. A generated paper alone is not evidence of the child's mastery.
- Check that each multiple-choice item has exactly one intended answer. Avoid conspicuous answer-position concentration or repeated patterns; recheck the key after reordering options. Do not force exact balance at the expense of question quality.
- Check units, diagram quantities, interval counts, alternative valid answers and consistency between the question, solution and printed figure.
- This review is a model responsibility. Structural validators and a `model_reviewed` flag alone do not establish mathematical correctness.

## Image-generation capability

A reasoning model designing a paper and an image model generating a raster page are separate capabilities. If the runtime has an actual image-generation tool and the parent chooses that route, it can produce a paper image; independently check every character, symbol, object count, diagram relation and answer before delivery. Do not claim image generation occurred when only markup was authored, and do not treat a prompt as a guarantee of exact typography or mathematical correctness. If no image tool is available, state that limitation. The standard path converts a model-designed document into PDF and preview images.

## Optional template path

Existing `sections/items` specs and `generate_visual_practice.py` remain available for quick repeatable drills. They are optional shortcuts. Do not reduce a requested rich or unfamiliar question to a supported template just to satisfy the renderer. For established templates, keep answers in the source spec and validate before printing.

## Dependencies and output

- HTML-route PDF: Chrome/Chromium; bounded export timeout. `--pdf` requires success; `--no-pdf` skips export. Direct-PDF generation instead uses the available PDF authoring tools and does not require a browser.
- Previews: Poppler (`pdftoppm`) or PyMuPDF (`python3 -m pip install pymupdf`). `--no-preview` skips previews.
- Outputs: `worksheet.html`, `worksheet.pdf` when available, `worksheet-page-1.png` etc. when available, and private `answer-key.md`.
- `--verify-print` checks the expected page count when a specific count is part of the request.
- The private source spec contains answers. Publish only the generated student-facing files; never the source spec or answer key.
