## Description: <br>
唯品会专属 AI 购物助手“小v”。当用户提及购物、穿搭建议、时尚趋势或特定商品搜索时，小v 会动态调用内部子技能提供商品推荐、详情查询及促销活动。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bfkkkd](https://clawhub.ai/user/bfkkkd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this agent to search Vipshop products, review product details, browse promotions, and receive shopping recommendations. The skill can initiate Vipshop QR-code login and authenticated shopping API calls before returning formatted results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request global installation or use of `vipshop-cli`, which may affect the user's local environment. <br>
Mitigation: Require explicit user confirmation before installing or updating the CLI, and verify the intended package and version before execution. <br>
Risk: The skill can initiate Vipshop account login, share QR-code login materials, poll login status, and rely on saved session state. <br>
Mitigation: Require explicit user confirmation before login, QR sharing, polling, token use, or logout, and confirm login status through `vipshop status` or `vipshop login --poll` rather than assuming success. <br>
Risk: Authenticated shopping API calls may expose account context or influence purchasing workflows. <br>
Mitigation: Limit execution to user-requested shopping tasks, present results for review, and require explicit confirmation before any action beyond search, detail lookup, promotion browsing, login, or logout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bfkkkd/xc-xiaov) <br>
- [Publisher profile](https://clawhub.ai/user/bfkkkd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown or plain text summaries derived from JSON CLI output, with shell commands used to check login state and query Vipshop services.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product tables, detail summaries, promotion lists, QR-code login links or local image paths, and follow-up guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
