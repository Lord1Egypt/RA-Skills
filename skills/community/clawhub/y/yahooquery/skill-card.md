## Description:

Access Yahoo Finance data including real-time pricing, fundamentals, analyst estimates, options, news, and historical data via the yahooquery Python library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[512z](https://clawhub.ai/user/512z)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to guide agents in retrieving Yahoo Finance market data, company fundamentals, screeners, options, news, historical prices, and premium research data through the yahooquery Python library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes user-controlled package installation and live network calls to Yahoo Finance.

Mitigation: Install in an isolated virtual environment, pin yahooquery and dependencies when reproducibility matters, and review generated commands before execution.

Risk: Premium research workflows may require Yahoo credentials.

Mitigation: Store credentials in a protected secret store or injected environment variables rather than source files or prompts.

Risk: Some examples discuss disabling TLS certificate verification.

Mitigation: Keep certificate verification enabled for real traffic and credentials; do not use `verify=False` outside disposable local testing.

Risk: Financial data may be rate-limited or reflect upstream availability and accuracy constraints.

Mitigation: Use retries and backoff for robustness, and verify important financial outputs against authoritative sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/512z/skills/yahooquery)
- [Introduction](references/index.md)
- [Ticker guide](references/ticker/intro.md)
- [Ticker modules](references/ticker/modules.md)
- [Financial statements](references/ticker/financials.md)
- [Historical prices](references/ticker/historical.md)
- [Options](references/ticker/options.md)
- [Screener](references/screener.md)
- [Research](references/research.md)
- [Keyword arguments](references/keyword_arguments.md)
- [Miscellaneous functions](references/misc.md)
- [Advanced session sharing](references/advanced.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe network access, authentication options, retries, async operation, and DataFrame-to-JSON conversion patterns.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
