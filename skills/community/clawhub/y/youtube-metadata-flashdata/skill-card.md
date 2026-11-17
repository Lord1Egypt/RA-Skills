## Description:

Read YouTube video metadata with FlashData: title, description, channel, statistics, chapters and available media formats. Use to inspect a known video, build video cards, create chapter links or choose download options. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to inspect a known YouTube video's metadata, create video cards or chapter links, and review available media formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a FlashData API key, and exposed credentials could be misused.

Mitigation: Keep FLASHDATA_API_KEY in protected environment or secret-manager settings; do not put it in prompts or skill files.

Risk: Metadata queries use paid FlashData Credits, and a timed-out submission may still have been charged.

Mitigation: Check pricing and the approved query budget before submitting; after a timeout, check the existing job or FlashData Jobs before retrying.

## Reference(s):

- [FlashData YouTube Metadata documentation](https://flashdata.dev/docs/sources/youtube_metadata?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_metadata-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_metadata-task)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text]

**Output Format:** [Structured video metadata with optional Markdown video cards or timestamped chapter links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available statistics, chapters, and formats vary by video; the response reports transcript availability but does not include caption text.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
