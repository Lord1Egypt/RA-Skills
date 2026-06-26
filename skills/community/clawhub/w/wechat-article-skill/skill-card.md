## Description: <br>
Fetches public WeChat article pages from mp.weixin.qq.com/s/ links and extracts the article body as plain text for an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlienHub](https://clawhub.ai/user/AlienHub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill when an agent needs to retrieve readable text from public WeChat public-account article links. The skill is intended for mp.weixin.qq.com/s/ URLs and provides browser fallback guidance when scripted fetching fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves external WeChat article pages, which can expose private or unintended URLs if used broadly. <br>
Mitigation: Keep use limited to mp.weixin.qq.com/s/ links and avoid submitting sensitive or private URLs. <br>
Risk: Article fetching may fail because WeChat pages can require login, expire, restrict access, or reject non-browser requests. <br>
Mitigation: Use the scripted fetch first, inspect stderr on failure, and only use browser fallback when the skill explicitly recommends it. <br>
Risk: The helper performs network retrieval from a user-provided URL. <br>
Mitigation: Add URL validation or runtime allowlisting before broader deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AlienHub/wechat-article-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text article content with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper writes extracted article text to stdout and failure reasons or fallback guidance to stderr.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
