## Description:

Track your own workarounds for bugs in other people's software; on each new release check with evidence whether the fix really shipped (merged is not released; backports via code markers) and recommend removal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holgergruenhagen](https://clawhub.ai/user/holgergruenhagen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system owners use this skill to track local workarounds and decide, with release and code evidence, whether each should stay or can be removed after a retest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a possible external transmission and an unresolved local reference, with partial scan coverage; the reported download appears purpose-related, but evidence is incomplete.

Mitigation: Review the upstream requests and local references used for each check, and verify the evidence before acting on a removal recommendation.

## Reference(s):

- [Upstream Fix Watch on ClawHub](https://clawhub.ai/holgergruenhagen/skills/upstream-fix-watch)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Analysis]

**Output Format:** [Markdown report and workaround register entries, or JSON register entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-backed verdicts with removal, retest, and rollback guidance; the owner carries out any removal.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
