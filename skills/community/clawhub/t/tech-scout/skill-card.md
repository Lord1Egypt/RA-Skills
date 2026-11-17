## Description:

Daily multi-source intelligence digest that proactively scans X, YouTube, Reddit, and GitHub for tools, techniques, and updates relevant to active projects, filters high-signal items using a 7/10 quality bar, and adds a practical relevance note for each surfaced item.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pingukim225](https://clawhub.ai/user/pingukim225)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, traders, and research-oriented users use this skill to scan fast-moving online sources for project-relevant tools, techniques, releases, and updates before a daily work session. It produces a short ranked digest with why each item matters and a suggested next action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may query external services using configured project keywords, which can expose sensitive project interests if broad or confidential terms are used.

Mitigation: Use narrow non-confidential keywords and avoid internal project names or private business terms in search targets.

Risk: Scheduled searches and local digest state can persist links and research interests under state/.

Mitigation: Confirm any automated schedule before enabling it and periodically review or clear saved digest and seen-URL state files.

## Reference(s):

- [Tech Scout ClawHub listing](https://clawhub.ai/pingukim225/skills/tech-scout)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown digest file with ranked items, links, relevance notes, and suggested actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily digest and seen-URL state files under state/ when implemented as described.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
