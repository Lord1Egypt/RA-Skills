## Description: <br>
Video download, metadata extraction, deduplication, subtitle handling, and archive organization for URLs from YouTube/Shorts, Xiaohongshu, Bilibili, and X/Twitter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiernk](https://clawhub.ai/user/feiernk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, archivists, and operations users use this skill to inspect video URLs, normalize metadata, identify duplicates, prepare sheet records, and organize requested video archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may run downloader tools and create or convert archive files for user-provided video URLs. <br>
Mitigation: Use a trusted yt-dlp installation, process only URLs intended for archiving, and review requested downloads, conversions, and archive-folder changes before approving them. <br>


## Reference(s): <br>
- [Field schema](references/field-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown or plain text with sheet fields and optional shell commands when an archive action is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Follows the requested sheet field order and leaves unknown fields blank.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
