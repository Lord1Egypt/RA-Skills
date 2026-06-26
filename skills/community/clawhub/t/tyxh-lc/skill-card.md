## Description: <br>
Queries patient information by patient number or ID through a curl-accessible API endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lc-nian](https://clawhub.ai/user/lc-nian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and authorized operators can use this skill to help an agent retrieve patient details when a user provides a patient identifier. Because the data is sensitive, use should be limited to approved patient-record lookup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query sensitive patient details from an unauthenticated external API. <br>
Mitigation: Install only for authorized patient-system users after lawful approval, and require authentication, authorization, audit logging, rate limiting, data minimization, and explicit confirmation before patient-record lookups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lc-nian/tyxh-lc) <br>
- [Patient information API endpoint](https://kjcrmcs.tianyuxh.com:8107/task/agent_test/getPatientInfo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl with a patient_id query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
