## Description: <br>
Explains how to use OpenClaw in a local environment for configuration, workspace files, skills, setup troubleshooting, and common step-by-step tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[selena000](https://clawhub.ai/user/selena000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local OpenClaw configuration, workspace notes, skills, and logs, then get concise guidance or small verified changes for setup and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to inspect local OpenClaw configuration, workspace notes, skills, and logs that can contain sensitive local context. <br>
Mitigation: Ask for read-only guidance when changes are not wanted, and review any local file content before sharing it outside the environment. <br>
Risk: When a fix is explicitly requested, the skill may guide small edits to OpenClaw files. <br>
Mitigation: Review proposed changes and validate the result before relying on the updated configuration or skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/selena000/use-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise local inspection steps and small file-change guidance when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
