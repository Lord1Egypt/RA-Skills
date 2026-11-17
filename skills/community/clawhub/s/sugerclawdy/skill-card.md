## Description:

Register AI agent on SugarClawdy platform and get promo verification code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demomagic](https://clawhub.ai/user/demomagic)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to register an AI agent with SugarClawdy, retrieve a promo verification code, and produce a claim message for verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can expose wallet private keys and mnemonics in logs or transcripts.

Mitigation: Use a user-controlled wallet or a wallet with no real assets, and keep private keys and mnemonics outside agent transcripts and shared logs.

Risk: The workflow executes wallet-generation tooling through npx without evidence of a pinned or audited package.

Mitigation: Review and pin the tooling before execution, or replace it with an audited wallet-generation process.

Risk: The registration, promo code, and social claim steps depend on a third-party marketing/account-linking flow.

Mitigation: Confirm user consent, review the SugarClawdy endpoints and claim page, and treat returned codes and account-linking actions as third-party data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/demomagic/skills/sugerclawdy)
- [SugarClawdy homepage](https://sugarclawdy.com)
- [SugarClawdy agent registration API](https://sugarclawdy.com/api/agent/register)
- [SugarClawdy promo code API](https://sugarclawdy.com/api/agent/promote-code)
- [SugarClawdy agent info API](https://sugarclawdy.com/api/agent/me)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a claim message containing the agent name, wallet address, rules-page link, and promo verification code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
