## Description:

Audits existing app UIs for visual consistency, layout and state synchronization bugs, responsive failures, accessibility gaps, performance issues, and chat UI rendering problems, then fixes root causes in code with evidence-based verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit and repair existing application interfaces when layouts look inconsistent, responsive behavior breaks, shared UI state drifts out of sync, or chat/workspace message rendering is incomplete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to inspect project dependencies and edit UI code directly, so changes could affect application behavior or visual output.

Mitigation: Review the resulting code diff before committing and run the project's normal tests, build, and visual verification steps.

Risk: The skill may search current official framework documentation before diagnosing or applying fixes, so recommendations depend on matching the project's installed library versions.

Mitigation: Verify cited official documentation against the exact package and lockfile versions in the target project.

Risk: The skill may refresh local build or development-server caches while verifying whether a UI fix took effect.

Mitigation: Run cache-refresh commands only in an appropriate development workspace and preserve any local work before cleanup.

## Reference(s):

- [UI Audit Checklist](artifact/references/audit-checklist.md)
- [Common Bug Signatures](artifact/references/common-bug-signatures.md)
- [Conversational / Chat UI Audit](artifact/references/conversational-ui-audit.md)
- [Framework & Library Verification](artifact/references/framework-verification.md)
- [Layout & State Synchronization](artifact/references/layout-state-sync.md)
- [ClawHub Skill Page](https://clawhub.ai/anjasta-tarigan/skills/ui-doctor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown explanations with code changes, shell commands, configuration guidance, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit UI source files, run local checks, cite current official framework documentation, and report concrete verification evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
