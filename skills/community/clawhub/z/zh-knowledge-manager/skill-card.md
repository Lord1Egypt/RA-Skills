## Description: <br>
中文 AI 增强知识管理。PREFIX 确定性分类 + hash/语义去重 + jieba 自动标签 + LLM 对话知识提取。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RomeoSY](https://clawhub.ai/user/RomeoSY) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to turn Chinese agent logs and reviewed conversation extracts into a structured Markdown knowledge base with deterministic classification, deduplication, summaries, and optional AI-assisted enrichment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local logs or backup dumps and writes a persistent knowledge base. <br>
Mitigation: Run it only in workspaces where those files are intended inputs, and review generated knowledge-base entries before relying on them. <br>
Risk: Semantic deduplication and extraction may send selected text to configured AI providers. <br>
Mitigation: Use basic sync for local-only operation, redact secrets before AI-enabled commands, and configure provider credentials deliberately. <br>
Risk: LLM extraction can produce draft knowledge that is incomplete or misleading. <br>
Mitigation: Review extracted drafts before importing them into the persistent knowledge base. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RomeoSY/zh-knowledge-manager) <br>
- [Publisher profile](https://clawhub.ai/user/RomeoSY) <br>
- [Knowledge base protocol template](templates/KNOWLEDGE-BASE.md) <br>
- [Configuration template](templates/km.config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and CLI text output, with JSON configuration and state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core sync is local-only; semantic deduplication and extraction can call configured AI providers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
