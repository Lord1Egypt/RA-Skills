## Description: <br>
Provides output quality assurance and verification through post-edit diagnostics, optional pre-commit test checks, session metrics, and hook runtime profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add quality gates around coding workflows, including immediate diagnostics after edits, optional test checks before commits, and lightweight session measurement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local lint and test commands from development hooks. <br>
Mitigation: Install it only in trusted development workspaces and review repository test scripts before enabling TEST_BEFORE_COMMIT. <br>
Risk: Hook behavior depends on local tools and project configuration, so diagnostics may be skipped or incomplete when expected tools are unavailable. <br>
Mitigation: Document required linters, type checkers, and test runners for each workspace before relying on the hooks as release gates. <br>
Risk: Session metrics are written using session identifiers from hook input or environment state. <br>
Mitigation: Use explicit capability metadata and session ID validation for stricter deployments. <br>


## Reference(s): <br>
- [Post-Edit Diagnostics](references/post-edit-diagnostics.md) <br>
- [Hook Runtime Profiles](references/hook-profiles.md) <br>
- [Hook Pair Bracket](references/hook-bracket.md) <br>
- [Test-Before-Commit Gate](references/test-before-commit.md) <br>
- [Atomic File Writes](references/atomic-writes.md) <br>
- [Session State Hygiene](references/session-hygiene.md) <br>
- [Extended Patterns](references/extended-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON hook outputs and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit hook additionalContext messages, permission-deny reasons, and local session metrics files when configured.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
