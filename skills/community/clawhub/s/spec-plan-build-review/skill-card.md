## Description: <br>
Run a proportional delivery lifecycle for software or skill work: clarify scope, create a concise plan, implement, verify, review, and ship. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage non-trivial software or skill work through scoped planning, implementation, verification, review, and release preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ship steps can involve commits, pushes, releases, or ClawHub/GitHub publication. <br>
Mitigation: Confirm the user intends those actions before running them, verify the worktree and checks, and keep release artifacts aligned with the intended version. <br>
Risk: Optional review agents may receive sensitive code or secrets if used in an untrusted runtime. <br>
Mitigation: Use only trusted review agents and keep sensitive code or secrets out of optional subagent review when trust is unclear. <br>


## Reference(s): <br>
- [Review Lenses](references/review-lenses.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/spec-plan-build-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scoped plans, verification notes, review findings, and ship checklists.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
