## Description:

Fetch a YouTube video transcript and provide a structured summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanopassari](https://clawhub.ai/user/ivanopassari)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in Claude Code to summarize public YouTube transcripts in a chosen language and optionally save the summary as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher can execute an unintended local cached script.

Mitigation: Review the installed script path before use and prefer a deterministic script path in sensitive workspaces.

Risk: The skill resolves an unpinned Python dependency at runtime.

Mitigation: Review or pin the youtube-transcript-api dependency before using the skill in a sensitive workspace.

Risk: The transcript fetch contacts YouTube caption services.

Mitigation: Use the skill only with public videos and content that is appropriate to request from YouTube caption services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivanopassari/skills/youtube-summary-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/ivanopassari)
- [Project homepage](https://github.com/ivanopassari/youtube-summary-skill)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Structured Markdown summary with optional saved Markdown file; transcript fetcher returns JSON for agent processing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a YouTube URL or video ID and optional language flag; requires uv to resolve the Python transcript dependency at runtime.]

## Skill Version(s):

1.0.7 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
