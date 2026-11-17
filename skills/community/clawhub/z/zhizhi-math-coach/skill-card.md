## Description:

Helps families grade primary-school math work, explain mistakes, track learning progress, and plan follow-up practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linzi007](https://clawhub.ai/user/linzi007)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and educators use the skill to review worksheet photos, explain errors, maintain learning records, and choose targeted practice for primary-school students.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub sync may back up sensitive child learning records.

Mitigation: Use a dedicated private learning repository; leave sync disabled unless the full archive is intended for backup, and review sync settings before enabling it.

Risk: Public Pages publishing may expose student data or answer keys.

Mitigation: Publish only child-facing worksheet pages and keep records, photos, and answer keys outside the public site.

Risk: Deploy keys and scheduled jobs may operate beyond the intended learning workspace.

Mitigation: Verify each deploy key and scheduled job is scoped to the dedicated learning repository before enabling automation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/linzi007/skills/zhizhi-math-coach)
- [Daily grading workflow](artifact/references/daily-grading-workflow.md)
- [Photo intake and learning records](artifact/references/photo-intake.md)
- [GitHub sync authorization](artifact/references/github-sync-authorization.md)
- [Public worksheet publishing](artifact/references/github-pages-publishing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, PDF worksheets, HTML worksheets, JSON learning records, Configuration guidance]

**Output Format:** [Parent-facing summaries and explanations; printable worksheets and local learning records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Student-facing worksheets are separate from answer keys and private learning records.]

## Skill Version(s):

0.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
