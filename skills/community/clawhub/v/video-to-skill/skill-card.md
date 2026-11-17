## Description:

Automatically converts video links from YouTube, Bilibili, Xigua, Douyin, Xiaohongshu, and similar platforms into an OpenClaw Skill and can upload the generated skill to GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eeyan2025-art](https://clawhub.ai/user/eeyan2025-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn online video content into reusable OpenClaw Skill documentation and publishing artifacts. It is intended for workflows that extract or transcribe video content, summarize it, generate a SKILL.md file, and optionally push the result to GitHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video URLs, transcripts, summaries, and generated skill content may be sent to MiniMax.

Mitigation: Use only content approved for third-party processing and avoid sensitive or confidential videos.

Risk: Generated SKILL.md content can be pushed to GitHub using a configured token.

Mitigation: Use a narrowly scoped GitHub token and review generated skill files before publishing.

Risk: The workflow can clone and push to a repository URL supplied at runtime.

Mitigation: Use only trusted repository URLs and prefer a controlled destination repository.

Risk: The audio fallback can automatically install yt-dlp if it is missing.

Mitigation: Preinstall and pin approved dependencies, or avoid the automatic installation path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eeyan2025-art/skills/video-to-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown files and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a generated SKILL.md file path and, when publishing succeeds, a GitHub link.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
