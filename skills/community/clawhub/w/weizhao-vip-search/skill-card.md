## Description: <br>
在唯品会(VIP.com)搜索商品，引导用户登录并调用搜索API获取关键字商品。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miketobusy](https://clawhub.ai/user/miketobusy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent to search VIP.com for products by keyword, using a user-supplied logged-in session cookie when VIP.com requires authenticated access. The skill guides cookie collection, runs a packaged Python search script, and formats returned product data for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a full logged-in VIP.com browser cookie. <br>
Mitigation: Use a temporary account or session where possible, avoid pasting a main-account cookie into chat or shell history, and log out afterward to invalidate the session. <br>
Risk: The packaged script passes the cookie to a VIP.com request and the upstream API may change over time. <br>
Mitigation: Run only the packaged script, avoid printing the cookie in results, and review failures or response-shape changes before relying on extracted product data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miketobusy/weizhao-vip-search) <br>
- [Publisher profile](https://clawhub.ai/user/miketobusy) <br>
- [VIP.com](https://www.vip.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or Markdown search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a search keyword and a user-provided VIP.com logged-in session cookie.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
