# HTML Resume Styles

Use this reference only for the single-file HTML output mode. These are
resume-specific presentation directions, not imported third-party templates.

| Style | Core characteristics | Visual language | Best for |
| --- | --- | --- | --- |
| **Classic** | Predictable one-column scan, restrained hierarchy, generous breathing room | A single muted accent, conventional sections, readable body copy, minimal decoration | Recruiter review, ATS-adjacent handoff, corporate roles, and a broad or unknown reader |
| **Editorial** | Narrative-led hierarchy that foregrounds a concise point of view | Measured rules, display-type emphasis, long-form summary, quieter project treatment | Research, strategy, product, senior IC, writing-led, and thought-leadership profiles |
| **Studio** | Project and capability modules carry more evidence than a chronological-only layout | Confident accessible color, compact metadata, modular blocks, deliberate visual rhythm | Design, creative technology, independent builders, founders, portfolios, and project-led applications |

## Selection rules

- The full three-style comparison is already shown from
  [template-selection.md](template-selection.md). Do not repeat an additional
  questionnaire; use this reference to implement the selected style.
- Recommend **Classic** for hiring systems, conventional corporate roles, or
  when the target reader is unknown; still wait for the user's choice unless
  they explicitly delegate it. Recommend **Editorial** when the reader benefits
  from a concise professional narrative. Recommend **Studio** only when visual
  craft or project work is itself relevant evidence.
- Keep every style semantically equivalent: the style changes presentation,
  never the facts, section availability, reading order, or accessibility
  requirements in `SKILL.md`.
- Use inline CSS, local/system font stacks, and no external images, stylesheets,
  scripts, or fonts unless the user explicitly provides and approves them.
- For bilingual resumes, use one primary reading order. Do not place two dense
  translations side by side on narrow screens; stack them or create separate
  files when the content would become difficult to scan.

## Delivery note

State the selected style and language in the handoff. If the user wants a
different look, change only the presentation while keeping the same verified
facts and the single-file acceptance checks.
