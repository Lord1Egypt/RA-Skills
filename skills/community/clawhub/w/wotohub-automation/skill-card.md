## Description: <br>
End-to-end WotoHub influencer outreach automation for product understanding, creator search, recommendation ranking, outreach email drafting, batch send, inbox review, and guarded reply assist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sa461151](https://clawhub.ai/user/sa461151) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams and developers use this skill to run WotoHub creator outreach campaigns for TikTok Shop, Amazon, and Shopify products, from product understanding through creator discovery, draft generation, sending, inbox review, and guarded reply assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WOTOHUB_API_KEY can enable outreach sending and inbox access. <br>
Mitigation: Use the credential only for intended authenticated WotoHub operations, store it securely, and validate it before send, inbox, reply, or campaign-cycle actions. <br>
Risk: Scheduled_send, safe_auto_send, and persistent campaign automation can send messages without a manual action at runtime. <br>
Mitigation: Review scheduled_send and safe_auto_send policies before scheduled cycles, and enable createCron only when persistent automation is intended. <br>
Risk: Locally configured bridge executors can run with broad host access. <br>
Mitigation: Keep bridge executor settings and campaign brief files trusted, validate host-injected data against schemas, and avoid accepting near-final execution payloads from untrusted model output. <br>
Risk: Disabling TLS verification can expose authenticated WotoHub traffic. <br>
Mitigation: Leave TLS verification enabled by default and only disable it in a controlled debug environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sa461151/wotohub-automation) <br>
- [Auth Guide](appendix-auth.md) <br>
- [Integration Contract](references/integration-contract.md) <br>
- [Runtime Guardrails](references/runtime-guardrails.md) <br>
- [Third-Party Integration Guide](references/third-party-integration-guide.md) <br>
- [Campaign Brief Schema](references/campaign-brief-schema.md) <br>
- [Search Parameters](references/search-params.md) <br>
- [Outreach Email Schema](references/outreach-email-schema.md) <br>
- [Conversation Analysis Schema](references/conversation-analysis-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON and Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API payloads, outreach drafts, campaign summaries, state summaries, and guarded reply previews; authenticated send and inbox actions require WOTOHUB_API_KEY.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
