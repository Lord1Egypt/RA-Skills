## Description: <br>
Provides a simple demo skill that replies with basic status and runtime context for testing ClawHub and OpenClaw skill workflows. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[agentsignals](https://clawhub.ai/user/agentsignals) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this demonstration skill to test skill installation, publication, and execution flows. It shows a basic reply sequence and reports simple runtime context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prints basic runtime context, including the workspace path and Node.js version, into the conversation. <br>
Mitigation: Use it for demo or learning contexts and avoid running it where workspace path disclosure would expose sensitive project or environment details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentsignals/test-skill-demo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown replies with a JSON-compatible execution result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the current timestamp, workspace path when provided, and Node.js version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
