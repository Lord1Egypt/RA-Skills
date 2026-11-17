## Description:

Captures smart-home automation conflicts, sensor drift, device connectivity failures, integration regressions, safety rule gaps, and energy optimization opportunities for continuous domotics improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and smart-home operators use this skill to record automation conflicts, sensor and occupancy issues, device reachability failures, integration regressions, safety gaps, and energy optimization opportunities as structured markdown notes. It also provides reminder-only hook guidance for capturing recurring domotics patterns without directly controlling physical devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Smart-home logs may capture sensitive household information such as lock codes, tokens, network credentials, or personal schedules.

Mitigation: Keep logs free of secrets and personal schedules, and periodically clean up retained .learnings content.

Risk: Optional hooks persist after installation and may add reminders outside the intended scope if enabled too broadly.

Mitigation: Enable hooks only intentionally, keep them project-scoped, use narrow matchers, and avoid empty or catch-all hook matchers.

Risk: Guidance about high-impact routines could be misapplied to locks, alarms, gas or water shutoff, or heaters.

Mitigation: Treat the skill as documentation and reminder guidance only; require explicit human confirmation and conservative fallback behavior for high-impact routines.

## Reference(s):

- [Self Improving Domotics on ClawHub](https://clawhub.ai/jose-compu/skills/self-improving-house)
- [OpenClaw Integration (Domotics)](references/openclaw-integration.md)
- [Domotics Hook Setup Guide](references/hooks-setup.md)
- [Domotics Entry Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline bash commands, JSON hook examples, and markdown entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends project/workspace learning logs; optional hooks emit reminder-only guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
