## Description:

Searches for, downloads, and verifies Zhongkao exam papers across Chinese regions, subjects, and years.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abill6688](https://clawhub.ai/user/abill6688)

### License/Terms of Use:

MIT-0

## Use Case:

External users and education-focused agents use this skill to locate Zhongkao exam papers, retrieve candidate files from public sources, verify basic file authenticity, and organize the resulting materials by year, region, subject, and answer availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retrieves exam files from public websites, social media, and cloud-drive links that may be unsafe or untrusted.

Mitigation: Use the skill only in a sandbox or dedicated download directory, avoid social-media and cloud-drive links unless independently trusted, and manually check downloaded archives before opening or uploading them.

Risk: The downloader and archive workflow expose users to arbitrary file writes and unsafe downloaded content.

Mitigation: Confine output paths to a dedicated directory, add URL/domain allowlisting and download size limits, and use safe archive extraction practices.

Risk: Security evidence reports weak verification and TLS handling in the downloader workflow.

Mitigation: Require fixes for TLS verification and keep the provided file validation step before any downstream use.

## Reference(s):

- [中考真题来源详细参考](references/sources.md)
- [特殊情况处理指南](references/edge-cases.md)
- [ClawHub skill page](https://clawhub.ai/abill6688/skills/zhongkao-exam-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON command output, source URLs, and downloaded exam-paper files when retrieval succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification results are emitted as JSON; downloaded materials may be PDF, DOCX, ZIP, RAR, PNG, or JPEG depending on the source.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
