## Description: <br>
Fetches a YouTube video transcript and produces a structured summary in the requested language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivanopassari](https://clawhub.ai/user/ivanopassari) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Claude Code users use this skill to turn a provided YouTube URL or video ID into a structured summary, with optional language selection and optional Markdown export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs uv and may download or use youtube-transcript-api at runtime while contacting YouTube transcript endpoints for videos the user provides. <br>
Mitigation: Review fetch_transcript.py before first use and run the skill only in environments where outbound transcript requests and runtime dependency downloads are allowed. <br>
Risk: The skill can optionally save generated summaries as local Markdown files. <br>
Mitigation: Confirm the save prompt intentionally and review generated Markdown before relying on or sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivanopassari/youtube-summary-skill) <br>
- [Project Homepage](https://github.com/ivanopassari/youtube-summary-skill) <br>
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional saved Markdown file; transcript fetch output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Language can be selected with --lang; saved summaries require user confirmation.] <br>

## Skill Version(s): <br>
1.0.7 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
