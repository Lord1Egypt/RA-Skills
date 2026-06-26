## Description: <br>
Generates a printable Markdown study schedule that spreads course topics across the days before an exam. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students or agents assisting students use this skill to distribute course topics across a configurable number of days before an exam and produce a printable checklist-style review plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A topics file may contain sensitive course or study details that are echoed into the generated Markdown schedule. <br>
Mitigation: Use only topics files whose contents are acceptable to include in the printed or shared schedule. <br>
Risk: The script prompts and generated notes are in Chinese, which may be unsuitable for users expecting another language. <br>
Mitigation: Review the generated schedule before sharing and localize the notes when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshengli0421/tianshu-review-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown schedule with a date and topic table plus brief study notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads topics from command-line input or a user-provided local topics file; prompts and generated notes are in Chinese.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
