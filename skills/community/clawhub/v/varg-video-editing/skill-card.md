## Description:

Routes existing-video editing tasks to suitable local or hosted tools and outlines workflows for cuts, captions, reframing, dubbing, AI edits, upscaling, quality checks, and editor handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video editors use the skill to choose a suitable service and plan safe, reviewable edits to existing footage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted editing workflows may share footage through public URLs, which can expose sensitive media.

Mitigation: Check the receiving service and approve the exposure before sharing; avoid public URLs for sensitive footage.

Risk: The installer example is unpinned.

Mitigation: Pin installation to a reviewed version.

Risk: The security scan is incomplete because one local reference could not be resolved.

Mitigation: Review the unresolved reference and treat the scan as incomplete until it is resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vargai/skills/varg-video-editing)
- [Editing services guide](https://skills.varg.ai/browse/skills/edit-services/)
- [Service reference table](artifact/references/services.md)
- [Editing practices](artifact/references/practices.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, JSON edit plans]

**Output Format:** [Markdown with commands, tool recommendations, and structured edit plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance and plans for editing existing footage; no fixed output length.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
