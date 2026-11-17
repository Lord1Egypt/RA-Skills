## Description:

为中小学生识别并修正常见中文病句，并在学生同意后追踪反复出现的语病。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT

## Use Case:

中小学生可用它分析和修改中文病句，并在同意后追踪反复出现的语病。小学高段学生须有家长或老师陪同。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because one local reference could not be resolved.

Mitigation: Review the unresolved reference and repeat the scan before relying on the release.

Risk: A learner profile can record recurring errors for a school-age user.

Mitigation: Create or share a profile only with the learner's consent, and honor pause and deletion controls.

## Reference(s):

- [ClawHub release](https://clawhub.ai/qizhitang/skills/xiaozhi-chinese-grammar-tracker)
- [Chinese grammar error library](artifact/references/grammar-error-library.md)
- [Chinese high-school sentence reference](artifact/references/chinese-hs-sentence.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Chinese-language explanations, sentence revisions, and optional plain-text profile exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent profile tracking is consent-based.]

## Skill Version(s):

2.12.7 (source: artifact frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
