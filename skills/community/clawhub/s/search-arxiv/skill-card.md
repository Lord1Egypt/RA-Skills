## Description:

Search arXiv for research papers matching the user's query. Use when the user asks to use arXiv for this purpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to have an agent open or reuse Brave and search arXiv for papers matching a query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research search terms are sent to arXiv and may reveal confidential research interests.

Mitigation: Avoid confidential queries when those terms should not leave the user's environment.

Risk: The skill may open or reuse Brave tabs and sessions.

Mitigation: Review the visible browser context before use; the skill is scoped to navigation and search, stops at login, and does not handle credentials or modify accounts.

## Reference(s):

- [arXiv Search](https://arxiv.org/search/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/search-arxiv)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Text guidance for browser navigation and search verification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's search query to open arXiv search results in Brave; no credential entry or account modification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
