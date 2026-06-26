## Description: <br>
Diagnoses always-loaded workspace context files such as AGENTS.md, SOUL.md, USER.md, MEMORY.md, and TOOLS.md to reduce context bloat, find duplicate rules, identify misplaced content, and audit file roles before reorganization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lethehades](https://clawhub.ai/user/lethehades) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit workspace context files before reorganizing them. It produces prioritized diagnostics for duplicate rules, overweight sections, misplaced content, and suggested moves without automatically rewriting files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local workspace context and memory files that may contain sensitive preferences, environment details, or operating rules. <br>
Mitigation: Run it only in workspaces where this local read access is acceptable, and review generated reports before sharing them outside the workspace. <br>
Risk: The diagnostic report may suggest moving or trimming content that is still useful in always-loaded context. <br>
Mitigation: Treat findings as review prompts, not automatic edits; confirm each suggested move against the workspace's operating needs before changing files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lethehades/workspace-context-linter) <br>
- [rules](references/rules.md) <br>
- [report format](references/report-format.md) <br>
- [file roles](references/file-roles.md) <br>
- [move guidelines](references/move-guidelines.md) <br>
- [release minimal](references/release-minimal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain-text or Markdown-style diagnostic report, optionally written to a report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local workspace context files and may write a report when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
