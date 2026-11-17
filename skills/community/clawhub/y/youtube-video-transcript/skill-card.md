## Description:

Fetch, summarize, and save YouTube transcripts with timestamp navigation, chapter detection, and searchable content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users, researchers, creators, students, and developers use this skill to extract YouTube transcripts, preserve timestamps, search within video content, summarize videos, and export transcript data in useful formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on yt-dlp installed from Homebrew or pip.

Mitigation: Use a trusted package source and pin a reviewed yt-dlp version when your environment requires dependency control.

Risk: Transcript caches and preferences may create local records of watched or processed videos.

Mitigation: Cache transcripts and preferences only after explicit user consent, disclose the save location, and honor requests to show or delete saved files.

Risk: Browser cookies can grant yt-dlp access to age-restricted content.

Mitigation: Do not provide browser cookies unless intentionally authorizing access for a specific video.

Risk: Auto-generated subtitles may contain transcription errors or weak punctuation.

Mitigation: Prefer manual subtitles when available and tell users when auto-generated subtitles are used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/youtube-video-transcript)
- [Skill homepage](https://clawic.com/skills/youtube-video-transcript)
- [Setup process](artifact/setup.md)
- [Memory template](artifact/memory-template.md)
- [Advanced patterns](artifact/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with timestamped transcript text, summaries, export guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local transcript cache files and preference files only after user consent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
