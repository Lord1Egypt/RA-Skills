## Description:

估值建模专家 helps Chinese-speaking users perform financial valuation analysis with DCF, PE, PB, PEG, WACC, sensitivity analysis, and Monte Carlo-style valuation outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External finance analysts, investors, and agent users can use this skill to structure valuation workflows, compare DCF and market-multiple estimates, calculate WACC assumptions, and produce risk-aware valuation summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command execution and file-write behavior could affect local files or expose sensitive financial data if the runtime is not constrained.

Mitigation: Run the skill in a sandboxed agent environment, review commands before execution, and grant access only to the files needed for the valuation task.

Risk: Financial data API credentials may be needed for market or fundamentals data access.

Mitigation: Use least-privilege API keys through environment variables and avoid sharing unrelated credentials or sensitive local files.

Risk: Generated valuation outputs can be sensitive to assumptions and may be misleading if treated as financial advice.

Mitigation: Review model assumptions, compare outputs across methods, and have qualified users validate decisions before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/valuation-model)
- [Skill homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [analysis, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON with optional code snippets, shell commands, configuration notes, and generated valuation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include valuation metrics, model assumptions, sensitivity matrices, risk notes, and references to financial data API credentials supplied by the user.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
