## Description: <br>
用户给出选题，小龙虾爬取信息、整理成一篇深度有创新的文章，展示给用户确认后一键发布到知乎。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to research a topic, draft a Zhihu article, review it, and publish it to a logged-in Zhihu account after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content to a user's Zhihu account. <br>
Mitigation: Require explicit user confirmation before publishing and review the generated article before replying with the publish command. <br>
Risk: Browser Relay could operate on the wrong Zhihu tab if attached broadly. <br>
Mitigation: Attach Browser Relay only to the intended, already-open Zhihu editor tab before running the browser publishing script. <br>
Risk: A broad or long-lived Zhihu access token could expose account publishing capability in shared environments. <br>
Mitigation: Use the narrowest practical token scope and avoid leaving ZHIHU_ACCESS_TOKEN configured in shared or persistent shells. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kelcey2023/zeelin-zhihu-autopost) <br>
- [Zhihu developer portal](https://dev.zhihu.com/) <br>
- [Zhihu article API endpoint](https://api.zhihu.com/v4/articles) <br>
- [OpenClaw Browser Relay documentation](https://learnclawdbot.org/docs/tools/chrome-extension) <br>
- [Referenced ClawHub Zhihu posting skill](https://clawhub.ai/InuyashaYang/zhihu-post) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown article draft, shell command guidance, and publication status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a reviewed article body to a temporary Markdown file before invoking the publishing script.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
