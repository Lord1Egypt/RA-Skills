## Description: <br>
Intercepts SSH exec calls and pauses them for explicit user approval, with one-time and session-wide approval modes plus automatic session cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanbo92](https://clawhub.ai/user/yanbo92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and configure the ssh-guard OpenClaw plugin so SSH command execution requires explicit user approval. It guides language selection, plugin loading, and direct-message session isolation settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session-wide SSH approval can allow later SSH commands without another approval prompt in the same approval scope. <br>
Mitigation: Prefer one-time SSH approvals, and avoid session-wide approval in sensitive environments. <br>
Risk: Approval state can be affected by subagent inheritance and session isolation boundaries. <br>
Mitigation: Review the installation when using subagents, and configure direct-message sessions with per-channel-peer or per-account-channel-peer isolation. <br>
Risk: SSH command snippets may expose passwords or other secrets in logs or approval prompts. <br>
Mitigation: Avoid putting passwords or secrets directly in SSH command lines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanbo92/ssh-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation and configuration guidance for an OpenClaw plugin with English and Chinese approval prompt options.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
