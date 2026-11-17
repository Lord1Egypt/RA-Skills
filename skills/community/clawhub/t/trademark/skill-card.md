## Description:

商标关键词搜索与详情查询（申请人、分类、公告等）。当用户说：查一下「某某」商标有没有被注册？这个商标注册人是谁？或类似商标问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Chinese trademark information by keyword, applicant, registration number, or class, then retrieve details such as registrant, status, announcement dates, and goods or services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trademark keywords, registration numbers, class IDs, and the JisuAPI AppKey are sent to JisuAPI.

Mitigation: Use a dedicated key with quota or billing limits, avoid confidential pre-launch brand searches unless approved, and rotate the key if request URLs may have been logged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/trademark)
- [JisuAPI trademark API documentation](https://www.jisuapi.com/api/trademark/)
- [JisuAPI](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON API results, usually summarized by the agent as concise text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends user-supplied trademark queries to JisuAPI.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
