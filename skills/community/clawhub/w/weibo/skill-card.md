## Description:

Use Weibo Open Platform for OAuth2 authentication, timeline retrieval, topic search, and structured social sentiment collection through the official Weibo API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure Weibo credentials, perform OAuth2 token workflows, retrieve timelines, query topics, and collect social signals through Weibo's official API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can send Weibo secrets to non-Weibo URLs through configurable endpoint overrides or generic absolute URL calls.

Mitigation: Review before installing, use only trusted configuration, avoid WEIBO_REST_BASE or WEIBO_OAUTH_BASE overrides with real credentials, and do not allow untrusted prompts to invoke call with absolute URLs.

Risk: WEIBO_ACCESS_TOKEN may be attached automatically to generic requests.

Mitigation: Prefer a patched version that rejects non-Weibo hosts and does not automatically attach WEIBO_ACCESS_TOKEN to generic requests.

Risk: Sensitive values can be supplied through environment paths that may not have the same audit visibility as the declared primary credential path.

Mitigation: Use managed secret references for WEIBO_APP_SECRET where available, and keep WEIBO_ACCESS_TOKEN or other sensitive values in a trusted external secret manager or controlled deployment environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oscraters/skills/weibo)
- [Weibo Open Platform](https://open.weibo.com/)
- [Weibo Open Platform API Guide](references/api_guide.md)
- [Weibo API Wiki](https://open.weibo.com/wiki/%E5%BE%AE%E5%8D%9AAPI)
- [Weibo OAuth Mechanism](https://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6)
- [Weibo OAuth2 Authorize](https://open.weibo.com/wiki/OAuth2/authorize)
- [Weibo OAuth2 Access Token](https://open.weibo.com/wiki/OAuth2/access_token)
- [Weibo OAuth2 Token Info](https://open.weibo.com/wiki/OAuth2/get_token_info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Weibo Open Platform credentials; the optional Brave Search companion uses a separate credential and provider dependency.]

## Skill Version(s):

1.0.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
