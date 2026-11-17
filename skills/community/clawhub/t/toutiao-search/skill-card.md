## Description:

Searches recent Toutiao articles and videos by keyword, summarizes engagement, and exports results as CSV or an interactive HTML report; low-credit responses can initiate Alipay recharge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, analysts, and brand teams use this skill to find recent Toutiao posts, track popular topics, compare engagement, and export results for further analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may expose the API key through unsafe content.

Mitigation: Until credential handling and report rendering are corrected, use CSV-only mode; rotate keys exposed in existing reports.

Risk: The local report service lacks access controls.

Mitigation: Avoid using the local report service until authenticated proxy access is available.

Risk: A low-credit response can start payment setup without explicit approval.

Mitigation: Require explicit approval and verify payment details before enabling recharge.

Risk: Search terms are sent to RedFox and searches consume API credits.

Mitigation: Confirm the query is appropriate to share and check expected credit use before searching.

## Reference(s):

- [Skill release](https://clawhub.ai/redfox-data/skills/toutiao-search)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [Alipay recharge instructions](artifact/references/alipay-recharge.md)

## Skill Output:

**Output Type(s):** [Text, CSV, HTML]

**Output Format:** [Terminal results table, CSV file, and interactive HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes post titles, authors, engagement metrics, publication times, content type, and source links.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
