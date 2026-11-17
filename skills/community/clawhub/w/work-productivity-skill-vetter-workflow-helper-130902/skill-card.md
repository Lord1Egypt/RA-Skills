## Description:

Vet third-party or generated skills for usefulness, safety, overlap, and publish quality before install, revision, or publication decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to review skill trigger quality, usefulness, safety, duplication risk, and publication readiness. It supports install, keep, rename, merge, improve, reject, or publish decisions with concrete fixes and validation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording and implicit invocation may select the skill during loosely related skill or security discussions.

Mitigation: Invoke it explicitly for skill-vetting work or tighten trigger keywords and examples before broad deployment.

Risk: Vetting recommendations can be misleading when the reviewer provides incomplete skill files, marketplace metadata, or intended-use context.

Mitigation: Collect the skill folder or listing, intended user job, trigger examples, overlapping local skills, and the target decision before relying on the recommendation.

Risk: Proposed revisions or shell commands could introduce incorrect guidance if applied without review.

Mitigation: Review proposed edits and run validation or scan commands before installing, publishing, or modifying a skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-130902)
- [Requirement Plan](references/requirement-plan.md)
- [Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [GitHub demand signal](https://clawhub.ai/skills/github)
- [SkillScan demand signal](https://clawhub.ai/skills/skillscan)
- [V2EX safety discussion demand signal](https://www.v2ex.com/t/1221581)
- [Hacker News demand signal](https://news.ycombinator.com/item?id=48608578)
- [Employee table search issue demand signal](https://github.com/rushikesh-bobade/empay-hrms/issues/100)
- [Enchanting clue cap issue demand signal](https://github.com/rfizzle/meridian/issues/83)
- [Token budget truncation issue demand signal](https://github.com/kdeps/kdeps/issues/566)
- [Shared package migration issue demand signal](https://github.com/poodle64/supacrawl/issues/141)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, checklists, revised skill text, and inline command or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are evidence-based review recommendations and proposed edits; they require user review before installing, publishing, or changing skills.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
