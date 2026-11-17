## Description:

帮助代理通过 umeng-cli 调用友盟 OpenAPI，为小程序、H5 和小游戏创建推广链接，并查询推广活动或渠道清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Umeng mini program campaign links from an agent session, including creating a campaign link after confirmation and listing existing campaign or channel records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable or unsafe CLI installation methods could install unreviewed code.

Mitigation: Use a trusted, pinned umeng-cli version and avoid the curl-to-shell installer.

Risk: The skill requests telemetry that can include an application AppKey.

Mitigation: Do not allow AppKey telemetry unless sharing application identifiers through the CLI is acceptable.

Risk: createCampaign creates irreversible campaign links in the user's account.

Mitigation: Manually confirm every createCampaign request and do not automatically retry failed writes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/squall0925/skills/uapp-campaign)
- [umeng-cli Project](https://github.com/umeng/umeng-cli)
- [Umeng OpenAPI Gateway](https://gateway.open.umeng.com/openapi)
- [Umeng Web Console](https://web.umeng.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Umeng OpenAPI response JSON; campaign creation guidance requires explicit user confirmation before execution.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
