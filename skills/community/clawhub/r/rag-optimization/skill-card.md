## Description: <br>
提供RAG检索增强与优化指导，涵盖Self-RAG、命题分块、片段提取、上下文压缩、引用溯源、查询意图、多跳检索和文档预处理等策略，并配套实现脚本、配置模板和评估框架。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiwifruit13](https://clawhub.ai/user/kiwifruit13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose, implement, configure, and evaluate RAG systems for knowledge-base question answering, retrieval accuracy improvement, noise reduction, citation tracking, and hallucination control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation data, document text, and user queries may be sent to external LLM providers during RAG evaluation or judging. <br>
Mitigation: Disable remote judging unless needed, pass only approved LLM clients, redact sensitive text before evaluation, and avoid private, regulated, or customer data unless controls are in place. <br>
Risk: API keys used by external model providers may be exposed if handled directly in prompts, files, or logs. <br>
Mitigation: Provide API keys through environment variables or a secrets manager and keep them out of skill content, test data, prompts, and logs. <br>
Risk: RAG optimization guidance can produce misleading results if applied without reviewing retrieval quality, citations, and evaluation assumptions. <br>
Mitigation: Review generated recommendations before execution, scan the skill before deployment, and validate changes against representative test cases and baseline metrics. <br>


## Reference(s): <br>
- [RAG检索优化技能 README](references/README.md) <br>
- [5分钟快速上手](references/quickstart.md) <br>
- [RAG高级技术实现指南](references/advanced-techniques.md) <br>
- [RAG优化实施指南](references/implementation-guide.md) <br>
- [全局操作说明](references/global-operations.md) <br>
- [RAG original paper](https://arxiv.org/abs/2005.11401) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python scripts and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance, diagnostic steps, reusable script recommendations, and configuration patterns for RAG workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
