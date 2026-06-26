## Description: <br>
EVR Framework - Execute-Verify-Report. Force AI to actually do, then verify, then report so completion claims are backed by evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to require real execution, independent verification, and evidence-based reporting before an agent claims a task is complete. It is intended for workflows such as file changes, command execution, scheduled jobs, package installation, service checks, repository actions, and outgoing messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage agents to perform real local or external actions from broad completion and verification triggers. <br>
Mitigation: Require explicit confirmation before commands, scheduled jobs, file changes, outgoing messages, or other actions with external effects. <br>
Risk: The security review flagged the release for careful review because action boundaries are not clearly limited. <br>
Mitigation: Review the skill text before installation and grant only the tool permissions needed for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub EVR Framework release page](https://clawhub.ai/aptratcn/xiaobai-evr-framework) <br>
- [Skill source artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with verification checklists, examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the agent to report evidence from verification steps before claiming completion.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
