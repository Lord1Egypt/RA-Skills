## Description:

目录结构转可折叠、可搜索、可点击的交互式HTML目录树.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and technical teams use this skill to turn pasted directory listings into interactive HTML views for code repositories, documentation sets, audits, and storage analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated directory views may expose sensitive names, internal paths, customer identifiers, or architecture details from the input listing.

Mitigation: Review and redact the directory listing before sharing generated HTML outside the intended audience.

Risk: Chinese-language instructions and labels may limit usability for teams that require another language.

Mitigation: Confirm the intended audience can use the Chinese-language workflow or localize labels before deployment.

Risk: The bundled HTML templates are placeholders, so runtime output quality depends on the agent generating the final HTML from the documented patterns.

Mitigation: Inspect generated HTML before distribution and verify the selected mode, styling, and interactions work as expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/tree-view-craft)
- [Project homepage](https://github.com/wwbwin/clawhub-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Single-file HTML with inline CSS and JavaScript, plus supporting guidance in Markdown or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact describes seven display modes; current HTML template files are placeholders awaiting implementation.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
