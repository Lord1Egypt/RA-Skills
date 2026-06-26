## Description: <br>
Analyzes pet monitoring videos or video URLs for feeding, drinking, excretion, mental state, vomiting, limping, and other health indicators, then returns pet health monitoring reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care agents use this skill to submit cat or dog monitoring footage for cloud-backed health behavior analysis and to retrieve historical pet health reports. The report is health guidance only and is not a substitute for professional veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet or home monitoring videos, video URLs, and an open-id may be sent to LifeEmergence/Open API services. <br>
Mitigation: Use only non-sensitive footage or approved accounts, and obtain user consent before sending private pet or home monitoring media to the service. <br>
Risk: The skill performs account-linked cloud calls and may persist tokens locally under the workspace data area. <br>
Mitigation: Review account creation and login behavior, token storage, and workspace data retention before deploying the skill. <br>
Risk: Historical report access and export links may expose prior pet health reports. <br>
Mitigation: Limit use to trusted open-id values, verify report ownership before sharing links, and avoid posting generated export URLs in public channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-pet-health-monitoring-analysis) <br>
- [Pet health analysis API documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands] <br>
**Output Format:** [Markdown report text, Markdown tables for history results, or JSON when requested; results may also be saved to a file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include pet type, monitoring period, behavior counts, detected abnormalities, health score, care suggestions, report links, and export URLs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; SKILL.md frontmatter says 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
