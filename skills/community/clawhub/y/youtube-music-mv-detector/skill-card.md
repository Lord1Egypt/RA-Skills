## Description:

Detect YouTube Music links as MV (music video) or song (audio). Use when user shares YouTube Music links (music.youtube.com/watch?v=...) and you need to classify them as MV or audio track.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicowu07](https://clawhub.ai/user/nicowu07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs to classify a YouTube Music watch link as a music video or an audio track and return the title with the classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Classifying a link sends the YouTube Music URL to YouTube's oEmbed service.

Mitigation: Avoid using the skill for links that should not be shared with YouTube, and review the returned title and author before relying on the classification.

## Reference(s):

- [YouTube oEmbed endpoint used by the skill](https://www.youtube.com/oembed?url={youtube_music_url}&format=json)
- [ClawHub skill page](https://clawhub.ai/nicowu07/skills/youtube-music-mv-detector)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [Markdown or plain text classification result with title and MV/song label]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send the submitted YouTube Music link to YouTube oEmbed for lookup; no credentials are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
