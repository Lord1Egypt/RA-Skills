## Description: <br>
A ClawHub agent skill for A-share stock screening using AKShare data and a multi-factor scoring model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeckygo](https://clawhub.ai/user/jeckygo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with stock-market experience use this skill to generate A-share screening reports, ranked recommendations, performance summaries, and email-ready output from AKShare-based factor calculations. Outputs should be treated as decision-support material, not investment advice. <br>

### Deployment Geography for Use: <br>
Global; market coverage is focused on China A-share equities. <br>

## Known Risks and Mitigations: <br>
Risk: Advertised win rates, return ranges, and factor completeness may mislead users if treated as validated financial performance. <br>
Mitigation: Require independent testing, keep financial disclaimers visible, and treat generated recommendations as decision support rather than investment advice. <br>
Risk: Automated schedules and email delivery can expose credentials or run incomplete workflows if configured before dependencies and missing modules are reviewed. <br>
Mitigation: Review the installed files before enabling email credentials or cron jobs, and confirm the data, tool, configuration, and email-sender modules are present. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeckygo/quant-stock-selector) <br>
- [Publisher Profile](https://clawhub.ai/user/jeckygo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked stock selections, factor scores, risk notes, email configuration guidance, and scheduled command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
