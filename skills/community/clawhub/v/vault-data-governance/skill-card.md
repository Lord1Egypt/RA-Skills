## Description:

Defines a data governance workflow for agents to audit, clean, deduplicate, and archive collected, reviewed, and research data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[managernet](https://clawhub.ai/user/managernet)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and team operators use this skill to standardize daily data governance across shared workspaces, including audit triggers, archival rules, deduplication, and cleanup reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to move files across team workspaces during cleanup.

Mitigation: Require a dry-run report, explicit allowlisted paths, and owner review before moving files.

Risk: The skill includes repository commit and push steps after cleanup.

Mitigation: Require secret scanning of staged content and separate human confirmation before commit or push.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/managernet/skills/vault-data-governance)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with shell command examples and a cleanup report template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to report archived, duplicate, and retained file counts.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
