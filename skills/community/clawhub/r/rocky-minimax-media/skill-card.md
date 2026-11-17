## Description:

MiniMax media generation plugin for images, video, text-to-speech, and music with interactive model and voice selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockytian-top](https://clawhub.ai/user/rockytian-top)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure MiniMax access and invoke media generation workflows for images, videos, TTS audio, and music from an agent environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled executable scripts expose a hardcoded MiniMax API key and may mishandle user-entered credentials.

Mitigation: Do not install until hardcoded credentials are removed, heredocs are quoted safely, and any exposed MiniMax key is rotated.

Risk: Installation writes MiniMax credentials into local OpenClaw configuration.

Mitigation: Use only a user-owned API key, review local config changes before running the skill, and document where secrets are stored.

Risk: The bundled generate.sh script is specifically called out as unsafe in server security guidance.

Mitigation: Avoid using generate.sh unless it has been reviewed and fixed.

## Reference(s):

- [MiniMax developer platform](https://platform.minimaxi.com/)
- [MiniMax API base URL](https://api.minimaxi.com)
- [OpenClaw](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/rockytian-top/skills/rocky-minimax-media)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions with bash and JSON snippets; generated outputs may include image, video, TTS audio, or music files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, bash, OpenClaw configuration, and a user-provided MiniMax API key.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and manifest report 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
