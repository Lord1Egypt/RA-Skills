## Description: <br>
Manages long OpenClaw agent conversations with tiered L1/L2/L3 context compression, memory tiering, cross-agent knowledge sharing, monitoring, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scorpioxyb](https://clawhub.ai/user/scorpioxyb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage long-running OpenClaw agent sessions by compacting context, organizing memories by retention tier, sharing selected knowledge across agents, and producing compression statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, rewrite, delete, archive, and share local OpenClaw conversation-derived data. <br>
Mitigation: Run dry-run or inspection modes first, keep restorable backups, and limit execution to workspaces where broad context management is intended. <br>
Risk: Hardcoded OpenClaw and shared-memory paths may affect the wrong local storage location or expose data across agents. <br>
Mitigation: Review and adjust paths before use, and add access controls or redaction before processing private, credential-bearing, or confidential sessions. <br>


## Reference(s): <br>
- [Tiered Context Manager Architecture](references/architecture.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/scorpioxyb/tiered-context-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript API examples, and generated reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, rewrite, compact, archive, and share local OpenClaw conversation and memory files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
