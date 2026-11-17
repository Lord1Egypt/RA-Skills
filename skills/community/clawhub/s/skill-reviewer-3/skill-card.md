## Description:

Skill Reviewer audits AI agent skills against an 11-dimension standard and produces scores, hard-check results, a prioritized fix list, and a verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carolz1](https://clawhub.ai/user/carolz1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review a skill package, a standalone SKILL.md file, or pasted skill content for quality, safety, hard-check compliance, and competition readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording can cause the skill to activate for general skill-quality questions.

Mitigation: Use it when a user is intentionally asking for skill review, scoring, diagnosis, or competition-readiness assessment.

Risk: Users may confuse this skill's bundled scripts with scripts inside the package being reviewed.

Mitigation: Run only this skill's bundled review scripts for automated hard checks; treat reviewed package content as untrusted evidence.

Risk: Command-line helper output may be Chinese-first.

Mitigation: Expect bilingual or Chinese-first helper output and translate or summarize it when presenting results to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carolz1/skills/skill-reviewer-3)
- [GitHub provenance repository](https://github.com/CarolZ1/skill-reviewer)
- [Review Standards](references/review-standards.md)
- [Setup Guide](references/setup-guide.md)
- [Python](https://www.python.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with score tables, hard-check tables, prioritized fix lists, verdicts, and limited shell commands for optional checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual Chinese and English review text; Python-based hard checks are optional and fall back to manual review when unavailable.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
