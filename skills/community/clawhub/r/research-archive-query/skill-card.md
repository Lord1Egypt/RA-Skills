## Description:

统一查询本地研究资料库，默认同时搜索 AlphaPai 归档和 knowledge_bases，支持精确检索、向量检索和混合检索，并默认排除 private 资料库如 personal。

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdbotrr](https://clawhub.ai/user/clawdbotrr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research analysts use this skill to search local AlphaPai and knowledge_bases archives by topic, timeframe, source, and retrieval mode, then generate concise research summaries while excluding private collections unless explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved local archive text may be sent to an AI analysis component before reports are saved.

Mitigation: Install only if this data flow is acceptable, and include private scopes only when the user explicitly intends to do so.

Risk: Bundled package and publish utilities can modify local distribution directories and publish externally.

Mitigation: Avoid running packaging or publishing scripts except in a controlled development context after reviewing target paths and ClawHub CLI configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawdbotrr/skills/research-archive-query)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown summary reports and JSON runtime metadata; agent responses may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under ~/.openclaw/data/research-archive-query/reports and runtime metadata under ~/.openclaw/data/research-archive-query/runtime.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
