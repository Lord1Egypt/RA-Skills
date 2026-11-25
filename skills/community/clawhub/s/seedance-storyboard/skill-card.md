## Description:

End-to-end Asset-First storyboard-to-video pipeline on HotAPI using Seedream 5.0 (character/scene/prop locking) and Seedance 2.5 / 2.0 (reference-to-video, draft-first 480p preview, 1080p finalize, and offline HTML review board). Use for multi-shot AI short dramas, consistent-character video generation, or executing exported project_bundle.json manifests to real media assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dikese411980](https://clawhub.ai/user/dikese411980)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to turn structured multi-shot storyboards into consistent reference images, video clips, and a reviewable production board through HotAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supplied manifest may cause unintended local file uploads or output writes, or request remote media.

Mitigation: Review manifests and referenced paths before execution, use non-sensitive files in an isolated working directory, and check output destinations.

## Reference(s):

- [HotAPI OpenAPI documentation](https://api.hotapi.ai/docs/json)
- [HotAPI model catalog](https://hotapi.ai/en/docs/models)
- [HotAPI pricing](https://hotapi.ai/en/pricing)
- [Server-resolved GitHub source](https://github.com/Dikese411980/hotapi-skill/tree/main/seedance-storyboard)
- [ClawHub skill listing](https://clawhub.ai/dikese411980/skills/seedance-storyboard)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Images and video, HTML]

**Output Format:** [Storyboard JSON, generated image and video files, and an offline HTML review board]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates reusable reference assets and rendered clips for storyboard segments.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
