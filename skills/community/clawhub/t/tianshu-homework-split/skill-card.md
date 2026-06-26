## Description: <br>
Splits syllabus, assignment, or study requirement text into a numbered Markdown checklist for students. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students use this skill to turn course assignment instructions, syllabus requirements, or review outlines into a Markdown task checklist for Notion, Obsidian, or a to-do list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated checklist items can miss or misstate deadlines, optional work, or task boundaries in the original assignment text. <br>
Mitigation: Review the Markdown checklist against the original teacher requirements before relying on it. <br>
Risk: Using the file input mode processes local documents supplied by the user. <br>
Mitigation: Use --file only with documents the user intends to process, or use --text for pasted content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshengli0421/tianshu-homework-split) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands] <br>
**Output Format:** [Markdown checklist printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided UTF-8 files or pasted text, preserves deadline wording when detected, and includes a short self-check section.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
