## Description:

Sano Intel is a Probe Capital healthcare intelligence skill for querying Chinese healthcare and biotech companies, financing events, patents, clinical trials, sector trends, and A/HK/US market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanjj-cmd](https://clawhub.ai/user/yanjj-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, investors, and developers use this skill to ask Chinese-language questions about China's healthcare industry and receive concise summaries from company, financing, patent, clinical trial, sector, market, and daily digest queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens and user query contents are sent to the Sano Intel service over plaintext HTTP.

Mitigation: Use only non-sensitive queries and short-lived tokens until an HTTPS endpoint with valid certificate verification is available; avoid storing long-lived tokens in shell startup files.

## Reference(s):

- [Sano Intel skill release](https://clawhub.ai/yanjj-cmd/skills/sano-intel)
- [Sano API token request](https://ffmp60ytnq.feishu.cn/share/base/shrcniDTJZknKba0LUeaF5BBuJg)
- [Sano Intel API base](http://47.102.196.1:8081)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise Chinese summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SANO_TOKEN for authenticated API requests and summarizes returned healthcare intelligence for the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
