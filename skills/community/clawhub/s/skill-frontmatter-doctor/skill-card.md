## Description:

Audits OpenClaw skill frontmatter, metadata, dependency declarations, install notes, and directory structure, then suggests reviewable fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to check OpenClaw skill folders for frontmatter, metadata, dependency declarations, install guidance, and required files before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit output can summarize local skill files, including sensitive material if the user points it at broad private directories.

Mitigation: Run it on scoped skill folders and avoid broad private directories unless local content disclosure in the generated report is acceptable.

Risk: Generated repair suggestions may still need release-owner review before being applied or published.

Mitigation: Review the Markdown or JSON report before making changes, and use dry-run or reviewable drafts for higher-risk updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/skill-frontmatter-doctor)
- [README](artifact/README.md)
- [OpenClaw skill audit spec](artifact/resources/spec.json)
- [Smoke test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with optional JSON output from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are reviewable audit reports and suggested next steps; the bundled script accepts input, output, format, limit, and dry-run parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
