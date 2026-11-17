## Description:

中文 AI 增强知识管理。PREFIX 确定性分类 + hash/语义去重 + jieba 自动标签 + LLM 对话知识提取。

This skill is ready for commercial/non-commercial use.

## Publisher:

[romeosy](https://clawhub.ai/user/romeosy)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to turn Chinese agent logs and reviewed conversation extracts into a structured workspace knowledge base with deterministic offline sync and optional AI-assisted deduplication, tagging, and extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual install provenance is inconsistent and no server-resolved GitHub import provenance is available.

Mitigation: Install only from the reviewed ClawHub package unless the maintainer clarifies the canonical repository.

Risk: Optional semantic deduplication and extraction can send selected log entries or conversation dumps to configured AI providers.

Mitigation: Review and redact sensitive content before enabling --semantic or extract, and configure only trusted API endpoints and keys.

Risk: Automated heartbeat sync may process unintended workspace memory files if pointed at the wrong workspace.

Mitigation: Keep heartbeat sync limited to the intended workspace memory directory and review configuration before scheduled use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romeosy/skills/zh-knowledge-manager)
- [README](artifact/README.md)
- [Knowledge base protocol template](artifact/templates/KNOWLEDGE-BASE.md)
- [Default configuration template](artifact/templates/km.config.json)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown knowledge-base entries and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core sync is offline; semantic deduplication and conversation extraction are opt-in and may call configured external AI providers.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
