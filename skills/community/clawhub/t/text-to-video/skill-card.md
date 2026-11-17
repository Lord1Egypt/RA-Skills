## Description:

Turns user-approved text and local media into a short video plan, editable HTML composition, and MP4 using local tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minibeanai](https://clawhub.ai/user/minibeanai)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, educators, and developers use this skill to turn approved scripts into short, locally rendered videos with editable storyboards and compositions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local media generation writes project files and runs installed tools.

Mitigation: Confirm the dedicated project path before generation or rendering and use only user-approved local inputs and preinstalled tools.

Risk: Optional online speech or asset services could transmit script text or search terms.

Mitigation: Keep the default local-only workflow; use an independently reviewed integration only after explicit consent naming the destination and data shared.

## Reference(s):

- [ClawHub text-to-video release](https://clawhub.ai/minibeanai/skills/text-to-video)
- [HyperFrames handoff](references/hyperframes-handoff.md)
- [Local speech synthesis](references/tts-providers.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Storyboard Markdown, HTML composition, local media files, and rendered MP4]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a user-reviewed video plan, project assets, narration audio, key-frame previews, and a short MP4.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
