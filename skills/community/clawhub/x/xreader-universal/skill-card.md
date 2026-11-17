## Description:

Universal content reader for WeChat, Bilibili, X/Twitter, YouTube, Xiaohongshu, Telegram, RSS, and general web pages, including browser fallback for sites that block simple HTTP fetching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoyaryyj](https://clawhub.ai/user/hoyaryyj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-workflow users use this skill to fetch article text, social platform content, RSS entries, generic web pages, and available video transcripts through an agent-accessible CLI or Python library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use saved browser or platform login sessions.

Mitigation: Run login only for accounts the agent is intended to access, and review session handling before using private or sensitive accounts.

Risk: The clear command may remove content from the configured inbox.

Mitigation: Confirm the inbox location and command scope before running clear, and keep a backup for important saved content.

Risk: Fetching external URLs can expose requests to third-party platforms and retrieve untrusted content.

Mitigation: Verify URLs before fetching and review retrieved content before relying on it in downstream work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hoyaryyj/skills/xreader-universal)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and extracted content text from the x-reader CLI or Python library.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use browser or saved-session fallbacks and local inbox operations when the installed x-reader implementation supports them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
