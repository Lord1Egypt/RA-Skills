## Description:

Pre-publish privacy scan for ClawHub skills. Detects tokens, keys, credentials, .env secrets, personal info, and internal IPs before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill before publishing or updating ClawHub skills to scan for leaked secrets, personal information, internal IPs, and other privacy-sensitive content. It also guides the agent to present the full scan report and request explicit confirmation before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan reports can expose detected secret values in terminal output, chat, or logs.

Mitigation: Use the skill only on directories you are comfortable scanning, review output before sharing it, and prefer a revised version that redacts credential values.

Risk: Regex-based privacy scans can produce false positives or miss sensitive values outside the covered patterns.

Mitigation: Treat the scan as a pre-publish aid, then manually review findings and the target skill before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weidongkl/skills/skill-publish-vetter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell command snippets, scan report text, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include full scan reports; detected secret values can appear in terminal output or chat.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
