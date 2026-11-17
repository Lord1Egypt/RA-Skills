## Description:

Use Warden Studio (studio.wardenprotocol.org) via browser automation to register/publish a Community Agent to the Warden Agent Hub with read-only validation and explicit confirmation gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryptopaid](https://clawhub.ai/user/kryptopaid)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to publish an already deployed Community Agent in Warden Studio, including endpoint checks, listing metadata, billing setup, registration payment review, and post-publish verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing a public agent listing or paying registration and gas fees can have unintended financial or operational effects.

Mitigation: Review the submission summary, network, fee, and transaction details before approving any final publish action or wallet prompt.

Risk: API keys, wallet credentials, or other secrets could be exposed if pasted into chat.

Mitigation: Enter API keys directly in Warden Studio and never provide seed phrases, private keys, or credentials to the agent.

Risk: Incorrect endpoint, billing, or metadata settings could publish a misleading or nonfunctional listing.

Mitigation: Use read-only validation, confirm the endpoint is HTTPS and reachable, verify required fields, and inspect the final listing details before submission.

## Reference(s):

- [Warden Studio UI Notes](references/warden-studio-ui-notes.md)
- [Warden Studio](https://studio.wardenprotocol.org/)
- [Warden Studio Register Agent Page](https://studio.wardenprotocol.org/agents/create)
- [ClawHub Skill Page](https://clawhub.ai/kryptopaid/skills/warden-studio-deploy)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with checklists and browser-action steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-controlled entry of secrets and explicit approval before publishing, fee payment, or wallet signing.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
