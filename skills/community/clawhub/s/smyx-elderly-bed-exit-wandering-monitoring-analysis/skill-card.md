## Description: <br>
Identifies nighttime elder-safety events in monitoring video, including bed exit, prolonged wandering, and extended immobility, for nursing-home and at-home care scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, nursing-home staff, family monitors, and developers use this skill to analyze nighttime monitoring videos for bed-exit, wandering, immobility, and alert-worthy elder-safety events. It can also query cloud-stored historical monitoring reports for a provided user identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Elder-monitoring video, report queries, and a username or phone number may be sent to a remote Life Emergence service. <br>
Mitigation: Use only approved monitoring media and identifiers, obtain appropriate consent, and review the configured service endpoint before running analysis. <br>
Risk: The runtime may create local user records and store access tokens in SQLite. <br>
Mitigation: Run the skill in a dedicated workspace, avoid shared machines for sensitive use, and apply local data-retention and token-rotation controls. <br>
Risk: The analysis output is advisory and may not catch every safety-critical situation. <br>
Mitigation: Treat alerts and reports as care-support signals and require human confirmation for abnormal events or emergencies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-elderly-bed-exit-wandering-monitoring-analysis) <br>
- [Elderly Bed-Exit & Wandering Monitor API Reference](references/api_doc.md) <br>
- [Common Analysis API Reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and JSON-formatted analysis or report-listing output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote report export links when returned by the analysis service.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
