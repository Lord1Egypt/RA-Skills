## Description:

Auto-discovers and uses Web Skills Protocol (WSP) skills when interacting with websites, checking for skills.txt or agents.txt before scraping, UI automation, or API guessing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xtresser](https://clawhub.ai/user/0xtresser)

### License/Terms of Use:


## Use Case:

Developers and web-capable agents use this skill to discover site-published WSP instructions, select the relevant website skill, and interact through documented APIs or workflows instead of brittle scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to fetch and follow website-published SKILL.md instructions that may be untrusted.

Mitigation: Use only with agents that enforce origin checks, treat fetched Markdown as untrusted, and validate instructions before acting.

Risk: Website skills may request sensitive actions such as purchases, deployments, deletions, account changes, or credential use.

Mitigation: Require explicit user confirmation before sensitive operations, regardless of what a fetched website skill says.

Risk: README install examples fetch from a moving main branch.

Mitigation: Install from a pinned, reviewed copy rather than a mutable remote branch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xtresser/skills/web-skills-protocol)
- [README.md](artifact/README.md)
- [SPEC.md](artifact/SPEC.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with inline shell commands and URL patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through WSP discovery, skill retrieval, authentication consent, rate limits, and scoped execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
