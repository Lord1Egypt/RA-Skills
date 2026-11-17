## Description:

Converts YouTube and Bilibili video links into plain-text transcripts by downloading and formatting available subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tupleye](https://clawhub.ai/user/tupleye)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to turn supported video links into readable transcripts when the source video already has subtitles. It is suited for extracting lecture notes, captions, or study material from YouTube and Bilibili links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes network requests through yt-dlp and saves transcript files persistently under the user's home directory.

Mitigation: Run it only in an environment where outbound video-site requests and persistent transcript storage are acceptable; clear or isolate the transcript directory between sensitive requests.

Risk: The skill can accidentally output an unrelated prior transcript from the transcript directory.

Mitigation: Use an isolated output directory or remove previous subtitle files before processing a new video.

Risk: The release should be treated as a subtitle downloader, not a translator.

Mitigation: Review outputs for completeness and language coverage before relying on them as translated content.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style transcript text with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp and videos with available subtitles; transcript files may be saved persistently under the user's home directory.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
