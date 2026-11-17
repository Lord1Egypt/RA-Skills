## Description:

Guides Chinese-language travel-planning conversations by clarifying vague requirements step by step, using trip length and budget to narrow options, and optionally preparing FlyAI CLI searches for hotels, points of interest, and flights once required details are known.

This skill is ready for commercial/non-commercial use.

## Publisher:

[david-cai-gpt](https://clawhub.ai/user/david-cai-gpt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn vague Chinese-language travel requests into practical itinerary directions, budget assumptions, and search-ready travel constraints. It supports hotel, attraction, and flight scanning through FlyAI commands only after required dates, destinations, budgets, and departure details are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents FlyAI commands with TLS certificate checks disabled.

Mitigation: Remove the TLS-bypass environment variable and require valid certificates before using the commands.

Risk: User-provided travel values may be incorporated into shell commands.

Mitigation: Use safe argument handling and validate dates, prices, city names, and keyword values before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/david-cai-gpt/skills/travel-schedule-brainstrom)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese-language Markdown with optional bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include FlyAI command examples after required travel constraints are known.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
