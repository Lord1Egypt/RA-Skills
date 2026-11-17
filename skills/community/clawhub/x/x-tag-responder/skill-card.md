## Description:

Detects when a human tags their AI familiar in someone else's X/Twitter thread, fetches full conversation context, infers intent, crafts an appropriate reply, and handles X API reply-chain restrictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-lwatcher](https://clawhub.ai/user/m-lwatcher)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and their agents use this skill to inspect an X/Twitter thread where the user tagged the agent, infer the requested action, draft a concise reply, and handle posting or fallback options with user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts can perform broader background automation than the skill description suggests, including automatic likes, replies, and gateway restarts.

Mitigation: Review or remediate before installation; remove unrelated daemon behavior and keep posting actions in draft-only mode unless the user explicitly approves each action.

Risk: Reply generation may send tweet context to Gemini before a public reply is posted.

Mitigation: Disclose Gemini processing to the user and require confirmation before using generated text with any real X account.

Risk: Shell-string command execution in bundled scripts can increase command execution risk.

Mitigation: Replace shell-string execution with argument-array APIs and review all command inputs before enabling automation.

## Reference(s):

- [X Tag Responder ClawHub listing](https://clawhub.ai/m-lwatcher/skills/x-tag-responder)
- [m-lwatcher publisher profile](https://clawhub.ai/user/m-lwatcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise draft reply text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft replies target X's short-form posting constraints and should be reviewed before public posting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
