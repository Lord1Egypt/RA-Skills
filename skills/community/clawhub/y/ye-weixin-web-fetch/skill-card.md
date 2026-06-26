## Description: <br>
Fetches complete content from WeChat public account articles on mp.weixin.qq.com when default web fetching returns incomplete content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ranhuang](https://clawhub.ai/user/ranhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve public WeChat official account articles and convert extracted article content into Markdown for downstream reading or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fetcher can make outbound requests to any HTTP or HTTPS URL, broader than the stated WeChat-only purpose. <br>
Mitigation: Use only trusted WeChat article URLs, and prefer an updated version that enforces an mp.weixin.qq.com allowlist, validates redirected hosts, and blocks localhost, private IPs, and non-WeChat domains. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ranhuang/ye-weixin-web-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [JSON object containing article metadata and extracted Markdown content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May truncate extracted content at 50,000 characters and reports blocked or error states.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
