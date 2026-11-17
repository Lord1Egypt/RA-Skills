## Description:

Use when you publish or maintain a portfolio of agent skills (ClawHub, GitHub, internal registry) and need a single health dashboard — which skills have dead links, missing READMEs, stale versions, inconsistent frontmatter, clone-count anomalies, or unpublishable structure — instead of checking each repo by hand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill portfolio maintainers use this tool to audit multiple agent skills for structure, frontmatter consistency, script syntax, credential patterns, and optional local Git state, then prioritize fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional checks may run repository-configured code.

Mitigation: Limit scans to the skills directory and leave --git disabled for repositories with untrusted configuration.

Risk: A perfect grade or successful JSON exit does not establish that credentials are absent.

Mitigation: Review the credential fix queue directly; inspect suspected files rather than relying on the grade alone.

Risk: Token revocation or history rewriting can have consequential effects.

Mitigation: Require a reviewed backup and explicit approval before revoking tokens or rewriting history.

## Reference(s):

- [Dashboard grading model and security patterns](references/dashboard-model.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/skill-portfolio-dashboard)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Human-readable portfolio report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports per-skill grades, a portfolio score, and a prioritized fix queue; Git state is optional.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
