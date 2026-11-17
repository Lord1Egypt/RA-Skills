## Description:

Extracts YouTube video transcripts and subtitles through the YouMind API, supports batches of up to five videos, saves videos to a YouMind board, and returns timestamped transcripts as markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve YouTube captions or transcripts, save videos to YouMind, and optionally summarize transcript contents without relying on local media extraction tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install the YouMind npm CLI globally.

Mitigation: Ask for explicit confirmation before global installation and prefer a controlled environment where global npm changes are acceptable.

Risk: YouTube URLs and resulting transcript material may be sent to and saved in YouMind.

Mitigation: Use the skill only for videos the user is comfortable saving to YouMind, and avoid sensitive or private content unless the user explicitly approves.

Risk: API-key command forms can expose credentials on shared or logged systems.

Mitigation: Check for configured environment variables without printing secrets, and avoid pasting or echoing API keys in chat, shell history, or logs.

Risk: The workflow may show promotional, upgrade, or pricing links.

Mitigation: Keep such messages relevant to actual service limits or setup needs and make clear when YouMind account or plan requirements affect execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dophinl/skills/youmind-youtube-transcript)
- [Publisher Profile](https://clawhub.ai/user/dophinl)
- [Setup](references/setup.md)
- [Environment Configuration](references/environment.md)
- [Long-Running Tasks](references/long-running-tasks.md)
- [Error Handling](references/error-handling.md)
- [YouMind API Keys](https://youmind.com/settings/api-keys?utm_source=youmind-youtube-transcript)
- [YouMind Skills Gallery](https://youmind.com/skills?utm_source=youmind-youtube-transcript)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown transcript files plus concise chat status messages and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one transcript markdown file per completed video; batches up to five YouTube URLs and reports title, language, word count, file name, and YouMind link.]

## Skill Version(s):

1.3.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
