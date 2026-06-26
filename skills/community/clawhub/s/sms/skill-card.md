## Description: <br>
Manage SMS templates with variable substitution and formatting for preparing bulk messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators preparing recurring SMS message text use this skill to create, list, preview, substitute variables in, and export local message templates before bulk messaging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Template content may include sensitive personal data or secrets in local files. <br>
Mitigation: Avoid storing sensitive customer data or credentials in templates and periodically review ~/.local/share/sms/. <br>
Risk: Exporting templates may overwrite or copy data to an unintended destination. <br>
Mitigation: Double-check export destinations before running export commands. <br>
Risk: The helper has weak argument handling and placeholder-style command output. <br>
Mitigation: Review generated commands and preview message text before relying on it in a bulk messaging workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/sms) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text command output and local template data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores template data locally under ~/.local/share/sms/ and may export templates to a user-provided file path.] <br>

## Skill Version(s): <br>
3.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
