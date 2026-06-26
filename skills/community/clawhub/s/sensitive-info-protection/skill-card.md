## Description: <br>
Sensitive Info Protection detects sensitive data in user interactions, supports custom detection rules, and helps users review or desensitize credentials, personal information, and business secrets before sharing them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeeFJ0606](https://clawhub.ai/user/LeeFJ0606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scan conversation or file content for credentials, personal data, and business secrets, then review or desensitize findings before sending or storing the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Detection reports may show raw secrets or personal data in the agent transcript. <br>
Mitigation: Prefer desensitized output for sharing or logging, and review detection reports before copying them into downstream systems. <br>
Risk: The bundled browser helper can monitor chat content and submit chat messages after button clicks. <br>
Mitigation: Review the helper before installation and avoid enabling it in sensitive workflows unless that UI automation is acceptable. <br>


## Reference(s): <br>
- [API Documentation](references/api.md) <br>
- [Configuration Guide](references/configuration.md) <br>
- [ClawHub skill page](https://clawhub.ai/LeeFJ0606/sensitive-info-protection) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown detection reports, desensitized text, Python examples, CLI commands, and JSON rule configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Detection reports may include raw matched values unless desensitization output is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
