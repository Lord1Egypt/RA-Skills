## Description:

Generate AI images, videos, voiceovers, and music, then compose them into captioned, multi-scene video renders through varg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use the skill to generate or edit visual and audio assets from prompts, and to compose them into captioned videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an unscoped updater and an incomplete scan, with two files only partially inspected.

Mitigation: Review the updater, package, version, and partially inspected files before installation or execution.

Risk: The security evidence reports persistent API-key storage.

Mitigation: Avoid automatic key storage; use a protected credential store and inspect setup behavior before providing a key.

Risk: Prompts and media may be sent to external services for generation.

Mitigation: Confirm that the content may be shared with those services, and avoid sending sensitive material.

## Reference(s):

- [varg.ai](https://varg.ai)
- [varg-ai skill release](https://clawhub.ai/vargai/skills/varg-ai)

## Skill Output:

**Output Type(s):** [Images, Video, Audio, Captions, Code, Shell commands]

**Output Format:** [Generated media files plus TSX or REST API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation output depends on the prompt, selected model, and render settings; service generation uses credits.]

## Skill Version(s):

2.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
