## Description: <br>
Dispatch coding tasks to tmux sessions via Sandboxer, including spawning Claude Code, Gemini, OpenCode, bash, or lazygit sessions in workspace repos, monitoring progress, and sending commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chriopter](https://clawhub.ai/user/chriopter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to dispatch and supervise coding work in tmux sessions on dedicated AI machines where workspace access and local terminal control are expected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad shell, file, and terminal control through a localhost Sandboxer service without clear containment. <br>
Mitigation: Install only on a dedicated, isolated machine or container that is fully controlled by the operator. <br>
Risk: Use on shared systems, personal desktops, production servers, or credential-bearing environments could expose sensitive workspace data or terminal control. <br>
Mitigation: Avoid shared or sensitive environments unless strong local isolation, least-privilege accounts, and authentication around the Sandboxer service are added. <br>
Risk: The artifact states that localhost access requires no authentication, increasing the impact of local compromise or unintended local access. <br>
Mitigation: Restrict local access to trusted users and add authentication or network isolation before relying on the service in higher-risk environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chriopter/sandboxer-tmux) <br>
- [Publisher profile](https://clawhub.ai/user/chriopter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No fixed output schema; commands target local Sandboxer HTTP endpoints and tmux sessions.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
