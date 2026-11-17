## Description:

Multimodal YouTube video analysis through audio transcripts and visual frame extraction, intended for summarizing, analyzing, and creating step-by-step guides from YouTube videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdrabent](https://clawhub.ai/user/sdrabent)

### License/Terms of Use:


## Use Case:

External users, developers, and knowledge workers use this skill to extract synchronized transcript and visual context from YouTube videos, especially tutorials, demos, explainers, and HowTo content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts YouTube and downloads metadata, captions, video, and frames, which can create network activity and temporary local files.

Mitigation: Run it from an unprivileged account, use a temporary working directory, and remove temporary files after analysis.

Risk: The optional browser-cookie workflow can expose logged-in YouTube session access to yt-dlp.

Mitigation: Use browser cookies only when necessary for videos you are authorized to access, and avoid sharing or persisting cookie-derived files.

Risk: The yt-dlp dependency is installed without a pinned version.

Mitigation: Install from a trusted package source and review dependency updates before use in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdrabent/skills/youtube-knowledge-extractor)
- [Publisher Profile](https://clawhub.ai/user/sdrabent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with timestamped analysis, visual anchors, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include step-by-step guides, comprehensive summaries, technical analyses, transcript excerpts, frame observations, and cleanup guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
