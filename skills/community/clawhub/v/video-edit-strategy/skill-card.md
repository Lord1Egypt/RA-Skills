## Description:

Analyzes video materials and user intent to produce a structured JSON editing strategy covering storyboard, timeline, transitions, audio, text overlays, and downstream execution steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[se7enelk](https://clawhub.ai/user/se7enelk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and video automation agents use this skill to turn short-video intent and media inputs into an executable edit plan. It is useful when the user provides media paths or asks for a short-video editing strategy rather than direct rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media probing can touch unintended local files if user-provided paths are ambiguous or untrusted.

Mitigation: Ask for clarification before probing unclear paths and validate media paths before passing them to downstream tools.

Risk: Downstream executors could over-trust generated execution steps as arbitrary shell instructions.

Mitigation: Allow only expected media actions and parameters, avoid arbitrary shell command execution, and run each job in a private temporary directory.

Risk: Generated editing plans may not match the user's creative intent or source media constraints.

Mitigation: Review the timeline, materials, audio, text overlays, and execution plan before rendering final media.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/se7enelk/skills/video-edit-strategy)
- [Strategy Schema](artifact/strategy-schema.md)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [JSON with a brief natural-language editing rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning output only; downstream skills or tools perform media probing and rendering.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
