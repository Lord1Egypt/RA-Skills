## Description:

Recommends gift options based on the recipient relationship, budget, preferences, and known taboos, with reasons, alternatives, exclusions, and clarifying questions when details are missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this Chinese-language skill to choose gifts for personal or professional situations. It helps tailor recommendations by relationship, budget, preferences, cultural taboos, and business gifting constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad gift-idea requests and can produce generic recommendations when relationship, budget, or preferences are missing.

Mitigation: Ask for budget tiers and preference directions before giving specific recommendations; label any non-personalized options.

Risk: Business or professional gifting advice may conflict with recipient rules, local norms, or compliance limits.

Mitigation: Treat compliance notes as prompts for human review and check the recipient organization's rules before acting.

Risk: The skill does not fetch current prices, seller links, or live product availability.

Mitigation: Use price ranges only and verify availability, current pricing, and seller legitimacy independently.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyuming0823/skills/ym-gift-pick-helper)
- [Server-Resolved Source Repository](https://github.com/liuyuming0823/ym-gift-pick-helper)
- [Relationship Rules](artifact/references/relationship-rules.md)
- [Gift Output Template](artifact/templates/gift-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown gift recommendations with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces three differentiated gift options when inputs are sufficient; asks up to three clarifying questions when key details are missing.]

## Skill Version(s):

0.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
