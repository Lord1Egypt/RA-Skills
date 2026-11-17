## Description:

Automatically fetch YouTube video subtitles and generate concise summaries for public videos with available captions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potatosolo](https://clawhub.ai/user/potatosolo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, students, and content curators use this skill to retrieve public YouTube captions and turn long videos into concise summaries, key points, or notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches captions from public YouTube videos through youtube-transcript-api, so dependency or service behavior can affect results.

Mitigation: Install in an isolated environment and pin youtube-transcript-api to a reviewed version before production use.

Risk: Fetched captions and generated summaries may contain sensitive or unwanted local working data if saved.

Mitigation: Treat transcripts and summaries as local working data and save files only when persistence is explicitly intended.

Risk: Auto-generated captions and AI summaries can omit, mishear, or over-compress important details.

Mitigation: Review important summaries against the source transcript or video before relying on them.

## Reference(s):

- [Reference Documentation for Youtube Summary](references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries and plain text transcript output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executive summaries, key points, optional detailed notes, transcript chunks, or saved text/Markdown files when explicitly requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
