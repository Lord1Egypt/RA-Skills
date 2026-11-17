## Description:

V.A.R. Protocol helps agents enforce Versioning, Archiving, and Rollback discipline for long-lived assets and multi-step delivery work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wewehg](https://clawhub.ai/user/wewehg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and agent operators use this skill to keep risky edits recoverable through explicit version labels, backups, changelogs, and rollback anchors. It is intended for codebases, websites, documents, prompts, configuration, brand assets, and multi-agent delivery work where preserving a stable baseline matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may create or preserve extra local copies during larger edits.

Mitigation: Confirm backup locations, retention expectations, and cleanup needs before applying strict mode.

Risk: The full protocol can add unnecessary process overhead for small one-off changes.

Mitigation: Use a lighter posture or tell the agent not to apply strict mode when recoverability requirements are low.

## Reference(s):

- [V.A.R. Protocol Reference](artifact/references/protocol.md)
- [V.A.R. Protocol on ClawHub](https://clawhub.ai/wewehg/skills/var-protocol)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional code, shell command, configuration, and delivery-summary snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the agent to name versions, preserve rollback anchors, create or retain backups, and include concise changelog notes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
