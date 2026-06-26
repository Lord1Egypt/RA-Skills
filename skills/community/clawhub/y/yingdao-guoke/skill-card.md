## Description: <br>
YingDao-GuoKe helps users bind a Yingdao RPA community profile and retrieve profile, achievement, balance, and development activity statistics. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[guoke416](https://clawhub.ai/user/guoke416) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Yingdao RPA community users use this skill to bind their community profile URL and ask an agent to return account details, achievement status, balances, and development statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Yingdao UUID and personalId locally. <br>
Mitigation: Install only if local storage of these identifiers is acceptable; remove the binding by deleting data/user.json. <br>
Risk: The skill sends the stored Yingdao identifiers to Yingdao APIs to retrieve profile and development statistics. <br>
Mitigation: Provide only the Yingdao community profile link or identifier; do not provide passwords, API keys, or other secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guoke416/yingdao-guoke) <br>
- [Yingdao community home page](https://www.yingdao.com/community/homePage) <br>
- [Yingdao community profile example](https://www.yingdao.com/community/userCenter?userUuid=687223449269694466) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown-style Chinese text responses with account statistics and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores the user's Yingdao UUID and derived personalId in local data/user.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
