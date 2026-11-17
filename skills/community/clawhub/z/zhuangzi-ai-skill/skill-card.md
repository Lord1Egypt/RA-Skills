## Description:

莊子哲學與《莊子》文本的三語對談與 JSON 知識整理 skill。用於產生繁體中文、簡體中文及英文並列的莊子對談，分析生平、內篇／外篇／雜篇、核心概念與寓言，並將對談或知識內容整理為可匯入系統的結構化 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Zhuangzi-inspired philosophical dialogue, trilingual knowledge records, import-ready JSON, test cases, and evaluation guidance while preserving source boundaries and safety limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional dynamic evaluator can send candidate responses to an OpenAI-compatible service.

Mitigation: Run dynamic evaluation only with data approved for that service; use static evaluation or local review for sensitive content.

Risk: The evaluator's dependency guidance includes a privileged package installation recommendation.

Mitigation: Install dependencies in a virtual environment or through a pinned dependency workflow instead of using privileged global installation.

Risk: Philosophical responses about grief, self-harm, medical care, or crisis situations could be mistaken for professional help.

Mitigation: Keep the skill's safety boundary: Zhuangzi-style reflection is supplemental and must not replace emergency, medical, mental health, legal, or financial support.

Risk: Creative imitation can be confused with source text from the Zhuangzi.

Mitigation: Label modern parables, paraphrases, and stylistic imitations clearly and avoid presenting them as original classical text.

## Reference(s):

- [Skill Definition](SKILL.md)
- [Zhuangzi Knowledge Base](references/zhuangzi_knowledge.json)
- [Zhuangzi AI Test Cases](references/zhuangzi_ai_test_cases.md)
- [Dynamic Smoke Report](references/dazongshi_dynamic_smoke_report.md)
- [Dazongshi Evaluation Report](references/dazongshi_evaluation_report.md)
- [Qiushui Evaluation Report](references/qiushui_evaluation_report.md)
- [Renjianshi Evaluation Report](references/renjianshi_evaluation_report.md)
- [Stanford Encyclopedia of Philosophy: Zhuangzi](https://plato.stanford.edu/entries/zhuangzi/)
- [Chinese Text Project: Zhuangzi](https://ctext.org/zhuangzi)
- [Internet Encyclopedia of Philosophy: Zhuangzi](https://iep.utm.edu/zhuangzi-chuang-tzu-chinese-philosopher/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Traditional Chinese, Simplified Chinese, and English fields; generated creative material should be labeled as imitation rather than original text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
