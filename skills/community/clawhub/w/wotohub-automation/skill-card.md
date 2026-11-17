## Description:

End-to-end WotoHub influencer outreach automation for product understanding, creator search, recommendation ranking, outreach email drafting, batch send, inbox review, and guarded reply assist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sa461151](https://clawhub.ai/user/sa461151)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run WotoHub creator outreach campaigns for TikTok Shop, Amazon, Shopify, and recurring creator prospecting workflows. It helps convert product descriptions or product URLs into creator search, recommendation, outreach draft, send, inbox review, and guarded reply-assist flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact local command execution can be exposed through executor fields, request configuration, and campaign brief paths.

Mitigation: Run the skill in an isolated environment, pass only trusted request configuration and brief paths, and constrain host bridge executors to fixed trusted commands.

Risk: The WOTOHUB_API_KEY credential enables authenticated user-state actions such as sending, inbox access, reply handling, and campaign cycles.

Mitigation: Treat the token as a send and inbox credential, keep it out of shared logs and prompts, and avoid CLI token entry when plaintext local persistence is unacceptable.

Risk: Product URL analysis and host-injected fields may introduce untrusted content into campaign planning.

Mitigation: Avoid untrusted product URLs, validate host-provided structures against the documented schemas, and block execution when required structured understanding is missing.

Risk: Scheduled cycles may send real outreach emails and low-risk replies automatically.

Mitigation: Use review-required or prepare-only modes for sensitive campaigns, and keep price, payment, contract, exclusivity, shipping, and timing commitments under human review.

Risk: Network actions depend on secure API communication.

Mitigation: Keep TLS verification enabled except in controlled debugging environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sa461151/skills/wotohub-automation)
- [Publisher profile](https://clawhub.ai/user/sa461151)
- [Integration contract](references/integration-contract.md)
- [Runtime guardrails](references/runtime-guardrails.md)
- [Third-party integration guide](references/third-party-integration-guide.md)
- [Campaign brief schema](references/campaign-brief-schema.md)
- [Model analysis schema](references/model-analysis-schema.md)
- [Conversation analysis schema](references/conversation-analysis-schema.md)
- [Outreach email schema](references/outreach-email-schema.md)
- [Search parameters](references/search-params.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON task results, Markdown guidance, email drafts, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform WotoHub API actions, stateful campaign cycles, email sending, inbox review, and guarded reply previews when configured with the required credential.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
