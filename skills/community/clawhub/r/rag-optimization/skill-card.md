## Description:

完整的RAG系统优化方案，涵盖21+种策略（Self-RAG、命题分块、上下文压缩、引用溯源、查询意图等）；提供诊断工具、实现代码与评估框架；当用户需要优化知识库问答、提升检索准确率、降低幻觉或评估RAG效果时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwifruit13](https://clawhub.ai/user/kiwifruit13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose, implement, configure, and evaluate RAG improvements for knowledge-base question answering, retrieval accuracy, context quality, citation tracing, and hallucination reduction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote LLM and embedding features can send API keys and document text to configured endpoints.

Mitigation: Use an isolated Python environment, pin dependencies before deployment, configure only HTTPS provider endpoints matching the intended API key, and avoid using remote model features with confidential documents unless external transmission is intended.

Risk: Several RAG features depend on configured LLM or embedding APIs and degrade when credentials or endpoints are unavailable.

Mitigation: Run the provided evaluation workflow on owned data, confirm endpoint configuration before use, and review degraded-mode results before relying on output quality.

## Reference(s):

- [RAG高级技术实现指南](references/advanced-techniques.md)
- [全局操作说明](references/global-operations.md)
- [RAG优化快速入门](references/quickstart.md)
- [RAG系统全链路问题与应对策略](references/implementation-guide.md)
- [Golden Set 建设指南](references/golden-set-guide.md)
- [scripts API 参考文档](references/api_reference.md)
- [scripts 类名速查表](references/api_class_reference.md)
- [scripts 枚举类型汇总](references/api_enums.md)
- [API 文档自动生成](references/api-docs-auto-generation.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce evaluation reports, retrieval pipeline configuration, and implementation guidance for RAG optimization workflows.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
