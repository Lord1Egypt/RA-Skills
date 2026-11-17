# Academic Paper Translator

![version](https://img.shields.io/badge/version-1.1.2-blue)

A Codex skill for translating complete English academic papers into polished Simplified Chinese DOCX files.

## Standard invocation (标准调用示例)

This is the canonical instruction to start the skill. When an AI receives this instruction together with an English paper, it must begin the full translation immediately and must not ask non-essential questions in between.

> 调用 translate-academic-papers 完整翻译这篇英文论文。直接开始，中间不要询问；生成“全文中文版”和“逐段中英对照版”两个 DOCX。所有图片必须调用 Image2 重新渲染，将图内英文覆盖为中文；保留公式和英文参考文献，并制作可在 WPS 中使用的引文跳转。

### Execution requirements

- Read and parse the entire paper directly; translate the body, title, abstract, methods, results, discussion, appendix, and figure captions.
- Generate two DOCX files: `全文中文版.docx` and `逐段中英对照版.docx`.
- In the bilingual edition, keep each complete English paragraph immediately followed by its complete Chinese paragraph; never merge or split paragraphs.
- Call Image2 for every image containing semantic English, overwriting the original English with Chinese at the same locations while preserving data, coordinates, scales, colors, shapes, error bars, significance marks, and layout.
- Keep citation numbers unchanged; keep the reference list in English (authors, journal names, paper titles, and DOIs untranslated).
- Build WPS-compatible citation-to-reference jumps with native OOXML `w:hyperlink` (Ctrl+click) and clickable DOI links.
- Preserve formulas, variables, units, statistical symbols, numbers, and data formats.
- Ask the user only for genuine blockers (unreadable/corrupt/password-protected file, missing pages, unwritable output directory, or no Image2 capability).

### Prohibited

- Do not output only a plan, summary, reading notes, or a partial translation.
- Do not ask about model, terminology, filename, output directory, or image format before starting.
- Do not claim a "missing translation engine" and stop.
- Do not use figure titles or captions to replace in-figure text translation.
- Do not build the bilingual edition as "all English + all Chinese".
- Do not claim completion before the Image2 overlays are done.

## Features

- Generates a full Chinese edition and a paragraph-aligned English–Chinese edition.
- Preserves equations, tables, citation numbering, and the original English reference list.
- Translates figure titles, captions, legends, and semantic labels inside figures.
- Requires an actual Image2 edit for every raster figure containing semantic English; captions and translation panels do not count.
- Keeps original and localized figures together in the bilingual edition.
- Adds WPS-compatible citation navigation and clickable DOI links.
- Starts immediately from a supplied paper and uses resumable source-ID translation state without asking setup questions.
- Renders DOCX files through installed Microsoft Word or WPS on Windows; LibreOffice is not required.
- Applies hard quality gates for paragraph alignment, Image2 hashes, figure pairing, references, navigation, and rendered-page integrity.
- Uses no arbitrary translation time limit; verified quality takes priority.

## Installation

Copy this repository to:

```text
~/.codex/skills/translate-academic-papers
```

On Windows, the typical location is:

```text
C:\Users\<username>\.codex\skills\translate-academic-papers
```

The repository root contains `SKILL.md`.

## Usage

> Use Academic Paper Translator now. Without asking setup questions, completely translate this English paper. Deliver an Image2 Chinese-only DOCX and a paragraph-aligned English–Chinese DOCX, preserve equations and English references, add WPS Ctrl+click citation jumps and DOI links, render every page through Word/WPS, and repair all validation failures before returning the files.

## Citation navigation and literature lookup

In Microsoft Word or WPS Writer, hold **Ctrl** and click a citation number with the **left mouse button** to jump to its reference entry. Hold **Ctrl** and left-click a DOI to open its official DOI page. Some installations are configured for single-click hyperlinks and do not require Ctrl.

If a hyperlink does not open, press **Ctrl + F** and search for the DOI, exact title, author surname, or reference number. Use lawful sources such as publisher pages, PubMed Central, institutional subscriptions, preprints, and author manuscripts.

## Example

See [Figure-interior localization and reference navigation](examples/figure-localization.md), based on Figure 1 of Yazdanpanah et al. (2026), PNAS, https://doi.org/10.1073/pnas.2513856123. The repository also includes a real accepted Image2 heatmap pair and its hash-backed audit record under `examples/`.

## Repository layout

- `SKILL.md` — core workflow
- `agents/openai.yaml` — Codex UI metadata
- `references/` — translation, figure, performance, output, and QA standards
- `scripts/` — resumable translation pipeline, Word/WPS rendering, citation linking, Image2 manifests, media replacement, contact sheets, and final validation
- `examples/` — source-grounded usage examples

## Links

- [ClawHub listing](https://clawhub.ai/fangmingqi2005-create/skills/translate-academic-papers)

## Privacy and copyright

Only process papers the user is authorized to access. Do not publish source papers or translated copyrighted content without permission.

## License

MIT. See [LICENSE](LICENSE).

