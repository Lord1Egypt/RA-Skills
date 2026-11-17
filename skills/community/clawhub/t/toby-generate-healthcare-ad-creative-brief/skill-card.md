## Description:

Plan campaign visuals and hooks for healthcare promotions for paid campaign planning by healthcare operators, clinic teams, and patient educators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare operators, clinic teams, and patient educators use this skill to draft paid campaign creative briefs that clarify audience, goals, constraints, visual hooks, and deliverables. Human review is needed before patient-facing content or regulated medical claims are used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Bash and Read access even though the described brief-generation workflow does not require shell or local file access.

Mitigation: Install with Bash and Read removed or denied unless a specific local workflow needs them; run in a constrained workspace when enabled.

Risk: Healthcare ad briefs may include patient-facing content or regulated medical claims.

Mitigation: Require qualified human review for accuracy, compliance, and suitability before publishing or relying on generated claims.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/tobeyrebecca/skills/toby-generate-healthcare-ad-creative-brief)
- [SkillBoss skill page](https://www.skillboss.co/skills/generate-healthcare-ad-creative-brief)
- [SkillBoss setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown creative brief guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include visual direction, messaging hooks, audience notes, constraints, deliverables, and human-review reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
