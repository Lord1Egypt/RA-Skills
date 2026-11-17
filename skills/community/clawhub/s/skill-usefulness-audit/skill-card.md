## Description:

Review your installed agent skills to see what you actually use, what overlaps, and what may no longer be worth keeping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongyu0918-debug](https://clawhub.ai/user/gongyu0918-debug)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and agent operators use this skill to audit installed agent skills for usage, overlap, cleanup options, bundle burden, and conservative ablation planning. It helps produce short user-facing reports and optional detailed evidence files without automatically deleting or disabling skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads installed skill folders and user-provided evidence files during local audits.

Mitigation: Pass --skills-root to limit the audited scope and review which evidence files are provided.

Risk: Usage or history files may contain conversation details, local paths, project names, or customer data.

Mitigation: Provide only necessary evidence files and review or redact sensitive data before running the audit.

## Reference(s):

- [Project homepage](https://github.com/gongyu0918-debug/skill-usefulness-audit)
- [Ablation Protocol](references/ablation-protocol.md)
- [Report Narration Prompt](references/report-narration-prompt.md)
- [Scoring Rubric](references/scoring-rubric.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Natural-language report, Markdown evidence report, and optional JSON audit or ablation-plan files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can consume user-provided usage, history, ablation, and community evidence files; supports English or Chinese reports.]

## Skill Version(s):

0.3.24 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
