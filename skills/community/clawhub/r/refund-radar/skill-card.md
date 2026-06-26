## Description: <br>
Scan bank statements to detect recurring charges, flag suspicious transactions, and draft refund requests with interactive HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreolf](https://clawhub.ai/user/andreolf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to audit local bank or card statement exports, identify recurring or suspicious charges, and prepare refund or dispute text for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports and refund templates can contain sensitive financial data. <br>
Mitigation: Use the skill only on a trusted device, keep generated HTML and JSON reports private, avoid sharing full card or account numbers, and delete local Refund Radar data when finished. <br>
Risk: The skill invokes an external Python module for bank-statement analysis. <br>
Mitigation: Verify the Python module or repository before running it on real bank statements. <br>


## Reference(s): <br>
- [Detection Rules Reference](references/detection-rules.md) <br>
- [Refund Template Reference](references/refund-templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/andreolf/refund-radar) <br>
- [Publisher profile](https://clawhub.ai/user/andreolf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus generated local HTML and JSON report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local analysis reports and refund-request templates that may contain sensitive financial details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
