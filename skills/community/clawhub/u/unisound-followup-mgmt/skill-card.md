## Description: <br>
Generates structured post-health-exam follow-up plans, including timing, recheck items, departments, target values, health coaching points, and patient-facing follow-up notices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Health exam centers and health management organizations use this skill to turn exam reports into follow-up schedules and clear patient notifications. It supports post-exam care coordination while keeping final medical decisions with clinicians. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installed files may differ from the reviewed listing or expected artifact contents. <br>
Mitigation: Inspect SKILL.md and scripts before use, and grant credentials, filesystem access, and network access only after confirming the files match the expected release. <br>
Risk: The skill processes health exam information and sends prompts to the configured medical model endpoint. <br>
Mitigation: De-identify direct personal identifiers before use and limit inputs to the minimum health data needed to create a follow-up plan. <br>
Risk: Generated follow-up plans may be mistaken for definitive medical decisions. <br>
Mitigation: Treat outputs as health management guidance and have clinicians confirm diagnosis, treatment, and visit decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/unisound-llm/unisound-followup-mgmt) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Internal medical model API base](https://maas-api.hivoice.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, shell commands, guidance] <br>
**Output Format:** [JSON followed by a human-readable follow-up notice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the generated follow-up plan to a user-specified output file or print it to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
