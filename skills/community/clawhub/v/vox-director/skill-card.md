## Description:

Vox Director helps an agent turn a single topic into a Vox-style paper-collage explainer or ad video by drafting the beat map, prompts, motion plan, narration, music, captions, and assembly commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alisa0808](https://clawhub.ai/user/alisa0808)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and marketing teams use this skill to plan and assemble short narrated collage-style explainer or advertising videos from a topic, product, or person. The workflow covers story beats, visual style selection, generation prompts, voice-over, music, captions, and final ffmpeg assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-person, celebrity, logo, or brand workflows may create rights, consent, or publication risks.

Mitigation: Use those workflows only with clear rights and consent, and review generated outputs carefully before publishing.

Risk: The workflow uses Atlas Cloud for generated media assets.

Mitigation: Install only if Atlas Cloud use is acceptable for the project, and avoid submitting sensitive or restricted content.

Risk: The inspected package appears incomplete because it references scripts and reference files that were not present in the artifact.

Mitigation: Verify that all required scripts and references are available before relying on the automated workflow.

Risk: A default watermark may be unsuitable for publication.

Mitigation: Remove or explicitly approve any watermark before publishing generated videos.

## Reference(s):

- [Server-resolved source repository](https://github.com/Alisa0808/vox-director)
- [ClawHub skill page](https://clawhub.ai/alisa0808/skills/vox-director)
- [Atlas Cloud model catalog](https://api.atlascloud.ai/api/v1/models)
- [Atlas Cloud API keys](https://www.atlascloud.ai/console/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of video project files and a final MP4 when required dependencies, scripts, credentials, and user approvals are available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
