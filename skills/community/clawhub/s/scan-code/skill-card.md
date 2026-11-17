## Description:

CodeGuard MCP is a real-time AI code security scanning skill for checking generated code for vulnerabilities, exposed secrets, and compliance issues during development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to submit code for vulnerability, secret, and compliance checks, and to request secure-fix guidance for identified issues. It is intended for development-time code security review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive source code or detected secrets may be uploaded to an external service during scanning.

Mitigation: Use only test or non-sensitive code unless the publisher provides clear terms for uploaded source, retention, deletion, and secret handling.

Risk: The required API key may be stored in a local plaintext .env file.

Mitigation: Avoid long-lived production keys, restrict the key where possible, and rotate any key or real secret that may have been submitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/scan-code)
- [Publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown summaries of API results, secure-fix guidance, and configuration prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw JSON fields from upstream scan responses when presenting findings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
