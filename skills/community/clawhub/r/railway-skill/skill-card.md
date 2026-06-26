## Description: <br>
Deploy and manage applications on Railway.app, including projects, services, logs, environment variables, and databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leicao-me](https://clawhub.ai/user/leicao-me) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for Railway CLI guidance when deploying projects, linking services, managing environments, checking logs, setting variables, and working with databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide production infrastructure actions such as deploys, SSH or remote commands, database changes, domain changes, and deletes. <br>
Mitigation: Require explicit approval before high-impact Railway commands, and confirm the active project, environment, and service before execution. <br>
Risk: Broad Railway access can increase blast radius if an agent runs commands in the wrong account or environment. <br>
Mitigation: Use least-privileged Railway access where possible and review generated commands before running them. <br>


## Reference(s): <br>
- [Railway Documentation](https://docs.railway.com) <br>
- [Railway CLI Reference](https://docs.railway.com/reference/cli-api) <br>
- [Railway Templates](https://railway.app/templates) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Railway CLI binary and appropriate Railway access before commands can be run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
