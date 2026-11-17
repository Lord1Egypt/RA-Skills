## Description:

Creates a Topaz-enhanced Instagram carousel from a popular-picks page by pairing destination photos with Reddit quotes and subreddit attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Content operators and social media agents use this skill to turn popular-picks pages into Instagram carousel posts with destination photos, Reddit quote overlays, Topaz image enhancement, and publication steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload generated images to external services, push repository changes, and publish branded content to Instagram without a clear approval checkpoint.

Mitigation: Require human review of every generated image, caption, destination account, repository change, public URL, and Instagram publication action before upload, push, or publish.

Risk: The workflow uses Topaz, GitHub/repository, and Instagram credentials and can expose processed images through external hosting or social media.

Mitigation: Install only when those credentialed actions are intended, scope credentials to the minimum needed access, and treat external image processing and hosting as public or persistent unless verified otherwise.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/psyduckler/skills/reddit-quote-topaz)
- [Topaz Labs image enhance API](https://api.topazlabs.com/image/v1/enhance)
- [Topaz Labs async image enhance API](https://api.topazlabs.com/image/v1/enhance/async)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, API Calls, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands, JSON manifest examples, image file outputs, caption text, and publication URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates temporary local image assets and a manifest, may upload images to repository hosting, and may publish a carousel to Instagram.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
