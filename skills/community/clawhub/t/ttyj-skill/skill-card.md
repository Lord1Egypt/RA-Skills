## Description:

天台宗教理研究与结构化报告生成。支持简单问答和深度研究两种模式。遵循两步工作流（检索→审核标注），所有论断标注CBETA出处。当用户提问天台宗教义、判教、观心、止观、祖师著作等相关问题时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gouchunlei2-png](https://clawhub.ai/user/gouchunlei2-png)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to answer Tiantai Buddhism questions, compare doctrinal systems, interpret patriarchal writings, and produce structured research reports with CBETA-backed citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use named knowledge-base search heavily and may rely on external CBETA or document tools when tasks call for them.

Mitigation: Confirm that the expected knowledge bases and external reference tools are available, and review generated CBETA links and citation tables before relying on research outputs.

Risk: Private documents may be exposed to document-handling workflows if users ask the agent to edit or process them.

Mitigation: Use the skill for private document editing only when the user intends the agent to access those files or online documents.

Risk: Doctrinal or source claims can be misleading if source coverage is incomplete or citations are not checked.

Mitigation: Keep the artifact's citation-first workflow: mark insufficient coverage clearly, avoid unsupported claims, and verify CBETA page-column-line citations during review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gouchunlei2-png/skills/ttyj-skill)
- [CBETA Online](https://cbetaonline.dila.edu.tw/)
- [CBETA Search API Dev](https://cbdata.dila.edu.tw/dev/search?q=關鍵詞)
- [CBETA Search API Stable](https://cbdata.dila.edu.tw/stable/search?q=關鍵詞)
- [CBETA Online Search API](https://api.cbetaonline.cn/search?q=關鍵詞)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured sections, source citations, CBETA links, and limitation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include short definitions, original-source excerpts, structured research reports, citation tables, CBETA link lists, and stated coverage limitations.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
