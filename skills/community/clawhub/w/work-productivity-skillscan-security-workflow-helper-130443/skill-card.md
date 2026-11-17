## Description:

Helps agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows for bug fixing, setup hardening, safety review, reliability improvement, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn SkillScan-style security and reliability needs into concise plans, templates, checklists, automation outlines, implementation support, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation may trigger too broadly because the skill enables auto-activation and uses generic trigger words.

Mitigation: Prefer explicit invocation or narrow the trigger terms before deployment in environments with many overlapping skills.

Risk: Workflow, checklist, code, or command suggestions could introduce incorrect guidance if applied without review.

Mitigation: Review outputs against the stated success criteria, scan generated artifacts before deployment, and validate changes in a local or staged environment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-130443)
- [Popular ClawHub Skill Demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Popular ClawHub Skill Demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Popular ClawHub Skill Demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent)
- [Popular ClawHub Skill Demand: AdMapix](https://clawhub.ai/skills/admapix)
- [Popular ClawHub Skill Demand: PollyReach](https://clawhub.ai/skills/pollyreach)
- [Hacker News: How Google decided to Destroy its Search Monopoly](https://news.ycombinator.com/item?id=48945074)
- [Hacker News: Where is your GitHub network building from?](https://news.ycombinator.com/item?id=48945115)
- [Hacker News: Vector search isn't the hard part. Deciding what should be searched is](https://news.ycombinator.com/item?id=48939470)
- [GitHub Issue: rdlp #500](https://github.com/crippledgeek/rdlp/issues/500)
- [GitHub Issue: perseus-vault #714](https://github.com/Perseus-Computing-LLC/perseus-vault/issues/714)
- [GitHub Issue: Stashpeak-app #244](https://github.com/Stashpeak/Stashpeak-app/issues/244)
- [GitHub Issue: anycast_healthchecker #54](https://github.com/unixsurfer/anycast_healthchecker/issues/54)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, templates, and concise verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should expose assumptions, limits, required inputs, remaining risks, and next steps when useful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
