## Description:

Converts bookmarked videos from YouTube, X (Twitter), and other yt-dlp-supported sites into a podcast RSS feed hosted on Cloudflare R2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryandeathridge](https://clawhub.ai/user/ryandeathridge)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add individual video URLs or YouTube playlists to a personal podcast feed, manage episodes, and publish audio files plus feed.xml to Cloudflare R2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads browser cookies by default for age-restricted or protected video downloads.

Mitigation: Set VIDPOD_COOKIE_BROWSER=none unless authenticated downloads are explicitly needed, and review any cookie use before running the skill.

Risk: The skill handles Cloudflare R2 credentials and writes them to ~/.openclaw/.env during setup.

Mitigation: Use a bucket-scoped R2 token and restrict ~/.openclaw/.env to owner-only permissions such as 0600.

Risk: Uploaded audio files and feed.xml may become publicly accessible through the configured R2 public URL.

Mitigation: Make the R2 bucket public only if the feed and uploaded audio are intended to be public.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryandeathridge/skills/video2podcast)
- [ClawHub publisher profile](https://clawhub.ai/user/ryandeathridge)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- [Cloudflare R2 get started](https://developers.cloudflare.com/r2/get-started/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands; generated podcast artifacts are MP3 audio files and RSS XML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg, yt-dlp, boto3, Cloudflare R2 credentials, and optional browser-cookie access for restricted downloads.]

## Skill Version(s):

1.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
