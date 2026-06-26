## Description: <br>
Install and use the RunAPI CLI as the universal execution layer for RunAPI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, authenticate, inspect, and automate RunAPI CLI workflows from an agent, terminal, server, or CI job. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an optional RunAPI API key and may rely on saved CLI authentication. <br>
Mitigation: Avoid pasting API keys into commands, prefer environment variables or stdin-based token import, and protect saved RunAPI configuration. <br>
Risk: The skill documents a remote shell installer for server or CI installation. <br>
Mitigation: Prefer the Homebrew install path when available and use the remote installer only when the target runtime needs it. <br>
Risk: The skill can install itself into other agent runtimes. <br>
Mitigation: Run agent-runtime install commands only for runtimes that should be modified. <br>


## Reference(s): <br>
- [RunAPI CLI ClawHub release](https://clawhub.ai/runapi-ai/runapi-cli) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [RunAPI models homepage](https://runapi.ai/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON request bodies, CLI stdout and stderr behavior, environment variables, and agent-runtime install targets.] <br>

## Skill Version(s): <br>
0.2.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
