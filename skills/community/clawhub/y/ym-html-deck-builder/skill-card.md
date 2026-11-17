## Description:

Turns a topic or Markdown outline into a standalone, paginated HTML slide deck with keyboard navigation, page numbers, a progress bar, and light or dark themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn a topic or Markdown outline into a local browser-presentable HTML slide deck. It is useful for quick PPT-style presentations when the user wants an offline, dependency-free file rather than PowerPoint or PDF export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator writes or overwrites deck.html in the current working directory.

Mitigation: Run it from the intended output directory or move existing deck.html files before rendering.

Risk: Input is expected to be UTF-8 Markdown, and non-UTF-8 outlines can fail or render incorrectly.

Mitigation: Save outlines as UTF-8 before running the script.

Risk: The skill is tailored for Chinese-language decks and does not export PowerPoint or PDF.

Mitigation: Use it for browser-based HTML presentations, and choose another workflow when PPTX or PDF export is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-html-deck-builder)
- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-html-deck-builder)
- [HTML slide interaction patterns](references/html-patterns.md)
- [Deck outline template](templates/deck-outline.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance, files]

**Output Format:** [Markdown guidance with shell commands that produce a standalone HTML file named deck.html]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or overwrites deck.html in the directory where the script runs; accepts UTF-8 Markdown input and supports light or dark themes.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
