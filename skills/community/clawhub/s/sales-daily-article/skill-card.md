## Description:

Generates roughly 1000-word Chinese sales-practice or anti-fraud article drafts with topic selection, compliance checks, Markdown storage, and local article-library sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meimei-shoulu](https://clawhub.ai/user/meimei-shoulu)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-language content creators use this skill to draft daily sales-practice or anti-fraud posts, check topic reuse and compliance risks, save Markdown articles, and sync them into a local HTML article library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated articles may include noncompliant claims, sensitive details, contact information, or misleading wording if published without review.

Mitigation: Review every draft before publishing and apply the compliance checklist to remove personal data, contact details, earnings guarantees, sensitive claims, and other risky wording.

Risk: The workflow writes Markdown files and updates a local HTML article library.

Mitigation: Use a dedicated article folder and review changed files before publishing, sharing, or relying on the generated library.

Risk: The artifact includes off-platform paid-upgrade and WeChat payment instructions.

Mitigation: Treat payment and upgrade steps as external to platform protections and do not rely on them for security, entitlement, or support guarantees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meimei-shoulu/skills/sales-daily-article)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown article drafts with YAML frontmatter, plus shell commands for local library updates when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Articles target about 900-1100 Chinese characters and may be saved as Markdown files before being added to a local HTML article library.]

## Skill Version(s):

1.2.1 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
