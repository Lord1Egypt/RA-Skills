## Description:

Sensitive information real-time protection skill that automatically detects, alerts, and handles sensitive data in user interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leefj0606](https://clawhub.ai/user/leefj0606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scan conversation text, files, or custom inputs for credentials, personal information, and business-sensitive patterns before sharing or submitting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser interaction helper watches chat DOM content, injects controls, and can submit messages through broad UI selectors.

Mitigation: Disable or omit the browser helper unless that automation is explicitly needed and accepted by the deploying user.

Risk: Detected values can appear verbatim in markdown output, CLI output, logs, chat history, or page globals.

Mitigation: Use desensitization output for real sensitive data and avoid scanning live secrets in shared or persistent environments.

Risk: Custom rule files control regex patterns loaded by the detector.

Mitigation: Load only trusted custom rule files and review patterns before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leefj0606/skills/sensitive-info-protection)
- [Publisher Profile](https://clawhub.ai/user/leefj0606)
- [Configuration Guide](references/configuration.md)
- [API Documentation](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown detection reports, CLI text output, Python API objects, and JSON rule configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detection reports may include matched sensitive values unless desensitization is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
