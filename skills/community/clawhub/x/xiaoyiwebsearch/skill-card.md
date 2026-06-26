## Description: <br>
使用华为云AI联网搜索API进行网页内容检索，获取实时网络信息. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flp516](https://clawhub.ai/user/flp516) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Chinese-oriented live web searches through Huawei Cloud AI Networking Search and return concise search results for current information, news, and reference lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships an embedded Huawei Cloud API token. <br>
Mitigation: Install only after confirming the publisher has removed and rotated the embedded token and requires user-supplied credentials. <br>
Risk: Search queries are sent to Huawei Cloud. <br>
Mitigation: Do not use the skill for secrets, personal data, internal company terms, or confidential research. <br>
Risk: Dependency metadata includes less safe pinned HTTP package sources. <br>
Mitigation: Regenerate dependency metadata with trusted HTTPS package sources before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/flp516/xiaoyiwebsearch) <br>
- [Huawei Cloud AI Networking Search endpoint](https://connect-api.cloud.huawei.com/api/aiNetworking/v1/webSearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code] <br>
**Output Format:** [Console text output and JavaScript API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a search query and optional result count; the executable caps requests at 20 results.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
