## Description:

Transcribe audio and video with the transcribe.so CLI, turning YouTube videos, podcasts, direct media URLs, and local files into speaker-labelled transcripts with timestamped segments, chapters, sections, cited Q&A, and subtitle files across 52 languages and dialects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shsunmoonlee](https://clawhub.ai/user/shsunmoonlee)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to produce transcripts, chapters, show notes, subtitles, quotes, and cited answers from audio or video sources through the transcribe.so CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned globally installed transcribe-so CLI package.

Mitigation: Install only from a trusted package source and prefer a pinned or verified CLI version before use.

Risk: The CLI uses TRANSCRIBE_API_KEY and can spend wallet balance when transcription jobs are created.

Mitigation: Use a scoped API key with a low spend cap and quote jobs before creating or running non-trivial transcriptions.

Risk: The optional heartbeat watcher can automatically upload recordings from a local folder.

Mitigation: Enable the watcher only on a dedicated folder that contains recordings intended for upload and transcription.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shsunmoonlee/skills/transcribe-so)
- [transcribe.so Agent Landing Page](https://transcribe.so/agent)
- [transcribe.so Developer Docs](https://transcribe.so/developers/docs)
- [transcribe.so OpenAPI Reference](https://transcribe.so/openapi.json)
- [transcribe-so npm Package](https://www.npmjs.com/package/transcribe-so)
- [transcribe.so MCP Server](https://transcribe.so/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to call the transcribe-so CLI, which returns JSON for most commands and raw SRT/VTT text for subtitles.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
