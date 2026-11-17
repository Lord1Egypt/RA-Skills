## Description:

文心审 is a Chinese-language humanities paper review assistant that helps graduate students and researchers deeply read Chinese academic articles by producing an eight-dimension structured review with source locations, evidence-strength labels, and separated author claims and reader judgments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzliya](https://clawhub.ai/user/yuzliya)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially humanities graduate students and researchers, use this skill to review Chinese-language academic papers in literature, history, philosophy, linguistics, and adjacent humanities fields. It supports pasted paper text, local PDF paths, or URLs and returns a structured reading report for deeper critique and reading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read a local PDF path or fetch a URL when the user provides one.

Mitigation: Only submit documents, paths, and links that the user intends the agent to process.

Risk: The generated paper critique may contain incorrect or overconfident academic judgments.

Mitigation: Use the report as reading support and verify important claims, citations, and evidence assessments against the original paper and relevant literature.

## Reference(s):

- [ClawHub Skill Page: 文心审](https://clawhub.ai/yuzliya/skills/wenxin-review)
- [人文学科审稿参考：常见论证漏洞模式](artifact/references/common-fallacies.md)
- [人文学科审稿参考：学科差异速查](artifact/references/discipline-differences.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown structured as an eight-part reading report with tables, source-location notes, evidence-strength labels, a final overall assessment, and a reading recommendation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each review point is expected to identify the original location and distinguish author claims from reader judgments.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
