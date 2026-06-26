## Description: <br>
Instance A skill for TallyPrime that parses invoice and bill PDFs or images from Telegram or WhatsApp, extracts structured accounting data, and posts canonical JSON to a configured bridge service for downstream Tally entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meetpaladiya44](https://clawhub.ai/user/meetpaladiya44) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accountants, CAs, and finance operators use this skill to turn invoice or bill documents received in chat into validated voucher payloads for TallyPrime. It is intended to reduce manual data entry while prompting for clarification when extraction confidence or accounting fields are incomplete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles sensitive invoice, GSTIN, ledger, and accounting data across chat messages, bridge requests, and Tally results. <br>
Mitigation: Use only trusted Telegram or WhatsApp channels and a controlled bridge deployment; restrict access to message history, bridge logs, and Tally output. <br>
Risk: The skill can trigger downstream Tally entries after extraction, so incorrect or low-confidence fields could affect accounting records. <br>
Mitigation: Require user confirmation for low-confidence fields, failed validation checks, high-value documents, and ambiguous voucher types before posting. <br>
Risk: Bridge credentials and HMAC secrets are required to authorize requests. <br>
Mitigation: Store BRIDGE_URL, BRIDGE_BEARER, and BRIDGE_HMAC_SECRET as protected environment variables, rotate shared secrets when access changes, and avoid exposing them in chat or logs. <br>
Risk: A misconfigured or untrusted bridge or tunnel could expose accounting operations outside the intended environment. <br>
Mitigation: Verify ownership and reachability of the bridge endpoint before use, keep Tally access on the controlled client machine, and require authenticated, signed requests for mutating operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meetpaladiya44/tally-extractor) <br>
- [Bridge HTTP Contract](artifact/reference/bridge.md) <br>
- [Extraction Schema](artifact/reference/extraction-schema.md) <br>
- [Telegram Reply Templates](artifact/reference/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with canonical JSON payloads, curl examples, and accountant-facing reply text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRIDGE_URL, BRIDGE_BEARER, and BRIDGE_HMAC_SECRET; generated voucher payloads include confidence scores, idempotency keys, and validation checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
