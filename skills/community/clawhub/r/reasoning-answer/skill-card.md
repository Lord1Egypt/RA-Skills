## Description:

Provides detailed reasoning-based answers in the user's language by default, with clickable citation footnotes when referencing sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvinecarn](https://clawhub.ai/user/alvinecarn)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide agents toward detailed reasoning answers that preserve the user's language preference and format citations as clickable, sequential footnotes when sources are used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Citation-formatting guidance could make unsupported or stale references look authoritative if source-backed claims are not checked.

Mitigation: Review source-backed claims and verify that each numbered citation points to the intended source before relying on the answer.

Risk: The skill changes answer-formatting behavior, including language matching and reference lists, which may conflict with a host agent's citation or style policy.

Mitigation: Test the skill in the target agent environment and set higher-priority citation or language instructions when local policy differs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown text with clickable numbered footnote citations when sources are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps the user's language unless explicitly changed.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
