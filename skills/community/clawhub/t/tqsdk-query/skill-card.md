## Description:

TqSdk Query retrieves real-time quotes, current K-line series, and historical K-line data for Chinese futures and options through TqSdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaingush](https://clawhub.ai/user/gaingush)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query TqSdk market data for contract symbols, including live quotes, recent K-line summaries, and bounded historical K-line records. It requires TQ_USERNAME and TQ_PASSWORD environment variables for account authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TqSdk account credentials are required and must remain confidential.

Mitigation: Provide TQ_USERNAME and TQ_PASSWORD only through isolated runtime environment variables that are accessible to this skill.

Risk: Dependencies are declared without a lockfile, which can change installed package versions over time.

Mitigation: Pin and review tqsdk and pandas versions before deployment in production environments.

## Reference(s):

- [TqSdk homepage](https://www.shinnytech.com/tqsdk/)
- [ClawHub skill page](https://clawhub.ai/gaingush/skills/tqsdk-query)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Text summary with JSON result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on valid TqSdk credentials, contract symbols, account entitlements, and market-data availability.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
