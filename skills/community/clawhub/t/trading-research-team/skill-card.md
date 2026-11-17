## Description:

Builds and back-tests trading strategy hypotheses with explicit risk limits and a written rejection log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3ratech](https://clawhub.ai/user/t3ratech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, trading researchers, and operations teams use this bundle to coordinate agents for strategy hypothesis generation, market and news ingestion, back-testing, risk review, trading workflow monitoring, and decision logging. Treat outputs as trading research or paper-trading guidance unless independent approval, scoped credentials, and operational controls are in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous trading workflows may access trading tools, shell commands, and files without clear approval gates.

Mitigation: Use paper trading or tightly scoped credentials, require independent approval for live actions, and enforce MCP method allowlists, file and shell restrictions, logging, and a kill switch.

Risk: Trading research outputs may be incomplete, stale, or unsuitable for live market decisions.

Mitigation: Require human review, position limits, drawdown limits, and evaluation pass criteria before applying any strategy or action proposal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/t3ratech/skills/trading-research-team)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured text with optional shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coordinated role outputs such as hypotheses, back-test summaries, risk reviews, rejection logs, and trading action proposals.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
