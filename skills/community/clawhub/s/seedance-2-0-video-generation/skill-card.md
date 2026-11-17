## Description:

Generate AI videos with ByteDance Seedance 2.0 from text prompts, image inputs, first and last frames, or chained long-video segments that preserve continuity through the previous segment's last frame.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liusaikang](https://clawhub.ai/user/liusaikang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create, monitor, download, and manage Seedance 2.0 video-generation tasks. It is especially suited for workflows that split videos longer than 15 seconds into sequential segments and reuse each completed segment's last frame as the next segment's first frame.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and selected local images may be sent to Volcengine/ByteDance infrastructure.

Mitigation: Use the skill only with inputs that are acceptable to share with that third-party service, and avoid confidential or sensitive content unless approved.

Risk: The helper can auto-open downloaded files on macOS through an unsafe shell call.

Mitigation: Avoid the download auto-open behavior on macOS until the helper uses a non-shell opener or removes automatic opening.

Risk: Task deletion or cancellation depends on a provided task ID.

Mitigation: Confirm task IDs before using delete operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liusaikang/skills/seedance-2-0-video-generation)
- [Publisher profile](https://clawhub.ai/user/liusaikang)
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local MP4 videos, PNG last-frame images, and sequence_manifest.json files when the helper is executed.]

## Skill Version(s):

1.0.1 (source: server release evidence, released 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
