## Description:

使用华为云AI联网增强API进行网页内容检索，获取实时网络信息

This skill is ready for commercial/non-commercial use.

## Publisher:

[flp516](https://clawhub.ai/user/flp516)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run live web searches through Huawei Cloud AI Networking when current web information, news, or Chinese-optimized search results are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a live Huawei Cloud token, and the artifact instructs users to place it directly in the JavaScript source file.

Mitigation: Use a dedicated, least-privileged token and store it in an environment variable or local secret file excluded from version control.

Risk: Server security evidence reports an unnecessary npm fs dependency and recommends review before production use.

Mitigation: Remove the npm fs dependency and pin reviewed dependency versions before production deployment.

Risk: Search results are live web content and may include incomplete, stale, or unsafe information.

Mitigation: Validate important results against authoritative sources before relying on them or presenting them to end users.

## Reference(s):

- [Huawei AI Networking service activation guide](https://developer.huawei.com/consumer/cn/doc/AppGallery-connect-Guides/agc-ainetworking-serviceopen-0000002370503878)
- [Huawei Cloud AI Networking webSearch endpoint](https://connect-api.cloud.huawei.com/api/aiNetworking/v1/webSearch)
- [ClawHub skill page](https://clawhub.ai/flp516/skills/xiaoyi-web-search-v2)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text search results with titles, URLs, snippets, and source names; the Node.js API returns an array.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Huawei Cloud AI Networking token and accepts a query plus optional result count.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
