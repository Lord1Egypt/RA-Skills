## Description: <br>
Swaps Intel lets agents query the Swaps Intelligence API for cryptocurrency address risk scoring, transaction tracing, and transaction risk signals across EVM, TRON, Bitcoin, Solana, XRP, TON, and other chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w3arecom](https://clawhub.ai/user/w3arecom) <br>

### License/Terms of Use: <br>
proprietary <br>


## Use Case: <br>
External users and agents use this skill to triage cryptocurrency wallet addresses and transactions for risk indicators, labels, and trace context. Outputs should support fraud-prevention, safety triage, and non-binding compliance pre-check workflows rather than definitive legal, financial, or investigative conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses or transaction hashes are sent to the external Swaps Intelligence API. <br>
Mitigation: Install only when users are comfortable sharing queried identifiers with Swaps Intelligence and keep logs minimal. <br>
Risk: Risk labels and scores may contain false positives, false negatives, or probabilistic attribution. <br>
Mitigation: Present outputs as signals or heuristic indicators and require independent verification before legal, compliance, financial, or public accusation actions. <br>
Risk: Open access can be misused for harassment, doxxing, unsupported accusations, or high-volume probing. <br>
Mitigation: Use key-based authentication, rate limits, abuse monitoring, and a correction or challenge path for disputed labels. <br>


## Reference(s): <br>
- [Swaps Intel ClawHub page](https://clawhub.ai/w3arecom/swaps-intel) <br>
- [Swaps product page](https://www.swaps.app/search) <br>
- [Swaps homepage](https://swaps.app) <br>
- [OpenAPI contract](artifact/openapi.json) <br>
- [Risk disclosure](artifact/RISK_DISCLOSURE.md) <br>
- [Acceptable Use Policy](artifact/AUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Swaps Intel API key; user-facing outputs must preserve returned factual fields, include request IDs when available, and frame results as heuristic risk signals.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
