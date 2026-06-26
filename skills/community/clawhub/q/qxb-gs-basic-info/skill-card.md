## Description: <br>
可快速验证企业真实性、经营状态，适用于商务合作前的背景核查、供应链准入审核、招投标资质验证，合同主体审查等场景，确保企业信息准确可靠。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llx-26](https://clawhub.ai/user/llx-26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, compliance, procurement, and contracting users can query Qixinbao enterprise registration data to verify company identity, operating status, capital, controllers, and related basic business information before decisions or reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried company names or IDs are sent to Qixinbao with the user's API token. <br>
Mitigation: Use the skill only when that external lookup is acceptable, store QXBENT_API_TOKEN like a password, and avoid exposing it in shared machines, logs, or screenshots. <br>
Risk: Fuzzy company-name matching can return the wrong enterprise when names are ambiguous. <br>
Mitigation: For important decisions, prefer enterprise ID lookup when available and verify the returned enterprise name and identifier before relying on the result. <br>
Risk: Dependency security can change over time for the axios package used by the skill. <br>
Mitigation: Pin or update axios according to local dependency policy before using the skill in a sensitive environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/llx-26/qxb-gs-basic-info) <br>
- [Qixinbao skill quota and API token page](https://www.qixin.com/app-center/home?route=skill-quota) <br>
- [getGsBasicInfo reference](references/getGsBasicInfo.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript code and JSON-shaped API result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, axios, and QXBENT_API_TOKEN; calls the Qixinbao external API and returns enterprise basic information fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
