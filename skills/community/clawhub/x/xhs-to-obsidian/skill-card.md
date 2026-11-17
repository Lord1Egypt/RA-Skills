## Description:

Extract Xiaohongshu (小红书) posts into Obsidian notes from shared Xiaohongshu or RedNote links, with support for single posts, batch extraction, and optional video transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmin1113](https://clawhub.ai/user/jmin1113)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preserve Xiaohongshu posts as Obsidian Markdown notes. It helps capture post text, images, source metadata, engagement counts, tags, and optional Chinese video transcripts for personal knowledge management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires exported Xiaohongshu browser cookies, which can expose a user's active session if mishandled.

Mitigation: Use a dedicated local cookie file with restricted permissions, refresh it only when needed, and avoid sharing generated logs or command output that may contain cookie paths or session-related errors.

Risk: Unsafe network validation can expose session cookies or downloaded media to unintended destinations.

Mitigation: Before use, validate Xiaohongshu hostnames, keep TLS certificate and hostname verification enabled, and restrict redirects and video URLs to expected Xiaohongshu domains.

Risk: Video transcription downloads media and stores temporary files locally.

Mitigation: Protect temporary files, clean them after transcription, and review generated transcripts before appending them to Obsidian notes.

Risk: Passing unvalidated values into inline code can lead to command or script execution issues.

Mitigation: Quote and validate URL, post ID, and path inputs before running extraction or transcription commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jmin1113/skills/xhs-to-obsidian)
- [Publisher profile](https://clawhub.ai/user/jmin1113)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, JSON command results, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Obsidian Markdown files and may append video transcription text when local transcription tools are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
