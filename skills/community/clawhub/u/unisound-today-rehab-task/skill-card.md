## Description: <br>
Shows and records today's postoperative rehabilitation tasks from an existing care plan, with structured status data and Markdown reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patients or care teams use this skill to filter an existing rehabilitation plan for a target date, see what must be completed today, and record completed, pending, or skipped task states. It does not adjust clinical training intensity or generate a new rehabilitation plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive rehabilitation task details may be sent to a remote model API. <br>
Mitigation: Use only in environments where that remote processing is approved, and avoid uploading real patient documents without consent and data-handling assurances. <br>
Risk: Broad PDF, Office, and image inputs may require conversion or OCR on untrusted files. <br>
Mitigation: Prefer JSON or CSV inputs when possible, and run document conversion in a sandbox with resource limits. <br>
Risk: Generated reminder text could be mistaken for clinical plan changes. <br>
Mitigation: Treat output as a reminder and status summary for an existing plan; clinical staff should review any medical interpretation before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-today-rehab-task) <br>
- [CareKit](https://github.com/carekit-apple/CareKit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, structured data, guidance] <br>
**Output Format:** [UTF-8 JSON containing structured task data and Markdown reminder text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey for the remote medical model API; JSON input works without optional document conversion dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
