## Description: <br>
This skill should be used when the user says "test skill", "run test skill", or asks to demonstrate the test skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxzhaoo](https://clawhub.ai/user/yxzhaoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill reviewers use this minimal skill to confirm that custom skill activation works by producing a greeting, the current date and time, and an activation confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is low-utility and only verifies custom skill activation. <br>
Mitigation: Install it for activation checks, not for task automation or production workflows. <br>
Risk: The skill asks the agent to report the current date and time, which can be wrong if the runtime clock or timezone context is wrong. <br>
Mitigation: Confirm date and time against the agent runtime or an authoritative clock when accuracy matters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a greeting, current date and time, and a confirmation that custom skills are active.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
