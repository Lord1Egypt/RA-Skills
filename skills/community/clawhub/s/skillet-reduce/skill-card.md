## Description: <br>
Use when asked to simplify, clean up, tidy, or refactor code for clarity without changing what it does, or when the user says "simplify this", "clean this up", "make it readable", "reduce the complexity", or "tidy this". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to simplify recently changed code through local, mechanical, behavior-preserving cleanup. It directs the agent to establish test evidence first, apply focused reductions when safe, and switch to report mode when behavior preservation cannot be proven. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose or apply code simplifications without enough behavior-preservation evidence. <br>
Mitigation: Require baseline verification and matching post-change verification before accepting any applied simplification; use report mode when coverage is thin or behavior cannot be locked. <br>
Risk: A future artifact or invocation could request credentials, broad local access, persistence, or destructive actions. <br>
Mitigation: Stop and manually inspect the skill before granting access or continuing, as directed by the security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/escoffier-labs/skillet-reduce) <br>
- [Publisher profile](https://clawhub.ai/user/escoffier-labs) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with simplification plans, change logs, verification evidence, and handoff notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May apply code edits only after behavior-preservation evidence is established; otherwise produces a report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
