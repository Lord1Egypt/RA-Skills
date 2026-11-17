## Description:

Connect Codex, Claude Code, or another shell-capable assistant to ZiggsAI without host MCP support. Use for Ziggs inbox, tasks, messages, shared context, artifacts, and agreements through the session-aware Ziggs CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwook-ziggs](https://clawhub.ai/user/kiwook-ziggs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Ziggs users can use a shell-capable assistant to read inbox items and work with tasks, messages, shared context, artifacts, and agreements through the Ziggs CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials or access may be exposed or used beyond the intended workspace.

Mitigation: Keep credentials private, never paste them into chat, and confirm or narrow the selected workspace before acting.

Risk: Messages or agreement actions can affect other people or shared work.

Mitigation: Review the target and content, and confirm the person's authority before sending messages or taking agreement actions.

## Reference(s):

- [Ziggs CLI on ClawHub](https://clawhub.ai/kiwook-ziggs/skills/ziggs-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text, JSON]

**Output Format:** [Session-aware Ziggs CLI commands and JSON response envelopes, with task or communication content as applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available operations and results depend on the user's Ziggs credentials, workspace access, and requested task.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
