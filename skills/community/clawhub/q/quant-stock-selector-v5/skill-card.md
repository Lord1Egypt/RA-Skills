## Description:

This skill helps agents run a three-layer quantitative A-share stock screening workflow that filters candidates, scores value, quality, and momentum factors, and returns an industry-balanced shortlist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to screen A-share stocks with a documented quantitative process and generate an informational ranked shortlist. It is not financial advice and should be reviewed before use in any investment workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports embedded JQData credentials.

Mitigation: Remove the embedded credentials, rotate them with the data provider, and require users to provide credentials through an external secret or environment configuration.

Risk: The security evidence reports that the documented screening method does not closely match the code for a finance workflow.

Mitigation: Review the implemented filters against the documentation before deployment and treat generated stock lists as informational only.

Risk: The artifact relies on live third-party market-data packages and a fixed JQData date noted in the documentation.

Mitigation: Test in an isolated environment with pinned dependencies and verify data-source availability and freshness before using the results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/quant-stock-selector-v5)
- [Original Zhihu strategy article](https://zhuanlan.zhihu.com/p/1996940902648796995)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text console output with ranked stock-screening results and brief guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are informational and depend on JQData and AKShare availability and data freshness.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
