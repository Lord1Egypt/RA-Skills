## Description:

Official Topview AI client. Generate videos, images, avatars, and TTS audio via the Topview API. All network calls go to *.topview.ai only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topviewai](https://clawhub.ai/user/topviewai)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and external users use this skill to let an agent create Topview media assets from natural-language requests, including AI images, video clips, talking avatars, text-to-speech audio, voice cloning, background removal, product showcase images, and board organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account credentials and user files.

Mitigation: Review before installing for sensitive media or account data, use a Topview account you are comfortable connecting, and prefer an isolated environment.

Risk: Local files may be uploaded during generation workflows.

Mitigation: Pass only files intended for Topview processing and avoid using the skill with confidential media unless that transfer is acceptable.

Risk: Credentials are saved under the user's home directory.

Mitigation: Protect the local environment and remove saved credentials when the skill no longer needs account access.

Risk: Network destinations may be less restricted than the documentation claims.

Mitigation: Review the skill before deployment and run it in an environment whose outbound network access is appropriate for the data being processed.

Risk: Webhook URLs can expose generated task events or results to external destinations.

Mitigation: Use only webhook URLs that you control.

## Reference(s):

- [Topview homepage](https://www.topview.ai)
- [ClawHub skill page](https://clawhub.ai/topviewai/skills/topview)
- [AI Image module](references/ai_image.md)
- [Auth module](references/auth.md)
- [Avatar4 module](references/avatar4.md)
- [Board module](references/board.md)
- [Error handling guide](references/error_handling.md)
- [Product Avatar module](references/product_avatar.md)
- [Remove Background module](references/remove_bg.md)
- [Text-to-Voice module](references/text2voice.md)
- [User module](references/user.md)
- [Video Generation module](references/video_gen.md)
- [Voice module](references/voice.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Files]

**Output Format:** [Markdown guidance with inline shell commands, task identifiers, media URLs, and generated file references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Topview account and local credentials or TOPVIEW_UID plus TOPVIEW_API_KEY.]

## Skill Version(s):

0.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
