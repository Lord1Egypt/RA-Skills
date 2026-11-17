## Description:

Create, sign, and verify WachAI Mandates (verifiable agent-to-agent agreements).

This skill is ready for commercial/non-commercial use.

## Publisher:

[akshat-mishra101](https://clawhub.ai/user/akshat-mishra101)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to create, sign, inspect, verify, and exchange cryptographically signed WachAI Mandates for agent-to-agent agreements. It is suited to workflows where parties need a durable record of intent and acceptance, such as payments, swaps, services, deliveries, or other commerce-heavy coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet files can contain private key material.

Mitigation: Protect ~/.wachai/wallet.json as sensitive credential material and avoid shared or synced storage directories.

Risk: A global latest npm install can introduce unreviewed CLI changes into the user's environment.

Mitigation: Use a pinned package version or an isolated environment before adopting the CLI in routine workflows.

Risk: Received or older mandates may be stale, unexpected, or unsuitable to sign.

Mitigation: Inspect mandate JSON before signing, sending, or relying on it.

## Reference(s):

- [WachAI Terminal](https://github.com/quillai-network/WachAI-Terminal)
- [ClawHub Skill Page](https://clawhub.ai/akshat-mishra101/skills/wachai-mandates)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation and handling of local wallet and mandate JSON files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
