## Description: <br>
Processes external code review feedback with technical rigor by verifying claims before implementation and tracking each item's disposition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to process LLM, human, PR, CI, or linter feedback with tool-based verification before applying code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to make code changes after confirmation. <br>
Mitigation: Review the valid-item list and verification artifacts before approving fixes, then inspect the resulting diff and command results. <br>
Risk: Incorrectly verified feedback could introduce an unsuitable change. <br>
Mitigation: Require concrete verification artifacts for each item and reject claims that are disproved by tool output or code references. <br>


## Reference(s): <br>
- [Skill Integration](references/skill-integration.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/receive-feedback) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and concise text with file, line, command, and diff references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May apply code edits and run verification commands after the user confirms the valid feedback set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
