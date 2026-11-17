## Description:

Query historical Runway Aleph task status with the RunAPI CLI; this retired model does not accept new tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other RunAPI users can check the status of existing Runway Aleph task IDs without starting new tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an untrusted RunAPI CLI or Homebrew tap, or sharing unnecessary API credentials, can expose access.

Mitigation: Confirm the CLI and tap are trusted; prefer existing environment or saved CLI authentication over pasting API keys.

Risk: New requests to the retired model return HTTP 410, and a failed status query may leave task status unknown.

Mitigation: Query only existing task IDs; preserve the ID and report status-query errors rather than retrying task creation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/runapi-ai/skills/runapi-runway-aleph)
- [Runway Aleph model documentation](https://runapi.ai/models/runway-aleph.md)
- [RunAPI Runway provider overview](https://runapi.ai/providers/runway.md)
- [Runway Aleph SDK integration](https://github.com/runapi-ai/runway-aleph-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status lookup requires an existing task ID; results can be saved as JSON.]

## Skill Version(s):

0.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
