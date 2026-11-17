## Description:

Get YouTube transcript text and timestamped segments with FlashData. Use to summarize a video, find quoted passages, create timestamp links or export subtitles. Selects existing automatic captions by default. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can retrieve an existing YouTube caption track to summarize videos, find and cite passages by timestamp, or prepare subtitle text. The skill supports automatic or uploader-provided captions in a selected language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript queries connect to FlashData and spend FlashData Credits.

Mitigation: Check FlashData pricing before querying and submit only the video and caption options needed for the task.

Risk: The hosted FlashData request uses the FLASHDATA_API_KEY credential.

Mitigation: Store the key in protected environment or secret-manager settings; do not put it in prompts or committed files.

Risk: The security review was benign, but its analysis was partial because two local reference checks were unavailable.

Mitigation: Review the skill and its linked FlashData documentation before installation, and account for the incomplete reference checks.

## Reference(s):

- [FlashData YouTube transcript documentation](https://flashdata.dev/docs/sources/youtube_transcript?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_transcript-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_transcript-task)
- [ClawHub skill page](https://clawhub.ai/flashdatadev/skills/youtube-transcript-flashdata)

## Skill Output:

**Output Type(s):** [Text, Markdown, Subtitle text]

**Output Format:** [Transcript text with timestamped segments; summaries, timestamp links, or subtitle text such as SRT or WebVTT as requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an existing caption track; automatic captions may contain recognition errors.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
