## Description:

Add new QQ Bot accounts to an existing OpenClaw Gateway instance. Use when a user provides a new QQ Bot appId and clientSecret (or app token) and wants to run multiple QQ bots under one Gateway. Covers both CLI and direct config edit approaches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[homer212416](https://clawhub.ai/user/homer212416)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add secondary QQ Bot accounts to an existing OpenClaw Gateway configuration, either through the OpenClaw CLI or by editing openclaw.json. It also guides optional routing of a new bot to a separate agent when independent persona and memory are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles QQ Bot appId and clientSecret values, and direct configuration edits may place credentials in plaintext.

Mitigation: Use SecretRef, the OpenClaw credential store, or a protected token file where possible, and check permissions on ~/.openclaw/openclaw.json before storing credentials there.

Risk: Secrets can be exposed if pasted into shell commands, chat messages, logs, or support transcripts.

Mitigation: Avoid pasting real secrets into commands or shared text; use protected files or credential references for operational use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configuration examples for QQ Bot accounts and optional multi-agent routing.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
