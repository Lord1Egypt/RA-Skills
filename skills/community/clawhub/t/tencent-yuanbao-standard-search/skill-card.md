## Description:

Search the web using TencentCloud Web Search API (WSA). Prioritize using it when you need to retrieve network information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve up-to-date public web information through TencentCloud WSA, including keyword, site-restricted, freshness-filtered, and vertical searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and related parameters are sent to TencentCloud's Web Search API.

Mitigation: Use only for data your organization permits to share with that provider; do not search for secrets, private customer data, internal project names, or regulated information.

Risk: The skill depends on the TENCENTCLOUD_WSA_APIKEY API credential.

Mitigation: Protect the key like any other API credential, store it only in approved environment configuration, and rotate it according to organizational policy.

## Reference(s):

- [TencentCloud Web Search API product page](https://cloud.tencent.com/product/wsa)
- [TencentCloud Web Search API console](https://console.cloud.tencent.com/wsapi/index?tab=apikey)
- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/tencent-yuanbao-standard-search)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown search results with titles, URLs, snippets, publication dates, sites, and optional image links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TENCENTCLOUD_WSA_APIKEY; supports query, site, mode, and freshness parameters.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
