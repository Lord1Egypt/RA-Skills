## Description:

Diffs two versions of the same document, marks insertions, deletions, edits, and moved content, separates substantive changes from cosmetic wording or formatting changes, and highlights high-risk changes for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, reviewers, and document owners use this skill to compare old and new versions of contracts, policies, proposals, requirements, or similar documents before signing, archiving, or review. It produces an objective change report that identifies substantive edits, cosmetic changes, moved sections, and items needing closer review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese trigger phrases may invoke the skill for general comparison requests.

Mitigation: Confirm that the task is specifically a two-version document comparison before relying on the report.

Risk: The skill can surface high-risk document changes such as amounts, dates, parties, penalties, exclusivity, or terms, but it does not judge legality or business desirability.

Mitigation: Use the high-risk review section as a checklist for qualified legal, commercial, or policy review where appropriate.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-doc-version-diff)
- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-doc-version-diff)
- [Substantive-change decision reference](artifact/references/实质判定对照表.md)
- [Diff report template](artifact/templates/diff-report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with alignment notes, a change table, high-risk review items, and cosmetic-change summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided document versions; requests the missing version when only one version is provided; asks for pasted text when file paths cannot be read.]

## Skill Version(s):

0.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
