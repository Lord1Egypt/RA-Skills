## Description: <br>
Automates restaurant AI inspections by managing an Ezviz intelligent agent, capturing device snapshots, and analyzing food safety, hygiene, and compliance conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsygcn](https://clawhub.ai/user/wsygcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant operators, compliance teams, and developers use this skill to run automated inspections over authorized Ezviz camera devices and review structured AI analysis of food safety, hygiene, staff practices, and compliance signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera snapshots and device identifiers are sent to Ezviz services for capture and AI analysis. <br>
Mitigation: Run only with authorization to inspect the configured cameras and confirm applicable workplace privacy, compliance, and data handling requirements before use. <br>
Risk: Ezviz app credentials grant access to device capture and agent operations. <br>
Mitigation: Use least-privilege Ezviz credentials, prefer environment variables over command-line secrets, avoid main account credentials, and rotate credentials regularly. <br>
Risk: The skill may create or reuse an Ezviz restaurant intelligent agent during execution. <br>
Mitigation: Review any created or selected Ezviz agent and ensure the account has sufficient quota and appropriate permissions before running the inspection workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wsygcn/test-restaurant-inspection) <br>
- [Ezviz token API documentation](https://open.ys7.com/help/81) <br>
- [Ezviz device capture API documentation](https://open.ys7.com/help/687) <br>
- [Ezviz AI analysis API documentation](https://open.ys7.com/help/5006) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Console logs with JSON-formatted inspection analysis and a plain-text inspection summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Ezviz app credentials and one or more device serials; uses a default 60 second analysis timeout and a 4 second delay between device captures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
