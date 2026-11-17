## Description:

Helps creators plan, draft, and review Chinese Toutiao articles using writing guidance, a TRACE quality checklist, and a local article-audit script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxq0607](https://clawhub.ai/user/sxq0607)

### License/Terms of Use:

MIT-0

## Use Case:

Toutiao creators and editors use this skill to develop article ideas, draft posts, check quality and potential policy issues before publishing, and review content performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit reads draft content and creates local JSON reports in the selected file or directory location.

Mitigation: Run it only on drafts or directories you intend to audit, and handle generated reports according to your content-sharing practices.

Risk: Automated content checks may miss issues or suggest a post will pass review when it will not.

Mitigation: Review facts, rights, and current Toutiao requirements manually before publishing; treat audit results as guidance, not approval.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sxq0607/skills/toutiao-master)
- [Writing guide](references/writing-guide.md)
- [TRACE review criteria](references/trace-review.md)
- [Violation guide](references/violation-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Chinese-language article drafts and review guidance in text or Markdown; local audit reports in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The audit script creates a JSON report beside each audited draft or in the audited directory.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
