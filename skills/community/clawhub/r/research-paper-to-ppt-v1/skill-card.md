## Description: <br>
将指定医学研究论文自动生成 PPTX 汇报文件的技能：先精确定位单篇文献，再读取全文和原文图表，最后按基础研究型汇报大纲生成中文组会风格 PPTX；若无法定位文献或获取全文，则返回检索失败而不编造内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jukiss1](https://clawhub.ai/user/jukiss1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, students, and medical-literature reviewers use this skill to convert a uniquely identified medical research paper into a Chinese PPTX presentation with paper metadata, background, methods, results, original figures, limitations, and take-home messages. It is intended for literature presentation workflows where generated medical claims and figure usage are reviewed before sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded or exposed InfoX-Med credentials could compromise paid or personal access tokens. <br>
Mitigation: Remove embedded credentials, supply tokens only through a controlled environment, and avoid personal or paid credentials until debug-token handling is fixed. <br>
Risk: Debug artifacts may reveal user tokens or sensitive request data. <br>
Mitigation: Disable or redact debug outputs before use and review the workspace for generated token-bearing files after each run. <br>
Risk: Hardcoded medical content can mislead readers or contaminate a presentation for a different paper. <br>
Mitigation: Eliminate hardcoded paper-specific content and manually verify every generated claim, figure source, and citation against the selected paper before presenting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jukiss1/research-paper-to-ppt-v1) <br>
- [Publisher profile](https://clawhub.ai/user/jukiss1) <br>
- [Integration Notes](references/integration-notes.md) <br>
- [Slide Schema](references/slide-schema.md) <br>
- [Figure Caption Policy](references/figure-caption-policy.md) <br>
- [Visual Rendering Spec](references/visual-rendering-spec.md) <br>
- [Output Filename Policy](references/output-filename-policy.md) <br>
- [Release Audit](references/release-audit.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Chinese presentation content, intermediate JSON, shell commands, and generated PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses original paper figures when available; fails closed instead of fabricating unavailable papers, claims, or images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
