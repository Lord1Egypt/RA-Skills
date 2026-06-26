## Description: <br>
Coordinate agents toward a unified objective; assign roles, sequence work, prevent conflicts, and define success criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-agent work by defining roles, sequencing, dependencies, handoffs, and success criteria for a shared objective. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate the planning workflow when high-level coordination was not intended. <br>
Mitigation: Invoke the skill explicitly for coordination tasks or narrow the trigger phrases in environments where accidental activation would be disruptive. <br>
Risk: Generated plans may propose irreversible or high-impact actions as part of a multi-agent workflow. <br>
Mitigation: Require explicit approval and governance alignment before carrying out irreversible actions, consistent with the skill's safety rules. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mzfshark/strategic-orchestration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown plan with structured sections for execution steps, roles, dependencies, handoff messages, and success criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an objective and current system state; outputs proposed coordination guidance rather than executing actions directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
