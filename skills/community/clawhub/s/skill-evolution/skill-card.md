## Description: <br>
Meta-skill for interactively evolving other skills through directed improvements or source-guided capability fusion, with backup and rollback safeguards before edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pillar-wang](https://clawhub.ai/user/pillar-wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to improve selected installed skills through guided direction selection, proposed diffs, testing prompts, and rollback-aware retention decisions. It also supports absorbing useful patterns from other skills, documents, or conversation experience into a target skill after user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify selected installed skills and use git operations. <br>
Mitigation: Review each proposed diff before approval, test the changed skill in a real scenario, and use the documented backup and rollback flow if results are unsatisfactory. <br>
Risk: Backup and log files may retain private skill content, document excerpts, or conversation-derived details. <br>
Mitigation: Avoid providing sensitive sources unless needed, and review or remove .skill-backups logs and backup files when they contain private material. <br>
Risk: Fusion from other skills, documents, or conversation experience may introduce conflicting or misleading guidance. <br>
Mitigation: Require user confirmation for selected sources and conflicts, keep frontmatter unchanged, and rescan or review the target skill before deployment. <br>


## Reference(s): <br>
- [Skill Evolution on ClawHub](https://clawhub.ai/pillar-wang/skill-evolution) <br>
- [Publisher Profile](https://clawhub.ai/user/pillar-wang) <br>
- [Evolution Directions](references/evolution-directions.md) <br>
- [Rollback and Fusion Resources](references/resources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured choices, tables, diffs, code blocks, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create skill backup files, logs, and git commands when the user approves changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
