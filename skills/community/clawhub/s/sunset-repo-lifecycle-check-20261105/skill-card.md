## Description:

Write a short repository recreation checklist from facts supplied by the user. Text-only test skill for a source repository lifecycle experiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunset-wave](https://clawhub.ai/user/sunset-wave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn user-supplied repository lifecycle observations into a short checklist. It records any supplied repository URL and commit, availability observations, registry listing and audit availability, and before-and-after comparisons without assuming that matching repository names prove matching identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied repository facts or availability observations may be incorrect or incomplete.

Mitigation: Use only the supplied facts, mark unknown availability as ‘not checked’, and verify repository identity from the supplied URL and commit rather than its name alone.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sunset-wave/skills/sunset-repo-lifecycle-check-20261105)
- [Publisher profile: sunset-wave](https://clawhub.ai/user/sunset-wave)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Four concise checklist items; unknown availability is recorded as ‘not checked’.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
