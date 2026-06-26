## Description: <br>
Audit and maintain workspace file structure, memory quality, and project documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SteveMichael001](https://clawhub.ai/user/SteveMichael001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit OpenClaw workspaces, check memory and project documentation hygiene, and generate prioritized local reports. When explicitly enabled, it can apply low-risk fixes such as consolidating timestamped memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill audits local workspace files and writes a local hygiene report. <br>
Mitigation: Install only for workspaces where local memory and project files may be audited, and review the generated report before acting on recommendations. <br>
Risk: When fixes are explicitly enabled, the skill can change memory files by consolidating timestamped entries. <br>
Mitigation: Run first without --fix, review the report, and enable --fix only for intended workspaces where memory-file consolidation is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SteveMichael001/workspace-hygiene) <br>
- [Audit Rules](audit.md) <br>
- [Memory Format](memory-format.md) <br>
- [RAG Index](rag-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with console text and suggested shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write projects/system/hygiene-YYYY-MM-DD.md; --fix can consolidate timestamped memory files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
