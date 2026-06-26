## Description: <br>
Displays and summarizes an existing postoperative rehabilitation plan by phase, goal, tasks, and precautions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External patient-facing users and care-plan agents use this skill to view an existing postoperative rehabilitation plan, summarize current phase goals, tasks, and precautions, and pass plan context to downstream task skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patient rehabilitation-plan content and the bearer appkey are sent to a remote medical model endpoint. <br>
Mitigation: Use only when the endpoint and appkey handling are approved for the patient-data workflow, and make clear that plan contents may leave the local environment. <br>
Risk: Office, PDF, and image inputs can add parsing and containment risk when supplied from untrusted sources. <br>
Mitigation: Prefer JSON or trusted simple files; sandbox and resource-limit the runtime before accepting untrusted documents or images. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unisound-llm/unisound-rehab-plan-view) <br>
- [CareKit care plan and task model](https://github.com/carekit-apple/CareKit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [UTF-8 JSON containing structured plan data and a Markdown text field] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey bearer token and sends rehabilitation-plan content to a remote medical model endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
