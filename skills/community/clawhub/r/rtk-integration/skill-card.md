## Description: <br>
Integrate RTK (Rust Token Killer) to reduce LLM token consumption by 60-90% on shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DavydenkovM](https://clawhub.ai/user/DavydenkovM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install RTK, configure command filtering, and guide agents to use rtk-prefixed shell commands for lower context-window and token usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup path can run unpinned remote installation code and modify shell startup files. <br>
Mitigation: Prefer Homebrew or a pinned, reviewed RTK release; review any shell profile changes before relying on the installed environment. <br>
Risk: RTK filtering can hide complete command output needed for commits, pushes, installs, failures, or security-sensitive debugging. <br>
Mitigation: Use raw commands when full output is required, especially for security review, failing commands, or operations where exact output affects the decision. <br>


## Reference(s): <br>
- [RTK Integration on ClawHub](https://clawhub.ai/DavydenkovM/rtk-integration) <br>
- [RTK Command Reference](references/commands.md) <br>
- [RTK Configuration Guide](references/config.md) <br>
- [RTK GitHub Repository](https://github.com/rtk-ai/rtk) <br>
- [RTK Releases](https://github.com/rtk-ai/rtk/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash and TOML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance favors compressed RTK command output and may omit full raw command details unless explicitly needed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
