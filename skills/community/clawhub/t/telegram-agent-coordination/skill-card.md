## Description:

Provides a strict role-based protocol for coordinating multiple AI agents in a Telegram group chat with sender validation, turn-taking, blocker escalation, and mission lifecycle control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiril-shturman](https://clawhub.ai/user/kiril-shturman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate COO and worker bots in a shared Telegram group without free-form bot chatter, runaway loops, or unclear mission ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The protocol does not enforce Telegram access controls by itself.

Mitigation: Configure Telegram-side permissions and explicit sender allowlists before using the protocol with real bots.

Risk: Multiple bots in one chat can trigger loops or respond to malformed messages if the protocol is not followed.

Mitigation: Use the defined sender validation rules, visible message prefixes, and strict turn-taking before adding status checks or blockers.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown protocol guidance with message labels and role rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, tool invocation, or data collection is requested by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
