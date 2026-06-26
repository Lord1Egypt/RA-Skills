## Description: <br>
连接时间之河（timehe.com）时间胶囊平台，帮助用户创建时间胶囊、每日写作、查看胶囊、管理团队胶囊和使用扫码写信亭。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yigenyecao-afk](https://clawhub.ai/user/yigenyecao-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to connect an agent to Timehe's time-capsule service, create and review personal or team capsules, answer daily writing prompts, and guide emotional writing workflows for future recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle personal messages, recipient details, and future unlock dates that users expect to remain private. <br>
Mitigation: Treat capsule content and recipient metadata as sensitive; confirm recipient, unlock date, and message content before create or submit actions. <br>
Risk: Authenticated operations require a Timehe access token. <br>
Mitigation: Provide only a Timehe-specific token through a secure environment variable, and do not paste tokens into chat or screenshots. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yigenyecao-afk/timehe) <br>
- [Timehe Website](https://www.timehe.com) <br>
- [Timehe API Base](https://www.timehe.com/api) <br>
- [Timehe Booth](https://www.timehe.com/booth) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Configuration] <br>
**Output Format:** [Markdown with JSON examples and API request descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated capsule operations require a TIMEHE_TOKEN; some team contribution and article-reading flows are described as public.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
