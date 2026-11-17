## Description:

Extract and analyze YouTube video content using yt-dlp, including metadata, transcripts, subtitles, comments, playlists, and channel overviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuya227939](https://clawhub.ai/user/xuya227939)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, content creators, and developers use this skill to extract structured YouTube metadata, transcript text, comments, playlist entries, and channel summaries for analysis, summarization, or content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied YouTube URLs may be passed into shell commands.

Mitigation: Validate that inputs are expected YouTube URLs, avoid shell string interpolation, and invoke yt-dlp with argument arrays where the agent runtime supports them.

Risk: The workflow depends on locally installed yt-dlp and may process public comments or create temporary subtitle files.

Mitigation: Install yt-dlp in an isolated environment, keep it updated, limit comment collection to the requested scope, and clean up temporary subtitle files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuya227939/skills/youtube-research-kit)
- [Project homepage](https://snapvee.com)
- [Support issues](https://github.com/nickeljiangjiang/youtube-research-kit/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables, timestamped transcript text, numbered comment lists, summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary subtitle files and process public YouTube comments when the agent follows the yt-dlp workflow.]

## Skill Version(s):

1.2.0 (source: release evidence, artifact metadata, and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
