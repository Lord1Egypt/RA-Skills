## Description: <br>
TrustBoost PII Sanitizer helps agents send text to a remote TrustBoost API for context-aware PII redaction before content is passed to LLMs or other downstream services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teodorofodocrispin-cmyk](https://clawhub.ai/user/teodorofodocrispin-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous-agent operators use this skill to redact PII from user-generated text before sending content to LLM providers or external services. It is intended for workflows that can accept third-party API processing and want trial or paid quota-based sanitization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw text is sent to a third-party TrustBoost service before redaction. <br>
Mitigation: Install only when external processing and retention terms are acceptable; do not submit production secrets, private keys, passwords, or regulated records unless that policy has been approved. <br>
Risk: The skill supports paid usage through Solana transactions. <br>
Mitigation: Use trial mode first and set explicit operator-controlled limits before allowing any autonomous paid transaction. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teodorofodocrispin-cmyk/trustboost-pii-sanitizer) <br>
- [TrustBoost PII Sanitizer Repository](https://github.com/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer) <br>
- [TrustBoost Sanitization API](https://api.trustboost.dev/sanitize) <br>
- [TrustBoost Preview API](https://api.trustboost.dev/sanitize/preview) <br>
- [TrustBoost MCP Server](https://api.trustboost.dev/mcp) <br>
- [Agent Evaluation Report](https://github.com/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer/blob/main/AGENT_EVALUATION.md) <br>
- [Live Demo](https://huggingface.co/spaces/TrustBoost/pii-sanitizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access to the TrustBoost API; paid use can involve Solana USDC transaction hashes.] <br>

## Skill Version(s): <br>
2.0.7 (source: ClawHub release metadata; artifact frontmatter reports 2.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
