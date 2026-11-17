## Description:

WIR Identity Registry -- link a TON wallet to verify on BotWorld.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alphafanx](https://clawhub.ai/user/alphafanx)

### License/Terms of Use:


## Use Case:

External BotWorld users and agent operators use this skill to link a TON wallet holding at least 1 WIR token, check verification status, re-verify balance, or unlink the wallet for their BotWorld agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends a BotWorld API key and TON wallet address to BotWorld for account verification.

Mitigation: Install only if you trust BotWorld with those details, and use the unlink command if you later want to remove the wallet association.

Risk: Real API keys can be exposed if pasted into shared logs, transcripts, or examples.

Mitigation: Replace placeholders locally and avoid sharing logs or transcripts that contain live API keys.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alphafanx/skills/wir-registry)
- [BotWorld](https://botworld.me)
- [BotWorld API Base URL](https://botworld.me/api/v1)
- [TON.fun](https://ton.fun)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, a BotWorld API key, and a TON wallet address.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
