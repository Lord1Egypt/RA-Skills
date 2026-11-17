## Description:

A QQ bot persona-management skill that lets OpenClaw use separate personas for private chats, group chats, and specific OpenIDs without changing personas for other channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdwdwd000](https://clawhub.ai/user/wdwdwd000)

### License/Terms of Use:

MIT

## Use Case:

External developers and QQ bot operators use this skill to manage per-session OpenClaw personas for QQ private chats, group chats, and OpenID-specific conversations. It is intended for installations where persona behavior must be isolated from other chat channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent QQ bootstrap hook that can replace trusted persona instructions.

Mitigation: Enable it only for deployments where administrators explicitly want QQ-session persona replacement, and review persona files before use.

Risk: Persona configuration can read local files into prompts through file-based persona paths.

Mitigation: Keep personas.json and persona files writable only by trusted administrators, and avoid absolute file paths.

Risk: Hook logs may contain session and OpenID metadata.

Mitigation: Treat hook.log as sensitive, restrict file permissions, and rotate or delete logs according to local privacy policy.

Risk: Some persona rules may instruct the assistant to hide or deny its AI identity.

Mitigation: Remove persona rules that hide AI identity before deployment.

## Reference(s):

- [Qqbot Persona on ClawHub](https://clawhub.ai/wdwdwd000/skills/qqbot-persona)
- [OpenClaw Hooks Documentation](https://docs.openclaw.ai/hooks)
- [OpenClaw SOUL.md Persona Guide](https://docs.openclaw.ai/soul)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown persona text and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Injects persona instructions into QQ agent bootstrap context based on configured channel and OpenID matching.]

## Skill Version(s):

1.0.0 (source: clawhub.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
