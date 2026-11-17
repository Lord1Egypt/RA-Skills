## Description:

Manage Twitch channel data, scores, and rankings from CLI. Use when rolling highlights, scoring streams, ranking metrics, tracking stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to manage a local, Twitch-labeled command-line log of channel activities, scores, rankings, stats, and related entries. It is suited to manual recordkeeping and export rather than Twitch API automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores command inputs and exported records locally under the user's home directory, which may expose sensitive entries on shared machines.

Mitigation: Do not enter Twitch tokens, passwords, private URLs, or personal identifiers; review local file permissions before use on shared systems.

Risk: The skill is an offline logging CLI and does not provide real Twitch API integration.

Mitigation: Use it for manual recordkeeping only, and verify any operational Twitch data against authoritative Twitch systems before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/twitch)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI stores local log files and can export entries as JSON, CSV, or plain text.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
