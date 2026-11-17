## Description:

Diagnose and recover broken Git state and worktree metadata with a staged, low-risk recovery flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delorenj](https://clawhub.ai/user/delorenj)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to diagnose damaged Git repository state, route symptoms to low-risk recovery steps, and verify the repository after each remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic snapshots may capture sensitive Git data such as remote URLs, refs, reflog details, and repository paths in .git-state-snapshots.

Mitigation: Use the skill only on repositories where local diagnostic snapshots are acceptable, then inspect or delete .git-state-snapshots before committing, uploading logs, or sharing the repository.

Risk: Remote URLs can contain embedded tokens or credentials, and the snapshot script does not redact them.

Mitigation: Avoid running the snapshot workflow on repositories with credentials in remote URLs unless the script is updated to redact secrets and create owner-only files.

Risk: Some recovery steps can affect Git refs, worktrees, or HEAD state if applied to the wrong symptom.

Mitigation: Follow the staged workflow: snapshot first, apply the smallest matching playbook, back up .git before manual repairs, and run the recovery checklist after each change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/delorenj/skills/unfuck-my-git-state)
- [Publisher Profile](https://clawhub.ai/user/delorenj)
- [Symptom Map](references/symptom-map.md)
- [Recovery Checklist](references/recovery-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local diagnostic snapshot files when the bundled snapshot script is run.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
