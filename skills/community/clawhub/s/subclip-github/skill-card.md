## Description:

Inspect a connected GitHub MCP account and its repositories, stars, commits, releases, and date-range changelogs. Use when a creator asks Subclip AI to discover or summarize GitHub activity; repository mutations remain separately confirmation-gated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Creators use Subclip AI to inspect connected GitHub profiles and repositories, review stars and repository activity, and summarize commits, pull requests, releases, or changelogs over a requested date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected GitHub access can expose repository information, and autonomous decisions could lead to unintended changes.

Mitigation: Use read-only access for reads where available. Before any repository change, confirm the GitHub account, repository, action, and submitted fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prosamik/skills/subclip-github)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown summaries and repository information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository metadata, date-bounded activity summaries, pull request details, and links to source records.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
