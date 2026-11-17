## Description:

Download YouTube video, audio or a clip to your cloud storage with FlashData. Use for YouTube-to-S3 delivery, MP4 or MP3 exports and media ingestion through asynchronous jobs. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operations teams use this skill to deliver authorized YouTube video, audio, or clips to customer-owned cloud storage and check asynchronous job results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service receives storage credentials to upload files, and MCP clients may retain tool arguments in history.

Mitigation: Use narrowly scoped destination credentials, keep them in protected configuration, and avoid exposing credentials or signed URLs in logs or summaries.

Risk: Downloads use paid Credits and settle by uploaded bytes, so duration alone cannot determine the exact cost.

Mitigation: Check the per-TB price and confirm destination, rights, and byte-based cost approval before submitting a download.

Risk: The security review was partial; its benign, medium-confidence verdict is not a guarantee of safety.

Mitigation: Review the skill before use and follow the credential and cost safeguards described above.

## Reference(s):

- [FlashData YouTube Download documentation](https://flashdata.dev/docs/sources/youtube_download?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_download-task)
- [Storage setup](references/storage.md)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_download-task)

## Skill Output:

**Output Type(s):** [API Calls, Files, JSON, Guidance]

**Output Format:** [JSON job status and delivery details with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous delivery to configured cloud storage; job results include a media file location and size when available.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
