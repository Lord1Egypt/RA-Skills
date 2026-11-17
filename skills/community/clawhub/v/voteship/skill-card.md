## Description:

Manage feature requests, votes, roadmaps, and changelogs with VoteShip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattkilmer](https://clawhub.ai/user/mattkilmer)

### License/Terms of Use:


## Use Case:

Developers, product teams, and support teams use this skill to manage VoteShip feature requests, votes, roadmaps, changelogs, analytics, AI-assisted triage, and webhook configuration from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external MCP server receives a VoteShip API key with broad project authority.

Mitigation: Use the least-privileged key available and install only after trusting or auditing the VoteShip MCP package.

Risk: Configured admin operations can make live writes, deletes, revenue updates, AI processing requests, and webhook changes.

Mitigation: Confirm destructive or privileged actions before execution and use public read-only mode when admin access is not needed.

Risk: AI ingestion may process sensitive customer, support, or credential data submitted through feedback workflows.

Mitigation: Avoid sending raw sensitive customer or credential data into AI-assisted triage, extraction, planning, or summarization flows.

Risk: The install metadata references an unpinned external Node package.

Mitigation: Prefer a pinned and audited package version for production deployments.

## Reference(s):

- [VoteShip Documentation](https://voteship.app/docs)
- [VoteShip App](https://voteship.app)
- [ClawHub VoteShip Skill](https://clawhub.ai/mattkilmer/skills/voteship)
- [mattkilmer ClawHub Profile](https://clawhub.ai/user/mattkilmer)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline tool, API, and environment-variable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live VoteShip reads and writes through the external MCP server when configured with project credentials.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
