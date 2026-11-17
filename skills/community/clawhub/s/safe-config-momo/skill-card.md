## Description:

Safely modifies OpenClaw configuration files by backing up the current file, previewing redacted changes, validating JSON, and requiring explicit user confirmation before edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to plan and perform changes to ~/.openclaw/openclaw.json, including model, channel, tool, and skill configuration updates. It guides them through backup, redacted preview, JSON validation, explicit confirmation, and post-change verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that redaction scripts can leave real API keys visible in previews.

Mitigation: Do not paste generated previews into chats, tickets, logs, or other shared locations unless credentials have been independently scrubbed.

Risk: Config edits and gateway restarts can disrupt OpenClaw if an incorrect setting is applied.

Mitigation: Review proposed changes, keep a timestamped backup, validate JSON before and after edits, and require clear confirmation before applying changes.

Risk: Provider connectivity tests and command examples may make external requests or expose credential patterns.

Mitigation: Use non-secret test tokens for connectivity checks and avoid logging or sharing command output that could contain credentials.

## Reference(s):

- [OpenClaw Configuration Examples](references/examples.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Release](https://clawhub.ai/justaboyhai-wq/skills/safe-config-momo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted previews and config-edit command sequences; users should independently scrub secrets before sharing outputs.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
