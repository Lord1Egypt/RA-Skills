## Description:

Guides an agent through turning an approved video previz and locked soundtrack into generated shots, then checking and handing off the footage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to choose code or AI generation per shot, plan and price video runs, make a low-cost first pass, and prepare checked footage and plates aligned to a locked soundtrack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance uses unpinned package commands.

Mitigation: Review package sources and pin versions before installing dependencies.

Risk: Project media or prompts may be sent to external generation providers.

Mitigation: Confirm the provider and its data terms, obtain the required project permissions, and approve costs before sending assets or prompts.

Risk: Security analysis is incomplete because some local references were unresolved.

Mitigation: Review the unresolved references and inspect the skill before deployment.

## Reference(s):

- [Project homepage](https://github.com/vargHQ/skills/tree/main/video-animate)
- [Animate a previz with AI video models](https://varg.ai/how-to/animate-a-previz-with-ai-video-models)
- [How to make a video with an AI agent in ten steps](https://varg.ai/how-to/make-a-video-in-ten-steps)
- [Shot routing](artifact/references/routing.md)
- [Model selection](artifact/references/models.md)
- [Drafts and takes](artifact/references/drafts-and-takes.md)
- [Sound and sync](artifact/references/sound-sync.md)
- [Post-ready handoff](artifact/references/post-ready.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Video, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown shot and run plans, JSON take sidecars, prompts, and Python/FFmpeg command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated video plates and take-check results; output depends on the user's project and selected generation services.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata; packaged frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
