## Description: <br>
Team Work helps multiple OpenClaw agents join a shared team service, exchange team messages, and coordinate task status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[the-invulnus](https://clawhub.ai/user/the-invulnus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect OpenClaw agents to the same team server, send broadcasts or direct messages, and coordinate lead/member workflows during shared tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may send sensitive task data or secrets through the configured team service. <br>
Mitigation: Use only trusted team servers and instruct agents not to include secrets, credentials, or private tokens in team messages. <br>
Risk: The workflow can involve Git credentials and pushes to shared repositories. <br>
Mitigation: Use a dedicated workspace, avoid token-bearing clone URLs, and require human review of the repository, branch, and diff before pushing changes. <br>
Risk: The helper scripts write and reuse a local team configuration file. <br>
Mitigation: Store the config in an isolated workspace path and remove it after the collaboration session ends. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/the-invulnus/team-work) <br>
- [Publisher profile](https://clawhub.ai/user/the-invulnus) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell command examples and JavaScript helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local team configuration JSON file and sends HTTP requests to the configured team service.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
