## Description: <br>
This skill helps agents manage validation rules, rule groups, and validation scenes for invoice verification through a Node.js CLI that prepares and sends configured API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[12266601032](https://clawhub.ai/user/12266601032) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to create, query, update, enable, disable, and delete invoice validation rules, rule groups, and validation scenes. It is intended for administering an existing validation-rule service with configured credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, enable, disable, or delete remote business validation rules. <br>
Mitigation: Use a least-privileged token, test changes in a non-production environment first, and manually confirm each write or delete action before execution. <br>
Risk: Access tokens may be exposed if stored in broadly discoverable config.json files. <br>
Mitigation: Prefer environment variables or tightly scoped configuration files and avoid committing credentials. <br>
Risk: Configured API endpoints may use plain HTTP. <br>
Mitigation: Use HTTPS endpoints where available and verify the target base URL before running commands. <br>


## Reference(s): <br>
- [Validation Rule Data Model](references/data-model.md) <br>
- [Validation Rule Usage Examples](references/examples.md) <br>
- [ClawHub Skill Release](https://clawhub.ai/12266601032/validation-rule-management) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured validation-rule service base URL and access token.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
