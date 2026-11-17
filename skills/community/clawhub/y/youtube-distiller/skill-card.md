## Description:

Automatically downloads subtitles from YouTube or Bilibili videos and turns them into structured knowledge summaries in multiple styles using AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumo0221](https://clawhub.ai/user/sumo0221)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to extract video subtitles and generate concise Chinese-language summaries, notes, action lists, news-style briefs, investment analyses, podcast-style recaps, ELI5 explanations, or bullet summaries. It is suited for turning YouTube or Bilibili videos into local research notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an exposed MiniMax API key.

Mitigation: Revoke and rotate the exposed key before use, remove it from the artifact and history, and require users to provide credentials through environment configuration.

Risk: Video subtitles or transcript text may be sent to MiniMax for AI summarization.

Mitigation: Use only with content approved for external processing, and disclose MiniMax processing before installation or execution.

Risk: Summaries are saved to configured local Windows directories and synced to SumoNoteBook by default.

Mitigation: Review output and sync paths before running, and use the no-sync option when local persistence or notebook updates are not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sumo0221/skills/youtube-distiller)
- [README.md](artifact/README.md)
- [youtube-knowledge-dev.md](artifact/youtube-knowledge-dev.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or UTF-8 text summaries with video metadata and selected summary style]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write summary files to local Windows directories and sync entries into SumoNoteBook unless disabled.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
