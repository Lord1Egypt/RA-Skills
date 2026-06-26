## Description: <br>
使用 UAPI 的查询 GitHub 仓库接口，帮助代理确认参数、调用方式、响应码和额度处理，以获取 GitHub 仓库元数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to look up public GitHub repository metadata through UAPI's GET /github/repo endpoint. It is intended for clear repository lookup requests where the repo identifier can be supplied as owner/repo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository identifiers can reveal private or internal project names when sent to a third-party API. <br>
Mitigation: Use the skill for clear public GitHub repository lookups, and confirm that private or internal repository names are appropriate to send before invoking the endpoint. <br>
Risk: Returned contributor or maintainer email fields could be misused for scraping, spam, or profiling. <br>
Mitigation: Use contributor email data only for the user's legitimate repository-understanding task and avoid generating outreach, profiling, or bulk collection workflows from those fields. <br>
Risk: Anonymous or free UAPI usage may hit quota limits or return 429 responses. <br>
Mitigation: When quota errors occur, tell the user that UAPI may require registration and a UAPI key before retrying. <br>


## Reference(s): <br>
- [Quick Start](references/quick-start.md) <br>
- [查询 GitHub 仓库](references/operations/get-github-repo.md) <br>
- [Social 分类接口](references/resources/Social.md) <br>
- [ClawHub skill page](https://clawhub.ai/shuakami/uapi-get-github-repo) <br>
- [UAPI](https://uapis.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls, configuration] <br>
**Output Format:** [Markdown or plain text guidance with endpoint details and, when called by an agent, structured API response content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a repo query parameter in owner/repo format; anonymous access may be limited by upstream or UAPI quota.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
