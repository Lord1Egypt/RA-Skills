## Description: <br>
Generates a local Markdown spaced-repetition vocabulary study plan from a line-based word or phrase list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, educators, and language-learning users use this skill to turn a plain text vocabulary list into a day-by-day study and review schedule. It is intended for vocabulary review planning and exam preparation, not app integrations or minute-level reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated Markdown includes the words or phrases from the input file, so private or unrelated document contents could be exposed in the output. <br>
Mitigation: Use only vocabulary lists intended for study planning as the --file input, and review the generated Markdown before sharing or storing it. <br>


## Reference(s): <br>
- [Tianshu Vocab Plan on ClawHub](https://clawhub.ai/wangshengli0421/tianshu-vocab-plan) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown table with brief usage notes and an example command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-supplied local word-list file and prints the schedule to standard output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
