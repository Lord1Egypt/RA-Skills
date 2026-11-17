## Description:

Create polished client education handouts with visuals, FAQs, and clear next steps tailored for executive recruiting boutique firms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External recruiting consultants, talent partners, and boutique executive search teams use this skill to draft client-facing education handouts that explain services, answer common questions, and outline next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Bash and local file-read authority that is not explained by the handout-generation workflow.

Mitigation: Install only in environments where shell execution and local file access are acceptable, or prefer a revised version that removes Bash and narrows file access to user-provided handout assets.

Risk: Generated recruiting handouts may include biased, inaccurate, or overly decisive employment-related guidance.

Mitigation: Require human review before client use and avoid relying on generated content for screening, selection, or employment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-generate-executive-recruiting-boutique-client-education-handout)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [SkillBoss skill homepage](https://www.skillboss.co/skills/generate-executive-recruiting-boutique-client-education-handout)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown handout draft with client education copy, FAQ content, visual directions, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommendations for visuals generated through chat and image generation APIs; human review is recommended before client delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
