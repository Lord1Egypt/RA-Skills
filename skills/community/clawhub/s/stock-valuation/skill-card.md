## Description:

Generates comprehensive company valuation reports as polished HTML/PDF from market data, peer comparisons, qualitative research, charts, and valuation models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xliucs](https://clawhub.ai/user/xliucs)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to produce deep-dive company valuation reports for a ticker by combining quantitative pipeline outputs with required qualitative research. It is not intended for quick price checks, daily watchlist alerts, real-time trading signals, or personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may expose local files or unsafe web-sourced content.

Mitigation: Run the skill only in a constrained environment with no sensitive local files or credentials available to the agent.

Risk: Untrusted input JSON may influence generated HTML reports.

Mitigation: Avoid untrusted input JSON and require path validation for chart files before report generation.

Risk: HTML report content may include unsafe web-sourced material.

Mitigation: Use HTML escaping or templating with autoescape, and disable JavaScript during PDF rendering.

Risk: Generated valuation reports could be misread as financial advice.

Mitigation: Treat generated reports as informational and review conclusions before relying on them.

Risk: Runtime dependencies are not pinned.

Mitigation: Pin dependencies before safer installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xliucs/skills/stock-valuation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands, JSON examples, and generated HTML/PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates /tmp ticker data JSON, research JSON, chart images, HTML reports, and optional PDF reports.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
