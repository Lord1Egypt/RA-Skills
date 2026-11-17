## Description:

Workspace boundary enforcement and file operation safety checks. Use before ANY file operation (read, write, edit, exec, delete) to: (1) Validate paths are within ~/openclaw workspace, (2) Confirm user permission for sensitive operations, (3) Check file operation safety, (4) Prevent unauthorized access outside workspace boundaries, or (5) Audit file access patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougchambes](https://clawhub.ai/user/dougchambes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review planned file operations, validate workspace boundaries, request confirmation for destructive or sensitive actions, and document blocked access attempts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Boundary-check examples may use unsafe path handling and should not be treated as a reliable enforcement layer.

Mitigation: Treat the skill as advisory guidance, review snippets before use, replace eval-based path expansion, and make path canonicalization fail closed.

Risk: Inconsistent workspace roots or external audit log locations can undermine boundary enforcement.

Mitigation: Define one canonical workspace root and keep audit logs inside that root with structured escaping and retention limits.

## Reference(s):

- [Workspace Boundaries Reference](references/boundaries.md)
- [Workspace Guard ClawHub Skill Page](https://clawhub.ai/dougchambes/skills/workspace-guard)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell snippets and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output for workspace-boundary review, permission prompts, and violation handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
