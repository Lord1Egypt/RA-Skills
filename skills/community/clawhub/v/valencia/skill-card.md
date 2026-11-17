## Description:

Navigate Valencia as visitor, resident, tech worker, student, or entrepreneur with neighborhoods, transport, costs, visas, and local insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to answer Valencia travel, relocation, work, study, business, and daily life questions. The skill helps an agent tailor guidance by user role, timeline, EU status, budget, and local priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store sensitive personal, immigration, healthcare, tax, address, and contact details in a persistent plaintext profile.

Mitigation: Use coarse statuses or masked values, avoid full NIE, SIP, Social Security numbers, exact address, third-party contacts, and detailed income or immigration information, and restrict file permissions.

Risk: The skill includes visa, tax, healthcare, school, and business guidance that can become outdated or depend on personal circumstances.

Mitigation: Treat the skill as a local Markdown reference and verify requirements with official sources or qualified local professionals before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/valencia)
- [Skill homepage](https://clawic.com/skills/valencia)
- [Setup guide](artifact/setup.md)
- [Personal profile template](artifact/memory-template.md)
- [Valencia city services](https://www.valencia.es)
- [Visit Valencia](https://www.visitvalencia.com)
- [Spain immigration portal](https://extranjeros.inclusion.gob.es)
- [Metrovalencia](https://www.metrovalencia.es)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with tables, checklists, and local reference file recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user to maintain local Markdown profile and progress files for personalization.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
