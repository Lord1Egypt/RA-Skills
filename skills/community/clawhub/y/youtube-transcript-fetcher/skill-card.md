## Description:

Fetch full YouTube transcripts with robust InnerTube fallback. Use when extracting captions/transcripts from a YouTube URL, channel, or batch config, especially when normal transcript tools fail, uploader subtitles are missing, or YouTube auto-generated captions may still be recoverable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ioridev](https://clawhub.ai/user/ioridev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch transcript-first source text from individual YouTube videos, recent channel videos, or batch channel configurations. The resulting transcript can then be analyzed, summarized, translated, quoted, or transformed by downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Channel input or batch configuration can cause network requests to non-YouTube destinations.

Mitigation: Use explicit YouTube video IDs, YouTube URLs, or trusted channel handles, and avoid untrusted batch config files until channel URL handling is restricted to YouTube domains.

Risk: The skill runs yt-dlp and Python dependencies with network access.

Mitigation: Install only in environments where outbound network access and those dependencies are acceptable, and review dependency versions before deployment.

Risk: Python dependencies are specified with lower bounds rather than pinned exact versions.

Mitigation: Pin and review dependency versions for production or controlled deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ioridev/skills/youtube-transcript-fetcher)
- [Publisher profile](https://clawhub.ai/user/ioridev)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Example batch configuration](artifact/config/channels.example.json)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, configuration, guidance]

**Output Format:** [JSON file containing transcript text, video metadata, per-item errors, and aggregate stats; agent guidance is Markdown with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output to /tmp/youtube_transcript_fetcher.json by default unless an explicit output path is supplied.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
