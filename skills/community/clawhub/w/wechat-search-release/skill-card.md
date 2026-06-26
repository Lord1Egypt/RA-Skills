## Description: <br>
Search WeChat Official Account articles using OpenClaw's web search and fetch capabilities with compliance-focused design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jixsonwang](https://clawhub.ai/user/jixsonwang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to find public WeChat Official Account articles through OpenClaw web search and fetch tools. It returns article-oriented search results such as titles, snippets, account names, and URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to configured OpenClaw web search/fetch providers and public search endpoints. <br>
Mitigation: Do not submit secrets, internal project names, regulated data, or other sensitive terms in queries. <br>
Risk: Python dependencies and command execution are required when running the helper manually. <br>
Mitigation: Run in an isolated environment with pinned dependencies and review the helper before deployment. <br>
Risk: Some documented behavior, including robots.txt handling, rate limiting, date filters, and JSON or markdown output, is not fully proven by the artifact implementation. <br>
Mitigation: Verify those behaviors in the target OpenClaw tooling before relying on them for production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jixsonwang/wechat-search-release) <br>
- [README](README.md) <br>
- [Weixin Sogou search endpoint](https://weixin.sogou.com/weixin?type=2&query={query}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text search results; artifact documentation also describes JSON and markdown output options that should be verified before relying on them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to up to five results and supports a configurable maximum of 20 results in the bundled Python helper.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
