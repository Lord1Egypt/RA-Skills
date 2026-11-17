## Description:

Give your AI agent access to your health and fitness data from RUNSTR. Fetches workouts, habits, journal entries, mood, steps, and more from Nostr. Use when the user asks about their workouts, fitness history, health habits, mood tracking, or wants AI fitness coaching based on real data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thewildhustle](https://clawhub.ai/user/thewildhustle)

### License/Terms of Use:


## Use Case:

External users use this skill to let an agent fetch and analyze RUNSTR fitness backups from Nostr for workout summaries, habit accountability, mood and energy trends, step history, and fitness coaching based on their own data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to provide a full Nostr private key for decrypting RUNSTR backups.

Mitigation: Use a dedicated fitness-only Nostr identity or a local signer/key manager instead of pasting a primary Nostr nsec into the agent.

Risk: The skill can produce and save sensitive health and fitness summaries.

Mitigation: Persist health summaries only after explicit user consent, and provide a review and deletion path for stored summaries.

Risk: The install metadata uses a mutable latest version of the nak dependency.

Mitigation: Prefer a pinned and verified nak version before installation.

## Reference(s):

- [RUNSTR Skill Page](https://clawhub.ai/thewildhustle/skills/runstr-fitness)
- [RUNSTR Website](https://runstr.app)
- [RUNSTR GitHub Organization](https://github.com/RUNSTR)
- [nak Nostr Army Knife](https://github.com/fiatjaf/nak)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fitness summaries, trend analysis, troubleshooting guidance, and proposed memory summaries derived from user-authorized RUNSTR data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
