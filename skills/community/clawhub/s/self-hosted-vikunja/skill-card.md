## Description: <br>
Interact with a self-hosted Vikunja task management instance via its REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bydavid](https://clawhub.ai/user/bydavid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage tasks, projects, labels, due dates, reminders, and recurring work in a trusted self-hosted Vikunja instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable authentication tokens or credentials can be exposed through command output, environment variables, or local config files. <br>
Mitigation: Use only trusted Vikunja servers, avoid logging or sharing the login token, and restrict permissions on config and token files. <br>
Risk: Task or project deletes and bulk updates can change or remove user data. <br>
Mitigation: Require explicit user confirmation before delete operations or bulk changes, and identify the affected task or project IDs before execution. <br>


## Reference(s): <br>
- [Vikunja API Reference](references/api_reference.md) <br>
- [ClawHub release page](https://clawhub.ai/bydavid/self-hosted-vikunja) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a configured Vikunja REST API through the bundled helper script.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
