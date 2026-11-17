## Description:

Export webpages into clean local TXT, DOCX, and PDF files with source metadata, fallback extraction logic, and browser-assisted recovery for difficult pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilw-yezi](https://clawhub.ai/user/lilw-yezi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to archive or prepare webpage content for downstream analysis, sharing, or citation while preserving source metadata and extraction quality signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs from the local machine and render pages with a headless browser.

Mitigation: Use it on trusted public webpages, disable browser or PDF fallback for untrusted URLs or shared environments, and prefer network isolation when browser rendering is necessary.

Risk: The skill writes exported content and metadata to local paths, which can be risky in shared workspaces or when filenames are user-controlled.

Mitigation: Choose a dedicated output directory and avoid user-controlled basename values.

## Reference(s):

- [Accuracy and Fallbacks](references/accuracy-and-fallbacks.md)
- [Chrome PDF Guide](references/chrome-pdf-guide.md)
- [Delivery Rules](references/delivery-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local TXT, DOCX, PDF, and JSON metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emits extraction quality, warnings, output paths, and partial-failure status in a metadata JSON file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
