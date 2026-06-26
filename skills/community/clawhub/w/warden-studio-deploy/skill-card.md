## Description: <br>
Uses Warden Studio browser automation to register or publish a Community Agent to the Warden Agent Hub with endpoint, authentication, billing, payment, and verification checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kryptopaid](https://clawhub.ai/user/Kryptopaid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare, register, and verify a Community Agent listing in Warden Studio. It guides browser-based submission, endpoint and billing checks, explicit publication approval, and post-registration verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing can trigger registration fees, gas costs, or wallet signing on the wrong network. <br>
Mitigation: Before final registration, verify the official Studio URL, Base network, USDC fee, gas estimate, and wallet prompt, then require explicit user approval. <br>
Risk: Secrets could be exposed if API keys, seed phrases, or private keys are shared in chat. <br>
Mitigation: Never request seed phrases or private keys; instruct users to enter API keys only directly into the Studio UI. <br>
Risk: Incorrect endpoint, authentication, or billing settings can produce a failed or misleading listing. <br>
Mitigation: Use read-only validation first, test the endpoint when the UI supports it, and show a submission summary before publishing. <br>


## Reference(s): <br>
- [Warden Studio UI Notes](references/warden-studio-ui-notes.md) <br>
- [Warden Studio](https://studio.wardenprotocol.org/) <br>
- [Warden Studio Register Agent](https://studio.wardenprotocol.org/agents/create) <br>
- [ClawHub Skill Page](https://clawhub.ai/Kryptopaid/warden-studio-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Browser automation steps] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before final registration or wallet confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
