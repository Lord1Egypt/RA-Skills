## Description:

Tencent Cloud COS Storage, CI Processing, MetaInsight Retrieval, Knowledge Base, and Console Feature Guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnminh](https://clawhub.ai/user/shawnminh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage Tencent Cloud object storage, run media and document processing, search indexed content, and work with knowledge bases. It translates requests into COS and CI operations and summarizes their results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML previews can expose private files, and exported previews may act as temporary file-access credentials.

Mitigation: Avoid HTML previews until the reported injection and bucket-binding defects are fixed; treat exported previews as temporary access credentials.

Risk: Destructive commands lack confirmation safeguards and may change or delete cloud data, depending on assigned permissions.

Mitigation: Use temporary credentials restricted to the required bucket and actions, preferably read-only. Strict mode reduces deletion risk but does not make every administrative operation read-only.

## Reference(s):

- [Tencent COS Node.js SDK documentation](https://cloud.tencent.com/document/product/436/8629)
- [Tencent Cloud Infinite documentation](https://cloud.tencent.com/document/product/460)
- [Skill API reference](artifact/references/api_reference.md)
- [Dataset search guidance](artifact/references/dataset-search.md)
- [Console feature guides](artifact/references/console-feature-guides.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API results]

**Output Format:** [Markdown responses with shell command examples and structured API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include signed URLs, file metadata, search results, and processing summaries.]

## Skill Version(s):

1.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
