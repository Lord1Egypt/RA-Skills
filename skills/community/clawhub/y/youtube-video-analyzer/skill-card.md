## Description:

Analyze YouTube videos by synchronizing transcript text with visual frames to produce detailed summaries, step-by-step guides, and content understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdrabent](https://clawhub.ai/user/sdrabent)

### License/Terms of Use:


## Use Case:

Developers, educators, analysts, and external users use this skill to turn YouTube tutorials, demos, explainers, and how-to videos into synchronized transcript-and-visual summaries, technical analyses, or step-by-step guides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads YouTube video, subtitle, and frame data to temporary local files, which can contain private or sensitive content.

Mitigation: Use the skill only on content the user is authorized to analyze, keep temporary working directories local, and remove downloaded files after analysis.

Risk: Installing and running yt-dlp, ffmpeg, curl, and Python commands introduces dependency and command-execution risk.

Mitigation: Install dependencies from trusted package sources and review generated shell commands before running them.

Risk: Using browser cookies for age-restricted or private videos can expose local session access.

Mitigation: Use browser cookies only after explicit user approval and only when the user understands that local authenticated access may be involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdrabent/skills/youtube-video-analyzer)
- [Publisher profile](https://clawhub.ai/user/sdrabent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries, step-by-step guides, technical analyses, and visual-text syntheses with timestamps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transcript excerpts, frame observations, visual-only findings, and commands for local video, subtitle, and frame extraction.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
