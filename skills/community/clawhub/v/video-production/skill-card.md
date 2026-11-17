## Description:

Complete A/B video pipeline: storyboard, Veo 3 batch generation, browser preview with feedback loop, and ffmpeg assembly into final videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omerflo](https://clawhub.ai/user/omerflo)

### License/Terms of Use:


## Use Case:

Developers, creators, and production teams use this skill to plan multi-scene AI video projects, generate and review clips, iterate from feedback, and assemble approved scenes into final videos or A/B test variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quota watcher can run unattended as a cron retry job and includes hardcoded personal notification recipients and local paths.

Mitigation: Audit and disable the quota watcher before installation, or replace all paths and notification targets with reviewed user-controlled values before enabling cron.

Risk: Provider API keys are documented for shell startup files that may be shared, backed up, or exposed beyond the current session.

Mitigation: Use a secret manager or session-scoped environment variables, and avoid storing provider API keys in shared shell startup files.

Risk: Storyboard, feedback, and preview handling can expose unsafe local file or HTML content when inputs are not trusted.

Mitigation: Use only trusted storyboard and feedback files until path validation and HTML escaping are reviewed and fixed.

## Reference(s):

- [Video Production skill page](https://clawhub.ai/omerflo/skills/video-production)
- [Storyboard Template](references/storyboard-template.md)
- [Veo 3 Platform Guide](references/platform-guide-veo3.md)
- [Timing and Audio Synchronization Guide](references/timing-sync.md)
- [Premiere Pro Export Guide](references/premiere-export.md)
- [Google Cloud API credentials](https://console.cloud.google.com/apis/credentials)
- [Google Cloud billing](https://console.cloud.google.com/billing/projects)
- [OpenAI API keys](https://platform.openai.com/api/keys)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON storyboards, shell commands, generated HTML previews, media files, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update storyboard JSON, feedback JSON, preview HTML, video/image assets, ffmpeg concat metadata, logs, and final MP4 outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
