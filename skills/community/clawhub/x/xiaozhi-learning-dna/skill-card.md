## Description:

With explicit consent, maintains a student's long-term learning profile and supports viewing, correcting, exporting, and deleting it, with separate controls for sensitive profile features and sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

Students, guardians, and educators use the skill to manage consent-based learning profiles for ongoing personalized tutoring, including controlled updates, access, export, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports medium-confidence concerns about consent for persistent student profiles and adherence to the skill's stated limits; part of the artifact was only partially analyzed.

Mitigation: Before use with minors, verify student identity separation and required guardian consent, and keep sensitive tracking and sharing disabled unless separately authorized. If the platform cannot enforce profile isolation and access controls, limit use to the current session.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qizhitang/skills/xiaozhi-learning-dna)
- [DNA profile schema](schemas/dna-profile.schema.json)
- [DNA profile schema guide](schemas/README.md)
- [Growth milestones](references/growth-milestones.md)
- [Crisis referral protocol](references/crisis-referral-protocol.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON learning profiles and handover records; plain-text summaries and exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile access and sharing depend on explicit consent and platform access controls.]

## Skill Version(s):

2.12.7 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
