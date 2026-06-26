## Description: <br>
System Continuity Check helps agents review system designs and workflows for continuity, automation, restart recovery, and error isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minijoy-b](https://clawhub.ai/user/minijoy-b) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill during system design or workflow discussions to run a checklist that highlights gaps in end-to-end flow, automatic recovery, restart behavior, and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger terms may activate the checklist during general development conversations where it is not needed. <br>
Mitigation: Use the skill explicitly or narrow trigger settings if automatic activation becomes distracting. <br>
Risk: Recommendations about auto-start, monitoring, and recovery are design advice and may not fit every environment. <br>
Mitigation: Review suggested operational changes before applying them and test them in the target workflow. <br>


## Reference(s): <br>
- [Checklist template](artifact/checklist_template.md) <br>
- [Error pattern library](artifact/error_patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/minijoy-b/system-continuity-check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown checklist with pass, warning, or fail statuses and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Checklist output is design review guidance and does not execute changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
