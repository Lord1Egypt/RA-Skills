## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows for bug fixing, setup hardening, safety review, reliability improvement, and adjacent skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent teams use this skill to turn broad security and productivity needs into concrete workflows, checklists, templates, analyses, code changes, or decision aids. It is intended for local-friendly planning and validation of SkillScan-style security, hardening, reliability, and workflow-extension tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on overly broad security or workflow-related requests.

Mitigation: Invoke it explicitly by name for sensitive work and narrow the trigger policy before broad deployment.

Risk: Generated workflow, hardening, or bug-fix guidance could be incorrect or incomplete for a specific environment.

Mitigation: Review outputs against the stated success criteria and scan or test any resulting skill changes before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-230850)
- [self-improving-agent demand signal](https://clawhub.ai/skills/self-improving-agent)
- [Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [SkillScan demand signal](https://clawhub.ai/skills/skillscan)
- [AdMapix demand signal](https://clawhub.ai/skills/admapix)
- [PollyReach demand signal](https://clawhub.ai/skills/pollyreach)
- [Ask HN Gsearch discussion demand signal](https://news.ycombinator.com/item?id=48878919)
- [Tell HN staged NPM publishing discussion demand signal](https://news.ycombinator.com/item?id=48893354)
- [A/B test homepage heroes discussion demand signal](https://news.ycombinator.com/item?id=48894437)
- [Daily PR Audit Reporter issue demand signal](https://github.com/extropolis/claudia/issues/109)
- [Spectre mitigation issue demand signal](https://github.com/m-novotny/memguard-rs/issues/7)
- [HGC QC issue demand signal](https://github.com/bigbio/hvantk/issues/205)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tailored artifacts, reusable checklists, workflow plans, analyses, and verification notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
