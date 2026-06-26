## Description: <br>
Force Harness mode for task decomposition, routing, package-first execution, and verifier-first completion evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[villiamsl](https://clawhub.ai/user/villiamsl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to apply a formal harness workflow to project advancement, dispatch, execution, verification, delivery, and governance escalation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may steer agents into a formal harness process for routine troubleshooting or small tasks. <br>
Mitigation: Require explicit opt-in for small or routine tasks, and define when the harness workflow should apply. <br>
Risk: The workflow depends on task routing, package format, verifier role, and governance boundaries that are not fully defined in the artifact. <br>
Mitigation: Define the routing matrix, task package format, verifier package format, verifier authority, and governance approval boundaries before organizational use. <br>
Risk: Agents could overstate completion by treating created or delivered work as verified without independent evidence. <br>
Mitigation: Require verifier evidence before marking work as VERIFIED or BusinessClosed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/villiamsl/using-harness) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance and structured task instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; it does not add code execution, data access, persistence, or credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
