## Description: <br>
Prepare a customer record field for reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxt-ai](https://clawhub.ai/user/wxt-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or reporting operators use this skill to prepare a concise customer record field value for routine reporting exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste real sensitive customer record data into an agent session while preparing report fields. <br>
Mitigation: Use synthetic or redacted customer notes unless the operator is approved to process the underlying data in the agent environment. <br>
Risk: A prepared field value could be copied into a report without confirming it matches the current export requirement. <br>
Mitigation: Review the source record note or report requirement before using the returned field value in a customer-facing or operational report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxt-ai/skills/record-export-field-identifier) <br>
- [Publisher profile](https://clawhub.ai/user/wxt-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text field value] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a concise field value; no commands, credential requests, private-file access, or external service calls are described by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
