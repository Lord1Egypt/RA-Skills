## Description:

Uses yt-dlp to retrieve YouTube video metadata and multilingual subtitles, then returns transcript text and a simple summary for agent workflows.

This skill is for research and development only.

## Publisher:

[miku233333](https://clawhub.ai/user/miku233333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect YouTube captions for transcript review, summarization, and downstream content analysis when YouTube access and yt-dlp use are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires YouTube network access while describing itself as local-only.

Mitigation: Use only in environments where YouTube access is approved, and disclose network access to reviewers and operators.

Risk: The extractor can install yt-dlp automatically if it is not already present.

Mitigation: Preinstall and pin yt-dlp through a trusted dependency process, and avoid runtime package installation during normal use.

Risk: The server security verdict is suspicious because the artifact under-discloses dependency and network behavior.

Mitigation: Review the skill before installation, run it in a constrained environment, and treat local/no-risk claims as incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miku233333/skills/youtube-transcript-local)
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp)
- [OpenClaw documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with optional subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create transcript and cache files in local working directories.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
