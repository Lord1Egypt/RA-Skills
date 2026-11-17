## Description:

WenDaoYun enterprise information lookup tool that uses the WenDaoYun API to query company basics, operations, finance, public opinion, and risk indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guojing1818](https://clawhub.ai/user/guojing1818)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query WenDaoYun for Chinese enterprise records, confirm the intended company, and retrieve business, legal, financial, public-opinion, and risk details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names and requested lookup categories are sent to the WenDaoYun external API.

Mitigation: Install only when that disclosure is acceptable for the intended use case and API account.

Risk: The skill requires a WenDaoYun API key for requests.

Mitigation: Keep WENDAOYUN_API_KEY private, store it only in the expected configuration, and revoke it promptly if exposed.

Risk: Ambiguous company names can return many possible matches.

Mitigation: Show a limited result list and wait for the user to confirm the exact enterprise before requesting detailed records.

## Reference(s):

- [WenDaoYun Open Platform](https://open.wintaocloud.com/home)
- [WenDaoYun API Invoke Base URL](https://h5.wintaocloud.com/prod-api/api/invoke)
- [WenDaoYun fuzzy-search-org example](https://h5.wintaocloud.com/prod-api/api/invoke/fuzzy-search-org?searchKey=XXX&pageNum=1&pageSize=5)
- [ClawHub skill page](https://clawhub.ai/guojing1818/skills/wentao-org-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown or plain text summaries of WenDaoYun API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied WENDAOYUN_API_KEY and sends company lookup terms to WenDaoYun.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
