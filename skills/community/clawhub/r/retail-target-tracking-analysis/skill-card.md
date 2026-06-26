## Description: <br>
A retail store target tracking analysis skill for daily, weekly, and monthly goal progress, T-N data delay handling, and traffic-light alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operations teams and analysts use this skill to compare store performance against daily, weekly, and monthly targets, generate status reports, and identify stores that need attention. Operators can also use it for scheduled T-N alert checks when they are authorized to access the relevant BI data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access broader business metrics than its store-level framing clearly discloses. <br>
Mitigation: Use only where the operator is authorized to access the BI API and organization-wide metrics; limit runs to store-level data unless city, province, region, or group analysis is explicitly intended. <br>
Risk: Goal tracking reports and alerts may influence operational decisions if targets, dates, or BI data are misconfigured. <br>
Mitigation: Review target configuration, store mappings, date ranges, and generated alerts before using the output for business action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-target-tracking-analysis) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, Python dictionaries, and alert lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include store identifiers, date ranges, target amounts, actual sales, achievement rates, alert levels, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact files contain internal v3.0, v3.0.0, and 3.1.0 labels) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
