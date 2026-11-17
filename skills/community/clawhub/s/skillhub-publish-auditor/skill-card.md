## Description:

Use when preparing a Skill folder for public release to SkillHub, ClawHub, or another agent-skill marketplace, especially before publishing third-party installable skills, scripts, references, metadata, or examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[debtvc2022](https://clawhub.ai/user/debtvc2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to audit agent skill folders before public marketplace release, checking structure, discovery metadata, safety, packaging, and release readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports a suspicious verdict because the bundled scanner can read outside the chosen skill folder through symlinks and can silently skip scans in some common paths.

Mitigation: Review before installing; avoid running it on untrusted skill archives that may contain symlinks or under excluded directory names such as build or dist.

Risk: Security evidence says scans may be incomplete when no files are scanned or when path containment is not enforced.

Mitigation: Prefer a patched version that rejects symlinks, enforces resolved-path containment, and reports when no files were scanned.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/debtvc2022/skills/skillhub-publish-auditor)
- [release-checklist.md](references/release-checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown or JSON release audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ends with a READY, READY_WITH_WARNINGS, or BLOCKED release decision.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
