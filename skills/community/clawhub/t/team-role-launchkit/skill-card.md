## Description: <br>
Launch clone-like multi-agent workflows using explicit role prompts (researcher, builder, editor), strict handoff contracts, and shared behavior files for consistent long-running execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cwheeler67](https://clawhub.ai/user/cwheeler67) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate complex, multi-step work across researcher, builder, and editor roles while preserving explicit handoff criteria and review boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Role handoffs may promote unnecessary or sensitive working notes into durable memory when the agent platform supports memory. <br>
Mitigation: Review handoff outputs before saving durable memory and only promote approved outcomes. <br>
Risk: Poorly scoped handoffs can cause a role to act outside the intended task boundaries. <br>
Mitigation: Require done criteria and receiver restatement before each role acts. <br>


## Reference(s): <br>
- [Handoff Contract](references/handoff-contract.md) <br>
- [Role Prompts](references/role-prompts.md) <br>
- [ClawHub skill page](https://clawhub.ai/cwheeler67/team-role-launchkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific handoff notes, final deliverables, unresolved risks or questions, and a next best action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
