## Description: <br>
Zipsa helps agents route sensitive prompts through a local privacy gateway that redacts identity, secrets, and proprietary context before using cloud LLMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sulgik](https://clawhub.ai/user/sulgik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams handling PII, health records, credentials, or internal business information use Zipsa to keep sensitive context local while still getting cloud-model assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles PII, health records, credentials, and business secrets through a local gateway whose source and configuration must be trusted. <br>
Mitigation: Install only after verifying the Zipsa server source and configuration, and bind the gateway to a trusted local endpoint. <br>
Risk: Cloud-bound prompts may still expose sensitive context if redaction or reformulation is misconfigured. <br>
Mitigation: Test redaction with representative sensitive prompts before production use and review results before sending real data. <br>
Risk: Admin features describe persistence and external alert forwarding that could expose logs or incident data. <br>
Mitigation: Review logging, retention, and alert-channel settings; disable or restrict Slack, email, Teams, webhook, SIEM, or SOAR forwarding unless needed. <br>


## Reference(s): <br>
- [Zipsa Technical Reference](references/README.md) <br>
- [Zipsa Admin Console Specification](references/admin-dashboard.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls] <br>
**Output Format:** [Markdown with configuration snippets and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local endpoint settings, session_id usage, and privacy routing guidance.] <br>

## Skill Version(s): <br>
0.4.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
