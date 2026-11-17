## Description:

Download videos from Instagram Reels, TikTok, YouTube Shorts, Twitter/X clips, and other supported social media platforms when the user clearly asks to save a video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elony-7](https://clawhub.ai/user/elony-7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to download public social-media videos from supported URLs and return the generated file when download intent is explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local downloader that makes network requests and returns generated files from the user's machine.

Mitigation: Install yt-dlp in an isolated pinned environment and run downloads in a network-restricted sandbox when possible.

Risk: The security summary flags temporary-file handling and SSRF controls as areas needing review before sensitive-host use.

Mitigation: Avoid use on sensitive hosts until those controls are reviewed and tightened.

## Reference(s):

- [Social Video Downloader skill page](https://clawhub.ai/elony-7/skills/social-video-downloader)
- [Setup instructions](artifact/SETUP.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Downloaded media file with concise status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp and network access; may provide a local file path when a generated file exceeds the messaging size limit.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
