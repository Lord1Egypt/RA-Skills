## Description: <br>
Generates customized incident response playbooks tailored to organizational assessment data and security requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operations centers, incident response teams, compliance officers, and security architects use this skill to generate organization-specific incident response playbooks from assessment data, security controls, risk profiles, compliance frameworks, and threat priorities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted assessment data may include sensitive organization details, critical systems, incident-response contacts, or security posture information. <br>
Mitigation: Verify the API operator, privacy terms, retention and logging practices, and authorization to share the data before using real organization information. <br>
Risk: Generated response procedures, escalation paths, legal considerations, or notification timelines may be incomplete or unsuitable for a specific organization. <br>
Mitigation: Have security, incident response, compliance, or legal staff review generated playbooks before operational use. <br>
Risk: Testing with realistic data may expose secrets or unnecessary personal contact information. <br>
Mitigation: Use redacted placeholders for testing and avoid submitting secrets or unnecessary personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-ir-playbook-generator) <br>
- [Incident Response Playbook Generator API documentation](https://api.mkkpro.com:8118/docs) <br>
- [Incident Response Playbook Generator API route](https://api.mkkpro.com/security/ir-playbook-generator) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON response containing playbook sections, roles, communication templates, escalation procedures, legal considerations, and contact lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated playbooks should be reviewed by security or legal staff before operational use.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
