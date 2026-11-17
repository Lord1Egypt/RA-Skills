## Description:

Use when the user asks to create, inspect, render, or repair an HTML-authored video from a brief, website, Markdown/text file, or GitHub repository; needs captions, voiceover, background music, generated images/video clips, or a HyperFrames-like local video pipeline using SenseAudio media APIs and AudioClaw LLM planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fridaylifan](https://clawhub.ai/user/fridaylifan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content producers use this skill to plan, author, inspect, repair, and render HTML-based videos from briefs, websites, Markdown or text files, and GitHub repository READMEs. It supports local project scaffolding, CLI-driven media generation, captions, narration, music, screenshot capture, audits, and rendered video delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch websites and capture page screenshots.

Mitigation: Avoid private or internal URLs unless the resulting screenshots and generated video are safe to store and share.

Risk: The skill can call SenseAudio and LLM providers using configured credentials.

Mitigation: Use trusted API endpoints, keep SenseAudio and LLM credentials separate, and review custom LLM base URLs before using stored AudioClaw credentials.

Risk: The skill can use browser profiles or cookie files for gated or personalized sites.

Mitigation: Use isolated profiles or cookie files only when necessary, and inspect captures for private or personalized content before delivery.

Risk: The skill writes generated project media and reports to disk.

Mitigation: Review manifests, render reports, captions, transcripts, and generated media before publishing or sharing outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fridaylifan/skills/senseaudio-video-gen)
- [SenseAudio API Reference](references/api.md)
- [HTML Authoring Guide](references/authoring.md)
- [SenseAudio Media Pipeline](references/media-pipeline.md)
- [Local Renderer](references/renderer.md)
- [Production Workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with CLI commands plus JSON, HTML, media, subtitle, manifest, and report files from generated projects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local HTML video project structures, generated media assets, captions, render reports, and MP4 outputs through CLI workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
