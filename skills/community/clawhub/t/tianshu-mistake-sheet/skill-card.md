## Description: <br>
Tianshu Mistake Sheet generates an empty Markdown mistake-notebook table or converts pipe-delimited mistake notes into a review table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and exam-prep users use this skill to create a structured Markdown mistake sheet for review planning. It is useful for converting typed notes in the form `question fragment|mistake reason|knowledge point` into a table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Node script can read a path supplied through `--file`. <br>
Mitigation: Use `--file` only with mistake-note text files the user intends to convert, and prefer the installed script path shown by the skill. <br>
Risk: The generated Markdown table reflects user-provided notes and may contain incomplete or incorrect study classifications. <br>
Mitigation: Review the table entries before relying on them for exam preparation or study planning. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown table or concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit a blank template or parse user-provided text/file rows into a four-column review table.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
