## Description:

测试-史新超

This skill is ready for commercial/non-commercial use.

## Publisher:

[roarday](https://clawhub.ai/user/roarday)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to send general questions to a third-party streaming Q&A API and return the resulting answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User questions are sent to a third-party service.

Mitigation: Do not submit secrets, personal data, proprietary text, or sensitive files through this skill.

Risk: The security summary flags the skill as a broad auto-triggering Q&A wrapper with unclear name, description, consent language, and credential handling.

Mitigation: Review the skill carefully before installing and confirm that its trigger behavior, user consent expectations, and provider setup are acceptable.

Risk: Credential setup is unclear because the script does not appear to load the documented API_KEY environment variable.

Mitigation: Verify the API provider and credential handling before execution or deployment.

## Reference(s):

- [API specification](references/api_spec.md)
- [ClawHub skill page](https://clawhub.ai/roarday/skills/shixinchao)
- [JointPilot async chat API](https://developer.jointpilot.com/v1/api/async_chat/completions/)
- [JointPilot file upload API](https://developer.jointpilot.com/v1/api/async_chat/api_upload_file/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown, with shell commands when explaining invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns answers from a third-party API; response quality and availability depend on that provider.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
