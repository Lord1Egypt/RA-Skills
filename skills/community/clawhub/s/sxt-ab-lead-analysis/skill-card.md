## Description:

私信通(私信AI) AB留资分析是面向会话级实验数据的分析 playbook, 从埋点 CSV 重建会话并完成留资标注、组间对比、行业标准化、漏斗分层、OR 归因和在线报告产出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zh-i9](https://clawhub.ai/user/zh-i9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to analyze private-message A/B experiments for lead-capture outcomes, including rate comparisons, confidence intervals, industry mix adjustment, funnel segmentation, and OR attribution. It is also applicable to similar binary conversation outcomes such as orders or WeChat-add events when the same schema and controls are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive private-message data and may transmit session text or identifiers during LLM-based rubric judgment.

Mitigation: Require dataset-owner approval, redact phone numbers, WeChat IDs, stable session or account identifiers, and other PII before any LLM call.

Risk: The LLM pipeline depends on a MaaS API key and can expose secrets if credentials are handled ad hoc.

Mitigation: Use approved secret management for the MaaS key and avoid embedding credentials in prompts, scripts, or artifacts.

Risk: Generated JSONL artifacts and dashboard updates can retain sensitive conversation records beyond the analysis need.

Mitigation: Restrict outputs to a controlled directory and define retention and deletion rules for JSONL artifacts and dashboard updates.

Risk: Evidence security review flags the release as suspicious because privacy, retention, and scoping controls are not sufficiently defined.

Mitigation: Review before installing or using on production data, and document privacy scope, output access, and data-retention controls before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zh-i9/skills/sxt-ab-lead-analysis)
- [Data Schema and Metric Definitions](artifact/references/data-schema.md)
- [LLM Rubrics to OR Attribution Pipeline](artifact/references/or-pipeline.md)
- [Rubrics Library](artifact/references/rubrics_final.json)
- [OR and FDR Calculation Script](artifact/scripts/or_fdr.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSONL artifacts, JSON results, shell commands, and report-writing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include session JSONL files, flagged-session JSONL files, OR/FDR JSON, and dashboard report guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
