## Description: <br>
A Japanese instruction-only coaching skill that pressures an agent to keep debugging, investigate actively, and verify work with concrete evidence after repeated task failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanweai](https://clawhub.ai/user/tanweai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a high-pressure Japanese debugging and verification posture when an agent repeatedly fails, tries to hand work back to the user, or proposes unverified conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly pressures the agent to act and use tools across nearly any task without clear scope limits. <br>
Mitigation: Keep normal tool approvals, privacy boundaries, safety refusals, and clarification requirements in place, especially before reading sensitive files or running commands with side effects. <br>
Risk: The skill is intended to create a high-pressure Japanese debugging posture that may be inappropriate for some deployments. <br>
Mitigation: Install only when that coaching style is intentional and appropriate for the agent's users and operating context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanweai/pua-ja) <br>
- [Publisher profile](https://clawhub.ai/user/tanweai) <br>
- [Homepage](https://openpua.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with possible inline command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no direct code execution is bundled.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
