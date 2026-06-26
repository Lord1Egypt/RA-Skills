## Description: <br>
Diagnose and recover broken Git state and worktree metadata with a staged, low-risk recovery flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[delorenj](https://clawhub.ai/user/delorenj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose broken Git repositories, plan low-risk worktree and ref recovery steps, and verify repository health after each fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git repair guidance can change local repository metadata, including refs, HEAD state, and worktree records. <br>
Mitigation: Snapshot or back up .git first, review branch and HEAD repair commands before execution, and use manual .git edits only after normal Git commands fail. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/delorenj/unfuck-my-git-state) <br>
- [Symptom Map](references/symptom-map.md) <br>
- [Recovery Checklist](references/recovery-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command blocks and stepwise repair guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes snapshot-first diagnostics, non-destructive repair plans, and verification gates before escalation.] <br>

## Skill Version(s): <br>
0.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
