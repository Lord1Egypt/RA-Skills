## Description:

Generates a 6-slide TikTok carousel with images and text, creates a draft post via Postiz API, and outputs a caption for review and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otman-ai](https://clawhub.ai/user/otman-ai)

### License/Terms of Use:


## Use Case:

Creators, marketers, and automation developers use this skill to generate TikTok carousel draft assets from a topic or persona, then review the caption and draft before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Postiz credentials and uploaded content can be sent to an arbitrary POSTIZ_API_URL configured in the runtime environment.

Mitigation: Review POSTIZ_API_URL before upload, leave it unset for the official endpoint when appropriate, and use a least-privileged Postiz API key.

Risk: Generated carousel images and captions may be uploaded unintentionally if the upload workflow is run on the wrong files.

Mitigation: Review generated images and captions before upload, and pass only intended image paths to the upload command.

Risk: Unpinned dependencies can change behavior across installs.

Mitigation: Pin and review dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/otman-ai/skills/tikto-automation)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with Python command examples, generated PNG image files, caption text, and optional Postiz draft response data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires environment variables for OpenAI image generation and optional Postiz draft upload; final publishing remains manual.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
