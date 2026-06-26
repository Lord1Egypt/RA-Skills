## Description: <br>
Standardized workspace directory layout for multi-agent OpenClaw deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaixi](https://clawhub.ai/user/zaixi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to standardize where agents create, exchange, audit, and clean files in multi-agent OpenClaw workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional apply command can move local workspace files when run in execute mode. <br>
Mitigation: Run the dry run first, confirm the workspace path, and review every proposed move before using execute mode. <br>
Risk: The workspace convention treats files/tmp/ and processed inbox/outbox items as disposable. <br>
Mitigation: Do not place secrets or important originals in disposable locations unless that handling is intended. <br>


## Reference(s): <br>
- [Directory Layout Reference](references/layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and local Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run audit behavior and an optional execute mode for applying workspace layout changes.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
