## Description:

Turn curated X/Twitter builder activity plus optional podcast and blog items into concise English and Chinese markdown digests with first-mention person blurbs, link preservation, and an optional compressed executive-style output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keziqicoze09-del](https://clawhub.ai/user/keziqicoze09-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and publishing teams use this skill to transform structured X/Twitter, podcast, and blog feed JSON into bilingual daily digests or publishable briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided feed content can be copied into generated Markdown, including HTML-like text or unsafe URL schemes if the digest is later rendered publicly.

Mitigation: Use curated or trusted inputs where possible, and sanitize generated Markdown before publication or render it with raw HTML and unsafe URL schemes disabled.

## Reference(s):

- [Sample input JSON](references/sample-input.json)
- [Sample Chinese output](references/sample-output-zh.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files with concise bilingual digest sections and preserved source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes digest-en.md and digest-zh.md from structured JSON input.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
