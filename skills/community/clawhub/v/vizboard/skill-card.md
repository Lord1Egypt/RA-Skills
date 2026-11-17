## Description:

Vizboard helps agents generate self-contained HTML dashboards and visual technical pages for architecture diagrams, flowcharts, KPI dashboards, data tables, diff reviews, plan reviews, and project recaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redf426](https://clawhub.ai/user/redf426)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use Vizboard to turn complex technical explanations, code reviews, plans, recaps, diagrams, dashboards, and tables into responsive HTML pages. The skill is suited for visualizing architecture, flow, project state, factual verification summaries, and comparison-heavy technical material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflows may inspect repository history, local agent memory, prior conversation context, and changed files.

Mitigation: Use only on projects where that scope is acceptable, or require explicit approval before repository, memory, or conversation-history inspection.

Risk: Generated reports are saved under ~/.agent/diagrams and can be copied into the workspace for delivery.

Mitigation: Review generated HTML for sensitive content before sharing and clean generated artifacts after delivery.

Risk: Some templates and references use external CDNs, Google Fonts, and optional surf/gemini image generation.

Mitigation: Disable external CDN, font, and image-generation use for confidential, offline, or network-restricted deployments.

Risk: The fact-check workflow can correct source documents in place.

Mitigation: Require explicit user approval or version-control review before applying in-place edits.

## Reference(s):

- [Vizboard ClawHub Skill Page](https://clawhub.ai/redf426/skills/vizboard)
- [CSS Patterns](references/css-patterns.md)
- [External Libraries](references/libraries.md)
- [Responsive Section Navigation](references/responsive-nav.md)
- [Mermaid.js CDN](https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs)
- [Mermaid ELK Layout CDN](https://cdn.jsdelivr.net/npm/@mermaid-js/layout-elk/dist/mermaid-layout-elk.esm.min.mjs)
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js)
- [Anime.js CDN](https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Shell commands, Guidance]

**Output Format:** [Self-contained HTML files with concise Markdown delivery notes and inline shell command snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated HTML under ~/.agent/diagrams and copy files into the workspace for delivery; the fact-check workflow can edit target documents in place.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
