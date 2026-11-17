## Description:

Fetches public webpages with Scrapling, extracts main content, and converts HTML into Markdown using static, async, stealth, or dynamic browser fetching modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumiu8103-hue](https://clawhub.ai/user/yumiu8103-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to collect public webpage content as Markdown for summarization, analysis, indexing, or saved extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper can fetch user-supplied URLs, which may expose private networks or cloud metadata endpoints if run in a sensitive environment.

Mitigation: Run it in an isolated environment and provide only public URLs you trust.

Risk: The release was flagged as suspicious because documented public-web constraints do not fully match runtime fetching behavior.

Mitigation: Review the skill carefully before installation and validate behavior against the security guidance before production use.

Risk: Dependency behavior may change or introduce unexpected browser and network behavior.

Mitigation: Pin or review dependencies before following the install commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yumiu8103-hue/skills/web-markdown-scraper)
- [Artifact README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON to stdout with per-page Markdown content and optional saved .md files plus index.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-URL success status, title, HTTP status when available, Markdown length, output file paths, and exact error strings on failure.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
