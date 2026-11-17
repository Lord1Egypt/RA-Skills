## Description:

Search X/Twitter with OAuth-backed xAI x_search; includes optional xso CLI companion guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leostehlik](https://clawhub.ai/user/leostehlik)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users can search X with the native xAI x_search tool, apply useful filters, and produce cited summaries. Terminal users can use the optional xso CLI for OAuth-backed searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search requests are sent to xAI, and the optional CLI stores OAuth state locally.

Mitigation: Authorize the CLI only if you trust xAI with your search queries, and protect access to the local authentication file.

Risk: The security assessment has medium confidence: two executable files received only partial analysis.

Mitigation: Review the release source and consider the assessment limits before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/leostehlik/skills/x-search-oauth)
- [Declared project homepage](https://github.com/LeoStehlik/x-search-oauth)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, JSON, Shell commands]

**Output Format:** [Cited Markdown summaries and search guidance; the optional CLI can emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cite original X post URLs and treat post content as untrusted external input.]

## Skill Version(s):

0.2.5 (source: frontmatter, CHANGELOG.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
