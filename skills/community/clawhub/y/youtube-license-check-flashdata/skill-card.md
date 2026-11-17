## Description:

Checks a known YouTube video's Creative Commons license classification through FlashData as one input to rights review, without verifying training or reuse permission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and rights reviewers can check a specific YouTube video's Creative Commons label and record the returned classification as one input to a separate rights review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is benign but partial, so it cannot guarantee safety; using the hosted FlashData service may expose request data and spend paid Credits.

Mitigation: Use the service only if trusted, keep the API key in protected secret settings, review what is sent, and check the query budget before running it.

Risk: A Creative Commons label match can be mistaken for permission to train on, download, or republish a video.

Mitigation: Treat the result only as a metadata observation and review the actual license, ownership, and intended use separately.

## Reference(s):

- [FlashData YouTube Trainability documentation](https://flashdata.dev/docs/sources/youtube_trainability?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_trainability-task)
- [FlashData hosted MCP service](https://data.flashdata.dev/mcp)
- [FlashData credit pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_trainability-task)
- [Input schema](references/schema.json)
- [ClawHub release page](https://clawhub.ai/flashdatadev/skills/youtube-license-check-flashdata)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON license-label result with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Record the video ID and retrieval time with the raw classification; a Creative Commons label is not reuse authorization.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
