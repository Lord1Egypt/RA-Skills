## Description:

Checks sender and beneficiary details in on-chain transfer records for basic VASP travel-rule fields, including geographic information above configured thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and compliance teams use this local checker to identify missing sender and beneficiary fields in on-chain or VASP transfer records. Treat its result as a basic completeness check, not identity verification or regulatory approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real KYC details passed through the command line may appear in shell history or process listings.

Mitigation: Use synthetic or redacted data for command-line checks; avoid putting real KYC details in --tx arguments.

Risk: A complete field check could be mistaken for identity verification or regulatory approval.

Mitigation: Treat results as basic field checks and verify identity and applicable requirements through qualified compliance processes.

Risk: The optional npx installer runs third-party code outside this review.

Mitigation: Verify the repository URL and third-party installer before using the optional installer.

## Reference(s):

- [LGD Ecosystem Hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD Theory](https://github.com/zhaoxinghua09-cell/LGD)
- [UIBC Protocol and Reference Implementation](https://github.com/zhaoxinghua09-cell/uibc-core)
- [Formal Paper](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [Structured JSON or human-readable terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes missing-field and completeness results; exit codes distinguish complete records (0), missing fields (1), and missing or invalid input (2).]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
