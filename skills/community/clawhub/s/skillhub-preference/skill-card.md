## Description:

Provides policy guidance to prefer skillhub for skill discovery, installation, and updates, with fallback to clawhub when skillhub is unavailable or finds no match.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcicq](https://clawhub.ai/user/pcicq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to standardize how agents search for, install, and update skills, including fallback behavior and pre-install risk summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes agent preference for skill-related tasks by trying skillhub before clawhub.

Mitigation: Review the source, version, and risk summary before approving any skill installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pcicq/skills/skillhub-preference)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Policy guidance may include the reported output of skillhub search commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
