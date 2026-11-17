## Description:

Extracts structured fields from telegraphic transfer voucher images, including remitter and payee names, account numbers, amount, date, and remitting and receiving banks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Agents and users who process telegraphic transfer vouchers use this skill to send a local image or PDF to Scnet OCR and receive structured voucher fields for downstream review or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads bank-transfer voucher files to Scnet's external OCR service, which may expose sensitive financial document contents.

Mitigation: Use only when the user intends to send the document to Scnet, redact unnecessary financial data when practical, and verify SCNET_API_BASE points to the intended HTTPS Scnet endpoint.

Risk: Voucher OCR fields may include sensitive account information and payment-password fields.

Mitigation: Limit inputs to necessary documents, avoid uploading unredacted payment passwords when possible, and handle returned JSON as sensitive data.

Risk: Dependency and runtime behavior depends on Python requests and a configurable remote API endpoint.

Mitigation: Install dependencies in an isolated environment with pinned versions where possible and review config/.env before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/telegraph-transfer-ocr)
- [Publisher profile](https://clawhub.ai/user/scnet-sugon)
- [Sugon-Scnet OCR API summary](references/api-docs.md)
- [Telegraphic transfer voucher field summary](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON OCR results on stdout, with text error messages for configuration, authentication, file, network, and API failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and accepts TELEGRAPHIC_TRANSFER_VOUCHER plus a local file path.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
