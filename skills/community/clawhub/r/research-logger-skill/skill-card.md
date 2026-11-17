## Description:

Research a topic via web search, auto-match a relevant GIF, and log structured notes to Bear using a configurable template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal productivity developers use this skill to research a topic, collect links and summary notes, match a GIF, and create a Bear note from a local template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Template replacement mixes user and web-fetched text into sed commands, creating a credible local command-execution risk.

Mitigation: Review before installing, avoid confidential topics or untrusted research targets, and fix template filling to treat replacement values as literal data with a safer templating implementation and preview or no-save mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/research-logger-skill)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands]

**Output Format:** [Markdown notes and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a Bear note with web-sourced summary, findings, links, GIF URL, tags, and action items; falls back to a local Markdown file when Bear is unavailable.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
