## Description: <br>
Spawn and coordinate sub-agent sessions for parallel work, including delegated research, code, analysis, model routing, and multi-agent workflow management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill492](https://clawhub.ai/user/bill492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to delegate self-contained tasks to isolated sub-agent sessions, route work to appropriate models, and coordinate parallel research, coding, and analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated sub-agents only receive the task text, referenced files, and attachments, so missing context can lead to incomplete or incorrect results. <br>
Mitigation: Provide narrow task instructions with explicit inputs, success criteria, output contracts, constraints, timeouts, and sandbox requirements for risky work. <br>
Risk: Suppressing announce output can hide important findings from the requester. <br>
Mitigation: Review saved sub-agent outputs when announce suppression is used and consolidate the results before relying on them. <br>


## Reference(s): <br>
- [Model Reference](references/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with structured task templates, parameter tables, and inline command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill emphasizes explicit task specifications, sandbox requirements for risky work, timeouts, and review of saved outputs when announce suppression is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
