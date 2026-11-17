## Description:

Turns text-only ideas, outlines, documents, or drafts into structured, well-designed enterprise HTML presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[owenzhouzhou](https://clawhub.ai/user/owenzhouzhou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn text-only source material into enterprise-style HTML slide presentations. The skill delegates generation to Alipay-hosted services, so it is best suited to non-sensitive presentation drafts unless remote-processing terms are separately confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected conversation history may be sent to Alipay-hosted endpoints.

Mitigation: Avoid confidential business data, personal data, credentials, and private documents unless remote processing, retention, and cleanup guarantees are documented.

Risk: Conversation context and session IDs may be stored in plaintext temporary local files.

Mitigation: Use an isolated environment for execution and remove related temporary files after use.

Risk: The skill delegates work to an external service and maintains changing remote session state.

Mitigation: Review the skill before installation, disclose external processing to users, and confirm failures or expired sessions do not expose sensitive context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/owenzhouzhou/skills/slide-writer-alipay-pay)
- [Alipay AgentPay proxy endpoint](https://agentpay.alipay.com/ai-pay/proxy/2088902259764064/S00000001784191990656)
- [Alipay streaming query endpoint](https://aipaymerchantorder-pre.alipay.com/test/agent/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text containing generated HTML presentation code and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-only inputs; remote responses are returned as streamed text.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
