## Description:

Provides a Chinese-language demo skill that replies with basic skill, runtime, and workspace context information.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[agentsignals](https://clawhub.ai/user/agentsignals)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to test ClawHub and OpenClaw skill installation, invocation, and release workflow behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may display the workspace path and runtime details in chat output.

Mitigation: Run it only where exposing workspace and environment information to the active chat is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentsignals/skills/test-skill-demo)
- [Publisher profile](https://clawhub.ai/user/agentsignals)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown chat replies with a structured execution result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies are in Chinese and may include runtime details such as workspace path, timestamp, and Node.js version.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, index.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
