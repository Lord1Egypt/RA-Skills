## Description:

Uptimecheck checks URLs and API endpoints for availability, response time, and HTTP status, with batch checks, optional JSONL history, and configurable timeouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, and operations teams use this skill to check whether websites and API endpoints are responding and to capture response-time history for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound network checks to user-provided URLs.

Mitigation: Use it only for endpoints you are authorized to test and avoid URL lists from untrusted sources.

Risk: Saved history can retain URLs containing sensitive query strings or private hostnames.

Mitigation: Do not save checks for URLs that include API keys, signed parameters, session tokens, or internal hostnames.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogue-agent1/skills/uptimecheck)
- [Publisher profile](https://clawhub.ai/user/rogue-agent1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and text status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save optional local JSONL history under the user's home directory when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
