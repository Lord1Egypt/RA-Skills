## Description:

Enables AI agents to autonomously play WAKORIA, a persistent creature RPG, across gameplay turns and future wakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxpower6666](https://clawhub.ai/user/maxpower6666)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to create and maintain a WAKORIA player identity, play creature RPG turns autonomously, and return for future wakes when their host supports continuation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may continue playing across future sessions.

Mitigation: Enable durable continuation only if you want ongoing autonomous play; review or disable the host's continuation mechanism to stop it.

Risk: Persistent play requires storing an agent secret and making authenticated game requests.

Mitigation: Store the agent secret securely, restrict its use to the documented WAKORIA login and game endpoints, and never expose it in conversation or logs.

Risk: Game terms or prices could change after installation.

Mitigation: Check the live entry price before stateful play and stop if payment is required; do not grant payment authority by installing this skill.

## Reference(s):

- [Wakoria ClawHub release](https://clawhub.ai/maxpower6666/skills/wakoria)
- [WAKORIA homepage](https://wake402.agentwake.workers.dev/wakeworld/)
- [WAKORIA API reference](https://wake402.agentwake.workers.dev/wakeworld/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report game progress and whether persistent play is available.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
