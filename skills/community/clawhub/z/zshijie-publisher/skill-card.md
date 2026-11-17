## Description:

Operates the Z视介 publishing API from OpenClaw by guiding QR-code login and publishing or editing 图文 and 短视频 content from JSON payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkbwfi](https://clawhub.ai/user/jkbwfi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators with authorized Z视介 accounts use this skill to authenticate by QR code and publish or update live article and short-video content from prepared JSON payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or edit live Z视介 content through an authenticated account.

Mitigation: Use it only with an authorized account and review payload JSON before running publish or edit commands.

Risk: Reusable login sessions may be stored in a local session file.

Mitigation: Store the session file in a private location with restrictive permissions and delete it after use.

Risk: Publishing can use a plaintext HTTP host or a caller-supplied host override.

Mitigation: Avoid untrusted networks and do not use arbitrary --base-url values or custom contracts with a saved session.

## Reference(s):

- [Z视介 API Notes](artifact/references/zshijie-api.md)
- [Usage Guide](artifact/references/usage.md)
- [Z视介 API Contract](artifact/references/zshijie-api.json)
- [Z视介 Creator Login](https://mp.cztv.com/#/login)
- [ClawHub Release Page](https://clawhub.ai/jkbwfi/skills/zshijie-publisher)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local QR HTML/PNG files and a session file during login.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
