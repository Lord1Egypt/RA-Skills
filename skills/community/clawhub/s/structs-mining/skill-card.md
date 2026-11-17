## Description:

Guides Structs resource extraction by mining ore, refining it into Alpha Matter, and verifying resource state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Structs operators use this skill to plan and run ore mining, ore refining, and post-transaction verification with the Structs CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mining and refining commands can launch long-running transactions that auto-submit completion later, after game state may have changed.

Mitigation: Confirm the struct ID, owner key, current ore, and acceptance of deferred auto-submission before launch; re-check running jobs through the documented reconnect flow.

Risk: Ore remains stealable until it is refined into Alpha Matter.

Mitigation: Refine promptly after mining completes and verify planet, struct, and player resource state after completion.

## Reference(s):

- [Structs Safety](https://structs.ai/SAFETY)
- [Structs Async Operations](https://structs.ai/awareness/async-operations)
- [Structs Async Operations Reconnect Protocol](https://structs.ai/awareness/async-operations#reconnecting-to-a-long-job)
- [Structs Resource Mechanics](https://structs.ai/knowledge/mechanics/resources)
- [Structs Planet Mechanics](https://structs.ai/knowledge/mechanics/planet)
- [Alpha Matter Lore](https://structs.ai/knowledge/lore/alpha-matter)
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL)
- [Structs Mining on ClawHub](https://clawhub.ai/abstrct/skills/structs-mining)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include long-running background transaction guidance and verification steps.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
