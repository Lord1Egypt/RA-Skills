## Description:

Transition from vibe coding to vibe clawing by trusting agents with full responsibilities, designing self-closing loops, and climbing the bottleneck ladder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to coach agents toward autonomous workflow ownership: auditing loops, defining delegation boundaries, tracking bottlenecks, and escalating only when human judgment is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages delegation of agent responsibilities, which may be inappropriate for high-cost, irreversible, credentialed, customer-facing, financial, or production actions.

Mitigation: Review proposed automation before using it in those contexts and require human approval for consequential or hard-to-recover decisions.

Risk: Local tracking files under ~/vibe-clawing/ may accumulate secrets or sensitive business details.

Mitigation: Keep tracking files free of credentials, secrets, customer data, and sensitive business information.

Risk: A loop may be delegated before success criteria, escalation triggers, and failure recovery paths are clear.

Mitigation: Document decision criteria, define escalation triggers, test in parallel, monitor outcomes, and audit periodically before reducing human oversight.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ivangdavila/skills/vibe-clawing)
- [Identifying and Closing Loops](artifact/loops.md)
- [The Bottleneck Framework](artifact/bottleneck.md)
- [Where the Value Moves](artifact/direction.md)
- [The Evolution: From Vibe Coding to Vibe Clawing](artifact/evolution.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with local tracking-file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest creating or updating local tracking files under ~/vibe-clawing/.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
