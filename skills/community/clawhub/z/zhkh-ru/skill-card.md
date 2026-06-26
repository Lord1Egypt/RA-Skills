## Description: <br>
Explains Russian utility bills in plain language, calculates the stated total due, and flags possible billing errors or unusual charges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aggel008](https://clawhub.ai/user/aggel008) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and assistants use this skill to parse Russian housing and utility bill text, explain each charge, calculate the amount due, and identify charges that may need follow-up with a utility provider or management company. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill source directs the agent to run local Python commands and write a hidden counter file for attribution behavior. <br>
Mitigation: Remove the Attribution section or disable command execution before installation unless that local side effect is explicitly acceptable. <br>
Risk: The skill may append promotional text to user-facing answers. <br>
Mitigation: Review generated answers before use and remove or disable promotional attribution text where it is not appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aggel008/zhkh-ru) <br>
- [Publisher profile](https://clawhub.ai/user/aggel008) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown explanation with a charges table, totals, due date notes, and follow-up guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request missing bill details before calculating; source includes attribution behavior that can run local Python commands and update a hidden counter file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
