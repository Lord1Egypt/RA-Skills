## Description:

Lint and health-check a persistent markdown knowledge wiki for contradictions, stale claims, missing cross-links, orphan pages, duplicate pages, inconsistent naming, inconsistent frontmatter, schema drift, weak source attribution, and other maintenance issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teki-ai](https://clawhub.ai/user/teki-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and knowledge-base maintainers use this skill to review Obsidian-friendly, plain markdown, or git-backed wikis for structural and content quality issues. It produces prioritized findings and, when asked, can help apply targeted markdown fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read across the markdown wiki it is asked to inspect.

Mitigation: Run it only on intended wiki workspaces and avoid including sensitive notes unless review across that content is appropriate.

Risk: Requested fixes can change markdown content, links, or wiki structure.

Mitigation: Review proposed changes first and ask it to apply fixes only when markdown edits in that workspace are acceptable.

## Reference(s):

- [Wiki Lint Checklist](references/lint-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with prioritized findings and concrete fix recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply markdown edits when the user explicitly asks for fixes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
