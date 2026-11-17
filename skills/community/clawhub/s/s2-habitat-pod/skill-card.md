## Description:

Assigns a deterministic local habitat, avatar profile, and Pod ID for an OpenClaw agent, then emits Markdown with remote Space2 image URLs and writes a local JSON state file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to initialize a small local identity and habitat profile for an agent, including a deterministic Pod ID, coordinate, and chosen avatar. It is useful when a visible Markdown profile and local state record are desired for a ClawHub/OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a local JSON state file in the current working directory.

Mitigation: Run it from an intended workspace and inspect the generated s2_matrix_data directory before preserving or sharing it.

Risk: Rendered Markdown fetches remote avatar images from a Space2 CDN.

Mitigation: Render the Markdown only in environments where external image requests are acceptable.

Risk: The generated Markdown contains agent-directed text and embeds user-provided names in HTML-like output.

Mitigation: Treat generated Markdown as display content, review it before use, and avoid pasting it into agent instruction or automation contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-habitat-pod)
- [Publisher profile](https://clawhub.ai/user/spacesq)
- [Space2.world](https://space2.world)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Console text, generated Markdown, and a local JSON state file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for an agent name and avatar choice; generated Markdown includes remote image URLs.]

## Skill Version(s):

1.0.4 (source: manifest.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
