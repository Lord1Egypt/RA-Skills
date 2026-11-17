## Description:

Use for factual, comparison, or support/capability questions, or when the user challenges accuracy: verify via search, documentation, or runtime evidence before answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[padepa](https://clawhub.ai/user/padepa)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to make agents verify factual, comparison, capability, relationship, and current-status questions before responding. It helps distinguish supported claims, explicit negative findings, partial evidence, and cases where no reliable source was found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can increase latency or require external lookups because it asks the agent to verify factual claims before answering.

Mitigation: Use trusted search, documentation, or runtime sources and disclose when reliable evidence cannot be found.

Risk: Installing with an unpinned ClawHub installer can expose users to installer changes outside this skill release.

Mitigation: Install only from trusted publishers and prefer a pinned ClawHub installer version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/padepa/skills/verify-before-answer)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown text with cited findings and occasional inline shell commands when runtime checks are relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include source boundaries, evidence timestamps, and explicit uncertainty statements.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
