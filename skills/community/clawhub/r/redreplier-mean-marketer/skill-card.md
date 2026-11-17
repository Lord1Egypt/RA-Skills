## Description:

A background accountability loop that surfaces fresh, high-scoring RedReplier lead opportunities and relays server-generated marketing nudges when the user has not approved or rejected the previous opportunity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarasshyn](https://clawhub.ai/user/tarasshyn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing operators use this skill to schedule RedReplier lead notifications, configure lead criteria, and triage surfaced opportunities. It is suited for agents that need to relay ready-to-send marketing accountability messages and opportunity links without rewriting or ranking leads locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to run as a recurring background job that uses a RedReplier token every 5 minutes and mutates lead or mention state.

Mitigation: Enable the schedule only when continuous polling is intended, use a dedicated limited token, confirm how to disable both the scheduler and the RedReplier loop, and always deliver any notify output instead of polling only to inspect it.

Risk: The skill depends on a bearer token that may be read from the environment or a local configuration file.

Mitigation: Keep the token out of command-line arguments and scheduler definitions, store configuration with restrictive permissions, and rotate or revoke the token if exposure is suspected.

Risk: Delivered opportunity links and messages are remote content from the service.

Mitigation: Treat links and messages as untrusted content and review opportunities before taking external marketing action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tarasshyn/skills/redreplier-mean-marketer)
- [Publisher profile](https://clawhub.ai/user/tarasshyn)
- [RedReplier homepage](https://redreplier.com)
- [RedReplier API host](https://ai.redreplier.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from CLI commands, with Markdown guidance and shell command examples in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The notify command emits user-facing text only when the service returns a message; the poll command emits raw JSON.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
