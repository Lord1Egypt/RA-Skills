## Description:

智能学术文献检索，覆盖中英文，支持 arXiv、Semantic Scholar、PubMed、CrossRef 和百度学术并发搜索，以及引用链追踪、作者检索、DOI 查询、BibTeX 导出和 AI 摘要。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly869](https://clawhub.ai/user/fly869)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and developers use this skill to retrieve and summarize academic literature across Chinese and English sources. It supports DOI lookup, BibTeX export, author search, and citation or reference tracing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Literature queries are sent to external scholarly providers selected by the skill.

Mitigation: Avoid submitting sensitive or confidential research topics, and use the source selection option when a provider should be excluded.

Risk: One documented arXiv endpoint uses HTTP rather than HTTPS.

Mitigation: Avoid sensitive arXiv searches until the endpoint is changed to HTTPS.

Risk: Generated review prompts and summaries may reflect incomplete or untrusted upstream paper metadata.

Mitigation: Treat generated summaries as drafts and verify important claims against the original publications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fly869/skills/xueshu-search)
- [Commands Reference](artifact/references/commands.md)
- [Routing Guide](artifact/references/routing-guide.md)
- [Field Mapping](artifact/references/field-mapping.md)
- [arXiv API User Manual](https://info.arxiv.org/help/api/user-manual.html)
- [Baidu Qianfan API documentation](https://cloud.baidu.com/doc/qianfan/s/Amkw9qpzd)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results, BibTeX for DOI exports, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated literature review prompts or summaries derived from retrieved paper metadata.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
