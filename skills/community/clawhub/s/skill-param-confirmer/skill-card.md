## Description: <br>
Downstream skill execution preflight layer that inspects a target skill, extracts explicit and implicit confirmation fields, normalizes candidate parameters, resolves ambiguity, applies risk gating, and returns a structured confirmation payload before handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pm-geeker](https://clawhub.ai/user/pm-geeker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill before invoking downstream skills to align required parameters, resolve ambiguity, confirm high-risk actions, and produce a traceable handoff payload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session logging can expose sensitive user inputs, identifiers, or downstream metadata if stored without controls. <br>
Mitigation: Store logs securely, redact secrets and sensitive identifiers, and limit retention before using the confirmation flow with confidential data. <br>
Risk: Ambiguous or inferred parameters can lead a downstream skill to act on the wrong target or scope. <br>
Mitigation: Use the skill's blocking and clarification flow for missing, conflicting, or unstable values, and require explicit confirmation for high-risk actions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/pm-geeker/skill-param-confirmer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/pm-geeker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Structured JSON handoff payloads and concise confirmation prompts or blocking guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include numbered confirmation menus, risk gates, uncertainty reports, decision mode, session identifiers, and audit fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
