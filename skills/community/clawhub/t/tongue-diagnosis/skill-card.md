## Description: <br>
Provides Chinese-language Traditional Chinese Medicine tongue-image observations and structured wellness reports based on uploaded tongue photos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwbwin](https://clawhub.ai/user/wwbwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can request a TCM-style tongue observation report from an uploaded tongue photo, including visible tongue features, a wellness rating, possible areas of concern, and general lifestyle guidance. The skill is informational and must not be used as a medical diagnostic tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake medical-style tongue analysis for clinical diagnosis. <br>
Mitigation: Present results as informational only and direct users with symptoms, persistent concerns, or urgent signs to a licensed clinician. <br>
Risk: Photo-only analysis can be unreliable because lighting, angle, focus, and single-image context affect visible tongue features. <br>
Mitigation: State image-quality limits, request clearer photos when needed, and keep conclusions conservative. <br>
Risk: Disease-specific claims could encourage self-treatment or delayed care. <br>
Mitigation: Do not recommend specific medications, do not rule out illness, and include guidance to seek professional medical advice. <br>


## Reference(s): <br>
- [舌质诊断（舌体）](references/tongue-body.md) <br>
- [舌苔诊断](references/tongue-coating.md) <br>
- [舌下络脉诊法](references/tongue-sublingual.md) <br>
- [舌下络脉诊法（补充知识）](references/sublingual-supplement.md) <br>
- [舌部分区与脏腑对应](references/tongue-zones.md) <br>
- [舌纹诊病（补充知识）](references/tongue-lines-supplement.md) <br>
- [常见证候与舌象对照](references/syndrome-patterns.md) <br>
- [报告输出模板](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured report in Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided tongue photos; outputs should include a medical disclaimer and avoid medication recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
