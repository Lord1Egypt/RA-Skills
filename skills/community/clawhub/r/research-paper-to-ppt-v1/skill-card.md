## Description:

将指定医学研究论文自动生成 PPTX 汇报文件的技能，会在唯一定位论文并获取全文与原文图表后，按基础研究型汇报大纲生成中文组会风格演示文稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jukiss1](https://clawhub.ai/user/jukiss1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and medical researchers use this skill to turn a uniquely identified medical research paper into a Chinese PPTX journal-club or group-meeting presentation. The skill is intended for workflows that can retrieve the full paper and use original paper figures rather than invented images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged scripts may handle InfoX-Med API credentials unsafely.

Mitigation: Remove and rotate embedded tokens, require secrets to be supplied explicitly at runtime, and avoid writing credentials to logs or debug artifacts before installation.

Risk: Generated presentations may include unrelated or hardcoded medical claims.

Mitigation: Remove hardcoded paper-specific claims from renderer and fallback logic, and require generated slide claims to trace to the retrieved full text, figures, or captions.

Risk: Full-paper retrieval and image handling may fetch from unsafe or unintended locations.

Mitigation: Use HTTPS, allowlist the InfoX-Med API host and trusted original-paper asset hosts, and apply download size and time limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jukiss1/skills/research-paper-to-ppt-v1)
- [Integration Notes](artifact/references/integration-notes.md)
- [Basic Research Outline](artifact/references/outline-basic-research.md)
- [Slide Schema](artifact/references/slide-schema.md)
- [Figure Caption Policy](artifact/references/figure-caption-policy.md)
- [Visual Rendering Spec](artifact/references/visual-rendering-spec.md)
- [Output Filename Policy](artifact/references/output-filename-policy.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell commands, intermediate JSON, and generated PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the target paper title for default PPTX filenames and returns a fixed Chinese failure message when the paper cannot be uniquely resolved or full-text evidence is insufficient.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
