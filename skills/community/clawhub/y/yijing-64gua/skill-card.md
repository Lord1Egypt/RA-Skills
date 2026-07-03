## Description: <br>
Yijing Upload helps agents perform I Ching hexagram lookup and interpretation from six-line numeric inputs, including classical text presentation, Zhu Xi and Nan Huaijin style readings, daily guidance, and simple statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuzijun-nm](https://clawhub.ai/user/qiuzijun-nm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to decode I Ching six-line numeric inputs, retrieve bundled hexagram texts, and generate cultural or entertainment-oriented readings and practical advice. It should not be treated as medical, legal, financial, safety, or other professional guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may record a user's question and reading result in a local log. <br>
Mitigation: Avoid entering sensitive personal details, and review or clear the local reading log according to the deployment's retention expectations. <br>
Risk: I Ching readings and daily advice can be mistaken for professional guidance. <br>
Mitigation: Present outputs as cultural or entertainment-oriented interpretation, not as medical, legal, financial, safety, or other professional advice. <br>


## Reference(s): <br>
- [Yijing Upload on ClawHub](https://clawhub.ai/qiuzijun-nm/skills/yijing-64gua) <br>
- [4096 hexagram lookup and interpretation table](references/yijing-4096.csv) <br>
- [64 hexagram classical text table](references/yijing-full.csv) <br>
- [2026 lunar calendar reference](references/yijing-2026-calendar.csv) <br>
- [Reading statistics data](references/yijing-stats.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with explanatory sections and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled CSV and JSON reference data and may update a local reading log or statistics file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
