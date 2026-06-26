## Description: <br>
Helps an agent consolidate multiple overlapping skills into one distilled skill while preserving traceability, resolving conflicts with user confirmation, and validating the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill when two or more local agent skills overlap enough to create routing ambiguity, duplicated context, or maintenance overhead. It guides collection, cross-analysis, user confirmation, generation, and post-generation validation of a distilled replacement skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose persistent edits to local skill files, including scripts and shared skill content. <br>
Mitigation: Review proposed diffs carefully before approving changes, especially when scripts, external searches, installs, or shared/team skills are involved. <br>


## Reference(s): <br>
- [Skill Distill on ClawHub](https://clawhub.ai/lanyasheng/skill-distill) <br>
- [Publisher profile](https://clawhub.ai/user/lanyasheng) <br>
- [Distillation checklist](references/distillation-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown plans and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Distilled SKILL.md output is constrained to 500 lines, with longer material moved to references.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
