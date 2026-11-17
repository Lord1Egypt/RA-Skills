## Description:

A Tekan AI creation skill that lets agents generate and edit videos, images, digital avatar videos, ecommerce visuals, speech, and voice clones from natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tekancn](https://clawhub.ai/user/tekancn)

### License/Terms of Use:

Apache 2.0

## Use Case:

External creators, marketers, ecommerce operators, and agents use this skill to turn natural-language requests and provided media into generated videos, edited images, digital avatar videos, product visuals, text-to-speech audio, voice clones, and organized board outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Tekan account and saved reusable credentials.

Mitigation: Install only for trusted agents and environments, review local credential storage, and log out or revoke access when no longer needed.

Risk: Generation workflows may consume paid credits, especially bulk ecommerce image or multi-step media jobs.

Mitigation: Confirm user intent, scope, and estimated cost before high-volume or automatic generation.

Risk: Voice cloning, watermark removal, and media transformation can be sensitive or rights-dependent.

Mitigation: Require explicit user confirmation and appropriate rights or consent before running these workflows.

Risk: Board and voice management commands can delete or modify account resources.

Mitigation: Confirm destructive operations and target identifiers before executing deletion or update commands.

Risk: The skill includes rigid messaging requirements that could override normal user-facing communication expectations.

Mitigation: Review messaging behavior during integration and keep platform safety, consent, and communication policies authoritative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tekancn/skills/tekan-skill)
- [Tekan](https://tekan.cn)
- [Agent Skills specification](https://agentskills.io/specification)
- [Avatar4](references/avatar4.md)
- [Video Gen](references/video_gen.md)
- [AI Image](references/ai_image.md)
- [Remove BG](references/remove_bg.md)
- [Product Avatar](references/product_avatar.md)
- [Text2Voice](references/text2voice.md)
- [Voice](references/voice.md)
- [Ecommerce Image](references/ecommerce_image.md)
- [Board](references/board.md)
- [Auth](references/auth.md)
- [User](references/user.md)
- [Error Handling](references/error_handling.md)
- [Model Mapping](references/model_mapping.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown status messages with command-line invocations and generated media, task, or board URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May consume Tekan credits and create, update, or delete Tekan account resources such as boards, tasks, generated media, and cloned voices.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
