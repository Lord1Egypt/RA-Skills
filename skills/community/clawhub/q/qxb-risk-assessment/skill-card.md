## Description: <br>
全面排查企业的经营风险情况，适用于供应商准入尽调、贷前风险筛查、合作伙伴背景调查等场景，全方位预警潜在经营风险，辅助决策者规避合作隐患。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llx-26](https://clawhub.ai/user/llx-26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, procurement teams, lenders, and partner-risk reviewers use this skill to query Qixin enterprise risk data for supplier onboarding, pre-loan screening, and business background checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, enterprise IDs, and due-diligence queries are sent to the Qixin API service. <br>
Mitigation: Install only if the user trusts the Qixin API service and is comfortable sharing queried company identifiers with it. <br>
Risk: Fuzzy company-name lookup can return the wrong enterprise when a name is ambiguous. <br>
Mitigation: Prefer exact enterprise IDs for sensitive reviews and verify the returned ename before relying on the result. <br>
Risk: The QXBENT_API_TOKEN grants access to the external service if exposed. <br>
Mitigation: Store the token with limited exposure and avoid putting it broadly in shell startup files on shared systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/llx-26/qxb-risk-assessment) <br>
- [Publisher Profile](https://clawhub.ai/user/llx-26) <br>
- [getRiskAssessment API Reference](references/getRiskAssessment.md) <br>
- [Qixin API Token Quota Center](https://www.qixin.com/app-center/home?route=skill-quota) <br>
- [Qixin Enterprise Public API Base](https://external-api.qixin.com/skill/ent/public) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance with JSON-like enterprise risk data returned from the Qixin API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, axios, and QXBENT_API_TOKEN; accepts either enterprise name or enterprise ID.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
