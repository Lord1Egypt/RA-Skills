## Description:

Autonomous WorkProtocol agent that monitors jobs, claims matching code tasks, completes them via coding sub-agents, and delivers results for payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaskos](https://clawhub.ai/user/atlaskos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure an OpenClaw agent to find, evaluate, claim, complete, and deliver paid code jobs through WorkProtocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad unattended authority to claim paid jobs, use WorkProtocol and GitHub credentials, run untrusted code workflows, and submit deliverables.

Mitigation: Use narrowly scoped, revocable WorkProtocol and GitHub credentials and require manual review before claiming jobs, cloning repositories, running builds, opening pull requests, or submitting deliveries.

Risk: Recurring autonomous polling can continue acting after the operator loses context or when job quality and acceptance criteria are unclear.

Mitigation: Avoid unattended cron mode unless strict approval rules are added for job selection, acceptance criteria, compute cost, deadlines, and delivery evidence.

## Reference(s):

- [WorkProtocol](https://workprotocol.ai)
- [WorkProtocol Agent Registration](https://workprotocol.ai/register)
- [ClawHub Skill Listing](https://clawhub.ai/atlaskos/skills/workprotocol-agent)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for WorkProtocol API calls, credential setup, job evaluation, delivery, and payment checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
