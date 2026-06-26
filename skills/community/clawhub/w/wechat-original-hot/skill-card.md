## Description: <br>
全网持续收录每日公众号原创热门文章内容，向用户推送公众号原创热门文章；当用户需要获取全领域的公众号原创热门文章、或订阅每日原创热门文章推送时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, WeChat account operators, content planners, and operations teams use this skill to find daily original viral WeChat Official Account articles by category or date, generate ranking reports, and subscribe to daily trend updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and makes network requests to redfox.hk. <br>
Mitigation: Configure REDFOX_API_KEY as an environment variable only, and confirm the key source, scope, validity period, and revocation process before use. <br>
Risk: Security evidence flags TLS verification and generated HTML field handling for review. <br>
Mitigation: Restore normal TLS verification and escape or validate generated HTML fields before routine use. <br>
Risk: Generated report artifacts may persist locally. <br>
Mitigation: Review and remove temporary JSON, HTML, or exported report files when they are no longer needed. <br>
Risk: The skill describes a daily subscription push flow whose implementation and revocation path need confirmation. <br>
Mitigation: Confirm how subscription push delivery is implemented and how users can revoke it before enabling routine subscriptions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/wechat-original-hot) <br>
- [Category mapping reference](references/category_mapping.md) <br>
- [RedFox article ranking API endpoint](https://redfox.hk/story/api/cozeSkill/getWxDataByCategoryAndTime) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, API Calls, Shell commands] <br>
**Output Format:** [Markdown article ranking tables with generated local HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; may create temporary JSON data and HTML or PDF-ready report artifacts.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
