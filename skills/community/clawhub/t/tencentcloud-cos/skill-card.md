## Description:

Tencent Cloud COS Storage, CI Processing, MetaInsight Retrieval, Knowledge Base, and Console Feature Guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnminh](https://clawhub.ai/user/shawnminh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage Tencent Cloud COS objects and buckets, run Cloud Infinite processing and search workflows, and get guidance for related console features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious with medium confidence, citing concerns about credential handling, dependencies, and preview generation; some files were only partly analyzed.

Mitigation: Review credential storage and encryption behavior, update vulnerable dependencies, and complete review of the partly analyzed scripts before installation.

Risk: The skill can persist credentials, create or index cloud resources, process images with cloud AI, and generate signed links.

Mitigation: Review these actions before use; prefer least-privilege sub-account keys and temporary STS credentials, and pay attention to credential persistence and signed-link sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawnminh/skills/tencentcloud-cos)
- [COS Node.js SDK documentation](https://cloud.tencent.com/document/product/436/8629)
- [Tencent Cloud CI documentation](https://cloud.tencent.com/document/product/460)
- [Skill API reference](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Cloud operation results]

**Output Format:** [Text and Markdown responses with shell commands, links, and operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create cloud resources, process or search user data, and generate signed URLs when requested.]

## Skill Version(s):

1.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
