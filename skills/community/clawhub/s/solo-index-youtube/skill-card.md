## Description:

Index YouTube channel videos and transcripts for semantic search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers and knowledge workers use this skill to collect YouTube channel transcripts, summarize video content, and make the resulting notes searchable through solograph MCP or local transcript files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may execute third-party Python packages without pinned versions.

Mitigation: Use an isolated environment and pin package versions before running setup or indexing commands.

Risk: Using browser cookies can expose an authenticated Chrome session to yt-dlp.

Mitigation: Avoid --cookies-from-browser chrome unless authenticated access is intentional and approved for the account being used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fortunto2/skills/solo-index-youtube)
- [Publisher profile](https://clawhub.ai/user/fortunto2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local Markdown index and transcript text files when used in standalone mode.]

## Skill Version(s):

2.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
