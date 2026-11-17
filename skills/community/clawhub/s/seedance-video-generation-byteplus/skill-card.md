## Description:

Generate AI videos using BytePlus Seedance API (International). Use when the user wants to: (1) generate videos from text prompts, (2) generate videos from images (first frame, first+last frame, reference images), or (3) query/manage video generation tasks. Supports Seedance 1.5 Pro (with audio & draft mode), 1.0 Pro, 1.0 Pro Fast, and 1.0 Lite models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackycser](https://clawhub.ai/user/jackycser)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and creative operators use this skill to generate, monitor, download, and manage BytePlus Seedance video generation tasks from text prompts or image inputs. The skill also provides guidance for optional delivery of generated videos through Feishu/Lark workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to BytePlus, and generated videos may be sent through Feishu when that optional workflow is used.

Mitigation: Use only approved non-sensitive inputs, avoid confidential prompts or private images, and confirm Feishu delivery is appropriate for the content.

Risk: The helper includes a local command-execution risk when downloaded videos are auto-opened on macOS.

Mitigation: Do not use the macOS auto-open download path until the helper replaces os.system with a non-shell file-opening call; download to a reviewed directory and open files manually.

Risk: The BytePlus API key grants access to video generation tasks and billing-relevant operations.

Mitigation: Keep ARK_API_KEY scoped, stored outside source files, rotated periodically, and available only to trusted runtime environments.

Risk: Generated video URLs expire and task history is temporary.

Mitigation: Download generated videos promptly and keep local copies of assets that need to be retained.

## Reference(s):

- [BytePlus Video Generation API](https://docs.byteplus.com/en/docs/ModelArk/Video_Generation_API)
- [BytePlus API Call Guide](https://docs.byteplus.com/en/docs/ModelArk/1366799)
- [BytePlus Model List and Pricing](https://docs.byteplus.com/en/docs/ModelArk/1330310)
- [BytePlus Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1587797)
- [Feishu Video Sending Guide](artifact/how_to_send_video_via_feishu_app.md)
- [ClawHub Skill Page](https://clawhub.ai/jackycser/skills/seedance-video-generation-byteplus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python CLI commands, curl examples, JSON API payloads, and downloaded MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY. The optional Feishu workflow requires Feishu app credentials configured outside the skill.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
