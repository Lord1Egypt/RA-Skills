## Description:

Creates a 9:16 faceless Reel from a topic or script by drafting a hook-driven script, preparing a teleprompter, timing the user's recorded voice, planning mixed AI visuals, and delivering a mute base video plus voice, cards, and an edit plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to turn a topic or existing script into a short faceless social video while keeping the user off camera and using their own recorded voice. The workflow is intended for explainer-style Reels, not talking-head videos, VSLs, or carousels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can use local facial photos and send them to an external video generation service without a dedicated consent step.

Mitigation: Require the publisher to remove the avatar photo path for this faceless workflow or add explicit opt-in consent that names the photo, recipient, purpose, and retention expectations before upload.

Risk: External tooling and service behavior can affect generated assets and delivery expectations.

Mitigation: Pin or preinstall required tools and clearly communicate that OpenClaw mode produces a mute base video plus separate voice and PNG assets.

## Reference(s):

- [Clip Director reference](reference/clip-director.md)
- [ClawHub skill page](https://clawhub.ai/formula100k/skills/reel-faceless-f100k)
- [F100K publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, plain text, JSON, shell commands, and generated media assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a mute 9:16 base video, the user-provided voice file, PNG card or pixel assets, and a timing plan for assembly in CapCut or Edits.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
