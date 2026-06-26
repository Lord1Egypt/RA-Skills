## Description: <br>
Use the acpx CLI to run coding agents over the Agent Client Protocol (ACP) instead of PTY scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route coding work through acpx-backed ACP clients such as Codex, Claude Code, Gemini CLI, Pi, and OpenCode. It helps agents select the intended local acpx runtime, inspect common commands, and follow the documented runtime policy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: acpx commands can launch coding agents that may read or modify files in local projects. <br>
Mitigation: Review acpx commands before execution and run them only in the intended workspace with the expected agent configuration. <br>
Risk: Manual experiments with npx acpx@latest may differ from the documented pinned local runtime. <br>
Mitigation: Use the plugin-local pinned acpx runtime for normal workflows and reserve latest-version checks for explicit upgrade testing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chaoyang78/stone-acpx) <br>
- [Upstream acpx Skill Reference](https://raw.githubusercontent.com/openclaw/acpx/main/skills/acpx/SKILL.md) <br>
- [Upstream acpx CLI Reference](https://raw.githubusercontent.com/openclaw/acpx/main/docs/CLI.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable payload is included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
