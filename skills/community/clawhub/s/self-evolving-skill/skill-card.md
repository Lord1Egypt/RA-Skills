## Description: <br>
Meta-cognitive self-learning system - Automated skill evolution based on predictive coding and value-driven mechanisms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whtoo](https://clawhub.ai/user/whtoo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to create, execute, analyze, list, save, and load adaptive skills through OpenClaw MCP tools and CLI-style workflows. It is intended to support self-learning behavior based on residual analysis, reflection triggers, experience replay, and value-gated updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists self-learning state that may include task context or embeddings. <br>
Mitigation: Set an explicit storage directory, inspect retention behavior, and avoid sensitive inputs until storage and deletion practices are reviewed. <br>
Risk: The skill can start or configure local helper/MCP code that may affect future agent behavior. <br>
Mitigation: Review MCP configuration before enabling auto-start and run the skill in a controlled local environment. <br>
Risk: The reviewed bundle references important Python core/server files that are not present. <br>
Mitigation: Confirm the missing files with the publisher before relying on the Python-backed behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/whtoo/self-evolving-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [INSTALLATION.md](artifact/INSTALLATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, code] <br>
**Output Format:** [JSON tool responses, console text, TypeScript interfaces, and Markdown documentation with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist skill state, embeddings, and execution statistics in a configured filesystem storage directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json, openclaw.yaml, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
