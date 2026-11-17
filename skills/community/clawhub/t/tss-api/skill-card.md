## Description:

tss-api provides Compass TSS API reference guidance for querying cross-chain transaction heights, pending transactions, orders, transaction hashes, and status records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbtsm](https://clawhub.ai/user/lbtsm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill as an API reference for inspecting Compass TSS cross-chain transaction records, pending transactions, block-height scans, order IDs, transaction hashes, and status codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries can expose sensitive or non-public order IDs or transaction hashes to the Compass TSS API endpoint.

Mitigation: Use only identifiers intended to be shared with that endpoint and avoid sending confidential transaction data.

Risk: The API reference is primarily in Chinese, which may cause localization or interpretation errors for non-Chinese readers.

Mitigation: Have bilingual reviewers confirm endpoint parameters and status semantics before operational use.

## Reference(s):

- [ClawHub tss-api skill page](https://clawhub.ai/lbtsm/skills/tss-api)
- [Compass TSS API base endpoint](https://tss-api.chainservice.io)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown API reference with JSON response examples and bash curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST endpoint paths, query parameters, response examples, status codes, and curl commands.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
