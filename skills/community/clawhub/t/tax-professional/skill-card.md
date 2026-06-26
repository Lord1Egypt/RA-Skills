## Description: <br>
Comprehensive US tax advisor, deduction optimizer, and expense tracker covering employment types, estimated tax payments, audit risk, life event triggers, multi-state filing, RV-as-home rules, tax bracket optimization, document retention, and year-round tax calendar nudges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScotTFO](https://clawhub.ai/user/ScotTFO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer US tax questions, evaluate deductions, track deductible expenses, plan estimated payments, assess audit risk, and prepare year-end deduction summaries. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read sensitive tax context from USER.md and store tax or expense records in the workspace. <br>
Mitigation: Use it only in workspaces where sensitive tax information is appropriate, review stored files, and avoid entering data that should not be retained. <br>
Risk: The skill includes persistent Telegram cron reminder commands for tax deadlines. <br>
Mitigation: Set up those reminders only with explicit consent, confirm the destination service and message contents, and document how to remove the scheduled jobs. <br>
Risk: Tax law changes frequently, so generated guidance may be outdated or incomplete. <br>
Mitigation: Verify important tax positions against current IRS guidance or a qualified tax professional before acting. <br>


## Reference(s): <br>
- [Common Write-Offs People Miss](artifact/references/common-writeoffs.md) <br>
- [IRS](https://www.irs.gov) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON expense records and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace tax expense JSON under data/tax-professional/ and propose cron reminders; tax guidance should be verified against current IRS rules.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
