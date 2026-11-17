## Description:

水滴筹众筹助手帮助用户浏览公开医疗众筹项目并生成捐款链接，也可在用户明确同意后提交手机号以便水滴筹顾问回访。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiwenbing](https://clawhub.ai/user/jiwenbing)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find Shuidichou medical crowdfunding projects for donation or to request fundraising assistance. For fundraising assistance, the skill asks for explicit consent before submitting a phone number for a Shuidichou advisor callback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may submit a phone number to Shuidichou while requesting fundraising help.

Mitigation: Ask for explicit consent, explain that the phone number is used for a Shuidichou advisor callback, and offer the official hotline before running registration.

Risk: Donation actions depend on external Shuidichou pages and changing crowdfunding project data.

Mitigation: Have users review donation links in the browser before paying and avoid representing projects as independently verified beyond the Shuidichou process described by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiwenbing/skills/shuidichou)
- [Shuidichou website](https://www.shuidichou.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with donation links and optional shell command execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language user-facing responses; may include external Shuidichou links and JSON-derived project summaries.]

## Skill Version(s):

2.1.1 (source: server-resolved release metadata; artifact frontmatter says 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
