## Description:

SBTI 恶搞人格测试数据包提供 20 道中文玩梗题目、5 种人格结果和 15 个评分维度，供代理帮助用户集成或改造自定义前端测试体验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a static Chinese-language parody personality-test data pack for building quiz interfaces, scoring flows, and customized entertainment experiences. It should be presented as humor rather than a professional or psychological assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the parody quiz for a serious psychological assessment.

Mitigation: Present the quiz as entertainment only and avoid using results for employment, medical, psychological, or other consequential decisions.

Risk: The Chinese-language parody content includes coarse, insulting humor and profanity.

Mitigation: Disclose the tone before use and add content warnings or moderation when exposing it in public-facing interfaces.

Risk: A frontend built from the data could save quiz progress or answers.

Mitigation: Disclose any saved progress, keep data local by default, and require user consent before sharing or uploading answers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijinhongucl-pixel/skills/sbti-personality-test)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [questions.json](artifact/data/questions.json)
- [results.json](artifact/data/results.json)
- [dimensions.json](artifact/data/dimensions.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with JSON and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static JSON quiz content; no executable payload, network behavior, credential handling, or hidden persistence reported by security evidence.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
