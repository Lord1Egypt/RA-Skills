## Description:

SEO Optimizer helps agents research keywords, analyze meta tags, score page content, and generate search-focused recommendations for website content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hughtan93-dev](https://clawhub.ai/user/hughtan93-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, website owners, content teams, and developers use this skill to prepare pages for publication by checking keywords, metadata, content structure, links, images, and SEO scoring guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned dependency installation can introduce supply-chain or reproducibility issues.

Mitigation: Install the skill in a virtual environment and pin or review dependencies before use.

Risk: Unusual regex-like keywords may cause analyzer failures.

Mitigation: Use plain keyword input where possible and review analyzer output when keywords contain regex metacharacters.

Risk: SEO scores and recommendations are heuristic and can be misleading if applied without review.

Mitigation: Treat generated recommendations as review aids and validate important content decisions against current site analytics and search guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hughtan93-dev/skills/seopro)
- [SEO Best Practices](references/best_practices.md)
- [SEO Checklist](references/seo_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; supporting scripts can emit text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
