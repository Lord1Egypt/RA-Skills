## Description:

Xena Protocol scans Gmail for phishing, crypto scams, impersonation, and business email compromise, with an optional Reporter mode that submits hashed reports to an on-chain registry on Ethereum Sepolia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickvanzo](https://clawhub.ai/user/nickvanzo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect a Gmail inbox, detect likely phishing and scam messages, and optionally participate in Reporter mode for shared on-chain threat reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires powerful Gmail read/modify access and may change inbox unread state during heartbeat processing.

Mitigation: Review the Gmail permissions and unread-label behavior before enabling heartbeat use; prefer manual runs until the workflow is understood.

Risk: Selected email content may be sent to an external LLM for ambiguous classifications.

Mitigation: Use the skill only with inboxes where that disclosure is acceptable, and avoid connecting accounts that may contain sensitive messages outside the intended security review scope.

Risk: Reporter mode uses a locally stored plaintext testnet wallet private key and may submit reports automatically.

Mitigation: Prefer Watcher mode unless reporting is required, fund the Reporter wallet only with tiny testnet amounts, and review Reporter behavior before enabling it.

Risk: Reporter mode can expose sender-domain metadata to an RPC provider and publish hashed reports to the Sepolia registry.

Mitigation: Enable Reporter mode only when this metadata exposure is acceptable; use Watcher mode for local detection without on-chain submissions.

## Reference(s):

- [Xena Protocol ClawHub release](https://clawhub.ai/nickvanzo/skills/xena-protocol)
- [Publisher profile](https://clawhub.ai/user/nickvanzo)
- [Project homepage from ClawHub metadata](https://github.com/NickVanzo/royal-hackathon-itu)
- [OpenClaw package](https://www.npmjs.com/package/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON parser outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces phishing classification summaries, setup instructions, status guidance, and optional transaction references; does not output full email contents as a primary result.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
