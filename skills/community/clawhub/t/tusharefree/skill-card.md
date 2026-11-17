## Description:

Tushare Pro financial data platform guidance for accessing A-share, index, fund, futures, bond, and macroeconomic data through token-authenticated Python APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to configure Tushare Pro access, retrieve financial market and macroeconomic datasets, and generate Python examples for analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tushare API access requires a personal token, which could be exposed if written into prompts, code, or commits.

Mitigation: Keep the token in an environment variable or local secret store rather than committed code or shared examples.

Risk: Routine package upgrades can pull unreviewed dependency updates.

Mitigation: Install in a virtual environment and pin reviewed dependency versions for repeatable use.

Risk: Some Tushare endpoints depend on credit level, rate limits, and live API availability.

Mitigation: Check for empty responses or API exceptions and throttle requests according to account limits before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderwpf/skills/tusharefree)
- [Tushare Pro homepage](https://tushare.pro)
- [Tushare Pro official documentation](https://tushare.pro/document/2)
- [Tushare Pro interface list](https://tushare.pro/document/1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, tushare and pandas packages, and a user-provided Tushare token; some APIs require sufficient Tushare credits.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
