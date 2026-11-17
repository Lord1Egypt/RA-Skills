## Description:

研究文章匠人 helps agents draft evidence-backed long-form research articles through topic research, outline design, section-by-section writing, hook and title optimization, and final review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan, research, draft, refine, and review long-form technical blogs, industry analyses, white papers, research reports, and deep product or technology reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for command execution, broad file handling, API connections, and possible credentials without enough scoping or user control.

Mitigation: Use it in a constrained workspace and grant command execution, filesystem access, network access, and credentials only when they are specifically needed.

Risk: Research article drafts may contain incorrect data, weak citations, or misleading claims if sources are not reviewed.

Mitigation: Review cited sources, verify facts and quotations, and perform editorial review before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/research-article-crafter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, outlines, research briefs, title candidates, review notes, and optional code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write article drafts to output/{slug}/article.md when the agent has filesystem access.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
