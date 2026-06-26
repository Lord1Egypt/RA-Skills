## Description: <br>
A US tax planning skill for identifying deductions, tracking expenses, estimating payments, assessing audit risk, and preparing year-round tax summaries across W-2, 1099, S-Corp, mixed, multi-state, and life-event scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shoumiksaha](https://clawhub.ai/user/shoumiksaha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
US taxpayers, freelancers, business owners, and mixed-income earners use this skill to plan deductions, track tax-related expenses, estimate quarterly payments, assess audit risk, and prepare summaries for review with official sources or a licensed tax professional. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive financial profile context and local tax or expense records. <br>
Mitigation: Require explicit confirmation before reading personal profile context or writing expense records, and review stored data before relying on it. <br>
Risk: Tax guidance can be outdated, incomplete, or unsuitable for a user's exact filing situation. <br>
Mitigation: Verify current rules with IRS or state sources and consult a licensed tax professional before filing, paying, or taking material tax positions. <br>
Risk: The skill includes persistent Telegram reminder setup and references cross-skill data access without clear user-control boundaries. <br>
Mitigation: Ask for explicit approval before creating Telegram cron reminders or reading mechanic, card-optimizer, or other skill data. <br>


## Reference(s): <br>
- [Tax Professional Advance ClawHub release](https://clawhub.ai/shoumiksaha/tax-professional-advance) <br>
- [IRS](https://www.irs.gov) <br>
- [Common Write-Offs People Miss](references/common-writeoffs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON expense records and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file writes for expense tracking and Telegram cron reminders only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
