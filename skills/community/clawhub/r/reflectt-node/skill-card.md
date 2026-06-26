## Description: <br>
Local team collaboration server on localhost:4445 managing tasks, messaging, presence, inbox, team health, and a dashboard through HTTP endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryancampbell](https://clawhub.ai/user/ryancampbell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-agent work through a local collaboration service, including task assignment, status updates, chat, inbox acknowledgements, presence, and team health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local task service can become a persistent instruction channel for agents. <br>
Mitigation: Install and use this skill only with a reflectt-node service you intentionally run and trust on localhost:4445, and have agents verify important or surprising tasks with the user before acting. <br>
Risk: Tasks and messages may expose sensitive information if secrets are placed in chat or task descriptions. <br>
Mitigation: Avoid placing secrets in chat messages, task titles, or task descriptions, and confirm who can write tasks and messages before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryancampbell/reflectt-node) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP endpoint examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill expects a trusted local reflectt-node service at http://127.0.0.1:4445 and stores service data under ~/.reflectt/data/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
