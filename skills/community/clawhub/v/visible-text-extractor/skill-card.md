## Description:

Extracts and reconstructs visible text from webpage URLs, article pages, screenshots, long images, image directories, and GIFs into clean, human-readable results with structure, OCR cleanup, deduplication, JSON, reading-order reconstruction, and uncertainty notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wunianze666-netizen](https://clawhub.ai/user/wunianze666-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content teams use this skill to recover readable visible text from URLs, screenshots, image folders, long images, GIFs, and WeChat articles when ordinary extraction or copy/paste is incomplete. It helps produce clean markdown, structured JSON, and Word deliverables while preserving uncertainty and audit data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching and rendering arbitrary pages can expose the execution environment to untrusted web content or unwanted network access.

Mitigation: Use the skill only with approved public or user-provided sources, and sandbox network and browser execution for sensitive environments.

Risk: OCR, browser, ffmpeg, and external script subprocesses can process untrusted files or mutable remote resources.

Mitigation: Run in a constrained workspace, review scripts before execution, and pin or audit mutable dependencies where possible.

Risk: Generated documents may contain sensitive extracted content, and the optional Feishu send path can disclose it to an external destination.

Mitigation: Review outputs before sharing and use Feishu sending only when the destination, identity, and content are explicitly approved.

## Reference(s):

- [Usage Guide](USAGE.md)
- [Output Schema](references/output-schema.md)
- [Deliverable Workflow](references/deliverable-workflow.md)
- [Troubleshooting](references/troubleshooting.md)
- [Universal Article Extractor Spec](references/universal-article-extractor-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, Word documents, shell commands, guidance]

**Output Format:** [Markdown, JSON, DOCX files, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Clean reading outputs are preferred; raw JSON and uncertainty notes are retained for audit or degraded-source cases.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
