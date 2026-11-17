## Description:

Helps AI-agent users, skill authors, maintainers, and teams create skill-vetting workflows, checklists, analyses, and implementation support for reliability and security work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to plan and produce practical skill-vetting workflows, bug-fix support, setup-hardening checklists, reliability improvements, and adjacent skill ideas. It is intended for local-friendly workflow, documentation, code, and analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad terms because implicit invocation metadata is broad.

Mitigation: Restrict or disable implicit invocation when the environment supports it, and invoke the skill explicitly for skill-vetting or reliability tasks.

Risk: Workflow guidance can still produce incorrect or incomplete vetting recommendations.

Mitigation: Review generated plans, checklists, and code changes against the stated success criteria before applying them.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-234020)
- [Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [GitHub demand signal](https://clawhub.ai/skills/github)
- [SkillScan demand signal](https://clawhub.ai/skills/skillscan)
- [Hacker News search-scope discussion](https://news.ycombinator.com/item?id=48939470)
- [moq-net GitHub issue](https://github.com/moq-dev/moq/issues/2313)
- [Harushion GitHub issue](https://github.com/Love-Rox/Harushion/issues/14)
- [Bimex governance GitHub issue](https://github.com/David1984TK/Bimex/issues/248)
- [OpenMinerva Markdown parser GitHub issue](https://github.com/OpenMinerva/client/issues/159)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, checklists, templates, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, remaining risks, and follow-up work when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
