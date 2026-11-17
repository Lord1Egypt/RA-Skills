## Description:

Run a TinyFish automation agent against a URL and stream live progress events (STARTED / PROGRESS / COMPLETE) as one-line JSON events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bunsdev](https://clawhub.ai/user/bunsdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a TinyFish browsing automation against a target URL with a defined goal and consume streamed progress and completion events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The target URL, automation goal, and resulting browsing activity are sent to TinyFish under the user's TinyFish account.

Mitigation: Use only with approved targets and prompts; avoid secret-bearing URLs, internal systems, regulated data, and confidential prompts unless external sharing is approved.

Risk: The skill requires a TinyFish API key to call the external service.

Mitigation: Provide TINYFISH_API_KEY through a secure environment mechanism and avoid exposing it in command history, logs, or shared output.

## Reference(s):

- [TinyFish Agent API documentation](https://docs.tinyfish.ai/agent-api)
- [ClawHub skill page](https://clawhub.ai/bunsdev/skills/tinyfish-agent-run)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and newline-delimited JSON event output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streams STARTED, PROGRESS, and COMPLETE events from the TinyFish API as one JSON object per line.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
