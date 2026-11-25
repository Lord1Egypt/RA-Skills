## Description:

Convert a project's native captions into an editable HyperFrames caption layer when the creator names a HyperFrames caption style or asks for HyperFrames/GSAP-designed captions. The HyperFrames layer becomes the source of truth for caption design; native captions are hidden, never deleted unless asked, and the word data stays in the layer variables. Do not use for ordinary subtitle correction or for native Dynamic Captions presets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and editing agents use this skill to turn existing caption words and timing into a styled, editable HyperFrames caption layer. It helps apply a chosen caption style while keeping native captions available for restoration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting native captions cannot be undone with the skill's restore action.

Mitigation: Keep the default reversible hide behavior; delete native captions only when explicitly requested and confirmed.

Risk: A caption layer can be hard to read over footage, overlap a face, or render alongside native captions.

Mitigation: Check representative frames, safe-zone placement, and native caption visibility after conversion; restore captions if needed.

Risk: Timing generated from synthetic speech may be approximate, and heavy caption styles can make exports slow or unsuitable on Linux software rendering.

Mitigation: Use native transcription for human speech or precise timing, prefer light styles, and inspect a short ranged export when requested.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/prosamik/skills/subclip-hyperframes-captions)
- [Publisher profile](https://clawhub.ai/user/prosamik)

## Skill Output:

**Output Type(s):** [Configuration, Guidance]

**Output Format:** [An editable HyperFrames caption layer in the project, with concise workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Copies caption words and project-time seconds into layer variables; native captions are hidden by default and remain restorable.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
