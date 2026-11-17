## Description:

Business analytics for Russian-speaking CEOs: KPI dashboards, unit economics, forecasting, P&L, cash flow, cohorts and investor-ready reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

External business owners, CEOs, CFOs, and commercial leaders use this skill to structure financial metrics, diagnose margins and sales funnels, create forecasts, and prepare management or investor-facing reports from company data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive company finance, sales, customer, and forecasting data.

Mitigation: Use only scoped and approved company datasets, avoid secrets and personal data, and define privacy, retention, and access-control rules before production use.

Risk: The artifact references agent memory, CRM, Sheets, 1C, Supabase, and testimonial storage, which could broaden data exposure if connected without scoping.

Mitigation: Do not grant access to general agent memory; limit connectors to the minimum required datasets and review each integration before enabling it.

Risk: Server security guidance reports broken shell scripts and a missing .env.example in the release package.

Mitigation: Fix and retest the installer, build script, smoke test, and environment template before relying on automated installation.

Risk: Business analysis quality depends on complete and current input data.

Mitigation: Require a named metrics owner and validate revenue, expense, product, funnel, cohort, and cash-flow inputs before using outputs for business decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raaipro/skills/raai-business-analyst-pro)
- [README](README.md)
- [Onboarding Guide](docs/onboarding.md)
- [ROI Guide](docs/roi.md)
- [Anti-Fail Guide](docs/anti-fail.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown business analysis reports with tables, formulas, scenarios, and action recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Russian-first financial analysis that depends on scoped, accurate user-supplied business metrics and configuration.]

## Skill Version(s):

3.5.4 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
