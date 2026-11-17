## Description:

Batch Chinese and Chinese/English text processing for cleaning, normalization, batch operations, and keyword extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huizong-cpu](https://clawhub.ai/user/huizong-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, developers, and automation pipelines can use this skill for local Chinese or Chinese/English text cleanup, normalization, batch processing, and keyword extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on translation, Markdown/table conversion, or simplified/traditional Chinese conversion claims that are not supported by the security guidance for this release.

Mitigation: Use the skill for cleanup, normalization, batch processing, and keyword extraction unless those additional capabilities are added or the description is corrected.

Risk: Frequency-based keyword extraction can return candidate character sequences that are not validated as publication-ready terms.

Mitigation: Review extracted keywords before publishing or using them in downstream content workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huizong-cpu/skills/text-processor)

## Skill Output:

**Output Type(s):** [Text, Code]

**Output Format:** [Plain text strings and JSON-compatible arrays returned by a JavaScript module]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes individual strings or arrays of strings; no network, credential, persistence, or destructive behavior was identified in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
