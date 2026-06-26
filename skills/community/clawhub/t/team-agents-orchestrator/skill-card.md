## Description: <br>
Run complex tasks with explicit role separation (operator, researcher, builder, editor), structured handoff contracts, and memory hygiene to prevent context pollution and role blur. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cwheeler67](https://clawhub.ai/user/cwheeler67) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-step work across research, implementation, and communication roles while keeping decisions, handoffs, and memory updates explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be used in environments with local repository access, credentials, or moderation capabilities. <br>
Mitigation: Install only where that access is appropriate, keep confirmation prompts for moderation or deletion actions, and avoid full-access autoreview mode for untrusted code. <br>
Risk: Role handoffs can still produce overreach, verbose output, or memory pollution if reviewers skip the stated discipline. <br>
Mitigation: Require each handoff to state objective, constraints, done criteria, open questions, and receiver restatement before execution. <br>


## Reference(s): <br>
- [Handoff Contract Template](references/handoff-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with role-scoped handoff details and concise final-result sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include what changed, unresolved risks or questions, and the next best action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
