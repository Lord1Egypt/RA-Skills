## Description: <br>
Agent Init initializes OpenClaw agent workspace Markdown files through an interview-driven workflow for new agents, behavior customization, environment setup, and host or container workspace configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szsip239](https://clawhub.ai/user/szsip239) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to interview for agent requirements, draft workspace instruction files, configure Python and uv guidance, and initialize either host-based or container-based OpenClaw workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional uv setup path may execute a remote installer script. <br>
Mitigation: Run the installer only with explicit user approval, and prefer a trusted package manager or reviewed installer when available. <br>
Risk: Generated workspace Markdown can persist incorrect instructions or expose sensitive information because OpenClaw injects workspace files into future agent context. <br>
Mitigation: Review every generated file before approving writes, keep secrets out of workspace Markdown, and keep files concise. <br>
Risk: Using the wrong host path, container ID, or agent workspace can update the wrong OpenClaw workspace. <br>
Mitigation: Verify the instance type, workspace path, container ID, and agent ID before writing or verifying files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szsip239/whois) <br>
- [OpenClaw workspace guide](artifact/references/openclaw-workspace.md) <br>
- [OpenClaw workspace templates](artifact/references/templates.md) <br>
- [uv installer](https://astral.sh/uv/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown file drafts with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files should be shown for user confirmation before writing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
