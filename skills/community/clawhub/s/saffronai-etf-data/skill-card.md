## Description:

Fetches Indian ETF tracker data from SaffronAI's public endpoint and returns full snapshots or symbol-filtered rows as JSON or CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subscriptionmanager26-png](https://clawhub.ai/user/subscriptionmanager26-png)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve last price, iNAV, timestamp, and related tracker fields for Indian ETF symbols or full SaffronAI ETF tracker snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes a network read to SaffronAI's public ETF endpoint through its bundled Python helper and depends on curl being available.

Mitigation: Run it only in environments where outbound access to the endpoint is acceptable, review network permissions before deployment, and ensure curl is installed.

## Reference(s):

- [SaffronAI ETF Data Endpoint](https://www.saffronai.in/api/etf-data)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; helper output is JSON or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filtered symbol lookups preserve requested symbol order when matches are returned.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
