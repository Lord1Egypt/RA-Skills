## Description:

Decode and encode Thunder (Xunlei) thunder:// download links to plain URLs locally, with support for decoding qqdl:// and flashget:// links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use this skill to decode thunder://, qqdl://, and flashget:// links into plain URLs, encode plain URLs as thunder:// links, and prepare standard downloader commands while preserving safety context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decoded links from untrusted sources may contain misleading destinations or terminal control characters.

Mitigation: Inspect decoded output before reuse and avoid pasting untrusted decoded text directly into an interactive terminal.

## Reference(s):

- [Thunder Skill Page](https://clawhub.ai/zhangifonly/skills/thunder)
- [Xunlei Official Website](https://www.xunlei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain text URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream output; decoded URLs from untrusted links should be treated as unsafe terminal output.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
