## Description:

模拟顶级名医临证逻辑，智能问诊、八纲辨证、九种体质匹配，动态生成方药、君臣佐使解析、典籍出处及历代医案参考，新增多证型、细化舌脉判断，全程合规科普，不替代诊疗。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuhuaikuan](https://clawhub.ai/user/zhuhuaikuan)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-speaking users and agents use this skill as educational Traditional Chinese Medicine reference material for structured symptom intake, pattern differentiation, constitution matching, classical context, and safety-oriented care guidance. It should not be used for diagnosis, treatment decisions, or unsupervised prescription-like recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce medical-style diagnosis and prescription output, including herb names, dosages, pediatric guidance, pregnancy guidance, and contraindications.

Mitigation: Use it only as educational TCM reference material and require review by a licensed clinician before any diagnosis, treatment, herb, dosage, pediatric, pregnancy, or contraindication decision.

Risk: Symptom intake workflows may encourage users to share personal health details that are not necessary for an educational reference interaction.

Mitigation: Ask users to avoid unnecessary personal health details and keep prompts limited to non-identifying information needed for general educational context.

Risk: The artifact has limited safeguards before prescription-like output.

Mitigation: Add explicit opt-in, scope limits, language handling, and safety gates before producing formula-style or contraindication content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuhuaikuan/skills/tcm-famous-doctor)
- [Source skill definition](artifact/SKILL.md)
- [Source helper script](artifact/scripts/tcm.py)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown-style Chinese text with optional shell command invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include symptom intake notes, TCM pattern differentiation, constitution assessment, formula-style herb lists with dosages, classical references, contraindication notes, and safety reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
