## Description: <br>
Submit learning insights to an organization's shared Feishu learning circle through a token-authenticated API configured by the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qyc314159](https://clawhub.ai/user/qyc314159) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and agents use this skill to turn learning insights into structured entries and submit them to a shared learning-circle server. It is intended for user-provided epiphanies, problem-solving notes, and research questions rather than private or sensitive content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided learning content to a configured shared server where content may be stored and removable only by an administrator. <br>
Mitigation: Submit only content appropriate for the shared system, avoid private or sensitive material, and confirm the server operator's retention and deletion practices. <br>
Risk: The bearer token in scripts/config.js grants access to the learning-circle API. <br>
Mitigation: Keep scripts/config.js private, do not publish the configured skill folder, and rotate the token through the administrator if it may have been exposed. <br>
Risk: Network requests depend on the configured api_base endpoint and token trust boundary. <br>
Mitigation: Use a trusted HTTPS api_base supplied by the administrator and install the skill only when the learning-circle server is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qyc314159/thu-epiphany-client) <br>
- [Publisher profile](https://clawhub.ai/user/qyc314159) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with command-line examples and JSON API submissions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submissions include a title, thoughts, optional URL, and optional source name.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
