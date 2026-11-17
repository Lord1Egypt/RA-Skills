## Description:

Finds and compares existing agent skills across ClawHub, skills.sh, SkillsMP, and two curated lists, ranking candidates and providing validated install commands where available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:

MIT

## Use Case:

Developers and other skill users can discover and compare skills for a specific task before choosing whether to install one. The skill provides recommendations, not execution of the requested task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to external skill directories and may disclose sensitive terms.

Mitigation: Avoid confidential names and unreleased codenames; use a generic query instead.

Risk: Optional security scans share result URLs with Gen Digital, and advisory labels do not establish safety.

Mitigation: Enable URL sharing only with user consent and review any candidate before installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/broedkrummen/skills/ultimate-skills-finder)
- [Source reference](references/sources.md)
- [ClawHub](https://clawhub.ai)
- [skills.sh](https://skills.sh)
- [SkillsMP](https://skillsmp.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Text or JSON with ranked skill candidates, source links, and validated install commands where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional advisory scan labels; browse-only results have no install command.]

## Skill Version(s):

1.3.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
