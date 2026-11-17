## Description:

Slacrawl helps agents search local Slack archives, check archive freshness, inspect threads and DMs, and run read-only SQL counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw](https://clawhub.ai/user/openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and employees with local Slack archive access use Slacrawl to answer questions from archived Slack data, check freshness, refresh archives when needed, and report bounded message slices, counts, and date spans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The slacrawl binary can access local Slack archive data and, when explicitly used, Slack API tokens.

Mitigation: Install only in environments approved for Slack data access, and do not assume Slack tokens are present or required for every workflow.

Risk: Installing the Go module with @latest can introduce unreviewed changes in environments with sensitive Slack data.

Mitigation: Prefer a pinned, reviewed slacrawl version for sensitive or controlled deployments.

## Reference(s):

- [Slacrawl GitHub repository](https://github.com/openclaw/slacrawl)
- [Slacrawl ClawHub release page](https://clawhub.ai/openclaw/skills/slacrawl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and SQL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workspace and channel names, absolute date spans, counts, and token or source limits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
