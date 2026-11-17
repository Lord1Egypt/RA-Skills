## Description:

《周易》智慧顾问可在用户提出周易、易经、起卦、占卜、卦象、八卦、六十四卦、变卦、互卦、爻辞、彖传、象传等相关请求时，提供铜钱、数字、时间三种起卦方式、六十四卦查询、多维度卦象解读、易经哲学分析、决策参考和交互式 HTML 可视化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Zhouyi or I Ching questions, perform coin, number, or time-based divination workflows, query hexagrams, discuss Yijing philosophy, and generate HTML reports for reflective decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include unescaped user-supplied question text.

Mitigation: Review generated reports before opening or sharing them, especially when the question text came from an untrusted source.

Risk: The report generator can write to custom output paths and may overwrite important files.

Mitigation: Use a dedicated report directory and avoid custom --output paths unless the destination has been reviewed.

Risk: Zhouyi interpretations may be mistaken for deterministic predictions or professional advice.

Mitigation: Use the skill only for explicit Zhouyi or I Ching requests and preserve its boundaries against medical, legal, financial, or final decision-making advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/zhouyi-advisor)
- [Divination Methods](references/divination-methods.md)
- [Ethics](references/ethics.md)
- [Yijing Philosophy](references/yijing-philosophy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Chinese-language conversational guidance, markdown summaries, shell command examples, and generated single-file HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected output is Chinese-language Zhouyi interpretation with optional local HTML report generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
