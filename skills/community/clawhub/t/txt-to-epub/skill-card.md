## Description:

Converts TXT text into EPUB files using rule-based chapter detection and splitting for novels, tutorials, and other long-form text, without built-in AI API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1oid](https://clawhub.ai/user/1oid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content maintainers use this skill to convert local TXT manuscripts or long-form documents into EPUB files with chapter detection, a navigable table of contents, and configurable title handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions may vary across environments.

Mitigation: Install in a virtual environment and pin or review ebooklib and chardet versions for reproducible conversion behavior.

Risk: EPUB language metadata defaults to zh-CN when the user does not specify a language.

Mitigation: Pass --language explicitly for non-zh-CN books so readers and catalogs receive accurate language metadata.

Risk: Rule-based chapter detection can mis-split complex or weakly structured TXT files.

Mitigation: Review the chapter count and preview after conversion, then rerun with an explicit split mode or adjusted chunk size when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1oid/skills/txt-to-epub)
- [README](README.md)
- [Simplified Chinese README](README.zh.md)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with shell commands and conversion summary; local EPUB file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local .epub file and reports the output path, chapter count, and chapter title preview.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
