## Description: <br>
Manage background coding agents in tmux sessions. Spawn Claude Code or other agents, check progress, get results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuba6112](https://clawhub.ai/user/cuba6112) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to launch, monitor, and collect work from coding agents running in persistent tmux sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent tmux-managed coding agents can run commands and change files with broad local authority. <br>
Mitigation: Use a disposable branch or sandbox, avoid sensitive repositories and secrets, monitor sessions with status.sh or tmux ls, and kill sessions when finished. <br>
Risk: Cloud agent sessions may use authenticated third-party CLIs and API credits. <br>
Mitigation: Verify which cloud CLIs are logged in before spawning sessions and choose local Ollama-backed agents when API spend or external processing is not intended. <br>
Risk: Untrusted task text can steer autonomous agents toward unwanted commands or edits. <br>
Mitigation: Review task prompts before launching agents and inspect generated changes before merging or deploying them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cuba6112/tmux-agents) <br>
- [Skill Homepage](https://clawdhub.com/skills/tmux-agents) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with shell commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces tmux session commands and status text for background coding-agent workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
