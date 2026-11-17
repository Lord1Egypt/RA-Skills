## Description:

Validate single video URLs, download highest-quality files with yt-dlp, and archive results into a Feishu Bitable using platform tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiernk](https://clawhub.ai/user/feiernk)

### License/Terms of Use:

MIT-0

## Use Case:

Users with video archiving workflows use this skill to validate a single video URL, download or complete the local archive with yt-dlp, and create or update the corresponding Feishu Bitable record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes detailed user and video metadata to a fixed Feishu Bitable.

Mitigation: Use it only with the intended Feishu destination, preview fields before writing, and avoid private, signed, internal, or token-bearing video URLs.

Risk: The skill depends on an external ytfetch.sh helper that is not included in the reviewed package.

Mitigation: Run it only when that helper is present, trusted, and under your control; prefer packaging reviewed executable helpers with the skill.

Risk: The skill can expose absolute local download paths in archived records.

Mitigation: Prefer a configuration that omits absolute local paths from shared records unless those paths are required and appropriate for the audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feiernk/skills/video-download-archive)
- [Target Feishu Bitable](https://my.feishu.cn/base/KMuEbR5b5aLXFosyxGlc7kTenpb)
- [Workflow](workflow.md)
- [Usage](usage.md)
- [Bitable Mapping](bitable-mapping.md)
- [Error Handling](error-handling.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON record_fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one video URL at a time and returns local path, media metadata, Feishu table identifiers, and fields for the archive record.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
