## Description:

This skill establishes a skill-routing discipline for agents at the start of conversations, requiring relevant skills to be checked before any response or action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianjin-ren](https://clawhub.ai/user/tianjin-ren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make skill discovery and invocation a required first step before answering, asking clarifying questions, or taking task actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to broadly control the agent workflow for every conversation and may cause unnecessary skill invocations.

Mitigation: Install only when a global skill-routing discipline is desired, and review the mandatory invocation wording before deployment.

Risk: Later-loaded skills can gain more influence over the session than users may expect.

Mitigation: Keep the available skill set trusted and review newly added skills before enabling this workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianjin-ren/skills/using-superpowers-tianjin)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance with a DOT process diagram]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires agents to check for relevant skills before responses or actions.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
