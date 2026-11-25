## Description:

Tencent Cloud COS Storage, CI Processing, MetaInsight Retrieval, Knowledge Base, and Console Feature Guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnminh](https://clawhub.ai/user/shawnminh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage Tencent Cloud object storage and run data processing, retrieval, and knowledge base workflows. It can also guide users to relevant COS console features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports credential-handling weaknesses.

Mitigation: Review the credential flow before use, prefer temporary STS credentials, and follow the skill's least-privilege guidance.

Risk: The security review reports vulnerable dependencies and could not fully assess several scripts.

Mitigation: Review the dependency state and the scripts that were not fully assessed before installing or running the skill.

Risk: The security guidance calls out cloud processing, sharing workflows, and a preview-generation flaw.

Mitigation: Check what bucket content and generated previews will be processed or shared, and review preview output before distributing it.

## Reference(s):

- [COS API reference](artifact/references/api_reference.md)
- [Dataset catalog](artifact/references/dataset-catalog.md)
- [Dataset search guide](artifact/references/dataset-search.md)
- [Query specification schema](artifact/references/query-spec.schema.json)
- [ClawHub release page](https://clawhub.ai/shawnminh/skills/tencent-cos-skill)
- [Tencent Cloud COS charges](https://cloud.tencent.com/document/product/436/16871)
- [Tencent Cloud CI charges](https://cloud.tencent.com/document/product/460/6970)

## Skill Output:

**Output Type(s):** [JSON, Files, Configuration instructions, Guidance]

**Output Format:** [Structured JSON results, file operations, and concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify objects and other cloud resources when requested.]

## Skill Version(s):

1.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
