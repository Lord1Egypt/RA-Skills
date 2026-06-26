## Description: <br>
Analyze the current conversation history and local installed skills to identify missed skill triggers, overlapping or duplicate skills, weak metadata, stale or risky skills, and workflow gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangchenchen](https://clawhub.ai/user/zhangchenchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit local skill directories and the current conversation for trigger, metadata, duplication, safety, and workflow issues before choosing whether to fix, merge, delete, or keep findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews current conversation context and visible local skill directories, which may expose sensitive workspace details. <br>
Mitigation: Review the exact scope and paths before use, and provide only the conversation logs or directories needed for the audit. <br>
Risk: Audit recommendations may lead to skill edits, merges, or deletions after user approval. <br>
Mitigation: Require explicit user selections for Fix, Merge, Delete, or Keep and Skip, and confirm exact deletion targets when there is ambiguity. <br>


## Reference(s): <br>
- [Report Schema](references/report-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhangchenchen/skill-optimizer-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with findings and an action queue] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user choices before editing, merging, or deleting skills.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
