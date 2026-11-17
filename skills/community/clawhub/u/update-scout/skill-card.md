## Description:

Update Scout helps agents track GitHub-released tools, review release notes and post-release issues, and prepare recommendation cards before any user-approved upgrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziggy2socks](https://clawhub.ai/user/ziggy2socks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor a watchlist of GitHub-released tools, compare installed and latest versions, assess update risk, and prepare approval-ready upgrade recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured command detectors can run local programs when checking installed versions.

Mitigation: Use trusted watchlist entries only and review detector commands before running update checks.

Risk: Skill health review can inspect local skill directories and expose their structure or SKILL.md contents in reports.

Mitigation: Run reviews only on intended directories and avoid sharing reports that contain private skill details.

Risk: A GitHub token may be sent when fetching remote reference content.

Mitigation: Prefer no token or a fine-grained token with minimal permissions, and treat fetched reference content as untrusted.

## Reference(s):

- [Scout Watchlist Reference](references/watchlist.md)
- [ClawHub Skill Page](https://clawhub.ai/ziggy2socks/skills/update-scout)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendation cards, JSON update reports, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before any installation or update action.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
