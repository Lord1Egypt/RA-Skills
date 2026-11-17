## Description:

Generate videos using Seedance models. Invoke when user wants to create videos from text prompts, images, or reference materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warm-wm](https://clawhub.ai/user/warm-wm)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and content-generation agents use this skill to create short videos from text prompts, first or last frame images, and reference images, videos, or audio through Seedance models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be persisted in plaintext workspace files if credential setup guidance is followed without review.

Mitigation: Use a dedicated low-privilege video API key and configure it through a secret manager or protected runtime environment.

Risk: Prompts, private media, signed URLs, or internal URLs are sent to the configured external video generation API.

Mitigation: Avoid submitting sensitive prompts, private media, signed URLs, or internal URLs unless the deployment has approved that data flow.

Risk: Generated video tasks can remain pending after polling timeout.

Mitigation: Use the returned task ID to query status later and report pending jobs clearly to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/warm-wm/skills/video-generate)
- [Implementation script](scripts/video_generate.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown with video URLs, optional local file paths, and JSON status objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated video URLs, task IDs for pending jobs, and error details.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
