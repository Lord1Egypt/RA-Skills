## Description:

Visual Explainer helps agents generate self-contained HTML pages for diagrams, architecture overviews, diff and plan reviews, project recaps, comparison tables, and other visual explanations of technical content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bengii](https://clawhub.ai/user/bengii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to turn complex codebase, plan, diff, architecture, and data-table explanations into browser-viewable HTML reports and slide-style visual summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can analyze broad project context and may expose private or sensitive repository information through generated reports or optional external generation.

Mitigation: Use it on sensitive repositories only after disabling external generation and reviewing generated HTML before sharing.

Risk: Generated HTML reports may execute browser-side scripts, load CDN resources, or persist locally beyond the original session.

Mitigation: Review reports before opening or distributing them, and vendor or remove external scripts when offline or controlled execution is required.

Risk: Server helper scripts can manage local HTTP servers and processes on ports 8080-8089.

Mitigation: Check port usage before running server scripts, avoid machines with important services on those ports, and stop or clean up the server after use.

## Reference(s):

- [Visual Explainer on ClawHub](https://clawhub.ai/bengii/skills/visual-explainer)
- [CSS Patterns](references/css-patterns.md)
- [Libraries](references/libraries.md)
- [Responsive Navigation](references/responsive-nav.md)
- [Slide Patterns](references/slide-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Self-contained HTML files with brief Markdown or text handoff]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated pages may include Mermaid diagrams, data tables, slide decks, browser-viewable reports, and local file paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json and CHANGELOG show 0.4.3, SKILL.md frontmatter shows 0.4.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
