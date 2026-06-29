## Description: <br>
Use when code review feedback arrives from a human reviewer, bot, or review agent before implementing any of it, especially when the feedback is unclear, technically questionable, or wrapped in authority. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to evaluate code review feedback as claims to verify before changing code. It helps decide when to implement, ask for clarification, or push back with concrete technical evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review feedback may be unclear, wrong, or conflict with existing code behavior. <br>
Mitigation: Restate unclear feedback concretely, verify each claim against the codebase, and ask for clarification before implementing dependent changes. <br>
Risk: The skill may lead an agent to push back on questionable feedback instead of immediately applying requested changes. <br>
Mitigation: Require pushback to cite concrete evidence such as a failing reproduction, caller search, documented contract, or pinned test. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/escoffier-labs/skillet-sendback) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance with ordered review workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code, tool calls, or hidden data access; responses should cite concrete checks before acting on review feedback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
