## Description:

Monitors OpenClaw agent sessions, token usage, runtime metadata, and active-session status with text, Feishu card, and optional web dashboard views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youhaveamydream-spec](https://clawhub.ai/user/youhaveamydream-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw runtime health, token consumption, and active agent sessions, and to share concise status updates in Feishu when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status outputs can disclose operational metadata including token usage, active session labels, node/channel, model, OS, and runtime.

Mitigation: Use the Feishu card output only in trusted chats and review status content before sharing outside the operating team.

Risk: The optional web dashboard may need hardening before exposure beyond a local trusted environment.

Mitigation: Run the dashboard only on trusted local networks unless access control, transport security, and data handling have been reviewed.

## Reference(s):

- [OpenClaw Dashboard ClawHub page](https://clawhub.ai/youhaveamydream-spec/skills/xc-openclaw-dashboard)
- [Publisher profile](https://clawhub.ai/user/youhaveamydream-spec)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Author link from artifact](https://github.com/xc66o)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Plain text and Markdown status summaries, Feishu interactive-card JSON, and optional HTML dashboard output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw status data and may expose operational metadata such as token usage, active session labels, node/channel, model, OS, and runtime.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
