## Description: <br>
Send SMS jobs and check per-recipient delivery status through the Retarus SMS for Applications REST API across the eu, de1, and de2 datacenters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aeggerd](https://clawhub.ai/user/aeggerd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare or validate Retarus SMS4A payloads, send SMS jobs, and retrieve per-recipient delivery status for a job ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real SMS messages through a Retarus account. <br>
Mitigation: Install it only on agents authorized to operate that account and require a dry run or human approval showing recipients, message text, datacenter, and payload before sending. <br>
Risk: Retarus credentials could be exposed if passed or stored carelessly. <br>
Mitigation: Prefer managed secrets, environment variables, or access-controlled secret files, and avoid command-line passwords except for local testing. <br>
Risk: Unrestricted network access could allow unintended SMS4A traffic. <br>
Mitigation: Restrict egress to the documented Retarus SMS4A hosts where possible. <br>


## Reference(s): <br>
- [Retarus SMS4A Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/aeggerd/retarus-sms4a) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text with bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Retarus datacenter selection, dry-run output, created job IDs, and per-recipient delivery status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
