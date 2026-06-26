## Description: <br>
Use Weibo Open Platform for OAuth2 authentication, timeline retrieval, topic search, and structured social sentiment collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to run reproducible Weibo Open Platform API workflows for OAuth setup, timeline retrieval, topic search, endpoint debugging, and social signal collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The raw call command can send a Weibo access token to arbitrary URLs. <br>
Mitigation: Prefer named Weibo commands, avoid absolute URLs with call, and policy-block or patch the script so credentials are only sent to api.weibo.com. <br>
Risk: WEIBO_APP_SECRET and WEIBO_ACCESS_TOKEN are sensitive credentials. <br>
Mitigation: Keep secrets in a secret manager or controlled deployment environment and avoid committing them to source control. <br>
Risk: The optional Brave companion sends search queries to a separate provider and uses a separate API key. <br>
Mitigation: Enable the Brave companion only when users intentionally accept the additional provider dependency and credential boundary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oscraters/weibo) <br>
- [Publisher profile](https://clawhub.ai/user/oscraters) <br>
- [Weibo Open Platform](https://open.weibo.com/) <br>
- [Weibo API Guide](references/api_guide.md) <br>
- [Weibo API wiki](https://open.weibo.com/wiki/%E5%BE%AE%E5%8D%9AAPI) <br>
- [Weibo OAuth mechanism](https://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6) <br>
- [Weibo OAuth authorize endpoint](https://open.weibo.com/wiki/OAuth2/authorize) <br>
- [Weibo OAuth access token endpoint](https://open.weibo.com/wiki/OAuth2/access_token) <br>
- [Weibo OAuth token info endpoint](https://open.weibo.com/wiki/OAuth2/get_token_info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, python3, Weibo OAuth configuration, and a Weibo access token for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
