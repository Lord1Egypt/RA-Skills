## Description: <br>
Send emails securely without exposing SMTP passwords, powered by MGC Blackbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkeviny](https://clawhub.ai/user/zkeviny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external MCP users use this skill to send plain-text SMTP email through an MCP tool while retrieving SMTP credentials from a local MGC Blackbox vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad secret-backed SMTP sending power. <br>
Mitigation: Install only from a trusted publisher and use an SMTP account scoped to the intended sending purpose. <br>
Risk: Email sender, recipient, subject, and body may be sent without enough confirmation. <br>
Mitigation: Require an explicit preview and confirmation step before each email is sent. <br>
Risk: Credential selection can be controlled through MGC secret identifiers. <br>
Mitigation: Prefer a version or deployment wrapper that hardcodes or allowlists the permitted SMTP secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zkeviny/smtp-sender-secure) <br>
- [Publisher profile](https://clawhub.ai/user/zkeviny) <br>
- [Artifact README](artifact/readme.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Configuration instructions, Shell commands] <br>
**Output Format:** [JSON tool result with plain-text email content and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends plain-text email only; no attachments or HTML are supported in this version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
