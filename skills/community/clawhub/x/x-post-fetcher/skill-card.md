## Description:

Automates a browser workflow to fetch publicly visible X posts from a specified user and generate a Markdown summary report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to collect publicly visible X posts for a target account, summarize post activity, and save a local Markdown report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login examples may expose X credentials if an agent is asked to type passwords or recovery details.

Mitigation: Have the user enter credentials, MFA codes, and recovery details directly in the visible isolated browser window, and clear or revoke the isolated X session when finished.

Risk: Collected post summaries may include sensitive or misleading content from X even when posts are publicly visible.

Mitigation: Review generated Markdown reports before sharing or using them in downstream decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/x-post-fetcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with browser automation command examples and summarized post data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved to the user's local workspace; the skill uses an isolated browser session for X access.]

## Skill Version(s):

1.0.2 (source: release evidence and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
