## Description: <br>
Meta-cognitive self-learning system - Automated skill evolution based on predictive coding and value-driven mechanisms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[86293073](https://clawhub.ai/user/86293073) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to create, execute, analyze, list, save, and load self-evolving OpenClaw skills through CLI and MCP-style tools. It supports local experimentation with residual analysis, reflection triggers, experience replay, and persisted skill state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store and reuse task context as learned skill state. <br>
Mitigation: Use a non-sensitive test workspace first and configure an explicit storage directory before use. <br>
Risk: Persisted or mutated skill state can affect later executions. <br>
Mitigation: Require manual review before executing, saving, loading, or clearing learned skill state. <br>
Risk: Server-mode operation may depend on runtime components that were not present in the release artifact. <br>
Mitigation: Verify the Python core and MCP server components before enabling server mode. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/86293073/self-evolving-skill-1-0-2) <br>
- [Project homepage](https://github.com/whtoo/self-evolving-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, JSON-like tool results, TypeScript code interfaces, shell commands, and OpenClaw configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may persist and reuse learned skill state in local filesystem storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata); artifact package version is 1.0.2 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
