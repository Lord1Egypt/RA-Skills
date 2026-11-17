## Description:

分院帽人格测试（随机抽卷 + 麻瓜词典）。当用户说「给我分院」「我是哪个学院」「测测我适合哪个学院」「戴帽子」「霍格沃茨分院」时使用，用户抱怨「手打答案串太累/怕把题目搞混」时也直接走这里。首选生成单文件点选答题页：一屏一题、随机抽卷、点选即记住、答完点「提交判定」出卡；纯文本通道走三轮闭环，一屏出题 + 卷号 + 答案串回传。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dora233](https://clawhub.ai/user/dora233)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language skill to run a local sorting-style personality quiz, either through a generated single-file HTML page or a three-round text interaction. The skill produces quiz questions, parses answer strings, handles close-score follow-up choices, and returns a shareable result card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML from untrusted custom configuration files may carry an HTML/script escaping risk.

Mitigation: Use the bundled data or custom configuration files you control, and do not generate or share HTML from untrusted configs until the escaping issue is fixed.

Risk: The alternate configuration is not fully de-IPed for commercial use.

Mitigation: For commercial use, replace remaining original-work settings and text before release, then rerun the skill's audit and verification commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dora233/skills/sk-8bec7ec2fe24)
- [Book Canon Reference](references/canon.md)
- [Regression Prompts and Expected Results](references/test-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown/plain text with inline shell commands and optional generated single-file HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON configuration and Python scripts; generated result cards include quiz paper numbers for reproducibility.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
