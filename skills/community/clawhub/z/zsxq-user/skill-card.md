## Description: <br>
知识星球用户信息与反馈：查看当前登录用户的个人资料、查询跨星球的最近发主题足迹、提交 NPS 反馈（推荐分数 + 建议）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsxq](https://clawhub.ai/user/zsxq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents supporting Knowledge Planet users use this skill to inspect the current logged-in account, retrieve recent cross-group posting footprints, and prepare or submit user-confirmed NPS feedback to Knowledge Planet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's logged-in zsxq-cli session and may surface private profile or posting-footprint data. <br>
Mitigation: Install and run it only for accounts where the agent is allowed to access that data, and treat profile JSON and footprint results as private. <br>
Risk: The NPS shortcut submits a score and written suggestion to Knowledge Planet as an external write action. <br>
Mitigation: Review the score and suggestion text with the user before execution, keep suggestions within the documented limit, and submit only after explicit confirmation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zsxq/zsxq-user) <br>
- [user +info reference](references/zsxq-user-info.md) <br>
- [user +footprints reference](references/zsxq-user-footprints.md) <br>
- [user +nps reference](references/zsxq-user-nps.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI results may be JSON, tables, or short status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated zsxq-cli session; NPS feedback submission should be confirmed by the user before execution.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
