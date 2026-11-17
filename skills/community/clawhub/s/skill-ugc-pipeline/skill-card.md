## Description:

End-to-end AI UGC video pipeline that turns product information into a spoken script, voiceover, Aurora talking-head video, Kling product B-roll, Whisper-synced captions, UGC-style avatar filtering, and a final MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to assemble a user-generated-content video workflow for product ads, including script generation, voiceover, avatar video, product B-roll, captions, and post-processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product details, avatar photos, product images, voice or audio, and captions may be sent to OpenAI, ElevenLabs, and fal.ai.

Mitigation: Do not use sensitive personal images, confidential product material, or regulated data unless those providers and account settings are approved for that use.

Risk: Generated UGC-style product videos can misstate product qualities if prompts, scripts, or captions are not reviewed.

Mitigation: Review generated scripts, captions, and final videos before publication, especially for product claims and endorsement context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-ugc-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash command examples and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent or developer through a multi-step video pipeline; generated media depends on local scripts, API credentials, third-party services, and ffmpeg processing.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
