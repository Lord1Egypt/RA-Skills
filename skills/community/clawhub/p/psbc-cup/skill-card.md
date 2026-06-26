## Description: <br>
易企收自动化访问 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dayhee](https://clawhub.ai/user/dayhee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users and operators use this skill to open the PSBC 易企收 payment-management portal or demo portal, choose the appropriate access mode from user intent, and receive guidance for common fee-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens a payment-management portal where uploads, refunds, blacklist changes, or other business actions may affect real accounts. <br>
Mitigation: Verify the openpayment.psbc.cn domain and confirm that each sensitive action is intended and authorized before logging in, uploading data, issuing refunds, or changing blacklist settings. <br>
Risk: Direct deep links to portal subpages may return users to the home page or the wrong navigation context. <br>
Mitigation: Use the visible browser session and navigate through the portal home-page menus for functional modules when direct URL access does not preserve context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dayhee/psbc-cup) <br>
- [易企收正式版登录](https://openpayment.psbc.cn/new/login) <br>
- [易企收演示版首页](https://openpayment.psbc.cn/newDemo/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown guidance with browser-navigation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a visible browser session and does not record user operations or input data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
