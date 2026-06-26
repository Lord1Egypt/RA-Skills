## Description: <br>
Audit and maintain workspace file structure, memory quality, and project documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SteveMichael001](https://clawhub.ai/user/SteveMichael001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to audit OpenClaw workspaces for file placement, memory hygiene, and missing project documentation. It produces a prioritized hygiene report and can optionally consolidate timestamped memory files when explicitly run with --fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local workspace memory, project folders, and documentation. <br>
Mitigation: Run it only against the intended workspace and review the generated hygiene report before acting on recommendations. <br>
Risk: The optional --fix mode can merge timestamped memory-file content into date-based files. <br>
Mitigation: Use --fix only when local memory-file consolidation is acceptable; review retained source files and the reported fixes afterward. <br>


## Reference(s): <br>
- [Workspace Hygiene Publish on ClawHub](https://clawhub.ai/SteveMichael001/workspace-hygiene-publish) <br>
- [Audit Rules](audit.md) <br>
- [Memory Format](memory-format.md) <br>
- [RAG Index](rag-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with terminal summary and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a hygiene report under projects/system; optional --fix mode appends timestamped memory content into date-based files while retaining source files for manual cleanup.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
