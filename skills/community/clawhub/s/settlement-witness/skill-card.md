## Description:

Verify signed SAR v0.1 settlement receipts locally with Ed25519 and RFC 8785 canonicalization, with optional DefaultVerifier-signed remote receipt issuance when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutstrut](https://clawhub.ai/user/nutstrut)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent workflows use SettlementWitness before trusting task-complete, evidence, or settlement-adjacent claims by checking whether a SAR receipt's digest, Ed25519 signature, signer lifecycle, and verdict verify against the bundled registry. Remote receipt issuance is optional and should be used only when intentionally sending the selected task_id, spec, and output to DefaultVerifier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on unpinned Python packages.

Mitigation: Install in a controlled environment and pin or review dependency versions before production use.

Risk: Optional remote issuance sends the selected task_id, spec, and output to DefaultVerifier.

Mitigation: Use local verification for sensitive outputs and request remote issuance only when the payload is appropriate to share.

Risk: A valid:true result primarily proves cryptographic receipt validity and does not prove legal settlement finality, payment finality, or external-world truth.

Mitigation: Use the verifier result as evidence input only, and apply separate business, legal, or schema checks before taking consequential downstream action.

Risk: Offline verification uses the bundled registry snapshot and may not reflect newer live key rotations.

Mitigation: Refresh or override the registry from the published DefaultVerifier key registry when verifying receipts that may use newer signing keys.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nutstrut/skills/settlement-witness)
- [DefaultVerifier Homepage](https://defaultverifier.com)
- [Public Key Registry](https://defaultverifier.com/.well-known/sar-keys.json)
- [Receipt Explorer and Public Spec](https://defaultverifier.com/verified)
- [SAR v0.1 Canonicalization Reference](spec/canonicalization.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON verifier results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification can run offline against a pinned public key registry; optional remote issuance requires explicit user action.]

## Skill Version(s):

0.1.4 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
