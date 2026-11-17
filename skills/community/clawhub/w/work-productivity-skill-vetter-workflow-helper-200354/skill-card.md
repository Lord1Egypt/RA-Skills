## Description:

Helps agent users, skill authors, maintainers, and teams create practical Skill Vetter-style workflows for bug fixing, safer setup, reliability improvement, and adjacent skill planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users, skill authors, maintainers, and teams use this skill to structure vetting-style workflows, checklists, templates, decision aids, analysis, or local implementation support for safer and more reliable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overly broad trigger words may activate the skill in unrelated security or GitHub conversations.

Mitigation: Use stricter runtime routing, narrow invocation terms, or explicitly confirm the desired vetting workflow before applying the skill.

Risk: Generated vetting workflows, checklists, or implementation advice may be incomplete or misleading for a specific environment.

Mitigation: Review outputs against the user's stated success criteria and scan or test artifacts before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github)
- [Popular ClawHub skill demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Hacker News discussion: evaluating a company](https://news.ycombinator.com/item?id=48898310)
- [Hacker News discussion: committing .env files](https://news.ycombinator.com/item?id=48904726)
- [GitHub issue: restricted Pod Security](https://github.com/kagent-dev/kagent/issues/2244)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, checklist, template, or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, constraints, validation steps, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
