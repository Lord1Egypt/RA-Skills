## Description: <br>
Auto-generate project workflow config (docs/workflow.md) from existing PRD and CLAUDE.md with zero questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill after project scaffolding to generate workflow documentation, capture TDD and verification expectations, and add a workflow reference to CLAUDE.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies project workflow documentation and CLAUDE.md. <br>
Mitigation: Run it only from the intended project root and review the resulting diffs before accepting changes. <br>
Risk: Optional solograph MCP tools may share project context with configured integrations. <br>
Mitigation: Disable the optional solograph MCP tools when that project context should not be shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortunto2/solo-setup) <br>
- [Publisher profile](https://clawhub.ai/user/fortunto2) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and concise setup summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates docs/workflow.md and may update CLAUDE.md.] <br>

## Skill Version(s): <br>
2.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
