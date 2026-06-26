## Description: <br>
售后管理技能，提供客户投诉管理、返单报价、满意度调查、分析报表和 OKKI CRM 同步功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to manage after-sales workflows, including customer complaints, repeat-order quotes, satisfaction surveys, analytics, and OKKI CRM synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OKKI CRM synchronization can modify external business records with weak access controls. <br>
Mitigation: Put API routes behind authentication and limit who can trigger OKKI synchronization or read synchronization logs. <br>
Risk: The OKKI integration uses dynamic temporary Python fallback handling and operator-controlled OKKI path environment variables. <br>
Mitigation: Remove the dynamic /tmp Python fallback and allow OKKI path environment variables only from trusted operators. <br>
Risk: The security evidence marks the release suspicious for real business use. <br>
Mitigation: Review before using in a real business environment and scan the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cjboy007/ssa-after-sales) <br>
- [E2E test report](test/e2e_test_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text, JSON API responses, Markdown reports, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create and update local after-sales records and trigger OKKI CRM synchronization when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
