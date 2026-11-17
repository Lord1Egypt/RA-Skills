## Description:

Web Slides helps agents create polished, mobile-friendly single-file HTML presentation decks from user outlines, structured content, or scene presets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to transform outlines, Markdown, or structured JSON into polished HTML slides for pitches, reports, launches, and presentations without API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional preview rendering can execute against generated HTML content in a local browser context.

Mitigation: Render previews only from trusted generated HTML, preferably in an isolated environment without private files or outbound network access.

Risk: Optional global npm installation can introduce supply-chain exposure if the package is not pinned and trusted.

Mitigation: Avoid global installation unless the preview renderer package and version are explicitly reviewed and trusted.

Risk: The security verdict is suspicious despite no specific risk findings being listed.

Mitigation: Review the skill before installation and scan the release artifact before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/web-pptx-generator)
- [Publisher Profile](https://clawhub.ai/user/tobewin)
- [Runtime](references/runtime.md)
- [Assembly Workflow](references/assembly-workflow.md)
- [Content Schema](references/content-schema.md)
- [Layout System](references/layout-system.md)
- [Theme Catalog](references/theme-catalog.md)
- [Quality Bar](references/quality-bar.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML/CSS/JavaScript code and optional JSON deck content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js for bundled scripts; optional preview rendering depends on a manually installed preview renderer.]

## Skill Version(s):

2.0.5 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
