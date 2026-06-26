## Description: <br>
Business analytics for Russian-speaking CEOs: KPI dashboards, unit economics, forecasting, P&L, cash flow, cohorts and investor-ready reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business owners, CEOs, CFOs, and commercial leaders use this skill to turn revenue, expense, sales funnel, cohort, and cash-flow inputs into management dashboards, financial analysis, forecasts, and investor-ready reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled shell scripts may not install cleanly because the security evidence notes syntax-check failures and a missing .env.example. <br>
Mitigation: Review and repair the shell scripts in a controlled environment before running installation commands. <br>
Risk: The configuration can contain sensitive revenue, margin, CAC/LTV, investor contact, and business-plan data. <br>
Mitigation: Treat config.yaml as sensitive, restrict access, and avoid sharing populated configuration files outside approved business systems. <br>
Risk: External integrations or memory and storage features can expand data exposure if enabled with broad credentials. <br>
Mitigation: Use scoped credentials and define retention rules before enabling integrations, memory, or persistent storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raaipro/raai-business-analyst-pro) <br>
- [README](README.md) <br>
- [ROI documentation](docs/roi.md) <br>
- [Onboarding documentation](docs/onboarding.md) <br>
- [Anti-fail guidance](docs/anti-fail.md) <br>
- [Quick-start examples](examples/quick-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured tables, formulas, recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces business analytics outputs from user-provided financial and operational inputs; configuration may include sensitive business metrics.] <br>

## Skill Version(s): <br>
3.5.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
