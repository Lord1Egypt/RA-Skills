## Description:

Generate self-contained HTML pages and slide decks that visually explain systems, code changes, plans, data tables, and technical concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keylimesoda](https://clawhub.ai/user/keylimesoda)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to convert architecture notes, reviews, implementation plans, recaps, comparisons, and technical explanations into browser-viewable HTML diagrams, reports, and slide decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can include repository content, git history, conversation context, or OpenClaw memory details.

Mitigation: Review generated HTML for secrets, internal details, and inaccurate claims before saving it as a durable record or sharing it.

Risk: The share workflow can publish an HTML report publicly and may default to the latest diagram when no file is specified.

Mitigation: Pass an explicit file path and confirm the selected report contents before using the share workflow on sensitive projects.

Risk: Optional Vercel, CDN-backed diagrams, and AI-image workflows rely on external dependencies.

Mitigation: Use those optional paths only when the project permits the dependency; otherwise keep the generated HTML local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keylimesoda/skills/visual-explainer-openclaw)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [CSS patterns](references/css-patterns.md)
- [External libraries](references/libraries.md)
- [Responsive navigation](references/responsive-nav.md)
- [Slide patterns](references/slide-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Self-contained HTML files with optional Markdown summaries, shell commands, configuration guidance, and share-workflow JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local HTML reports to ~/.openclaw/workspace/diagrams; optional workflows can open files in a browser or publish selected HTML through Vercel.]

## Skill Version(s):

0.5.1-openclaw.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
