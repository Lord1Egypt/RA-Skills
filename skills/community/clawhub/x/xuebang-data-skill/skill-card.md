## Description: <br>
查看学邦数据。用于登录学邦后台并读取首页今日经营数据与待办数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuanSir123](https://clawhub.ai/user/chuanSir123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or operators with authorized Xuebang EDU.BOSS access use this skill to sign in, read today's business metrics and pending items, and receive a concise operational summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Xuebang backend username and password and saves them in a workspace note by default. <br>
Mitigation: Use a least-privilege account, tell the skill not to save the password when appropriate, and remove credentials from `workspace/TOOLS.md` after use. <br>
Risk: The skill reads business operating metrics and pending-work data from an authenticated backend session. <br>
Mitigation: Run it only for authorized users and review the generated summary before sharing it outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chuanSir123/xuebang-data-skill) <br>
- [Publisher profile](https://clawhub.ai/user/chuanSir123) <br>
- [Xuebang EDU.BOSS login](https://boss.xuebangsoft.net/eduboss/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Missing metrics are marked as not read, and passwords should not be repeated in output.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
