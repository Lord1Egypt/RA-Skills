## Description:

Quant Research Lab is a multi-agent quantitative strategy research skill that helps coding agents design, backtest, risk-manage, optimize, and document trading strategy workflows through 15 specialized role prompts.

This skill is for research and development only.

## Publisher:

[yili1992](https://clawhub.ai/user/yili1992)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and quantitative strategy teams use this skill to structure LLM-assisted research across strategy design, backtesting, factor modeling, risk review, execution planning, portfolio optimization, and compliance-oriented review. It supports both individual role prompts and sequenced pipeline tracks for end-to-end quantitative research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated trading, market-data, or execution-system snippets may be treated as production-ready infrastructure.

Mitigation: Use the outputs as design guidance and add authentication, authorization, rate limiting, compliance review, and testing before deployment.

Risk: Pipeline state can retain sensitive strategy details in state/research-context.md.

Mitigation: Review and remove retained local state before sharing the workspace or publishing derived materials.

Risk: Quantitative research outputs can be inaccurate, incomplete, or unsuitable as financial advice.

Mitigation: Perform independent due diligence, data validation, backtesting, and risk review before relying on any strategy output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yili1992/skills/quant-research-lab)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Hermes Agent](https://hermes.nousresearch.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured sections, formulas, pseudocode, QAGATE blocks, and occasional shell commands or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pipeline workflows may persist local research context in state/research-context.md; generated strategy, market-data, and execution-system material requires review before use.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
