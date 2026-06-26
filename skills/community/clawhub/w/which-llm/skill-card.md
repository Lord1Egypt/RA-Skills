## Description: <br>
Deterministic decision-ranking API with HTTP 402 payments and outcome credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zapkid](https://clawhub.ai/user/Zapkid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose an LLM deterministically under explicit cost and quality constraints, then report outcomes to receive credits for later paid requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid Which-LLM API requests may require wallet-backed USDC payments. <br>
Mitigation: Use per-request confirmation, a low-balance wallet, spending caps, and independent verification of recipient and amount before payment. <br>
Risk: Wallet addresses, transaction IDs, payment headers, and credit tokens can expose sensitive payment metadata if logged. <br>
Mitigation: Redact payment identifiers, payment proof headers, and credit tokens from prompts, logs, tickets, and shared transcripts. <br>
Risk: The skill depends on an external API and may retry paid requests after payment is satisfied. <br>
Mitigation: Check free status, pricing, and capabilities endpoints before paid use, and require host-managed approval for outbound API calls and payment retries. <br>


## Reference(s): <br>
- [Which-LLM homepage](https://which-llm.com) <br>
- [Which-LLM API](https://api.which-llm.com) <br>
- [Which-LLM payment addresses](https://which-llm.com/docs/payment-addresses) <br>
- [ClawHub skill page](https://clawhub.ai/Zapkid/which-llm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown instructions with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; paid requests may require host-managed wallet payment handling.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
