## Description:

Chinese-language stock multi-agent analysis report generation that uses six analyst roles, bull-bear debate, trading-plan creation, and risk assessment to produce a professional PDF report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanteng](https://clawhub.ai/user/tanteng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through Chinese stock analysis workflows, including structured data extraction, recent-news review, multi-role analyst debate, trading-plan drafting, risk assessment, and PDF report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The normal workflow includes command execution, local file writes, and PDF rendering that require review before installation.

Mitigation: Run only in an isolated workspace with limited filesystem and network access until command construction, stock-code validation, path containment, HTML escaping, renderer network restrictions, and log minimization are reviewed.

Risk: Report and log files may store stock inputs, screenshots, or private trading information locally.

Mitigation: Avoid sensitive account screenshots or private trading information unless local report and log storage is acceptable, and remove generated artifacts when no longer needed.

Risk: Generated stock analysis and trading plans can be incomplete, stale, or misleading.

Mitigation: Treat outputs as research support only and require human review before any financial decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanteng/skills/tradingagents-cn-skill)
- [README](artifact/README.md)
- [Analysis result JSON data schema](artifact/references/data_schema.md)
- [Bull analyst prompt](artifact/references/bull_prompt.md)
- [Bear analyst prompt](artifact/references/bear_prompt.md)
- [Technical analyst prompt](artifact/references/tech_prompt.md)
- [Fundamentals analyst prompt](artifact/references/fundamentals_prompt.md)
- [News analyst prompt](artifact/references/news_prompt.md)
- [Social media analyst prompt](artifact/references/social_prompt.md)
- [Research manager prompt](artifact/references/manager_prompt.md)
- [Trader prompt](artifact/references/trader_prompt.md)
- [Risk debate prompt](artifact/references/risk_debate_prompt.md)
- [Risk manager prompt](artifact/references/risk_manager_prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Chinese Markdown and text guidance with JSON intermediate structures, shell command snippets, and generated PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; normal workflow writes local logs and stock analysis reports.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and _meta.json state 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
