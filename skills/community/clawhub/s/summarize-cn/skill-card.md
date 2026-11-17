## Description:

智能内容摘要工具，支持长文本、文档、网页内容自动摘要，提取核心要点、关键词，支持自定义摘要长度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to summarize long text, local documents, and web pages in Chinese or English, and to extract ranked keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted URL fetching can reach internal or otherwise sensitive network resources in network-sensitive environments.

Mitigation: Install only where arbitrary outbound HTTP(S) requests are acceptable, and avoid using --url on untrusted prompts or links when the runtime can reach internal services.

Risk: Summarizing confidential local files can expose sensitive content through command output or environment logs.

Mitigation: Use the skill only in trusted execution environments with appropriate output and log handling for confidential files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Plain text, Markdown, or JSON summary with keywords and optional metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports short, medium, and long summary lengths and optional metadata.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
