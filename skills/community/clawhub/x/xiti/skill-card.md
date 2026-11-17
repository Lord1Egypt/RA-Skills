## Description:

析题 generates Chinese-language heuristic competitive-programming solution writeups that teach reasoning, explain code, preserve samples, and produce Markdown, HTML, or Typst/PDF-ready materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External users, instructors, and developers use this skill to turn programming contest problems or reference solutions into explanatory Chinese writeups, annotated code, visualizations, and delivery artifacts. It is aimed at teaching the reasoning path behind a solution rather than only returning an answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may contact external CDNs when opened.

Mitigation: Review the generated HTML before sharing and host dependencies locally when operating in restricted or offline environments.

Risk: The SVG helper writes local files and the bundled example uses a shared /var/tmp path.

Mitigation: Run helper scripts with a user-controlled output directory and inspect paths before execution on shared machines.

Risk: Generated competitive-programming explanations or code may be incomplete or misleading for edge cases.

Mitigation: Review solution logic, preserve original samples, and test reference code against representative and boundary inputs before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/xiti)
- [Publisher profile](https://clawhub.ai/user/fslong520)
- [anime.js CDN dependency](https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js)
- [KaTeX CDN dependency](https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.css)
- [highlight.js CDN dependency](https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.11.1/build/highlight.min.js)
- [Mermaid CDN dependency](https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js)
- [AtCoder ABC457 task examples](https://atcoder.jp/contests/abc457/tasks)
- [AtCoder ABC460 task examples](https://atcoder.jp/contests/abc460/tasks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, single-file HTML, Typst source intended for PDF compilation, SVG assets, and annotated code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese instructional prose, preserved problem samples, Mermaid diagrams, KaTeX formulas, highlighted C++ snippets, static SVG figure sequences, and validation commands.]

## Skill Version(s):

1.7.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
