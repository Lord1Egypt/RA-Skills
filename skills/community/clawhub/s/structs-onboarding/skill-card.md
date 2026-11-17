## Description:

Onboards a new player into Structs. Handles key creation/recovery, player creation (via reactor-infuse or guild signup), planet exploration, and initial infrastructure builds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to onboard a fresh Structs player, create or recover keys, join through reactor infusion or guild signup, explore a first planet, and start initial infrastructure builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet recovery phrases and generated mnemonics can grant account control if exposed in logs, command history, or transcripts.

Mitigation: Use a secret store or non-logged environment handling, avoid command-line mnemonics, avoid logging script output, and rotate any mnemonic that may have been exposed.

Risk: Remote guild signup endpoints receive signed onboarding payloads and can affect account onboarding if the endpoint is incorrect or unsafe.

Mitigation: Prefer independently verified HTTPS guild endpoints and cross-check the endpoint against the on-chain guild record before posting signup data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abstrct/skills/structs-onboarding)
- [Structs interface routing](https://structs.ai/skills/conventions#choosing-your-interface-capability-aware)
- [Structs safety contract](https://structs.ai/SAFETY)
- [Structs agent security awareness](https://structs.ai/awareness/agent-security)
- [Structs UGC moderation mechanics](https://structs.ai/knowledge/mechanics/ugc-moderation#official-webapp-client-convention-the-5-layer-avatar)
- [Structs building mechanics](https://structs.ai/knowledge/mechanics/building)
- [Structs async operations awareness](https://structs.ai/awareness/async-operations)
- [Structs CLI install skill](https://structs.ai/skills/structsd-install/SKILL)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown instructions with shell commands and a Node.js helper that returns JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet mnemonics, addresses, public keys, player IDs, guild IDs, signup responses, and next-step commands.]

## Skill Version(s):

1.25.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
