## Description:

Video download, metadata extraction, deduplication, subtitle handling, and archive organization for URLs from YouTube/Shorts, Xiaohongshu, Bilibili, and X/Twitter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiernk](https://clawhub.ai/user/feiernk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, archivists, and external users use this skill to inspect video URLs, normalize video metadata, detect duplicate records, map sheet fields, and organize downloadable archive files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow assumes Chinese-language sheet fields and Beijing-time date formatting, which may not match every archive.

Mitigation: Review and customize the field schema, localized field names, and timezone expectations before using the workflow for another archive format.

Risk: Downloading, converting, archiving, or updating sheet records can affect local files or records if applied to the wrong video.

Mitigation: Follow the documented stop rules for duplicate matches, unresolved uploaders, filename conflicts, non-video URLs, and ambiguous metadata before proceeding.

## Reference(s):

- [Field schema](references/field-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or concise text with normalized sheet fields and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Beijing-time date formatting and Chinese-language sheet field names unless customized.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
