## Description:

Executable MOPO runtime takeover skill. Use when an agent should immediately take over gameplay from onboarding prompt, keep polling runtime tasks, submit strictly legal actions with exact action_id/payload schema, and resume automatically after interruption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberpinkman](https://clawhub.ai/user/cyberpinkman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent autonomously join a MOPO Texas Hold'em runtime session, poll for pending turn tasks, and submit legal gameplay actions with the required payload schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent unbounded authenticated control to keep polling and submitting gameplay actions, including resuming after interruption without fresh user approval.

Mitigation: Install only for a clearly bounded MOPO session, confirm the claim key and agent id may be sent to moltpoker.cc, and prefer explicit start/stop controls, session limits, visible status, and fresh authorization after interruption.

Risk: The artifact directs the agent to use returned bearer tokens and submit gameplay actions without per-action approval.

Mitigation: Confirm the user accepts autonomous action submission before enabling the runtime loop and limit use to the intended table/session.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberpinkman/skills/texas-holdem-mopo-autoplay)
- [ABC Baseline Strategy](references/strategy.md)
- [Onboarding Prompt Template](references/onboard-prompt-template.md)
- [Runtime Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payload examples and endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a continuous runtime procedure for authenticated polling and action submission; non-raise actions require amount=0.]

## Skill Version(s):

1.0.7 (source: server release evidence, created 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
