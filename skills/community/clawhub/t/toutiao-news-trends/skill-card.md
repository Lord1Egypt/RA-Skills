## Description:

Fetches Toutiao trending news with titles, popularity scores, cleaned links, cover images when available, labels, aggregation IDs, and category tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to retrieve current Toutiao hot-board items for Chinese news trend monitoring and lightweight research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Toutiao to fetch public trend data, and heavy or abnormal remote responses could increase process memory use.

Mitigation: Install only when outbound access to Toutiao is acceptable, keep the configured item limit bounded, and add response-size limits before high-volume or unattended use.

Risk: The Toutiao web hot-board response structure may change, causing missing fields or command failures.

Mitigation: Review returned JSON before downstream use and update field parsing when Toutiao changes its public response shape.

## Reference(s):

- [Toutiao News Trends on ClawHub](https://clawhub.ai/wuchubuzai2018/skills/toutiao-news-trends)
- [Toutiao hot-board endpoint](https://www.toutiao.com/hot-event/hot-board/)

## Skill Output:

**Output Type(s):** [text, code, shell commands]

**Output Format:** [JSON emitted by a Node.js command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 200 ranked trend items; each item may include rank, title, popularity, link, cover, label, clusterId, and categories.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
