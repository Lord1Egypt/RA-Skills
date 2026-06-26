## Description: <br>
Analyzes thermal-imaging videos of multi-person gatherings to flag relative skin-temperature anomalies against the group average and recommend thermometer recheck without making a medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and smart-home or facility operators use this skill to analyze thermal camera video from family, meeting, kindergarten, or nursing-home gathering areas and produce relative temperature anomaly alerts plus report history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send thermal or video footage and persistent identifiers to external services. <br>
Mitigation: Use only with consent from recorded people, approved service endpoints, and documented upload, retention, deletion, and history-access controls. <br>
Risk: The security review notes under-disclosed account creation, token storage, and persistent identifier handling. <br>
Mitigation: Do not reuse an API key as a user identifier; review configuration and token storage before installation. <br>
Risk: The security review reports broader remote analysis behavior than the fever-screening description suggests. <br>
Mitigation: Limit use to the documented thermal fever-screening workflow and review generated reports before taking action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-thermal-fever-screening-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON report output and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report links and recommends calibrated thermometer recheck; requires thermal video input and open-id.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
