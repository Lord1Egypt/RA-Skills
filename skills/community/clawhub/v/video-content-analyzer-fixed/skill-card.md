## Description:

Downloads videos from platforms such as Bilibili, Douyin, and YouTube, then uses AI-assisted transcription, key-frame review, background research, and content analysis to produce a structured report.

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content analysts use this skill to turn a video URL into a structured analysis report with transcript, scene structure, hook analysis, pacing notes, summary, and references. It can also guide storing video metadata in Supabase or writing reports to Feishu Wiki.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run local command-line tools for video download and media processing.

Mitigation: Run commands in an isolated environment such as a virtual environment or pipx-managed install, review commands before execution, and avoid system-wide package installation flags.

Risk: Video, transcript, and report content may be sent to external services including OpenAI, search providers, Supabase, and Feishu.

Mitigation: Confirm consent and data handling requirements before upload, redact sensitive content, and review transcripts and reports before storing or publishing them.

Risk: Video downloads may involve copyright, platform terms, network access, cookies, or authentication requirements.

Mitigation: Analyze only content the user has rights to process, follow source platform terms, and avoid sharing downloaded media or derived transcripts without permission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/video-content-analyzer-fixed)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with shell, JSON, SQL, and API examples when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include full transcripts, video metadata, analysis summaries, reference links, and optional Supabase or Feishu Wiki write guidance]

## Skill Version(s):

1.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
