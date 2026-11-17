## Description:

Context-aware PII sanitization for autonomous AI agent pipelines that sends text to the TrustBoost API, redacts detected PII across supported languages, and returns sanitized text with safety and risk metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teodorofodocrispin-cmyk](https://clawhub.ai/user/teodorofodocrispin-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to sanitize user-generated or workflow text before sending it to LLMs or external services. It is intended for multilingual privacy-risk reduction where a remote third-party API is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw input is transmitted to a third-party remote API before sanitization.

Mitigation: Install only where third-party processing is approved; do not send secrets, private keys, passwords, regulated records, or zero-transmission workloads without separate contractual and technical controls.

Risk: The skill includes autonomous cryptocurrency payment guidance.

Mitigation: Do not grant agents wallet-signing authority or automatic USDC payment capability through this skill; handle billing manually or through a separately approved payment workflow.

Risk: Sanitization may not remove every sensitive value in adversarial or high-risk inputs.

Mitigation: Review sanitized output before downstream use in sensitive workflows and treat the service as risk reduction rather than a complete data-loss-prevention control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teodorofodocrispin-cmyk/skills/trustboost-pii-sanitizer)
- [TrustBoost API Endpoint](https://api.trustboost.dev/sanitize)
- [TrustBoost Preview Endpoint](https://api.trustboost.dev/sanitize/preview)
- [TrustBoost MCP Server](https://api.trustboost.dev/mcp)
- [GitHub Repository](https://github.com/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer)
- [Agent Evaluation Report](https://github.com/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer/blob/main/AGENT_EVALUATION.md)
- [MOLT Schema](https://raw.githubusercontent.com/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer/main/molt.json)
- [Live Demo](https://huggingface.co/spaces/TrustBoost/pii-sanitizer)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with curl examples and JSON request/response payloads; runtime API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access to TrustBoost API; paid use may involve Solana USDC transaction fields.]

## Skill Version(s):

2.0.7 (source: server release metadata; artifact frontmatter declares 2.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
