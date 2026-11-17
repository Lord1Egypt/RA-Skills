## Description:

Extracts YouTube video transcripts from existing manual or auto-generated captions using yt-dlp, with optional timestamps and local SQLite caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itzsubhadip](https://clawhub.ai/user/itzsubhadip)

### License/Terms of Use:


## Use Case:

Developers, researchers, and agents use this skill to turn a YouTube URL or video ID into transcript text or structured caption segments for summarization, search, and downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unused third-party provider functions conflict with the skill's privacy claims.

Mitigation: Review before installation; the publisher should remove those functions or clearly document and gate them behind explicit opt-in.

Risk: Optional YouTube cookies may expose account secrets if handled carelessly.

Mitigation: Only provide cookies when necessary and keep them under ~/.config/yt-transcript/.

Risk: Transcript results are cached locally in SQLite.

Mitigation: Treat the cache as local transcript data and clear or protect it according to the user's privacy requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itzsubhadip/skills/youtube-transcript-yt-dlp)
- [ClawHub publisher profile](https://clawhub.ai/user/itzsubhadip)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON transcript segments or newline-separated plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional timestamps; transcript source is manual captions, auto-generated captions, or YouTube transcript panel fallback.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
