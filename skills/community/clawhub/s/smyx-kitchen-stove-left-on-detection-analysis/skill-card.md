## Description: <br>
Analyzes fixed kitchen camera video to detect unattended stove flame or heat-source activity and generate a stove-left-on alert for caregivers or smart-home workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, caregivers, elder-care operators, and smart-home integrators use this skill to analyze kitchen camera video or video URLs for unattended active stove conditions and retrieve structured safety reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kitchen videos or video URLs may be processed by the provider's cloud service. <br>
Mitigation: Use only with informed consent and review retention, access, and privacy handling before analyzing home, elder-care, or nursing-setting footage. <br>
Risk: The skill can silently create or reuse a local identity and store authentication tokens locally. <br>
Mitigation: Review token storage, workspace access, account deletion or reset behavior, and cleanup procedures before installation or shared-workspace use. <br>
Risk: Stove-left-on alerts and valve-shutdown suggestions may affect safety-critical household decisions. <br>
Mitigation: Treat outputs as auxiliary monitoring, verify alerts through human follow-up, and apply site-approved emergency response procedures before relying on automation. <br>


## Reference(s): <br>
- [Kitchen stove left-on API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured JSON report content, status messages, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local kitchen media or video URLs, can query cloud report history, and can optionally write the report output to a file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
