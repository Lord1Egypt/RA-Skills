## Description: <br>
Taobao Sycm (Business Advisor) data analysis tool for retrieving a store's weekly business report, generating business insights, and fetching Sycm data for a Taobao store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncai519](https://clawhub.ai/user/simoncai519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators, analysts, and agents use this skill to retrieve Taobao Sycm weekly business reports from an authenticated Sycm session and turn the returned report into business insight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's logged-in Taobao Sycm session and may retrieve private store analytics. <br>
Mitigation: Run it only for accounts the user is authorized to access, and treat the returned report, charts, and Qianniu links as sensitive business information. <br>
Risk: Repeated Sycm polling can trigger service controls or produce incomplete results if the report is not ready. <br>
Mitigation: Keep the documented 5-second polling interval, stop after the 5-minute timeout, and ask the user to retry later when Sycm reports the service is busy. <br>


## Reference(s): <br>
- [Workflow Details](references/workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/simoncai519/sycm-analysis-skill) <br>
- [Taobao Sycm](https://sycm.taobao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown weekly business report with preserved charts and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated sycm.taobao.com browser session; report generation may take up to 5 minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
