## Description:

基于 AgentScope 的多智能体股票诊断系统。一键执行完整诊断流程，自动生成技术面、基本面、舆情面分析、研究员辩论、交易员决策、风控讨论及最终投资决策报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ganyu21](https://clawhub.ai/user/ganyu21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can run a multi-agent workflow that gathers Chinese stock market data, performs technical, fundamental, and news analysis, conducts bullish and bearish debate, and produces trading and risk-management reports. The generated investment decisions should be reviewed by qualified users before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External services may receive stock symbols, generated reports, prompts, and summaries through market-data, LLM, or DingTalk paths.

Mitigation: Run only with data approved for those services, disable DingTalk messaging unless needed, and disclose external sharing to users before execution.

Risk: Runtime package installation and unpinned dependency ranges can change the execution environment.

Mitigation: Preinstall reviewed, pinned dependencies in a dedicated virtual environment or sandbox before running the skill.

Risk: Generated investment recommendations may be inaccurate, stale, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as analytical drafts and require human financial review before making trading decisions.

Risk: Background execution and log redirection may persist sensitive prompts, report text, credentials, or stock analysis data.

Mitigation: Avoid redirecting sensitive runs to shared logs, restrict report directory permissions, and remove logs after review.

Risk: User-provided stock codes and output paths can affect generated filenames and report locations.

Mitigation: Validate stock codes against expected exchange formats and use a controlled report directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ganyu21/skills/trading-agents)
- [DashScope-compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON diagnosis data, PDF report files, Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates multiple role-specific reports and a combined PDF under a report directory; outputs may contain stock symbols, prompts, summaries, and investment recommendations.]

## Skill Version(s):

1.0.7 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
