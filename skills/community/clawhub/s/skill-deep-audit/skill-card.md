## Description:

Generic skill-quality auditor for agent skills that runs a seven-dimension static or read-only dry-run analysis, scores findings with ERR/WARN severity, and produces a scorecard with fix guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit agent skill packages before release, checking process closure, portability, usability, security posture, code quality, and dependency footprint. It is intended for quality review and release readiness decisions rather than for executing the audited skill's business workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the selected target skill folder and writes an audit report into it by default.

Mitigation: Run it on trusted or sandboxed skill copies and review the generated AUDIT report before relying on its findings.

Risk: The bundled path-boundary checker may read outside the chosen target when an untrusted archive contains symlinks.

Mitigation: Avoid running it directly on untrusted archives; inspect or unpack them in a sandbox that prevents symlink traversal to sensitive paths.

Risk: Fix mode can modify audited skill files.

Mitigation: Require explicit confirmation before fix mode edits and keep the documented backup step before any changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/skill-deep-audit)
- [README](README.md)
- [Complete check rules](references/check-rules.md)
- [Audit report output template](references/output-template.md)
- [Scan command reference](references/scan-commands.md)
- [Controlled-domain configuration](references/controlled-domains.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit scorecard with cited ERR/WARN findings, summary text, dependency notes, and fix recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an AUDIT-{YYYY-MM-DD}.md report by default; fix-mode changes require explicit user confirmation and a backup first.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
