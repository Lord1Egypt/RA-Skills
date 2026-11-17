## Description:

Generates an MP4 lip-sync video from a visible-face image and the user's own audio recording using ComfyDeploy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

External creators, developers, and automation agents use this skill to turn a face image and an owned or consented audio recording into a lip-synced MP4 video while preserving the supplied audio timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive face images, voice recordings, audio URLs, and generated media are sent through ComfyDeploy.

Mitigation: Use only media you own or have consent to process, and provide a least-privileged ComfyDeploy API key.

Risk: Private or internal media URLs could expose data to third-party processing.

Mitigation: Avoid private or internal URLs; prefer media intentionally prepared for external processing.

Risk: URL limits, upload consent, timeouts, temporary file cleanup, and dependency locking need review before broad deployment.

Mitigation: Run in a constrained environment and review these controls before installation or operational use.

## Reference(s):

- [UGC Manual ClawHub skill page](https://clawhub.ai/pauldelavallaz/skills/ugc-manual)
- [ComfyDeploy deployment queue endpoint](https://api.comfydeploy.com/api/run/deployment/queue)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands; runtime artifact is an MP4 video file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires COMFY_DEPLOY_API_KEY and ffmpeg; uploads image and audio media to ComfyDeploy.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
