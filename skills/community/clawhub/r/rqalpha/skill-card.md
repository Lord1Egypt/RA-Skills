## Description:

RQAlpha 米筐开源事件驱动回测框架 - 支持A股和期货，模块化架构，可自由扩展。

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers use this skill to get concise RQAlpha guidance for installing the framework, structuring backtest strategies, running simulations, and using common trading, data, scheduling, and portfolio APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can introduce unreviewed package behavior or version drift.

Mitigation: Install in an isolated virtual environment or container and prefer pinned, reviewed dependency versions.

Risk: Order-placement examples could be misapplied outside backtesting or simulation.

Mitigation: Treat trading examples as backtest or simulation code unless a user deliberately connects RQAlpha to a live broker and accepts the financial risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderwpf/skills/rqalpha)
- [RQAlpha documentation](https://rqalpha.readthedocs.io/)
- [RQAlpha GitHub project](https://github.com/ricequant/rqalpha)
- [RiceQuant](https://www.ricequant.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; examples may rely on rqalpha, pandas, and numpy.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
