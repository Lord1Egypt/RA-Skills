## Description:

Guide for using wjx-cli (Wenjuanxing CLI) to create AI homepages, posters, PPTs, and surveys, query responses, and analyze data. Use when the user mentions: AI主页, AI海报, AI PPT, 问卷, 调查, 收集, 表单, 投票, 考试, 测评, 满意度, NPS, 问卷星, wjx, survey, questionnaire, or wants to create or update those resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orzwq](https://clawhub.ai/user/orzwq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and survey operators use this skill to configure Wenjuanxing's CLI, create or update surveys and AI pages, retrieve responses, and analyze survey data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers account, administrator, contact, and organization management commands that can have broad or destructive effects.

Mitigation: Review the requested operation and its target before running management or response commands.

Risk: Installation guidance includes remote-script and sudo steps.

Mitigation: Independently verify installation instructions and scripts before using remote execution or elevated privileges.

Risk: One referenced section was only partially analyzed.

Mitigation: Review the relevant source section before relying on its guidance.

## Reference(s):

- [Survey logic and references](references/logic.md)
- [Question types](references/question-types.md)
- [Survey commands](references/survey-commands.md)
- [Response commands](references/response-commands.md)
- [Analytics commands](references/analytics-commands.md)
- [Contacts commands](references/contacts-commands.md)
- [Host routing](references/host-routing.md)
- [Node.js installation guidance](references/install-nodejs.md)
- [Formula helper](references/formula-helper.md)
- [ClawHub release](https://clawhub.ai/orzwq/skills/wjx-cli-use)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Survey content, Analysis]

**Output Format:** [Markdown guidance with shell commands, JSONL examples, and Wenjuanxing survey or response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the user's survey or AI page task; may include configuration steps, survey logic, response queries, or data analysis guidance.]

## Skill Version(s):

0.4.6 (source: SKILL.md frontmatter; ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
