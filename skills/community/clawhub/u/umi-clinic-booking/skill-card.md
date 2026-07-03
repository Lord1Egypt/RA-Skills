## Description: <br>
Umi helps users view booking guidance, open clinic pages, submit appointment requests, consult customer service, query prices, and access app download links for UMI Clinic in Myeongdong, Seoul. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautsgo](https://clawhub.ai/user/beautsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to get UMI Clinic booking guidance, submit appointment details, contact BeautsGO support, and check clinic pricing or app access links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Appointment timing, party size, and any phone number provided by the user may be sent to the BeautsGO or clinic booking service. <br>
Mitigation: Install and use the skill only when this data sharing is acceptable, and add a clear confirmation step before submitting appointment details. <br>
Risk: The security review notes hardcoded API tokens. <br>
Mitigation: Replace hardcoded tokens with scoped, revocable credentials before relying on the skill in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beautsgo/umi-clinic-booking) <br>
- [BeautsGO publisher profile](https://clawhub.ai/user/beautsgo) <br>
- [UMI Clinic booking page](https://i.beautsgo.com/cn/hospital/umi-skin-clinic/skill) <br>
- [UMI Clinic details page](https://i.beautsgo.com/cn/hospital/umi-skin-clinic?from=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown text responses with booking status, guidance, links, and price information] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open allowed BeautsGO clinic pages and submit appointment or price queries through configured external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
