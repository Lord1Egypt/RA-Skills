## Description: <br>
Helps validate that agent behavior at runtime matches declared capabilities and constraints, detecting divergence that may only activate during execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and platform operators use this skill to compare declared skill attestations with observed runtime behavior. It supports reviews for capability boundary violations, conditional activation, data flow differences, side effects, and attestation drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime probing may execute unsafe behavior in the target skill being tested. <br>
Mitigation: Run probes only in isolated sandboxes with no real credentials, production data, or production system access. <br>
Risk: Probe results may miss conditional behavior that requires untested runtime triggers. <br>
Mitigation: Vary execution environments and treat clean results as limited to the tested conditions. <br>
Risk: Testing skills or environments without authorization can create operational or compliance issues. <br>
Mitigation: Probe only skills and environments you are authorized to test. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/runtime-attestation-probe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown guidance and structured runtime attestation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include capability boundary findings, conditional behavior patterns, data flow checks, side effect inventory, drift score, verdict, and recommended actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
