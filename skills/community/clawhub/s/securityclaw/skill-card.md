## Description:

SecurityClaw audits OpenClaw skills for prompt-injection, exfiltration, unsafe tool-use, and supply-chain risk indicators, with optional quarantine and owner-action guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mallen-lbx](https://clawhub.ai/user/mallen-lbx)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use SecurityClaw to scan OpenClaw skill directories before installation or during incident response, review JSON findings, quarantine suspicious skills, and decide whether to delete, report, allow, or scan all.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can produce false positives from simple regex-based rules.

Mitigation: Run read-only first, review the JSON report and file/line evidence, and use allowlists or contextual checks before acting.

Risk: Quarantine mode moves matching skill folders out of the active skills directory.

Mitigation: Enable quarantine only after review or owner approval and use a dedicated quarantine directory so files are preserved.

Risk: Dynamic checks of unknown skills may expose secrets, writable config, or network access if run without isolation.

Mitigation: Run dynamic analysis only with owner approval in an OS-level sandbox with no network egress, read-only mounts, a temporary workspace, and no access to OpenClaw config or secrets.

## Reference(s):

- [SecurityClaw rule catalog](references/rules.md)
- [Sandboxing strategy](references/sandboxing.md)
- [ClawHub skill page](https://clawhub.ai/mallen-lbx/skills/securityclaw)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with bash commands and JSON report references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner writes a JSON report and can move flagged skill folders when quarantine is explicitly enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
