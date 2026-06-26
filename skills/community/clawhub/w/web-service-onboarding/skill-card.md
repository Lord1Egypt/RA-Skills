## Description: <br>
Autonomous signup for external web services through browser automation, email verification, API key generation, and secure storage in 1Password. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to onboard accounts for explicitly named external web services, complete verification flows, create API credentials, store them in 1Password, and wire local environment configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create external service accounts and credentials with broad operational impact. <br>
Mitigation: Use it only for explicitly named services and confirm account creation, paid tier selection, API key creation, and credential storage before execution. <br>
Risk: The skill writes generated credentials to 1Password and may edit local environment configuration. <br>
Mitigation: Review the target vault, item names, credential fields, and .env changes before applying them. <br>
Risk: The skill requires signup metadata to be logged to Notion. <br>
Mitigation: Install and run only if the user accepts the mandatory Notion logging requirement for service name, email, date, and purpose. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/web-service-onboarding) <br>
- [Publisher profile](https://clawhub.ai/user/nissan) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account setup steps, browser automation patterns, API key creation guidance, 1Password storage commands, and environment configuration edits.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
